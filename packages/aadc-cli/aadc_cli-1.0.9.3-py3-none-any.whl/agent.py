"""
Core Agent Module for AADC
Handles API communication and tool execution loop
Supports multiple providers: Gemini, OpenAI, Anthropic
"""

import json
import os
from typing import Any, Generator, Optional
from abc import ABC, abstractmethod

from config import config, PERMISSION_MODES, AVAILABLE_MODELS, OPENROUTER_MODEL_MAP
from prompts import SYSTEM_PROMPT
from tools import TOOL_FUNCTIONS, TOOL_DECLARATIONS
from memory import memory_manager
from terminal_manager import terminal_manager
from project_init import get_project_summary, has_project_summary
from utils import (
    print_tool_call,
    print_tool_result,
    print_assistant_message,
    print_error,
    print_warning,
    print_iteration,
    print_thinking,
    clear_thinking,
    confirm_action,
    print_task_complete,
    print_status,
    Colors
)


class BaseAgent(ABC):
    """Abstract base class for AI agents."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.working_directory = config.working_directory
        self.plan_mode = config.plan_mode
        self.history = []
        self.confirm_callback = None  # Callback for permission confirmation
        self._confirm_callback = None  # Internal callback storage
    
    def set_confirmation_callback(self, callback):
        """Set the callback for tool confirmation."""
        self.confirm_callback = callback
        self._confirm_callback = callback
    
    @abstractmethod
    def start_chat(self):
        pass
    
    @abstractmethod
    def send_message(self, message: str, confirm_callback=None) -> Generator[dict, None, None]:
        pass
    
    def clear_history(self):
        self.history = []
    
    def change_directory(self, path: str) -> bool:
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
        mode = config.permission_mode
        if mode == "auto":
            return False
        elif mode == "ask":
            return True
        elif mode == "command_ask":
            return function_name in ["execute_command", "open_terminal", "send_terminal_input"]
        return False
    
    def execute_tool(self, function_name: str, function_args: dict) -> dict:
        if function_name not in TOOL_FUNCTIONS:
            return {"success": False, "error": f"Unknown tool: {function_name}"}
        
        try:
            func = TOOL_FUNCTIONS[function_name]
            
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
    
    def run_single_message(self, message: str) -> str:
        final_text = []
        print_thinking()
        
        has_tool_calls = False
        skipped_tools = set()  # Track which tools were denied
        
        def on_confirm(tool_name: str, tool_args: dict) -> bool:
            """Callback for tool confirmation. Returns True if allowed."""
            if not self.should_confirm_tool(tool_name):
                return True
            
            # Ask user for confirmation
            print_tool_call(tool_name, tool_args)
            if confirm_action(f"Execute {tool_name}?"):
                return True
            else:
                print(f"{Colors.WARNING}   └─ Denied by user{Colors.RESET}")
                skipped_tools.add(tool_name)
                return False
        
        for event in self.send_message(message, confirm_callback=on_confirm):
            clear_thinking()
            
            if event["type"] == "text":
                print_assistant_message(event["content"])
                final_text.append(event["content"])
            elif event["type"] == "tool_call":
                has_tool_calls = True
                # Tool call display is handled in on_confirm for confirmed tools
                # For auto mode, display here
                if not event.get("needs_confirmation", False):
                    print_iteration(event["iteration"], event["max_iterations"])
                    print_tool_call(event["name"], event["args"])
            elif event["type"] == "tool_skipped":
                # Tool was denied by user
                pass
            elif event["type"] == "tool_result":
                print_tool_result(event["result"], event["success"], event.get("name"))
            elif event["type"] == "warning":
                print_warning(event["content"])
            elif event["type"] == "error":
                print_error(event["content"])
                final_text.append(f"Error: {event['content']}")
        
        # Print completion message
        if has_tool_calls:
            print_task_complete()
        
        return "\n".join(final_text)
    
    def run_single_message_capture(self, message: str) -> str:
        """Run message and capture tool calls for web interface (no console output)."""
        final_text = []
        self.last_tool_calls = []
        
        for event in self.send_message(message):
            if event["type"] == "text":
                final_text.append(event["content"])
            elif event["type"] == "tool_call":
                self.last_tool_calls.append({
                    "name": event["name"],
                    "args": event["args"],
                    "result": None
                })
            elif event["type"] == "tool_result":
                # Update last tool call with result
                if self.last_tool_calls:
                    self.last_tool_calls[-1]["result"] = event["result"]
            elif event["type"] == "error":
                final_text.append(f"Error: {event['content']}")
        
        return "\n".join(final_text)
    
    def run_single_message_with_callbacks(self, message: str, on_tool_call=None, on_tool_result=None) -> str:
        """Run message with callbacks for streaming to web interface."""
        final_text = []
        
        for event in self.send_message(message):
            if event["type"] == "text":
                final_text.append(event["content"])
            elif event["type"] == "tool_call":
                if on_tool_call:
                    on_tool_call(event["name"], event["args"])
            elif event["type"] == "tool_result":
                if on_tool_result:
                    on_tool_result(event.get("name", ""), event["result"])
            elif event["type"] == "error":
                final_text.append(f"Error: {event['content']}")
        
        return "\n".join(final_text)
    
    def cleanup(self):
        terminal_manager.cleanup()


class GeminiAgent(BaseAgent):
    """Agent using Google's Gemini API."""
    
    def __init__(self, api_key: str, model_name: str = "gemini-3-pro-preview"):
        super().__init__(api_key)
        self.model_name = model_name
        
        import google.generativeai as genai
        from google.generativeai.types import GenerationConfig, Tool, FunctionDeclaration
        
        self.genai = genai
        genai.configure(api_key=api_key)
        
        # Build tools
        function_declarations = []
        for decl in TOOL_DECLARATIONS:
            func_decl = FunctionDeclaration(
                name=decl["name"],
                description=decl["description"],
                parameters=decl["parameters"]
            )
            function_declarations.append(func_decl)
        
        self.tools = [Tool(function_declarations=function_declarations)]
        
        # Initialize model
        self.model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=GenerationConfig(
                max_output_tokens=config.max_tokens,
                temperature=config.temperature,
            ),
            tools=self.tools,
            system_instruction=self.get_system_prompt(),
        )
        
        self.chat = None
    
    def start_chat(self):
        self.chat = self.model.start_chat(history=self.history)
    
    def send_message(self, message: str, confirm_callback=None) -> Generator[dict, None, None]:
        if self.chat is None:
            self.start_chat()
        
        iteration = 0
        max_iterations = config.max_iterations
        retry_count = 0
        max_retries = 2
        
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
        
        memory_manager.add_conversation("user", message)
        current_message = message
        
        try:
            response = self.chat.send_message(current_message)
            
            while iteration < max_iterations:
                iteration += 1
                
                # Check for malformed function call error
                if response.candidates:
                    candidate = response.candidates[0]
                    if hasattr(candidate, 'finish_reason'):
                        finish_reason = str(candidate.finish_reason)
                        if 'MALFORMED_FUNCTION_CALL' in finish_reason:
                            retry_count += 1
                            if retry_count <= max_retries:
                                yield {"type": "warning", "content": f"Model generated malformed function call, retrying... ({retry_count}/{max_retries})"}
                                # Reset chat and ask model to be more careful
                                self.chat = None
                                self.start_chat()
                                retry_message = f"""The previous attempt failed. Please be very careful with function calls and ensure all required parameters are properly formatted.

Original request: {message}

IMPORTANT: Generate valid JSON for all function parameters. Do not include comments in JSON. Make sure all strings are properly quoted."""
                                response = self.chat.send_message(retry_message)
                                continue
                            else:
                                yield {"type": "error", "content": "Model keeps generating malformed function calls. Try simplifying your request or using a different model (/models)."}
                                return
                
                text_response, tool_calls = self._process_response(response)
                
                if text_response:
                    yield {"type": "text", "content": text_response}
                    memory_manager.add_conversation("assistant", text_response)
                
                if not tool_calls:
                    break
                
                tool_results = []
                for tool_call in tool_calls:
                    needs_confirm = self.should_confirm_tool(tool_call["name"])
                    
                    # Yield tool_call first so user can see what's being called
                    yield {
                        "type": "tool_call",
                        "name": tool_call["name"],
                        "args": tool_call["args"],
                        "iteration": iteration,
                        "max_iterations": max_iterations,
                        "needs_confirmation": needs_confirm
                    }
                    
                    # Check confirmation AFTER showing the tool call
                    if confirm_callback and needs_confirm:
                        if not confirm_callback(tool_call["name"], tool_call["args"]):
                            # User denied - tell AI the tool was denied
                            yield {
                                "type": "tool_skipped",
                                "name": tool_call["name"],
                                "reason": "denied by user"
                            }
                            tool_results.append({
                                "name": tool_call["name"], 
                                "response": {"success": False, "error": "Tool execution denied by user. Please ask for alternative approach or skip this action."}
                            })
                            continue
                    
                    result = self.execute_tool(tool_call["name"], tool_call["args"])
                    
                    yield {
                        "type": "tool_result",
                        "name": tool_call["name"],
                        "result": result,
                        "success": result.get("success", False)
                    }
                    
                    tool_results.append({"name": tool_call["name"], "response": result})
                
                response_parts = []
                for tr in tool_results:
                    response_parts.append(
                        self.genai.protos.Part(
                            function_response=self.genai.protos.FunctionResponse(
                                name=tr["name"],
                                response={"result": json.dumps(tr["response"])}
                            )
                        )
                    )
                
                response = self.chat.send_message(response_parts)
            
            if iteration >= max_iterations:
                yield {"type": "warning", "content": f"Reached maximum iterations ({max_iterations})."}
                
        except Exception as e:
            error_str = str(e)
            # Check for malformed function call in exception
            if 'MALFORMED_FUNCTION_CALL' in error_str or 'malformed' in error_str.lower():
                yield {"type": "error", "content": "The AI generated an invalid function call. This can happen with complex requests. Try:\n1. Breaking your request into smaller steps\n2. Using a different model (/models)\n3. Being more specific about what you want"}
            else:
                yield {"type": "error", "content": error_str}
    
    def _process_response(self, response):
        text_parts = []
        tool_calls = []
        
        try:
            for candidate in response.candidates:
                # Check for blocked or error responses
                if hasattr(candidate, 'finish_reason'):
                    reason = str(candidate.finish_reason)
                    if 'SAFETY' in reason or 'BLOCKED' in reason:
                        text_parts.append("[Response blocked by safety filters]")
                        continue
                    if 'MALFORMED' in reason:
                        # Skip malformed candidates
                        continue
                
                if not hasattr(candidate, 'content') or not candidate.content:
                    continue
                    
                for part in candidate.content.parts:
                    if hasattr(part, 'text') and part.text:
                        text_parts.append(part.text)
                    elif hasattr(part, 'function_call') and part.function_call:
                        fc = part.function_call
                        try:
                            # Try to safely extract args
                            args = dict(fc.args) if fc.args else {}
                            tool_calls.append({"name": fc.name, "args": args})
                        except Exception:
                            # Skip malformed function calls
                            pass
        except Exception as e:
            text_parts.append(f"[Error processing response: {str(e)}]")
        
        text_response = "\n".join(text_parts) if text_parts else None
        return text_response, tool_calls


