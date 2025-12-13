"""
Terminal Manager for Gemini Agent
Handles multiple terminal sessions and background processes (servers, etc.)
"""

import os
import subprocess
import signal
import threading
import queue
import time
from typing import Dict, Optional, List
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TerminalSession:
    """Represents a terminal/process session."""
    id: str
    name: str
    command: str
    process: subprocess.Popen
    working_directory: str
    started_at: datetime = field(default_factory=datetime.now)
    output_queue: queue.Queue = field(default_factory=queue.Queue)
    is_server: bool = False
    
    @property
    def is_running(self) -> bool:
        return self.process.poll() is None
    
    @property
    def pid(self) -> int:
        return self.process.pid
    
    @property
    def uptime(self) -> str:
        delta = datetime.now() - self.started_at
        seconds = int(delta.total_seconds())
        if seconds < 60:
            return f"{seconds}s"
        elif seconds < 3600:
            return f"{seconds // 60}m {seconds % 60}s"
        else:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours}h {minutes}m"


class TerminalManager:
    """Manages multiple terminal sessions and background processes."""
    
    def __init__(self):
        self.sessions: Dict[str, TerminalSession] = {}
        self._session_counter = 0
        self._output_threads: Dict[str, threading.Thread] = {}
    
    def _generate_session_id(self) -> str:
        """Generate a unique session ID."""
        self._session_counter += 1
        return f"term_{self._session_counter}"
    
    def _output_reader(self, session_id: str, pipe, output_queue: queue.Queue):
        """Background thread to read output from a process."""
        try:
            for line in iter(pipe.readline, ''):
                if line:
                    output_queue.put(line.rstrip('\n'))
                if session_id not in self.sessions:
                    break
        except Exception:
            pass
        finally:
            pipe.close()
    
    def open_terminal(
        self,
        command: str,
        name: Optional[str] = None,
        working_directory: Optional[str] = None,
        is_server: bool = False
    ) -> dict:
        """
        Open a new terminal session running a command in the background.
        
        Args:
            command: The command to run
            name: Optional friendly name for the session
            working_directory: Directory to run the command in
            is_server: Whether this is a long-running server process
        
        Returns:
            dict with session info or error
        """
        try:
            session_id = self._generate_session_id()
            cwd = working_directory or os.getcwd()
            
            # Start the process
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                text=True,
                bufsize=1,
                preexec_fn=os.setsid if os.name != 'nt' else None
            )
            
            # Create session
            session = TerminalSession(
                id=session_id,
                name=name or f"Session {self._session_counter}",
                command=command,
                process=process,
                working_directory=cwd,
                is_server=is_server
            )
            
            self.sessions[session_id] = session
            
            # Start output reader thread
            thread = threading.Thread(
                target=self._output_reader,
                args=(session_id, process.stdout, session.output_queue),
                daemon=True
            )
            thread.start()
            self._output_threads[session_id] = thread
            
            # Wait a moment to check if it started successfully
            time.sleep(0.5)
            
            if not session.is_running:
                # Process ended immediately, might be an error
                output = self.get_output(session_id)
                return {
                    "success": False,
                    "error": f"Process exited immediately with code {process.returncode}",
                    "output": output,
                    "session_id": session_id
                }
            
            return {
                "success": True,
                "session_id": session_id,
                "name": session.name,
                "pid": session.pid,
                "command": command,
                "message": f"Started background process: {session.name} (PID: {session.pid})"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to open terminal: {str(e)}"
            }
    
    def close_terminal(self, session_id: str) -> dict:
        """Close/kill a terminal session."""
        if session_id not in self.sessions:
            return {
                "success": False,
                "error": f"Session not found: {session_id}"
            }
        
        try:
            session = self.sessions[session_id]
            
            if session.is_running:
                # Kill the process group
                if os.name != 'nt':
                    os.killpg(os.getpgid(session.process.pid), signal.SIGTERM)
                else:
                    session.process.terminate()
                
                # Wait for it to terminate
                try:
                    session.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    if os.name != 'nt':
                        os.killpg(os.getpgid(session.process.pid), signal.SIGKILL)
                    else:
                        session.process.kill()
            
            # Clean up
            del self.sessions[session_id]
            if session_id in self._output_threads:
                del self._output_threads[session_id]
            
            return {
                "success": True,
                "message": f"Closed terminal session: {session.name}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to close terminal: {str(e)}"
            }
    
    def get_output(self, session_id: str, max_lines: int = 100) -> str:
        """Get recent output from a terminal session."""
        if session_id not in self.sessions:
            return ""
        
        session = self.sessions[session_id]
        lines = []
        
        try:
            while not session.output_queue.empty() and len(lines) < max_lines:
                lines.append(session.output_queue.get_nowait())
        except queue.Empty:
            pass
        
        return "\n".join(lines)
    
    def send_input(self, session_id: str, text: str) -> dict:
        """Send input to a terminal session."""
        if session_id not in self.sessions:
            return {
                "success": False,
                "error": f"Session not found: {session_id}"
            }
        
        try:
            session = self.sessions[session_id]
            
            if not session.is_running:
                return {
                    "success": False,
                    "error": "Process is not running"
                }
            
            session.process.stdin.write(text + "\n")
            session.process.stdin.flush()
            
            return {
                "success": True,
                "message": f"Sent input to {session.name}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to send input: {str(e)}"
            }
    
    def list_terminals(self) -> dict:
        """List all terminal sessions."""
        terminals = []
        
        for session_id, session in self.sessions.items():
            terminals.append({
                "id": session_id,
                "name": session.name,
                "command": session.command,
                "pid": session.pid,
                "is_running": session.is_running,
                "is_server": session.is_server,
                "uptime": session.uptime,
                "working_directory": session.working_directory
            })
        
        return {
            "success": True,
            "count": len(terminals),
            "terminals": terminals
        }
    
    def get_terminal_status(self, session_id: str) -> dict:
        """Get status of a specific terminal."""
        if session_id not in self.sessions:
            return {
                "success": False,
                "error": f"Session not found: {session_id}"
            }
        
        session = self.sessions[session_id]
        output = self.get_output(session_id)
        
        return {
            "success": True,
            "id": session_id,
            "name": session.name,
            "command": session.command,
            "pid": session.pid,
            "is_running": session.is_running,
            "is_server": session.is_server,
            "uptime": session.uptime,
            "recent_output": output
        }
    
    def cleanup(self):
        """Close all terminal sessions."""
        for session_id in list(self.sessions.keys()):
            self.close_terminal(session_id)
    
    def get_active_count(self) -> int:
        """Get count of active/running terminal sessions."""
        return sum(1 for s in self.sessions.values() if s.is_running)
    
    def get_running_count(self) -> int:
        """Alias for get_active_count - get count of running background tasks."""
        return self.get_active_count()
    
    def get_all_status(self) -> dict:
        """Get status of all terminal sessions with their recent output."""
        statuses = []
        
        for session_id, session in self.sessions.items():
            output = self.get_output(session_id, max_lines=20)
            statuses.append({
                "id": session_id,
                "name": session.name,
                "command": session.command,
                "pid": session.pid,
                "is_running": session.is_running,
                "is_server": session.is_server,
                "uptime": session.uptime,
                "recent_output": output,
                "working_directory": session.working_directory
            })
        
        return {
            "success": True,
            "total": len(statuses),
            "running": sum(1 for s in statuses if s["is_running"]),
            "terminals": statuses
        }
    
    def get_summary_line(self) -> str:
        """Get a one-line summary of background tasks for display."""
        running = self.get_active_count()
        total = len(self.sessions)
        
        if total == 0:
            return ""
        
        # Build summary
        names = [s.name for s in self.sessions.values() if s.is_running]
        if running == 0:
            return f"⚪ {total} background task(s) stopped"
        elif running == 1:
            return f"🟢 {names[0]} running"
        else:
            return f"🟢 {running} tasks running: {', '.join(names[:3])}{'...' if len(names) > 3 else ''}"


# Global terminal manager instance
terminal_manager = TerminalManager()
