#!/usr/bin/env python3
"""
GitHub Integration for AADC
Handles GitHub authentication, repo creation, and automatic commits
"""

import os
import json
import subprocess
import webbrowser
from pathlib import Path
from typing import Optional, Dict, Any
import httpx

# GitHub OAuth App credentials
# Client ID is public and safe to include in code
# To set up your own OAuth app:
# 1. Go to https://github.com/settings/developers
# 2. Click "New OAuth App" or "New GitHub App"
# 3. For OAuth App: No callback URL needed for device flow
# 4. For GitHub App: Enable "Device Flow" in permissions
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID", "Ov23liMVxt2t9tAC5P34")
# Client Secret is loaded from environment for security
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET", "")

# File to store GitHub token
GITHUB_TOKEN_FILE = Path.home() / ".aadc" / "github_token.json"


class GitHubIntegration:
    """Manages GitHub integration for automatic repo creation and commits."""
    
    def __init__(self):
        self.token = None
        self.username = None
        self._load_token()
    
    def _load_token(self):
        """Load GitHub token from file."""
        if GITHUB_TOKEN_FILE.exists():
            try:
                data = json.loads(GITHUB_TOKEN_FILE.read_text())
                self.token = data.get("token")
                self.username = data.get("username")
            except Exception:
                pass
    
    def _save_token(self, token: str, username: str):
        """Save GitHub token to file."""
        GITHUB_TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
        data = {"token": token, "username": username}
        GITHUB_TOKEN_FILE.write_text(json.dumps(data, indent=2))
        self.token = token
        self.username = username
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated with GitHub."""
        return self.token is not None
    
    async def authenticate_with_device_flow(self) -> bool:
        """
        Authenticate with GitHub using device flow.
        Returns True if successful.
        """
        from utils import Colors
        
        try:
            async with httpx.AsyncClient() as client:
                # Step 1: Request device code
                response = await client.post(
                    "https://github.com/login/device/code",
                    data={
                        "client_id": GITHUB_CLIENT_ID,
                        "scope": "repo user"
                    },
                    headers={"Accept": "application/json"}
                )
                
                if response.status_code != 200:
                    print(f"{Colors.RED}Failed to get device code: {response.status_code} - {response.text}{Colors.RESET}")
                    print(f"\n{Colors.YELLOW}⚠️  GitHub OAuth app may not be configured correctly.{Colors.RESET}")
                    print(f"{Colors.GRAY}The OAuth app needs to support Device Flow authentication.{Colors.RESET}")
                    print(f"{Colors.GRAY}Current Client ID: {GITHUB_CLIENT_ID}{Colors.RESET}\n")
                    return False
                
                data = response.json()
                device_code = data["device_code"]
                user_code = data["user_code"]
                verification_uri = data["verification_uri"]
                interval = data.get("interval", 5)
            
            # Step 2: Show user code and open browser
            print(f"\n{Colors.CYAN}🔐 GitHub Authentication{Colors.RESET}")
            print(f"{Colors.WHITE}Visit: {Colors.CYAN}{verification_uri}{Colors.RESET}")
            print(f"{Colors.WHITE}Enter code: {Colors.YELLOW}{user_code}{Colors.RESET}\n")
            
            webbrowser.open(verification_uri)
            
            print(f"{Colors.GRAY}Waiting for authentication...{Colors.RESET}")
            
            # Step 3: Poll for access token
            import asyncio
            while True:
                await asyncio.sleep(interval)
                
                token_response = await client.post(
                    "https://github.com/login/oauth/access_token",
                    data={
                        "client_id": GITHUB_CLIENT_ID,
                        "device_code": device_code,
                        "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
                    },
                    headers={"Accept": "application/json"}
                )
                
                result = token_response.json()
                
                if "access_token" in result:
                    token = result["access_token"]
                    
                    # Get username
                    user_response = await client.get(
                        "https://api.github.com/user",
                        headers={
                            "Authorization": f"Bearer {token}",
                            "Accept": "application/vnd.github+json"
                        }
                    )
                    
                    if user_response.status_code == 200:
                        username = user_response.json()["login"]
                        self._save_token(token, username)
                        print(f"\n{Colors.GREEN}✓ Authenticated as {username}{Colors.RESET}\n")
                        return True
                    break
                
                elif result.get("error") == "authorization_pending":
                    continue
                elif result.get("error") == "slow_down":
                    interval += 5
                    continue
                else:
                    print(f"{Colors.RED}Authentication failed: {result.get('error')}{Colors.RESET}")
                    break
        except Exception as e:
            print(f"{Colors.RED}Error during authentication: {str(e)}{Colors.RESET}")
            import traceback
            traceback.print_exc()
        
        return False
    
    def logout(self):
        """Log out from GitHub."""
        if GITHUB_TOKEN_FILE.exists():
            GITHUB_TOKEN_FILE.unlink()
        self.token = None
        self.username = None
    
    async def create_repo(self, repo_name: str, description: str = "", private: bool = False) -> Optional[str]:
        """
        Create a new GitHub repository.
        Returns the repo URL if successful, None otherwise.
        """
        if not self.is_authenticated():
            return None
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.github.com/user/repos",
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Accept": "application/vnd.github+json",
                    "X-GitHub-Api-Version": "2022-11-28"
                },
                json={
                    "name": repo_name,
                    "description": description,
                    "private": private,
                    "auto_init": False
                }
            )
            
            if response.status_code == 201:
                data = response.json()
                return data["html_url"]
            elif response.status_code == 422:
                # Repo already exists
                return f"https://github.com/{self.username}/{repo_name}"
            else:
                return None
    
    async def check_repo_exists(self, repo_name: str) -> bool:
        """Check if a repository exists."""
        if not self.is_authenticated():
            return False
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.github.com/repos/{self.username}/{repo_name}",
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Accept": "application/vnd.github+json"
                }
            )
            return response.status_code == 200
    
    def init_git_repo(self, project_path: str) -> bool:
        """Initialize git repository in project if not already initialized."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=project_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return True  # Already a git repo
            
            # Initialize new repo
            subprocess.run(["git", "init"], cwd=project_path, check=True)
            subprocess.run(["git", "branch", "-M", "main"], cwd=project_path, check=True)
            return True
            
        except Exception:
            return False
    
    def add_remote(self, project_path: str, repo_name: str) -> bool:
        """Add GitHub remote to local repository."""
        try:
            remote_url = f"https://github.com/{self.username}/{repo_name}.git"
            
            # Check if remote already exists
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                cwd=project_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Remote exists, update it
                subprocess.run(
                    ["git", "remote", "set-url", "origin", remote_url],
                    cwd=project_path,
                    check=True
                )
            else:
                # Add new remote
                subprocess.run(
                    ["git", "remote", "add", "origin", remote_url],
                    cwd=project_path,
                    check=True
                )
            
            return True
        except Exception:
            return False
    
    def commit_and_push(self, project_path: str, message: str = "Auto-commit by AADC") -> bool:
        """
        Commit all changes and push to GitHub.
        Returns True if successful.
        """
        try:
            # Stage all changes
            subprocess.run(["git", "add", "."], cwd=project_path, check=True)
            
            # Check if there are changes to commit
            result = subprocess.run(
                ["git", "diff", "--cached", "--quiet"],
                cwd=project_path,
                capture_output=True
            )
            
            if result.returncode == 0:
                # No changes to commit
                return True
            
            # Commit changes
            subprocess.run(
                ["git", "commit", "-m", message],
                cwd=project_path,
                check=True,
                capture_output=True
            )
            
            # Push to GitHub using token authentication
            remote_url = f"https://{self.username}:{self.token}@github.com/{self.username}/"
            
            subprocess.run(
                ["git", "push", "-u", "origin", "main"],
                cwd=project_path,
                check=True,
                capture_output=True,
                env={**os.environ, "GIT_TERMINAL_PROMPT": "0"}
            )
            
            return True
            
        except subprocess.CalledProcessError:
            return False
    
    def get_last_commit_hash(self, project_path: str) -> Optional[str]:
        """Get the hash of the last commit."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=project_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except Exception:
            return None


# Global GitHub integration instance
github_integration = GitHubIntegration()
