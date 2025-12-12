#!/usr/bin/env python3
"""
General Conversion Module - Convertable Formats: JPEG, PNG, BMP, TIFF, ICO, WEBP, HEIC/HEIF, AVIF
"""

from pathlib import Path
from typing import Optional, List, Dict, Tuple, Iterable, Union
import gc
import io

from PIL import Image, UnidentifiedImageError

# --- Optional: Register HEIF/AVIF Decoders/Encoders if Available ---
_HEIF_AVAILABLE = False
try:
    import pillow_heif  # type: ignore
    # Register Encoders so Pillow can open .heic/.heif/.avif files
    pillow_heif.register_heif_opener()
    try:
        pillow_heif.register_avif_opener()
    except Exception:
        # Older Versions Only Need/Register_heif_opener; AVIF May Already be Covered
        pass
    _HEIF_AVAILABLE = True
except Exception:
    _HEIF_AVAILABLE = False

# --- SVG Support (using PyMuPDF - no system dependencies required) ---
_PYMUPDF_AVAILABLE = False
try:
    import fitz  # PyMuPDF
    _PYMUPDF_AVAILABLE = True
except Exception:
    _PYMUPDF_AVAILABLE = False


SUPPORTED_OUT_FORMATS = {
    "JPEG": (".jpg", ".jpeg"),
    "PNG": (".png",),
    "BMP": (".bmp",),
    "TIFF": (".tif", ".tiff"),
    "ICO": (".ico",),
    "WEBP": (".webp",),
    "HEIF": (".heif", ".heic"),   # via pillow-heif
    "AVIF": (".avif",),           # via pillow-heif
}

# SVG is Input-only Format (can be converted to other formats)
SUPPORTED_INPUT_FORMATS = {
    "SVG": (".svg",),  # via PyMuPDF (no system dependencies)
}

# Map Common Aliases to Pillow's Format Names
FORMAT_ALIASES = {
    "JPG": "JPEG",
    "JPEG": "JPEG",
    "PNG": "PNG",
    "BMP": "BMP",
    "TIF": "TIFF",
    "TIFF": "TIFF",
    "ICO": "ICO",
    "WEBP": "WEBP",
    "HEIC": "HEIF",
    "HEIF": "HEIF",
    "AVIF": "AVIF",
}

DEFAULT_ICO_SIZES = (16, 20, 24, 32, 40, 48, 64, 72, 80, 96, 128, 160, 192, 256, 320, 384, 512)


def normalize_format(fmt: str) -> str:
    key = fmt.strip().upper()
    if key not in FORMAT_ALIASES:
        raise ValueError(f"Unknown/unsupported format: {fmt}")
    norm = FORMAT_ALIASES[key]
    # Guard HEIF/AVIF if Plugin Missing
    if norm in {"HEIF", "AVIF"} and not _HEIF_AVAILABLE:
        raise RuntimeError(
            f"{norm} support requires 'pillow-heif'. Install with: pip install pillow-heif"
        )
    return norm


def ensure_rgb_without_alpha(img: Image.Image, background=(255, 255, 255)) -> Image.Image:
    """JPEG does not support alpha; flatten transparent or LA/P modes."""
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        # Convert with Alpha Compositing onto Background
        bg = Image.new("RGB", img.size, background)
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        bg.paste(img, mask=img.getchannel("A"))
        return bg
    elif img.mode in ("P", "L"):
        return img.convert("RGB")
    elif img.mode == "CMYK":
        return img.convert("RGB")
    return img


