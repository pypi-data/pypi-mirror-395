#!/usr/bin/env python3

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# Colors / styling (works even if colorama isn't installed)
# ─────────────────────────────────────────────────────────────
try:
    from colorama import init as colorama_init, Fore, Style as CStyle

    colorama_init(autoreset=True)

    class Color:
        INFO = Fore.CYAN
        OK = Fore.GREEN
        WARN = Fore.YELLOW
        ERR = Fore.RED
        BOLD = CStyle.BRIGHT
        DIM = CStyle.DIM
        RESET = CStyle.RESET_ALL

except ImportError:
    class Color:
        INFO = ""
        OK = ""
        WARN = ""
        ERR = ""
        BOLD = ""
        DIM = ""
        RESET = ""


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────
def print_banner():
    print(f"{Color.BOLD}{Color.INFO}")
    print("┌───────────────────────────────────────────────┐")
    print("│        🧰  Git Setup Anywhere (CLI)          │")
    print("└───────────────────────────────────────────────┘")
    print(Color.RESET, end="")

def run(cmd, check=True, shell=False):
    if isinstance(cmd, (list, tuple)):
        cmd_str = " ".join(cmd)
    else:
        cmd_str = cmd
    print(f"{Color.DIM}[RUN] {cmd_str}{Color.RESET}")
    return subprocess.run(cmd, check=check, shell=shell)

def command_exists(cmd):
    return shutil.which(cmd) is not None

def input_with_default(prompt, default=None):
    if default is not None:
        full = f"{prompt} [{default}]: "
    else:
        full = f"{prompt}: "
    val = input(full).strip()
    return val or (default if default is not None else "")

def choice_menu(prompt, options, default=None):
    """
    options: list of (key, label) like [("1", "Do X"), ("2", "Do Y")]
    default: key or None
    """
    print(prompt)
    for key, label in options:
        dmark = " (default)" if default is not None and key == default else ""
        print(f"  {Color.INFO}{key}{Color.RESET} - {label}{dmark}")
    while True:
        ans = input("> ").strip().lower()
        if not ans and default is not None:
            return default
        for key, _ in options:
            if ans == key.lower():
                return key
        print(f"{Color.WARN}Invalid choice, try again.{Color.RESET}")


# ─────────────────────────────────────────────────────────────
# Git installation per OS
# ─────────────────────────────────────────────────────────────
def install_git_linux():
    print(f"\n{Color.INFO}=== Installing/Updating Git on Linux ==={Color.RESET}")
    if command_exists("git"):
        print(f"{Color.OK}Git already installed. Will try to update using your package manager (if supported).{Color.RESET}")

    if command_exists("apt"):
        print("Using apt...")
        run(["sudo", "apt", "update", "-y"])
        run(["sudo", "apt", "install", "-y", "git"])
    elif command_exists("dnf"):
        print("Using dnf...")
        run(["sudo", "dnf", "install", "-y", "git"])
    elif command_exists("yum"):
        print("Using yum...")
        run(["sudo", "yum", "install", "-y", "git"])
    elif command_exists("pacman"):
        print("Using pacman...")
        run(["sudo", "pacman", "-Sy", "--noconfirm", "git"])
    elif command_exists("zypper"):
        print("Using zypper...")
        run(["sudo", "zypper", "install", "-y", "git"])
    else:
        print(f"{Color.ERR}❌ No supported package manager found (apt/dnf/yum/pacman/zypper).{Color.RESET}")
        print("Install Git manually and re-run this script.")
        sys.exit(1)


def install_git_macos():
    print(f"\n{Color.INFO}=== Installing/Updating Git on macOS ==={Color.RESET}")
    if command_exists("git"):
        print(f"{Color.OK}Git already installed. Using Homebrew to ensure it's present/up-to-date.{Color.RESET}")

    if not command_exists("brew"):
        print(f"{Color.WARN}Homebrew not found.{Color.RESET}")
        ch = choice_menu(
            "Install Homebrew automatically?",
            [("y", "Yes, install Homebrew"), ("n", "No, I'll handle it myself and rerun script")],
            default="y",
        )
        if ch == "n":
            print("Install Homebrew from https://brew.sh and rerun this script.")
            sys.exit(1)

        try:
            run('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"', shell=True)
            print(f"{Color.OK}✅ Homebrew installed.{Color.RESET}")
        except subprocess.CalledProcessError:
            print(f"{Color.ERR}❌ Failed to install Homebrew automatically.{Color.RESET}")
            sys.exit(1)

    print("Installing Git via Homebrew...")
    run(["brew", "install", "git"])


