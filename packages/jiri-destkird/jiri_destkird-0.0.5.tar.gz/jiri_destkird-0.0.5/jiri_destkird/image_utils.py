# In jiri_destkird/image_utils.py

import os
import logging
from PIL import Image, UnidentifiedImageError # Import specific error

# Setup basic logging for the library user to configure
logger = logging.getLogger(__name__)
# Optional: Add a default null handler to prevent "No handler found" warnings
# logging.getLogger(__name__).addHandler(logging.NullHandler())

def rotate_folder(folder_path, degrees=90, overwrite=False, output_folder=None,
                   expand_canvas=True, output_suffix="_rotated",
                   supported_formats=('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
    """
    Rotates all images in a folder by specified degrees.

    Args:
        folder_path (str): Path to the folder containing images.
        degrees (int, optional): Rotation angle. Defaults to 90.
        overwrite (bool, optional): Overwrite original files if True. Defaults to False.
        output_folder (str, optional): Custom output folder path. Defaults to None.
        expand_canvas (bool, optional): Allows the image canvas to expand to fit the
                                     entire rotated image. Defaults to True.
        output_suffix (str, optional): Suffix to add to filename when not overwriting
                                    and no output_folder is specified. Defaults to "_rotated".
        supported_formats (tuple, optional): Tuple of image file extensions to process.
                                            Defaults to ('.jpg', '.jpeg', '.png', '.bmp', '.gif').

    Raises:
        FileNotFoundError: If the input folder_path does not exist.
        ValueError: If degrees is not a number or output_suffix is invalid.
    """
    if not isinstance(degrees, (int, float)):
        raise ValueError("Degrees must be a number.")
    if not isinstance(output_suffix, str): # Example of more input validation
        raise ValueError("output_suffix must be a string.")

    if not os.path.isdir(folder_path): # Check if it's a directory
        raise FileNotFoundError(f"Input folder not found or is not a directory: {folder_path}")

    # Create output folder if needed and doesn't exist
    save_to_output_dir = output_folder is not None
    if save_to_output_dir and not overwrite:
        if not os.path.exists(output_folder):
            try:
                os.makedirs(output_folder)
                logger.info(f"Created output folder: {output_folder}")
            except OSError as e:
                logger.error(f"Could not create output folder {output_folder}: {e}")
                return # Stop processing if output folder cannot be created
        elif not os.path.isdir(output_folder):
             logger.error(f"Output path {output_folder} exists but is not a directory.")
             return # Stop if output path is invalid


    processed_count = 0
    error_count = 0
    for filename in os.listdir(folder_path):
        # Check if the file has a supported extension AND is actually a file
        file_path = os.path.join(folder_path, filename)
        if filename.lower().endswith(supported_formats) and os.path.isfile(file_path):
            try:
                with Image.open(file_path) as img: # Use 'with' to ensure file is closed
                    # Rotate image
                    rotated_img = img.rotate(degrees, expand=expand_canvas)

                    # Determine output path
                    if overwrite:
                        output_path = file_path
                    elif save_to_output_dir:
                        output_path = os.path.join(output_folder, filename)
                    else:
                        name, ext = os.path.splitext(filename)
                        output_path = os.path.join(folder_path, f"{name}{output_suffix}{ext}")

                    rotated_img.save(output_path)
                    logger.debug(f'Processed: {filename} -> {output_path} (Rotated {degrees}°, Expand: {expand_canvas})')
                    processed_count += 1

            except UnidentifiedImageError:
                 logger.warning(f'Skipping non-image or corrupted file: {filename}')
                 error_count += 1
            except IOError as e: # Catch file saving errors
                 logger.error(f"Could not save rotated image {output_path}: {e}")
                 error_count += 1
            except Exception as e: # Catch unexpected errors but log them
                logger.error(f'Unexpected error processing {filename}: {e}', exc_info=True) # exc_info adds traceback
                error_count += 1
        # Optional: Log files that are skipped due to format or not being a file
        # else:
        #    if os.path.isfile(file_path): # Only log actual files being skipped
        #        logger.debug(f"Skipping file with unsupported format: {filename}")


    logger.info(f"Image rotation complete. Processed: {processed_count}, Errors/Skipped: {error_count}")


# DO NOT INCLUDE THIS EXAMPLE CALL IN YOUR LIBRARY FILE
# Example usage (put this in a separate file, e.g., examples/rotate_example.py)
# if __name__ == "__main__":
#     import logging
#     logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
#     try:
#         rotate_folder(
#             folder_path=r'path/to/your/input_images',
#             degrees=90,
#             overwrite=False,
#             output_folder=r'path/to/your/output_images',
#             expand_canvas=False # Example: Don't expand canvas
#         )
#     except FileNotFoundError as e:
#         logging.error(e)
#     except ValueError as e:
#         logging.error(e)