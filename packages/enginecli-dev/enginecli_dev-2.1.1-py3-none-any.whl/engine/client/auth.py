"""
Auth module - handles local license key storage.
"""
import json
import uuid
import hashlib
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict
from datetime import datetime


# Config directory
ENGINE_DIR = Path.home() / ".engine"
LICENSE_FILE = ENGINE_DIR / "license.json"


@dataclass
class StoredLicense:
    """Locally stored license info."""
    license_key: str
    tier: str
    activated_at: str
    machine_id: str
    # Cached limits for offline grace period
    daily_limit: int = 0
    monthly_limit: int = 0


def get_machine_id() -> str:
    """Generate a unique machine ID."""
    # Use a combination of factors to create a stable machine ID
    import platform
    
    factors = [
        platform.node(),  # Hostname
        platform.machine(),  # CPU architecture
        platform.system(),  # OS name
    ]
    
    combined = "|".join(factors)
    return hashlib.sha256(combined.encode()).hexdigest()[:32]


def ensure_engine_dir():
    """Create .engine directory if it doesn't exist."""
    ENGINE_DIR.mkdir(parents=True, exist_ok=True)


def save_license(license_key: str, tier: str, limits: dict = None):
    """Save license key locally after activation."""
    ensure_engine_dir()
    
    stored = StoredLicense(
        license_key=license_key,
        tier=tier,
        activated_at=datetime.utcnow().isoformat(),
        machine_id=get_machine_id(),
        daily_limit=limits.get("generations_per_day", 0) if limits else 0,
        monthly_limit=limits.get("generations_per_month", 0) if limits else 0,
    )
    
    with open(LICENSE_FILE, "w") as f:
        json.dump(asdict(stored), f, indent=2)


def get_license_key() -> Optional[str]:
    """Get stored license key."""
    if not LICENSE_FILE.exists():
        return None
    
    try:
        with open(LICENSE_FILE) as f:
            data = json.load(f)
            return data.get("license_key")
    except (json.JSONDecodeError, IOError):
        return None


def get_stored_license() -> Optional[StoredLicense]:
    """Get full stored license info."""
    if not LICENSE_FILE.exists():
        return None
    
    try:
        with open(LICENSE_FILE) as f:
            data = json.load(f)
            return StoredLicense(**data)
    except (json.JSONDecodeError, IOError, TypeError):
        return None


def clear_license():
    """Remove stored license."""
    if LICENSE_FILE.exists():
        LICENSE_FILE.unlink()


def is_license_stored() -> bool:
    """Check if a license is stored locally."""
    return get_license_key() is not None
