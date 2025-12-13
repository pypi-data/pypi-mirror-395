import os
import tempfile
import shutil
import logging

logger = logging.getLogger(__name__)

class FileManager:
    """Handles temporary file operations"""
    
    @staticmethod
    def create_temp_directory(product_name: str) -> str:
        """Create temporary directory for product files"""
        temp_dir = os.path.join(tempfile.gettempdir(), product_name)
        os.makedirs(temp_dir, exist_ok=True)
        logger.info(f"Created temp directory: {temp_dir}")
        return temp_dir
    
    @staticmethod
    def cleanup_temp_files(temp_dir: str) -> None:
        """Clean up temporary files"""
        try:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                logger.info(f"Cleaned up temp directory: {temp_dir}")
        except Exception as e:
            logger.error(f"Error cleaning up temp directory: {e}")