def install_git_windows():
    print(f"\n{Color.INFO}=== Installing/Updating Git on Windows ==={Color.RESET}")
    if not command_exists("winget"):
        print(f"{Color.ERR}❌ winget is not available.{Color.RESET}")
        print("Install Git manually from https://git-scm.com/download/win and rerun this script.")
        sys.exit(1)

    if command_exists("git"):
        print(f"{Color.OK}Git already installed. Using winget upgrade to ensure it's up-to-date.{Color.RESET}")
        run(["winget", "upgrade", "--id", "Git.Git", "-e", "--source", "winget"], check=False)
    else:
        print("Git not detected. Installing with winget...")
        run(["winget", "install", "--id", "Git.Git", "-e", "--source", "winget"])


def detect_os_and_handle_git():
    system = platform.system()
    print(f"{Color.INFO}Detected OS: {system}{Color.RESET}")

    git_exists = command_exists("git")
    git_version = None
    if git_exists:
        try:
            git_version = subprocess.check_output(["git", "--version"], text=True).strip()
        except subprocess.CalledProcessError:
            git_version = None

    if git_version:
        print(f"{Color.OK}Current Git: {git_version}{Color.RESET}")
        choice = choice_menu(
            "What do you want to do with Git?",
            [
                ("1", "Keep current Git, do NOT attempt install/update"),
                ("2", "Try to install/update Git using system package manager")
            ],
            default="2",
        )
        if choice == "1":
            print(f"{Color.INFO}Skipping Git install/update.{Color.RESET}")
        else:
            if system == "Linux":
                install_git_linux()
            elif system == "Darwin":
                install_git_macos()
            elif system == "Windows":
                install_git_windows()
            else:
                print(f"{Color.ERR}❌ Unsupported OS: {system}{Color.RESET}")
                sys.exit(1)
    else:
        print(f"{Color.WARN}Git is not installed or not working.{Color.RESET}")
        choice = choice_menu(
            "Install Git now?",
            [("y", "Yes, install Git"), ("n", "No, exit")],
            default="y",
        )
        if choice == "n":
            print("Cannot continue without Git. Exiting.")
            sys.exit(1)
        if system == "Linux":
            install_git_linux()
        elif system == "Darwin":
            install_git_macos()
        elif system == "Windows":
            install_git_windows()
        else:
            print(f"{Color.ERR}❌ Unsupported OS: {system}{Color.RESET}")
            sys.exit(1)

    print(f"\n{Color.INFO}=== Verifying Git ==={Color.RESET}")
    try:
        run(["git", "--version"])
    except subprocess.CalledProcessError:
        print(f"{Color.ERR}❌ Git still not working after installation.{Color.RESET}")
        sys.exit(1)


# ─────────────────────────────────────────────────────────────
# Git config
# ─────────────────────────────────────────────────────────────
def get_git_config(key):
    try:
        out = subprocess.check_output(["git", "config", "--global", key], text=True).strip()
        return out if out else None
    except subprocess.CalledProcessError:
        return None

def configure_git_user():
    print(f"\n{Color.INFO}=== Git User Configuration ==={Color.RESET}")

    existing_name = get_git_config("user.name")
    existing_email = get_git_config("user.email")

    if existing_name or existing_email:
        print(f"{Color.WARN}Existing global Git config detected:{Color.RESET}")
        if existing_name:
            print(f"  user.name  = {Color.OK}{existing_name}{Color.RESET}")
        if existing_email:
            print(f"  user.email = {Color.OK}{existing_email}{Color.RESET}")

        choice = choice_menu(
            "How do you want to proceed?",
            [
                ("1", "Keep existing values"),
                ("2", "Edit / overwrite them"),
            ],
            default="2",
        )
        if choice == "1":
            print(f"{Color.OK}Keeping existing Git user config.{Color.RESET}")
            return existing_email or ""
    else:
        print("No existing global Git user config found.")

    # Ask for new values
    git_username = input_with_default("Enter your Git username", existing_name or None).strip()
    git_email = input_with_default("Enter your Git email", existing_email or None).strip()

    if not git_username or not git_email:
        print(f"{Color.ERR}❌ Username or email empty. Aborting.{Color.RESET}")
        sys.exit(1)

    run(["git", "config", "--global", "user.name", git_username])
    run(["git", "config", "--global", "user.email", git_email])

    # Defaults
    run(["git", "config", "--global", "init.defaultBranch", "main"])
    run(["git", "config", "--global", "color.ui", "auto"])
    run(["git", "config", "--global", "core.editor", "nano"])

    print(f"\n{Color.OK}✅ Git user configuration saved.{Color.RESET}")
    print(f"\n{Color.INFO}=== Current Global Git Config ==={Color.RESET}")
    run(["git", "config", "--list"])

    return git_email


