#!/usr/bin/env python3
"""
AADC - Agentic AI Developer Console
An AI-powered CLI tool for creating complete applications
"""

import os
import sys
import json
import argparse
import atexit
from pathlib import Path

from config import config, get_api_key, PERMISSION_MODES, AVAILABLE_MODELS
from utils import (
    print_header,
    print_welcome,
    print_user_prompt,
    print_error,
    print_info,
    print_success,
    print_warning,
    print_separator,
    print_help,
    print_file_tree,
    print_background_status,
    print_background_details,
    print_status_bar,
    Colors
)
from project_init import init_project, has_project_summary, get_summary_age
from terminal_manager import terminal_manager
from input_handler import InputHandler
from auth import auth_manager, require_auth, use_credit
from proxy_agent import create_proxy_agent, ProxyAgent

# Global input handler instance
input_handler = None


# All available commands with descriptions
AVAILABLE_COMMANDS = {
    "/help": "Show help message",
    "/exit": "Exit the agent",
    "/quit": "Exit the agent",
    "/q": "Exit the agent",
    "/pwd": "Print working directory",
    "/ls": "List files in current directory",
    "/model": "Show or switch AI models",
    "/models": "Show or switch AI models",
    "/init": "Initialize project context",
    "/perm": "Set/cycle permission mode",
    "/plan": "Toggle plan mode",
    "/terminals": "List active terminals",
    "/term": "List active terminals",
    "/bg": "Show background tasks (interactive)",
    "/background": "Show background tasks",
    "/tasks": "Interactive background task viewer",
    "/todo": "Show AI's task list",
    "/kill": "Kill a terminal session",
    "/output": "Show terminal output",
    "/tool": "Show last tool call output",
    "/tools": "Show all recent tool calls",
    "/memory": "Show stored memories",
    "/mem": "Show stored memories",
    "/forget": "Forget a memory",
    "/approve": "Approve the current plan",
    "/reject": "Reject the current plan with feedback",
    "/login": "Log in to your AADC account",
    "/logout": "Log out of your account",
    "/credits": "Check your credit balance",
    "/whoami": "Show logged in user info",
    "/github": "Connect to GitHub",
    "/gh": "Connect to GitHub",
    "/github-logout": "Disconnect from GitHub",
    "/repo": "Create GitHub repo for this project",
    "/push": "Push current changes to GitHub",
    "/auto-commit": "Toggle auto-commit to GitHub",
}

# Store recent tool calls for viewing
recent_tool_calls = []
MAX_TOOL_HISTORY = 50

# Store last plan for approval workflow
last_plan = None
plan_pending_approval = False


def show_command_suggestions(partial: str):
    """Show commands that match the partial input."""
    if not partial.startswith("/"):
        return
    
    c = Colors
    matches = [(cmd, desc) for cmd, desc in AVAILABLE_COMMANDS.items() 
               if cmd.startswith(partial.lower())]
    
    if matches and partial != matches[0][0]:  # Don't show if exact match
        print(f"{c.GRAY}╭─ Matching commands:{c.RESET}")
        for cmd, desc in matches[:5]:  # Show max 5
            print(f"{c.GRAY}│  {c.RED}{cmd}{c.GRAY} - {desc}{c.RESET}")
        print(f"{c.GRAY}╰─{c.RESET}")


def get_input_with_plan_mode(cwd: str, plan_mode: bool) -> tuple:
    """
    Get user input with support for plan mode toggle and quick shortcuts.
    Returns (user_input, new_plan_mode).
    
    Quick shortcuts:
    - '>' or 'pc': Cycle permission modes (auto -> ask -> command_ask)
    - '^' or '/bg': Open background task selector
    
    Typing 'plan:' prefix enables plan mode for that message.
    """
    global plan_pending_approval, input_handler
    c = Colors
    
    # Initialize input handler if needed
    if input_handler is None:
        from input_handler import InputHandler
        input_handler = InputHandler(terminal_manager, config)
    
    # Print status bar (like Claude Code)
    print()  # Empty line before status bar
    print_status_bar(
        terminal_manager, 
        permission_mode=config.permission_mode,
        plan_mode=plan_mode,
        pending_approval=plan_pending_approval
    )
    
    # Show plan approval hint if pending
    if plan_pending_approval:
        print(f"{c.YELLOW}📋 Plan pending: {c.RED}/approve{c.YELLOW} or {c.RED}/reject <feedback>{c.RESET}")
    
    # Show quick shortcuts hint
    print(f"{c.DIM}← permission · → tasks{c.RESET}")
    
    # Try advanced input with special key handling
    try:
        user_input, new_plan_mode, action = input_handler.get_input_advanced(
            f"{c.GRAY}>{c.RESET} ", 
            plan_mode
        )
        
        # Handle special actions
        if action == "permission_cycled":
            print(f"{c.CYAN}✓ Permission mode: {config.permission_mode}{c.RESET}")
            return get_input_with_plan_mode(cwd, plan_mode)  # Recurse to show new status
        
        if action == "task_selected":
            return get_input_with_plan_mode(cwd, plan_mode)  # Recurse after returning from task view
        
    except Exception:
        # Fallback to simple input
        user_input = input(f"{c.GRAY}>{c.RESET} ").strip()
        new_plan_mode = plan_mode
        
        if user_input.lower().startswith("plan:"):
            user_input = user_input[5:].strip()
            new_plan_mode = True
    
    # Show command suggestions if typing a command
    if user_input.startswith("/") and len(user_input) > 1:
        show_command_suggestions(user_input.split()[0])
    
    return user_input, new_plan_mode


