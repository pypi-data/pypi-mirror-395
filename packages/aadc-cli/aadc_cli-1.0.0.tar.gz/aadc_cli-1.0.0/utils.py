"""
Utility functions for AADC - Agentic AI Developer Console
Provides display formatting and helper functions with red/white theme
"""

import json
import sys
import time
import threading
from typing import Any, Optional

# ANSI color codes - Red/White Theme
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    
    # Primary theme colors
    RED = "\033[91m"           # Bright red - primary accent
    WHITE = "\033[97m"         # Bright white - main text
    DARK_RED = "\033[31m"      # Dark red - secondary
    
    # Supporting colors
    GRAY = "\033[90m"          # Dim gray for subtle text
    LIGHT_GRAY = "\033[37m"    # Light gray
    
    # Semantic colors
    SUCCESS = "\033[92m"       # Green for success
    WARNING = "\033[93m"       # Yellow for warnings
    ERROR = "\033[91m"         # Red for errors
    INFO = "\033[96m"          # Cyan for info
    
    # Legacy mappings for compatibility
    BLACK = "\033[30m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_WHITE = "\033[47m"


def enable_windows_ansi():
    """Enable ANSI escape sequences on Windows."""
    if sys.platform == "win32":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            # Enable ANSI escape sequences on Windows 10+
            # STD_OUTPUT_HANDLE = -11
            # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            handle = kernel32.GetStdHandle(-11)
            mode = ctypes.c_ulong()
            kernel32.GetConsoleMode(handle, ctypes.byref(mode))
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)
            return True
        except Exception:
            return False
    return True


def supports_color() -> bool:
    """Check if the terminal supports color output."""
    if sys.platform == "win32":
        return enable_windows_ansi()
    return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()


# Enable ANSI colors
if not supports_color():
    for attr in dir(Colors):
        if not attr.startswith('_'):
            setattr(Colors, attr, '')


def print_header():
    """Print the application header with AADC branding."""
    c = Colors
    import os
    
    # Get username
    username = os.environ.get('USERNAME', os.environ.get('USER', 'Developer'))
    
    # Get current working directory (shortened)
    cwd = os.getcwd()
    home = os.path.expanduser("~")
    if cwd.startswith(home):
        cwd = "~" + cwd[len(home):]
    
    header = f"""
{c.GRAY}┌─ {c.RED}AADC v1.0{c.GRAY} ─────────────────────────────────────────────────────────────────┐{c.RESET}
{c.GRAY}│{c.RESET}                                                                              {c.GRAY}│{c.RESET}
{c.GRAY}│{c.RESET}    {c.WHITE}{c.BOLD}Welcome back {c.RED}{username}{c.WHITE}!{c.RESET}                                                      {c.GRAY}│{c.RESET}
{c.GRAY}│{c.RESET}                                                                              {c.GRAY}│{c.RESET}
{c.GRAY}│{c.RESET}        {c.RED}╔═══╗╔═══╗╔═══╗╔═══╗{c.RESET}    {c.RED}{c.BOLD}Tips for getting started{c.RESET}                       {c.GRAY}│{c.RESET}
{c.GRAY}│{c.RESET}        {c.RED}║ A ║║ A ║║ D ║║ C ║{c.RESET}    {c.GRAY}Run {c.RED}/init{c.GRAY} to analyze project for AI context{c.RESET}     {c.GRAY}│{c.RESET}
{c.GRAY}│{c.RESET}        {c.RED}╚═══╝╚═══╝╚═══╝╚═══╝{c.RESET}    {c.GRAY}Run {c.RED}/help{c.GRAY} for all available commands{c.RESET}            {c.GRAY}│{c.RESET}
{c.GRAY}│{c.RESET}                              {c.GRAY}Run {c.RED}/models{c.GRAY} to switch AI models{c.RESET}                {c.GRAY}│{c.RESET}
{c.GRAY}│{c.RESET}                                                                              {c.GRAY}│{c.RESET}
{c.GRAY}│{c.RESET}    {c.RED}{c.BOLD}Agentic AI Developer{c.RESET}      {c.RED}{c.BOLD}Capabilities{c.RESET}                                        {c.GRAY}│{c.RESET}
{c.GRAY}│{c.RESET}                              {c.GRAY}Build websites, apps, games, CLI tools{c.RESET}           {c.GRAY}│{c.RESET}
{c.GRAY}│{c.RESET}                              {c.GRAY}Any language: TypeScript, Python, Kotlin...{c.RESET}       {c.GRAY}│{c.RESET}
{c.GRAY}│{c.RESET}    {c.GRAY}{cwd[:25]:<25}{c.RESET}   {c.GRAY}Run servers, manage files, execute commands{c.RESET}        {c.GRAY}│{c.RESET}
{c.GRAY}│{c.RESET}                                                                              {c.GRAY}│{c.RESET}
{c.GRAY}└──────────────────────────────────────────────────────────────────────────────┘{c.RESET}
"""
    print(header)