def build_ico_images(img: Image.Image, sizes: Iterable[int] = None) -> List[Image.Image]:
    """Create resized copies for ICO multi-resolution icon.

    Args:
        img: Source image
        sizes: Icon sizes to generate. If None, uses original size or smart defaults.
    """
    images = []
    src = img
    # Prefer RGBA for Icons to Keep Transparency
    if src.mode not in ("RGBA", "RGB"):
        try:
            src = src.convert("RGBA")
        except Exception:
            src = src.convert("RGB")

    # 如果没有指定尺寸,使用智能默认值
    if sizes is None or not sizes:
        original_width = src.width
        original_height = src.height

        # 如果原图是正方形且尺寸合适,使用原始尺寸
        if original_width == original_height:
            # 检查是否是常见的ICO尺寸
            common_sizes = [16, 20, 24, 32, 40, 48, 64, 72, 80, 96, 128, 160, 192, 256, 320, 384, 512]
            if original_width in common_sizes:
                # 使用原图尺寸和一些常见的其他尺寸
                sizes = [s for s in [original_width, 256, 128, 64, 48, 32, 16] if s <= original_width]
                # 去重并排序
                sizes = sorted(list(set(sizes)), reverse=True)
            else:
                # 原图尺寸不是标准尺寸,找到最接近的标准尺寸
                sizes = [s for s in common_sizes if s <= min(original_width, 512)]
                if not sizes:
                    sizes = [16]  # 至少包含16x16
                sizes = sorted(sizes, reverse=True)[:6]  # 最多6个尺寸
        else:
            # 原图不是正方形,使用较小边的尺寸作为参考
            min_dimension = min(original_width, original_height)
            # 选择不超过最小尺寸的标准尺寸
            common_sizes = [16, 20, 24, 32, 40, 48, 64, 72, 80, 96, 128, 160, 192, 256, 320, 384, 512]
            sizes = [s for s in common_sizes if s <= min(min_dimension, 256)]
            if not sizes:
                sizes = [16]  # 至少包含16x16
            sizes = sorted(sizes, reverse=True)[:6]  # 最多6个尺寸

    for s in sizes:
        if src.size == (s, s):
            images.append(src.copy())
        else:
            # 如果原图不是正方形,需要先裁剪或调整
            if src.width != src.height:
                # 创建正方形画布,保持宽高比居中放置
                square = Image.new(src.mode, (s, s), (255, 255, 255, 0) if src.mode == "RGBA" else (255, 255, 255))
                # 计算缩放比例,保持宽高比
                ratio = min(s / src.width, s / src.height)
                new_width = int(src.width * ratio)
                new_height = int(src.height * ratio)
                resized = src.resize((new_width, new_height), Image.LANCZOS)
                # 居中放置
                x = (s - new_width) // 2
                y = (s - new_height) // 2
                if src.mode == "RGBA" or "transparency" in src.info:
                    square.paste(resized, (x, y), resized)
                else:
                    square.paste(resized, (x, y))
                images.append(square)
            else:
                images.append(src.resize((s, s), Image.LANCZOS))
    return images


def save_image(
    img: Image.Image,
    out_path: Path,
    out_fmt: str,
    *,
    quality: Optional[int],
    optimize: bool,
    progressive: bool,
    background_for_jpeg: Tuple[int, int, int],
    ico_sizes: Tuple[int, ...] = None,
    extra_save_kwargs: Optional[Dict] = None,
) -> None:
    exif = img.info.get("exif")
    save_kwargs = dict(extra_save_kwargs or {})

    if out_fmt == "JPEG":
        img = ensure_rgb_without_alpha(img, background=background_for_jpeg)
        if quality is not None:
            save_kwargs["quality"] = quality
        save_kwargs["optimize"] = optimize
        save_kwargs["progressive"] = progressive
        if exif:
            save_kwargs["exif"] = exif
        img.save(out_path, format="JPEG", **save_kwargs)

    elif out_fmt == "PNG":
        # Keep Alpha if Present
        if img.mode == "P" and "transparency" not in img.info:
            img = img.convert("RGBA")  # Safer Default
        save_kwargs["optimize"] = optimize
        img.save(out_path, format="PNG", **save_kwargs)

    elif out_fmt == "BMP":
        # BMP Doesn't Support Alpha; Drop It
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGB")
        img.save(out_path, format="BMP", **save_kwargs)

    elif out_fmt == "TIFF":
        # Preserve Exif if Present
        if exif:
            save_kwargs["exif"] = exif
        # Default to Lossless Compression
        save_kwargs.setdefault("compression", "tiff_lzw")
        img.save(out_path, format="TIFF", **save_kwargs)

    elif out_fmt == "WEBP":
        # WebP Supports Alpha + Lossy/Lossless
        if quality is not None:
            save_kwargs["quality"] = quality
        # Supports Lossless Mode via Extra_save_kwargs
        img.save(out_path, format="WEBP", **save_kwargs)

    elif out_fmt == "ICO":
        # Build Multi-res Icon
        images = build_ico_images(img, ico_sizes)
        # Pillow Expects "sizes" kw OR a List via "append_images" (for .ico it's "sizes")
        save_kwargs["sizes"] = [(im.width, im.height) for im in images]
        # Save Using the Largest as Base; Pillow Constructs ICO from it.
        images[0].save(out_path, format="ICO", **save_kwargs)

    elif out_fmt in {"HEIF", "AVIF"}:
        # Pillow-heif Handles Both; Quality Applies
        if quality is not None:
            save_kwargs["quality"] = quality
        # Advanced Options Available via Extra_save_kwargs
        img.save(out_path, format=out_fmt, **save_kwargs)

    else:
        raise ValueError(f"Unsupported output format: {out_fmt}")


