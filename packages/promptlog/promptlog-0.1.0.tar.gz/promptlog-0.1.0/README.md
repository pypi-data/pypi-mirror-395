# PromptLog

A version control tool for prompts, designed to help you manage, track, and compare different versions of your prompts.

## Features

- **Version Management**: Create, save, and load different versions of prompts
- **Version Comparison**: Compare different versions of prompts to see changes
- **Metadata Tracking**: Record information about each version (timestamp, author, description, etc.)
- **Local Storage**: Store prompts and their versions locally on your file system

## Installation

```bash
pip install promptlog
```

## Usage

### Basic Usage

```python
from promptlog import PromptManager

# Initialize prompt manager
pm = PromptManager("my_prompt_project")

# Create and save a new prompt version
pm.save_prompt(
    name="welcome_message",
    content="Hello, welcome to our service!",
    description="Initial welcome message",
    author="John Doe"
)

# Update the prompt and save as a new version
pm.save_prompt(
    name="welcome_message",
    content="Hello, welcome to our improved service!",
    description="Updated welcome message with improved wording",
    author="John Doe"
)

# List all versions of a prompt
versions = pm.list_versions("welcome_message")
print(versions)

# Load a specific version
prompt_v1 = pm.load_version("welcome_message", version=1)
print(prompt_v1.content)

# Compare two versions
comparison = pm.compare_versions("welcome_message", version1=1, version2=2)
print(comparison)
```

### Advanced Features

```python
# Search prompts by metadata
prompts = pm.search_prompts(author="John Doe")

# Get prompt history
history = pm.get_prompt_history("welcome_message")

# Delete a specific version
pm.delete_version("welcome_message", version=1)

# Delete all versions of a prompt
pm.delete_prompt("welcome_message")
```

## API Reference

### PromptManager

- `__init__(project_name, storage_path=None)`: Initialize the prompt manager
- `save_prompt(name, content, description="", author="", tags=None)`: Save a new prompt version
- `list_versions(name)`: List all versions of a prompt
- `load_version(name, version)`: Load a specific version of a prompt
- `compare_versions(name, version1, version2)`: Compare two versions of a prompt
- `search_prompts(**kwargs)`: Search prompts by metadata
- `get_prompt_history(name)`: Get the full history of a prompt
- `delete_version(name, version)`: Delete a specific version
- `delete_prompt(name)`: Delete all versions of a prompt

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
