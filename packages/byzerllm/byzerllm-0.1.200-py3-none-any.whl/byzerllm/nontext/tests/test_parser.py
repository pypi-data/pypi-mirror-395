

"""
Unit tests for the TagParser module
"""

import pytest
from ..parser import TagParser, ParseError, Tag


class TestTagParser:
    """Test cases for TagParser"""
    
    def test_parse_simple_tags(self):
        """Test parsing simple tags"""
        parser = TagParser()
        text = "<_image_>path/to/image.jpg</_image_>"
        
        tags = parser.parse(text)
        assert len(tags) == 1
        assert tags[0].name == "_image_"
        assert tags[0].content == "path/to/image.jpg"
        assert tags[0].start_pos == 0
        assert tags[0].end_pos == len(text)
    
    def test_parse_multiple_tags(self):
        """Test parsing multiple tags"""
        parser = TagParser()
        text = "<_image_>img1.jpg</_image_> Some text <_audio_>audio.mp3</_audio_>"
        
        tags = parser.parse(text)
        assert len(tags) == 2
        assert tags[0].name == "_image_"
        assert tags[0].content == "img1.jpg"
        assert tags[1].name == "_audio_"
        assert tags[1].content == "audio.mp3"
    
    def test_parse_tags_without_underscores(self):
        """Test parsing tags without underscores"""
        parser = TagParser()
        text = "<image>photo.png</image> <audio>sound.wav</audio>"
        
        tags = parser.parse(text)
        assert len(tags) == 2
        assert tags[0].name == "image"
        assert tags[1].name == "audio"
    
    def test_parse_empty_tags(self):
        """Test parsing empty tags"""
        parser = TagParser()
        text = "<_image_></_image_>"
        
        tags = parser.parse(text)
        assert len(tags) == 1
        assert tags[0].content == ""
    
    def test_parse_tags_with_whitespace(self):
        """Test parsing tags with whitespace in content"""
        parser = TagParser()
        text = "<_image_>  path/to/image.jpg  </_image_>"
        
        tags = parser.parse(text)
        assert len(tags) == 1
        assert tags[0].content == "path/to/image.jpg"  # Content is stripped
    
    def test_parse_tags_with_newlines(self):
        """Test parsing tags with newlines"""
        parser = TagParser()
        text = """<_image_>
        path/to/image.jpg
        </_image_>"""
        
        tags = parser.parse(text)
        assert len(tags) == 1
        assert tags[0].content.strip() == "path/to/image.jpg"
    
    def test_extract_by_tag_name(self):
        """Test extracting content by specific tag name"""
        parser = TagParser()
        text = "<_image_>img1.jpg</_image_> <_audio_>audio.mp3</_audio_> <_image_>img2.png</_image_>"
        
        images = parser.extract_by_tag_name(text, "_image_")
        assert len(images) == 2
        assert images[0] == "img1.jpg"
        assert images[1] == "img2.png"
        
        audio = parser.extract_by_tag_name(text, "_audio_")
        assert len(audio) == 1
        assert audio[0] == "audio.mp3"
    
    def test_replace_tags(self):
        """Test replacing tags with custom function"""
        parser = TagParser()
        text = "<_image_>img.jpg</_image_> text <_audio_>audio.mp3</_audio_>"
        
        def replacer(tag):
            if tag.name == "_image_":
                return f"[IMAGE: {tag.content}]"
            return f"[{tag.name.upper()}: {tag.content}]"
        
        result = parser.replace_tags(text, replacer)
        assert result == "[IMAGE: img.jpg] text [_AUDIO_: audio.mp3]"
    
    def test_replace_tags_with_filter(self):
        """Test replacing only specific tags"""
        parser = TagParser()
        text = "<_image_>img.jpg</_image_> <_audio_>audio.mp3</_audio_>"
        
        def replacer(tag):
            return "[REPLACED]"
        
        def filter_func(tag):
            return tag.name == "_image_"
        
        result = parser.replace_tags(text, replacer, filter_func)
        assert "[REPLACED]" in result
        assert "audio.mp3" in result
    
    def test_validate_tags_valid(self):
        """Test tag validation with valid tags"""
        parser = TagParser()
        text = "<_image_>img.jpg</_image_> <_audio_>audio.mp3</_audio_>"
        
        is_valid, errors = parser.validate_tags(text)
        assert is_valid
        assert len(errors) == 0
    
    def test_validate_tags_unclosed(self):
        """Test tag validation with unclosed tags"""
        parser = TagParser()
        text = "<_image_>img.jpg</_image_> <_audio_>audio.mp3"
        
        is_valid, errors = parser.validate_tags(text)
        assert not is_valid
        assert len(errors) > 0
        assert "_audio_" in errors[0]
    
    def test_validate_tags_mismatched(self):
        """Test tag validation with mismatched tags"""
        parser = TagParser()
        text = "<_image_>img.jpg</_audio_>"
        
        is_valid, errors = parser.validate_tags(text)
        assert not is_valid
        assert len(errors) > 0
    
    def test_validate_nested_tags(self):
        """Test validation detects nested tags of same type"""
        parser = TagParser()
        text = "<_image_>outer <_image_>inner</_image_> content</_image_>"
        
        is_valid, errors = parser.validate_tags(text)
        assert not is_valid
        assert any("Nested" in error for error in errors)
    
    def test_extract_with_positions(self):
        """Test extracting tags with position information"""
        parser = TagParser()
        text = "<_image_>img.jpg</_image_> text <_audio_>audio.mp3</_audio_>"
        
        results = parser.extract_with_positions(text)
        assert len(results) == 2
        
        assert results[0]['name'] == "_image_"
        assert results[0]['content'] == "img.jpg"
        assert results[0]['start'] == 0
        assert results[0]['full_tag'] == "<_image_>img.jpg</_image_>"
        
        assert results[1]['name'] == "_audio_"
        assert results[1]['content'] == "audio.mp3"
    
    def test_max_tag_length_strict(self):
        """Test maximum tag length in strict mode"""
        parser = TagParser(strict_mode=True, max_tag_length=10)
        text = "<_image_>this_is_a_very_long_path_that_exceeds_limit.jpg</_image_>"
        
        with pytest.raises(ParseError) as exc_info:
            parser.parse(text)
        assert "exceeds maximum length" in str(exc_info.value)
    
    def test_max_tag_length_non_strict(self):
        """Test maximum tag length in non-strict mode"""
        parser = TagParser(strict_mode=False, max_tag_length=10)
        text = "<_image_>short.jpg</_image_> <_image_>this_is_too_long.jpg</_image_>"
        
        tags = parser.parse(text)
        assert len(tags) == 1  # Only the short one is parsed
        assert tags[0].content == "short.jpg"
    
    def test_custom_tag_pattern(self):
        """Test using custom tag pattern"""
        # Pattern for tags like [[image:content]]
        custom_pattern = r'\[\[(\w+):(.*?)\]\]'
        parser = TagParser(tag_pattern=custom_pattern)
        text = "[[image:photo.jpg]] and [[audio:sound.mp3]]"
        
        tags = parser.parse(text)
        assert len(tags) == 2
        assert tags[0].name == "image"
        assert tags[0].content == "photo.jpg"
        assert tags[1].name == "audio"
        assert tags[1].content == "sound.mp3"
    
    def test_parse_empty_text(self):
        """Test parsing empty text"""
        parser = TagParser()
        tags = parser.parse("")
        assert len(tags) == 0
        
        tags = parser.parse(None)
        assert len(tags) == 0
    
    def test_parse_text_without_tags(self):
        """Test parsing text without any tags"""
        parser = TagParser()
        text = "This is just plain text without any tags"
        
        tags = parser.parse(text)
        assert len(tags) == 0
    
    def test_invalid_regex_pattern(self):
        """Test handling invalid regex pattern"""
        with pytest.raises(ParseError) as exc_info:
            parser = TagParser(tag_pattern=r'[invalid(regex')
        assert "Invalid regex pattern" in str(exc_info.value)


