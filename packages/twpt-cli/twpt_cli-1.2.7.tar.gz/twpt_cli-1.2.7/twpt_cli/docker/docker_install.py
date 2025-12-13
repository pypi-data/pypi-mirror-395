"""Docker installation management for Linux systems."""

import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Optional, Tuple

import distro
from rich.console import Console

console = Console()


def is_docker_installed() -> bool:
    """Check if Docker is installed and accessible.

    Returns:
        True if Docker is installed and running, False otherwise
    """
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def detect_linux_distro() -> Tuple[str, str]:
    """Detect the Linux distribution.

    Returns:
        Tuple of (distro_name, distro_version)
    """
    # Use the distro library for reliable detection
    dist_id = distro.id().lower()
    dist_version = distro.version()

    # Map distro IDs to our categories
    distro_map = {
        'kali': 'kali',
        'ubuntu': 'debian',
        'debian': 'debian',
        'linuxmint': 'debian',
        'pop': 'debian',
        'elementary': 'debian',
        'fedora': 'fedora',
        'centos': 'rhel',
        'rhel': 'rhel',
        'redhat': 'rhel',
        'rocky': 'rhel',
        'almalinux': 'rhel',
        'oracle': 'rhel',
        'arch': 'arch',
        'manjaro': 'arch',
        'endeavouros': 'arch',
        'opensuse': 'opensuse',
        'suse': 'opensuse',
        'opensuse-leap': 'opensuse',
        'opensuse-tumbleweed': 'opensuse',
    }

    distro_type = distro_map.get(dist_id, 'unknown')
    return (distro_type, dist_version)


def get_architecture() -> str:
    """Get system architecture.

    Returns:
        Architecture string (amd64, arm64, armhf)
    """
    machine = platform.machine().lower()

    arch_map = {
        'x86_64': 'amd64',
        'amd64': 'amd64',
        'aarch64': 'arm64',
        'arm64': 'arm64',
        'armv7l': 'armhf',
        'armv6l': 'armhf',
    }

    return arch_map.get(machine, machine)


def run_command(cmd: str, check: bool = True) -> bool:
    """Run a shell command with sudo if needed.

    Args:
        cmd: Command to run
        check: Whether to check return code

    Returns:
        True if successful, False otherwise
    """
    try:
        # Check if we need sudo
        if os.geteuid() != 0:
            cmd = f"sudo {cmd}"

        console.print(f"Running: {cmd}", style="dim")
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=False,
            text=True
        )

        if check and result.returncode != 0:
            return False
        return True

    except subprocess.SubprocessError as e:
        console.print(f"✗ Command failed: {e}", style="red")
        return False


def install_docker_kali() -> bool:
    """Install Docker on Kali Linux."""
    console.print("Installing Docker on Kali Linux...", style="blue")

    commands = [
        "apt-get update",
        "apt-get install -y ca-certificates curl gnupg",
        "install -m 0755 -d /etc/apt/keyrings",
        "curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg",
        "chmod a+r /etc/apt/keyrings/docker.gpg",
        'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] '
        'https://download.docker.com/linux/debian bookworm stable" > /etc/apt/sources.list.d/docker.list',
        "apt-get update",
        "apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin",
    ]

    for cmd in commands:
        if not run_command(cmd):
            return False

    return post_install_setup()


def install_docker_debian() -> bool:
    """Install Docker on Debian/Ubuntu."""
    console.print("Installing Docker on Debian/Ubuntu...", style="blue")

    # Detect codename
    codename = distro.codename()
    if not codename:
        # Fallback to lsb_release
        try:
            result = subprocess.run(
                ["lsb_release", "-cs"],
                capture_output=True,
                text=True
            )
            codename = result.stdout.strip()
        except:
            codename = "bookworm"  # Default fallback

    arch = get_architecture()

    commands = [
        "apt-get update",
        "apt-get install -y ca-certificates curl gnupg",
        "install -m 0755 -d /etc/apt/keyrings",
        "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg",
        "chmod a+r /etc/apt/keyrings/docker.gpg",
        f'echo "deb [arch={arch} signed-by=/etc/apt/keyrings/docker.gpg] '
        f'https://download.docker.com/linux/ubuntu {codename} stable" > /etc/apt/sources.list.d/docker.list',
        "apt-get update",
        "apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin",
    ]

    for cmd in commands:
        if not run_command(cmd):
            return False

    return post_install_setup()


