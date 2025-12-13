"""
Tools module for Gemini Agent
Provides file system operations and command execution capabilities
"""

import os
import shutil
import subprocess
from typing import Optional
from pathlib import Path

from terminal_manager import terminal_manager
from memory import memory_manager


# ============================================================================
# SANDBOX CONFIGURATION - Restricts AI to project folder only
# ============================================================================

# This will be set by the agent to the current project directory
SANDBOX_ROOT = None

def set_sandbox_root(path: str):
    """Set the sandbox root directory. AI cannot access files outside this."""
    global SANDBOX_ROOT
    SANDBOX_ROOT = Path(path).resolve()

def get_sandbox_root() -> Path:
    """Get the current sandbox root."""
    global SANDBOX_ROOT
    if SANDBOX_ROOT is None:
        # Default to current working directory if not set
        SANDBOX_ROOT = Path.cwd()
    return SANDBOX_ROOT


def auto_commit_changes(message: str = "Auto-commit by AADC"):
    """Auto-commit changes to GitHub if enabled."""
    try:
        from config import config
        from github_integration import github_integration
        
        if not config.github_auto_commit:
            return
        
        if not github_integration.is_authenticated():
            return
        
        sandbox = get_sandbox_root()
        github_integration.commit_and_push(str(sandbox), message)
    except Exception:
        # Silently fail - don't break file operations if git fails
        pass


def is_path_safe(path: str) -> tuple[bool, str]:
    """
    Check if a path is within the sandbox.
    Returns (is_safe, resolved_path_or_error_message)
    """
    try:
        sandbox = get_sandbox_root()
        
        # Resolve the path (handles .., symlinks, etc.)
        if Path(path).is_absolute():
            resolved = Path(path).resolve()
        else:
            resolved = (sandbox / path).resolve()
        
        # Check if the resolved path is within the sandbox
        try:
            resolved.relative_to(sandbox)
            return True, str(resolved)
        except ValueError:
            return False, f"Access denied: Path '{path}' is outside the project folder. You can only access files within: {sandbox}"
    
    except Exception as e:
        return False, f"Invalid path: {str(e)}"

def is_command_safe(command: str) -> tuple[bool, str]:
    """
    Check if a command is safe to execute.
    Blocks commands that could navigate outside sandbox or access sensitive data.
    """
    command_lower = command.lower().strip()
    
    # Dangerous patterns that could escape sandbox
    dangerous_patterns = [
        'cd ..',           # Navigate up
        'cd...',           # Navigate up (no space)
        'cd /',            # Navigate to root
        'cd ~',            # Navigate to home
        'cd %',            # Windows env vars
        'cd $',            # Unix env vars
        'pushd ..',        # Navigate up
        'set-location ..',  # PowerShell navigate up
        'sl ..',           # PowerShell alias
        'chdir ..',        # Change directory up
        '../',             # Relative path up
        '..\\',            # Windows relative path up
        '%userprofile%',   # Windows user folder
        '%appdata%',       # Windows app data
        '%homepath%',      # Windows home
        '$home',           # Unix home
        '$user',           # Unix user
        '/etc/',           # System config
        '/usr/',           # System binaries  
        '/var/',           # System data
        '/root',           # Root home
        'c:\\users',       # Windows users folder
        'c:\\windows',     # Windows system
        'c:\\program',     # Windows programs
    ]
    
    for pattern in dangerous_patterns:
        if pattern in command_lower:
            return False, f"Command blocked for security: Contains '{pattern}' which could access files outside your project."
    
    # Block commands that read sensitive files
    sensitive_commands = [
        'type %',          # Windows read env paths
        'cat /etc',        # Unix system files
        'cat ~',           # Home directory
        'more %',          # Windows read env paths
        'get-content $',   # PowerShell read vars
        'gc ~',            # PowerShell home
        '.env',            # Environment files (unless creating)
        'password',        # Password files
        'credentials',     # Credential files
        'ssh/',            # SSH keys
        '.ssh',            # SSH folder
    ]
    
    for pattern in sensitive_commands:
        if pattern in command_lower and 'create' not in command_lower and 'echo' not in command_lower:
            return False, f"Command blocked for security: May access sensitive data."
    
    return True, command


