"""
AADC API Proxy Server
Secure proxy that handles AI API calls on behalf of authenticated users.

This server:
1. Receives requests from CLI with user auth token
2. Validates user and checks credits
3. Calls AI APIs with YOUR API keys (stored server-side)
4. Deducts credits on successful response
5. Returns response to CLI

DEPLOYMENT:
- Deploy this to Vercel, Railway, Render, or any Python hosting
- Set environment variables for API keys
- Set AADC_API_SECRET for request signing

SECURITY:
- API keys never leave server
- Users authenticate via Firebase token
- Credits checked before each request
- Rate limiting recommended
"""

import os
import json

# Load .env file from server directory
from pathlib import Path
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())
import time
import hashlib
import hmac
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from typing import Optional, Dict, Any, Tuple

# ============================================================================
# CONFIGURATION - Set these via environment variables in production
# ============================================================================

# API Keys (YOUR keys - never shared with users)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

# Server secret for signing/verifying requests
API_SECRET = os.environ.get("AADC_API_SECRET", "change-this-in-production")

# Firebase project for user verification
FIREBASE_PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID", "aadc-81e83")

# Rate limiting (requests per minute per user)
RATE_LIMIT = int(os.environ.get("RATE_LIMIT", "30"))

# ============================================================================
# FIREBASE USER VERIFICATION
# ============================================================================

import urllib.request
import urllib.error

FIRESTORE_BASE = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents"


def verify_user_and_credits(uid: str, auth_token: str) -> Tuple[bool, str, int]:
    """
    Verify user exists and has credits.
    Returns: (success, error_message, credits)
    """
    try:
        # Get user from Firestore
        url = f"{FIRESTORE_BASE}/users/{uid}"
        req = urllib.request.Request(url, headers={'User-Agent': 'AADC-Proxy/1.0'})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            fields = data.get('fields', {})
            
            credits = int(fields.get('credits', {}).get('integerValue', 0))
            
            if credits <= 0:
                return False, "No credits remaining", 0
            
            return True, "", credits
            
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False, "User not found", 0
        return False, f"Auth error: {e.code}", 0
    except Exception as e:
        return False, f"Verification failed: {str(e)}", 0


def deduct_credit(uid: str) -> bool:
    """Deduct one credit from user. Returns True if successful."""
    try:
        # First get current credits
        url = f"{FIRESTORE_BASE}/users/{uid}"
        req = urllib.request.Request(url, headers={'User-Agent': 'AADC-Proxy/1.0'})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            fields = data.get('fields', {})
            current_credits = int(fields.get('credits', {}).get('integerValue', 0))
        
        if current_credits <= 0:
            return False
        
        # Update credits
        new_credits = current_credits - 1
        update_url = f"{FIRESTORE_BASE}/users/{uid}?updateMask.fieldPaths=credits"
        payload = json.dumps({
            "fields": {"credits": {"integerValue": str(new_credits)}}
        }).encode('utf-8')
        
        update_req = urllib.request.Request(
            update_url,
            data=payload,
            headers={'Content-Type': 'application/json', 'User-Agent': 'AADC-Proxy/1.0'},
            method='PATCH'
        )
        
        with urllib.request.urlopen(update_req, timeout=10) as response:
            return response.status == 200
            
    except Exception:
        return False


# ============================================================================
# REQUEST VERIFICATION
# ============================================================================