def handle_command(command: str, agent) -> bool:
    """
    Handle special commands. Returns True if command was handled.
    """
    global plan_pending_approval, last_plan
    
    cmd_parts = command.split(maxsplit=1)
    cmd = cmd_parts[0].lower()
    arg = cmd_parts[1] if len(cmd_parts) > 1 else ""
    
    if cmd == "/exit" or cmd == "/quit" or cmd == "/q":
        agent.cleanup()
        print(f"\n{Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
        print(f"{Colors.WHITE}Goodbye! Happy coding!{Colors.RESET}")
        print(f"{Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}\n")
        sys.exit(0)
    
    elif cmd == "/help" or cmd == "/?":
        print_help()
        return True
    
    elif cmd == "/pwd":
        print_info(f"Current directory: {agent.working_directory}")
        return True
    
    elif cmd == "/ls":
        from tools import list_files
        result = list_files(agent.working_directory)
        if result["success"]:
            print(f"\n{Colors.RED}━━━{Colors.RESET} {Colors.WHITE}{Colors.BOLD}Files{Colors.RESET} {Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}\n")
            if result["items"]:
                print_file_tree(result["items"])
            else:
                print(f"{Colors.GRAY}(empty directory){Colors.RESET}")
        else:
            print_error(result["error"])
        return True
    
    elif cmd == "/model" or cmd == "/models":
        if not arg:
            # Show current model and available options
            print(f"\n{Colors.RED}━━━{Colors.RESET} {Colors.WHITE}{Colors.BOLD}Available Models{Colors.RESET} {Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}\n")
            
            current_provider = None
            for model_id, info in AVAILABLE_MODELS.items():
                provider = info["provider"]
                is_coming_soon = info.get("coming_soon", False)
                
                # Print provider header
                if provider != current_provider:
                    current_provider = provider
                    provider_name = {
                        "auto": "SMART ROUTING",
                        "gemini": "Google Gemini", 
                        "openai": "OpenAI", 
                        "anthropic": "Anthropic",
                        "openrouter": "OpenRouter"
                    }
                    print(f"  {Colors.GRAY}{provider_name.get(provider, provider).upper()}{Colors.RESET}")
                
                if is_coming_soon:
                    marker = f"{Colors.GRAY}○{Colors.RESET}"
                    status = f" {Colors.YELLOW}🚧 Coming Soon{Colors.RESET}"
                    print(f"    {marker} {Colors.GRAY}{model_id}{Colors.RESET}{status}")
                elif model_id == config.model:
                    marker = f"{Colors.RED}●{Colors.RESET}"
                    current = f" {Colors.SUCCESS}← current{Colors.RESET}"
                    
                    # Show additional info for auto mode
                    if model_id == "auto":
                        auto_info = f" {Colors.GRAY}(nova-2-lite ↔ gemini-3-pro-preview){Colors.RESET}"
                        print(f"    {marker} {Colors.WHITE}{model_id}{Colors.RESET}{current}{auto_info}")
                    else:
                        print(f"    {marker} {Colors.WHITE}{model_id}{Colors.RESET}{current}")
                else:
                    marker = f"{Colors.GRAY}○{Colors.RESET}"
                    
                    # Show additional info for auto mode
                    if model_id == "auto":
                        auto_info = f" {Colors.GRAY}(nova-2-lite ↔ gemini-3-pro-preview){Colors.RESET}"
                        print(f"    {marker} {Colors.WHITE}{model_id}{Colors.RESET}{auto_info}")
                    else:
                        print(f"    {marker} {Colors.WHITE}{model_id}{Colors.RESET}")
            
            print(f"\n{Colors.GRAY}Usage: /models <model_name>{Colors.RESET}")
        else:
            model_name = arg.strip()
            if model_name in AVAILABLE_MODELS:
                model_info = AVAILABLE_MODELS[model_name]
                if model_info.get("coming_soon", False):
                    print_error(f"{model_name} is coming soon! Please use a Gemini model for now.")
                    return True
                config.model = model_name
                print_success(f"Switched to {model_name}")
                return "reinit"  # Signal to reinitialize the agent
            else:
                print_error(f"Unknown model: {model_name}")
                print(f"{Colors.GRAY}Available: {', '.join(AVAILABLE_MODELS.keys())}{Colors.RESET}")
        return True
    
    elif cmd == "/init":
        print(f"\n{Colors.GRAY}◌ Analyzing project...{Colors.RESET}")
        result = init_project(agent.working_directory)
        
        if result["success"]:
            stats = result["stats"]
            print(f"\n{Colors.RED}━━━{Colors.RESET} {Colors.WHITE}{Colors.BOLD}Project Initialized{Colors.RESET} {Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}\n")
            print(f"  {Colors.WHITE}Files analyzed:{Colors.RESET} {stats['total_files']}")
            print(f"  {Colors.WHITE}Total lines:{Colors.RESET} {stats['total_lines']:,}")
            print(f"  {Colors.WHITE}Summary saved:{Colors.RESET} {Colors.GRAY}aadc.md{Colors.RESET}")
            print(f"\n{Colors.SUCCESS}✓ AI will now use this context for better understanding.{Colors.RESET}")
        else:
            print_error(result["error"])
        return True
    
    elif cmd == "/perm":
        if not arg:
            # Show current mode and options
            print(f"\n{Colors.RED}━━━{Colors.RESET} {Colors.WHITE}{Colors.BOLD}Permission Modes{Colors.RESET} {Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}\n")
            for mode, desc in PERMISSION_MODES.items():
                if mode == config.permission_mode:
                    marker = f"{Colors.RED}●{Colors.RESET}"
                    current = f" {Colors.SUCCESS}← current{Colors.RESET}"
                else:
                    marker = f"{Colors.GRAY}○{Colors.RESET}"
                    current = ""
                print(f"  {marker} {Colors.RED}{mode}{Colors.RESET}  {Colors.GRAY}{desc}{Colors.RESET}{current}")
            print(f"\n{Colors.GRAY}Usage: /perm <mode> or /perm cycle{Colors.RESET}")
        elif arg.lower() == "cycle":
            # Cycle through permission modes
            modes = list(PERMISSION_MODES.keys())
            current_idx = modes.index(config.permission_mode)
            next_idx = (current_idx + 1) % len(modes)
            config.permission_mode = modes[next_idx]
            print_success(f"Permission mode: {config.permission_mode} - {PERMISSION_MODES[config.permission_mode]}")
        else:
            mode = arg.lower().strip()
            if mode in PERMISSION_MODES:
                config.permission_mode = mode
                print_success(f"Permission mode: {mode} - {PERMISSION_MODES[mode]}")
            else:
                print_error(f"Unknown mode: {mode}")
                print(f"{Colors.GRAY}Available: {', '.join(PERMISSION_MODES.keys())}, cycle{Colors.RESET}")
        return True
    
    elif cmd == "/plan":
        # Toggle plan mode
        agent.plan_mode = not agent.plan_mode
        config.plan_mode = agent.plan_mode
        if agent.plan_mode:
            print_success("Plan mode ENABLED - AI will create plan.md before coding")
        else:
            print_info("Plan mode DISABLED - AI will code directly")
        return True
    
    elif cmd == "/terminals" or cmd == "/term":
        from terminal_manager import terminal_manager
        result = terminal_manager.list_terminals()
        
        if result["count"] == 0:
            print(f"\n{Colors.GRAY}No active terminal sessions{Colors.RESET}")
        else:
            print(f"\n{Colors.RED}━━━{Colors.RESET} {Colors.WHITE}{Colors.BOLD}Active Terminals{Colors.RESET} {Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}\n")
            for term in result["terminals"]:
                status = f"{Colors.SUCCESS}●{Colors.RESET}" if term["is_running"] else f"{Colors.ERROR}●{Colors.RESET}"
                server = f" {Colors.RED}[SERVER]{Colors.RESET}" if term["is_server"] else ""
                print(f"  {status} {Colors.WHITE}{Colors.BOLD}{term['id']}{Colors.RESET}: {term['name']}{server}")
                print(f"    {Colors.GRAY}├─ Command: {term['command'][:45]}{'...' if len(term['command']) > 45 else ''}{Colors.RESET}")
                print(f"    {Colors.GRAY}╰─ PID: {term['pid']} │ Uptime: {term['uptime']}{Colors.RESET}")
        return True
    
    elif cmd == "/bg" or cmd == "/background" or cmd == "/tasks":
        # Interactive background tasks view
        global input_handler
        if input_handler is None:
            input_handler = InputHandler(terminal_manager, config)
        
        tasks = terminal_manager.get_all_status()
        terminals = tasks.get("terminals", [])
        
        if not terminals:
            print(f"\n{Colors.GRAY}No background tasks running.{Colors.RESET}")
            print(f"{Colors.DIM}Start a server with: 'run npm dev in background'{Colors.RESET}")
            return True
        
        # Show tasks list with interactive option
        print_background_details(terminal_manager)
        print(f"{Colors.CYAN}Enter task ID to view details, or press Enter to continue:{Colors.RESET}")
        
        try:
            task_id = input(f"{Colors.GRAY}>{Colors.RESET} ").strip()
            if task_id:
                # Check if valid task ID
                if any(t["id"] == task_id for t in terminals):
                    input_handler.show_terminal_view(task_id)
                else:
                    print(f"{Colors.RED}Task not found: {task_id}{Colors.RESET}")
        except (KeyboardInterrupt, EOFError):
            pass
        
        return True
    
    elif cmd == "/todo":
        from tools import manage_todo
        result = manage_todo(action="list")
        
        summary = result.get("summary", {})
        tasks = result.get("tasks", [])
        
        if not tasks:
            print(f"\n{Colors.GRAY}No tasks in todo list{Colors.RESET}")
            print(f"{Colors.DIM}The AI will create a todo list when working on complex tasks.{Colors.RESET}")
        else:
            print(f"\n{Colors.RED}━━━{Colors.RESET} {Colors.WHITE}{Colors.BOLD}Todo List{Colors.RESET} {Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}\n")
            print(f"  {Colors.WHITE}Progress:{Colors.RESET} {Colors.SUCCESS}{summary.get('done', 0)}{Colors.RESET}/{summary.get('total', 0)} completed\n")
            
            # Group by status
            pending = [t for t in tasks if t["status"] == "pending"]
            in_progress = [t for t in tasks if t["status"] == "in_progress"]
            done = [t for t in tasks if t["status"] == "done"]
            
            if in_progress:
                print(f"  {Colors.YELLOW}⚡ In Progress:{Colors.RESET}")
                for task in in_progress:
                    print(f"     🔄 #{task['id']}: {task['text']}")
                print()
            
            if pending:
                print(f"  {Colors.WHITE}📋 Pending:{Colors.RESET}")
                for task in pending:
                    print(f"     ⬜ #{task['id']}: {task['text']}")
                print()
            
            if done:
                print(f"  {Colors.SUCCESS}✓ Completed:{Colors.RESET}")
                for task in done:
                    print(f"     {Colors.DIM}✅ #{task['id']}: {task['text']}{Colors.RESET}")
                print()
        
        return True
    
    elif cmd == "/kill":
        if not arg:
            print_error("Usage: /kill <session_id>")
            print(f"{Colors.DIM}Use /terminals to see active sessions{Colors.RESET}")
        else:
            from terminal_manager import terminal_manager
            result = terminal_manager.close_terminal(arg.strip())
            if result["success"]:
                print_success(result["message"])
            else:
                print_error(result["error"])
        return True
    
    elif cmd == "/output":
        if not arg:
            print_error("Usage: /output <session_id>")
        else:
            from terminal_manager import terminal_manager
            result = terminal_manager.get_terminal_status(arg.strip())
            if result["success"]:
                print(f"\n{Colors.RED}━━━{Colors.RESET} {Colors.WHITE}{Colors.BOLD}Output: {result['name']}{Colors.RESET} {Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}\n")
                if result["recent_output"]:
                    print(f"{Colors.GRAY}{result['recent_output']}{Colors.RESET}")
                else:
                    print(f"{Colors.GRAY}(no recent output){Colors.RESET}")
            else:
                print_error(result["error"])
        return True
    
    elif cmd == "/memory" or cmd == "/mem":
        from memory import memory_manager
        
        if not arg:
            result = memory_manager.list_memories()
            if result["count"] == 0:
                print(f"\n{Colors.GRAY}No memories stored yet{Colors.RESET}")
            else:
                print(f"\n{Colors.RED}━━━{Colors.RESET} {Colors.WHITE}{Colors.BOLD}Stored Memories{Colors.RESET} {Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}\n")
                for mem in result["memories"]:
                    print(f"  {Colors.RED}●{Colors.RESET} {Colors.WHITE}{Colors.BOLD}{mem['key']}{Colors.RESET}")
                    print(f"    {Colors.GRAY}├─ {mem['value']}{Colors.RESET}")
                    print(f"    {Colors.GRAY}╰─ [{mem['category']}]{Colors.RESET}")
        else:
            # Search memories
            result = memory_manager.search_memories(arg)
            if result["count"] == 0:
                print(f"\n{Colors.GRAY}No memories found for: {arg}{Colors.RESET}")
            else:
                print(f"\n{Colors.RED}━━━{Colors.RESET} {Colors.WHITE}{Colors.BOLD}Search Results{Colors.RESET} {Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}\n")
                for mem in result["results"]:
                    print(f"  {Colors.RED}●{Colors.RESET} {Colors.WHITE}{Colors.BOLD}{mem['key']}{Colors.RESET}: {Colors.GRAY}{mem['value']}{Colors.RESET}")
        return True
    
    elif cmd == "/forget":
        if not arg:
            print_error("Usage: /forget <key>")
        else:
            from memory import memory_manager
            result = memory_manager.forget(arg.strip())
            if result["success"]:
                print_success(result["message"])
            else:
                print_error(result["error"])
        return True
    
    elif cmd == "/tool":
        # Show last tool call output
        if not recent_tool_calls:
            print(f"\n{Colors.GRAY}No recent tool calls{Colors.RESET}")
        else:
            if arg:
                # Show specific tool by index
                try:
                    idx = int(arg) - 1
                    if 0 <= idx < len(recent_tool_calls):
                        tc = recent_tool_calls[idx]
                        print(f"\n{Colors.RED}━━━{Colors.RESET} {Colors.WHITE}{Colors.BOLD}Tool Call #{idx + 1}: {tc['name']}{Colors.RESET} {Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}\n")
                        print(f"{Colors.CYAN}Arguments:{Colors.RESET}")
                        print(json.dumps(tc['args'], indent=2))
                        print(f"\n{Colors.CYAN}Result:{Colors.RESET}")
                        print(json.dumps(tc['result'], indent=2))
                    else:
                        print_error(f"Invalid tool index. Use 1-{len(recent_tool_calls)}")
                except ValueError:
                    print_error("Usage: /tool <number>")
            else:
                # Show last tool call
                tc = recent_tool_calls[-1]
                print(f"\n{Colors.RED}━━━{Colors.RESET} {Colors.WHITE}{Colors.BOLD}Last Tool Call: {tc['name']}{Colors.RESET} {Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}\n")
                print(f"{Colors.CYAN}Arguments:{Colors.RESET}")
                print(json.dumps(tc['args'], indent=2))
                print(f"\n{Colors.CYAN}Result:{Colors.RESET}")
                print(json.dumps(tc['result'], indent=2))
        return True
    
    elif cmd == "/tools":
        # Show all recent tool calls
        if not recent_tool_calls:
            print(f"\n{Colors.GRAY}No recent tool calls{Colors.RESET}")
        else:
            print(f"\n{Colors.RED}━━━{Colors.RESET} {Colors.WHITE}{Colors.BOLD}Recent Tool Calls{Colors.RESET} {Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}\n")
            for i, tc in enumerate(recent_tool_calls[-20:], 1):  # Show last 20
                status = f"{Colors.SUCCESS}✓{Colors.RESET}" if tc.get('success', True) else f"{Colors.ERROR}✗{Colors.RESET}"
                args_preview = str(tc['args'])[:40] + "..." if len(str(tc['args'])) > 40 else str(tc['args'])
                print(f"  {Colors.RED}{i:2}{Colors.RESET}. {status} {Colors.WHITE}{tc['name']}{Colors.RESET} {Colors.GRAY}{args_preview}{Colors.RESET}")
            print(f"\n{Colors.GRAY}Use /tool <number> to see full details{Colors.RESET}")
        return True
    
    elif cmd == "/approve":
        if not plan_pending_approval:
            print_error("No plan pending approval")
        else:
            plan_pending_approval = False
            config.plan_mode = False
            print_success("Plan approved! Implementing...")
            # Return special signal to trigger implementation
            return "approve_plan"
    
    elif cmd == "/reject":
        if not plan_pending_approval:
            print_error("No plan pending approval")
        else:
            feedback = arg if arg else "Please revise the plan"
            plan_pending_approval = False
            print_info(f"Plan rejected with feedback: {feedback}")
            # Return special signal with feedback
            return ("reject_plan", feedback)
    
    elif cmd == "/login":
        if auth_manager.is_logged_in():
            user = auth_manager.get_user()
            print(f"\n{Colors.SUCCESS}Already logged in as {user.get('displayName', 'User')}{Colors.RESET}")
            print(f"{Colors.GRAY}Credits: {user.get('credits', 0)} │ Plan: {user.get('plan', 'free')}{Colors.RESET}")
        else:
            auth_manager.login()
        return True
    
    elif cmd == "/logout":
        if auth_manager.is_logged_in():
            user = auth_manager.get_user()
            auth_manager.logout()
            print_success(f"Logged out. Goodbye, {user.get('displayName', 'User')}!")
        else:
            print_info("Not currently logged in")
        return True
    
    elif cmd == "/credits":
        if auth_manager.is_logged_in():
            print(f"{Colors.GRAY}Syncing credits from server...{Colors.RESET}")
            auth_manager.sync_user_data()  # Sync from Firestore
            user = auth_manager.get_user()
            credits = user.get('credits', 0)
            plan = user.get('plan', 'free')
            print(f"\n{Colors.RED}━━━{Colors.RESET} {Colors.WHITE}{Colors.BOLD}Credits{Colors.RESET} {Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}\n")
            print(f"  {Colors.WHITE}Balance:{Colors.RESET} {Colors.SUCCESS}{credits}{Colors.RESET} credits")
            print(f"  {Colors.WHITE}Plan:{Colors.RESET} {plan.capitalize()}")
            print(f"\n{Colors.GRAY}Visit aadc.dev/pricing to purchase more credits{Colors.RESET}")
        else:
            print_error("Not logged in. Use /login to authenticate.")
        return True
    
    elif cmd == "/whoami":
        if auth_manager.is_logged_in():
            print(f"{Colors.GRAY}Syncing account data...{Colors.RESET}")
            auth_manager.sync_user_data()  # Sync from Firestore
            user = auth_manager.get_user()
            print(f"\n{Colors.RED}━━━{Colors.RESET} {Colors.WHITE}{Colors.BOLD}Account{Colors.RESET} {Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}\n")
            print(f"  {Colors.WHITE}Name:{Colors.RESET} {user.get('displayName', 'N/A')}")
            print(f"  {Colors.WHITE}Email:{Colors.RESET} {user.get('email', 'N/A')}")
            print(f"  {Colors.WHITE}Credits:{Colors.RESET} {user.get('credits', 0)}")
            print(f"  {Colors.WHITE}Plan:{Colors.RESET} {user.get('plan', 'free').capitalize()}")
        else:
            print_error("Not logged in. Use /login to authenticate.")
        return True
    
    # GitHub commands
    elif cmd in ["/github", "/gh"]:
        from github_integration import github_integration
        import asyncio
        
        if github_integration.is_authenticated():
            print_success(f"Already connected to GitHub as {github_integration.username}")
        else:
            print(f"\n{Colors.CYAN}Connecting to GitHub...{Colors.RESET}\n")
            if asyncio.run(github_integration.authenticate_with_device_flow()):
                print_success("GitHub connected successfully!")
            else:
                print_error("Failed to connect to GitHub")
        return True
    
    elif cmd == "/github-logout":
        from github_integration import github_integration
        
        if github_integration.is_authenticated():
            username = github_integration.username
            github_integration.logout()
            print_success(f"Disconnected from GitHub ({username})")
        else:
            print_info("Not connected to GitHub")
        return True
    
    elif cmd == "/repo":
        from github_integration import github_integration
        import asyncio
        
        if not github_integration.is_authenticated():
            print_error("Not connected to GitHub. Use /github to connect.")
            return True
        
        # Get repo name from project directory
        project_path = agent.working_directory
        repo_name = Path(project_path).name
        
        print(f"{Colors.GRAY}Creating GitHub repo '{repo_name}'...{Colors.RESET}")
        
        # Create repo
        repo_url = asyncio.run(github_integration.create_repo(
            repo_name,
            description=f"Project created with AADC",
            private=False
        ))
        
        if repo_url:
            # Initialize git and add remote
            if github_integration.init_git_repo(project_path):
                if github_integration.add_remote(project_path, repo_name):
                    print_success(f"Created repo: {repo_url}")
                    print(f"{Colors.GRAY}Git remote added. Use /push to push your code.{Colors.RESET}")
                else:
                    print_warning(f"Repo created but failed to add remote: {repo_url}")
            else:
                print_warning(f"Repo created but failed to init git: {repo_url}")
        else:
            print_error("Failed to create repository")
        return True
    
    elif cmd == "/push":
        from github_integration import github_integration
        
        if not github_integration.is_authenticated():
            print_error("Not connected to GitHub. Use /github to connect.")
            return True
        
        project_path = agent.working_directory
        print(f"{Colors.GRAY}Pushing to GitHub...{Colors.RESET}")
        
        if github_integration.commit_and_push(project_path, "Update from AADC"):
            print_success("Successfully pushed to GitHub!")
        else:
            print_error("Failed to push to GitHub. Make sure you have a repo set up with /repo")
        return True
    
    elif cmd == "/auto-commit":
        current = config.github_auto_commit
        config.github_auto_commit = not current
        
        if config.github_auto_commit:
            from github_integration import github_integration
            if not github_integration.is_authenticated():
                print_warning("Auto-commit enabled, but you're not connected to GitHub.")
                print(f"{Colors.GRAY}Use /github to connect and /repo to create a repository.{Colors.RESET}")
            else:
                print_success("Auto-commit enabled. Changes will be pushed to GitHub automatically.")
        else:
            print_success("Auto-commit disabled.")
        return True
    
    elif cmd.startswith("/"):
        print_error(f"Unknown command: {cmd}")
        print(f"{Colors.GRAY}Type /help for available commands{Colors.RESET}")
        return True
    
    return False


def run_single_message_streaming(agent, message: str) -> str:
    """
    Run a message with real-time streaming output and tool call storage.
    Shows thinking, tool calls as they happen, and stores results for later viewing.
    """
    global recent_tool_calls, plan_pending_approval, last_plan
    
    from utils import print_thinking, clear_thinking, print_tool_call, print_tool_result, print_assistant_message, print_iteration, print_task_complete, confirm_action
    
    final_text = []
    print_thinking()
    
    has_tool_calls = False
    current_tool_index = len(recent_tool_calls)
    
    # Create confirmation callback that uses confirm_action
    def confirm_callback(tool_name, tool_args):
        return confirm_action(f"Execute {tool_name}?")
    
    for event in agent.send_message(message, confirm_callback=confirm_callback):
        clear_thinking()
        
        if event["type"] == "text":
            print_assistant_message(event["content"])
            final_text.append(event["content"])
            
            # Check if this looks like a plan (for plan approval flow)
            if config.plan_mode and ("## " in event["content"] or "### " in event["content"]):
                last_plan = event["content"]
                plan_pending_approval = True
                
        elif event["type"] == "tool_call":
            has_tool_calls = True
            print_iteration(event["iteration"], event["max_iterations"])
            print_tool_call(event["name"], event["args"])
            
            # Store the tool call for later viewing
            tool_entry = {
                "name": event["name"],
                "args": event["args"],
                "result": None,
                "success": None
            }
            recent_tool_calls.append(tool_entry)
            
            # Trim history if too long
            if len(recent_tool_calls) > MAX_TOOL_HISTORY:
                recent_tool_calls = recent_tool_calls[-MAX_TOOL_HISTORY:]
            
            # Note: Confirmation is handled by callback passed to agent.send_message
            # The agent will yield tool_skipped event if user denies
                    
        elif event["type"] == "tool_result":
            print_tool_result(event["result"], event["success"], event.get("name"))
            
            # Update the stored tool call with result
            if recent_tool_calls:
                recent_tool_calls[-1]["result"] = event["result"]
                recent_tool_calls[-1]["success"] = event["success"]
        
        elif event["type"] == "tool_skipped":
            print(f"{Colors.WARNING}   └─ ⏭️  Skipped: {event.get('reason', 'Denied by user')}{Colors.RESET}")
            # Update stored tool call
            if recent_tool_calls:
                recent_tool_calls[-1]["result"] = {"skipped": True, "reason": event.get("reason")}
                recent_tool_calls[-1]["success"] = False
                
        elif event["type"] == "warning":
            print_warning(event["content"])
        elif event["type"] == "error":
            print_error(event["content"])
            final_text.append(f"Error: {event['content']}")
    
    # Print completion message
    if has_tool_calls:
        print_task_complete()
        # Show hint about viewing tool outputs
        tool_count = len(recent_tool_calls) - current_tool_index
        if tool_count > 0:
            print(f"{Colors.GRAY}💡 Tip: Use /tools to see {tool_count} tool call(s) or /tool <n> for details{Colors.RESET}")
    
    # If in plan mode, remind user to approve
    if plan_pending_approval:
        print(f"\n{Colors.YELLOW}📋 Plan created! Review above and use:{Colors.RESET}")
        print(f"   {Colors.RED}/approve{Colors.RESET} - Implement the plan")
        print(f"   {Colors.RED}/reject <feedback>{Colors.RESET} - Request changes")
    
    return "\n".join(final_text)


def run_pipe_mode():
    """
    Run in pipe mode for desktop app integration.
    Reads from stdin, writes to stdout without interactive UI.
    """
    import sys
    import json
    from tools import list_files
    
    # Disable Rich formatting
    os.environ["NO_COLOR"] = "1"
    os.environ["TERM"] = "dumb"
    
    # Flush output immediately
    sys.stdout.reconfigure(line_buffering=True)
    
    # Print ready signal
    print("[AADC_READY]", flush=True)
    
    # Check authentication
    if not auth_manager.is_logged_in():
        # Get login URL and send to desktop app
        login_url = auth_manager.get_login_url()
        print(f"[AADC_LOGIN_REQUIRED] {login_url}", flush=True)
        # Start server and wait for login
        if auth_manager.start_login_server_and_wait(timeout=300):
            print("[AADC_INFO] Login successful!", flush=True)
        else:
            print("[AADC_ERROR] Login failed or timed out.", flush=True)
            sys.exit(1)
    
    # Check beta access
    if not auth_manager.has_beta_access():
        print("[AADC_BETA_REQUIRED] https://aadc-website.vercel.app/beta", flush=True)
        sys.exit(1)
    
    user = auth_manager.get_user()
    print(f"[AADC_USER] {user.get('displayName', 'User')} | Credits: {user.get('credits', 0)} | Plan: {user.get('plan', 'free')}", flush=True)
    
    # Create proxy agent
    agent = create_proxy_agent()
    if agent is None:
        print("[AADC_ERROR] Failed to initialize agent.", flush=True)
        sys.exit(1)
    
    # Register cleanup
    atexit.register(agent.cleanup)
    
    print(f"[AADC_CWD] {agent.working_directory}", flush=True)
    
    # Check for project summary
    if has_project_summary(agent.working_directory):
        age = get_summary_age(agent.working_directory)
        if age is not None and age < 24:
            print("[AADC_INFO] Project context loaded (aadc.md)", flush=True)
    
    # Main loop - read from stdin
    try:
        for line in sys.stdin:
            message = line.strip()
            if not message:
                continue
            
            # Handle commands
            cmd = message.lower().split()[0] if message.startswith("/") else ""
            arg = message[len(cmd):].strip() if cmd else ""
            
            # Exit commands
            if cmd in ["/exit", "/quit", "/q"]:
                print("[AADC_EXIT]", flush=True)
                break
            
            # Help command
            elif cmd == "/help":
                help_text = """Available Commands:
/help - Show this help message
/exit, /quit, /q - Exit the app
/pwd - Print working directory
/ls - List files in current directory
/model, /models - Show or switch AI models
/init - Initialize project context
/credits - Check your credit balance
/whoami - Show logged in user info
/logout - Log out of your account"""
                for help_line in help_text.split("\n"):
                    print(f"[AADC_TEXT] {help_line}", flush=True)
                print("[AADC_DONE]", flush=True)
                continue
            
            # PWD command
            elif cmd == "/pwd":
                print(f"[AADC_TEXT] Current directory: {agent.working_directory}", flush=True)
                print("[AADC_DONE]", flush=True)
                continue
            
            # LS command
            elif cmd == "/ls":
                result = list_files(agent.working_directory)
                if result["success"]:
                    print("[AADC_TEXT] Files:", flush=True)
                    for item in result.get("items", []):
                        icon = "📁" if item.get("is_dir") else "📄"
                        print(f"[AADC_TEXT]   {icon} {item.get('name', '')}", flush=True)
                else:
                    print(f"[AADC_ERROR] {result.get('error', 'Failed to list files')}", flush=True)
                print("[AADC_DONE]", flush=True)
                continue
            
            # Models command
            elif cmd in ["/model", "/models"]:
                if not arg:
                    print("[AADC_TEXT] Available Models:", flush=True)
                    for model_id, info in AVAILABLE_MODELS.items():
                        is_current = "← current" if model_id == config.model else ""
                        is_coming = "🚧 Coming Soon" if info.get("coming_soon") else ""
                        status = is_current or is_coming
                        print(f"[AADC_TEXT]   {'●' if model_id == config.model else '○'} {model_id} {status}", flush=True)
                    print("[AADC_TEXT] ", flush=True)
                    print("[AADC_TEXT] Usage: /models <model_name>", flush=True)
                else:
                    if arg in AVAILABLE_MODELS:
                        if AVAILABLE_MODELS[arg].get("coming_soon"):
                            print(f"[AADC_ERROR] {arg} is coming soon!", flush=True)
                        else:
                            config.model = arg
                            print(f"[AADC_TEXT] Switched to {arg}", flush=True)
                    else:
                        print(f"[AADC_ERROR] Unknown model: {arg}", flush=True)
                print("[AADC_DONE]", flush=True)
                continue
            
            # Init command
            elif cmd == "/init":
                print("[AADC_THINKING]", flush=True)
                print("[AADC_TEXT] Analyzing project structure...", flush=True)
                try:
                    summary = init_project(agent.working_directory)
                    if summary:
                        print("[AADC_TEXT] Project context created (aadc.md)", flush=True)
                        agent.project_summary = summary
                    else:
                        print("[AADC_ERROR] Failed to initialize project.", flush=True)
                except Exception as e:
                    print(f"[AADC_ERROR] {str(e)}", flush=True)
                print("[AADC_DONE]", flush=True)
                continue
            
            # Credits command
            elif cmd == "/credits":
                auth_manager.refresh_credits()
                user = auth_manager.get_user()
                print(f"[AADC_TEXT] Credits: {user.get('credits', 0)}", flush=True)
                print(f"[AADC_TEXT] Plan: {user.get('plan', 'free')}", flush=True)
                print("[AADC_DONE]", flush=True)
                continue
            
            # Whoami command
            elif cmd == "/whoami":
                user = auth_manager.get_user()
                print(f"[AADC_TEXT] Name: {user.get('displayName', 'Unknown')}", flush=True)
                print(f"[AADC_TEXT] Email: {user.get('email', 'Unknown')}", flush=True)
                print(f"[AADC_TEXT] Plan: {user.get('plan', 'free')}", flush=True)
                print(f"[AADC_TEXT] Credits: {user.get('credits', 0)}", flush=True)
                print("[AADC_DONE]", flush=True)
                continue
            
            # Logout command
            elif cmd == "/logout":
                auth_manager.logout()
                print("[AADC_TEXT] Logged out successfully.", flush=True)
                print("[AADC_EXIT]", flush=True)
                break
            
            # GitHub commands
            elif cmd in ["/github", "/gh"]:
                from github_integration import github_integration
                import asyncio
                
                if github_integration.is_authenticated():
                    print(f"[AADC_TEXT] Already connected as {github_integration.username}", flush=True)
                else:
                    print("[AADC_TEXT] Opening browser for GitHub authentication...", flush=True)
                    if asyncio.run(github_integration.authenticate_with_device_flow()):
                        print(f"[AADC_TEXT] ✓ Connected to GitHub as {github_integration.username}", flush=True)
                    else:
                        print("[AADC_ERROR] Failed to connect to GitHub", flush=True)
                print("[AADC_DONE]", flush=True)
                continue
            
            elif cmd == "/repo":
                from github_integration import github_integration
                import asyncio
                
                if not github_integration.is_authenticated():
                    print("[AADC_ERROR] Not connected to GitHub. Use /github first", flush=True)
                    print("[AADC_DONE]", flush=True)
                    continue
                
                repo_name = Path(agent.working_directory).name
                print(f"[AADC_TEXT] Creating repo '{repo_name}'...", flush=True)
                
                repo_url = asyncio.run(github_integration.create_repo(
                    repo_name,
                    description="Project created with AADC",
                    private=False
                ))
                
                if repo_url:
                    if github_integration.init_git_repo(agent.working_directory):
                        if github_integration.add_remote(agent.working_directory, repo_name):
                            print(f"[AADC_TEXT] ✓ Created: {repo_url}", flush=True)
                        else:
                            print(f"[AADC_TEXT] ⚠ Repo created but remote failed: {repo_url}", flush=True)
                    else:
                        print(f"[AADC_TEXT] ⚠ Repo created but git init failed: {repo_url}", flush=True)
                else:
                    print("[AADC_ERROR] Failed to create repository", flush=True)
                print("[AADC_DONE]", flush=True)
                continue
            
            elif cmd == "/push":
                from github_integration import github_integration
                
                if not github_integration.is_authenticated():
                    print("[AADC_ERROR] Not connected to GitHub", flush=True)
                    print("[AADC_DONE]", flush=True)
                    continue
                
                print("[AADC_TEXT] Pushing to GitHub...", flush=True)
                if github_integration.commit_and_push(agent.working_directory, "Update from AADC"):
                    print("[AADC_TEXT] ✓ Pushed to GitHub!", flush=True)
                else:
                    print("[AADC_ERROR] Failed to push. Set up repo with /repo first", flush=True)
                print("[AADC_DONE]", flush=True)
                continue
            
            elif cmd == "/auto-commit":
                current = config.github_auto_commit
                config.github_auto_commit = not current
                
                if config.github_auto_commit:
                    print("[AADC_TEXT] ✓ Auto-commit enabled", flush=True)
                else:
                    print("[AADC_TEXT] Auto-commit disabled", flush=True)
                print("[AADC_DONE]", flush=True)
                continue
            
            # Unknown command
            elif cmd.startswith("/"):
                print(f"[AADC_ERROR] Unknown command: {cmd}", flush=True)
                print("[AADC_TEXT] Type /help for available commands", flush=True)
                print("[AADC_DONE]", flush=True)
                continue
            
            # Regular message - send to AI
            # Check credits first
            if not use_credit():
                print("[AADC_NO_CREDITS] https://aadc-website.vercel.app/pricing", flush=True)
                continue
            
            # Process the message
            print("[AADC_THINKING]", flush=True)
            
            try:
                for event in agent.send_message(message):
                    if event["type"] == "text":
                        # Output text line by line
                        for text_line in event["content"].split("\n"):
                            print(f"[AADC_TEXT] {text_line}", flush=True)
                    
                    elif event["type"] == "tool_call":
                        tool_info = json.dumps({"name": event["name"], "args": event["args"]})
                        print(f"[AADC_TOOL] {tool_info}", flush=True)
                    
                    elif event["type"] == "tool_result":
                        status = "success" if event["success"] else "error"
                        print(f"[AADC_TOOL_RESULT] {status}", flush=True)
                    
                    elif event["type"] == "error":
                        print(f"[AADC_ERROR] {event['content']}", flush=True)
                
                print("[AADC_DONE]", flush=True)
                
            except Exception as e:
                print(f"[AADC_ERROR] {str(e)}", flush=True)
    
    except KeyboardInterrupt:
        pass
    except EOFError:
        pass
    
    print("[AADC_EXIT]", flush=True)


def run_interactive():
    """Run the agent in interactive mode."""
    global plan_pending_approval, last_plan
    
    print_header()
    
    # Check authentication
    if not auth_manager.is_logged_in():
        print(f"{Colors.YELLOW}Welcome to AADC!{Colors.RESET}")
        print(f"{Colors.GRAY}Please log in to continue using the AI assistant.{Colors.RESET}\n")
        
        if not auth_manager.login():
            print_error("Authentication required. Please run the CLI again and log in.")
            sys.exit(1)
    else:
        user = auth_manager.get_user()
        print(f"{Colors.SUCCESS}✓ Logged in as {user.get('displayName', 'User')}{Colors.RESET}")
        print(f"{Colors.GRAY}  Credits: {user.get('credits', 0)} │ Plan: {user.get('plan', 'free')}{Colors.RESET}\n")
    
    # Check beta access
    if not auth_manager.has_beta_access():
        print(f"\n{Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
        print(f"{Colors.YELLOW}🔒 CLOSED BETA{Colors.RESET}")
        print(f"{Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
        print(f"\n{Colors.WHITE}AADC is currently in closed beta.{Colors.RESET}")
        print(f"{Colors.GRAY}You need beta access to use the CLI.{Colors.RESET}\n")
        print(f"{Colors.WHITE}To request access:{Colors.RESET}")
        print(f"{Colors.GRAY}  1. Visit {Colors.CYAN}https://aadc-website.vercel.app/beta{Colors.RESET}")
        print(f"{Colors.GRAY}  2. Fill out the beta request form{Colors.RESET}")
        print(f"{Colors.GRAY}  3. Wait for approval (we'll email you){Colors.RESET}\n")
        print(f"{Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}\n")
        sys.exit(1)
    
    # Create proxy agent (communicates through secure server)
    agent = create_proxy_agent()
    
    if agent is None:
        print_error("Failed to initialize agent. Please log in again.")
        sys.exit(1)
    
    # Register cleanup on exit
    atexit.register(agent.cleanup)
    
    # Check for existing project summary
    if has_project_summary(agent.working_directory):
        age = get_summary_age(agent.working_directory)
        if age is not None:
            if age < 24:
                print(f"{Colors.SUCCESS}✓ Project context loaded (aadc.md){Colors.RESET}")
            else:
                print(f"{Colors.WARNING}⚠ Project summary is {int(age)}h old. Run /init to refresh.{Colors.RESET}")
    
    print_welcome()
    
    plan_mode = config.plan_mode
    
    # Track consecutive Ctrl+C presses for double-exit
    last_interrupt_time = 0
    interrupt_count = 0
    
    # Main interaction loop
    while True:
        try:
            # Get user input with plan mode support
            user_input, plan_mode = get_input_with_plan_mode(agent.working_directory, plan_mode)
            agent.plan_mode = plan_mode
            
            # Reset interrupt counter on successful input
            interrupt_count = 0
            last_interrupt_time = 0
            
            if not user_input:
                continue
            
            # Check for commands
            result = handle_command(user_input, agent)
            
            if result == "reinit":
                # Reinitialize agent with new model (just update config, proxy handles the rest)
                print_success(f"Model switched to {config.model}")
                continue
            
            elif result == "approve_plan":
                # User approved the plan, now implement it
                if last_plan:
                    if not use_credit():
                        print(f"{Colors.RED}No credits remaining to implement the plan.{Colors.RESET}")
                        print(f"{Colors.WHITE}Purchase credits at:{Colors.RESET} {Colors.CYAN}https://aadc-website.vercel.app/pricing{Colors.RESET}")
                        continue
                    implement_message = "The user approved your plan. Now implement it exactly as planned. Build the complete project."
                    run_single_message_streaming(agent, implement_message)
                plan_mode = False
                print_separator()
                continue
            
            elif isinstance(result, tuple) and result[0] == "reject_plan":
                # User rejected the plan with feedback
                if not use_credit():
                    print(f"{Colors.RED}No credits remaining to revise the plan.{Colors.RESET}")
                    print(f"{Colors.WHITE}Purchase credits at:{Colors.RESET} {Colors.CYAN}https://aadc-website.vercel.app/pricing{Colors.RESET}")
                    continue
                feedback = result[1]
                revise_message = f"The user rejected your plan with this feedback: {feedback}\n\nPlease revise the plan and present an updated version."
                run_single_message_streaming(agent, revise_message)
                print_separator()
                continue
            
            elif result:
                plan_mode = config.plan_mode
                continue
            
            # Process with agent using streaming
            # Check credits before sending to AI
            if not use_credit():
                print(f"{Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
                print(f"{Colors.WHITE}Purchase credits at:{Colors.RESET} {Colors.CYAN}https://aadc-website.vercel.app/pricing{Colors.RESET}")
                print(f"{Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
                continue
            
            run_single_message_streaming(agent, user_input)
            
            # Reset plan mode after execution (one-shot plan mode)
            if plan_mode and not config.plan_mode and not plan_pending_approval:
                plan_mode = False
            
            print_separator()
            
        except KeyboardInterrupt:
            import time
            current_time = time.time()
            
            # Reset counter if more than 5 seconds have passed
            if current_time - last_interrupt_time > 5:
                interrupt_count = 0
            
            interrupt_count += 1
            last_interrupt_time = current_time
            
            if interrupt_count == 1:
                print(f"\n\n{Colors.WARNING}Press Ctrl+C again within 5 seconds to exit, or type /exit to quit.{Colors.RESET}\n")
            elif interrupt_count >= 2:
                # Double Ctrl+C pressed - exit cleanly
                agent.cleanup()
                print(f"\n{Colors.WHITE}Goodbye!{Colors.RESET}\n")
                break
            
            continue
        except EOFError:
            agent.cleanup()
            print(f"\n{Colors.WHITE}Goodbye!{Colors.RESET}\n")
            break
        except Exception as e:
            print_error(f"An error occurred: {e}")
            continue


def run_single_command(prompt: str):
    """Run a single command and exit."""
    # Check authentication first
    if not auth_manager.is_logged_in():
        if not auth_manager.login():
            print_error("Authentication required.")
            sys.exit(1)
    
    # Check beta access
    if not auth_manager.has_beta_access():
        print_error("AADC is in closed beta. Visit https://aadc-website.vercel.app/beta to request access.")
        sys.exit(1)
    
    agent = create_proxy_agent()
    
    if agent is None:
        print_error("Failed to initialize agent. Please log in again.")
        sys.exit(1)
    
    try:
        agent.run_single_message(prompt)
        agent.cleanup()
    except Exception as e:
        print_error(f"Failed: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Gemini Coding Agent - AI-powered code generation tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Start interactive mode
  %(prog)s "Create a snake game"    # Run single command
  %(prog)s -d ./projects "Build a todo app"  # Run in specific directory
  %(prog)s --plan "Create a REST API"        # Start in plan mode
        """
    )
    
    parser.add_argument(
        "prompt",
        nargs="?",
        help="Optional prompt to run (non-interactive mode)"
    )
    
    parser.add_argument(
        "-d", "--directory",
        help="Working directory for file operations"
    )
    
    parser.add_argument(
        "-p", "--plan",
        action="store_true",
        help="Enable plan mode (create plan.md before coding)"
    )
    
    parser.add_argument(
        "-m", "--mode",
        choices=["ask", "auto", "command_ask"],
        default="auto",
        help="Permission mode: ask (all tools), auto (no confirm), command_ask (only commands)"
    )
    
    parser.add_argument(
        "--model",
        choices=list(AVAILABLE_MODELS.keys()),
        default="gemini-3-pro-preview",
        help="AI model to use"
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    parser.add_argument(
        "--pipe",
        action="store_true",
        help="Run in pipe mode for desktop app (no interactive UI)"
    )
    
    args = parser.parse_args()
    
    # Set working directory if specified
    if args.directory:
        path = Path(args.directory).resolve()
        if path.is_dir():
            os.chdir(path)
            config.working_directory = str(path)
            # Set sandbox root to this directory
            from tools import set_sandbox_root
            set_sandbox_root(str(path))
        else:
            print_error(f"Directory does not exist: {args.directory}")
            sys.exit(1)
    else:
        # Default sandbox to current directory
        from tools import set_sandbox_root
        set_sandbox_root(os.getcwd())
    
    # Set model if provided
    if args.model:
        config.model = args.model
    
    # Set plan mode
    if args.plan:
        config.plan_mode = True
    
    # Set permission mode
    config.permission_mode = args.mode
    
    # Run in pipe mode (for desktop app)
    if args.pipe:
        run_pipe_mode()
    # Run in single command or interactive mode
    elif args.prompt:
        run_single_command(args.prompt)
    else:
        run_interactive()


if __name__ == "__main__":
    main()