# ============================================================================
# TOOL IMPLEMENTATIONS
# ============================================================================

def create_file(file_path: str, content: str = "") -> dict:
    """Create a new file with optional content."""
    # Security check
    is_safe, result = is_path_safe(file_path)
    if not is_safe:
        return {"success": False, "error": result}
    
    safe_path = result
    
    try:
        path = Path(safe_path)
        # Create parent directories if they don't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "success": True,
            "message": f"Successfully created file: {file_path}",
            "path": str(path.absolute())
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to create file: {str(e)}"
        }


def create_folder(folder_path: str) -> dict:
    """Create a new folder/directory."""
    # Security check
    is_safe, result = is_path_safe(folder_path)
    if not is_safe:
        return {"success": False, "error": result}
    
    safe_path = result
    
    try:
        path = Path(safe_path)
        path.mkdir(parents=True, exist_ok=True)
        
        return {
            "success": True,
            "message": f"Successfully created folder: {folder_path}",
            "path": str(path.absolute())
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to create folder: {str(e)}"
        }


def delete_file(file_path: str) -> dict:
    """Delete a file."""
    # Security check
    is_safe, result = is_path_safe(file_path)
    if not is_safe:
        return {"success": False, "error": result}
    
    safe_path = result
    
    try:
        path = Path(safe_path)
        
        if not path.exists():
            return {
                "success": False,
                "error": f"File does not exist: {file_path}"
            }
        
        if path.is_dir():
            return {
                "success": False,
                "error": f"Path is a directory, use delete_folder instead: {file_path}"
            }
        
        path.unlink()
        
        return {
            "success": True,
            "message": f"Successfully deleted file: {file_path}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to delete file: {str(e)}"
        }


def delete_folder(folder_path: str) -> dict:
    """Delete a folder and all its contents recursively."""
    # Security check
    is_safe, result = is_path_safe(folder_path)
    if not is_safe:
        return {"success": False, "error": result}
    
    safe_path = result
    
    try:
        path = Path(safe_path)
        
        if not path.exists():
            return {
                "success": False,
                "error": f"Folder does not exist: {folder_path}"
            }
        
        if not path.is_dir():
            return {
                "success": False,
                "error": f"Path is not a directory, use delete_file instead: {folder_path}"
            }
        
        shutil.rmtree(path)
        
        return {
            "success": True,
            "message": f"Successfully deleted folder and all contents: {folder_path}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to delete folder: {str(e)}"
        }


def list_files(folder_path: str = ".", recursive: bool = False, max_depth: int = 2) -> dict:
    """List files and folders in a directory."""
    # Security check
    is_safe, result = is_path_safe(folder_path)
    if not is_safe:
        return {"success": False, "error": result}
    
    safe_path = result
    
    try:
        path = Path(safe_path)
        
        if not path.exists():
            return {
                "success": False,
                "error": f"Path does not exist: {folder_path}"
            }
        
        if not path.is_dir():
            return {
                "success": False,
                "error": f"Path is not a directory: {folder_path}"
            }
        
        items = []
        
        def scan_directory(dir_path: Path, current_depth: int = 0):
            if current_depth > max_depth:
                return
            
            try:
                for item in sorted(dir_path.iterdir()):
                    # Skip hidden files and common ignored directories
                    if item.name.startswith('.') or item.name in ['node_modules', '__pycache__', 'venv', '.git']:
                        continue
                    
                    relative_path = item.relative_to(path)
                    item_info = {
                        "name": item.name,
                        "path": str(relative_path),
                        "type": "directory" if item.is_dir() else "file",
                    }
                    
                    if item.is_file():
                        try:
                            item_info["size"] = item.stat().st_size
                        except:
                            item_info["size"] = 0
                    
                    items.append(item_info)
                    
                    if recursive and item.is_dir():
                        scan_directory(item, current_depth + 1)
            except PermissionError:
                pass
        
        scan_directory(path)
        
        return {
            "success": True,
            "path": str(path.absolute()),
            "item_count": len(items),
            "items": items
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to list files: {str(e)}"
        }