class OpenAIAgent(BaseAgent):
    """Agent using OpenAI's API."""
    
    def __init__(self, api_key: str, model_name: str = "GPT-5.1"):
        super().__init__(api_key)
        self.model_name = model_name
        
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)
        self.messages = []
    
    def start_chat(self):
        self.messages = [{"role": "system", "content": self.get_system_prompt()}]
    
    def _build_tools(self):
        """Convert tool declarations to OpenAI format."""
        tools = []
        for decl in TOOL_DECLARATIONS:
            tools.append({
                "type": "function",
                "function": {
                    "name": decl["name"],
                    "description": decl["description"],
                    "parameters": decl["parameters"]
                }
            })
        return tools
    
    def send_message(self, message: str, confirm_callback=None) -> Generator[dict, None, None]:
        if confirm_callback:
            self.set_confirmation_callback(confirm_callback)
            
        if not self.messages:
            self.start_chat()
        
        iteration = 0
        max_iterations = config.max_iterations
        
        if self.plan_mode:
            message = f"""[PLAN MODE ACTIVE] 
Create a file called 'plan.md' with overview, file structure, technologies, implementation plan, and challenges.
DO NOT create any code files yet. Only create plan.md.

User request: {message}"""
        
        self.messages.append({"role": "user", "content": message})
        memory_manager.add_conversation("user", message)
        
        try:
            while iteration < max_iterations:
                iteration += 1
                
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=self.messages,
                    tools=self._build_tools(),
                    tool_choice="auto",
                    max_tokens=config.max_tokens,
                    temperature=config.temperature
                )
                
                msg = response.choices[0].message
                
                if msg.content:
                    yield {"type": "text", "content": msg.content}
                    memory_manager.add_conversation("assistant", msg.content)
                    self.messages.append({"role": "assistant", "content": msg.content})
                
                if not msg.tool_calls:
                    break
                
                self.messages.append(msg)
                
                for tool_call in msg.tool_calls:
                    func_name = tool_call.function.name
                    func_args = json.loads(tool_call.function.arguments)
                    
                    needs_confirm = self.should_confirm_tool(func_name)
                    
                    yield {
                        "type": "tool_call",
                        "name": func_name,
                        "args": func_args,
                        "iteration": iteration,
                        "max_iterations": max_iterations,
                        "needs_confirmation": needs_confirm
                    }
                    
                    # Check confirmation BEFORE executing tool
                    if needs_confirm and self._confirm_callback:
                        approved = self._confirm_callback(func_name, func_args)
                        if not approved:
                            yield {"type": "tool_skipped", "name": func_name, "reason": "Denied by user"}
                            self.messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps({"success": False, "error": "Action denied by user"})
                            })
                            continue
                    
                    result = self.execute_tool(func_name, func_args)
                    
                    yield {
                        "type": "tool_result",
                        "name": func_name,
                        "result": result,
                        "success": result.get("success", False)
                    }
                    
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result)
                    })
            
            if iteration >= max_iterations:
                yield {"type": "warning", "content": f"Reached maximum iterations ({max_iterations})."}
                
        except Exception as e:
            yield {"type": "error", "content": str(e)}
    
    def clear_history(self):
        super().clear_history()
        self.messages = []