def print_welcome():
    """Print welcome tips after header."""
    c = Colors
    print(f"""
{c.GRAY}>{c.RESET} Try {c.WHITE}"create a landing page for my startup"{c.RESET}
{c.GRAY}>{c.RESET} Try {c.WHITE}"build a snake game in Python"{c.RESET}
{c.GRAY}>{c.RESET} {c.RED}/help{c.RESET} {c.GRAY}for commands{c.RESET}
""")


def print_user_prompt(cwd: str) -> str:
    """Print the user input prompt and return input."""
    c = Colors
    user_input = input(f"\n{c.GRAY}>{c.RESET} ").strip()
    return user_input


def print_thinking():
    """Print thinking indicator - Claude Code style."""
    c = Colors
    print(f"\n{c.GRAY}● Thinking...{c.RESET}", end="", flush=True)


def clear_thinking():
    """Clear the thinking indicator."""
    print("\r" + " " * 20 + "\r", end="", flush=True)


# Tool action icons and descriptions
TOOL_ICONS = {
    # File operations
    "create_file": ("📄", "Creating file", "Created"),
    "create_folder": ("📁", "Creating folder", "Created"),
    "delete_file": ("🗑️", "Deleting file", "Deleted"),
    "delete_folder": ("🗑️", "Deleting folder", "Deleted"),
    "list_files": ("📂", "Scanning directory", "Scanned"),
    "read_file": ("👁️", "Reading file", "Read"),
    "write_file": ("✏️", "Writing file", "Written"),
    "edit_file": ("🔧", "Editing file", "Edited"),
    # Commands
    "execute_command": ("⚡", "Executing command", "Executed"),
    # Terminal / Servers
    "open_terminal": ("🖥️", "Starting terminal", "Started"),
    "close_terminal": ("⏹️", "Stopping terminal", "Stopped"),
    "list_terminals": ("📋", "Listing terminals", "Listed"),
    "get_terminal_output": ("📤", "Getting output", "Retrieved"),
    "send_terminal_input": ("📥", "Sending input", "Sent"),
    "check_all_backgrounds": ("👀", "Checking all background tasks", "Checked"),
    "wait_for_output": ("⏳", "Waiting for output", "Received"),
    "serve_website": ("🌐", "Starting web server", "Server running"),
    # Memory
    "remember": ("💾", "Saving to memory", "Saved"),
    "recall": ("🔍", "Recalling memory", "Recalled"),
    "search_memory": ("🔎", "Searching memory", "Found"),
    "list_memories": ("📝", "Listing memories", "Listed"),
    "forget": ("🧹", "Removing memory", "Removed"),
    # Todo
    "manage_todo": ("✅", "Managing todo list", "Updated"),
}


