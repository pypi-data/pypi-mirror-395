
"""
Tag Parser Module - Robust regex-based tag parsing with error handling
"""

import re
from typing import List, Dict, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


class ParseError(Exception):
    """Custom exception for parsing errors"""
    def __init__(self, message: str, position: Optional[int] = None):
        self.message = message
        self.position = position
        super().__init__(self.message)


@dataclass
class Tag:
    """Represents a parsed tag with its content"""
    name: str
    content: str
    start_pos: int
    end_pos: int
    attributes: Dict[str, str] = field(default_factory=dict)


class TagParser:
    """
    Robust regex-based tag parser that extracts tagged content from text.
    
    Supports multiple tag formats:
    - <_tag_>content</_tag_>
    - <tag>content</tag>
    - Custom tag patterns
    """
    
    def __init__(self, 
                 tag_pattern: Optional[str] = None,
                 strict_mode: bool = True,
                 max_tag_length: int = 10_000_000):  # 10MB limit for base64 data
        """
        Initialize the parser with optional custom tag pattern.
        
        Args:
            tag_pattern: Custom regex pattern for tags (default supports <_tag_> and <tag>)
            strict_mode: If True, raises exceptions on malformed tags
            max_tag_length: Maximum allowed tag content length (default: 10MB for base64 data)
        """
        self.strict_mode = strict_mode
        self.max_tag_length = max_tag_length
        
        # Default pattern supports both <_tag_> and <tag> formats
        if tag_pattern is None:
            self.tag_pattern = r'<(_?\w+_?)>(.*?)</\1>'
        else:
            self.tag_pattern = tag_pattern
            
        try:
            self.compiled_pattern = re.compile(self.tag_pattern, re.DOTALL)
        except re.error as e:
            raise ParseError(f"Invalid regex pattern: {e}")
    
    def parse(self, text: str) -> List[Tag]:
        """
        Parse all tags from the input text.
        
        Args:
            text: Input text containing tags
            
        Returns:
            List of Tag objects
            
        Raises:
            ParseError: If strict_mode is True and malformed tags are found
        """
        if not text:
            return []
            
        tags = []
        
        try:
            for match in self.compiled_pattern.finditer(text):
                tag_name = match.group(1)
                content = match.group(2)
                
                # Validate tag content length
                if len(content) > self.max_tag_length:
                    error_msg = f"Tag content exceeds maximum length of {self.max_tag_length}"
                    if self.strict_mode:
                        raise ParseError(error_msg, match.start())
                    else:
                        logger.warning(f"{error_msg} at position {match.start()}")
                        continue
                
                tag = Tag(
                    name=tag_name,
                    content=content.strip(),
                    start_pos=match.start(),
                    end_pos=match.end()
                )
                tags.append(tag)
                
        except re.error as e:
            raise ParseError(f"Invalid regex pattern: {str(e)}")
            
        return tags
    
    def extract_by_tag_name(self, text: str, tag_name: str) -> List[str]:
        """
        Extract all content for a specific tag name.
        
        Args:
            text: Input text
            tag_name: Name of the tag to extract
            
        Returns:
            List of content strings for the specified tag
        """
        tags = self.parse(text)
        return [tag.content for tag in tags if tag.name == tag_name]
    
    def replace_tags(self, 
                     text: str, 
                     replacer_func: Callable[[Tag], str],
                     tag_filter: Optional[Callable[[Tag], bool]] = None) -> str:
        """
        Replace tags in text using a custom replacer function.
        
        Args:
            text: Input text
            replacer_func: Function that takes a Tag and returns replacement string
            tag_filter: Optional function to filter which tags to replace
            
        Returns:
            Text with tags replaced
        """
        tags = self.parse(text)
        
        # Sort tags by position in reverse to avoid offset issues
        tags.sort(key=lambda t: t.start_pos, reverse=True)
        
        result = text
        for tag in tags:
            if tag_filter is None or tag_filter(tag):
                replacement = replacer_func(tag)
                result = result[:tag.start_pos] + replacement + result[tag.end_pos:]
                
        return result
    
    def validate_tags(self, text: str) -> Tuple[bool, List[str]]:
        """
        Validate that all tags in the text are properly formed.
        
        Args:
            text: Input text to validate
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check for unclosed tags
        opening_pattern = r'<(_?\w+_?)>'
        closing_pattern = r'</(_?\w+_?)>'
        
        opening_tags = re.findall(opening_pattern, text)
        closing_tags = re.findall(closing_pattern, text)
        
        # Count occurrences
        opening_counts = {}
        closing_counts = {}
        
        for tag in opening_tags:
            opening_counts[tag] = opening_counts.get(tag, 0) + 1
            
        for tag in closing_tags:
            closing_counts[tag] = closing_counts.get(tag, 0) + 1
            
        # Check for mismatches
        all_tags = set(opening_counts.keys()) | set(closing_counts.keys())
        
        for tag in all_tags:
            open_count = opening_counts.get(tag, 0)
            close_count = closing_counts.get(tag, 0)
            
            if open_count != close_count:
                errors.append(f"Tag '{tag}' has {open_count} opening tags but {close_count} closing tags")
                
        # Check for nested tags of the same type (which would break the regex)
        for tag_name in opening_counts:
            pattern = f'<{tag_name}>.*?<{tag_name}>.*?</{tag_name}>.*?</{tag_name}>'
            if re.search(pattern, text, re.DOTALL):
                errors.append(f"Nested tags of type '{tag_name}' detected")
                
        return len(errors) == 0, errors
    
    def extract_with_positions(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract tags with their positions in the original text.
        
        Returns:
            List of dictionaries containing tag info and positions
        """
        tags = self.parse(text)
        return [
            {
                'name': tag.name,
                'content': tag.content,
                'start': tag.start_pos,
                'end': tag.end_pos,
                'full_tag': text[tag.start_pos:tag.end_pos]
            }
            for tag in tags
        ]