def generate_unique_filename(base_path: Path) -> Path:
    """
    Generate a unique filename by adding sequential numbers if file already exists.

    Args:
        base_path (Path): Base path with target extension

    Returns:
        Path: Unique filename that doesn't exist
    """
    if not base_path.exists():
        return base_path

    # Get Base Name and Extension
    base_name = base_path.stem
    extension = base_path.suffix

    # Try Sequential Numbers: 01, 02, 03, etc.
    counter = 1
    while True:
        new_name = f"{base_name} {counter:02d}{extension}"
        new_path = base_path.parent / new_name
        if not new_path.exists():
            return new_path
        counter += 1


def get_format_from_extension(extension: str) -> Optional[str]:
    """
    Get format name from file extension using the global SUPPORTED_OUT_FORMATS and SUPPORTED_INPUT_FORMATS.

    Args:
        extension (str): File extension (e.g., '.jpg', '.png', '.svg')

    Returns:
        Optional[str]: Format name or None if not found
    """
    extension = extension.lower()
    # Check output formats first
    for format_name, extensions in SUPPORTED_OUT_FORMATS.items():
        if extension in extensions:
            return format_name
    # Check input-only formats (like SVG)
    for format_name, extensions in SUPPORTED_INPUT_FORMATS.items():
        if extension in extensions:
            return format_name
    return None


def convert_svg_to_image(svg_path: Path, target_format: str, dpi: int = 300, backend: str = "auto") -> Image.Image:
    """
    Convert SVG file to PIL Image using PyMuPDF (no system dependencies required).

    Args:
        svg_path: Path to SVG file
        target_format: Target format (not used, kept for compatibility)
        dpi: DPI for rendering (default 300)
        backend: Backend to use (not used, kept for compatibility)

    Returns:
        PIL Image object
    """
    if not _PYMUPDF_AVAILABLE:
        raise RuntimeError(
            "SVG conversion requires 'pymupdf'. Install with: pip install pymupdf"
        )
    try:
        # Open SVG with PyMuPDF
        doc = fitz.open(str(svg_path))
        if len(doc) == 0:
            raise RuntimeError(f"SVG file has no pages: {svg_path}")

        # Get first page and render to pixmap
        page = doc[0]
        pix = page.get_pixmap(dpi=dpi)

        # Convert to PNG bytes and then to PIL Image
        png_bytes = pix.tobytes('png')
        img = Image.open(io.BytesIO(png_bytes))
        img.load()

        # Clean up
        doc.close()

        return img
    except Exception as e:
        raise RuntimeError(f"Failed to convert SVG to image: {e}")


def generate_unique_folder_name(base_folder: Path, folder_name: str) -> Path:
    """
    Generate a unique folder name by adding sequential numbers if folder already exists.

    Args:
        base_folder (Path): Base directory where folder will be created
        folder_name (str): Base folder name

    Returns:
        Path: Unique folder path that doesn't exist
    """
    folder_path = base_folder / folder_name
    if not folder_path.exists():
        return folder_path

    # Try Sequential Numbers: 01, 02, 03, etc.
    counter = 1
    while True:
        new_folder_name = f"{folder_name} {counter:02d}"
        new_folder_path = base_folder / new_folder_name
        if not new_folder_path.exists():
            return new_folder_path
        counter += 1


