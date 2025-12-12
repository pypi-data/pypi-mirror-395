"""
Authentication management for IvyBloom CLI
"""

import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any
from rich.console import Console
from rich.prompt import Prompt

from .config import Config
from .crypto import encrypt_json, decrypt_json
from .colors import get_console, print_success, print_error, print_warning, print_info

console = get_console()

def _is_keyring_disabled(config: Optional["Config"] = None) -> bool:
    """Return True when keyring access should be disabled.

    Controlled by either environment variables or config:
      - IVYBLOOM_DISABLE_KEYRING=1 disables keyring entirely
      - PYTHON_KEYRING_BACKEND ending with "null.Keyring" implies disabled
      - config.config["disable_keyring"] set to truthy disables keyring
    """
    try:
        if os.getenv("IVYBLOOM_DISABLE_KEYRING") == "1":
            return True
        backend = os.getenv("PYTHON_KEYRING_BACKEND", "")
        if backend.endswith("null.Keyring"):
            return True
        if config is not None:
            cfg_map = getattr(config, "config", {}) or {}
            if bool(cfg_map.get("disable_keyring", False)):
                return True
    except Exception:
        pass
    return False

class AuthManager:
    """Manages authentication for IvyBloom CLI"""
    
    def __init__(self, config: Config):
        self.config = config
        self.service_name = "ivybloom-cli"
    
    def store_api_key(self, api_key: str, username: str = "default") -> None:
        """Store API key securely"""
        try:
            if not _is_keyring_disabled(self.config):
                try:
                    import keyring as _keyring  # Lazy import to avoid backend init when disabled
                    _keyring.set_password(self.service_name, username, api_key)
                    console.print("[green]API key stored securely[/green]")
                except Exception as e:
                    # Do not fail if secure storage is unavailable
                    console.print(f"[yellow]Warning: Could not use secure storage ({e})[/yellow]")
            # Also persist a local fallback copy to ensure subprocesses can read it
            # even if keyring backend differs or is unavailable.
            self._store_api_key_file(api_key)
        except Exception as e:
            # Fallback to file storage if keyring fails
            console.print(f"[yellow]Warning: Could not use secure storage ({e})[/yellow]")
            console.print("[yellow]Falling back to file storage[/yellow]")
            self._store_api_key_file(api_key)
    
    def get_api_key(self, username: str = "default") -> Optional[str]:
        """Retrieve stored API key from env, file fallback, or secure storage.
        
        Updated order of precedence (to avoid stale keyring entries in TUI/subprocesses):
          1) OS env var IVYBLOOM_API_KEY
          2) OS env var IVY_API_KEY (legacy)
          3) Local file fallback in config dir
          4) Secure storage via keyring
        """
        # 1) Environment variable overrides for easy persistence in CI/TUI subprocesses
        try:
            import os
            env_api_key = os.getenv("IVYBLOOM_API_KEY") or os.getenv("IVY_API_KEY")
            if env_api_key:
                return env_api_key.strip()
        except Exception:
            pass
        
        # 2) File fallback (preferred over keyring for cross-process consistency)
        file_key = self._get_api_key_file()
        if file_key:
            return file_key
        
        # 3) Secure storage via keyring (only if not disabled)
        if not _is_keyring_disabled(self.config):
            try:
                import keyring as _keyring  # Lazy import
                api_key = _keyring.get_password(self.service_name, username)
                if api_key:
                    return api_key
            except Exception:
                pass
        
        return None
    
    def remove_api_key(self, username: str = "default") -> None:
        """Remove stored API key and all authentication data"""
        if not _is_keyring_disabled(self.config):
            try:
                import keyring as _keyring
                _keyring.delete_password(self.service_name, username)
            except Exception:
                pass
        
        # Also remove from file storage
        self._remove_api_key_file()
        # Remove OAuth tokens as well
        self._remove_oauth_tokens()
        # Remove Clerk session
        self._remove_clerk_session()
        # Remove auth token
        self.remove_auth_token()
        console.print("[green]All credentials removed[/green]")
    
    def store_oauth_tokens(self, tokens: Dict[str, Any]) -> None:
        """Store OAuth tokens securely with expiration metadata"""
        # Add metadata for token management
        enhanced_tokens = tokens.copy()
        
        # Calculate expiration timestamp
        if 'expires_in' in tokens and tokens['expires_in']:
            expires_in_seconds = int(tokens['expires_in'])
            expiration_time = datetime.now() + timedelta(seconds=expires_in_seconds)
            enhanced_tokens['expires_at'] = expiration_time.isoformat()
        
        # Add storage timestamp
        enhanced_tokens['stored_at'] = datetime.now().isoformat()
        
        try:
            # Store tokens in keyring (optional) and file fallback
            if not _is_keyring_disabled(self.config):
                try:
                    import keyring as _keyring
                    tokens_json = json.dumps(enhanced_tokens)
                    _keyring.set_password(self.service_name, "oauth_tokens", tokens_json)
                    console.print("[green]OAuth tokens stored securely[/green]")
                except Exception as e:
                    console.print(f"[yellow]Warning: Could not use secure storage ({e})[/yellow]")
            # Always persist file fallback for robustness
            self._store_oauth_tokens_file(enhanced_tokens)
        except Exception as e:
            # Fallback to file storage only
            console.print(f"[yellow]Warning: Could not persist OAuth tokens ({e})[/yellow]")
    
    def get_oauth_tokens(self) -> Optional[Dict[str, Any]]:
        """Retrieve stored OAuth tokens.

        Order: file first (to avoid prompting), then keyring if enabled.
        """
        # 1) File first to avoid any secure storage prompts in TUI/subprocesses
        try:
            file_tokens = self._get_oauth_tokens_file()
            if file_tokens:
                return file_tokens
        except Exception:
            pass

        # 2) Secure storage via keyring (only if not disabled)
        if not _is_keyring_disabled(self.config):
            try:
                import keyring as _keyring
                tokens_json = _keyring.get_password(self.service_name, "oauth_tokens")
                if tokens_json:
                    return json.loads(tokens_json)
            except Exception:
                pass
        
        return None
    
    def _store_oauth_tokens_file(self, tokens: Dict[str, Any]) -> None:
        """Store OAuth tokens in file (fallback)"""
        tokens_path = self.config.config_dir / "oauth_tokens.json"
        tokens_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(tokens_path, 'w') as f:
            json.dump(tokens, f)
        
        # Set restrictive permissions
        tokens_path.chmod(0o600)
    
    def _get_oauth_tokens_file(self) -> Optional[Dict[str, Any]]:
        """Get OAuth tokens from file (fallback)"""
        tokens_path = self.config.config_dir / "oauth_tokens.json"
        
        if tokens_path.exists():
            try:
                with open(tokens_path, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        
        return None
    
    def _remove_oauth_tokens(self) -> None:
        """Remove OAuth tokens"""
        if not _is_keyring_disabled(self.config):
            try:
                import keyring as _keyring
                _keyring.delete_password(self.service_name, "oauth_tokens")
            except Exception:
                pass
        
        # Remove from file storage
        tokens_path = self.config.config_dir / "oauth_tokens.json"
        if tokens_path.exists():
            tokens_path.unlink()
    
    def are_tokens_expired(self, tokens: Dict[str, Any]) -> bool:
        """Check if OAuth tokens are expired"""
        if not tokens:
            return True
        
        # Check if we have expiration metadata
        if 'expires_at' in tokens:
            try:
                expires_at = datetime.fromisoformat(tokens['expires_at'])
                # Consider tokens expired if they expire within the next 5 minutes
                buffer_time = timedelta(minutes=5)
                return datetime.now() + buffer_time >= expires_at
            except (ValueError, TypeError):
                pass
        
        # Fallback: check if tokens are older than 1 hour (typical OAuth token lifetime)
        if 'stored_at' in tokens:
            try:
                stored_at = datetime.fromisoformat(tokens['stored_at'])
                return datetime.now() - stored_at > timedelta(hours=1)
            except (ValueError, TypeError):
                pass
        
        # If no metadata, assume expired for safety
        return True
    
    def refresh_oauth_tokens(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """Refresh OAuth tokens using refresh token"""
        try:
            import httpx
            
            api_url = self.config.get_api_url()
            token_url = f"{api_url.rstrip('/')}/auth/oauth/token"
            
            token_data = {
                'grant_type': 'refresh_token',
                'client_id': 'ivybloom-cli',
                'refresh_token': refresh_token
            }
            
            with httpx.Client() as client:
                response = client.post(token_url, data=token_data)
                
                if response.status_code == 200:
                    new_tokens = response.json()
                    
                    # Store the new tokens
                    self.store_oauth_tokens(new_tokens)
                    
                    return new_tokens
                else:
                    print_warning("Failed to refresh OAuth tokens. Please re-authenticate.")
                    return None
                    
        except Exception as e:
            print_warning(f"Token refresh failed: {e}")
            return None
    
    def get_valid_oauth_tokens(self) -> Optional[Dict[str, Any]]:
        """Get valid OAuth tokens, refreshing if necessary"""
        tokens = self.get_oauth_tokens()
        
        if not tokens:
            return None
        
        # Check if tokens are expired
        if self.are_tokens_expired(tokens):
            # Try to refresh if we have a refresh token
            if 'refresh_token' in tokens:
                refreshed_tokens = self.refresh_oauth_tokens(tokens['refresh_token'])
                if refreshed_tokens:
                    return refreshed_tokens
            
            # If refresh failed or no refresh token, remove expired tokens
            self._remove_oauth_tokens()
            return None
        
        return tokens
    
    def _store_api_key_file(self, api_key: str) -> None:
        """Store API key in file (fallback)"""
        api_key_path = self.config.get_api_key_path()
        api_key_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Store with restricted permissions (encrypted when crypto is available)
        payload = {"api_key": api_key}
        enc = encrypt_json(self.config, payload)
        if enc is not None:
            with open(api_key_path, 'wb') as f:
                f.write(enc)
        else:
            with open(api_key_path, 'w') as f:
                json.dump(payload, f)
        
        # Set file permissions (Unix-like systems only)
        try:
            api_key_path.chmod(0o600)
        except Exception:
            pass
    
    def _get_api_key_file(self) -> Optional[str]:
        """Get API key from file (fallback)"""
        api_key_path = self.config.get_api_key_path()
        
        if api_key_path.exists():
            try:
                # Try decrypt first
                try:
                    data_bytes = api_key_path.read_bytes()
                    dec = decrypt_json(self.config, data_bytes)
                    if isinstance(dec, dict) and dec.get("api_key"):
                        return dec.get("api_key")
                except Exception:
                    pass
                # Fallback to plaintext JSON
                with open(api_key_path, 'r') as f:
                    data = json.load(f)
                    return data.get("api_key")
            except Exception:
                pass
        
        return None
    
    def _remove_api_key_file(self) -> None:
        """Remove API key file (fallback)"""
        api_key_path = self.config.get_api_key_path()
        
        if api_key_path.exists():
            try:
                api_key_path.unlink()
            except Exception:
                pass
    
    def store_auth_token(self, token: str) -> None:
        """Store authentication token (for Clerk JWT)"""
        auth_token_path = self.config.get_auth_token_path()
        auth_token_path.parent.mkdir(parents=True, exist_ok=True)
        
        payload = {"token": token, "type": "jwt"}
        enc = encrypt_json(self.config, payload)
        if enc is not None:
            with open(auth_token_path, 'wb') as f:
                f.write(enc)
        else:
            with open(auth_token_path, 'w') as f:
                json.dump(payload, f)
        
        # Set file permissions
        try:
            auth_token_path.chmod(0o600)
        except Exception:
            pass

    def store_clerk_session(self, session_data: Dict[str, Any]) -> None:
        """Store Clerk session data securely"""
        # Add metadata for session management
        enhanced_session = session_data.copy()
        enhanced_session['stored_at'] = datetime.now().isoformat()
        
        # Calculate expiration if provided
        if 'expires_at' in session_data:
            # Store as-is if already provided
            pass
        elif 'expires_in' in session_data:
            # Convert expires_in to expires_at
            expires_in_seconds = int(session_data['expires_in'])
            expiration_time = datetime.now() + timedelta(seconds=expires_in_seconds)
            enhanced_session['expires_at'] = expiration_time.isoformat()
        
        try:
            # Store session in keyring (optional) and always in file
            if not _is_keyring_disabled(self.config):
                try:
                    import keyring as _keyring
                    session_json = json.dumps(enhanced_session)
                    _keyring.set_password(self.service_name, "clerk_session", session_json)
                    console.print("[green]Clerk session stored securely[/green]")
                except Exception as e:
                    console.print(f"[yellow]Warning: Could not use secure storage ({e})[/yellow]")
            # Always persist a local fallback copy (encrypted when available)
            self._store_clerk_session_file(enhanced_session)
        except Exception as e:
            console.print(f"[yellow]Warning: Could not persist Clerk session ({e})[/yellow]")

    def get_clerk_session(self) -> Optional[Dict[str, Any]]:
        """Retrieve stored Clerk session.

        Order: file first (to avoid prompting), then keyring if enabled.
        """
        # 1) File first to avoid any secure storage prompts in TUI/subprocesses
        try:
            file_session = self._get_clerk_session_file()
            if file_session:
                return file_session
        except Exception:
            pass

        # 2) Secure storage via keyring (only if not disabled)
        if not _is_keyring_disabled(self.config):
            try:
                import keyring as _keyring
                session_json = _keyring.get_password(self.service_name, "clerk_session")
                if session_json:
                    return json.loads(session_json)
            except Exception:
                pass
        
        return None

    def _store_clerk_session_file(self, session_data: Dict[str, Any]) -> None:
        """Store Clerk session in file (fallback)"""
        session_path = self.config.config_dir / "clerk_session.json"
        session_path.parent.mkdir(parents=True, exist_ok=True)
        
        enc = encrypt_json(self.config, session_data)
        if enc is not None:
            with open(session_path, 'wb') as f:
                f.write(enc)
        else:
            with open(session_path, 'w') as f:
                json.dump(session_data, f)
        
        # Set restrictive permissions
        session_path.chmod(0o600)

    def _get_clerk_session_file(self) -> Optional[Dict[str, Any]]:
        """Get Clerk session from file (fallback)"""
        session_path = self.config.config_dir / "clerk_session.json"
        
        if session_path.exists():
            try:
                # Try decrypt first
                try:
                    data_bytes = session_path.read_bytes()
                    dec = decrypt_json(self.config, data_bytes)
                    if isinstance(dec, dict):
                        return dec
                except Exception:
                    pass
                with open(session_path, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        
        return None

    def _remove_clerk_session(self) -> None:
        """Remove Clerk session"""
        if not _is_keyring_disabled(self.config):
            try:
                import keyring as _keyring
                _keyring.delete_password(self.service_name, "clerk_session")
            except Exception:
                pass
        
        # Remove from file storage
        session_path = self.config.config_dir / "clerk_session.json"
        if session_path.exists():
            session_path.unlink()

    def is_clerk_session_expired(self, session: Dict[str, Any]) -> bool:
        """Check if Clerk session is expired"""
        if not session:
            return True
        
        # Check if we have expiration metadata
        if 'expires_at' in session:
            try:
                expires_at = datetime.fromisoformat(session['expires_at'])
                # Consider session expired if it expires within the next 5 minutes
                buffer_time = timedelta(minutes=5)
                return datetime.now() + buffer_time >= expires_at
            except (ValueError, TypeError):
                pass
        
        # Fallback: check if session is older than 1 hour (typical JWT lifetime)
        if 'stored_at' in session:
            try:
                stored_at = datetime.fromisoformat(session['stored_at'])
                return datetime.now() - stored_at > timedelta(hours=1)
            except (ValueError, TypeError):
                pass
        
        # If no metadata, assume expired for safety
        return True

    def get_valid_clerk_session(self) -> Optional[Dict[str, Any]]:
        """Get valid Clerk session, removing if expired"""
        session = self.get_clerk_session()
        
        if not session:
            return None
        
        # Check if session is expired
        if self.is_clerk_session_expired(session):
            # Remove expired session
            self._remove_clerk_session()
            return None
        
        return session
    
    def get_auth_token(self) -> Optional[str]:
        """Get stored authentication token"""
        auth_token_path = self.config.get_auth_token_path()
        
        if auth_token_path.exists():
            # Try decrypt first
            try:
                data_bytes = auth_token_path.read_bytes()
                dec = decrypt_json(self.config, data_bytes)
                if isinstance(dec, dict) and dec.get("token"):
                    return dec.get("token")
            except Exception:
                pass
            # Fallback plaintext JSON
            try:
                with open(auth_token_path, 'r') as f:
                    data = json.load(f)
                    return data.get("token")
            except Exception:
                pass
        
        return None
    
    def remove_auth_token(self) -> None:
        """Remove stored authentication token"""
        auth_token_path = self.config.get_auth_token_path()
        
        if auth_token_path.exists():
            try:
                auth_token_path.unlink()
            except Exception:
                pass
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated with valid credentials.
        
        Prefers JWT auth if present; falls back to API key authentication.
        """
        # Prefer stored JWT token if available
        if self.get_auth_token():
            return True
        # Consider OAuth tokens valid if present and not expired (auto-refresh may occur)
        try:
            tokens = self.get_valid_oauth_tokens()
            if tokens and (tokens.get("access_token") or tokens.get("id_token")):
                return True
        except Exception:
            pass
        # Fallback to API key
        return self.get_api_key() is not None
    
    def get_auth_headers(self, *, prefer_jwt: bool = False) -> Dict[str, str]:
        """Get authentication headers for API requests.
        
        Default order (prefer_jwt=False): API key → stored JWT → OAuth access token
        When prefer_jwt=True: stored JWT → OAuth access token → API key
        
        This allows callers to override per-request behavior (e.g., retrying with JWT
        for backends that require a verifiable user token rather than an API key).
        """
        headers: Dict[str, str] = {}

        if prefer_jwt:
            # 1) Stored dedicated JWT
            jwt_token = self.get_auth_token()
            if jwt_token:
                headers["Authorization"] = f"Bearer {jwt_token}"
                return headers
            # 2) OAuth access token
            oauth_tokens = self.get_valid_oauth_tokens()
            if oauth_tokens and oauth_tokens.get("access_token"):
                headers["Authorization"] = f"Bearer {oauth_tokens['access_token']}"
                return headers
            # 3) Fallback to API key
            api_key = self.get_api_key()
            if api_key:
                # Prefer explicit API key header to avoid JWT parsing on backends
                headers["X-API-KEY"] = api_key
                # Maintain Authorization for backward compatibility
                headers["Authorization"] = f"Bearer {api_key}"
                return headers
            return headers

        # Default behavior: prefer API key first for CLI stability
        api_key = self.get_api_key()
        if api_key:
            # Prefer explicit API key header to avoid JWT parsing on backends
            headers["X-API-KEY"] = api_key
            # Maintain Authorization for backward compatibility
            headers["Authorization"] = f"Bearer {api_key}"
            return headers
        jwt_token = self.get_auth_token()
        if jwt_token:
            headers["Authorization"] = f"Bearer {jwt_token}"
            return headers
        oauth_tokens = self.get_valid_oauth_tokens()
        if oauth_tokens and oauth_tokens.get("access_token"):
            headers["Authorization"] = f"Bearer {oauth_tokens['access_token']}"
        return headers
    
    def prompt_for_api_key(self) -> Optional[str]:
        """Prompt user to enter API key"""
        console.print("\n[bold cyan]API Key Setup[/bold cyan]")
        console.print("You can create an API key at: https://ivybiosciences.com/settings/api-keys")
        console.print()
        
        api_key = Prompt.ask(
            "Enter your API key",
            password=True,
            show_default=False
        )
        
        if api_key and api_key.strip():
            return api_key.strip()
        
        return None