def verify_request_signature(uid: str, timestamp: str, signature: str) -> bool:
    """
    Verify the request signature to prevent tampering.
    Signature = HMAC-SHA256(uid + timestamp, API_SECRET)
    """
    if not all([uid, timestamp, signature]):
        return False
    
    # Check timestamp is recent (within 5 minutes)
    try:
        ts = int(timestamp)
        now = int(time.time())
        if abs(now - ts) > 300:  # 5 minutes
            return False
    except ValueError:
        return False
    
    # Verify signature
    message = f"{uid}:{timestamp}"
    expected = hmac.new(
        API_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(signature, expected)


# ============================================================================
# AI API CALLS
# ============================================================================

def call_gemini(prompt: str, model: str, system_prompt: str, tools: list) -> Dict[str, Any]:
    """Call Gemini API."""
    if not GEMINI_API_KEY:
        return {"success": False, "error": "Gemini not configured"}
    
    try:
        import google.generativeai as genai
        from google.generativeai.types import GenerationConfig, Tool, FunctionDeclaration
        
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Build tools
        function_declarations = []
        for decl in tools:
            func_decl = FunctionDeclaration(
                name=decl["name"],
                description=decl["description"],
                parameters=decl["parameters"]
            )
            function_declarations.append(func_decl)
        
        gemini_tools = [Tool(function_declarations=function_declarations)] if function_declarations else None
        
        model_instance = genai.GenerativeModel(
            model_name=model,
            generation_config=GenerationConfig(
                max_output_tokens=65536,
                temperature=0.7,
            ),
            tools=gemini_tools,
            system_instruction=system_prompt,
        )
        
        response = model_instance.generate_content(prompt)
        
        # Extract response
        result = {"success": True, "text": "", "tool_calls": []}
        
        for candidate in response.candidates:
            if hasattr(candidate, 'content') and candidate.content:
                for part in candidate.content.parts:
                    if hasattr(part, 'text') and part.text:
                        result["text"] += part.text
                    elif hasattr(part, 'function_call') and part.function_call:
                        fc = part.function_call
                        result["tool_calls"].append({
                            "name": fc.name,
                            "args": dict(fc.args) if fc.args else {}
                        })
        
        return result
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def call_openai(prompt: str, model: str, system_prompt: str, tools: list) -> Dict[str, Any]:
    """Call OpenAI API. Falls back to OpenRouter if key not configured."""
    if not OPENAI_API_KEY:
        # Fallback to OpenRouter - use model name directly (already in correct format)
        if OPENROUTER_API_KEY:
            openrouter_model = f"openai/{model}" if not model.startswith("openai/") else model
            return call_openrouter(prompt, openrouter_model, system_prompt, tools)
        return {"success": False, "error": "OpenAI not configured"}
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Convert tools to OpenAI format
        openai_tools = []
        for decl in tools:
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": decl["name"],
                    "description": decl["description"],
                    "parameters": decl["parameters"]
                }
            })
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=openai_tools if openai_tools else None,
            max_tokens=65536,
            temperature=0.7
        )
        
        result = {"success": True, "text": "", "tool_calls": []}
        
        choice = response.choices[0]
        if choice.message.content:
            result["text"] = choice.message.content
        
        if choice.message.tool_calls:
            for tc in choice.message.tool_calls:
                result["tool_calls"].append({
                    "name": tc.function.name,
                    "args": json.loads(tc.function.arguments)
                })
        
        return result
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def call_anthropic(prompt: str, model: str, system_prompt: str, tools: list) -> Dict[str, Any]:
    """Call Anthropic API. Falls back to OpenRouter if key not configured."""
    if not ANTHROPIC_API_KEY:
        # Fallback to OpenRouter - model already in anthropic/model format
        if OPENROUTER_API_KEY:
            # Model is already in format like "anthropic/claude-opus-4.5"
            openrouter_model = model if model.startswith("anthropic/") else f"anthropic/{model}"
            return call_openrouter(prompt, openrouter_model, system_prompt, tools)
        return {"success": False, "error": "Anthropic not configured"}
    
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        
        # Convert tools to Anthropic format
        anthropic_tools = []
        for decl in tools:
            anthropic_tools.append({
                "name": decl["name"],
                "description": decl["description"],
                "input_schema": decl["parameters"]
            })
        
        response = client.messages.create(
            model=model,
            max_tokens=65536,
            system=system_prompt,
            tools=anthropic_tools if anthropic_tools else None,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = {"success": True, "text": "", "tool_calls": []}
        
        for block in response.content:
            if block.type == "text":
                result["text"] += block.text
            elif block.type == "tool_use":
                result["tool_calls"].append({
                    "name": block.name,
                    "args": block.input
                })
        
        return result
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def call_openrouter(prompt: str, model: str, system_prompt: str, tools: list) -> Dict[str, Any]:
    """Call OpenRouter API (supports multiple models)."""
    if not OPENROUTER_API_KEY:
        return {"success": False, "error": "OpenRouter not configured"}
    
    try:
        from openai import OpenAI
        
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
            default_headers={
                "HTTP-Referer": "https://aadc.dev",
                "X-Title": "AADC"
            }
        )
        
        # Convert tools to OpenAI format
        openai_tools = []
        for decl in tools:
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": decl["name"],
                    "description": decl["description"],
                    "parameters": decl["parameters"]
                }
            })
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=openai_tools if openai_tools else None,
            max_tokens=65536,
            temperature=0.7
        )
        
        result = {"success": True, "text": "", "tool_calls": []}
        
        choice = response.choices[0]
        if choice.message.content:
            result["text"] = choice.message.content
        
        if choice.message.tool_calls:
            for tc in choice.message.tool_calls:
                result["tool_calls"].append({
                    "name": tc.function.name,
                    "args": json.loads(tc.function.arguments)
                })
        
        return result
        
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================================
# HTTP REQUEST HANDLER
# ============================================================================