def auto_convert_folder(
    input_files: Union[str, List[str]],
    target_format: str,
    **kwargs
) -> Dict[str, List[str]]:
    """
    Convert images to the specified format. Supports both folder path and file list.

    Args:
        input_files (str or List[str]): Path to folder containing images OR list of image file paths
        target_format (str): Target format (jpeg, png, webp, heic, avif, bmp, tiff, ico)
        **kwargs: Additional conversion options (quality, optimize, etc.)

    Returns:
        Dict[str, List[str]]: {"converted": [list of converted files], "skipped": [list of skipped files]}

    Raises:
        ValueError: If input is invalid or format is unsupported
        RuntimeError: If no images are found or conversion fails
    """
    # Validate Target Format
    try:
        normalized_target = normalize_format(target_format)
    except Exception as e:
        raise ValueError(f"Unsupported target format '{target_format}': {e}")

    # Handle two modes: folder path or file list
    if isinstance(input_files, list):
        # Mode 1: List of file paths
        image_files = []
        already_target_format = []

        # Validate all files exist
        for file_path_str in input_files:
            file_path = Path(file_path_str)
            if not file_path.exists():
                raise ValueError(f"Input file does not exist: {file_path_str}")
            if not file_path.is_file():
                raise ValueError(f"Input path is not a file: {file_path_str}")

            # Check if file is already in target format
            if file_path.suffix.lower() in [ext.lower() for ext in SUPPORTED_OUT_FORMATS[normalized_target]]:
                already_target_format.append(str(file_path))
                continue

            image_files.append(file_path)

        # Use first file's directory as output location
        if image_files:
            base_output_dir = image_files[0].parent
        elif already_target_format:
            base_output_dir = Path(already_target_format[0]).parent
        else:
            raise ValueError("No valid image files provided")

        # Create Output Folder with Smart Naming
        base_folder_name = "Converted Images"
        output_folder = generate_unique_folder_name(base_output_dir, base_folder_name)
        output_folder.mkdir(parents=True, exist_ok=True)

        print(f"PROCESSING: Converting {len(image_files)} images from file list to {normalized_target}")

    else:
        # Mode 2: Folder path (original behavior)
        input_path = Path(input_files)
        if not input_path.exists():
            raise ValueError(f"Input folder does not exist: {input_files}")
        if not input_path.is_dir():
            raise ValueError(f"Input path is not a directory: {input_files}")

        # Create Output Folder with Smart Naming
        base_folder_name = "Converted Images"
        output_folder = generate_unique_folder_name(input_path, base_folder_name)
        output_folder.mkdir(parents=True, exist_ok=True)

        # Get Supported Image Extensions (including SVG)
        supported_extensions = set()
        for format_exts in SUPPORTED_OUT_FORMATS.values():
            supported_extensions.update(ext.lower() for ext in format_exts)
        for format_exts in SUPPORTED_INPUT_FORMATS.values():
            supported_extensions.update(ext.lower() for ext in format_exts)

        # Find All Image Files in the Folder
        image_files = []
        already_target_format = []

        for file_path in input_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                # Check if File is Already in Target Format
                if file_path.suffix.lower() in [ext.lower() for ext in SUPPORTED_OUT_FORMATS[normalized_target]]:
                    already_target_format.append(str(file_path))
                    continue
                image_files.append(file_path)

        print(f"PROCESSING: Found {len(image_files)} images to convert to {normalized_target}")

    # Common validation
    if not image_files:
        print(f"INFO: No images need conversion - all files are already {normalized_target}")
        return {
            "converted": [],
            "skipped": already_target_format if 'already_target_format' in locals() else [],
            "output_folder": str(output_folder)
        }

    if already_target_format:
        print(f"SKIPPING: {len(already_target_format)} files already in {normalized_target} format")
    print(f"OUTPUT: Output folder: {output_folder.name}")

    # Convert Images
    converted_files = []
    failed_files = []

    for image_file in image_files:
        try:
            # Convert the Image Directly - Auto_convert_image Handles Unique Naming
            result = auto_convert_image(
                str(image_file),
                target_format,
                str(output_folder),
                **kwargs
            )

            if result:
                converted_files.append(result)

        except Exception as e:
            print(f"(WARNING) Failed to convert {image_file.name}: {e}")
            failed_files.append(str(image_file))

    # Summary Report
    print(f"\nSUCCESS: Conversion completed!")
    print(f"SUMMARY: Converted: {len(converted_files)} images")
    if failed_files:
        print(f"ERROR: Failed: {len(failed_files)} images")
    if already_target_format:
        print(f"SKIPPED: Skipped (already {normalized_target}): {len(already_target_format)} files")
    print(f"OUTPUT: Output location: {output_folder}")

    return {
        "converted": converted_files,
        "failed": failed_files,
        "skipped_already_target": already_target_format if 'already_target_format' in locals() else [],
        "output_folder": str(output_folder)
    }


