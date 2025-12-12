
"""
Media Processors Module - Handle image and audio file processing
"""

import base64
import os
import mimetypes
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
import logging
from PIL import Image as PILImage
import io

logger = logging.getLogger(__name__)


class ProcessorError(Exception):
    """Custom exception for processor errors"""
    pass


class BaseProcessor:
    """Base class for media processors"""
    
    def __init__(self, max_file_size: int = 10 * 1024 * 1024):  # 10MB default
        self.max_file_size = max_file_size
        self.supported_formats = set()
        
    def validate_file_path(self, path: str) -> Path:
        """
        Validate that the file path exists and is accessible.
        
        Args:
            path: File path to validate
            
        Returns:
            Path object
            
        Raises:
            ProcessorError: If file doesn't exist or is inaccessible
        """
        file_path = Path(path)
        
        if not file_path.exists():
            raise ProcessorError(f"File not found: {path}")
            
        if not file_path.is_file():
            raise ProcessorError(f"Path is not a file: {path}")
            
        if not os.access(file_path, os.R_OK):
            raise ProcessorError(f"File is not readable: {path}")
            
        # Check file size
        file_size = file_path.stat().st_size
        if file_size > self.max_file_size:
            raise ProcessorError(
                f"File size ({file_size} bytes) exceeds maximum allowed size ({self.max_file_size} bytes)"
            )
            
        return file_path
    
    def get_mime_type(self, file_path: Path) -> str:
        """Get MIME type of the file"""
        mime_type, _ = mimetypes.guess_type(str(file_path))
        return mime_type or 'application/octet-stream'
    
    def validate_base64(self, data: str) -> bool:
        """Validate base64 string"""
        try:
            # Check if it's a data URI
            if data.startswith('data:'):
                # Extract base64 part
                parts = data.split(',', 1)
                if len(parts) != 2:
                    return False
                data = parts[1]
                
            # Try to decode
            base64.b64decode(data, validate=True)
            return True
        except Exception:
            return False


class ImageProcessor(BaseProcessor):
    """
    Process images: load from path, convert to base64, save from base64
    """
    
    def __init__(self, max_file_size: int = 10 * 1024 * 1024):
        super().__init__(max_file_size)
        self.supported_formats = {
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', 
            '.webp', '.ico', '.tiff', '.svg'
        }
        
    def load_image_from_path(self, 
                           path: str, 
                           validate_image: bool = True,
                           as_data_uri: bool = True) -> str:
        """
        Load image from file path and convert to base64.
        
        Args:
            path: Path to the image file
            validate_image: Whether to validate the image can be opened
            as_data_uri: Return as data URI format (data:image/type;base64,...)
            
        Returns:
            Base64 encoded image string
            
        Raises:
            ProcessorError: If image cannot be loaded or validated
        """
        file_path = self.validate_file_path(path)
        
        # Check file extension
        extension = file_path.suffix.lower()
        if extension not in self.supported_formats:
            logger.warning(f"Unsupported image format: {extension}")
        
        # Validate image if requested
        if validate_image and extension != '.svg':
            try:
                with PILImage.open(file_path) as img:
                    # Verify the image can be loaded
                    img.verify()
            except Exception as e:
                raise ProcessorError(f"Invalid image file: {str(e)}")
        
        # Read and encode the file
        try:
            with open(file_path, 'rb') as f:
                image_data = f.read()
                encoded = base64.b64encode(image_data).decode('utf-8')
                
            if as_data_uri:
                # Determine image type
                mime_type = self.get_mime_type(file_path)
                if mime_type == 'application/octet-stream':
                    # Fallback to extension-based type
                    image_type = extension[1:] if extension else 'png'
                    mime_type = f'image/{image_type}'
                    
                return f"data:{mime_type};base64,{encoded}"
            else:
                return encoded
                
        except Exception as e:
            raise ProcessorError(f"Failed to read image file: {str(e)}")
    
    def save_image_from_base64(self,
                             image_data: str,
                             output_path: str,
                             auto_fix_extension: bool = True,
                             validate_image: bool = True) -> str:
        """
        Save base64 image data to file.
        
        Args:
            image_data: Base64 encoded image (with or without data URI prefix)
            output_path: Path where to save the image
            auto_fix_extension: Automatically fix file extension based on image type
            validate_image: Validate the decoded image before saving
            
        Returns:
            Final output path (may differ if auto_fix_extension is True)
            
        Raises:
            ProcessorError: If image data is invalid or cannot be saved
        """
        # Validate base64 data
        if not self.validate_base64(image_data):
            raise ProcessorError("Invalid base64 image data")
        
        # Parse data URI if present
        if image_data.startswith('data:'):
            try:
                header, encoded = image_data.split(',', 1)
                # Extract MIME type
                mime_type = header.split(':')[1].split(';')[0]
                image_type = mime_type.split('/')[1]
            except Exception:
                raise ProcessorError("Invalid data URI format")
        else:
            encoded = image_data
            image_type = None
        
        # Decode base64
        try:
            decoded_data = base64.b64decode(encoded)
        except Exception as e:
            raise ProcessorError(f"Failed to decode base64 data: {str(e)}")
        
        # Validate image if requested
        if validate_image:
            try:
                img = PILImage.open(io.BytesIO(decoded_data))
                img.verify()
                # Get actual format if not provided
                if image_type is None:
                    image_type = img.format.lower()
            except Exception as e:
                raise ProcessorError(f"Invalid image data: {str(e)}")
        
        # Handle output path and extension
        output_path = Path(output_path)
        
        if auto_fix_extension and image_type:
            correct_extension = f'.{image_type}'
            if output_path.suffix.lower() != correct_extension:
                output_path = output_path.with_suffix(correct_extension)
        
        # Create parent directories if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the file
        try:
            with open(output_path, 'wb') as f:
                f.write(decoded_data)
        except Exception as e:
            raise ProcessorError(f"Failed to save image: {str(e)}")
        
        return str(output_path)
    
    def get_image_info(self, path: str) -> Dict[str, Any]:
        """
        Get information about an image file.
        
        Returns:
            Dictionary with image metadata
        """
        file_path = self.validate_file_path(path)
        
        info = {
            'path': str(file_path),
            'size': file_path.stat().st_size,
            'mime_type': self.get_mime_type(file_path)
        }
        
        try:
            with PILImage.open(file_path) as img:
                info.update({
                    'format': img.format,
                    'mode': img.mode,
                    'width': img.width,
                    'height': img.height
                })
        except Exception as e:
            logger.warning(f"Could not read image metadata: {str(e)}")
            
        return info


