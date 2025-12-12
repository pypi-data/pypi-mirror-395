


"""
Integration tests for the nontext AC module
"""

import pytest
import tempfile
from pathlib import Path
from PIL import Image
import base64
import os

from ..extractors import MediaExtractor
from ..parser import TagParser
from ..processors import ImageProcessor, AudioProcessor


class TestIntegration:
    """Integration tests for the complete nontext module"""
    
    @pytest.fixture
    def test_environment(self, tmp_path):
        """Create a complete test environment with various media files"""
        env = {'root': tmp_path}
        
        # Create image files
        images_dir = tmp_path / "images"
        images_dir.mkdir()
        
        # Small PNG
        small_png = images_dir / "small.png"
        img = Image.new('RGB', (50, 50), color='red')
        img.save(small_png)
        env['small_png'] = small_png
        
        # Large JPEG
        large_jpg = images_dir / "large.jpg"
        img = Image.new('RGB', (500, 500), color='blue')
        img.save(large_jpg)
        env['large_jpg'] = large_jpg
        
        # Create audio files
        audio_dir = tmp_path / "audio"
        audio_dir.mkdir()
        
        # MP3 file
        mp3_file = audio_dir / "sample.mp3"
        mp3_file.write_bytes(b"ID3" + b"\x00" * 1000)  # Fake MP3 header
        env['mp3_file'] = mp3_file
        
        # WAV file
        wav_file = audio_dir / "sample.wav"
        wav_file.write_bytes(b"RIFF" + b"\x00" * 1000)  # Fake WAV header
        env['wav_file'] = wav_file
        
        return env
    
    def test_complete_workflow_images(self, test_environment):
        """Test complete workflow for image extraction and conversion"""
        # Create text with multiple image tags
        text = f"""
        Here is a small image: <_image_>{test_environment['small_png']}</_image_>
        And here is a large one: <img>{test_environment['large_jpg']}</img>
        """
        
        # Initialize extractor
        extractor = MediaExtractor(image_tags=['_image_', 'img'])
        
        # Extract and convert to base64
        images = extractor.extract_images(text, to_base64=True)
        assert len(images) == 2
        
        # Verify both are valid base64
        for img_data in images:
            assert img_data.startswith('data:image/')
            # Extract base64 part
            _, base64_part = img_data.split(',', 1)
            # Verify it decodes properly
            decoded = base64.b64decode(base64_part)
            assert len(decoded) > 0
    
    def test_complete_workflow_audio(self, test_environment):
        """Test complete workflow for audio extraction"""
        text = f"""
        Audio files:
        <_audio_>{test_environment['mp3_file']}</_audio_>
        <audio>{test_environment['wav_file']}</audio>
        """
        
        extractor = MediaExtractor()
        
        # Extract audio files
        audio_files = extractor.extract_audio(text, to_base64=True)
        assert len(audio_files) == 2
        
        # Check MIME types
        assert 'audio/mpeg' in audio_files[0] or 'audio/mp3' in audio_files[0]
        assert 'audio/wav' in audio_files[1] or 'audio/x-wav' in audio_files[1]
    
    def test_mixed_content_extraction(self, test_environment):
        """Test extracting mixed content (text, images, audio)"""
        text = f"""
        Welcome to our media demo!
        
        Here's an image:
        <_image_>{test_environment['small_png']}</_image_>
        
        Listen to this audio:
        <_audio_>{test_environment['mp3_file']}</_audio_>
        
        Another image:
        <img>{test_environment['large_jpg']}</img>
        
        That's all folks!
        """
        
        extractor = MediaExtractor(image_tags=['_image_', 'img'])
        content_list = extractor.to_content_list(text)
        
        # Verify content structure
        types = [list(item.keys())[0] for item in content_list]
        assert types == ['text', 'image', 'text', 'audio', 'text', 'image', 'text']
        
        # Verify media was converted
        assert content_list[1]['image'].startswith('data:image/')
        assert content_list[3]['audio'].startswith('data:audio/')
        assert content_list[5]['image'].startswith('data:image/')
    
    def test_error_recovery(self, test_environment):
        """Test error recovery with mixed valid/invalid paths"""
        text = f"""
        Valid: <_image_>{test_environment['small_png']}</_image_>
        Invalid: <_image_>/does/not/exist.png</_image_>
        Valid: <_audio_>{test_environment['mp3_file']}</_audio_>
        Invalid: <_audio_>/fake/audio.mp3</_audio_>
        """
        
        # Non-strict mode should skip errors
        extractor = MediaExtractor(strict_mode=False)
        
        images = extractor.extract_images(text, to_base64=True)
        assert len(images) == 1  # Only valid image
        
        audio = extractor.extract_audio(text, to_base64=True)
        assert len(audio) == 1  # Only valid audio
    
    def test_tag_format_conversion(self, test_environment):
        """Test converting between different tag formats"""
        # Original text with custom tags
        original = f"""
        [[img:{test_environment['small_png']}]]
        {{audio|{test_environment['mp3_file']}}}
        """
        
        # First convert to standard format
        extractor = MediaExtractor()
        
        # Convert custom image tags
        step1 = original.replace(f"[[img:{test_environment['small_png']}]]", 
                               f"<img>{test_environment['small_png']}</img>")
        step2 = step1.replace(f"{{audio|{test_environment['mp3_file']}}}",
                            f"<audio>{test_environment['mp3_file']}</audio>")
        
        # Now convert to standard underscore format
        converted = extractor.convert_tag_format(step2, "<img>", "<_image_>")
        converted = extractor.convert_tag_format(converted, "<audio>", "<_audio_>", media_type='audio')
        
        # Extract to verify
        images = extractor.extract_images(converted, to_base64=False)
        audio = extractor.extract_audio(converted, to_base64=False)
        
        assert len(images) == 1
        assert len(audio) == 1
        assert str(test_environment['small_png']) in images
        assert str(test_environment['mp3_file']) in audio
    
    def test_round_trip_conversion(self, test_environment):
        """Test loading from file and saving back"""
        # Load image and convert to base64
        processor = ImageProcessor()
        base64_data = processor.load_image_from_path(str(test_environment['small_png']))
        
        # Save to new location
        output_path = test_environment['root'] / "output" / "saved.png"
        saved_path = processor.save_image_from_base64(base64_data, str(output_path))
        
        # Load again and compare
        base64_data2 = processor.load_image_from_path(saved_path)
        
        # Should be identical (minus potential metadata differences)
        assert base64_data == base64_data2
    
    def test_validation_workflow(self, test_environment):
        """Test media path validation workflow"""
        # Create some symlinks and special cases
        symlink_path = test_environment['root'] / "symlink.png"
        if os.name != 'nt':  # Skip on Windows
            symlink_path.symlink_to(test_environment['small_png'])
        
        text = f"""
        Regular file: <_image_>{test_environment['small_png']}</_image_>
        Non-existent: <_image_>/fake/path.png</_image_>
        Already base64: <_image_>data:image/png;base64,iVBORw0KGg==</_image_>
        """
        
        if os.name != 'nt':
            text += f"\nSymlink: <_image_>{symlink_path}</_image_>"
        
        extractor = MediaExtractor()
        validation = extractor.validate_media_paths(text)
        
        assert str(test_environment['small_png']) in validation['valid']
        assert '/fake/path.png' in validation['invalid']
        if os.name != 'nt':
            assert str(symlink_path) in validation['valid']
    
    def test_performance_with_many_tags(self, test_environment):
        """Test performance with many media tags"""
        # Create text with many tags
        parts = ["Start of document"]
        
        for i in range(50):
            if i % 2 == 0:
                parts.append(f"<_image_>{test_environment['small_png']}</_image_>")
            else:
                parts.append(f"<_audio_>{test_environment['mp3_file']}</_audio_>")
            parts.append(f"Text segment {i}")
        
        text = "\n".join(parts)
        
        # Extract all media
        extractor = MediaExtractor()
        images = extractor.extract_images(text, to_base64=False)
        audio = extractor.extract_audio(text, to_base64=False)
        
        assert len(images) == 25
        assert len(audio) == 25
    
    def test_unicode_and_special_characters(self, test_environment):
        """Test handling of unicode and special characters"""
        # Create file with unicode name
        unicode_img = test_environment['root'] / "图片🎨.png"
        img = Image.new('RGB', (10, 10), color='green')
        img.save(unicode_img)
        
        text = f"""
        Unicode path: <_image_>{unicode_img}</_image_>
        Text with émojis 🎉 and spëcial characters
        """
        
        extractor = MediaExtractor()
        images = extractor.extract_images(text, to_base64=True)
        
        assert len(images) == 1
        assert images[0].startswith('data:image/')
    
    def test_nested_directories(self, test_environment):
        """Test handling deeply nested directory structures"""
        # Create deeply nested structure
        deep_dir = test_environment['root']
        for i in range(5):
            deep_dir = deep_dir / f"level{i}"
        deep_dir.mkdir(parents=True)
        
        # Put image in deep directory
        deep_img = deep_dir / "deep.png"
        img = Image.new('RGB', (10, 10), color='yellow')
        img.save(deep_img)
        
        text = f"<_image_>{deep_img}</_image_>"
        
        extractor = MediaExtractor()
        images = extractor.extract_images(text, to_base64=True)
        
        assert len(images) == 1
        assert images[0].startswith('data:image/')
    
    def test_concurrent_processing_simulation(self, test_environment):
        """Test that the module can handle concurrent-like usage"""
        # Create multiple extractors (simulating concurrent usage)
        extractors = [MediaExtractor() for _ in range(3)]
        
        texts = [
            f"<_image_>{test_environment['small_png']}</_image_>",
            f"<_audio_>{test_environment['mp3_file']}</_audio_>",
            f"<img>{test_environment['large_jpg']}</img>"
        ]
        
        results = []
        for extractor, text in zip(extractors, texts):
            if "_image_" in text or "img" in text:
                result = extractor.extract_images(text, to_base64=True)
            else:
                result = extractor.extract_audio(text, to_base64=True)
            results.append(result)
        
        # All should succeed
        assert all(len(r) == 1 for r in results)
        assert results[0][0].startswith('data:image/')
        assert results[1][0].startswith('data:audio/')
        assert results[2][0].startswith('data:image/')