def read_file(file_path: str, start_line: Optional[int] = None, end_line: Optional[int] = None) -> dict:
    """Read content from a file, optionally specifying line range."""
    # Security check
    is_safe, result = is_path_safe(file_path)
    if not is_safe:
        return {"success": False, "error": result}
    
    safe_path = result
    
    try:
        path = Path(safe_path)
        
        if not path.exists():
            return {
                "success": False,
                "error": f"File does not exist: {file_path}"
            }
        
        if path.is_dir():
            return {
                "success": False,
                "error": f"Path is a directory, not a file: {file_path}"
            }
        
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        
        if start_line is not None or end_line is not None:
            start = (start_line or 1) - 1  # Convert to 0-indexed
            end = end_line or total_lines
            lines = lines[start:end]
            content = ''.join(lines)
            line_info = f"Lines {start + 1}-{min(end, total_lines)} of {total_lines}"
        else:
            content = ''.join(lines)
            line_info = f"All {total_lines} lines"
        
        return {
            "success": True,
            "path": str(path.absolute()),
            "content": content,
            "line_info": line_info,
            "total_lines": total_lines
        }
    except UnicodeDecodeError:
        return {
            "success": False,
            "error": f"File is not a text file or uses unsupported encoding: {file_path}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to read file: {str(e)}"
        }


def write_file(file_path: str, content: str) -> dict:
    """Write/overwrite content to a file."""
    # Security check
    is_safe, result = is_path_safe(file_path)
    if not is_safe:
        return {"success": False, "error": result}
    
    safe_path = result
    
    try:
        path = Path(safe_path)
        
        # Create parent directories if they don't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        lines = content.count('\n') + (1 if content and not content.endswith('\n') else 0)
        
        result = {
            "success": True,
            "message": f"Successfully wrote to file: {file_path}",
            "path": str(path.absolute()),
            "lines_written": lines,
            "bytes_written": len(content.encode('utf-8'))
        }
        
        # Auto-commit if enabled
        auto_commit_changes(f"Update {path.name}")
        
        return result
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to write to file: {str(e)}"
        }


def edit_file(file_path: str, old_content: str, new_content: str) -> dict:
    """Replace specific content in a file. The old_content must exist exactly once in the file."""
    # Security check
    is_safe, result = is_path_safe(file_path)
    if not is_safe:
        return {"success": False, "error": result}
    
    safe_path = result
    
    try:
        path = Path(safe_path)
        
        if not path.exists():
            return {
                "success": False,
                "error": f"File does not exist: {file_path}"
            }
        
        with open(path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        # Check how many times old_content appears
        count = file_content.count(old_content)
        
        if count == 0:
            return {
                "success": False,
                "error": "The specified content to replace was not found in the file"
            }
        
        if count > 1:
            return {
                "success": False,
                "error": f"The specified content appears {count} times in the file. Please provide more context to make it unique."
            }
        
        # Replace the content
        new_file_content = file_content.replace(old_content, new_content, 1)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_file_content)
        
        result = {
            "success": True,
            "message": f"Successfully edited file: {file_path}",
            "path": str(path.absolute())
        }
        
        # Auto-commit if enabled
        auto_commit_changes(f"Edit {path.name}")
        
        return result
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to edit file: {str(e)}"
        }


def execute_command(command: str, working_directory: Optional[str] = None, timeout: int = 120) -> dict:
    """Execute a shell command."""
    # Security check - block dangerous commands
    is_safe, result = is_command_safe(command)
    if not is_safe:
        return {"success": False, "error": result, "command": command}
    
    # Security check - validate working directory
    if working_directory:
        is_safe, result = is_path_safe(working_directory)
        if not is_safe:
            return {"success": False, "error": result, "command": command}
        cwd = result
    else:
        cwd = str(get_sandbox_root())
    
    try:
        # Run the command
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        return {
            "success": result.returncode == 0,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": command,
            "working_directory": cwd
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Command timed out after {timeout} seconds",
            "command": command
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to execute command: {str(e)}",
            "command": command
        }


