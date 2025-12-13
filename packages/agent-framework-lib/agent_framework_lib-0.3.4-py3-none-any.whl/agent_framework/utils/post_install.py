"""
Post-installation script for agent-framework-lib.

This script automatically installs Playwright browsers after package installation.
"""

import subprocess
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def post_install():
    """Install playwright browsers after package installation"""
    try:
        logger.info("🔧 Installing Playwright Chromium browser...")
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("✅ Playwright Chromium installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.warning(f"⚠️  Could not install Playwright Chromium automatically: {e}")
        logger.warning("   Please run manually: playwright install chromium")
        return False
    except FileNotFoundError:
        logger.warning("⚠️  Playwright not found in dependencies")
        logger.warning("   Install with: uv add playwright")
        return False
    except Exception as e:
        logger.warning(f"⚠️  Unexpected error during Playwright installation: {e}")
        logger.warning("   Please run manually: playwright install chromium")
        return False


if __name__ == "__main__":
    post_install()
