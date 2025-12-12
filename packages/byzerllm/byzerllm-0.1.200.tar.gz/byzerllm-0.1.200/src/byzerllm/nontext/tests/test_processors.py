

"""
Unit tests for the media processors module
"""

import pytest
import base64
import tempfile
import os
from pathlib import Path
from PIL import Image
import io

from ..processors import (
    ImageProcessor, AudioProcessor, ProcessorError, BaseProcessor
)


class TestBaseProcessor:
    """Test cases for BaseProcessor"""
    
    def test_validate_file_path_valid(self, tmp_path):
        """Test validating a valid file path"""
        # Create a test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        processor = BaseProcessor()
        result = processor.validate_file_path(str(test_file))
        
        assert isinstance(result, Path)
        assert result.exists()
    
    def test_validate_file_path_not_exists(self):
        """Test validating non-existent file"""
        processor = BaseProcessor()
        
        with pytest.raises(ProcessorError) as exc_info:
            processor.validate_file_path("/path/that/does/not/exist.txt")
        assert "File not found" in str(exc_info.value)
    
    def test_validate_file_path_is_directory(self, tmp_path):
        """Test validating a directory instead of file"""
        processor = BaseProcessor()
        
        with pytest.raises(ProcessorError) as exc_info:
            processor.validate_file_path(str(tmp_path))
        assert "Path is not a file" in str(exc_info.value)
    
    def test_validate_file_size_limit(self, tmp_path):
        """Test file size validation"""
        # Create a file that's too large
        test_file = tmp_path / "large.txt"
        test_file.write_bytes(b"x" * 1000)
        
        processor = BaseProcessor(max_file_size=500)  # 500 bytes limit
        
        with pytest.raises(ProcessorError) as exc_info:
            processor.validate_file_path(str(test_file))
        assert "exceeds maximum allowed size" in str(exc_info.value)
    
    def test_get_mime_type(self, tmp_path):
        """Test MIME type detection"""
        processor = BaseProcessor()
        
        # Test various file types
        test_cases = [
            ("test.jpg", "image/jpeg"),
            ("test.png", "image/png"),
            ("test.mp3", "audio/mpeg"),
            ("test.txt", "text/plain"),
            ("test.unknown", "application/octet-stream")
        ]
        
        for filename, expected_mime in test_cases:
            test_file = tmp_path / filename
            test_file.write_text("dummy")
            
            mime_type = processor.get_mime_type(test_file)
            assert mime_type == expected_mime
    
    def test_validate_base64_valid(self):
        """Test validating valid base64 strings"""
        processor = BaseProcessor()
        
        # Test plain base64
        valid_b64 = base64.b64encode(b"test data").decode()
        assert processor.validate_base64(valid_b64) is True
        
        # Test data URI
        valid_data_uri = f"data:image/png;base64,{valid_b64}"
        assert processor.validate_base64(valid_data_uri) is True
    
    def test_validate_base64_invalid(self):
        """Test validating invalid base64 strings"""
        processor = BaseProcessor()
        
        # Invalid base64
        assert processor.validate_base64("not valid base64!@#") is False
        
        # Invalid data URI
        assert processor.validate_base64("data:image/png;base64,invalid!") is False
        
        # Malformed data URI
        assert processor.validate_base64("data:image/png") is False


