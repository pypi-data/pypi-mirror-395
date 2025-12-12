"""Main Entry Point for the Image Batch Converter MCP Server."""

from .conversion import auto_convert_folder

from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent, ErrorData
from mcp import McpError
import gc
import sys
from typing import Optional

mcp = FastMCP("image-batch-converter")


def ok(msg: str) -> TextContent:
    """Create a Success Response."""
    return TextContent(type="text", text=msg)


@mcp.tool(
    "batch_convert_images",
    description="Batch convert image file list to specified format (jpeg, png, webp, heic, avif, bmp, tiff, ico). "
    "Supports SVG input format (using PyMuPDF, no system dependencies required). "
    "Converted images will be saved in a new subfolder in the directory of the first file. "
    "Parameters: input_files (list) = List of image file paths || "
    "target_format (str) = Target format (jpeg, png, webp, heic, avif, bmp, tiff, ico) || "
    "ico_sizes (list)(optional) = ICO icon size list, only for ico format, e.g. [16,32,48,64,128,256]. Defaults to smart size selection || "
    "dpi (int)(optional) = DPI for SVG conversion, defaults to 300 || "
    "svg_backend (str)(optional) = SVG rendering backend (defaults to 'auto', uses PyMuPDF) || "
    "quality (int)(optional) = Output quality (1-100), only for JPEG/WEBP/HEIF/AVIF, defaults to None (uses format default) || "
    "optimize (bool)(optional) = Whether to optimize file size, defaults to True"
)
def batch_convert_images_tool(
    input_files: list,
    target_format: str,
    ico_sizes: Optional[list] = None,
    dpi: int = 300,
    svg_backend: str = "auto",
    quality: Optional[int] = None,
    optimize: bool = True
) -> TextContent:
    """Batch Convert Multiple Image Files to Target Format."""
    try:
        # Validate input_files is a list
        if not input_files or not isinstance(input_files, list):
            raise McpError(ErrorData(
                code=-1,
                message="Failed to Convert Images: input_files must be a non-empty list of file paths",
                data={"input_files": input_files, "target_format": target_format}
            ))

        # Capture stdout/stderr to collect output
        import io
        from contextlib import redirect_stdout, redirect_stderr

        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer), redirect_stderr(output_buffer):
            # 准备kwargs参数
            kwargs = {}
            if ico_sizes is not None:
                kwargs['ico_sizes'] = tuple(ico_sizes)
            if dpi is not None:
                kwargs['dpi'] = dpi
            if svg_backend is not None:
                kwargs['svg_backend'] = svg_backend
            if quality is not None:
                kwargs['quality'] = quality
            if optimize is not None:
                kwargs['optimize'] = optimize

            result = auto_convert_folder(input_files, target_format, **kwargs)

        # Get output text
        output_text = output_buffer.getvalue()

        # Check for failures and include error details
        if result.get('failed'):
            # Extract error messages from output
            error_lines = [line for line in output_text.split('\n') if 'WARNING' in line or 'ERROR' in line or 'Failed' in line]
            error_details = '\n'.join(error_lines) if error_lines else 'Unknown error'
            # Raise MCP error so caller sees isError=true when any file fails
            raise McpError(ErrorData(
                code=-1,
                message="Failed to Convert Some Images",
                data={
                    "converted": result.get("converted", []),
                    "failed": result.get("failed", []),
                    "skipped_already_target": result.get("skipped_already_target", []),
                    "output_folder": result.get("output_folder", "N/A"),
                    "details": error_details
                }
            ))

        # Build success message with details
        success_msg = f"Successfully converted {len(result.get('converted', []))} images\n"
        success_msg += f"Output folder: {result.get('output_folder', 'N/A')}\n"

        if result.get('skipped_already_target'):
            success_msg += f"\nSkipped {len(result.get('skipped_already_target', []))} files already in target format"

        # Include any warnings from the output
        warnings = [line.strip() for line in output_text.split('\n') if "(WARNING)" in line]
        if warnings:
            success_msg += f"\n\nWarnings:\n" + "\n".join(warnings)

        return ok(success_msg)

    except McpError:
        # Re-raise McpError as is
        raise
    except Exception as e:
        # Convert any other exception to McpError
        raise McpError(ErrorData(
            code=-1,
            message=f"Failed to Convert Images: {str(e)}",
            data={"input_files": input_files, "target_format": target_format}
        ))
    finally:
        # Simple Memory Cleanup
        gc.collect()


def main():
    """Run the MCP Server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
