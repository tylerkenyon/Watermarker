#!/usr/bin/env python3
"""
Watermarker - Add diagonal watermarks to images
"""

import argparse
import os
import sys
from PIL import Image, ImageDraw, ImageFont
import math


def add_watermark(image_path, watermark_text, output_path=None):
    """
    Add a diagonal watermark to an image.
    
    Args:
        image_path: Path to the input image
        watermark_text: Text to use as watermark
        output_path: Path for the output image (optional)
    
    Returns:
        Path to the output image
    """
    try:
        # Open the image
        img = Image.open(image_path).convert("RGBA")
        
        # Create a transparent layer for the watermark
        watermark_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark_layer)
        
        # Calculate font size based on image dimensions
        # Aim for watermark text to be about 1/10th of diagonal
        diagonal = math.sqrt(img.width**2 + img.height**2)
        font_size = int(diagonal / 10)
        
        # Try to use a system font, fall back to default if not available
        try:
            # Try common font locations
            font_paths = [
                "C:/Windows/Fonts/arial.ttf",  # Windows
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
                "/System/Library/Fonts/Helvetica.ttc",  # macOS
                "/Library/Fonts/Arial.ttf",  # macOS alternative
            ]
            font = None
            for font_path in font_paths:
                if os.path.exists(font_path):
                    font = ImageFont.truetype(font_path, font_size)
                    break
            
            if font is None:
                # If no system font found, use default
                font = ImageFont.load_default()
                print("Warning: Using default font. Install system fonts for better results.")
        except Exception:
            font = ImageFont.load_default()
            print("Warning: Using default font. Install system fonts for better results.")
        
        # Get text bounding box
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Create a new image for rotated text
        # Make it large enough to fit the rotated text
        max_dim = max(text_width, text_height) * 2
        text_image = Image.new("RGBA", (max_dim, max_dim), (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_image)
        
        # Draw text in the center with semi-transparent gray
        text_x = (max_dim - text_width) // 2
        text_y = (max_dim - text_height) // 2
        text_draw.text((text_x, text_y), watermark_text, 
                      fill=(128, 128, 128, 128), font=font)
        
        # Rotate the text image by 45 degrees (diagonal)
        rotated_text = text_image.rotate(-45, expand=True)
        
        # Calculate position to center the watermark
        x = (img.width - rotated_text.width) // 2
        y = (img.height - rotated_text.height) // 2
        
        # Paste the rotated text onto the watermark layer
        watermark_layer.paste(rotated_text, (x, y), rotated_text)
        
        # Composite the watermark onto the original image
        watermarked = Image.alpha_composite(img, watermark_layer)
        
        # Convert back to RGB if needed
        if watermarked.mode == "RGBA":
            rgb_img = Image.new("RGB", watermarked.size, (255, 255, 255))
            rgb_img.paste(watermarked, mask=watermarked.split()[3])
            watermarked = rgb_img
        
        # Generate output path if not provided
        if output_path is None:
            base_name, ext = os.path.splitext(image_path)
            output_path = f"{base_name}_watermarked{ext}"
        
        # Save the watermarked image
        watermarked.save(output_path)
        print(f"Watermarked image saved to: {output_path}")
        return output_path
        
    except FileNotFoundError:
        print(f"Error: Image file not found: {image_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing image: {e}")
        sys.exit(1)


def interactive_mode():
    """
    Interactive mode for drag-and-drop style usage.
    """
    print("=" * 50)
    print("Watermarker - Interactive Mode")
    print("=" * 50)
    
    # Get image path
    image_path = input("\nEnter the path to your image (or drag and drop): ").strip()
    
    # Remove quotes if user dragged and dropped (Windows adds quotes)
    if image_path.startswith('"') and image_path.endswith('"'):
        image_path = image_path[1:-1]
    if image_path.startswith("'") and image_path.endswith("'"):
        image_path = image_path[1:-1]
    
    # Validate file exists
    if not os.path.exists(image_path):
        print(f"Error: File not found: {image_path}")
        sys.exit(1)
    
    # Get watermark text
    watermark_text = input("\nEnter the watermark text: ").strip()
    
    if not watermark_text:
        print("Error: Watermark text cannot be empty")
        sys.exit(1)
    
    # Add watermark
    print("\nProcessing...")
    add_watermark(image_path, watermark_text)
    print("\nDone!")


def main():
    """Main entry point for the watermarker."""
    parser = argparse.ArgumentParser(
        description="Add diagonal watermarks to images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  watermark --path image.jpg --text "CONFIDENTIAL"
  watermark --path photo.png --text "© 2024 MyCompany"
  watermark  (for interactive mode)
        """
    )
    
    parser.add_argument(
        "--path",
        type=str,
        help="Path to the image file"
    )
    
    parser.add_argument(
        "--text",
        type=str,
        help="Watermark text to add"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        help="Output path for watermarked image (optional)"
    )
    
    args = parser.parse_args()
    
    # If both path and text are provided, use command-line mode
    if args.path and args.text:
        add_watermark(args.path, args.text, args.output)
    # If only one is provided, show error
    elif args.path or args.text:
        print("Error: Both --path and --text are required for command-line mode")
        print("Run 'watermark --help' for usage information")
        print("\nOr run 'watermark' without arguments for interactive mode")
        sys.exit(1)
    # Otherwise, use interactive mode
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
