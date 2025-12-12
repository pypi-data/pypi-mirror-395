import os
import shutil
import signal
from pathlib import Path

from .defaults import get_default_config
from .logger import get_logger
from .utils import ensure_dir, get_s3_client, parse_s3_url


class AssetDownloader:
    """Download simulation assets from S3 using rclone's native caching."""

    def __init__(
        self, cache_dir="~/.fourierassets/cache", endpoint_url=None, verbose=False
    ):
        # Note: cache_dir is kept for backward compatibility but rclone handles caching internally
        self.cache_dir = Path(cache_dir).expanduser().resolve()
        self.verbose = verbose

        # Prioritize: explicit endpoint_url > user config > default config
        if endpoint_url:
            self.endpoint_url = endpoint_url
        else:
            # Get user's current configuration
            from .config import S3Config

            config = S3Config()
            user_creds = config.get_credentials()
            self.endpoint_url = user_creds.get(
                "endpoint_url"
            ) or get_default_config().get("endpoint_url")

        self.logger = get_logger(f"{__name__}.AssetDownloader")
        
        # Track current download for cleanup on interrupt
        self._current_download_path = None
        self._is_directory_download = False

    def _cleanup_incomplete_download(self):
        """Clean up incomplete download on interrupt."""
        if self._current_download_path and self._is_directory_download:
            path = Path(self._current_download_path)
            if path.exists():
                self.logger.warning(
                    "Cleaning up incomplete download: %s", self._current_download_path
                )
                try:
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()
                except Exception as e:
                    self.logger.error("Failed to clean up %s: %s", path, e)

    def download(self, s3_url):
        """Download asset from S3 URL and return local path.

        Simple approach: let rclone do what it does best.
        """
        # Parse S3 URL
        bucket, key = parse_s3_url(s3_url)
        s3_client = get_s3_client(self.endpoint_url, verbose=self.verbose)

        # Create a simple cache directory structure based on S3 path
        safe_bucket = bucket.replace("/", "_").replace(":", "_")
        if key:
            safe_key = key.replace("/", os.sep)
            cache_path = self.cache_dir / safe_bucket / safe_key
        else:
            cache_path = self.cache_dir / safe_bucket

        # Simple check: if it already exists, return it
        if cache_path.exists():
            self.logger.info("Asset already exists: %s", cache_path)
            return str(cache_path)

        # Determine if this is a file or directory download
        is_file = key and ("." in key.split("/")[-1])
        
        # Track current download for cleanup on interrupt
        self._current_download_path = str(cache_path)
        self._is_directory_download = not is_file
        
        # Set up interrupt handler for cleanup
        original_sigint = signal.getsignal(signal.SIGINT)
        original_sigterm = signal.getsignal(signal.SIGTERM)
        
        def interrupt_handler(signum, frame):
            self._cleanup_incomplete_download()
            # Reset to original handler and re-raise
            signal.signal(signal.SIGINT, original_sigint)
            signal.signal(signal.SIGTERM, original_sigterm)
            if signum == signal.SIGINT:
                raise KeyboardInterrupt()
            else:
                raise SystemExit(1)
        
        signal.signal(signal.SIGINT, interrupt_handler)
        signal.signal(signal.SIGTERM, interrupt_handler)

        try:
            # Ensure cache directory exists
            ensure_dir(cache_path.parent)

            self.logger.info("Downloading %s to %s", s3_url, cache_path)

            # Download to the exact target path
            if is_file:
                # This looks like a file - download it as a file
                s3_client.copyto_optimized(bucket, key, str(cache_path))
            else:
                # This looks like a directory - download it as a directory
                s3_client.copy_directory_optimized(bucket, key, str(cache_path))

            # Verify the download
            if cache_path.exists():
                self.logger.info("Downloaded to expected path: %s", cache_path)
                return str(cache_path)
            else:
                raise FileNotFoundError(
                    f"Download failed - {cache_path} does not exist"
                )

        except (KeyboardInterrupt, SystemExit):
            # Clean up on interrupt
            self._cleanup_incomplete_download()
            raise
        except Exception as e:
            # Clean up on error for directory downloads
            if self._is_directory_download:
                self._cleanup_incomplete_download()
            self.logger.error("Failed to download asset %s: %s", s3_url, str(e))
            raise
        finally:
            # Restore original signal handlers
            signal.signal(signal.SIGINT, original_sigint)
            signal.signal(signal.SIGTERM, original_sigterm)
            # Clear tracking
            self._current_download_path = None
            self._is_directory_download = False