class OpenRouterAgent(BaseAgent):
    """Agent using OpenRouter API (supports multiple providers)."""
    
    def __init__(self, api_key: str, model_name: str = "gpt-4o", openrouter_model_id: str = "openai/gpt-4o"):
        super().__init__(api_key)
        self.model_name = model_name
        self.model_id = openrouter_model_id
        
        from openai import OpenAI
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        self.messages = []
    
    def start_chat(self):
        self.messages = [{"role": "system", "content": self.get_system_prompt()}]
    
    def _build_tools(self):
        """Convert tool declarations to OpenAI format."""
        tools = []
        for decl in TOOL_DECLARATIONS:
            tools.append({
                "type": "function",
                "function": {
                    "name": decl["name"],
                    "description": decl["description"],
                    "parameters": decl["parameters"]
                }
            })
        return tools
    
    def send_message(self, message: str, confirm_callback=None) -> Generator[dict, None, None]:
        if confirm_callback:
            self.set_confirmation_callback(confirm_callback)
            
        if not self.messages:
            self.start_chat()
        
        iteration = 0
        max_iterations = config.max_iterations
        
        if self.plan_mode:
            message = f"""[PLAN MODE ACTIVE] 
Create a file called 'plan.md' with overview, file structure, technologies, implementation plan, and challenges.
DO NOT create any code files yet. Only create plan.md.

User request: {message}"""
        
        self.messages.append({"role": "user", "content": message})
        memory_manager.add_conversation("user", message)
        
        try:
            while iteration < max_iterations:
                iteration += 1
                
                response = self.client.chat.completions.create(
                    model=self.model_id,
                    messages=self.messages,
                    tools=self._build_tools(),
                    tool_choice="auto",
                    max_tokens=config.max_tokens,
                    temperature=config.temperature,
                    extra_headers={
                        "HTTP-Referer": "https://github.com/aadc",
                        "X-Title": "AADC - Agentic AI Developer Console"
                    }
                )
                
                msg = response.choices[0].message
                
                if msg.content:
                    yield {"type": "text", "content": msg.content}
                    memory_manager.add_conversation("assistant", msg.content)
                    self.messages.append({"role": "assistant", "content": msg.content})
                
                if not msg.tool_calls:
                    break
                
                self.messages.append(msg)
                
                for tool_call in msg.tool_calls:
                    func_name = tool_call.function.name
                    func_args = json.loads(tool_call.function.arguments)
                    
                    needs_confirm = self.should_confirm_tool(func_name)
                    
                    yield {
                        "type": "tool_call",
                        "name": func_name,
                        "args": func_args,
                        "iteration": iteration,
                        "max_iterations": max_iterations,
                        "needs_confirmation": needs_confirm
                    }
                    
                    # Check confirmation BEFORE executing tool
                    if needs_confirm and self._confirm_callback:
                        approved = self._confirm_callback(func_name, func_args)
                        if not approved:
                            yield {"type": "tool_skipped", "name": func_name, "reason": "Denied by user"}
                            self.messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps({"success": False, "error": "Action denied by user"})
                            })
                            continue
                    
                    result = self.execute_tool(func_name, func_args)
                    
                    yield {
                        "type": "tool_result",
                        "name": func_name,
                        "result": result,
                        "success": result.get("success", False)
                    }
                    
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result)
                    })
            
            if iteration >= max_iterations:
                yield {"type": "warning", "content": f"Reached maximum iterations ({max_iterations})."}
                
        except Exception as e:
            yield {"type": "error", "content": str(e)}
    
    def clear_history(self):
        super().clear_history()
        self.messages = []


