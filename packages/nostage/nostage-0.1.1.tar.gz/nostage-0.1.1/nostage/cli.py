"""Command-line interface for NoStage."""

import click
import sys
from colorama import Fore, Style, init
from pathlib import Path
from .config import NoStageConfig
from .hook import install_hook, uninstall_hook, run_pre_commit_hook

# Initialize colorama
init(autoreset=True)


@click.group()
@click.version_option(version="0.1.1")
def main():
    """🛡️  NoStage - Protect files from accidental commits.
    
    NoStage helps you mark specific files or patterns that should never
    be committed, even when you use 'git add .'. Perfect for temporary
    debug files, experimental code, and personal workflow files.
    """
    pass


@main.command()
@click.argument('files', nargs=-1, required=True)
def add(files):
    """Add files to the protection list.
    
    Examples:
        nostage add debug.js test-output.txt
        nostage add scratch/*.py
    """
    try:
        config = NoStageConfig()
        added = []
        already_added = []
        
        for filepath in files:
            if config.add_file(filepath):
                added.append(filepath)
            else:
                already_added.append(filepath)
        
        if added:
            print(f"{Fore.GREEN}✓ Protected {len(added)} file(s):{Style.RESET_ALL}")
            for f in added:
                print(f"  • {f}")
        
        if already_added:
            print(f"{Fore.YELLOW}⚠ Already protected:{Style.RESET_ALL}")
            for f in already_added:
                print(f"  • {f}")
        
    except RuntimeError as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(1)


@main.command()
@click.argument('files', nargs=-1, required=True)
def remove(files):
    """Remove files from the protection list.
    
    Examples:
        nostage remove debug.js
    """
    try:
        config = NoStageConfig()
        removed = []
        not_found = []
        
        for filepath in files:
            if config.remove_file(filepath):
                removed.append(filepath)
            else:
                not_found.append(filepath)
        
        if removed:
            print(f"{Fore.GREEN}✓ Unprotected {len(removed)} file(s):{Style.RESET_ALL}")
            for f in removed:
                print(f"  • {f}")
        
        if not_found:
            print(f"{Fore.YELLOW}⚠ Not in protection list:{Style.RESET_ALL}")
            for f in not_found:
                print(f"  • {f}")
        
    except RuntimeError as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(1)


@main.command()
def list():
    """List all protected files and patterns."""
    try:
        config = NoStageConfig()
        files = config.get_protected_files()
        patterns = config.get_patterns()
        
        if not files and not patterns:
            print(f"{Fore.YELLOW}No files or patterns are currently protected.{Style.RESET_ALL}")
            print(f"\nUse {Fore.CYAN}nostage add <file>{Style.RESET_ALL} to protect files.")
            return
        
        if files:
            print(f"{Fore.CYAN}Protected files:{Style.RESET_ALL}")
            for f in files:
                print(f"  • {f}")
        
        if patterns:
            if files:
                print()
            print(f"{Fore.CYAN}Protected patterns:{Style.RESET_ALL}")
            for p in patterns:
                print(f"  • {p}")
        
    except RuntimeError as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(1)


@main.command()
@click.argument('pattern')
def pattern(pattern):
    """Add a pattern to protect matching files.
    
    Examples:
        nostage pattern "*.temp.js"
        nostage pattern "debug_*.py"
        nostage pattern "scratch/*"
    """
    try:
        config = NoStageConfig()
        
        if config.add_pattern(pattern):
            print(f"{Fore.GREEN}✓ Pattern added: {pattern}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠ Pattern already exists: {pattern}{Style.RESET_ALL}")
        
    except RuntimeError as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(1)


@main.command(name='remove-pattern')
@click.argument('pattern')
def remove_pattern(pattern):
    """Remove a pattern from the protection list.
    
    Examples:
        nostage remove-pattern "*.temp.js"
    """
    try:
        config = NoStageConfig()
        
        if config.remove_pattern(pattern):
            print(f"{Fore.GREEN}✓ Pattern removed: {pattern}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠ Pattern not found: {pattern}{Style.RESET_ALL}")
        
    except RuntimeError as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(1)


@main.command()
def init():
    """Install NoStage pre-commit hook in the current repository."""
    success, message = install_hook()
    
    if success:
        print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}NoStage is now active!{Style.RESET_ALL}")
        print(f"Add files to protect: {Fore.CYAN}nostage add <file>{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(1)


@main.command()
def uninstall():
    """Uninstall NoStage pre-commit hook."""
    success, message = uninstall_hook()
    
    if success:
        print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(1)


@main.command(hidden=True)
def hook():
    """Run the pre-commit hook (called automatically by Git)."""
    sys.exit(run_pre_commit_hook())


@main.command()
def status():
    """Show NoStage status and statistics."""
    try:
        config = NoStageConfig()
        files = config.get_protected_files()
        patterns = config.get_patterns()
        
        print(f"{Fore.CYAN}NoStage Status:{Style.RESET_ALL}\n")
        print(f"Repository: {config.repo_root}")
        print(f"Protected files: {len(files)}")
        print(f"Protected patterns: {len(patterns)}")
        
        # Check if hook is installed
        hook_path = config.repo_root / ".git" / "hooks" / "pre-commit"
        if hook_path.exists():
            with open(hook_path, 'r') as f:
                if "NoStage" in f.read():
                    print(f"Hook status: {Fore.GREEN}✓ Installed{Style.RESET_ALL}")
                else:
                    print(f"Hook status: {Fore.YELLOW}⚠ Different hook installed{Style.RESET_ALL}")
        else:
            print(f"Hook status: {Fore.RED}✗ Not installed{Style.RESET_ALL}")
            print(f"\nRun {Fore.CYAN}nostage init{Style.RESET_ALL} to install the hook.")
        
    except RuntimeError as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
