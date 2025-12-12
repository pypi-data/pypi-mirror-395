from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


def _read_version_file() -> str:
    """Read version from VERSION file, with proper error handling."""
    # Try multiple possible locations for VERSION file
    possible_version_paths = [
        # Production deployment path (where deployment scripts copy VERSION)
        Path("/sphere/VERSION"),
        # Development/repository path 
        Path(__file__).parent.parent / "VERSION",
        # Alternative production paths
        Path("/sphere/app/VERSION"),
        # Current working directory (fallback)
        Path("VERSION"),
    ]
    
    for version_file in possible_version_paths:
        try:
            if version_file.exists():
                version = version_file.read_text().strip()
                if version and version != "unknown":
                    return version
        except Exception:
            continue
    
    # Don't hide deployment issues with misleading fallbacks
    raise FileNotFoundError(
        f"VERSION file not found in expected locations: {[str(p) for p in possible_version_paths]}. "
        f"This indicates a deployment configuration issue."
    )


class Config(BaseSettings):
    """Configuration settings and dev defaults."""

    # Pull env vars from ".env" file, ignore any extra env vars defined
    # there that are not in this class.
    model_config = SettingsConfigDict(env_file='.env', extra='ignore', protected_namespaces=())

    # Read version from VERSION file - fail explicitly if not found
    try:
        version: str = _read_version_file()
    except FileNotFoundError as e:
        # Don't hide version issues - make them visible
        version: str = "VERSION_FILE_NOT_FOUND"
        print(f"⚠️ CONFIG WARNING: {e}")
        print("⚠️ This indicates a deployment configuration problem!")

    queue_dir: Path = Path("/sphere/app/featrix_queue")
    output_dir: Path = Path("/sphere/app/featrix_output")
    data_dir: Path = Path("/sphere/app/featrix_data")
    session_dir: Path = Path("/sphere/app/featrix_sessions")
    session_private_dir: Path = Path("/sphere/app/featrix_sessions_private")

    slack_hook_file: Path = Path("/etc/.hook")
    slack_hook_url: str | None = None

    resend_api_key: str | None = None
    
    # S3 configuration for customer uploads
    s3_uploads_bucket: str | None = None  # e.g., "featrix-customer-uploads"
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
    aws_region: str = "us-east-1"


config = Config(_env_file=".env", _env_file_encoding='utf-8')