# ============================================================================
# TOOL REGISTRY - Maps function names to implementations
# ============================================================================

# Terminal management tools
def open_terminal(command: str, name: Optional[str] = None, working_directory: Optional[str] = None, is_server: bool = False) -> dict:
    """Open a new background terminal session."""
    return terminal_manager.open_terminal(command, name, working_directory, is_server)

def close_terminal(session_id: str) -> dict:
    """Close a terminal session."""
    return terminal_manager.close_terminal(session_id)

def list_terminals() -> dict:
    """List all terminal sessions."""
    return terminal_manager.list_terminals()

def get_terminal_output(session_id: str) -> dict:
    """Get output from a terminal session."""
    return terminal_manager.get_terminal_status(session_id)

def send_terminal_input(session_id: str, text: str) -> dict:
    """Send input to a terminal session."""
    return terminal_manager.send_input(session_id, text)

def check_all_backgrounds() -> dict:
    """Check status and output of all background terminal sessions."""
    return terminal_manager.get_all_status()

def wait_for_output(session_id: str, timeout: int = 5) -> dict:
    """Wait for and get output from a terminal session."""
    import time
    start = time.time()
    output_lines = []
    
    while time.time() - start < timeout:
        result = terminal_manager.get_terminal_status(session_id)
        if not result.get("success"):
            return result
        
        if result.get("recent_output"):
            output_lines.append(result["recent_output"])
        
        if not result.get("is_running"):
            break
        
        time.sleep(0.5)
    
    return {
        "success": True,
        "id": session_id,
        "output": "\n".join(output_lines),
        "is_running": result.get("is_running", False)
    }

# Memory tools
def remember(key: str, value: str, category: str = "fact") -> dict:
    """Store information in persistent memory."""
    return memory_manager.remember(key, value, category)

def recall(key: str) -> dict:
    """Retrieve information from memory."""
    return memory_manager.recall(key)

def search_memory(query: str) -> dict:
    """Search memories."""
    return memory_manager.search_memories(query)

def list_memories(category: Optional[str] = None) -> dict:
    """List all stored memories."""
    return memory_manager.list_memories(category)

def forget(key: str) -> dict:
    """Remove a memory."""
    return memory_manager.forget(key)


def serve_website(folder_path: str, port: int = 8080, name: str = None) -> dict:
    """
    Start a local HTTP server to serve a website/web app.
    Uses Python's built-in http.server which is always available.
    
    Args:
        folder_path: Path to the folder containing the website (with index.html)
        port: Port to serve on (default 8080)
        name: Friendly name for the server
        
    Returns:
        dict with server info and URL
    """
    import os
    from pathlib import Path
    
    folder = Path(folder_path)
    
    # Check if folder exists
    if not folder.exists():
        return {
            "success": False,
            "error": f"Folder does not exist: {folder_path}"
        }
    
    # Check if index.html exists
    index_file = folder / "index.html"
    if not index_file.exists():
        return {
            "success": False,
            "error": f"No index.html found in {folder_path}. Create an index.html file first."
        }
    
    # Use Python's built-in HTTP server
    command = f"python -m http.server {port}"
    server_name = name or f"Web Server ({folder.name})"
    
    result = terminal_manager.open_terminal(
        command=command,
        name=server_name,
        working_directory=str(folder.absolute()),
        is_server=True
    )
    
    if result.get("success"):
        result["url"] = f"http://localhost:{port}"
        result["message"] = f"🌐 Website running at http://localhost:{port}"
        result["folder"] = str(folder.absolute())
    
    return result


# Todo list storage (in-memory for current session)
_todo_list = []

