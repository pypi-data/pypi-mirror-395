"""
CLI Authentication Module
Handles user authentication via web browser OAuth flow.
"""

import os
import json
import webbrowser
import http.server
import socketserver
import urllib.parse
import threading
import time
from pathlib import Path
from typing import Optional, Dict, Any

# Auth configuration
AUTH_DIR = Path.home() / ".aadc"
AUTH_FILE = AUTH_DIR / "auth.json"
WEBSITE_URL = os.environ.get("AADC_WEBSITE_URL", "https://aadc-website.vercel.app")
CALLBACK_PORT = 8742

# Import Firebase client for direct Firestore access
try:
    from firebase_client import get_user_data, deduct_credit_firestore
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False

class AuthManager:
    """Manages CLI authentication state."""
    
    def __init__(self):
        self.auth_data: Optional[Dict[str, Any]] = None
        self._load_auth()
    
    def _load_auth(self):
        """Load saved authentication data."""
        if AUTH_FILE.exists():
            try:
                with open(AUTH_FILE, 'r') as f:
                    self.auth_data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.auth_data = None
    
    def _save_auth(self):
        """Save authentication data to disk."""
        AUTH_DIR.mkdir(parents=True, exist_ok=True)
        with open(AUTH_FILE, 'w') as f:
            json.dump(self.auth_data, f, indent=2)
        # Set restrictive permissions on auth file
        try:
            os.chmod(AUTH_FILE, 0o600)
        except:
            pass  # Windows doesn't support chmod the same way
    
    def is_logged_in(self) -> bool:
        """Check if user is currently logged in."""
        return self.auth_data is not None and 'uid' in self.auth_data
    
    def get_user(self) -> Optional[Dict[str, Any]]:
        """Get current user data."""
        return self.auth_data
    
    def get_credits(self) -> int:
        """Get current credit balance from Firestore."""
        if not self.auth_data or 'uid' not in self.auth_data:
            return 0
        
        # Try to sync from Firestore
        if FIREBASE_AVAILABLE:
            try:
                user_data = get_user_data(self.auth_data['uid'])
                if user_data:
                    self.auth_data['credits'] = user_data.get('credits', 0)
                    self._save_auth()
                    return user_data.get('credits', 0)
            except Exception:
                pass  # Fall back to cached value
        
        return self.auth_data.get('credits', 0)
    
    def update_credits(self, new_balance: int):
        """Update local credit balance."""
        if self.auth_data:
            self.auth_data['credits'] = new_balance
            self._save_auth()
    
    def deduct_credit(self) -> bool:
        """Deduct one credit from Firestore. Returns True if successful, False if no credits."""
        if not self.auth_data or 'uid' not in self.auth_data:
            return False
        
        if FIREBASE_AVAILABLE:
            try:
                success, remaining = deduct_credit_firestore(self.auth_data['uid'])
                if success:
                    self.auth_data['credits'] = remaining
                    self._save_auth()
                    return True
                else:
                    # No credits or failed
                    self.auth_data['credits'] = remaining
                    self._save_auth()
                    return False
            except Exception as e:
                from utils import Colors
                print(f"{Colors.YELLOW}⚠ Could not sync with Firestore: {e}{Colors.RESET}")
        
        # Fallback to local deduction
        credits = self.auth_data.get('credits', 0)
        if credits <= 0:
            return False
        self.auth_data['credits'] = credits - 1
        self._save_auth()
        return True
    
    def sync_user_data(self) -> bool:
        """Sync user data from Firestore."""
        if not self.auth_data or 'uid' not in self.auth_data:
            return False
        
        if FIREBASE_AVAILABLE:
            try:
                user_data = get_user_data(self.auth_data['uid'])
                if user_data:
                    self.auth_data['credits'] = user_data.get('credits', 0)
                    self.auth_data['plan'] = user_data.get('plan', 'free')
                    self.auth_data['displayName'] = user_data.get('displayName', self.auth_data.get('displayName'))
                    self.auth_data['betaAccess'] = user_data.get('betaAccess', False)
                    self._save_auth()
                    return True
            except Exception:
                pass
        return False
    
    def has_beta_access(self) -> bool:
        """Check if user has beta access."""
        if not self.auth_data or 'uid' not in self.auth_data:
            return False
        
        # Sync from Firestore to get latest beta status
        if FIREBASE_AVAILABLE:
            try:
                user_data = get_user_data(self.auth_data['uid'])
                if user_data:
                    beta_access = user_data.get('betaAccess', False)
                    self.auth_data['betaAccess'] = beta_access
                    self._save_auth()
                    return beta_access
            except Exception:
                pass
        
        # Fallback to cached value
        return self.auth_data.get('betaAccess', False)
    
    def login(self) -> bool:
        """
        Initiate login flow via web browser.
        Opens browser to website login, waits for callback with auth token.
        Returns True if login successful.
        """
        from utils import Colors
        
        print(f"\n{Colors.CYAN}🔐 Authentication Required{Colors.RESET}")
        print(f"{Colors.GRAY}Opening browser to log in...{Colors.RESET}\n")
        
        # Create a simple HTTP server to receive the callback
        auth_received = threading.Event()
        auth_result = {'success': False, 'data': None}
        
        class CallbackHandler(http.server.BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                pass  # Suppress HTTP logs
            
            def do_GET(self):
                parsed = urllib.parse.urlparse(self.path)
                if parsed.path == '/callback':
                    # Parse query parameters
                    params = urllib.parse.parse_qs(parsed.query)
                    
                    if 'data' in params:
                        try:
                            # Decode the auth data from URL
                            import base64
                            data_str = base64.b64decode(params['data'][0]).decode('utf-8')
                            auth_result['data'] = json.loads(data_str)
                            auth_result['success'] = True
                        except Exception as e:
                            auth_result['success'] = False
                    
                    # Send success response
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    
                    if auth_result['success']:
                        response = '''
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <title>AADC - Login Successful</title>
                            <style>
                                body { 
                                    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                                    background: #0a0a0a; 
                                    color: white; 
                                    display: flex; 
                                    align-items: center; 
                                    justify-content: center; 
                                    height: 100vh; 
                                    margin: 0;
                                    text-align: center;
                                }
                                .container { max-width: 400px; padding: 40px; }
                                h1 { color: #ef4444; margin-bottom: 16px; }
                                p { color: #9ca3af; }
                                .checkmark { font-size: 64px; margin-bottom: 24px; }
                            </style>
                        </head>
                        <body>
                            <div class="container">
                                <div class="checkmark">✅</div>
                                <h1>Login Successful!</h1>
                                <p>You can close this window and return to the terminal.</p>
                            </div>
                        </body>
                        </html>
                        '''
                    else:
                        response = '''
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <title>AADC - Login Failed</title>
                            <style>
                                body { 
                                    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                                    background: #0a0a0a; 
                                    color: white; 
                                    display: flex; 
                                    align-items: center; 
                                    justify-content: center; 
                                    height: 100vh; 
                                    margin: 0;
                                    text-align: center;
                                }
                                .container { max-width: 400px; padding: 40px; }
                                h1 { color: #ef4444; margin-bottom: 16px; }
                                p { color: #9ca3af; }
                            </style>
                        </head>
                        <body>
                            <div class="container">
                                <h1>❌ Login Failed</h1>
                                <p>Please try again from the terminal.</p>
                            </div>
                        </body>
                        </html>
                        '''
                    
                    self.wfile.write(response.encode())
                    auth_received.set()
                else:
                    self.send_response(404)
                    self.end_headers()
        
        # Start callback server in a thread
        server = None
        try:
            # Use allow_reuse_address to prevent "address already in use" errors
            class ReusableTCPServer(socketserver.TCPServer):
                allow_reuse_address = True
            
            server = ReusableTCPServer(("127.0.0.1", CALLBACK_PORT), CallbackHandler)
            server.timeout = 1
            
            server_thread = threading.Thread(target=lambda: self._run_server(server, auth_received))
            server_thread.daemon = True
            server_thread.start()
            
            # Open browser to login page with callback URL
            callback_url = f"http://localhost:{CALLBACK_PORT}/callback"
            login_url = f"{WEBSITE_URL}/auth/cli?callback={urllib.parse.quote(callback_url)}"
            
            print(f"{Colors.WHITE}If browser doesn't open, visit:{Colors.RESET}")
            print(f"{Colors.CYAN}{login_url}{Colors.RESET}\n")
            
            webbrowser.open(login_url)
            
            # Wait for callback (timeout after 5 minutes)
            print(f"{Colors.GRAY}Waiting for authentication...{Colors.RESET}")
            auth_received.wait(timeout=300)
            
            if auth_result['success'] and auth_result['data']:
                self.auth_data = auth_result['data']
                self._save_auth()
                print(f"\n{Colors.GREEN}✓ Logged in as {self.auth_data.get('displayName', 'User')}{Colors.RESET}")
                print(f"{Colors.GRAY}  Credits: {self.auth_data.get('credits', 0)}{Colors.RESET}\n")
                return True
            else:
                print(f"\n{Colors.RED}✗ Login failed or timed out{Colors.RESET}\n")
                return False
                
        except OSError as e:
            print(f"{Colors.RED}Error starting auth server: {e}{Colors.RESET}")
            print(f"{Colors.YELLOW}Try manually logging in at {WEBSITE_URL}/login{Colors.RESET}")
            return False
        finally:
            if server:
                try:
                    server.shutdown()
                    server.server_close()
                except:
                    pass
                time.sleep(0.1)  # Brief delay to ensure cleanup
    
    def _run_server(self, server, stop_event):
        """Run the callback server until auth is received."""
        while not stop_event.is_set():
            server.handle_request()
    
    def logout(self):
        """Log out the current user."""
        self.auth_data = None
        if AUTH_FILE.exists():
            AUTH_FILE.unlink()
    
    def get_login_url(self) -> str:
        """Get the login URL for opening in browser."""
        callback_url = f"http://localhost:{CALLBACK_PORT}/callback"
        return f"{WEBSITE_URL}/auth/cli?callback={urllib.parse.quote(callback_url)}"
    
    def start_login_server_and_wait(self, timeout: int = 300) -> bool:
        """
        Start the callback server and wait for login.
        This is for pipe mode where we can't use interactive prompts.
        Returns True if login successful.
        """
        auth_received = threading.Event()
        auth_result = {'success': False, 'data': None}
        
        class CallbackHandler(http.server.BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                pass
            
            def do_GET(self):
                parsed = urllib.parse.urlparse(self.path)
                if parsed.path == '/callback':
                    params = urllib.parse.parse_qs(parsed.query)
                    
                    if 'data' in params:
                        try:
                            import base64
                            data_str = base64.b64decode(params['data'][0]).decode('utf-8')
                            auth_result['data'] = json.loads(data_str)
                            auth_result['success'] = True
                        except Exception:
                            auth_result['success'] = False
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    
                    response = '''
                    <!DOCTYPE html>
                    <html>
                    <head><title>AADC - Login</title>
                    <style>
                        body { font-family: sans-serif; background: #0a0a0a; color: white; 
                               display: flex; align-items: center; justify-content: center; 
                               height: 100vh; margin: 0; text-align: center; }
                        .container { max-width: 400px; padding: 40px; }
                        h1 { color: #ef4444; }
                    </style>
                    </head>
                    <body>
                        <div class="container">
                            <h1>''' + ('✅ Login Successful!' if auth_result['success'] else '❌ Login Failed') + '''</h1>
                            <p>You can close this window.</p>
                        </div>
                    </body>
                    </html>
                    '''
                    self.wfile.write(response.encode())
                    auth_received.set()
                else:
                    self.send_response(404)
                    self.end_headers()
        
        server = None
        try:
            class ReusableTCPServer(socketserver.TCPServer):
                allow_reuse_address = True
            
            server = ReusableTCPServer(("127.0.0.1", CALLBACK_PORT), CallbackHandler)
            server.timeout = 1
            
            server_thread = threading.Thread(target=lambda: self._run_server(server, auth_received))
            server_thread.daemon = True
            server_thread.start()
            
            # Wait for callback
            auth_received.wait(timeout=timeout)
            
            if auth_result['success'] and auth_result['data']:
                self.auth_data = auth_result['data']
                self._save_auth()
                return True
            return False
                
        except OSError:
            return False
        finally:
            if server:
                try:
                    server.shutdown()
                    server.server_close()
                except:
                    pass
                time.sleep(0.1)

    def refresh_from_server(self) -> bool:
        """
        Refresh user data from the server (sync credits, etc.)
        Returns True if successful.
        """
        return self.sync_user_data()


# Global auth manager instance
auth_manager = AuthManager()


def require_auth():
    """
    Decorator/function to require authentication.
    Returns True if authenticated, False otherwise.
    """
    if not auth_manager.is_logged_in():
        return auth_manager.login()
    return True


def check_credits() -> bool:
    """
    Check if user has credits available (syncs with server).
    Returns True if credits available, False otherwise.
    """
    from utils import Colors
    
    if not auth_manager.is_logged_in():
        print(f"{Colors.RED}Not logged in. Use /login to authenticate.{Colors.RESET}")
        return False
    
    # Get credits from server (syncs automatically)
    credits = auth_manager.get_credits()
    if credits <= 0:
        print(f"\n{Colors.RED}❌ No credits remaining!{Colors.RESET}")
        print(f"{Colors.YELLOW}Visit {WEBSITE_URL}/pricing to purchase more credits.{Colors.RESET}\n")
        return False
    
    return True


def use_credit() -> bool:
    """
    Use one credit for an AI prompt (deducts from server).
    Returns True if credit was deducted, False if no credits available.
    """
    from utils import Colors
    
    if not auth_manager.is_logged_in():
        print(f"{Colors.RED}Not logged in. Use /login to authenticate.{Colors.RESET}")
        return False
    
    success = auth_manager.deduct_credit()
    if success:
        remaining = auth_manager.auth_data.get('credits', 0) if auth_manager.auth_data else 0
        if remaining <= 3:
            print(f"{Colors.YELLOW}⚠️  {remaining} credits remaining{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}❌ No credits remaining!{Colors.RESET}")
        print(f"{Colors.YELLOW}Visit {WEBSITE_URL}/pricing to purchase more credits.{Colors.RESET}\n")
    
    return success