class AnthropicAgent(BaseAgent):
    """Agent using Anthropic's Claude API."""
    
    def __init__(self, api_key: str, model_name: str = "claude-sonnet-4-5"):
        super().__init__(api_key)
        self.model_name = model_name
        
        from anthropic import Anthropic
        self.client = Anthropic(api_key=api_key)
        self.messages = []
    
    def start_chat(self):
        self.messages = []
    
    def _build_tools(self):
        """Convert tool declarations to Anthropic format."""
        tools = []
        for decl in TOOL_DECLARATIONS:
            tools.append({
                "name": decl["name"],
                "description": decl["description"],
                "input_schema": decl["parameters"]
            })
        return tools
    
    def send_message(self, message: str, confirm_callback=None) -> Generator[dict, None, None]:
        if confirm_callback:
            self.set_confirmation_callback(confirm_callback)
            
        iteration = 0
        max_iterations = config.max_iterations
        
        if self.plan_mode:
            message = f"""[PLAN MODE ACTIVE] 
Create a file called 'plan.md' with overview, file structure, technologies, implementation plan, and challenges.
DO NOT create any code files yet. Only create plan.md.

User request: {message}"""
        
        self.messages.append({"role": "user", "content": message})
        memory_manager.add_conversation("user", message)
        
        try:
            while iteration < max_iterations:
                iteration += 1
                
                response = self.client.messages.create(
                    model=self.model_name,
                    max_tokens=config.max_tokens,
                    system=self.get_system_prompt(),
                    tools=self._build_tools(),
                    messages=self.messages
                )
                
                # Process response
                assistant_content = []
                tool_uses = []
                
                for block in response.content:
                    if block.type == "text":
                        yield {"type": "text", "content": block.text}
                        memory_manager.add_conversation("assistant", block.text)
                        assistant_content.append({"type": "text", "text": block.text})
                    elif block.type == "tool_use":
                        tool_uses.append(block)
                        assistant_content.append({
                            "type": "tool_use",
                            "id": block.id,
                            "name": block.name,
                            "input": block.input
                        })
                
                self.messages.append({"role": "assistant", "content": assistant_content})
                
                if not tool_uses or response.stop_reason == "end_turn":
                    break
                
                # Execute tools
                tool_results = []
                for tool_use in tool_uses:
                    needs_confirm = self.should_confirm_tool(tool_use.name)
                    
                    yield {
                        "type": "tool_call",
                        "name": tool_use.name,
                        "args": tool_use.input,
                        "iteration": iteration,
                        "max_iterations": max_iterations,
                        "needs_confirmation": needs_confirm
                    }
                    
                    # Check confirmation BEFORE executing tool
                    if needs_confirm and self._confirm_callback:
                        approved = self._confirm_callback(tool_use.name, tool_use.input)
                        if not approved:
                            yield {"type": "tool_skipped", "name": tool_use.name, "reason": "Denied by user"}
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": tool_use.id,
                                "content": json.dumps({"success": False, "error": "Action denied by user"})
                            })
                            continue
                    
                    result = self.execute_tool(tool_use.name, tool_use.input)
                    
                    yield {
                        "type": "tool_result",
                        "name": tool_use.name,
                        "result": result,
                        "success": result.get("success", False)
                    }
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": json.dumps(result)
                    })
                
                self.messages.append({"role": "user", "content": tool_results})
            
            if iteration >= max_iterations:
                yield {"type": "warning", "content": f"Reached maximum iterations ({max_iterations})."}
                
        except Exception as e:
            yield {"type": "error", "content": str(e)}
    
    def clear_history(self):
        super().clear_history()
        self.messages = []


