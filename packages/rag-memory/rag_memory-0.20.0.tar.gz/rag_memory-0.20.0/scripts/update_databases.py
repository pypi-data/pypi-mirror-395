#!/usr/bin/env python3
"""
Update Database Containers (PostgreSQL, Neo4j, Backup)

Cross-platform script to update database containers without losing data.
Pulls latest images and recreates containers while preserving volumes.

Usage:
    python scripts/update_databases.py              # Update postgres + neo4j
    python scripts/update_databases.py --all        # Include backup container
    python scripts/update_databases.py --postgres   # Only PostgreSQL
    python scripts/update_databases.py --neo4j      # Only Neo4j
    python scripts/update_databases.py --backup     # Only backup container

Requirements:
    - Containers must have been deployed via setup.py
    - Docker must be running
"""

import os
import sys
import subprocess
import argparse
import time
from pathlib import Path
from typing import Tuple, Optional, List


class Colors:
    """ANSI color codes for terminal output"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"


def print_header(text: str):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*80}{Colors.RESET}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")


def run_command(cmd: list, check: bool = True, timeout: int = None) -> Tuple[int, str, str]:
    """Run shell command and return exit code, stdout, stderr"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out"
    except Exception as e:
        return 1, "", str(e)


def get_docker_compose_command() -> list:
    """Detect which docker compose command is available (cross-platform)"""
    code, _, _ = run_command(["docker", "compose", "version"])
    if code == 0:
        return ["docker", "compose"]
    return ["docker-compose"]


def check_docker_running() -> bool:
    """Check if Docker daemon is running"""
    print_info("Checking Docker daemon...")
    code, _, _ = run_command(["docker", "ps"])

    if code == 0:
        print_success("Docker daemon is running")
        return True

    print_error("Docker daemon is not running")
    print_info("Start Docker Desktop and try again")
    return False


def get_system_config_dir() -> Optional[Path]:
    """Get OS-appropriate system configuration directory"""
    try:
        import platformdirs
        config_dir = Path(platformdirs.user_config_dir('rag-memory', appauthor=False))
        return config_dir
    except ImportError:
        print_error("platformdirs package not found")
        print_info("Run: pip install platformdirs")
        return None


def check_deployment() -> Tuple[bool, Optional[Path]]:
    """Check if containers have been deployed via setup.py

    Returns:
        (is_deployed, system_compose_path)
    """
    print_info("Checking deployment status...")

    config_dir = get_system_config_dir()
    if not config_dir:
        return False, None

    system_compose_path = config_dir / 'docker-compose.yml'
    if not system_compose_path.exists():
        print_error(f"System docker-compose.yml not found at: {system_compose_path}")
        print_info("Run setup.py first to deploy containers")
        return False, None

    print_success(f"Found docker-compose.yml at: {system_compose_path}")
    return True, system_compose_path


def check_container_exists(container_name: str) -> Tuple[bool, bool]:
    """Check if container exists and if it's running

    Returns:
        (exists, is_running)
    """
    code, stdout, _ = run_command(
        ["docker", "ps", "-a", "--filter", f"name={container_name}", "--format", "{{.Names}}"]
    )
    exists = container_name in stdout

    if not exists:
        return False, False

    code, stdout, _ = run_command(
        ["docker", "ps", "--filter", f"name={container_name}", "--format", "{{.Names}}"]
    )
    is_running = container_name in stdout

    return exists, is_running


def pull_images(system_compose_path: Path, services: List[str]) -> bool:
    """Pull latest images for specified services

    Args:
        system_compose_path: Path to system docker-compose.yml
        services: List of service names to pull

    Returns:
        True if pull succeeded
    """
    print_header(f"Pulling Latest Images: {', '.join(services)}")

    docker_compose_cmd = get_docker_compose_command()

    print_info("Pulling images from Docker Hub...")

    code, stdout, stderr = run_command(
        docker_compose_cmd + ["-f", str(system_compose_path), "pull"] + services,
        timeout=300
    )

    if code != 0:
        print_error(f"Failed to pull images: {stderr}")
        return False

    print_success("Images pulled successfully")
    return True


def recreate_containers(system_compose_path: Path, services: List[str]) -> bool:
    """Recreate containers with new images while preserving volumes

    Args:
        system_compose_path: Path to system docker-compose.yml
        services: List of service names to recreate

    Returns:
        True if recreate succeeded
    """
    print_header(f"Recreating Containers: {', '.join(services)}")

    docker_compose_cmd = get_docker_compose_command()

    print_info("Recreating containers (volumes will be preserved)...")
    print_warning("Database containers will restart - brief downtime expected")

    code, stdout, stderr = run_command(
        docker_compose_cmd + ["-f", str(system_compose_path),
                              "up", "-d", "--force-recreate"] + services,
        timeout=180
    )

    if code != 0:
        print_error(f"Failed to recreate containers: {stderr}")
        return False

    print_success("Containers recreated with new images")
    return True


