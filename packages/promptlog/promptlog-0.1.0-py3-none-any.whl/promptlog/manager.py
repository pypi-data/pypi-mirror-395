import json
import os
import re
import time
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple

# Third-party imports
from deepdiff import DeepDiff
from appdirs import user_data_dir

class PromptVersion:
    """
    Represents a single version of a prompt
    """
    def __init__(self, content: str, description: str = "", author: str = "", 
                 tags: Optional[List[str]] = None, timestamp: Optional[float] = None, 
                 version: Optional[int] = None):
        self.content: str = content
        self.description: str = description
        self.author: str = author
        self.tags: List[str] = tags or []
        self.timestamp: float = timestamp or time.time()
        self.version: Optional[int] = version
        self.created_at: str = datetime.fromtimestamp(self.timestamp).strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the prompt version to a dictionary"""
        return {
            "content": self.content,
            "description": self.description,
            "author": self.author,
            "tags": self.tags,
            "timestamp": self.timestamp,
            "version": self.version,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PromptVersion':
        """Create a PromptVersion instance from a dictionary"""
        return cls(
            content=data["content"],
            description=data.get("description", ""),
            author=data.get("author", ""),
            tags=data.get("tags", []),
            timestamp=data.get("timestamp"),
            version=data.get("version")
        )


class PromptManager:
    """
    Manages prompt versions, providing functionality to save, load, compare, and track versions
    """
    def __init__(self, project_name: str, storage_path: Optional[str] = None):
        """
        Initialize the prompt manager
        
        Args:
            project_name (str): Name of the project
            storage_path (str, optional): Path to store prompt data. Defaults to user's app data directory.
        """
        self.project_name: str = project_name
        # Use appdirs to get standard app data directory for better cross-platform compatibility
        default_storage: str = os.path.join(user_data_dir("promptkit"), project_name)
        self.storage_path: str = storage_path or default_storage
        self._ensure_storage_exists()

    def _ensure_storage_exists(self) -> None:
        """Ensure the storage directory exists"""
        os.makedirs(self.storage_path, exist_ok=True)
    
    def _sanitize_prompt_name(self, name: str) -> str:
        """
        Sanitize prompt name to ensure it's a valid filename across all platforms
        
        Args:
            name (str): Original prompt name
            
        Returns:
            str: Sanitized prompt name
        """
        # Remove or replace invalid characters for Windows filenames
        # Windows invalid chars: < > : " / \ | ? *
        sanitized: str = re.sub(r'[<>:"/\\|?*]', '_', name)
        
        # Remove leading/trailing whitespace and dots
        sanitized = sanitized.strip().strip('.')
        
        # Ensure the name is not empty after sanitization
        if not sanitized:
            sanitized = "untitled"
        
        # Check for reserved Windows filenames
        reserved_names: List[str] = [
            "CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4", "COM5",
            "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4",
            "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
        ]
        if sanitized.upper() in reserved_names:
            sanitized = f"{sanitized}_prompt"
        
        # Limit length (Windows has 255 character limit for full path, so keep filename reasonable)
        max_length: int = 100
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized

    def save_prompt(self, name: str, content: str, description: str = "", 
                   author: str = "", tags: Optional[List[str]] = None) -> int:
        """
        Save a new version of a prompt
        
        Args:
            name (str): Name of the prompt
            content (str): Content of the prompt
            description (str, optional): Description of the changes. Defaults to "".
            author (str, optional): Author of the change. Defaults to "".
            tags (list, optional): Tags for the prompt. Defaults to None.
            
        Returns:
            int: The new version number
        """
        # Sanitize prompt name for cross-platform compatibility
        sanitized_name = self._sanitize_prompt_name(name)
        
        # Get existing versions
        prompt_path = os.path.join(self.storage_path, f"{sanitized_name}.json")
        versions = []
        
        if os.path.exists(prompt_path):
            with open(prompt_path, "r") as f:
                versions = json.load(f)
        
        # Determine new version number
        new_version = len(versions) + 1
        
        # Create new version
        new_prompt_version = PromptVersion(
            content=content,
            description=description,
            author=author,
            tags=tags,
            version=new_version
        )
        
        # Add to versions and save
        versions.append(new_prompt_version.to_dict())
        
        with open(prompt_path, "w") as f:
            json.dump(versions, f, indent=2)
        
        return new_version

    def list_versions(self, name: str) -> List[Dict[str, Any]]:
        """
        List all versions of a prompt
        
        Args:
            name (str): Name of the prompt
            
        Returns:
            list: List of version metadata dictionaries
        """
        # Sanitize prompt name for cross-platform compatibility
        sanitized_name: str = self._sanitize_prompt_name(name)
        prompt_path: str = os.path.join(self.storage_path, f"{sanitized_name}.json")
        
        if not os.path.exists(prompt_path):
            return []
        
        with open(prompt_path, "r") as f:
            versions: List[Dict[str, Any]] = json.load(f)
        
        # Return basic metadata for each version
        return [{
            "version": v["version"],
            "description": v["description"],
            "author": v["author"],
            "created_at": v["created_at"]
        } for v in versions]

    def load_version(self, name: str, version: int) -> 'PromptVersion':
        """
        Load a specific version of a prompt
        
        Args:
            name (str): Name of the prompt
            version (int): Version number to load
            
        Returns:
            PromptVersion: The loaded prompt version
            
        Raises:
            ValueError: If the version does not exist
        """
        # Sanitize prompt name for cross-platform compatibility
        sanitized_name = self._sanitize_prompt_name(name)
        prompt_path = os.path.join(self.storage_path, f"{sanitized_name}.json")
        
        if not os.path.exists(prompt_path):
            raise ValueError(f"Prompt '{name}' does not exist")
        
        with open(prompt_path, "r") as f:
            versions = json.load(f)
        
        # Find the requested version
        for v in versions:
            if v["version"] == version:
                return PromptVersion.from_dict(v)
        
        raise ValueError(f"Version {version} of prompt '{name}' does not exist")

    def compare_versions(self, name: str, version1: int, version2: int) -> Dict[str, Any]:
        """
        Compare two versions of a prompt
        
        Args:
            name (str): Name of the prompt
            version1 (int): First version to compare
            version2 (int): Second version to compare
            
        Returns:
            dict: Comparison result showing differences
        """
        # Sanitize prompt name once for both loads
        sanitized_name = self._sanitize_prompt_name(name)
        # Load both versions
        prompt_v1 = self.load_version(sanitized_name, version1)
        prompt_v2 = self.load_version(sanitized_name, version2)
        
        # Compare content
        diff = DeepDiff(prompt_v1.content, prompt_v2.content, ignore_order=True)
        
        return {
            "version1": {
                "version": prompt_v1.version,
                "created_at": prompt_v1.created_at,
                "author": prompt_v1.author
            },
            "version2": {
                "version": prompt_v2.version,
                "created_at": prompt_v2.created_at,
                "author": prompt_v2.author
            },
            "differences": diff
        }

    def search_prompts(self, **kwargs: Any) -> List[Tuple[str, 'PromptVersion']]:
        """
        Search prompts by metadata
        
        Args:
            **kwargs: Metadata filters (e.g., author="John", tags=["greeting"])
            
        Returns:
            list: List of matching prompts with their latest versions
        """
        results = []
        
        # Iterate through all prompt files
        for filename in os.listdir(self.storage_path):
            if filename.endswith(".json"):
                prompt_name = filename[:-5]  # Remove .json extension
                prompt_path = os.path.join(self.storage_path, filename)
                
                with open(prompt_path, "r") as f:
                    versions = json.load(f)
                
                if not versions:
                    continue
                
                # Check each version for matches
                for version_data in versions:
                    match = True
                    
                    for key, value in kwargs.items():
                        if key == "tags":
                            # Check if all requested tags are present
                            prompt_tags = version_data.get("tags", [])
                            for tag in value:
                                if tag not in prompt_tags:
                                    match = False
                                    break
                        elif version_data.get(key) != value:
                            match = False
                            break
                    
                    if match:
                        # Create PromptVersion and add to results
                        prompt_version = PromptVersion.from_dict(version_data)
                        results.append((prompt_name, prompt_version))
                        break  # Only add one version per prompt
        
        return results

    def get_prompt_history(self, name: str) -> List['PromptVersion']:
        """
        Get the full history of a prompt
        
        Args:
            name (str): Name of the prompt
            
        Returns:
            list: List of all PromptVersion objects for the prompt
        """
        # Sanitize prompt name for cross-platform compatibility
        sanitized_name = self._sanitize_prompt_name(name)
        prompt_path = os.path.join(self.storage_path, f"{sanitized_name}.json")
        
        if not os.path.exists(prompt_path):
            return []
        
        with open(prompt_path, "r") as f:
            versions = json.load(f)
        
        return [PromptVersion.from_dict(v) for v in versions]

    def delete_version(self, name: str, version: int) -> None:
        """
        Delete a specific version of a prompt
        
        Args:
            name (str): Name of the prompt
            version (int): Version number to delete
            
        Raises:
            ValueError: If the version does not exist
        """
        # Sanitize prompt name for cross-platform compatibility
        sanitized_name = self._sanitize_prompt_name(name)
        prompt_path = os.path.join(self.storage_path, f"{sanitized_name}.json")
        
        if not os.path.exists(prompt_path):
            raise ValueError(f"Prompt '{name}' does not exist")
        
        with open(prompt_path, "r") as f:
            versions = json.load(f)
        
        # Find and remove the requested version
        new_versions = []
        found = False
        
        for v in versions:
            if v["version"] == version:
                found = True
            else:
                # Adjust version numbers for remaining versions if we removed an earlier one
                if found and v["version"] > version:
                    v["version"] -= 1
                new_versions.append(v)
        
        if not found:
            raise ValueError(f"Version {version} of prompt '{name}' does not exist")
        
        # Save the updated versions
        with open(prompt_path, "w") as f:
            json.dump(new_versions, f, indent=2)

    def get_latest_version(self, name: str) -> Optional['PromptVersion']:
        """
        Get the latest version of a prompt
        
        Args:
            name (str): Name of the prompt
            
        Returns:
            PromptVersion: The latest prompt version, or None if no versions exist
        """
        versions: List[Dict[str, Any]] = self.list_versions(name)
        if not versions:
            return None
        
        # Return the highest version number (latest)
        latest_version = max(versions, key=lambda x: x["version"])
        return PromptVersion.from_dict(latest_version)

    def list_prompts(self) -> List[str]:
        """
        List all prompts in the current project
        
        Returns:
            list: List of prompt names
        """
        prompts: List[str] = []
        if os.path.exists(self.storage_path):
            for filename in os.listdir(self.storage_path):
                if filename.endswith('.json'):
                    # Remove the .json extension
                    prompt_name = os.path.splitext(filename)[0]
                    prompts.append(prompt_name)
        return prompts

    def delete_prompt(self, name: str) -> None:
        """
        Delete all versions of a prompt
        
        Args:
            name (str): Name of the prompt to delete
        """
        # Sanitize prompt name for cross-platform compatibility
        sanitized_name: str = self._sanitize_prompt_name(name)
        prompt_path: str = os.path.join(self.storage_path, f"{sanitized_name}.json")
        
        if os.path.exists(prompt_path):
            os.remove(prompt_path)
