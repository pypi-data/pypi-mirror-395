
"""
Media Extractors Module - High-level API for extracting and converting media content
"""

import re
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import logging
import os

from .parser import TagParser, Tag
from .processors import ImageProcessor, AudioProcessor, ProcessorError

logger = logging.getLogger(__name__)


class MediaExtractor:
    """
    High-level extractor for media content from tagged text.
    
    Provides a simple API for extracting images and audio from text,
    converting between formats, and managing media content.
    """
    
    def __init__(self,
                 image_tags: Optional[List[str]] = None,
                 audio_tags: Optional[List[str]] = None,
                 strict_mode: bool = False,
                 max_file_size: Optional[int] = None):
        """
        Initialize the media extractor.
        
        Args:
            image_tags: List of tag names to treat as images (default: ['_image_', '_img_', 'image', 'img'])
            audio_tags: List of tag names to treat as audio (default: ['_audio_', 'audio'])
            strict_mode: Whether to raise exceptions on errors
            max_file_size: Maximum file size for media files
        """
        self.image_tags = image_tags or ['_image_', '_img_', 'image', 'img']
        self.audio_tags = audio_tags or ['_audio_', 'audio']
        self.strict_mode = strict_mode
        
        # Initialize components
        self.parser = TagParser(strict_mode=strict_mode, max_tag_length=10_000_000)  # 10MB for base64 data
        
        if max_file_size:
            self.image_processor = ImageProcessor(max_file_size=max_file_size)
            self.audio_processor = AudioProcessor(max_file_size=max_file_size)
        else:
            self.image_processor = ImageProcessor()
            self.audio_processor = AudioProcessor()
    
    def extract_images(self, 
                      text: str, 
                      to_base64: bool = True,
                      return_positions: bool = False) -> Union[List[str], List[Dict[str, Any]]]:
        """
        Extract all image paths or base64 data from text.
        
        Args:
            text: Input text containing image tags
            to_base64: Convert file paths to base64
            return_positions: Return tag positions along with content
            
        Returns:
            List of image paths/base64 strings, or list of dicts with positions
        """
        tags = self.parser.parse(text)
        results = []
        
        for tag in tags:
            if tag.name in self.image_tags:
                content = tag.content.strip()
                
                # Skip if already base64
                if content.startswith('data:image/'):
                    if return_positions:
                        results.append({
                            'content': content,
                            'start': tag.start_pos,
                            'end': tag.end_pos,
                            'tag_name': tag.name
                        })
                    else:
                        results.append(content)
                    continue
                
                # Convert to base64 if requested
                if to_base64:
                    # Validate that content looks like a file path before processing
                    if not self._is_valid_file_path(content):
                        continue  # Skip invalid paths silently
                        
                    try:
                        base64_data = self.image_processor.load_image_from_path(content)
                        if return_positions:
                            results.append({
                                'content': base64_data,
                                'original_path': content,
                                'start': tag.start_pos,
                                'end': tag.end_pos,
                                'tag_name': tag.name
                            })
                        else:
                            results.append(base64_data)
                    except ProcessorError as e:
                        if self.strict_mode:
                            raise
                        logger.warning(f"Image file not found, skipping: {content} - {str(e)}")
                        continue  # Skip this tag and continue processing others
                else:
                    if return_positions:
                        results.append({
                            'content': content,
                            'start': tag.start_pos,
                            'end': tag.end_pos,
                            'tag_name': tag.name
                        })
                    else:
                        results.append(content)
        
        return results
    
    def extract_audio(self, 
                     text: str, 
                     to_base64: bool = True,
                     return_positions: bool = False) -> Union[List[str], List[Dict[str, Any]]]:
        """
        Extract all audio paths or base64 data from text.
        
        Args:
            text: Input text containing audio tags
            to_base64: Convert file paths to base64
            return_positions: Return tag positions along with content
            
        Returns:
            List of audio paths/base64 strings, or list of dicts with positions
        """
        tags = self.parser.parse(text)
        results = []
        
        for tag in tags:
            if tag.name in self.audio_tags:
                content = tag.content.strip()
                
                # Skip if already base64
                if content.startswith('data:audio/'):
                    if return_positions:
                        results.append({
                            'content': content,
                            'start': tag.start_pos,
                            'end': tag.end_pos,
                            'tag_name': tag.name
                        })
                    else:
                        results.append(content)
                    continue
                
                # Convert to base64 if requested
                if to_base64:
                    # Validate that content looks like a file path before processing
                    if not self._is_valid_file_path(content):
                        continue  # Skip invalid paths silently
                        
                    try:
                        base64_data = self.audio_processor.load_audio_from_path(content)
                        if return_positions:
                            results.append({
                                'content': base64_data,
                                'original_path': content,
                                'start': tag.start_pos,
                                'end': tag.end_pos,
                                'tag_name': tag.name
                            })
                        else:
                            results.append(base64_data)
                    except ProcessorError as e:
                        if self.strict_mode:
                            raise
                        logger.warning(f"Audio file not found, skipping: {content} - {str(e)}")
                        continue  # Skip this tag and continue processing others
                else:
                    if return_positions:
                        results.append({
                            'content': content,
                            'start': tag.start_pos,
                            'end': tag.end_pos,
                            'tag_name': tag.name
                        })
                    else:
                        results.append(content)
        
        return results
    
    def convert_tag_format(self,
                          text: str,
                          from_format: str,
                          to_format: str,
                          media_type: str = 'image') -> str:
        """
        Convert between different tag formats.
        
        Args:
            text: Input text
            from_format: Source tag format (e.g., '<img>')
            to_format: Target tag format (e.g., '<_image_>')
            media_type: Type of media ('image' or 'audio')
            
        Returns:
            Text with converted tags
        """
        # Build regex pattern
        tag_name = from_format.strip('<>')
        pattern = f'<{re.escape(tag_name)}>(.+?)</{re.escape(tag_name)}>'
        
        # Determine target tags
        if media_type == 'image':
            target_tags = self.image_tags
        else:
            target_tags = self.audio_tags
        
        # Use first tag in list as default
        target_tag = to_format.strip('<>') if to_format else target_tags[0]
        
        def replacer(match):
            content = match.group(1).strip()
            return f'<{target_tag}>{content}</{target_tag}>'
        
        return re.sub(pattern, replacer, text, flags=re.DOTALL)
    
    def to_content_list(self, text: str) -> List[Dict[str, str]]:
        """
        Convert text with media tags to a list of content dictionaries.
        
        This method extracts media content and returns a list where each item
        is either {'text': '...'}, {'image': '...'}, or {'audio': '...'}.
        
        Args:
            text: Input text with media tags
            
        Returns:
            List of content dictionaries
        """
        # Extract all media with positions
        images = self.extract_images(text, to_base64=True, return_positions=True)
        audio = self.extract_audio(text, to_base64=True, return_positions=True)
        
        # Combine and sort by position
        all_media = []
        for img in images:
            all_media.append({
                'type': 'image',
                'content': img['content'],
                'start': img['start'],
                'end': img['end']
            })
        
        for aud in audio:
            all_media.append({
                'type': 'audio',
                'content': aud['content'],
                'start': aud['start'],
                'end': aud['end']
            })
        
        # Sort by position
        all_media.sort(key=lambda x: x['start'])
        
        # Build result list
        result = []
        last_pos = 0
        
        for media in all_media:
            # Add text before this media
            text_before = text[last_pos:media['start']].strip()
            if text_before:
                result.append({'text': text_before})
            
            # Add media
            result.append({media['type']: media['content']})
            
            last_pos = media['end']
        
        # Add remaining text
        remaining_text = text[last_pos:].strip()
        if remaining_text:
            result.append({'text': remaining_text})
        
        return result
    
    def remove_media_tags(self, text: str) -> str:
        """
        Remove all media tags from text, leaving only the text content.
        
        Args:
            text: Input text with media tags
            
        Returns:
            Text with all media tags removed
        """
        def remover(tag):
            return ''
        
        # Remove both image and audio tags
        result = self.parser.replace_tags(
            text, 
            remover,
            lambda tag: tag.name in self.image_tags + self.audio_tags
        )
        
        # Clean up extra whitespace
        result = re.sub(r'\s+', ' ', result)
        return result.strip()
    
    def validate_media_paths(self, text: str) -> Dict[str, List[str]]:
        """
        Validate all media file paths in the text.
        
        Returns:
            Dictionary with 'valid' and 'invalid' lists of paths
        """
        valid_paths = []
        invalid_paths = []
        
        # Check images
        image_paths = self.extract_images(text, to_base64=False)
        for path in image_paths:
            if path.startswith('data:'):
                continue
            try:
                self.image_processor.validate_file_path(path)
                valid_paths.append(path)
            except ProcessorError:
                invalid_paths.append(path)
        
        # Check audio
        audio_paths = self.extract_audio(text, to_base64=False)
        for path in audio_paths:
            if path.startswith('data:'):
                continue
            try:
                self.audio_processor.validate_file_path(path)
                valid_paths.append(path)
            except ProcessorError:
                invalid_paths.append(path)
        
        return {
            'valid': valid_paths,
            'invalid': invalid_paths
        }

    def _is_valid_file_path(self, path: str) -> bool:
        """Check if the file path exists"""
        try:
            return os.path.exists(path.strip())
        except:
            return False


# Convenience functions for backward compatibility
def extract_image_paths(text: str, to_base64: bool = False) -> List[str]:
    """Extract image paths from text (backward compatibility)"""
    extractor = MediaExtractor()
    return extractor.extract_images(text, to_base64=to_base64)


def extract_audio_paths(text: str, to_base64: bool = False) -> List[str]:
    """Extract audio paths from text (backward compatibility)"""
    extractor = MediaExtractor()
    return extractor.extract_audio(text, to_base64=to_base64)


def convert_image_paths_from(text: str, 
                           start_tag: str = "<img>", 
                           end_tag: str = "</img>") -> str:
    """Convert custom image tags to standard format (backward compatibility)"""
    extractor = MediaExtractor()
    return extractor.convert_tag_format(text, start_tag, "<_image_>", media_type='image')