def get_tool_display_info(tool_name: str, args: dict) -> tuple:
    """Get display information for a tool based on its name and arguments."""
    icon, action, past = TOOL_ICONS.get(tool_name, ("⚙️", "Processing", "Completed"))
    
    # Build a descriptive message based on the tool and its arguments
    detail = ""
    
    if tool_name == "create_file":
        path = args.get("file_path", "file")
        detail = f"{path}"
    elif tool_name == "create_folder":
        path = args.get("folder_path", "folder")
        detail = f"{path}"
    elif tool_name == "delete_file":
        path = args.get("file_path", "file")
        detail = f"{path}"
    elif tool_name == "delete_folder":
        path = args.get("folder_path", "folder")
        detail = f"{path}"
    elif tool_name == "list_files":
        path = args.get("folder_path", ".")
        detail = f"{path}"
    elif tool_name == "read_file":
        path = args.get("file_path", "file")
        detail = f"{path}"
    elif tool_name == "write_file":
        path = args.get("file_path", "file")
        content_len = len(args.get("content", ""))
        detail = f"{path} ({content_len} chars)"
    elif tool_name == "edit_file":
        path = args.get("file_path", "file")
        detail = f"{path}"
    elif tool_name == "execute_command":
        cmd = args.get("command", "")
        if len(cmd) > 40:
            cmd = cmd[:40] + "..."
        detail = f"{cmd}"
    elif tool_name == "open_terminal":
        name = args.get("name", "")
        cmd = args.get("command", "")[:30]
        detail = f"{name or cmd}"
    elif tool_name == "close_terminal":
        session_id = args.get("session_id", "")
        detail = f"session {session_id}"
    elif tool_name == "serve_website":
        folder = args.get("folder_path", "")
        port = args.get("port", 8080)
        detail = f"{folder} on port {port}"
    elif tool_name == "remember":
        key = args.get("key", "")
        detail = f"'{key}'"
    elif tool_name == "recall":
        key = args.get("key", "")
        detail = f"'{key}'"
    elif tool_name == "search_memory":
        query = args.get("query", "")
        detail = f"'{query}'"
    elif tool_name == "forget":
        key = args.get("key", "")
        detail = f"'{key}'"
    elif tool_name == "manage_todo":
        action = args.get("action", "")
        text = args.get("text", "")
        task_id = args.get("task_id", "")
        if action == "add" and text:
            detail = f"adding: {text[:30]}{'...' if len(text) > 30 else ''}"
        elif action == "update" and task_id:
            detail = f"updating task #{task_id}"
        elif action == "delete" and task_id:
            detail = f"deleting task #{task_id}"
        else:
            detail = action
    
    return icon, action, past, detail


def print_tool_call(tool_name: str, args: dict):
    """Print a formatted tool call - Claude Code style."""
    c = Colors
    icon, action, _, detail = get_tool_display_info(tool_name, args)
    
    # Compact tool call display
    print(f"\n{c.GRAY}○{c.RESET} {c.WHITE}{action}{c.RESET}", end="")
    
    if detail:
        # Truncate long details
        if len(detail) > 60:
            detail = detail[:60] + "..."
        print(f" {c.GRAY}{detail}{c.RESET}")
    else:
        print()


