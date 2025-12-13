# Copyright 2025 Subnoto
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import asyncio
from http.cookiejar import Cookie, CookieJar
from typing import Optional
from urllib.parse import urlparse

import httpx

try:
    from oak_session_py.oak_client import PyClientSession
except ImportError as e:
    raise ImportError(
        f"oak_client module not found: {e}\n"
        "Make sure oak_session_py is built:\n"
        "  eval \"$(direnv export bash)\" && bazel build //oak_session_py:oak_client"
    )

from .types import SubnotoConfig, SubnotoError


class SessionManager:
    """Manages Oak session encryption using PyO3 bindings from oak_session_py"""
    
    def __init__(self, config: SubnotoConfig, http_client: Optional[httpx.AsyncClient] = None):
        self.config = config
        self.session_id: Optional[str] = None
        self.handshake_in_progress = False
        self.cookie_jar = CookieJar()
        self.http_client = http_client  # Use provided client for handshake (with signatures)
        
        # Create Oak client session using PyO3
        self._session = PyClientSession(
            unattested=config.unattested,
            attester_key=config.attester_key
        )
    
    def _is_session_open(self) -> bool:
        """Check if the session is open"""
        return self._session.is_open()
    
    async def ensure_session(self) -> None:
        """Ensure session is established, performing handshake if needed"""
        if self._is_session_open():
            return
        
        if self.handshake_in_progress:
            # Wait for existing handshake
            while self.handshake_in_progress:
                await asyncio.sleep(0.05)
            return
        
        await self._handshake()
    
    async def _handshake(self) -> None:
        """Perform the Oak session handshake"""
        self.handshake_in_progress = True
        
        try:
            max_steps = 4
            step = 0
            
            while not self._is_session_open() and step < max_steps:
                step += 1
                
                # Get outgoing handshake message
                outgoing = self._session.get_outgoing_message()
                if not outgoing:
                    break
                
                if self._is_session_open():
                    break
                
                # Send to server
                url = f"{self.config.api_base_url}/tunnel/session"
                headers = {"Content-Type": "application/octet-stream"}
                
                if self.session_id:
                    headers["X-Session-Id"] = self.session_id
                
                # Add cookies
                cookies_str = self._get_cookies_for_request(url)
                if cookies_str:
                    headers["Cookie"] = cookies_str
                
                # Use provided client if available (has signatures), otherwise create new one
                if self.http_client:
                    response = await self.http_client.post(
                        url,
                        content=outgoing,
                        headers=headers
                    )
                else:
                    async with httpx.AsyncClient() as client:
                        response = await client.post(
                            url,
                            content=outgoing,
                            headers=headers
                        )
                
                # Extract session ID from first response
                if not self.session_id:
                    session_id_header = response.headers.get("X-Session-Id")
                    if not session_id_header:
                        raise SubnotoError("No session ID received from server")
                    self.session_id = session_id_header
                
                if not response.is_success:
                    error_text = response.text
                    raise SubnotoError(
                        f"Handshake failed with status {response.status_code}: {error_text}",
                        response.status_code
                    )
                
                # Store cookies
                self._store_cookies(response, url)
                
                # Process response
                response_data = response.content
                if len(response_data) > 0:
                    self._session.put_incoming_message(bytes(response_data))
                else:
                    raise SubnotoError("Empty response from server during handshake")
            
            if not self._is_session_open() or not self.session_id:
                raise SubnotoError("Failed to establish session after handshake")
        
        finally:
            self.handshake_in_progress = False
    
    def encrypt_request(self, plaintext: bytes) -> bytes:
        """Encrypt a request body"""
        if not self._is_session_open():
            raise SubnotoError("Session not open")
        
        try:
            # PyClientSession.write expects string, returns bytes
            plaintext_str = plaintext.decode('utf-8')
            self._session.write(plaintext_str)
            
            # Get the encrypted message
            encrypted = self._session.get_outgoing_message()
            if not encrypted:
                raise SubnotoError("No encrypted message available")
            
            return encrypted
        except Exception as e:
            raise SubnotoError(f"Encryption failed: {e}")
    
    def decrypt_response(self, encrypted: bytes) -> bytes:
        """Decrypt a response body"""
        if not self._is_session_open():
            raise SubnotoError("Session not open")
        
        try:
            # Put the encrypted response into the session
            self._session.put_incoming_message(encrypted)
            
            # Read the decrypted plaintext
            decrypted_str = self._session.read()
            if decrypted_str is None:
                raise SubnotoError("No decrypted message available")
            
            return decrypted_str.encode('utf-8')
        except Exception as e:
            raise SubnotoError(f"Decryption failed: {e}")
    
    def get_session_id(self) -> Optional[str]:
        """Get the current session ID"""
        return self.session_id
    
    def _get_cookies_for_request(self, url: str) -> str:
        """Get cookies for a request URL"""
        from urllib.request import Request as UrllibRequest
        request = UrllibRequest(url)
        self.cookie_jar.add_cookie_header(request)
        return request.get_header("Cookie", "")
    
    def _store_cookies(self, response: httpx.Response, url: str) -> None:
        """Store cookies from a response"""
        # Extract Set-Cookie headers and add to jar
        for cookie_str in response.headers.get_list("set-cookie"):
            # Parse cookie string into Cookie object
            try:
                # Simple parsing - in production might want to use http.cookies
                parts = cookie_str.split(';')[0].split('=', 1)
                if len(parts) == 2:
                    name, value = parts
                    parsed_url = urlparse(url)
                    cookie = Cookie(
                        version=0,
                        name=name.strip(),
                        value=value.strip(),
                        port=None,
                        port_specified=False,
                        domain=parsed_url.netloc,
                        domain_specified=True,
                        domain_initial_dot=False,
                        path='/',
                        path_specified=True,
                        secure=False,
                        expires=None,
                        discard=True,
                        comment=None,
                        comment_url=None,
                        rest={},
                        rfc2109=False
                    )
                    self.cookie_jar.set_cookie(cookie)
            except Exception:
                pass  # Skip malformed cookies
    
    def destroy(self) -> None:
        """Destroy the session"""
        self._session = None
        self.session_id = None
    
    def get_attestation_results(self) -> Optional[str]:
        """Get attestation results as JSON string"""
        if not self._session:
            return None
        try:
            return self._session.get_attestation_results()
        except Exception:
            return None
    
    def get_attestation_status(self) -> Optional[str]:
        """Get attestation status as JSON string"""
        if not self._session:
            return None
        try:
            return self._session.get_attestation_status()
        except Exception:
            return None