def manage_todo(action: str, task_id: Optional[int] = None, text: str = None, status: str = None) -> dict:
    """Manage the todo list for tracking tasks."""
    global _todo_list
    
    try:
        if action == "add":
            if not text:
                return {"success": False, "error": "Task text is required for add action"}
            new_id = max([t["id"] for t in _todo_list], default=0) + 1
            task = {
                "id": new_id,
                "text": text,
                "status": "pending",  # pending, in_progress, done
                "created_at": __import__("datetime").datetime.now().isoformat()
            }
            _todo_list.append(task)
            return {
                "success": True,
                "message": f"Added task #{new_id}",
                "task": task,
                "total_tasks": len(_todo_list)
            }
        
        elif action == "list":
            pending = [t for t in _todo_list if t["status"] == "pending"]
            in_progress = [t for t in _todo_list if t["status"] == "in_progress"]
            done = [t for t in _todo_list if t["status"] == "done"]
            return {
                "success": True,
                "tasks": _todo_list,
                "summary": {
                    "total": len(_todo_list),
                    "pending": len(pending),
                    "in_progress": len(in_progress),
                    "done": len(done)
                }
            }
        
        elif action == "update":
            if task_id is None:
                return {"success": False, "error": "Task ID is required for update action"}
            for task in _todo_list:
                if task["id"] == task_id:
                    if text:
                        task["text"] = text
                    if status:
                        task["status"] = status
                    return {
                        "success": True,
                        "message": f"Updated task #{task_id}",
                        "task": task
                    }
            return {"success": False, "error": f"Task #{task_id} not found"}
        
        elif action == "delete":
            if task_id is None:
                return {"success": False, "error": "Task ID is required for delete action"}
            for i, task in enumerate(_todo_list):
                if task["id"] == task_id:
                    removed = _todo_list.pop(i)
                    return {
                        "success": True,
                        "message": f"Deleted task #{task_id}",
                        "deleted_task": removed
                    }
            return {"success": False, "error": f"Task #{task_id} not found"}
        
        elif action == "clear_done":
            before = len(_todo_list)
            _todo_list = [t for t in _todo_list if t["status"] != "done"]
            cleared = before - len(_todo_list)
            return {
                "success": True,
                "message": f"Cleared {cleared} completed tasks",
                "remaining": len(_todo_list)
            }
        
        elif action == "clear_all":
            count = len(_todo_list)
            _todo_list = []
            return {
                "success": True,
                "message": f"Cleared all {count} tasks"
            }
        
        else:
            return {"success": False, "error": f"Unknown action: {action}. Use: add, list, update, delete, clear_done, clear_all"}
    
    except Exception as e:
        return {"success": False, "error": f"Todo operation failed: {str(e)}"}


TOOL_FUNCTIONS = {
    "create_file": create_file,
    "create_folder": create_folder,
    "delete_file": delete_file,
    "delete_folder": delete_folder,
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "edit_file": edit_file,
    "execute_command": execute_command,
    # Terminal tools
    "open_terminal": open_terminal,
    "close_terminal": close_terminal,
    "list_terminals": list_terminals,
    "get_terminal_output": get_terminal_output,
    "send_terminal_input": send_terminal_input,
    "check_all_backgrounds": check_all_backgrounds,
    "wait_for_output": wait_for_output,
    # Web server
    "serve_website": serve_website,
    # Memory tools
    "remember": remember,
    "recall": recall,
    "search_memory": search_memory,
    "list_memories": list_memories,
    "forget": forget,
    # Todo list
    "manage_todo": manage_todo,
}


# ============================================================================
# GEMINI FUNCTION DECLARATIONS
# ============================================================================