def print_tool_result(result: dict, success: bool = True, tool_name: str = None):
    """Print a formatted tool result - Claude Code style."""
    c = Colors
    
    if success:
        # Compact success display
        if tool_name == "create_file":
            path = result.get("path", "")
            filename = path.split('/')[-1] if '/' in path else path.split(chr(92))[-1]
            print(f"  {c.SUCCESS}✓{c.RESET} {c.GRAY}Created {filename}{c.RESET}")
        elif tool_name == "create_folder":
            print(f"  {c.SUCCESS}✓{c.RESET} {c.GRAY}Folder created{c.RESET}")
        elif tool_name == "read_file":
            lines = result.get("total_lines", 0)
            print(f"  {c.SUCCESS}✓{c.RESET} {c.GRAY}Read {lines} lines{c.RESET}")
        elif tool_name == "write_file":
            lines = result.get("lines_written", 0)
            print(f"  {c.SUCCESS}✓{c.RESET} {c.GRAY}Wrote {lines} lines{c.RESET}")
        elif tool_name == "edit_file":
            print(f"  {c.SUCCESS}✓{c.RESET} {c.GRAY}File updated{c.RESET}")
        elif tool_name == "execute_command":
            rc = result.get("return_code", 0)
            stdout = result.get("stdout", "")
            stderr = result.get("stderr", "")
            if stdout:
                # Show first few lines of output
                lines = stdout.strip().split('\n')
                if len(lines) > 3:
                    for line in lines[:3]:
                        print(f"  {c.GRAY}│ {line[:70]}{c.RESET}")
                    print(f"  {c.GRAY}│ ... ({len(lines) - 3} more lines){c.RESET}")
                else:
                    for line in lines:
                        print(f"  {c.GRAY}│ {line[:70]}{c.RESET}")
            print(f"  {c.SUCCESS}✓{c.RESET} {c.GRAY}Exit code: {rc}{c.RESET}")
        elif tool_name == "open_terminal":
            session_id = result.get("session_id", "")
            print(f"  {c.SUCCESS}✓{c.RESET} {c.GRAY}Started (ID: {session_id}){c.RESET}")
        elif tool_name == "list_files":
            count = result.get("item_count", 0)
            print(f"  {c.SUCCESS}✓{c.RESET} {c.GRAY}Found {count} items{c.RESET}")
        elif tool_name == "remember":
            print(f"  {c.SUCCESS}✓{c.RESET} {c.GRAY}Memory saved{c.RESET}")
        elif tool_name == "recall":
            value = result.get("value", "")
            if value:
                print(f"  {c.SUCCESS}✓{c.RESET} {c.GRAY}Found: {str(value)[:50]}{'...' if len(str(value)) > 50 else ''}{c.RESET}")
            else:
                print(f"  {c.WARNING}⚠{c.RESET} {c.GRAY}Not found{c.RESET}")
        elif tool_name == "search_memory":
            count = result.get("count", 0)
            print(f"  {c.SUCCESS}✓{c.RESET} {c.GRAY}Found {count} memories{c.RESET}")
        elif tool_name == "check_all_backgrounds":
            total = result.get("total", 0)
            running = result.get("running", 0)
            print(f"  {c.SUCCESS}✓{c.RESET} {c.GRAY}{running}/{total} tasks running{c.RESET}")
        elif tool_name == "wait_for_output":
            is_running = result.get("is_running", False)
            output = result.get("output", "")
            lines = len(output.split('\n')) if output else 0
            status = "running" if is_running else "done"
            print(f"  {c.SUCCESS}✓{c.RESET} {c.GRAY}Got {lines} lines ({status}){c.RESET}")
        elif tool_name == "manage_todo":
            summary = result.get("summary", {})
            if summary:
                done = summary.get("done", 0)
                total = summary.get("total", 0)
                print(f"  {c.SUCCESS}✓{c.RESET} {c.GRAY}Todo: {done}/{total} done{c.RESET}")
            else:
                print(f"  {c.SUCCESS}✓{c.RESET} {c.GRAY}Todo updated{c.RESET}")
        else:
            print(f"  {c.SUCCESS}✓{c.RESET} {c.GRAY}Done{c.RESET}")
    else:
        error = result.get("error", "Unknown error")
        print(f"  {c.ERROR}✗{c.RESET} {c.GRAY}{error}{c.RESET}")


def print_assistant_message(message: str):
    """Print assistant's text response - Claude Code style."""
    c = Colors
    print()
    # Clean markdown-style output
    for line in message.split('\n'):
        print(f"{c.WHITE}{line}{c.RESET}")


def print_task_complete():
    """Print task completion message."""
    c = Colors
    print(f"\n{c.SUCCESS}✓{c.RESET} {c.GRAY}Done{c.RESET}")


def print_status(message: str, status_type: str = "info"):
    """Print a status update message."""
    c = Colors
    icons = {
        "info": ("ℹ️", c.INFO),
        "working": ("⚙️", c.GRAY),
        "success": ("✅", c.SUCCESS),
        "warning": ("⚠️", c.WARNING),
        "error": ("❌", c.ERROR),
        "thinking": ("🤔", c.GRAY),
        "analyzing": ("🔍", c.CYAN),
        "planning": ("📋", c.MAGENTA),
    }
    icon, color = icons.get(status_type, ("•", c.GRAY))
    print(f"{c.RED}│{c.RESET} {icon} {color}{message}{c.RESET}")


def print_error(message: str):
    """Print an error message."""
    c = Colors
    print(f"\n{c.ERROR}✗ Error: {message}{c.RESET}")


def print_warning(message: str):
    """Print a warning message."""
    c = Colors
    print(f"\n{c.WARNING}⚠ Warning: {message}{c.RESET}")


