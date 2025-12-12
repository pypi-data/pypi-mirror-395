from typing import List, Dict, Any, Union, Optional
import pydantic
import base64
import os

# Import from the new modular implementation
from ..nontext import MediaExtractor, TagParser, ImageProcessor, AudioProcessor
from ..nontext.parser import Tag as ModularTag


class Tag(pydantic.BaseModel):
    start_tag: str
    end_tag: str
    content: Union[str, List["Tag"], "Tag"]
    parent: Optional["Tag"] = None


class TagExtractor:
    def __init__(self, text: str):
        self.text = text
        self.pos = -1
        self.len = len(text)
        self.root_tag = Tag(start_tag="<_ROOT_>", end_tag="</_ROOT_>", content=[])
        self.current_tag = None
        self.is_extracted = False

        # Use the new modular parser internally
        self._parser = TagParser()    

    def extract(self) -> Tag:
        if self.is_extracted:
            return self.root_tag
            
        try:
            # Use the new modular parser to parse tags
            parsed_tags = self._parser.parse(self.text)
            
            # Convert the parsed tags back to the old Tag structure
            self._build_tag_tree(parsed_tags)
            
        except Exception:
            # Fallback: if parsing fails, just return root with text content
            self.root_tag.content = self.text
            
        self.is_extracted = True
        return self.root_tag
    
    def _build_tag_tree(self, parsed_tags):
        """Convert modular parser results to old Tag structure"""
        if not parsed_tags:
            self.root_tag.content = self.text
            return
            
        # Sort tags by position
        sorted_tags = sorted(parsed_tags, key=lambda t: t.start_pos)
        
        # Build content list with text and tags
        content_items = []
        last_end = 0
        
        for parsed_tag in sorted_tags:
            # Add text before this tag
            if parsed_tag.start_pos > last_end:
                text_content = self.text[last_end:parsed_tag.start_pos]
                if text_content.strip():
                    content_items.append(text_content)
            
            # Create Tag object for this parsed tag
            tag = Tag(
                start_tag=f"<{parsed_tag.name}>",
                end_tag=f"</{parsed_tag.name}>", 
                content=parsed_tag.content,
                parent=self.root_tag
            )
            content_items.append(tag)
            
            last_end = parsed_tag.end_pos
        
        # Add remaining text
        if last_end < len(self.text):
            remaining_text = self.text[last_end:]
            if remaining_text.strip():
                content_items.append(remaining_text)
        
        # Set the content
        if len(content_items) == 1:
            self.root_tag.content = content_items[0]
        else:
            self.root_tag.content = content_items


class Image(TagExtractor):

    def __init__(self, text: str):
        super().__init__(text)
        self.is_extracted = False
        # Use new modular components
        self._extractor = MediaExtractor()
        self._image_processor = ImageProcessor()

    def has_image(self) -> bool:
        try:
            images = self._extractor.extract_images(self.text, to_base64=False)
            return len(images) > 0
        except:
            # Fallback to original logic
            self.extract()
            for item in self.root_tag.content:
                if (
                    isinstance(item, Tag)
                    and item.start_tag == "<_image_>"
                    and item.end_tag == "</_image_>"
                ):
                    return True
            return False

    @staticmethod
    def convert_image_paths_from(
        text: str, start_tag: str = "<img>", end_tag: str = "</img>"
    ) -> str:
        extractor = MediaExtractor()
        return extractor.convert_tag_format(text, start_tag, "<_image_>", media_type='image')

    @staticmethod
    def extract_image_paths(text: str, to_base64: bool = False) -> List[str]:
        extractor = MediaExtractor()
        # Ensure we get List[str] by setting return_positions=False
        result = extractor.extract_images(text, to_base64=to_base64, return_positions=False)
        # When return_positions=False, result should be List[str]
        return result  # type: ignore

    @staticmethod
    def load_image_from_path(path: str, only_content: bool = False) -> str:
        processor = ImageProcessor()
        result = processor.load_image_from_path(path, as_data_uri=True)
        
        if only_content:
            return result
        return f"<_image_>{result}</_image_>"

    @staticmethod
    def save_image_to_path(
        image_data: str, output_path: str, auto_fix_suffix: bool = False
    ) -> str:
        processor = ImageProcessor()
        return processor.save_image_from_base64(
            image_data, output_path, auto_fix_extension=auto_fix_suffix
        )

    def to_content(self) -> List[Dict[str, str]]:
        try:
            # Use new modular implementation
            return self._extractor.to_content_list(self.text)
        except:
            # Fallback to original logic
            self.extract()

        result = []
        current_item = {}

        for item in self.root_tag.content:
            if isinstance(item, Tag) and item.start_tag == "<_image_>":
                if current_item:
                    result.append(current_item)
                    current_item = {}
                current_item["image"] = item.content

        if current_item:
            result.append(current_item)
            
        new_text = self.text
        for res in result:
            new_text = new_text.replace(f"<_image_>{res['image']}</_image_>", "")

        result.append({"text": new_text.strip()})

        for res in result:
            if "image" in res and not res["image"].startswith("data:image/"):
                # Validate that the content looks like a file path
                image_path = res["image"].strip()
                if self._is_valid_file_path(image_path):
                    try:
                        res["image"] = Image.load_image_from_path(
                            image_path, only_content=True
                        )
                    except Exception:
                        # If loading fails, keep the original path
                        pass

        return result

    def _is_valid_file_path(self, path: str) -> bool:
        """Check if the file path exists"""
        try:
            return os.path.exists(path.strip())
        except:
            return False


