"""
Proxy Agent for AADC CLI
Communicates with the AADC API proxy server instead of calling AI APIs directly.
This ensures API keys stay on the server and credits are properly managed.
"""

import os
import json
import time
import hashlib
import hmac
import urllib.request
import urllib.error
from typing import Generator, Optional, Dict, Any

from config import config, AVAILABLE_MODELS
from prompts import SYSTEM_PROMPT
from tools import TOOL_DECLARATIONS
from memory import memory_manager
from terminal_manager import terminal_manager
from project_init import get_project_summary, has_project_summary


# ============================================================================
# CONFIGURATION
# ============================================================================

# API proxy server URL - set via environment or use default
# For local testing, use localhost
PROXY_URL = os.environ.get("AADC_PROXY_URL", "http://localhost:8000")

# Get the signing secret (should match server's AADC_API_SECRET)
# For beta testing, using a shared secret
# In production, this should be securely distributed per-user
def get_auth_secret() -> str:
    """Get the auth secret for request signing."""
    # For beta, use the shared secret
    return os.environ.get("AADC_AUTH_SECRET", "beta-testing-secret-2024")


# ============================================================================
# REQUEST SIGNING
# ============================================================================

def sign_request(uid: str, timestamp: str, secret: str) -> str:
    """
    Create HMAC signature for request authentication.
    Must match server's verify_request_signature().
    """
    message = f"{uid}:{timestamp}"
    return hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()


# ============================================================================
# PROXY AGENT
# ============================================================================