def print_info(message: str):
    """Print an info message."""
    c = Colors
    print(f"\n{c.INFO}ℹ {message}{c.RESET}")


def print_success(message: str):
    """Print a success message."""
    c = Colors
    print(f"\n{c.SUCCESS}✓ {message}{c.RESET}")


def print_separator():
    """Print a visual separator - minimal style."""
    # Just a blank line for cleaner output
    print()


def print_background_status(terminal_manager) -> str:
    """Print background tasks status line and return the status text."""
    c = Colors
    summary = terminal_manager.get_summary_line()
    if summary:
        print(f"{c.GRAY}  {summary} {c.DIM}(type /bg to view details){c.RESET}")
    return summary


def print_status_bar(terminal_manager, permission_mode: str = "auto", plan_mode: bool = False, pending_approval: bool = False):
    """
    Print a status bar at the bottom showing:
    - Permission mode (accept edits on/ask mode)
    - Background tasks count
    - Plan mode indicator
    Like Claude Code's status bar.
    """
    c = Colors
    parts = []
    
    # Permission mode indicator (cyan/teal colored like in the image)
    if permission_mode == "auto":
        parts.append(f"{c.CYAN}▸▸ accept edits on{c.RESET} {c.DIM}(← cycle){c.RESET}")
    elif permission_mode == "ask":
        parts.append(f"{c.YELLOW}▸▸ ask mode on{c.RESET} {c.DIM}(← cycle){c.RESET}")
    elif permission_mode == "command_ask":
        parts.append(f"{c.CYAN}▸▸ command ask mode{c.RESET} {c.DIM}(← cycle){c.RESET}")
    
    # Background tasks count
    bg_count = terminal_manager.get_running_count() if terminal_manager else 0
    if bg_count > 0:
        task_word = "task" if bg_count == 1 else "tasks"
        parts.append(f"{c.CYAN}{bg_count} background {task_word}{c.RESET}")
    
    # Plan mode indicator
    if plan_mode:
        parts.append(f"{c.RED}PLAN MODE{c.RESET}")
    
    # Pending approval indicator
    if pending_approval:
        parts.append(f"{c.YELLOW}⏳ awaiting approval{c.RESET}")
    
    # Print the status bar
    if parts:
        status_line = " · ".join(parts)
        print(f"{status_line}")


def print_background_details(terminal_manager):
    """Print detailed view of all background tasks."""
    c = Colors
    result = terminal_manager.get_all_status()
    
    total = result.get("total", 0)
    running = result.get("running", 0)
    
    print(f"\n{c.RED}━━━{c.RESET} {c.WHITE}{c.BOLD}Background Tasks{c.RESET} {c.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{c.RESET}")
    
    if total == 0:
        print(f"\n  {c.GRAY}No background tasks running{c.RESET}")
        print(f"  {c.DIM}Start a server with: 'run npm dev in background'{c.RESET}\n")
        return
    
    print(f"\n  {c.WHITE}Active: {c.SUCCESS}{running}{c.RESET}/{c.WHITE}{total}{c.RESET} tasks\n")
    
    for term in result.get("terminals", []):
        session_id = term.get("id", "")
        name = term.get("name", "Unknown")
        command = term.get("command", "")
        is_running = term.get("is_running", False)
        uptime = term.get("uptime", "0s")
        pid = term.get("pid", "")
        output = term.get("recent_output", "")
        
        # Status indicator
        if is_running:
            status = f"{c.SUCCESS}● RUNNING{c.RESET}"
        else:
            status = f"{c.ERROR}● STOPPED{c.RESET}"
        
        print(f"  {c.RED}┌─{c.RESET} {c.WHITE}{c.BOLD}{name}{c.RESET} {status}")
        print(f"  {c.RED}│{c.RESET}  {c.GRAY}ID: {session_id} │ PID: {pid} │ Uptime: {uptime}{c.RESET}")
        print(f"  {c.RED}│{c.RESET}  {c.GRAY}Command: {command[:50]}{'...' if len(command) > 50 else ''}{c.RESET}")
        
        # Show recent output
        if output:
            print(f"  {c.RED}│{c.RESET}")
            print(f"  {c.RED}│{c.RESET}  {c.DIM}Recent output:{c.RESET}")
            lines = output.strip().split('\n')[-5:]  # Last 5 lines
            for line in lines:
                print(f"  {c.RED}│{c.RESET}  {c.GRAY}│ {line[:60]}{'...' if len(line) > 60 else ''}{c.RESET}")
        
        print(f"  {c.RED}╰{'─' * 50}{c.RESET}\n")
    
    print(f"  {c.DIM}Commands: /kill <id> to stop │ /output <id> to view full output{c.RESET}\n")