TOOL_DECLARATIONS = [
    {
        "name": "create_file",
        "description": "Create a new file with optional content. Parent directories are created automatically if they don't exist.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path where the file should be created (relative or absolute)"
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file. Defaults to empty string."
                }
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "create_folder",
        "description": "Create a new folder/directory. Parent directories are created automatically if they don't exist.",
        "parameters": {
            "type": "object",
            "properties": {
                "folder_path": {
                    "type": "string",
                    "description": "The path where the folder should be created (relative or absolute)"
                }
            },
            "required": ["folder_path"]
        }
    },
    {
        "name": "delete_file",
        "description": "Delete a file from the filesystem.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to delete"
                }
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "delete_folder",
        "description": "Delete a folder and ALL its contents recursively. Use with caution!",
        "parameters": {
            "type": "object",
            "properties": {
                "folder_path": {
                    "type": "string",
                    "description": "The path to the folder to delete"
                }
            },
            "required": ["folder_path"]
        }
    },
    {
        "name": "list_files",
        "description": "List all files and folders in a directory. Use this to explore the project structure.",
        "parameters": {
            "type": "object",
            "properties": {
                "folder_path": {
                    "type": "string",
                    "description": "The path to the directory to list. Defaults to current directory."
                },
                "recursive": {
                    "type": "boolean",
                    "description": "Whether to list files recursively. Defaults to false."
                },
                "max_depth": {
                    "type": "integer",
                    "description": "Maximum depth for recursive listing. Defaults to 2."
                }
            },
            "required": []
        }
    },
    {
        "name": "read_file",
        "description": "Read the content of a file. Can optionally read specific line ranges.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to read"
                },
                "start_line": {
                    "type": "integer",
                    "description": "Optional starting line number (1-indexed)"
                },
                "end_line": {
                    "type": "integer",
                    "description": "Optional ending line number (inclusive)"
                }
            },
            "required": ["file_path"]
        }
    },
    {
        "name": "write_file",
        "description": "Write content to a file, completely replacing any existing content. Creates the file if it doesn't exist.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to write"
                },
                "content": {
                    "type": "string",
                    "description": "The complete content to write to the file"
                }
            },
            "required": ["file_path", "content"]
        }
    },
    {
        "name": "edit_file",
        "description": "Edit a file by replacing specific content. The old_content must appear exactly once in the file for the replacement to work. Use this for surgical edits to existing files.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to edit"
                },
                "old_content": {
                    "type": "string",
                    "description": "The exact content to find and replace (must be unique in the file)"
                },
                "new_content": {
                    "type": "string",
                    "description": "The new content to replace the old content with"
                }
            },
            "required": ["file_path", "old_content", "new_content"]
        }
    },
    {
        "name": "execute_command",
        "description": "Execute a shell command in the terminal. Use this to run programs, install packages, start servers, run tests, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The shell command to execute"
                },
                "working_directory": {
                    "type": "string",
                    "description": "The directory to run the command in. Defaults to current directory."
                },
                "timeout": {
                    "type": "integer",
                    "description": "Maximum time in seconds to wait for the command. Defaults to 120."
                }
            },
            "required": ["command"]
        }
    },
    # Terminal Management Tools
    {
        "name": "serve_website",
        "description": "Start a local HTTP server to serve a website or web application. This is the PREFERRED way to run HTML/JS/CSS websites. Uses Python's built-in server which is always available. Automatically checks for index.html and starts serving on the specified port.",
        "parameters": {
            "type": "object",
            "properties": {
                "folder_path": {
                    "type": "string",
                    "description": "Path to the folder containing the website (must have index.html)"
                },
                "port": {
                    "type": "integer",
                    "description": "Port to serve on (default 8080)"
                },
                "name": {
                    "type": "string",
                    "description": "Friendly name for the server"
                }
            },
            "required": ["folder_path"]
        }
    },
    {
        "name": "open_terminal",
        "description": "Open a new background terminal session to run long-running processes like servers. Use this for Node.js servers, Python servers, watch processes, etc. The terminal runs in the background while you continue other work.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The command to run in the terminal (e.g., 'npm run dev', 'python server.py')"
                },
                "name": {
                    "type": "string",
                    "description": "A friendly name for this terminal session (e.g., 'Frontend Server', 'API Server')"
                },
                "working_directory": {
                    "type": "string",
                    "description": "Directory to run the command in"
                },
                "is_server": {
                    "type": "boolean",
                    "description": "Whether this is a long-running server process"
                }
            },
            "required": ["command"]
        }
    },
    {
        "name": "close_terminal",
        "description": "Close/stop a background terminal session.",
        "parameters": {
            "type": "object",
            "properties": {
                "session_id": {
                    "type": "string",
                    "description": "The ID of the terminal session to close"
                }
            },
            "required": ["session_id"]
        }
    },
    {
        "name": "list_terminals",
        "description": "List all active background terminal sessions.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "get_terminal_output",
        "description": "Get the recent output from a background terminal session.",
        "parameters": {
            "type": "object",
            "properties": {
                "session_id": {
                    "type": "string",
                    "description": "The ID of the terminal session"
                }
            },
            "required": ["session_id"]
        }
    },
    {
        "name": "send_terminal_input",
        "description": "Send input/text to a background terminal session.",
        "parameters": {
            "type": "object",
            "properties": {
                "session_id": {
                    "type": "string",
                    "description": "The ID of the terminal session"
                },
                "text": {
                    "type": "string",
                    "description": "The text to send to the terminal"
                }
            },
            "required": ["session_id", "text"]
        }
    },
    {
        "name": "check_all_backgrounds",
        "description": "Check the status and recent output of ALL background terminal sessions at once. Use this to monitor all running servers, build processes, or any background tasks. Returns status and output for each session.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "wait_for_output",
        "description": "Wait for output from a terminal session. Useful after starting a server to wait for it to be ready, or after running a command to capture its full output.",
        "parameters": {
            "type": "object",
            "properties": {
                "session_id": {
                    "type": "string",
                    "description": "The ID of the terminal session to wait for"
                },
                "timeout": {
                    "type": "integer",
                    "description": "Maximum seconds to wait for output. Defaults to 5."
                }
            },
            "required": ["session_id"]
        }
    },
    # Memory Tools
    {
        "name": "remember",
        "description": "Store important information in persistent memory. Use this to remember user preferences, project details, names, or any facts you should recall later.",
        "parameters": {
            "type": "object",
            "properties": {
                "key": {
                    "type": "string",
                    "description": "A short identifier for this memory (e.g., 'user_name', 'preferred_framework')"
                },
                "value": {
                    "type": "string",
                    "description": "The information to remember"
                },
                "category": {
                    "type": "string",
                    "description": "Category: 'fact', 'preference', 'project', or 'note'"
                }
            },
            "required": ["key", "value"]
        }
    },
    {
        "name": "recall",
        "description": "Retrieve a specific memory by its key.",
        "parameters": {
            "type": "object",
            "properties": {
                "key": {
                    "type": "string",
                    "description": "The key of the memory to retrieve"
                }
            },
            "required": ["key"]
        }
    },
    {
        "name": "search_memory",
        "description": "Search through memories by keyword.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query to find relevant memories"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "list_memories",
        "description": "List all stored memories, optionally filtered by category.",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Optional category to filter by: 'fact', 'preference', 'project', 'note'"
                }
            },
            "required": []
        }
    },
    {
        "name": "forget",
        "description": "Remove a memory by its key.",
        "parameters": {
            "type": "object",
            "properties": {
                "key": {
                    "type": "string",
                    "description": "The key of the memory to forget"
                }
            },
            "required": ["key"]
        }
    },
    {
        "name": "manage_todo",
        "description": "Manage your todo list to track tasks during complex projects. IMPORTANT: Always create a todo list BEFORE starting any medium/complex task. Use this to plan, track progress, and ensure nothing is missed.",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "Action to perform: 'add' (add new task), 'list' (show all tasks), 'update' (modify task text or status), 'delete' (remove task), 'clear_done' (remove completed), 'clear_all' (reset list)"
                },
                "task_id": {
                    "type": "integer",
                    "description": "Task ID (required for update/delete actions)"
                },
                "text": {
                    "type": "string",
                    "description": "Task description (required for add, optional for update)"
                },
                "status": {
                    "type": "string",
                    "description": "Task status: 'pending', 'in_progress', or 'done' (for update action)"
                }
            },
            "required": ["action"]
        }
    }
]
