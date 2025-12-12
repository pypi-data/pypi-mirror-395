#!/usr/bin/env python3
"""
Update MCP Server Container

Cross-platform script to rebuild and restart only the MCP server container
without affecting PostgreSQL or Neo4j databases.

Usage:
    python scripts/update_mcp.py

Requirements:
    - MCP container must have been deployed via setup.py
    - Docker must be running
    - Run from the rag-memory repository root
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Tuple, Optional


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
    """Detect which docker compose command is available (cross-platform)

    Modern Docker Desktop uses 'docker compose' (space)
    Older installations use 'docker-compose' (hyphen)
    """
    # Try new format first (docker compose)
    code, _, _ = run_command(["docker", "compose", "version"])
    if code == 0:
        return ["docker", "compose"]
    # Fall back to old format (docker-compose)
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


def check_container_exists(container_name: str) -> Tuple[bool, bool]:
    """Check if container exists and if it's running

    Returns:
        (exists, is_running)
    """
    # Check if container exists (running or stopped)
    code, stdout, _ = run_command(["docker", "ps", "-a", "--filter", f"name={container_name}", "--format", "{{.Names}}"])
    exists = container_name in stdout

    if not exists:
        return False, False

    # Check if it's running
    code, stdout, _ = run_command(["docker", "ps", "--filter", f"name={container_name}", "--format", "{{.Names}}"])
    is_running = container_name in stdout

    return exists, is_running


def check_mcp_deployment() -> Tuple[bool, Path, Path]:
    """Check if MCP has been deployed via setup.py

    Returns:
        (is_deployed, system_compose_path, repo_compose_path)
    """
    print_info("Checking MCP deployment status...")

    # Get system config directory
    config_dir = get_system_config_dir()
    if not config_dir:
        return False, None, None

    # Check if system docker-compose.yml exists
    system_compose_path = config_dir / 'docker-compose.yml'
    if not system_compose_path.exists():
        print_error(f"System docker-compose.yml not found at: {system_compose_path}")
        print_info("Run setup.py first to deploy the MCP server")
        return False, None, None

    # Check if repo docker-compose.yml exists
    project_root = Path(__file__).parent.parent
    repo_compose_path = project_root / 'deploy' / 'docker' / 'compose' / 'docker-compose.yml'
    if not repo_compose_path.exists():
        print_error(f"Repo docker-compose.yml not found at: {repo_compose_path}")
        print_info("Run setup.py first to generate docker-compose.yml")
        return False, None, None

    # Check if MCP container exists
    container_name = "rag-memory-mcp-local"
    exists, is_running = check_container_exists(container_name)

    if not exists:
        print_warning(f"Container '{container_name}' does not exist")
        print_info("Run setup.py first to create the MCP container")
        return False, None, None

    status = "running" if is_running else "stopped"
    print_success(f"MCP container exists and is {status}")

    return True, system_compose_path, repo_compose_path


def rebuild_mcp_image(repo_compose_path: Path) -> bool:
    """Rebuild the MCP Docker image from source code

    Args:
        repo_compose_path: Path to repo docker-compose.yml (has build context)

    Returns:
        True if build succeeded
    """
    print_header("Step 1: Rebuilding MCP Image")

    docker_compose_cmd = get_docker_compose_command()

    print_info("Building MCP server image from latest code...")
    print_info(f"Using: {repo_compose_path}")

    code, stdout, stderr = run_command(
        docker_compose_cmd + ["-f", str(repo_compose_path),
                              "build", "rag-mcp-local"],
        timeout=600
    )

    if code != 0:
        print_error(f"Failed to build MCP image: {stderr}")
        return False

    print_success("MCP image rebuilt successfully")
    return True


def restart_mcp_container(system_compose_path: Path) -> bool:
    """Restart only the MCP container without affecting databases

    Args:
        system_compose_path: Path to system docker-compose.yml

    Returns:
        True if restart succeeded
    """
    print_header("Step 2: Restarting MCP Container")

    docker_compose_cmd = get_docker_compose_command()

    print_info("Restarting MCP container (databases will NOT be affected)...")
    print_info(f"Using: {system_compose_path}")

    # Use --no-deps to prevent restarting postgres-local and neo4j-local
    # Use --force-recreate to ensure container picks up new image
    code, stdout, stderr = run_command(
        docker_compose_cmd + ["-f", str(system_compose_path),
                              "up", "-d", "--no-deps", "--force-recreate", "rag-mcp-local"],
        timeout=120
    )

    if code != 0:
        print_error(f"Failed to restart MCP container: {stderr}")
        return False

    print_success("MCP container restarted with updated code")
    return True


def verify_mcp_health(timeout_seconds: int = 60) -> bool:
    """Wait for MCP container to become healthy

    Args:
        timeout_seconds: How long to wait for health check

    Returns:
        True if container became healthy
    """
    print_header("Step 3: Verifying MCP Health")

    import time

    container_name = "rag-memory-mcp-local"
    print_info(f"Waiting up to {timeout_seconds}s for MCP to become healthy...")

    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        code, stdout, _ = run_command(
            ["docker", "inspect", "--format", "{{.State.Health.Status}}", container_name]
        )

        if code == 0:
            health_status = stdout.strip()

            if health_status == "healthy":
                elapsed = int(time.time() - start_time)
                print_success(f"MCP container is healthy (took {elapsed}s)")
                return True

            print_info(f"Health status: {health_status}, waiting...")

        time.sleep(5)

    print_warning("Health check timeout - container may still be starting")
    print_info("Check logs with: docker logs rag-memory-mcp-local")
    return False


def main():
    """Main update flow"""
    print(f"\n{Colors.BOLD}{Colors.GREEN}RAG Memory - MCP Server Update Script{Colors.RESET}")
    print("Updates only the MCP container, databases are not affected\n")

    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    print_info(f"Working directory: {project_root}")

    # Step 0: Check Docker is running
    if not check_docker_running():
        sys.exit(1)

    # Step 1: Check MCP deployment exists
    is_deployed, system_compose_path, repo_compose_path = check_mcp_deployment()
    if not is_deployed:
        sys.exit(1)

    # Step 2: Rebuild MCP image from repo
    if not rebuild_mcp_image(repo_compose_path):
        sys.exit(1)

    # Step 3: Restart MCP container from system compose
    if not restart_mcp_container(system_compose_path):
        sys.exit(1)

    # Step 4: Verify health
    verify_mcp_health(timeout_seconds=60)

    # Success summary
    print_header("Update Complete")
    print_success("MCP server has been updated with your latest code changes")
    print_info("PostgreSQL and Neo4j containers were not affected")
    print()
    print_info("Useful commands:")
    print(f"  View logs: {Colors.CYAN}docker logs -f rag-memory-mcp-local{Colors.RESET}")
    print(f"  Check status: {Colors.CYAN}docker ps{Colors.RESET}")
    print(f"  Health check: {Colors.CYAN}curl http://localhost:8000/health{Colors.RESET}")
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