def install_docker_fedora() -> bool:
    """Install Docker on Fedora."""
    console.print("Installing Docker on Fedora...", style="blue")

    commands = [
        "dnf -y install dnf-plugins-core",
        "dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo",
        "dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin",
    ]

    for cmd in commands:
        if not run_command(cmd):
            return False

    return post_install_setup()


def install_docker_rhel() -> bool:
    """Install Docker on RHEL/CentOS/Rocky/AlmaLinux."""
    console.print("Installing Docker on RHEL-based system...", style="blue")

    # Detect package manager
    pkg_manager = "dnf" if subprocess.call(["which", "dnf"], stdout=subprocess.DEVNULL) == 0 else "yum"

    commands = [
        f"{pkg_manager} install -y yum-utils",
        f"{pkg_manager}-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo",
        f"{pkg_manager} install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin",
    ]

    for cmd in commands:
        if not run_command(cmd):
            return False

    return post_install_setup()


def install_docker_arch() -> bool:
    """Install Docker on Arch Linux/Manjaro."""
    console.print("Installing Docker on Arch-based system...", style="blue")

    commands = [
        "pacman -Sy --noconfirm docker docker-compose",
    ]

    for cmd in commands:
        if not run_command(cmd):
            return False

    return post_install_setup()


def install_docker_opensuse() -> bool:
    """Install Docker on openSUSE."""
    console.print("Installing Docker on openSUSE...", style="blue")

    commands = [
        "zypper refresh",
        "zypper install -y docker docker-compose",
    ]

    for cmd in commands:
        if not run_command(cmd):
            return False

    return post_install_setup()


def post_install_setup() -> bool:
    """Perform post-installation setup for Docker."""
    console.print("Configuring Docker...", style="blue")

    # Enable and start Docker service
    commands = [
        "systemctl enable docker",
        "systemctl start docker",
    ]

    for cmd in commands:
        if not run_command(cmd, check=False):
            console.print(f"Warning: {cmd} failed", style="yellow")

    # Add current user to docker group (if not root)
    if os.geteuid() != 0:
        username = os.environ.get('USER', 'user')
        if run_command(f"usermod -aG docker {username}", check=False):
            console.print(
                f"✓ User {username} added to docker group. "
                "You may need to log out and back in for this to take effect.",
                style="green"
            )

    return True


def install_docker_if_needed() -> bool:
    """Install Docker if not already installed.

    Returns:
        True if Docker is installed (or was successfully installed), False otherwise
    """
    # Check if Docker is already installed
    if is_docker_installed():
        console.print("✓ Docker is already installed", style="green")
        return True

    # Check if running on Linux
    if platform.system() != "Linux":
        console.print(
            f"✗ Docker installation is only supported on Linux. "
            f"Current platform: {platform.system()}",
            style="red"
        )
        console.print(
            "Please install Docker manually: https://docs.docker.com/get-docker/",
            style="yellow"
        )
        return False

    # Detect distribution
    distro_type, distro_version = detect_linux_distro()

    console.print(f"Detected distribution: {distro_type} {distro_version}", style="blue")

    # Install based on distribution
    install_functions = {
        'kali': install_docker_kali,
        'debian': install_docker_debian,
        'fedora': install_docker_fedora,
        'rhel': install_docker_rhel,
        'arch': install_docker_arch,
        'opensuse': install_docker_opensuse,
    }

    install_func = install_functions.get(distro_type)

    if not install_func:
        console.print(
            f"✗ Unsupported distribution: {distro_type}",
            style="red"
        )
        console.print(
            "Please install Docker manually: https://docs.docker.com/get-docker/",
            style="yellow"
        )
        return False

    # Prompt user for confirmation
    console.print(
        f"\n⚠ This will install Docker on your system.",
        style="yellow bold"
    )
    response = console.input("Do you want to continue? [y/N]: ")

    if response.lower() != 'y':
        console.print("Installation cancelled", style="yellow")
        return False

    # Run installation
    success = install_func()

    if success:
        console.print("\n✓ Docker installed successfully!", style="green bold")
        # Verify installation
        if is_docker_installed():
            console.print("✓ Docker is running correctly", style="green")
            return True
        else:
            console.print(
                "⚠ Docker installed but not running. Try: sudo systemctl start docker",
                style="yellow"
            )
            return False
    else:
        console.print("\n✗ Docker installation failed", style="red")
        return False