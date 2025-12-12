"""
Module signing functionality for HLA-Compass SDK.

Provides RSA-PSS signing and verification for module packages.
Compatible with frontend Web Crypto API implementation.
"""

import json
import base64
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature


class ModuleSigner:
    """Handles RSA-PSS signing and verification of module manifests."""

    KEY_SIZE = 4096
    ALGORITHM = "RSA-PSS"
    HASH_ALGORITHM = "SHA-256"

    def __init__(self, keys_dir: Optional[Path] = None):
        """
        Initialize the ModuleSigner.

        Args:
            keys_dir: Directory to store keys. Defaults to ~/.hla-compass/keys/
        """
        if keys_dir is None:
            keys_dir = Path.home() / ".hla-compass" / "keys"
        self.keys_dir = Path(keys_dir)
        self.keys_dir.mkdir(parents=True, exist_ok=True)

        self.private_key_path = self.keys_dir / "private.pem"
        self.public_key_path = self.keys_dir / "public.pem"

    def generate_keys(self, force: bool = False) -> Tuple[str, str]:
        """
        Generate RSA key pair for module signing.

        Args:
            force: If True, overwrite existing keys

        Returns:
            Tuple of (private_key_path, public_key_path)
        """
        if self.private_key_path.exists() and not force:
            raise FileExistsError(
                f"Keys already exist at {self.keys_dir}. "
                "Use force=True to regenerate."
            )

        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=self.KEY_SIZE, backend=default_backend()
        )

        # Save private key
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        self.private_key_path.write_bytes(private_pem)
        self.private_key_path.chmod(0o600)  # Secure permissions

        # Extract and save public key
        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        self.public_key_path.write_bytes(public_pem)
        self.public_key_path.chmod(0o644)

        return str(self.private_key_path), str(self.public_key_path)

    def load_private_key(self) -> rsa.RSAPrivateKey:
        """Load private key from file."""
        if not self.private_key_path.exists():
            raise FileNotFoundError(
                f"Private key not found at {self.private_key_path}. "
                "Run 'hla-compass configure' to generate keys."
            )

        private_pem = self.private_key_path.read_bytes()
        return serialization.load_pem_private_key(
            private_pem, password=None, backend=default_backend()
        )

    def load_public_key(self) -> rsa.RSAPublicKey:
        """Load public key from file."""
        if not self.public_key_path.exists():
            raise FileNotFoundError(
                f"Public key not found at {self.public_key_path}. "
                "Run 'hla-compass configure' to generate keys."
            )

        public_pem = self.public_key_path.read_bytes()
        return serialization.load_pem_public_key(public_pem, backend=default_backend())

    def get_public_key_string(self) -> str:
        """Get public key as base64 string (without PEM headers)."""
        public_key = self.load_public_key()
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return base64.b64encode(public_bytes).decode("utf-8")

    def sign_manifest(self, manifest: Dict[str, Any]) -> str:
        """
        Sign a module manifest using RSA-PSS with SHA-256.

        Args:
            manifest: Module manifest dictionary

        Returns:
            Base64-encoded signature string
        """
        # Remove signature field if present
        manifest_copy = {k: v for k, v in manifest.items() if k != "signature"}

        # Sort keys for consistent signing
        manifest_json = json.dumps(manifest_copy, sort_keys=True, separators=(",", ":"))
        manifest_bytes = manifest_json.encode("utf-8")

        # Load private key
        private_key = self.load_private_key()

        # Sign using RSA-PSS with SHA-256
        signature = private_key.sign(
            manifest_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )

        # Return base64-encoded signature
        return base64.b64encode(signature).decode("utf-8")

    def verify_signature(
        self,
        manifest: Dict[str, Any],
        signature: str,
        public_key_pem: Optional[str] = None,
    ) -> bool:
        """
        Verify a module manifest signature.

        Args:
            manifest: Module manifest dictionary
            signature: Base64-encoded signature string
            public_key_pem: Optional PEM-encoded public key (uses stored key if not provided)

        Returns:
            True if signature is valid, False otherwise
        """
        try:
            # Load public key
            if public_key_pem:
                public_key = serialization.load_pem_public_key(
                    public_key_pem.encode("utf-8"), backend=default_backend()
                )
            else:
                public_key = self.load_public_key()

            # Remove signature field for verification
            manifest_copy = {k: v for k, v in manifest.items() if k != "signature"}
            manifest_json = json.dumps(
                manifest_copy, sort_keys=True, separators=(",", ":")
            )
            manifest_bytes = manifest_json.encode("utf-8")

            # Decode signature
            signature_bytes = base64.b64decode(signature)

            # Verify using RSA-PSS with SHA-256
            public_key.verify(
                signature_bytes,
                manifest_bytes,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
            return True

        except (InvalidSignature, Exception):
            return False

    def get_key_fingerprint(self) -> str:
        """Get SHA-256 fingerprint of the public key."""
        public_key = self.load_public_key()
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        fingerprint = hashlib.sha256(public_bytes).digest()
        return base64.b64encode(fingerprint).decode("utf-8")

    def export_public_key(self, output_path: Optional[Path] = None) -> str:
        """
        Export public key in PEM format.

        Args:
            output_path: Optional path to save the key

        Returns:
            PEM-encoded public key string
        """
        public_pem = self.public_key_path.read_text()

        if output_path:
            output_path = Path(output_path)
            output_path.write_text(public_pem)

        return public_pem


def sign_module_package(
    package_path: Path, signer: Optional[ModuleSigner] = None
) -> Dict[str, Any]:
    """
    Sign a module package by adding signature to manifest.

    Args:
        package_path: Path to module package directory
        signer: Optional ModuleSigner instance (creates new if not provided)

    Returns:
        Updated manifest with signature
    """
    if signer is None:
        signer = ModuleSigner()

    # Load manifest
    manifest_path = package_path / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found at {manifest_path}")

    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    # Sign manifest
    signature = signer.sign_manifest(manifest)

    # Add signature and public key to manifest
    manifest["signature"] = signature
    manifest["publicKey"] = signer.get_public_key_string()
    manifest["signatureAlgorithm"] = signer.ALGORITHM
    manifest["hashAlgorithm"] = signer.HASH_ALGORITHM
    manifest["keyFingerprint"] = signer.get_key_fingerprint()

    # Save updated manifest
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    return manifest


def verify_module_package(
    package_path: Path, public_key_pem: Optional[str] = None
) -> bool:
    """
    Verify a signed module package.

    Args:
        package_path: Path to module package directory
        public_key_pem: Optional PEM-encoded public key

    Returns:
        True if signature is valid, False otherwise
    """
    # Load manifest
    manifest_path = package_path / "manifest.json"
    if not manifest_path.exists():
        return False

    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    # Check for signature
    if "signature" not in manifest:
        return False

    # Use embedded public key if available and no key provided
    if not public_key_pem and "publicKey" in manifest:
        # Convert base64 DER to PEM format
        public_der = base64.b64decode(manifest["publicKey"])
        public_key = serialization.load_der_public_key(
            public_der, backend=default_backend()
        )
        public_key_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")

    signer = ModuleSigner()
    return signer.verify_signature(manifest, manifest["signature"], public_key_pem)