def auto_convert_image(file_name, target_format: str, output_dir: str, **kwargs):
    """
    Auto-convert image file(s) to the specified format.

    Args:
        file_name (str or List[str]): Path(s) to the input image file(s)
        target_format (str): Target format (jpeg, png, webp, heic, avif, bmp, tiff, ico)
        output_dir (str): Output directory path
        **kwargs: Additional conversion options (quality, optimize, etc.)

    Returns:
        str or List[str]: Path(s) to the converted image file(s)

    Raises:
        ValueError: If input file doesn't exist or format is unsupported
        RuntimeError: If conversion fails
    """
    # Handle both single file and list of files
    if isinstance(file_name, str):
        file_names = [file_name]
        single_file = True
    else:
        file_names = file_name
        single_file = False

    # Validate Target Format
    try:
        normalized_target = normalize_format(target_format)
        print(f"OK: Target format: {normalized_target}")
    except Exception as e:
        raise ValueError(f"Unsupported target format '{target_format}': {e}")

    # Create Output Directory if it Doesn't Exist
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    converted_files = []

    for file_path_str in file_names:
        # Validate Input File
        input_path = Path(file_path_str)
        if not input_path.exists():
            raise ValueError(f"Input file does not exist: {file_path_str}")
        if not input_path.is_file():
            raise ValueError(f"Input path is not a file: {input_path}")

        # Auto-detect Input Format from File Extension
        input_extension = input_path.suffix.lower()
        input_format = get_format_from_extension(input_extension)

        if input_format:
            print(f"OK: Auto-detected input format: {input_format} for {input_path.name}")
        else:
            print(f"(WARNING) Unknown input format: {input_extension} for {input_path.name}")

        # Check if Input Format Matches Target Format (Skip Unnecessary Conversion)
        if input_format and input_format == normalized_target:
            print(f"INFO: File {input_path.name} is already in {normalized_target} format - no conversion needed")
            converted_files.append(str(input_path))  # Return Original File Path
            continue

        # Use Input Filename (Without Extension) as Base Name
        base_name = input_path.stem

        # Get the Appropriate Extension for the Target Format
        user_format_upper = target_format.strip().upper()
        if user_format_upper == "JPEG" and normalized_target == "JPEG":
            target_ext = ".jpeg"  # Use .jpeg when user explicitly requests JPEG
        elif user_format_upper == "JPG" and normalized_target == "JPEG":
            target_ext = ".jpg"   # Use .jpg when user requests JPG
        else:
            target_ext = SUPPORTED_OUT_FORMATS[normalized_target][0]

        # Create the Base Output Path
        base_output_path = output_dir_path / f"{base_name}{target_ext}"

        # Generate Unique Filename to Avoid Overwriting
        final_output_path = generate_unique_filename(base_output_path)
        if final_output_path != base_output_path:
            print(f"INFO: File exists, generating unique name: {final_output_path.name}")

        print(f"OUTPUT: Output filename: {final_output_path.name}")

        # Set Default Conversion Options
        conversion_options = {
            'overwrite': kwargs.get('overwrite', False),
            'quality': kwargs.get('quality', None),
            'optimize': kwargs.get('optimize', True),
            'progressive': kwargs.get('progressive', True),
            'background_for_jpeg': kwargs.get('jpeg_bg', (255, 255, 255)),
            'ico_sizes': kwargs.get('ico_sizes', None),
            'extra_save_kwargs': kwargs.get('extra_save_kwargs', {})
        }

        print(f"PROCESSING: Converting {input_path.name} ({input_format or 'unknown'}) → {normalized_target}")

        # Perform Conversion
        try:
            # Check if input is SVG
            if input_format == "SVG":
                # Convert SVG to PIL Image first
                im = convert_svg_to_image(
                    input_path,
                    normalized_target,
                    dpi=kwargs.get('dpi', 300),
                    backend=kwargs.get('svg_backend', 'auto'),
                )
                save_image(
                    im,
                    final_output_path,
                    normalized_target,
                    quality=conversion_options['quality'],
                    optimize=conversion_options['optimize'],
                    progressive=conversion_options['progressive'],
                    background_for_jpeg=conversion_options['background_for_jpeg'],
                    ico_sizes=conversion_options['ico_sizes'],
                    extra_save_kwargs=conversion_options['extra_save_kwargs']
                )
            else:
                # Standard image conversion
                with Image.open(input_path) as im:
                    im.load()
                    save_image(
                        im,
                        final_output_path,
                        normalized_target,
                        quality=conversion_options['quality'],
                        optimize=conversion_options['optimize'],
                        progressive=conversion_options['progressive'],
                        background_for_jpeg=conversion_options['background_for_jpeg'],
                        ico_sizes=conversion_options['ico_sizes'],
                        extra_save_kwargs=conversion_options['extra_save_kwargs']
                    )
            print(f"SUCCESS: Conversion successful: {final_output_path}")
            converted_files.append(str(final_output_path))
        except Exception as e:
            raise RuntimeError(f"Conversion failed: {input_path} → {normalized_target}: {e}")

    print(f"OUTPUT: All converted files saved to: {output_dir_path}")

    # Return single string if single file was provided, otherwise return list
    if single_file:
        return converted_files[0]
    else:
        return converted_files
