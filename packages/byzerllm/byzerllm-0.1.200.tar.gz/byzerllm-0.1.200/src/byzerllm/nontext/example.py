
#!/usr/bin/env python3
"""
Example usage of the nontext AC module
"""

from pathlib import Path
from byzerllm.nontext import MediaExtractor, TagParser, ImageProcessor, AudioProcessor


def example_basic_extraction():
    """Basic example of extracting images and audio"""
    print("=== Basic Extraction Example ===")
    
    # Sample text with media tags
    text = """
    Welcome to our demo!
    
    Here's our logo:
    <_image_>logo.png</_image_>
    
    And here's some background music:
    <_audio_>background.mp3</_audio_>
    
    Enjoy!
    """
    
    extractor = MediaExtractor()
    
    # Extract images (paths only)
    image_paths = extractor.extract_images(text, to_base64=False)
    print(f"Found {len(image_paths)} images: {image_paths}")
    
    # Extract audio (paths only)
    audio_paths = extractor.extract_audio(text, to_base64=False)
    print(f"Found {len(audio_paths)} audio files: {audio_paths}")
    print()


def example_base64_conversion():
    """Example of converting media to base64"""
    print("=== Base64 Conversion Example ===")
    
    # Create a sample image for testing
    from PIL import Image
    import tempfile
    
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
        img = Image.new('RGB', (100, 100), color='blue')
        img.save(tmp.name)
        tmp_path = tmp.name
    
    text = f"<_image_>{tmp_path}</_image_>"
    
    extractor = MediaExtractor()
    base64_images = extractor.extract_images(text, to_base64=True)
    
    if base64_images:
        print(f"Converted image to base64:")
        print(f"Data URI preview: {base64_images[0][:50]}...")
    
    # Clean up
    Path(tmp_path).unlink()
    print()


def example_custom_tags():
    """Example using custom tag formats"""
    print("=== Custom Tags Example ===")
    
    # Text with custom tags
    text = """
    Custom format examples:
    <img>photo1.jpg</img>
    <photo>photo2.png</photo>
    <sound>audio1.mp3</sound>
    """
    
    # Configure extractor with custom tags
    extractor = MediaExtractor(
        image_tags=['img', 'photo'],
        audio_tags=['sound']
    )
    
    images = extractor.extract_images(text, to_base64=False)
    audio = extractor.extract_audio(text, to_base64=False)
    
    print(f"Images found: {images}")
    print(f"Audio found: {audio}")
    print()


def example_content_list():
    """Example of converting to content list"""
    print("=== Content List Example ===")
    
    text = """
    Chapter 1: Introduction
    
    <_image_>chapter1.jpg</_image_>
    
    Welcome to our tutorial. Let's start with a demo:
    
    <_audio_>demo.mp3</_audio_>
    
    That's all for now!
    """
    
    extractor = MediaExtractor()
    content_list = extractor.to_content_list(text)
    
    print("Content structure:")
    for i, item in enumerate(content_list):
        content_type = list(item.keys())[0]
        content_preview = str(item[content_type])[:50]
        if len(str(item[content_type])) > 50:
            content_preview += "..."
        print(f"  [{i}] {content_type}: {content_preview}")
    print()


def example_validation():
    """Example of validating media paths"""
    print("=== Validation Example ===")
    
    text = """
    Valid file: <_image_>real_file.jpg</_image_>
    Invalid file: <_image_>/does/not/exist.png</_image_>
    Base64 data: <_image_>data:image/png;base64,iVBORw0KGg==</_image_>
    """
    
    extractor = MediaExtractor()
    validation = extractor.validate_media_paths(text)
    
    print(f"Valid paths: {validation['valid']}")
    print(f"Invalid paths: {validation['invalid']}")
    print()


def example_error_handling():
    """Example of error handling modes"""
    print("=== Error Handling Example ===")
    
    text = """
    <_image_>valid.jpg</_image_>
    <_image_>/invalid/path.jpg</_image_>
    <_image_>another_valid.png</_image_>
    """
    
    # Lenient mode (default) - skips errors
    extractor_lenient = MediaExtractor(strict_mode=False)
    results_lenient = extractor_lenient.extract_images(text, to_base64=False)
    print(f"Lenient mode found: {len(results_lenient)} valid images")
    
    # Strict mode - raises on first error
    extractor_strict = MediaExtractor(strict_mode=True)
    try:
        results_strict = extractor_strict.extract_images(text, to_base64=False)
    except Exception as e:
        print(f"Strict mode raised error: {type(e).__name__}: {e}")
    print()


def example_tag_parser():
    """Example of using TagParser directly"""
    print("=== Tag Parser Example ===")
    
    parser = TagParser()
    text = "<_image_>img1.jpg</_image_> text <_audio_>sound.mp3</_audio_>"
    
    tags = parser.parse(text)
    print(f"Found {len(tags)} tags:")
    for tag in tags:
        print(f"  - {tag.name}: {tag.content} (pos: {tag.start_pos}-{tag.end_pos})")
    
    # Validate tags
    validation_result = parser.validate_tags(text)
    print(f"Tags valid: {validation_result['valid']}")
    print()


if __name__ == "__main__":
    print("Nontext AC Module Examples\n")
    
    example_basic_extraction()
    example_base64_conversion()
    example_custom_tags()
    example_content_list()
    example_validation()
    example_error_handling()
    example_tag_parser()
    
    print("Examples completed!")
