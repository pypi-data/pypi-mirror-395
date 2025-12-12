"""Git hook implementation for NoStage."""

import subprocess
import sys
from pathlib import Path
from typing import List, Set
from .config import NoStageConfig


def get_staged_files() -> List[str]:
    """Get list of currently staged files.
    
    Returns:
        List of staged file paths
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            check=True
        )
        files = result.stdout.strip().split('\n')
        return [f for f in files if f]  # Filter empty strings
    except subprocess.CalledProcessError:
        return []


def unstage_file(filepath: str):
    """Unstage a specific file.
    
    Args:
        filepath: Path to file to unstage
    """
    try:
        # Try with HEAD first (for normal commits)
        subprocess.run(
            ["git", "reset", "HEAD", filepath],
            capture_output=True,
            check=True
        )
    except subprocess.CalledProcessError:
        # If that fails (e.g., initial commit), use reset without HEAD
        try:
            subprocess.run(
                ["git", "reset", filepath],
                capture_output=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to unstage {filepath}: {e}", file=sys.stderr)


def run_pre_commit_hook() -> int:
    """Run the pre-commit hook logic.
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        config = NoStageConfig()
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    # Get staged files
    staged_files = get_staged_files()
    
    if not staged_files:
        return 0
    
    # Check which files are protected
    protected_files = []
    for filepath in staged_files:
        if config.is_protected(filepath):
            protected_files.append(filepath)
    
    # Unstage protected files
    if protected_files:
        print(f"\n🛡️  NoStage: Protecting {len(protected_files)} file(s) from commit:\n")
        for filepath in protected_files:
            print(f"   • {filepath}")
            unstage_file(filepath)
        print()
    
    return 0


def install_hook():
    """Install the pre-commit hook in the current repository."""
    try:
        config = NoStageConfig()
        hook_dir = config.repo_root / ".git" / "hooks"
        hook_path = hook_dir / "pre-commit"
        
        # Create hooks directory if it doesn't exist
        hook_dir.mkdir(parents=True, exist_ok=True)
        
        # Hook script content
        hook_content = """#!/usr/bin/env python3
\"\"\"NoStage pre-commit hook - Auto-generated, do not edit manually.\"\"\"

import sys
import os

try:
    from nostage.hook import run_pre_commit_hook
    sys.exit(run_pre_commit_hook())
except ImportError:
    # NoStage was uninstalled via pip - clean up everything
    print("⚠️  NoStage package not found (was it uninstalled?)")
    print("🧹 Cleaning up...")
    
    # Remove this hook file
    hook_path = os.path.abspath(__file__)
    try:
        os.remove(hook_path)
        print("   ✓ Removed pre-commit hook")
    except Exception as e:
        print(f"   ✗ Could not remove hook: {e}")
    
    # Remove .nostage config file
    try:
        repo_root = os.path.dirname(os.path.dirname(os.path.dirname(hook_path)))
        nostage_config = os.path.join(repo_root, '.nostage')
        if os.path.exists(nostage_config):
            os.remove(nostage_config)
            print("   ✓ Removed .nostage config file")
    except Exception as e:
        print(f"   ✗ Could not remove .nostage: {e}")
    
    print("✅ NoStage cleanup complete. Commit will proceed normally.")
    sys.exit(0)  # Don't block the commit
except Exception as e:
    print(f"⚠️  NoStage hook error: {e}")
    print("   Continuing with commit...")
    sys.exit(0)  # Don't block commits on errors
"""
        
        # Check if hook already exists
        if hook_path.exists():
            with open(hook_path, 'r') as f:
                existing_content = f.read()
                if "NoStage" in existing_content:
                    return False, "NoStage hook already installed"
                else:
                    return False, f"A different pre-commit hook already exists at {hook_path}"
        
        # Write hook
        with open(hook_path, 'w') as f:
            f.write(hook_content)
        
        # Make executable
        hook_path.chmod(0o755)
        
        return True, f"Hook installed at {hook_path}"
        
    except Exception as e:
        return False, f"Failed to install hook: {e}"


def uninstall_hook():
    """Uninstall the pre-commit hook."""
    try:
        config = NoStageConfig()
        hook_path = config.repo_root / ".git" / "hooks" / "pre-commit"
        
        if not hook_path.exists():
            return False, "No pre-commit hook found"
        
        # Check if it's our hook
        with open(hook_path, 'r') as f:
            content = f.read()
            if "NoStage" not in content:
                return False, "Pre-commit hook exists but is not a NoStage hook"
        
        # Remove hook
        hook_path.unlink()
        
        return True, "NoStage hook uninstalled"
        
    except Exception as e:
        return False, f"Failed to uninstall hook: {e}"