def print_iteration(current: int, max_iter: int):
    """Print iteration counter - minimal style."""
    # Omit iteration display for cleaner output
    pass


def format_json(data: Any, indent: int = 2) -> str:
    """Format data as pretty JSON string."""
    return json.dumps(data, indent=indent, default=str)


def truncate_string(s: str, max_length: int = 500) -> str:
    """Truncate a string to maximum length."""
    if len(s) <= max_length:
        return s
    return s[:max_length] + f"... ({len(s) - max_length} more chars)"


def confirm_action(prompt: str) -> bool:
    """Ask user to confirm an action."""
    c = Colors
    response = input(f"{c.WARNING}{prompt} {c.GRAY}(y/N):{c.RESET} ").strip().lower()
    return response in ['y', 'yes']


def get_multiline_input(prompt: str = "Enter your request (empty line to finish):") -> str:
    """Get multi-line input from user."""
    c = Colors
    print(f"{c.GRAY}{prompt}{c.RESET}")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines)


def print_file_tree(items: list, prefix: str = ""):
    """Print a file tree structure."""
    c = Colors
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        current_prefix = "╰── " if is_last else "├── "
        
        if item["type"] == "directory":
            print(f"{c.GRAY}{prefix}{current_prefix}{c.RESET}{c.RED}{c.BOLD}{item['name']}/{c.RESET}")
        else:
            size = item.get("size", 0)
            size_str = format_size(size)
            print(f"{c.GRAY}{prefix}{current_prefix}{c.RESET}{c.WHITE}{item['name']}{c.RESET} {c.GRAY}({size_str}){c.RESET}")


def format_size(size_bytes: int) -> str:
    """Format byte size to human readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def print_help():
    """Print detailed help information."""
    c = Colors
    help_text = f"""
{c.RED}┌────────────────────────────────────────────────────────────────┐{c.RESET}
{c.RED}│{c.RESET}                      {c.WHITE}{c.BOLD}AADC HELP{c.RESET}                               {c.RED}│{c.RESET}
{c.RED}└────────────────────────────────────────────────────────────────┘{c.RESET}