class Audio(TagExtractor):
    def __init__(self, text: str):
        super().__init__(text)
        self.is_extracted = False
        # Use new modular components
        self._extractor = MediaExtractor()
        self._audio_processor = AudioProcessor()

    def has_audio(self) -> bool:
        try:
            audio = self._extractor.extract_audio(self.text, to_base64=False)
            return len(audio) > 0
        except:
            # Fallback to original logic
            self.extract()
        for item in self.root_tag.content:
            if (
                isinstance(item, Tag)
                and item.start_tag == "<_audio_>"
                and item.end_tag == "</_audio_>"
            ):
                return True
        return False

    @staticmethod
    def extract_audio_paths(text: str, to_base64: bool = False) -> List[str]:
        extractor = MediaExtractor()
        # Ensure we get List[str] by setting return_positions=False
        result = extractor.extract_audio(text, to_base64=to_base64, return_positions=False)
        # When return_positions=False, result should be List[str]
        return result  # type: ignore

    @staticmethod
    def load_audio_from_path(path: str, only_content: bool = False) -> str:
        processor = AudioProcessor()
        result = processor.load_audio_from_path(path, as_data_uri=True)

        if only_content:
            return result
        return f"<_audio_>{result}</_audio_>"

    @staticmethod
    def save_audio_to_path(
        audio_data: str, output_path: str, auto_fix_suffix: bool = False
    ) -> str:
        processor = AudioProcessor()
        return processor.save_audio_from_base64(
            audio_data, output_path, auto_fix_extension=auto_fix_suffix
        )

    def to_content(self) -> List[Dict[str, str]]:
        try:
            # Use new modular implementation
            return self._extractor.to_content_list(self.text)
        except:
            # Fallback to original logic  
            self.extract()

        result = []
        current_item = {}

        for item in self.root_tag.content:
            if isinstance(item, Tag) and item.start_tag == "<_audio_>":
                if current_item:
                    result.append(current_item)
                    current_item = {}
                current_item["audio"] = item.content

        if current_item:
            result.append(current_item)

        new_text = self.text
        for res in result:
            new_text = new_text.replace(f"<_audio_>{res['audio']}</_audio_>", "")

        if new_text.strip(): 
            result.append({"text": new_text.strip()})

        for res in result:
            if "audio" in res and not res["audio"].startswith("data:audio/"):
                # Validate that the content looks like a file path
                audio_path = res["audio"].strip()
                if self._is_valid_file_path(audio_path):
                    try:
                        res["audio"] = Audio.load_audio_from_path(
                            audio_path, only_content=True
                        )
                    except Exception:
                        # If loading fails, keep the original path
                        pass

        return result

    def _is_valid_file_path(self, path: str) -> bool:
        """Check if the file path exists"""
        try:
            return os.path.exists(path.strip())
        except:
            return False
