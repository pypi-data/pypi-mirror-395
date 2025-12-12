"""Configuration management for NoStage."""

import json
import os
from pathlib import Path
from typing import List, Dict, Set


class NoStageConfig:
    """Manages NoStage configuration for a git repository."""
    
    CONFIG_FILE = ".nostage"
    
    def __init__(self, repo_root: str = None):
        """Initialize config manager.
        
        Args:
            repo_root: Root directory of the git repository
        """
        if repo_root is None:
            repo_root = self._find_git_root()
        
        self.repo_root = Path(repo_root)
        self.config_path = self.repo_root / self.CONFIG_FILE
        self.config = self._load_config()
    
    def _find_git_root(self) -> Path:
        """Find the root of the git repository.
        
        Returns:
            Path to git repository root
            
        Raises:
            RuntimeError: If not in a git repository
        """
        current = Path.cwd()
        
        while current != current.parent:
            if (current / ".git").exists():
                return current
            current = current.parent
        
        raise RuntimeError("Not in a git repository. Run 'git init' first.")
    
    def _load_config(self) -> Dict:
        """Load configuration from file.
        
        Returns:
            Configuration dictionary
        """
        if not self.config_path.exists():
            return {
                "files": [],
                "patterns": []
            }
        
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {
                "files": [],
                "patterns": []
            }
    
    def _save_config(self):
        """Save configuration to file."""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def add_file(self, filepath: str) -> bool:
        """Add a file to the protection list.
        
        Args:
            filepath: Path to file (relative to repo root)
            
        Returns:
            True if file was added, False if already exists
        """
        # Normalize path
        filepath = str(Path(filepath))
        
        if filepath in self.config["files"]:
            return False
        
        self.config["files"].append(filepath)
        self._save_config()
        return True
    
    def remove_file(self, filepath: str) -> bool:
        """Remove a file from the protection list.
        
        Args:
            filepath: Path to file (relative to repo root)
            
        Returns:
            True if file was removed, False if not found
        """
        filepath = str(Path(filepath))
        
        if filepath not in self.config["files"]:
            return False
        
        self.config["files"].remove(filepath)
        self._save_config()
        return True
    
    def add_pattern(self, pattern: str) -> bool:
        """Add a pattern to the protection list.
        
        Args:
            pattern: File pattern (e.g., *.temp.js)
            
        Returns:
            True if pattern was added, False if already exists
        """
        if pattern in self.config["patterns"]:
            return False
        
        self.config["patterns"].append(pattern)
        self._save_config()
        return True
    
    def remove_pattern(self, pattern: str) -> bool:
        """Remove a pattern from the protection list.
        
        Args:
            pattern: File pattern to remove
            
        Returns:
            True if pattern was removed, False if not found
        """
        if pattern not in self.config["patterns"]:
            return False
        
        self.config["patterns"].remove(pattern)
        self._save_config()
        return True
    
    def get_protected_files(self) -> List[str]:
        """Get list of protected files.
        
        Returns:
            List of protected file paths
        """
        return self.config["files"].copy()
    
    def get_patterns(self) -> List[str]:
        """Get list of protection patterns.
        
        Returns:
            List of patterns
        """
        return self.config["patterns"].copy()
    
    def is_protected(self, filepath: str) -> bool:
        """Check if a file is protected.
        
        Args:
            filepath: Path to file (relative to repo root)
            
        Returns:
            True if file is protected
        """
        from fnmatch import fnmatch
        
        filepath = str(Path(filepath))
        
        # Check exact match
        if filepath in self.config["files"]:
            return True
        
        # Check patterns
        for pattern in self.config["patterns"]:
            if fnmatch(filepath, pattern):
                return True
        
        return False
