"""Image processing and optimization service."""
from typing import List, Optional, Tuple
from pathlib import Path
import httpx
from PIL import Image
import io
import structlog

from config.settings import settings
from core.exceptions import MigrationError

logger = structlog.get_logger()


class ImageService:
    """Service for downloading, optimizing, and processing images."""
    
    def __init__(self):
        """Initialize image service."""
        self.storage_path = Path(settings.IMAGE_STORAGE_PATH)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        self.max_width = settings.IMAGE_MAX_WIDTH
        self.max_height = settings.IMAGE_MAX_HEIGHT
        self.quality = settings.IMAGE_QUALITY
        self.format = settings.IMAGE_FORMAT
    
    async def download_image(self, url: str) -> Optional[bytes]:
        """
        Download image from URL.
        
        Args:
            url: Image URL
            
        Returns:
            Optional[bytes]: Image data or None if download fails
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=30.0)
                response.raise_for_status()
                return response.content
        except Exception as e:
            logger.warning("Failed to download image", url=url, error=str(e))
            return None
    
    def optimize_image(
        self,
        image_data: bytes,
        max_width: Optional[int] = None,
        max_height: Optional[int] = None
    ) -> bytes:
        """
        Optimize and resize image.
        
        Args:
            image_data: Original image data
            max_width: Maximum width (optional)
            max_height: Maximum height (optional)
            
        Returns:
            bytes: Optimized image data
        """
        try:
            # Open image
            img = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Resize if needed
            width, height = img.size
            max_w = max_width or self.max_width
            max_h = max_height or self.max_height
            
            if width > max_w or height > max_h:
                img.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
            
            # Save to bytes
            output = io.BytesIO()
            img.save(
                output,
                format=self.format,
                quality=self.quality,
                optimize=True
            )
            
            return output.getvalue()
            
        except Exception as e:
            logger.error("Failed to optimize image", error=str(e))
            # Return original if optimization fails
            return image_data
    
    async def process_image(
        self,
        url: str,
        optimize: bool = True
    ) -> Optional[Tuple[bytes, str]]:
        """
        Download and optionally optimize image.
        
        Args:
            url: Image URL
            optimize: Whether to optimize the image
            
        Returns:
            Optional[Tuple[bytes, str]]: (image_data, filename) or None
        """
        # Download image
        image_data = await self.download_image(url)
        if not image_data:
            return None
        
        # Optimize if requested
        if optimize and settings.ENABLE_IMAGE_OPTIMIZATION:
            image_data = self.optimize_image(image_data)
        
        # Extract filename from URL
        filename = Path(url).name
        
        return (image_data, filename)
    
    async def process_images(
        self,
        urls: List[str],
        optimize: bool = True
    ) -> List[Tuple[bytes, str]]:
        """
        Process multiple images.
        
        Args:
            urls: List of image URLs
            optimize: Whether to optimize images
            
        Returns:
            List[Tuple[bytes, str]]: List of (image_data, filename) tuples
        """
        results = []
        
        for url in urls:
            result = await self.process_image(url, optimize)
            if result:
                results.append(result)
        
        return results
    
    def save_image(self, image_data: bytes, filename: str) -> Path:
        """
        Save image to storage.
        
        Args:
            image_data: Image data
            filename: Filename to save as
            
        Returns:
            Path: Path to saved file
        """
        file_path = self.storage_path / filename
        
        with open(file_path, 'wb') as f:
            f.write(image_data)
        
        logger.debug("Image saved", path=str(file_path))
        return file_path