{c.RED}━━━{c.RESET} {c.WHITE}{c.BOLD}Description{c.RESET} {c.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{c.RESET}

  {c.GRAY}An AI-powered coding assistant that creates, modifies, and
  manages your code projects through natural language.{c.RESET}

{c.RED}━━━{c.RESET} {c.WHITE}{c.BOLD}Available Models{c.RESET} {c.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{c.RESET}

  {c.GRAY}Google:{c.RESET}      {c.WHITE}gemini-3-pro-preview, gemini-2.5-pro{c.RESET}
  {c.GRAY}OpenAI:{c.RESET}      {c.WHITE}GPT-5.1, gpt-5-pro{c.RESET}
  {c.GRAY}Anthropic:{c.RESET}   {c.WHITE}claude-sonnet-4-5, claude-opus-4-5{c.RESET}

{c.RED}━━━{c.RESET} {c.WHITE}{c.BOLD}Permission Modes{c.RESET} {c.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{c.RESET}

  {c.RED}ask{c.RESET}            {c.GRAY}Ask before executing ANY tool{c.RESET}
  {c.RED}auto{c.RESET}           {c.GRAY}Execute all tools automatically{c.RESET} {c.DIM}(default){c.RESET}
  {c.RED}command_ask{c.RESET}    {c.GRAY}Only ask before shell commands{c.RESET}

{c.RED}━━━{c.RESET} {c.WHITE}{c.BOLD}Plan Mode & Approval{c.RESET} {c.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{c.RESET}

  {c.GRAY}The AI creates a plan for review before coding.{c.RESET}
  {c.RED}/plan{c.RESET}          {c.GRAY}Toggle plan mode on/off{c.RESET}
  {c.RED}plan: <msg>{c.RESET}    {c.GRAY}One-shot plan mode{c.RESET}
  {c.RED}/approve{c.RESET}       {c.GRAY}Approve the plan and start implementation{c.RESET}
  {c.RED}/reject <fb>{c.RESET}   {c.GRAY}Reject plan with feedback for revision{c.RESET}

{c.RED}━━━{c.RESET} {c.WHITE}{c.BOLD}Tool Call History{c.RESET} {c.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{c.RESET}

  {c.RED}/tools{c.RESET}         {c.GRAY}List recent tool calls{c.RESET}
  {c.RED}/tool <n>{c.RESET}      {c.GRAY}View full details of tool call #n{c.RESET}
  {c.RED}/tool{c.RESET}          {c.GRAY}View the last tool call{c.RESET}

{c.RED}━━━{c.RESET} {c.WHITE}{c.BOLD}General Commands{c.RESET} {c.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{c.RESET}

  {c.RED}/init{c.RESET}          {c.GRAY}Analyze codebase, generate summary for AI{c.RESET}
  {c.RED}/models{c.RESET}        {c.GRAY}List/switch AI models{c.RESET}
  {c.RED}/help{c.RESET}          {c.GRAY}Show this help{c.RESET}
  {c.RED}/pwd{c.RESET}           {c.GRAY}Print current directory{c.RESET}
  {c.RED}/ls{c.RESET}            {c.GRAY}List files in directory{c.RESET}
  {c.RED}/perm [mode]{c.RESET}   {c.GRAY}View/set/cycle permission mode{c.RESET}
  {c.RED}/todo{c.RESET}          {c.GRAY}View AI's task list{c.RESET}
  {c.RED}/bg{c.RESET}            {c.GRAY}Interactive background tasks viewer{c.RESET}
  {c.RED}/terminals{c.RESET}     {c.GRAY}List background terminals{c.RESET}
  {c.RED}/kill <id>{c.RESET}     {c.GRAY}Stop a terminal{c.RESET}
  {c.RED}/output <id>{c.RESET}   {c.GRAY}View terminal output{c.RESET}
  {c.RED}/memory{c.RESET}        {c.GRAY}List stored memories{c.RESET}
  {c.RED}/mem <query>{c.RESET}   {c.GRAY}Search memories{c.RESET}
  {c.RED}/forget <key>{c.RESET}  {c.GRAY}Remove a memory{c.RESET}
  {c.RED}/exit{c.RESET}          {c.GRAY}Exit AADC{c.RESET}

{c.RED}━━━{c.RESET} {c.WHITE}{c.BOLD}Quick Shortcuts{c.RESET} {c.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{c.RESET}

  {c.RED}← Left Arrow{c.RESET}   {c.GRAY}Cycle permission modes (auto → ask → command_ask){c.RESET}
  {c.RED}→ Right Arrow{c.RESET}  {c.GRAY}Open background task selector{c.RESET}
  
  {c.DIM}Press arrow keys at empty prompt before typing{c.RESET}

{c.RED}━━━{c.RESET} {c.WHITE}{c.BOLD}Examples{c.RESET} {c.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{c.RESET}

  {c.GRAY}"{c.WHITE}Create a snake game in JavaScript{c.GRAY}"{c.RESET}
  {c.GRAY}"{c.WHITE}Build a REST API with Express{c.GRAY}"{c.RESET}
  {c.GRAY}"{c.WHITE}plan: Create a portfolio website{c.GRAY}"{c.RESET}

{c.RED}━━━{c.RESET} {c.WHITE}{c.BOLD}CLI Options{c.RESET} {c.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{c.RESET}

  {c.RED}-d{c.RESET}             {c.GRAY}Set working directory{c.RESET}
  {c.RED}-p, --plan{c.RESET}     {c.GRAY}Start in plan mode{c.RESET}
  {c.RED}-m, --mode{c.RESET}     {c.GRAY}Set permission mode{c.RESET}
  {c.RED}--model{c.RESET}        {c.GRAY}Select AI model{c.RESET}
"""
    print(help_text)
