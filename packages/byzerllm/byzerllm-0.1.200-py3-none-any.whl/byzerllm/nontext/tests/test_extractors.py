

"""
Unit tests for the MediaExtractor module
"""

import pytest
import tempfile
from pathlib import Path
from PIL import Image

from ..extractors import MediaExtractor, extract_image_paths, extract_audio_paths, convert_image_paths_from
from ..processors import ProcessorError


# Module-level fixtures for sharing between test classes
@pytest.fixture
def sample_images(tmp_path):
    """Create sample image files for testing"""
    images = {}
    
    # Create a red image
    img1_path = tmp_path / "red.png"
    img1 = Image.new('RGB', (10, 10), color='red')
    img1.save(img1_path)
    images['red'] = img1_path
    
    # Create a blue image
    img2_path = tmp_path / "blue.jpg"
    img2 = Image.new('RGB', (10, 10), color='blue')
    img2.save(img2_path)
    images['blue'] = img2_path
    
    return images


@pytest.fixture
def sample_audio(tmp_path):
    """Create sample audio files for testing"""
    audio_path = tmp_path / "test.mp3"
    audio_path.write_bytes(b"fake mp3 content" * 100)
    return audio_path


class TestMediaExtractor:
    """Test cases for MediaExtractor"""
    
    def test_extract_images_as_paths(self, sample_images):
        """Test extracting image paths without conversion"""
        extractor = MediaExtractor()
        
        text = f"<_image_>{sample_images['red']}</_image_> and <_image_>{sample_images['blue']}</_image_>"
        
        paths = extractor.extract_images(text, to_base64=False)
        assert len(paths) == 2
        assert str(sample_images['red']) in paths
        assert str(sample_images['blue']) in paths
    
    def test_extract_images_as_base64(self, sample_images):
        """Test extracting images and converting to base64"""
        extractor = MediaExtractor()
        
        text = f"<_image_>{sample_images['red']}</_image_>"
        
        results = extractor.extract_images(text, to_base64=True)
        assert len(results) == 1
        assert results[0].startswith("data:image/png;base64,")
    
    def test_extract_images_with_positions(self, sample_images):
        """Test extracting images with position information"""
        extractor = MediaExtractor()
        
        text = f"Start <_image_>{sample_images['red']}</_image_> middle <_image_>{sample_images['blue']}</_image_> end"
        
        results = extractor.extract_images(text, to_base64=False, return_positions=True)
        assert len(results) == 2
        
        # Check first image
        assert results[0]['content'] == str(sample_images['red'])
        assert results[0]['tag_name'] == '_image_'
        assert 'start' in results[0]
        assert 'end' in results[0]
        
        # Check positions make sense
        assert results[0]['start'] < results[0]['end']
        assert results[1]['start'] > results[0]['end']
    
    def test_extract_images_already_base64(self):
        """Test handling images that are already base64"""
        extractor = MediaExtractor()
        
        base64_data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        text = f"<_image_>{base64_data}</_image_>"
        
        results = extractor.extract_images(text, to_base64=True)
        assert len(results) == 1
        assert results[0] == base64_data  # Should return as-is
    
    def test_extract_images_custom_tags(self, sample_images):
        """Test extracting images with custom tag names"""
        extractor = MediaExtractor(image_tags=['img', 'photo'])
        
        text = f"<img>{sample_images['red']}</img> and <photo>{sample_images['blue']}</photo>"
        
        paths = extractor.extract_images(text, to_base64=False)
        assert len(paths) == 2
    
    def test_extract_images_error_handling(self, tmp_path):
        """Test error handling for invalid image paths"""
        # Test strict mode
        extractor_strict = MediaExtractor(strict_mode=True)
        text = "<_image_>/path/does/not/exist.jpg</_image_>"
        
        with pytest.raises(ProcessorError):
            extractor_strict.extract_images(text, to_base64=True)
        
        # Test non-strict mode (should log error but not raise)
        extractor_lenient = MediaExtractor(strict_mode=False)
        results = extractor_lenient.extract_images(text, to_base64=True)
        assert len(results) == 0  # Invalid path is skipped
    
    def test_extract_audio(self, sample_audio):
        """Test extracting audio files"""
        extractor = MediaExtractor()
        
        text = f"<_audio_>{sample_audio}</_audio_>"
        
        # Test path extraction
        paths = extractor.extract_audio(text, to_base64=False)
        assert len(paths) == 1
        assert paths[0] == str(sample_audio)
        
        # Test base64 conversion
        results = extractor.extract_audio(text, to_base64=True)
        assert len(results) == 1
        assert results[0].startswith("data:audio/mpeg;base64,")
    
    def test_extract_audio_with_positions(self, sample_audio):
        """Test extracting audio with position information"""
        extractor = MediaExtractor()
        
        text = f"Audio here: <_audio_>{sample_audio}</_audio_> done"
        
        results = extractor.extract_audio(text, to_base64=False, return_positions=True)
        assert len(results) == 1
        assert results[0]['content'] == str(sample_audio)
        assert results[0]['tag_name'] == '_audio_'
        assert 'start' in results[0]
        assert 'end' in results[0]
    
    def test_convert_tag_format(self, sample_images):
        """Test converting between tag formats"""
        extractor = MediaExtractor()
        
        # Convert from <img> to <_image_>
        text = f"<img>{sample_images['red']}</img> text <img>{sample_images['blue']}</img>"
        converted = extractor.convert_tag_format(text, "<img>", "<_image_>", media_type='image')
        
        assert "<img>" not in converted
        assert "<_image_>" in converted
        assert str(sample_images['red']) in converted
        assert str(sample_images['blue']) in converted
    
    def test_to_content_list(self, sample_images, sample_audio):
        """Test converting text to content list"""
        extractor = MediaExtractor()
        
        text = f"""
        This is some text.
        <_image_>{sample_images['red']}</_image_>
        More text here.
        <_audio_>{sample_audio}</_audio_>
        Final text.
        """
        
        content_list = extractor.to_content_list(text)
        
        # Should have alternating text and media
        assert len(content_list) == 5
        assert 'text' in content_list[0]
        assert 'image' in content_list[1]
        assert 'text' in content_list[2]
        assert 'audio' in content_list[3]
        assert 'text' in content_list[4]
        
        # Check that image was converted to base64
        assert content_list[1]['image'].startswith('data:image/')
        assert content_list[3]['audio'].startswith('data:audio/')
    
    def test_to_content_list_no_text_between(self, sample_images):
        """Test content list when media tags are adjacent"""
        extractor = MediaExtractor()
        
        text = f"<_image_>{sample_images['red']}</_image_><_image_>{sample_images['blue']}</_image_>"
        
        content_list = extractor.to_content_list(text)
        
        # Should only have images, no text
        assert len(content_list) == 2
        assert 'image' in content_list[0]
        assert 'image' in content_list[1]
    
    def test_remove_media_tags(self, sample_images, sample_audio):
        """Test removing all media tags from text"""
        extractor = MediaExtractor()
        
        text = f"""
        Text before <_image_>{sample_images['red']}</_image_> text middle 
        <_audio_>{sample_audio}</_audio_> text after
        """
        
        cleaned = extractor.remove_media_tags(text)
        
        assert "<_image_>" not in cleaned
        assert "<_audio_>" not in cleaned
        assert str(sample_images['red']) not in cleaned
        assert str(sample_audio) not in cleaned
        assert "Text before" in cleaned
        assert "text middle" in cleaned
        assert "text after" in cleaned
    
    def test_validate_media_paths(self, sample_images, tmp_path):
        """Test validating media file paths"""
        extractor = MediaExtractor()
        
        # Mix of valid and invalid paths
        text = f"""
        <_image_>{sample_images['red']}</_image_>
        <_image_>/invalid/path.jpg</_image_>
        <_image_>data:image/png;base64,abc123</_image_>
        <_audio_>/another/invalid.mp3</_audio_>
        """
        
        validation = extractor.validate_media_paths(text)
        
        assert str(sample_images['red']) in validation['valid']
        assert '/invalid/path.jpg' in validation['invalid']
        assert '/another/invalid.mp3' in validation['invalid']
        # Base64 data should be skipped, not validated
        assert 'data:image/png;base64,abc123' not in validation['valid']
        assert 'data:image/png;base64,abc123' not in validation['invalid']
    
    def test_max_file_size_configuration(self, tmp_path):
        """Test configuring maximum file size"""
        # Create a large file
        large_file = tmp_path / "large.png"
        large_file.write_bytes(b"x" * 1000)
        
        # Extractor with small file size limit
        extractor = MediaExtractor(max_file_size=500)
        
        text = f"<_image_>{large_file}</_image_>"
        
        # Should fail in strict mode
        extractor_strict = MediaExtractor(strict_mode=True, max_file_size=500)
        with pytest.raises(ProcessorError):
            extractor_strict.extract_images(text, to_base64=True)


class TestBackwardCompatibility:
    """Test backward compatibility functions"""
    
    def test_extract_image_paths(self, sample_images):
        """Test backward compatible extract_image_paths function"""
        text = f"<_image_>{sample_images['red']}</_image_>"
        
        # Test without base64 conversion
        paths = extract_image_paths(text, to_base64=False)
        assert len(paths) == 1
        assert paths[0] == str(sample_images['red'])
        
        # Test with base64 conversion
        results = extract_image_paths(text, to_base64=True)
        assert len(results) == 1
        assert results[0].startswith("data:image/")
    
    def test_extract_audio_paths(self, sample_audio):
        """Test backward compatible extract_audio_paths function"""
        text = f"<_audio_>{sample_audio}</_audio_>"
        
        paths = extract_audio_paths(text, to_base64=False)
        assert len(paths) == 1
        assert paths[0] == str(sample_audio)
    
    def test_convert_image_paths_from(self, sample_images):
        """Test backward compatible convert_image_paths_from function"""
        text = f"<img>{sample_images['red']}</img>"
        
        converted = convert_image_paths_from(text, "<img>", "</img>")
        assert "<_image_>" in converted
        assert str(sample_images['red']) in converted


