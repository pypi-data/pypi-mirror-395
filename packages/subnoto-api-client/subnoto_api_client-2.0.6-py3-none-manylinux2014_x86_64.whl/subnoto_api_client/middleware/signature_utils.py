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

"""
HTTP signature utilities for signing requests (RFC 9421)

Uses http-message-signatures library (RFC 9421 implementation)
"""

import base64
import hashlib
import time
from typing import Dict

from http_message_signatures import HTTPMessageSigner, HTTPSignatureKeyResolver, algorithms
from http_message_signatures import http_sfv


class SubnotoHTTPSignatureKeyResolver(HTTPSignatureKeyResolver):
    """Key resolver for Subnoto API signatures"""
    
    def __init__(self, access_key: str, secret_key: str):
        self.access_key = access_key
        self.secret_key_bytes = bytes.fromhex(secret_key)
    
    def resolve_private_key(self, key_id: str):
        if key_id == self.access_key:
            return self.secret_key_bytes
        return None


def sign_request_headers(
    url: str,
    method: str,
    body_content: bytes,
    access_key: str,
    secret_key: str,
    existing_headers: Dict[str, str]
) -> Dict[str, str]:
    """
    Generate HTTP signature headers for a request using RFC 9421
    
    Returns a dictionary of headers to add to the request, including:
    - X-Timestamp
    - Digest (legacy)
    - Content-Digest (RFC 9530)
    - Content-Type
    - Content-Length
    - Signature-Input
    - Signature
    """
    # Generate digests
    sha256_hash = hashlib.sha256(body_content).digest()
    digest_base64 = base64.b64encode(sha256_hash).decode("utf-8")
    
    # Legacy Digest header (for compatibility)
    digest = f"SHA-256={digest_base64}"
    
    # RFC 9530 Content-Digest header (using http_sfv for proper formatting)
    content_digest_dict = http_sfv.Dictionary({"sha-256": sha256_hash})
    content_digest = str(content_digest_dict)
    
    # Timestamp
    timestamp = str(int(time.time() * 1000))
    
    # Get content type from existing headers (case-insensitive)
    content_type = "application/json"
    for k, v in existing_headers.items():
        if k.lower() == "content-type":
            content_type = v
            break
    
    # Build headers dict
    headers = {
        "X-Timestamp": timestamp,
        "Digest": digest,
        "Content-Digest": content_digest,
        "Content-Type": content_type,
        "Content-Length": str(len(body_content)),
    }
    
    # Simple object for the signing library (modifies headers in place)
    class SignableRequest:
        pass
    
    request = SignableRequest()
    request.method = method
    request.url = url
    request.headers = headers
    request.body = body_content
    
    # Sign the request
    key_resolver = SubnotoHTTPSignatureKeyResolver(access_key, secret_key)
    signer = HTTPMessageSigner(
        signature_algorithm=algorithms.HMAC_SHA256,
        key_resolver=key_resolver
    )
    signer.sign(
        request,
        key_id=access_key,
        covered_component_ids=(
            "x-timestamp",
            "@authority",
            "content-type",
            "content-digest",
            "content-length"
        )
    )
    
    # Replace "pyhms" label with "team"
    if "Signature" in headers:
        headers["Signature"] = headers["Signature"].replace("pyhms=", "team=")
    if "Signature-Input" in headers:
        headers["Signature-Input"] = headers["Signature-Input"].replace("pyhms=", "team=")
    
    return headers
