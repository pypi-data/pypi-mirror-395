import os
import shutil
import tempfile
import unittest
from promptlog import PromptManager


class TestPromptManager(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.temp_dir = tempfile.mkdtemp()
        self.project_name = "test_project"
        self.pm = PromptManager(self.project_name, storage_path=self.temp_dir)
    
    def tearDown(self):
        # Remove the temporary directory after tests
        shutil.rmtree(self.temp_dir)
    
    def test_save_prompt(self):
        # Test saving a new prompt
        version = self.pm.save_prompt(
            name="test_prompt",
            content="Hello, world!",
            description="Test prompt",
            author="Test Author",
            tags=["test", "greeting"]
        )
        
        self.assertEqual(version, 1)
        
        # Test saving a second version
        version = self.pm.save_prompt(
            name="test_prompt",
            content="Hello, everyone!",
            description="Updated test prompt",
            author="Test Author"
        )
        
        self.assertEqual(version, 2)
    
    def test_list_versions(self):
        # Save two versions
        self.pm.save_prompt(
            name="test_prompt",
            content="Version 1",
            description="First version"
        )
        
        self.pm.save_prompt(
            name="test_prompt",
            content="Version 2",
            description="Second version"
        )
        
        # List versions
        versions = self.pm.list_versions("test_prompt")
        
        self.assertEqual(len(versions), 2)
        self.assertEqual(versions[0]["version"], 1)
        self.assertEqual(versions[1]["version"], 2)
        self.assertEqual(versions[0]["description"], "First version")
        self.assertEqual(versions[1]["description"], "Second version")
    
    def test_load_version(self):
        # Save a prompt
        self.pm.save_prompt(
            name="test_prompt",
            content="Test content",
            description="Test prompt"
        )
        
        # Load the prompt
        prompt = self.pm.load_version("test_prompt", version=1)
        
        self.assertEqual(prompt.content, "Test content")
        self.assertEqual(prompt.description, "Test prompt")
        self.assertEqual(prompt.version, 1)
        
        # Test loading non-existent version
        with self.assertRaises(ValueError):
            self.pm.load_version("test_prompt", version=2)
    
    def test_compare_versions(self):
        # Save two versions
        self.pm.save_prompt(
            name="test_prompt",
            content="Hello, world!",
            description="Version 1"
        )
        
        self.pm.save_prompt(
            name="test_prompt",
            content="Hello, everyone!",
            description="Version 2"
        )
        
        # Compare versions
        comparison = self.pm.compare_versions("test_prompt", version1=1, version2=2)
        
        self.assertEqual(comparison["version1"]["version"], 1)
        self.assertEqual(comparison["version2"]["version"], 2)
        self.assertIn("differences", comparison)
    
    def test_search_prompts(self):
        # Save prompts with different metadata
        self.pm.save_prompt(
            name="prompt1",
            content="Content 1",
            author="Author 1",
            tags=["tag1", "tag2"]
        )
        
        self.pm.save_prompt(
            name="prompt2",
            content="Content 2",
            author="Author 2",
            tags=["tag1", "tag3"]
        )
        
        # Search by author
        results = self.pm.search_prompts(author="Author 1")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], "prompt1")
        
        # Search by tag
        results = self.pm.search_prompts(tags=["tag1"])
        self.assertEqual(len(results), 2)
        
        # Search by author and tag
        results = self.pm.search_prompts(author="Author 1", tags=["tag2"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], "prompt1")
    
    def test_get_prompt_history(self):
        # Save three versions
        self.pm.save_prompt(
            name="test_prompt",
            content="Version 1",
            description="First version"
        )
        
        self.pm.save_prompt(
            name="test_prompt",
            content="Version 2",
            description="Second version"
        )
        
        self.pm.save_prompt(
            name="test_prompt",
            content="Version 3",
            description="Third version"
        )
        
        # Get history
        history = self.pm.get_prompt_history("test_prompt")
        
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0].content, "Version 1")
        self.assertEqual(history[1].content, "Version 2")
        self.assertEqual(history[2].content, "Version 3")
    
    def test_delete_version(self):
        # Save three versions
        self.pm.save_prompt(
            name="test_prompt",
            content="Version 1",
            description="First version"
        )
        
        self.pm.save_prompt(
            name="test_prompt",
            content="Version 2",
            description="Second version"
        )
        
        self.pm.save_prompt(
            name="test_prompt",
            content="Version 3",
            description="Third version"
        )
        
        # Delete version 2
        self.pm.delete_version("test_prompt", version=2)
        
        # Check versions after deletion
        versions = self.pm.list_versions("test_prompt")
        self.assertEqual(len(versions), 2)
        self.assertEqual(versions[0]["version"], 1)
        self.assertEqual(versions[1]["version"], 2)  # Version 3 becomes version 2
        
        # Load the new version 2 (previously version 3)
        prompt = self.pm.load_version("test_prompt", version=2)
        self.assertEqual(prompt.content, "Version 3")
    
    def test_delete_prompt(self):
        # Save a prompt
        self.pm.save_prompt(
            name="test_prompt",
            content="Test content",
            description="Test prompt"
        )
        
        # Delete the prompt
        self.pm.delete_prompt("test_prompt")
        
        # Check that the prompt no longer exists
        versions = self.pm.list_versions("test_prompt")
        self.assertEqual(len(versions), 0)


if __name__ == "__main__":
    unittest.main()