class ProxyAgent:
    """
    Agent that communicates through the AADC proxy server.
    All AI API calls go through the proxy, which handles:
    - Authentication
    - Credit checking/deduction
    - Actual API calls with server-side keys
    """
    
    def __init__(self, uid: str, auth_secret: str):
        self.uid = uid
        self.auth_secret = auth_secret
        self.working_directory = config.working_directory
        self.plan_mode = config.plan_mode
        self.history = []
        self.confirm_callback = None
        self._confirm_callback = None
        self.last_credits = None
    
    def set_confirmation_callback(self, callback):
        """Set the callback for tool confirmation."""
        self.confirm_callback = callback
        self._confirm_callback = callback
    
    def start_chat(self):
        """Initialize chat session."""
        self.history = []
    
    def clear_history(self):
        """Clear conversation history."""
        self.history = []
    
    def change_directory(self, path: str) -> bool:
        """Change working directory."""
        try:
            new_path = os.path.abspath(os.path.expanduser(path))
            if os.path.isdir(new_path):
                os.chdir(new_path)
                self.working_directory = new_path
                return True
            return False
        except Exception:
            return False
    
    def should_confirm_tool(self, function_name: str) -> bool:
        """Check if tool requires confirmation."""
        mode = config.permission_mode
        if mode == "auto":
            return False
        elif mode == "ask":
            return True
        elif mode == "command_ask":
            return function_name in ["execute_command", "open_terminal", "send_terminal_input"]
        return False
    
    def execute_tool(self, function_name: str, function_args: dict) -> dict:
        """Execute a tool locally."""
        from tools import TOOL_FUNCTIONS
        
        if function_name not in TOOL_FUNCTIONS:
            return {"success": False, "error": f"Unknown tool: {function_name}"}
        
        try:
            func = TOOL_FUNCTIONS[function_name]
            
            # Adjust paths for file operations
            if function_name == "execute_command":
                if "working_directory" not in function_args or not function_args["working_directory"]:
                    function_args["working_directory"] = self.working_directory
            
            if function_name in ["create_file", "delete_file", "read_file", "write_file", "edit_file"]:
                if "file_path" in function_args:
                    path = function_args["file_path"]
                    if not os.path.isabs(path):
                        function_args["file_path"] = os.path.join(self.working_directory, path)
            
            if function_name in ["create_folder", "delete_folder", "list_files"]:
                path_key = "folder_path" if "folder_path" in function_args else "path"
                if path_key in function_args and function_args[path_key]:
                    path = function_args[path_key]
                    if not os.path.isabs(path):
                        function_args[path_key] = os.path.join(self.working_directory, path)
                elif function_name == "list_files":
                    function_args["folder_path"] = self.working_directory
            
            result = func(**function_args)
            return result
        except Exception as e:
            return {"success": False, "error": f"Tool execution failed: {str(e)}"}
    
    def get_system_prompt(self) -> str:
        """Build full system prompt with memory and project context."""
        parts = [SYSTEM_PROMPT]
        
        # Add memory context
        memory_context = memory_manager.get_memory_summary()
        if memory_context and memory_context != "No memories stored yet.":
            parts.append(f"\n\n{memory_context}")
        
        # Add project summary if available
        if has_project_summary(self.working_directory):
            project_summary = get_project_summary(self.working_directory)
            if project_summary:
                parts.append(f"\n\n## Current Project Context\n{project_summary[:4000]}")
        
        return "\n".join(parts)
    
    def _route_request(self, prompt: str) -> tuple[str, bool]:
        """
        Send request to nova-2-lite first to determine routing.
        Returns (model_to_use, should_forward_to_nova)
        - If simple: ('nova-2-lite', True) - nova will answer with full system prompt
        - If complex: ('gemini-3-pro-preview', False) - forward to gemini
        """
        routing_system = """You are a request router for an AI coding assistant.

Your job: Decide if YOU can handle this request or if it needs a more powerful model.

YOU can handle:
- Greetings (hi, hello, hey)
- Questions about yourself or the system
- Simple explanations
- Reading/listing files
- Small text edits
- General conversation

FORWARD to Gemini 3 Pro if:
- Creating new projects from scratch
- Building complex features
- Major refactoring or debugging
- Architecture decisions
- Multiple file operations

Respond with ONLY:
"HANDLE" - if you can answer this yourself
"FORWARD" - if it needs Gemini 3 Pro"""

        # Call nova-2-lite for routing decision with custom system prompt
        response = self._call_proxy(
            prompt=prompt,
            model="amazon/nova-2-lite-v1:free",
            provider="openrouter",
            system_prompt=routing_system,
            use_tools=False
        )
        
        if response.get('success') and 'response' in response:
            decision = response['response'].strip().upper()
            
            if 'HANDLE' in decision:
                return ('nova-2-lite', True)
            elif 'FORWARD' in decision:
                return ('gemini-3-pro-preview', False)
        
        # Default: let nova handle it
        return ('nova-2-lite', True)
    
    def _call_proxy(self, prompt: str, model: str, provider: str, system_prompt: str = None, use_tools: bool = True) -> Dict[str, Any]:
        """
        Make authenticated request to proxy server.
        Returns response dict or error.
        """
        timestamp = str(int(time.time()))
        signature = sign_request(self.uid, timestamp, self.auth_secret)
        
        # Prepare request
        request_data = {
            "prompt": prompt,
            "model": model,
            "provider": provider,
            "system_prompt": system_prompt if system_prompt else self.get_system_prompt(),
            "tools": TOOL_DECLARATIONS if use_tools else [],
            "history": self.history[-10:]  # Send last 10 messages for context
        }
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'AADC-CLI/1.0',
            'X-Auth-UID': self.uid,
            'X-Auth-Timestamp': timestamp,
            'X-Auth-Signature': signature
        }
        
        try:
            url = f"{PROXY_URL}/api/chat"
            data = json.dumps(request_data).encode('utf-8')
            
            req = urllib.request.Request(url, data=data, headers=headers, method='POST')
            
            with urllib.request.urlopen(req, timeout=300) as response:
                result = json.loads(response.read().decode())
                
                # Track remaining credits
                if 'credits_remaining' in result:
                    self.last_credits = result['credits_remaining']
                
                return result
                
        except urllib.error.HTTPError as e:
            error_body = e.read().decode() if e.fp else ""
            try:
                error_data = json.loads(error_body)
                return {"success": False, "error": error_data.get('error', f'HTTP {e.code}')}
            except:
                return {"success": False, "error": f"Server error: {e.code}"}
        except urllib.error.URLError as e:
            return {"success": False, "error": f"Connection failed: {str(e.reason)}"}
        except Exception as e:
            return {"success": False, "error": f"Request failed: {str(e)}"}
    
    def send_message(self, message: str, confirm_callback=None) -> Generator[dict, None, None]:
        """
        Send message through proxy and handle tool calls.
        Yields events similar to other agents.
        """
        iteration = 0
        max_iterations = config.max_iterations
        
        if self.plan_mode:
            message = f"""[PLAN MODE ACTIVE] 
Create a file called 'plan.md' with:
1. Overview of what will be built
2. File structure
3. Technologies used
4. Step-by-step implementation plan
5. Potential challenges

DO NOT create any code files yet. Only create plan.md.

User request: {message}"""
        
        # Add to history
        self.history.append({"role": "user", "content": message})
        memory_manager.add_conversation("user", message)
        
        # Get model info
        model = config.model
        model_info = AVAILABLE_MODELS.get(model, {})
        
        # Handle auto mode - route the request
        actual_model = model
        nova_should_answer = False
        
        if model == "auto":
            actual_model, nova_should_answer = self._route_request(message)
            model_info = AVAILABLE_MODELS.get(actual_model, {})
            provider = model_info.get("provider", "gemini")
            
            # Get the actual model ID to send to server
            if provider == "openrouter":
                server_model = model_info.get("openrouter_id", actual_model)
            else:
                server_model = actual_model
            
            # Show which model was selected
            model_name = model_info.get("display_name", actual_model)
            yield {"type": "text", "content": f"🤖 {model_name}\n\n"}
            
            # If nova decided to handle it, we need to call it again with full system prompt
            if nova_should_answer:
                # Nova will now answer with full agent capabilities
                pass
        else:
            provider = model_info.get("provider", "gemini")
            if provider == "openrouter":
                server_model = model_info.get("openrouter_id", model)
            else:
                server_model = model
        
        current_prompt = message
        
        while iteration < max_iterations:
            iteration += 1
            
            # Call proxy
            response = self._call_proxy(current_prompt, server_model, provider)
            
            if not response.get('success'):
                error = response.get('error', 'Unknown error')
                if 'credits' in error.lower() or 'credit' in error.lower():
                    yield {"type": "error", "content": f"❌ {error}\nVisit https://aadc.dev/pricing to purchase more credits."}
                else:
                    yield {"type": "error", "content": error}
                return
            
            # Process text response
            text = response.get('text', '')
            if text:
                yield {"type": "text", "content": text}
                self.history.append({"role": "assistant", "content": text})
                memory_manager.add_conversation("assistant", text)
            
            # Process tool calls
            tool_calls = response.get('tool_calls', [])
            
            if not tool_calls:
                # No more tool calls, we're done
                break
            
            tool_results = []
            for tool_call in tool_calls:
                tool_name = tool_call.get('name', '')
                tool_args = tool_call.get('args', {})
                
                needs_confirm = self.should_confirm_tool(tool_name)
                
                yield {
                    "type": "tool_call",
                    "name": tool_name,
                    "args": tool_args,
                    "iteration": iteration,
                    "max_iterations": max_iterations,
                    "needs_confirmation": needs_confirm
                }
                
                # Check confirmation
                if confirm_callback and needs_confirm:
                    if not confirm_callback(tool_name, tool_args):
                        yield {
                            "type": "tool_skipped",
                            "name": tool_name,
                            "reason": "denied by user"
                        }
                        tool_results.append({
                            "name": tool_name,
                            "result": {"success": False, "error": "Denied by user"}
                        })
                        continue
                
                # Execute tool locally
                result = self.execute_tool(tool_name, tool_args)
                
                yield {
                    "type": "tool_result",
                    "name": tool_name,
                    "result": result,
                    "success": result.get("success", False)
                }
                
                tool_results.append({"name": tool_name, "result": result})
            
            # Build next prompt with tool results
            result_text = "Tool results:\n"
            for tr in tool_results:
                result_text += f"\n{tr['name']}: {json.dumps(tr['result'])}\n"
            
            current_prompt = result_text + "\n\nContinue based on these results."
        
        if iteration >= max_iterations:
            yield {"type": "warning", "content": f"Reached maximum iterations ({max_iterations})."}
    
    def cleanup(self):
        """Cleanup resources."""
        terminal_manager.cleanup()


# ============================================================================
# FACTORY FUNCTION
# ============================================================================

def create_proxy_agent() -> Optional[ProxyAgent]:
    """
    Create a proxy agent using the current auth session.
    Returns None if not authenticated.
    """
    try:
        from auth import auth_manager
        
        if not auth_manager.is_logged_in():
            return None
        
        uid = auth_manager.auth_data.get('uid', '')
        
        if not uid:
            return None
        
        # Use the get_auth_secret() function which has the beta default
        auth_secret = get_auth_secret()
        
        return ProxyAgent(uid, auth_secret)
        
    except Exception:
        return None