# ─────────────────────────────────────────────────────────────
# SSH key generation
# ─────────────────────────────────────────────────────────────
def ssh_menu(existing_key, email):
    print(f"\n{Color.INFO}=== SSH Key Setup ==={Color.RESET}")

    if existing_key:
        print(f"{Color.WARN}Existing SSH key detected: {existing_key}{Color.RESET}")
        options = [
            ("1", "Show existing public key"),
            ("2", "Generate a NEW key (overwrite existing)"),
            ("3", "Skip SSH setup"),
        ]
        choice = choice_menu("Choose an option:", options, default="1")
        return choice
    else:
        options = [
            ("1", "Generate a new SSH key"),
            ("2", "Skip SSH setup"),
        ]
        choice = choice_menu("No SSH key found. Choose an option:", options, default="1")
        return choice


def generate_or_show_ssh_key(git_email):
    home = Path.home()
    ssh_dir = home / ".ssh"
    ssh_dir.mkdir(parents=True, exist_ok=True)
    key_file = ssh_dir / "id_ed25519"
    pub_key_file = key_file.with_suffix(".pub")

    existing_key = key_file if key_file.exists() else None
    choice = ssh_menu(existing_key, git_email)

    if existing_key and choice == "1":
        if pub_key_file.exists():
            print(f"\n{Color.INFO}=== Existing SSH Public Key ==={Color.RESET}")
            print(pub_key_file.read_text())
            print(f"\nAdd this to your Git provider (e.g. GitHub → Settings → SSH and GPG keys).")
        else:
            print(f"{Color.ERR}Public key file not found, but private key exists. You may need to regenerate it.{Color.RESET}")
        return

    if (existing_key and choice == "3") or (not existing_key and choice == "2"):
        print(f"{Color.WARN}Skipping SSH key generation.{Color.RESET}")
        return

    # At this point: generate new key
    print(f"\n{Color.INFO}Generating new ed25519 SSH key...{Color.RESET}")
    if existing_key:
        print(f"{Color.WARN}This will overwrite: {key_file}{Color.RESET}")

    cmd = [
        "ssh-keygen",
        "-t",
        "ed25519",
        "-C",
        git_email,
        "-f",
        str(key_file),
        "-N",
        "",
    ]

    try:
        run(cmd)
    except FileNotFoundError:
        print(f"{Color.ERR}❌ ssh-keygen not found. Install OpenSSH tools and re-run this step.{Color.RESET}")
        return

    system = platform.system()
    # Best-effort ssh-agent handling
    if system in ("Linux", "Darwin"):
        try:
            print(f"{Color.DIM}Starting ssh-agent and adding key...{Color.RESET}")
            agent_output = subprocess.check_output(["ssh-agent", "-s"], text=True)
            for line in agent_output.splitlines():
                if "SSH_AUTH_SOCK" in line or "SSH_AGENT_PID" in line:
                    parts = line.split(";")[0]
                    key, value = parts.split("=", 1)
                    os.environ[key] = value
            run(["ssh-add", str(key_file)], check=False)
        except Exception as e:
            print(f"{Color.WARN}Could not add key to ssh-agent automatically: {e}{Color.RESET}")
    elif system == "Windows":
        print(f"{Color.DIM}Attempting to add key with ssh-add on Windows...{Color.RESET}")
        try:
            run(["ssh-add", str(key_file)], check=False)
        except Exception as e:
            print(f"{Color.WARN}Could not add key to ssh-agent automatically: {e}{Color.RESET}")

    if pub_key_file.exists():
        print(f"\n{Color.OK}✅ SSH key generated successfully.{Color.RESET}")
        print(f"\n{Color.INFO}=== Your SSH Public Key ==={Color.RESET}")
        print(pub_key_file.read_text())
        print(
            f"\nCopy this key and add it to your Git provider "
            f"(e.g. GitHub → Settings → SSH and GPG keys → New SSH key)."
        )
    else:
        print(f"{Color.ERR}❌ Public key file not found, something went wrong.{Color.RESET}")


# ─────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────
def main():
    print_banner()
    print(f"{Color.INFO}This will help you install Git, configure it, and set up SSH for Git hosting.{Color.RESET}")
    print()

    detect_os_and_handle_git()
    git_email = configure_git_user()
    generate_or_show_ssh_key(git_email)

    print(f"\n{Color.OK}{Color.BOLD}🚀 All done. Your Git environment is ready.{Color.RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Color.WARN}Interrupted by user. Exiting.{Color.RESET}")
        sys.exit(1)