class AudioProcessor(BaseProcessor):
    """
    Process audio files: load from path, convert to base64, save from base64
    """
    
    def __init__(self, max_file_size: int = 50 * 1024 * 1024):  # 50MB default for audio
        super().__init__(max_file_size)
        self.supported_formats = {
            '.mp3', '.wav', '.ogg', '.m4a', '.flac',
            '.aac', '.wma', '.opus', '.webm'
        }
        
    def load_audio_from_path(self,
                           path: str,
                           as_data_uri: bool = True) -> str:
        """
        Load audio from file path and convert to base64.
        
        Args:
            path: Path to the audio file
            as_data_uri: Return as data URI format
            
        Returns:
            Base64 encoded audio string
        """
        file_path = self.validate_file_path(path)
        
        # Check file extension
        extension = file_path.suffix.lower()
        if extension not in self.supported_formats:
            logger.warning(f"Unsupported audio format: {extension}")
        
        # Read and encode the file
        try:
            with open(file_path, 'rb') as f:
                audio_data = f.read()
                encoded = base64.b64encode(audio_data).decode('utf-8')
                
            if as_data_uri:
                mime_type = self.get_mime_type(file_path)
                if mime_type == 'application/octet-stream':
                    # Fallback to extension-based type
                    audio_type = extension[1:] if extension else 'mpeg'
                    mime_type = f'audio/{audio_type}'
                    
                return f"data:{mime_type};base64,{encoded}"
            else:
                return encoded
                
        except Exception as e:
            raise ProcessorError(f"Failed to read audio file: {str(e)}")
    
    def save_audio_from_base64(self,
                             audio_data: str,
                             output_path: str,
                             auto_fix_extension: bool = True) -> str:
        """
        Save base64 audio data to file.
        
        Args:
            audio_data: Base64 encoded audio
            output_path: Path where to save the audio
            auto_fix_extension: Automatically fix file extension
            
        Returns:
            Final output path
        """
        # Validate base64 data
        if not self.validate_base64(audio_data):
            raise ProcessorError("Invalid base64 audio data")
        
        # Parse data URI if present
        if audio_data.startswith('data:'):
            try:
                header, encoded = audio_data.split(',', 1)
                mime_type = header.split(':')[1].split(';')[0]
                audio_type = mime_type.split('/')[1]
            except Exception:
                raise ProcessorError("Invalid data URI format")
        else:
            encoded = audio_data
            audio_type = None
        
        # Decode base64
        try:
            decoded_data = base64.b64decode(encoded)
        except Exception as e:
            raise ProcessorError(f"Failed to decode base64 data: {str(e)}")
        
        # Handle output path and extension
        output_path = Path(output_path)
        
        if auto_fix_extension and audio_type:
            correct_extension = f'.{audio_type}'
            if output_path.suffix.lower() != correct_extension:
                output_path = output_path.with_suffix(correct_extension)
        
        # Create parent directories if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the file
        try:
            with open(output_path, 'wb') as f:
                f.write(decoded_data)
        except Exception as e:
            raise ProcessorError(f"Failed to save audio: {str(e)}")
        
        return str(output_path)