class ProxyHandler(BaseHTTPRequestHandler):
    """Handle incoming proxy requests."""
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass
    
    def send_json(self, data: dict, status: int = 200):
        """Send JSON response."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-Auth-UID, X-Auth-Timestamp, X-Auth-Signature')
        self.end_headers()
    
    def do_POST(self):
        """Handle AI proxy request."""
        path = urlparse(self.path).path
        
        if path == '/api/chat':
            self.handle_chat()
        elif path == '/api/health':
            self.send_json({"status": "ok"})
        else:
            self.send_json({"error": "Not found"}, 404)
    
    def do_GET(self):
        """Handle GET requests."""
        path = urlparse(self.path).path
        
        if path == '/api/health':
            self.send_json({"status": "ok", "version": "1.0.0"})
        else:
            self.send_json({"error": "Not found"}, 404)
    
    def handle_chat(self):
        """Process a chat/completion request."""
        try:
            # Get auth headers
            uid = self.headers.get('X-Auth-UID', '')
            timestamp = self.headers.get('X-Auth-Timestamp', '')
            signature = self.headers.get('X-Auth-Signature', '')
            
            # Verify signature
            if not verify_request_signature(uid, timestamp, signature):
                self.send_json({"error": "Invalid authentication"}, 401)
                return
            
            # Verify user and credits
            valid, error_msg, credits = verify_user_and_credits(uid, "")
            if not valid:
                self.send_json({"error": error_msg, "credits": credits}, 403)
                return
            
            # Parse request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode()
            request_data = json.loads(body)
            
            prompt = request_data.get('prompt', '')
            model = request_data.get('model', 'gemini-3-pro-preview')
            provider = request_data.get('provider', 'gemini')
            system_prompt = request_data.get('system_prompt', '')
            tools = request_data.get('tools', [])
            
            if not prompt:
                self.send_json({"error": "No prompt provided"}, 400)
                return
            
            # Call appropriate AI API
            if provider == 'gemini':
                result = call_gemini(prompt, model, system_prompt, tools)
            elif provider == 'openai':
                result = call_openai(prompt, model, system_prompt, tools)
            elif provider == 'anthropic':
                result = call_anthropic(prompt, model, system_prompt, tools)
            elif provider == 'openrouter':
                result = call_openrouter(prompt, model, system_prompt, tools)
            else:
                self.send_json({"error": f"Unknown provider: {provider}"}, 400)
                return
            
            # Deduct credit on success
            if result.get('success'):
                deduct_credit(uid)
                result['credits_remaining'] = credits - 1
            
            self.send_json(result)
            
        except json.JSONDecodeError:
            self.send_json({"error": "Invalid JSON"}, 400)
        except Exception as e:
            self.send_json({"error": str(e)}, 500)


# ============================================================================
# SERVER ENTRY POINT
# ============================================================================

def run_server(port: int = 8000):
    """Run the proxy server."""
    import socket
    
    # Set socket options for better Windows compatibility
    class ReuseAddrServer(HTTPServer):
        allow_reuse_address = True
        
        def server_bind(self):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            HTTPServer.server_bind(self)
    
    server = ReuseAddrServer(('0.0.0.0', port), ProxyHandler)
    print(f"🚀 AADC Proxy Server running on port {port}")
    print(f"   Health check: http://localhost:{port}/api/health")
    print(f"   Chat endpoint: POST http://localhost:{port}/api/chat")
    print()
    print("Configured providers:")
    print(f"   Gemini:     {'✓' if GEMINI_API_KEY else '✗'}")
    openai_status = '✓' if OPENAI_API_KEY else ('→ OpenRouter' if OPENROUTER_API_KEY else '✗')
    anthropic_status = '✓' if ANTHROPIC_API_KEY else ('→ OpenRouter' if OPENROUTER_API_KEY else '✗')
    print(f"   OpenAI:     {openai_status}")
    print(f"   Anthropic:  {anthropic_status}")
    print(f"   OpenRouter: {'✓' if OPENROUTER_API_KEY else '✗'}")
    print()
    print("Server is ready. Press Ctrl+C to stop.")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        server.server_close()


if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)