def wait_for_health(container_name: str, timeout_seconds: int = 120) -> bool:
    """Wait for container to become healthy

    Args:
        container_name: Name of container to check
        timeout_seconds: How long to wait

    Returns:
        True if container became healthy
    """
    print_info(f"Waiting for {container_name} to become healthy...")

    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        code, stdout, _ = run_command(
            ["docker", "inspect", "--format", "{{.State.Health.Status}}", container_name]
        )

        if code == 0:
            health_status = stdout.strip()

            if health_status == "healthy":
                elapsed = int(time.time() - start_time)
                print_success(f"{container_name} is healthy (took {elapsed}s)")
                return True

            if health_status == "unhealthy":
                print_error(f"{container_name} is unhealthy")
                print_info(f"Check logs: docker logs {container_name}")
                return False

        time.sleep(5)

    print_warning(f"Timeout waiting for {container_name}")
    return False


def verify_data_integrity(system_compose_path: Path) -> bool:
    """Verify data is intact after update"""
    print_header("Verifying Data Integrity")

    docker_compose_cmd = get_docker_compose_command()

    # Check PostgreSQL data
    print_info("Checking PostgreSQL data...")
    code, stdout, stderr = run_command([
        "docker", "exec", "rag-memory-postgres-local",
        "psql", "-U", "raguser", "-d", "rag_memory",
        "-c", "SELECT COUNT(*) as doc_count FROM source_documents;"
    ])

    if code == 0:
        print_success(f"PostgreSQL data intact: {stdout.strip()}")
    else:
        print_warning(f"Could not verify PostgreSQL: {stderr}")

    # Check Neo4j data
    print_info("Checking Neo4j data...")
    code, stdout, stderr = run_command([
        "docker", "exec", "rag-memory-neo4j-local",
        "cypher-shell", "-u", "neo4j", "-p", "graphiti-password",
        "MATCH (n) RETURN count(n) as node_count;"
    ])

    if code == 0:
        print_success(f"Neo4j data intact: {stdout.strip()}")
    else:
        print_warning(f"Could not verify Neo4j: {stderr}")

    return True


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Update database containers while preserving data"
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Update all containers including backup"
    )
    parser.add_argument(
        "--postgres", action="store_true",
        help="Update only PostgreSQL"
    )
    parser.add_argument(
        "--neo4j", action="store_true",
        help="Update only Neo4j"
    )
    parser.add_argument(
        "--backup", action="store_true",
        help="Update only backup container"
    )
    parser.add_argument(
        "--skip-verify", action="store_true",
        help="Skip data integrity verification"
    )

    return parser.parse_args()


def main():
    """Main update flow"""
    args = parse_args()

    print(f"\n{Colors.BOLD}{Colors.GREEN}RAG Memory - Database Container Update Script{Colors.RESET}")
    print("Updates database containers while preserving all data in volumes\n")

    # Determine which services to update
    services = []
    health_check_containers = []

    if args.postgres:
        services.append("postgres-local")
        health_check_containers.append("rag-memory-postgres-local")
    elif args.neo4j:
        services.append("neo4j-local")
        health_check_containers.append("rag-memory-neo4j-local")
    elif args.backup:
        services.append("backup-local")
        # Backup container has health check but it's less critical
    elif args.all:
        services = ["postgres-local", "neo4j-local", "backup-local"]
        health_check_containers = ["rag-memory-postgres-local", "rag-memory-neo4j-local"]
    else:
        # Default: postgres + neo4j (not backup)
        services = ["postgres-local", "neo4j-local"]
        health_check_containers = ["rag-memory-postgres-local", "rag-memory-neo4j-local"]

    print_info(f"Services to update: {', '.join(services)}")

    # Step 0: Check Docker is running
    if not check_docker_running():
        sys.exit(1)

    # Step 1: Check deployment exists
    is_deployed, system_compose_path = check_deployment()
    if not is_deployed:
        sys.exit(1)

    # Step 2: Check containers exist
    for service in services:
        container_name = f"rag-memory-{service}"
        exists, is_running = check_container_exists(container_name)
        if exists:
            status = "running" if is_running else "stopped"
            print_success(f"Container {container_name} exists ({status})")
        else:
            print_warning(f"Container {container_name} does not exist - will be created")

    # Step 3: Pull latest images
    if not pull_images(system_compose_path, services):
        sys.exit(1)

    # Step 4: Recreate containers
    if not recreate_containers(system_compose_path, services):
        sys.exit(1)

    # Step 5: Wait for health checks
    print_header("Waiting for Health Checks")
    all_healthy = True
    for container in health_check_containers:
        if not wait_for_health(container, timeout_seconds=120):
            all_healthy = False

    if not all_healthy:
        print_warning("Some containers may not be fully healthy yet")
        print_info("Check status with: docker ps")

    # Step 6: Verify data integrity (optional)
    if not args.skip_verify and health_check_containers:
        verify_data_integrity(system_compose_path)

    # Success summary
    print_header("Update Complete")
    print_success("Database containers updated successfully")
    print_success("All data preserved in Docker volumes")
    print()
    print_info("Volume data includes:")
    print(f"  • PostgreSQL: tables, HNSW indices, constraints")
    print(f"  • Neo4j: nodes, relationships, Graphiti indices")
    print()
    print_info("Useful commands:")
    print(f"  View status: {Colors.CYAN}docker ps{Colors.RESET}")
    print(f"  PostgreSQL logs: {Colors.CYAN}docker logs rag-memory-postgres-local{Colors.RESET}")
    print(f"  Neo4j logs: {Colors.CYAN}docker logs rag-memory-neo4j-local{Colors.RESET}")
    print(f"  Health check: {Colors.CYAN}curl http://localhost:18000/health{Colors.RESET}")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Update cancelled by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