class TestImageProcessor:
    """Test cases for ImageProcessor"""
    
    @pytest.fixture
    def sample_image(self, tmp_path):
        """Create a sample image for testing"""
        img_path = tmp_path / "test_image.png"
        
        # Create a simple 10x10 red image
        img = Image.new('RGB', (10, 10), color='red')
        img.save(img_path)
        
        return img_path
    
    def test_load_image_from_path(self, sample_image):
        """Test loading image and converting to base64"""
        processor = ImageProcessor()
        
        # Test with data URI
        result = processor.load_image_from_path(str(sample_image))
        assert result.startswith("data:image/png;base64,")
        
        # Test without data URI
        result = processor.load_image_from_path(str(sample_image), as_data_uri=False)
        assert not result.startswith("data:")
        # Verify it's valid base64
        base64.b64decode(result)
    
    def test_load_image_validation(self, tmp_path):
        """Test image validation during loading"""
        # Create an invalid image file
        invalid_img = tmp_path / "invalid.png"
        invalid_img.write_bytes(b"not an image")
        
        processor = ImageProcessor()
        
        with pytest.raises(ProcessorError) as exc_info:
            processor.load_image_from_path(str(invalid_img), validate_image=True)
        assert "Invalid image file" in str(exc_info.value)
    
    def test_load_image_unsupported_format_warning(self, tmp_path, caplog):
        """Test warning for unsupported formats"""
        # Create a file with unsupported extension
        weird_file = tmp_path / "image.xyz"
        # Write valid PNG data but with weird extension
        img = Image.new('RGB', (10, 10))
        img.save(weird_file, format='PNG')
        
        processor = ImageProcessor()
        processor.load_image_from_path(str(weird_file), validate_image=False)
        
        assert "Unsupported image format: .xyz" in caplog.text
    
    def test_save_image_from_base64(self, sample_image, tmp_path):
        """Test saving image from base64 data"""
        processor = ImageProcessor()
        
        # Load image as base64
        base64_data = processor.load_image_from_path(str(sample_image))
        
        # Save to new location
        output_path = tmp_path / "output" / "saved_image.png"
        saved_path = processor.save_image_from_base64(base64_data, str(output_path))
        
        assert Path(saved_path).exists()
        assert Path(saved_path).suffix == ".png"
        
        # Verify the saved image is valid
        img = Image.open(saved_path)
        assert img.size == (10, 10)
    
    def test_save_image_auto_fix_extension(self, sample_image, tmp_path):
        """Test automatic extension fixing"""
        processor = ImageProcessor()
        
        # Load PNG image
        base64_data = processor.load_image_from_path(str(sample_image))
        
        # Try to save with wrong extension
        output_path = tmp_path / "image.jpg"
        saved_path = processor.save_image_from_base64(
            base64_data, 
            str(output_path),
            auto_fix_extension=True
        )
        
        # Should be saved as .png
        assert Path(saved_path).suffix == ".png"
    
    def test_save_image_invalid_base64(self, tmp_path):
        """Test saving with invalid base64 data"""
        processor = ImageProcessor()
        
        with pytest.raises(ProcessorError) as exc_info:
            processor.save_image_from_base64(
                "invalid base64 data",
                str(tmp_path / "output.png")
            )
        assert "Invalid base64 image data" in str(exc_info.value)
    
    def test_get_image_info(self, sample_image):
        """Test getting image information"""
        processor = ImageProcessor()
        
        info = processor.get_image_info(str(sample_image))
        
        assert info['path'] == str(sample_image)
        assert info['size'] > 0
        assert info['mime_type'] == 'image/png'
        assert info['format'] == 'PNG'
        assert info['width'] == 10
        assert info['height'] == 10
        assert 'mode' in info
    
    def test_supported_formats(self):
        """Test supported image formats"""
        processor = ImageProcessor()
        
        expected_formats = {
            '.jpg', '.jpeg', '.png', '.gif', '.bmp',
            '.webp', '.ico', '.tiff', '.svg'
        }
        
        assert processor.supported_formats == expected_formats


class TestAudioProcessor:
    """Test cases for AudioProcessor"""
    
    @pytest.fixture
    def sample_audio(self, tmp_path):
        """Create a sample audio file for testing"""
        # Create a dummy audio file (just bytes, not real audio)
        audio_path = tmp_path / "test_audio.mp3"
        audio_path.write_bytes(b"dummy audio content" * 100)
        return audio_path
    
    def test_load_audio_from_path(self, sample_audio):
        """Test loading audio and converting to base64"""
        processor = AudioProcessor()
        
        # Test with data URI
        result = processor.load_audio_from_path(str(sample_audio))
        assert result.startswith("data:audio/mpeg;base64,")
        
        # Test without data URI
        result = processor.load_audio_from_path(str(sample_audio), as_data_uri=False)
        assert not result.startswith("data:")
        # Verify it's valid base64
        base64.b64decode(result)
    
    def test_save_audio_from_base64(self, sample_audio, tmp_path):
        """Test saving audio from base64 data"""
        processor = AudioProcessor()
        
        # Load audio as base64
        base64_data = processor.load_audio_from_path(str(sample_audio))
        
        # Save to new location
        output_path = tmp_path / "output" / "saved_audio.mp3"
        saved_path = processor.save_audio_from_base64(base64_data, str(output_path))
        
        assert Path(saved_path).exists()
        # mimetypes might return .mpeg for mp3 files
        assert Path(saved_path).suffix in [".mp3", ".mpeg"]
        
        # Verify content matches
        with open(sample_audio, 'rb') as f1, open(saved_path, 'rb') as f2:
            assert f1.read() == f2.read()
    
    def test_audio_max_file_size(self):
        """Test audio processor has larger default file size limit"""
        processor = AudioProcessor()
        assert processor.max_file_size == 50 * 1024 * 1024  # 50MB
    
    def test_supported_audio_formats(self):
        """Test supported audio formats"""
        processor = AudioProcessor()
        
        expected_formats = {
            '.mp3', '.wav', '.ogg', '.m4a', '.flac',
            '.aac', '.wma', '.opus', '.webm'
        }
        
        assert processor.supported_formats == expected_formats
    
    def test_audio_mime_type_fallback(self, tmp_path):
        """Test MIME type fallback for audio files"""
        # Create audio file with uncommon extension
        audio_file = tmp_path / "audio.m4a"
        audio_file.write_bytes(b"dummy m4a content")
        
        processor = AudioProcessor()
        result = processor.load_audio_from_path(str(audio_file))
        
        # Should have correct MIME type
        assert "data:audio/" in result


