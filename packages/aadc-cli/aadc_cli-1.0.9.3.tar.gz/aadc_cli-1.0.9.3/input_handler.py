"""
Advanced Input Handler for AADC
Handles arrow keys for quick actions: Left=permission, Right=tasks
"""

import sys
import os

# Windows-specific imports
if sys.platform == "win32":
    import msvcrt
else:
    import tty
    import termios
    import select


class Colors:
    """ANSI color codes."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    CLEAR_LINE = "\033[2K"


class InputHandler:
    """
    Handles keyboard input with arrow key support.
    
    Arrow keys:
    - Left Arrow: Cycle permission modes
    - Right Arrow: Open background task selector
    """
    
    PERMISSION_MODES = ["auto", "ask", "command_ask"]
    
    def __init__(self, terminal_manager, config):
        self.terminal_manager = terminal_manager
        self.config = config
    
    def cycle_permission_mode(self):
        """Cycle through permission modes."""
        current_idx = self.PERMISSION_MODES.index(self.config.permission_mode)
        next_idx = (current_idx + 1) % len(self.PERMISSION_MODES)
        self.config.permission_mode = self.PERMISSION_MODES[next_idx]
        return self.config.permission_mode
    
    def show_terminal_view(self, session_id: str):
        """Show terminal view for a background task."""
        c = Colors
        
        session = self.terminal_manager.sessions.get(session_id)
        if not session:
            print(f"{c.RED}Session not found: {session_id}{c.RESET}")
            return
        
        print(f"\n{c.RED}{'━' * 60}{c.RESET}")
        print(f"{c.WHITE}{c.BOLD}Terminal: {session.name}{c.RESET}")
        print(f"{c.RED}{'━' * 60}{c.RESET}")
        
        status = f"{c.GREEN}● RUNNING{c.RESET}" if session.is_running else f"{c.RED}● STOPPED{c.RESET}"
        print(f"\n  {c.GRAY}Status:{c.RESET}  {status}")
        print(f"  {c.GRAY}PID:{c.RESET}     {session.pid}")
        print(f"  {c.GRAY}Uptime:{c.RESET}  {session.uptime}")
        
        print(f"\n{c.YELLOW}Command:{c.RESET} $ {session.command}")
        
        output = self.terminal_manager.get_output(session_id, max_lines=25)
        print(f"\n{c.CYAN}Output:{c.RESET}")
        if output:
            for line in output.split('\n')[-25:]:
                print(f"  {line}")
        else:
            print(f"  {c.DIM}(no output yet){c.RESET}")
        
        print(f"\n{c.GRAY}[r]efresh [i]nput [k]ill [Enter]back{c.RESET}")
        
        while True:
            try:
                action = input(f"{c.GRAY}>{c.RESET} ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                return
            
            if action == '' or action == 'q':
                return
            elif action == 'r':
                output = self.terminal_manager.get_output(session_id, max_lines=25)
                print(f"\n{c.CYAN}Output (refreshed):{c.RESET}")
                for line in (output or "(no output)").split('\n')[-25:]:
                    print(f"  {line}")
            elif action == 'i':
                user_input = input(f"{c.YELLOW}Input:{c.RESET} ")
                if user_input:
                    result = self.terminal_manager.send_input(session_id, user_input)
                    print(f"{c.GREEN}✓ Sent{c.RESET}" if result.get("success") else f"{c.RED}✗ Failed{c.RESET}")
            elif action == 'k':
                confirm = input(f"{c.YELLOW}Kill? (y/N):{c.RESET} ").strip().lower()
                if confirm == 'y':
                    self.terminal_manager.close_terminal(session_id)
                    print(f"{c.GREEN}✓ Killed{c.RESET}")
                    return
    
    def show_task_selector(self):
        """Show background tasks and let user select one."""
        c = Colors
        tasks = self.terminal_manager.get_all_status()
        terminals = tasks.get("terminals", [])
        
        if not terminals:
            print(f"\r{c.CLEAR_LINE}{c.GRAY}No background tasks.{c.RESET}")
            return
        
        print(f"\r{c.CLEAR_LINE}{c.CYAN}Tasks:{c.RESET}")
        for i, task in enumerate(terminals):
            status = f"{c.GREEN}●{c.RESET}" if task["is_running"] else f"{c.RED}●{c.RESET}"
            print(f"  {i+1}. {status} {task['name']}")
        
        try:
            choice = input(f"{c.GRAY}#{c.RESET} ").strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(terminals):
                    self.show_terminal_view(terminals[idx]["id"])
        except (EOFError, KeyboardInterrupt):
            pass
    
    def get_input_with_arrows(self, prompt: str, plan_mode: bool) -> tuple:
        """
        Custom input that catches arrow keys.
        Left = cycle permission, Right = show tasks
        
        Returns: (user_input, new_plan_mode, action)
        """
        c = Colors
        buffer = []
        
        print(prompt, end="", flush=True)
        
        if sys.platform == "win32":
            return self._input_windows(buffer, plan_mode)
        else:
            return self._input_unix(buffer, plan_mode)
    
    def _input_windows(self, buffer, plan_mode):
        """Windows input handling with arrow keys."""
        c = Colors
        
        while True:
            key = msvcrt.getwch()
            
            # Special keys (arrows)
            if key in ('\x00', '\xe0'):
                key2 = msvcrt.getwch()
                
                if key2 == 'K':  # Left arrow
                    print(f"\r{c.CLEAR_LINE}", end="", flush=True)
                    new_mode = self.cycle_permission_mode()
                    print(f"{c.CYAN}✓ Permission: {new_mode}{c.RESET}")
                    return ("", plan_mode, "permission_cycled")
                
                elif key2 == 'M':  # Right arrow
                    print(f"\r{c.CLEAR_LINE}", end="", flush=True)
                    self.show_task_selector()
                    return ("", plan_mode, "task_selected")
                
                # Ignore up/down arrows
                continue
            
            # Enter
            elif key == '\r':
                print()
                text = ''.join(buffer)
                new_mode = plan_mode
                if text.lower().startswith("plan:"):
                    text = text[5:].strip()
                    new_mode = True
                return (text, new_mode, None)
            
            # Backspace
            elif key == '\x08':
                if buffer:
                    buffer.pop()
                    print('\b \b', end="", flush=True)
            
            # Ctrl+C
            elif key == '\x03':
                raise KeyboardInterrupt
            
            # Printable character
            elif key.isprintable():
                buffer.append(key)
                print(key, end="", flush=True)
    
    def _input_unix(self, buffer, plan_mode):
        """Unix input handling with arrow keys."""
        c = Colors
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        
        try:
            tty.setcbreak(fd)
            
            while True:
                key = sys.stdin.read(1)
                
                # Escape sequence
                if key == '\x1b':
                    if select.select([sys.stdin], [], [], 0.1)[0]:
                        key2 = sys.stdin.read(1)
                        if key2 == '[':
                            key3 = sys.stdin.read(1)
                            
                            if key3 == 'D':  # Left arrow
                                print(f"\r{c.CLEAR_LINE}", end="", flush=True)
                                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                                new_mode = self.cycle_permission_mode()
                                print(f"{c.CYAN}✓ Permission: {new_mode}{c.RESET}")
                                return ("", plan_mode, "permission_cycled")
                            
                            elif key3 == 'C':  # Right arrow
                                print(f"\r{c.CLEAR_LINE}", end="", flush=True)
                                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                                self.show_task_selector()
                                return ("", plan_mode, "task_selected")
                    continue
                
                # Enter
                elif key in ('\n', '\r'):
                    print()
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                    text = ''.join(buffer)
                    new_mode = plan_mode
                    if text.lower().startswith("plan:"):
                        text = text[5:].strip()
                        new_mode = True
                    return (text, new_mode, None)
                
                # Backspace
                elif key in ('\x7f', '\x08'):
                    if buffer:
                        buffer.pop()
                        print('\b \b', end="", flush=True)
                
                # Ctrl+C
                elif key == '\x03':
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                    raise KeyboardInterrupt
                
                # Printable
                elif key.isprintable():
                    buffer.append(key)
                    print(key, end="", flush=True)
        
        except:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            raise
    
    # Keep old method for compatibility
    def get_input_advanced(self, prompt: str, plan_mode: bool) -> tuple:
        """Alias for get_input_with_arrows."""
        return self.get_input_with_arrows(prompt, plan_mode)


def create_input_handler(terminal_manager, config):
    """Create an input handler instance."""
    return InputHandler(terminal_manager, config)
