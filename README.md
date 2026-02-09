# Watermarker
Add diagonal watermarks to your images, just like in Microsoft Word!

## Features
- Diagonal watermark text (auto-scaled based on image size)
- Command-line mode with `--path` and `--text` arguments
- Interactive drag-and-drop mode
- Easy installation with automatic PATH setup (Windows)
- Supports common image formats (JPEG, PNG, etc.)

## Installation

### Windows
1. Clone or download this repository
2. Run `install.cmd` (double-click or run from command prompt)
3. Follow the on-screen instructions
4. Restart your command prompt if you added to PATH

### Linux/macOS
1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Make the script executable (optional):
   ```bash
   chmod +x watermark.py
   ```

## Usage

### Command-Line Mode
Add a watermark by specifying the image path and text:
```bash
watermark --path image.jpg --text "CONFIDENTIAL"
watermark --path photo.png --text "© 2024 My Company"
watermark --path document.jpg --text "DRAFT" --output custom_output.jpg
```

### Interactive Mode
Run without arguments for an interactive experience:
```bash
watermark
```
Then follow the prompts to:
1. Enter or drag-and-drop your image path
2. Enter the watermark text

### Options
- `--path`: Path to the input image file
- `--text`: Text to use as the watermark
- `--output`: (Optional) Custom output path for the watermarked image
- `--help`: Show help message

## Examples

### Example 1: Mark a document as confidential
```bash
watermark --path contract.jpg --text "CONFIDENTIAL"
```

### Example 2: Add copyright to a photo
```bash
watermark --path photo.jpg --text "© 2024 John Doe"
```

### Example 3: Interactive mode
```bash
watermark
> Enter the path to your image: C:\Users\Me\Pictures\photo.jpg
> Enter the watermark text: SAMPLE
```

## How It Works
The watermark is added diagonally across the center of the image, with:
- Automatic text sizing based on image dimensions
- Semi-transparent gray text for subtle but visible watermarking
- 45-degree rotation for the classic diagonal watermark look
- No degradation of original image quality

## Requirements
- Python 3.6 or higher
- Pillow (PIL) library

## License
MIT License - Feel free to use and modify!
