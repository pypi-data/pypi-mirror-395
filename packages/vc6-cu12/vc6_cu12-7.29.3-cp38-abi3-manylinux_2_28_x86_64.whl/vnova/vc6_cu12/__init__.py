import os
import sys
import json
from pathlib import Path
from importlib import import_module

__version__ = '7.29.3-b8950063'
__gpu_framework__ = 'cu12'  

_utils_module = import_module(f".{'_PyVc6ILUtils'}", __name__)

_SSL_CERT_ERROR_MSG = (
    "SSL certificate verification failed. Please set the CURL_CA_BUNDLE environment "
    "variable to the path of your CA certificate bundle (e.g., /etc/ssl/certs/ca-certificates.crt)"
)

def _get_manifest_path():
    """Get the path to the manifest file using best practice location (OS-agnostic)."""
    home = Path.home()
    vc6_dir = home / ".vc6"
    return vc6_dir / "manifest.vc6metadata"


def _read_manifest():
    """Read license metadata from manifest file if it exists (OS-agnostic)."""
    manifest_path = _get_manifest_path()
    if not manifest_path.exists():
        return None
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError, OSError):
        return None


def _write_manifest(metadata):
    """Write license metadata to manifest file (OS-agnostic). Only saves license_key and license_secret."""
    if not isinstance(metadata, dict):
        return False
    
    # Extract only the fields we want to save
    manifest_data = {}
    if "license_key" in metadata:
        manifest_data["license_key"] = metadata["license_key"]
    if "license_secret" in metadata:
        manifest_data["license_secret"] = metadata["license_secret"]
    
    # Only write if we have at least one field
    if not manifest_data:
        return False
    
    manifest_path = _get_manifest_path()
    manifest_dir = manifest_path.parent
    
    try:
        # Create directory with appropriate permissions (OS-agnostic)
        # On Windows, mode parameter is ignored but doesn't cause errors
        manifest_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        
        # Write the manifest file with only license_key and license_secret
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest_data, f, indent=2)
        
        # Set file permissions (OS-agnostic - chmod silently fails on Windows but doesn't error)
        try:
            manifest_path.chmod(0o600)
        except (OSError, NotImplementedError):
            # chmod may not work on Windows or some filesystems, ignore silently
            pass
        
        return True
    except (IOError, OSError):
        return False


def _load_binary_metadata():
    # First check if manifest file exists
    manifest_data = _read_manifest()
    if manifest_data is not None:
        return manifest_data
    
    # If manifest doesn't exist, make API call
    if hasattr(_utils_module, "vc6_il_utils_get_binary_metadata"):
        try:
            raw = _utils_module.vc6_il_utils_get_binary_metadata() or ""
            if raw:
                metadata = json.loads(raw)
                
                status_code = metadata.get("status_code")
                if status_code and status_code != 200:
                    status = metadata.get("status", "Unknown error")
                    print(f"Error: Failed to retrieve VC-6 Licensing Information (status_code: {status_code}, status: {status})", file=sys.stderr)
                    return metadata
                
                # Save to manifest if API call was successful
                if status_code == 200:
                    _write_manifest(metadata)
                
                return metadata
        except Exception as exc:
            print(f"Error: Failed to retrieve VC-6 Licensing Information({exc})", file=sys.stderr)
    return {}


def _ensure_license_env():
    # Check if manifest file exists
    manifest_path = _get_manifest_path()
    if manifest_path.exists():
        print("VC-6 Licensing information acquired.")
        metadata = _load_binary_metadata()
    else:
        # Manifest doesn't exist, show EULA and get user acceptance
        if hasattr(_utils_module, "vc6_il_utils_get_eula_text"):
            eula_license = str(_utils_module.vc6_il_utils_get_eula_text())
        else:
            print("Installation Error: Missing Util Binaries")
            return

        msg = (
            "\nV-Nova VC-6 Python SDK EULA\n"
            "=====================================================\n\n"
            + eula_license
            + "\n"
        )

        if not sys.stdin or not sys.stdin.isatty():
            raise RuntimeError(
                msg + "\nNon-interactive session detected; set the environment variables VC6_LICENSE_ACTIVATION_KEY, VC6_LICENSE_ACTIVATION_PASSWORD and retry."
            )

        print(msg)
        while True:
            response = input("Do you accept the VC-6 SDK EULA? [y/N]: ").strip().lower()
            if response in {"y", "yes"}:
                break
            if response in {"n", "no", ""}:
                print("EULA not accepted; aborting initialisation.")
                return

        metadata = _load_binary_metadata()

    key = (metadata.get("license_key") or "").strip()
    pwd = (metadata.get("license_secret") or "").strip()

    if not key or not pwd:
        raise RuntimeError(
            "License information not found. Try to re-install the SDK or contact ai@v-nova.com."
        )


    os.environ["VC6_LICENSE_ACTIVATION_KEY"] = key
    os.environ["VC6_LICENSE_ACTIVATION_PASSWORD"] = pwd


_ensure_license_env()