def create_agent(api_key: Optional[str] = None, model_name: Optional[str] = None) -> BaseAgent:
    """Factory function to create the appropriate agent based on model."""
    model = model_name or config.model
    
    if model not in AVAILABLE_MODELS:
        raise ValueError(f"Unknown model: {model}")
    
    model_info = AVAILABLE_MODELS[model]
    provider = model_info["provider"]
    
    # Check if we should use OpenRouter instead of native provider
    if config.use_openrouter or provider == "openrouter":
        key = api_key or config.get_api_key("OPENROUTER_API_KEY") or os.environ.get("OPENROUTER_API_KEY", "")
        if not key:
            raise ValueError("Service configuration error. Please contact support.")
        # Get the OpenRouter model ID for this model
        openrouter_model_id = model_info.get("openrouter_id", OPENROUTER_MODEL_MAP.get(provider, "openai/gpt-4o"))
        return OpenRouterAgent(key, model, openrouter_model_id)
    
    # Use native provider
    key = api_key or config.get_api_key(model)
    
    if not key:
        key_env = model_info["api_key_env"]
        raise ValueError(f"Service configuration error for {model}. Please contact support.")
    
    if provider == "gemini":
        return GeminiAgent(key, model)
    elif provider == "openai":
        return OpenAIAgent(key, model)
    elif provider == "anthropic":
        return AnthropicAgent(key, model)
    else:
        raise ValueError(f"Unknown provider: {provider}")
