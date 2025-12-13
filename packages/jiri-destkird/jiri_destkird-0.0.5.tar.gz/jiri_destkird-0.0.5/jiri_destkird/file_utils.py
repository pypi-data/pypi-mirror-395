# In jiri_destkird/file_utils.py

import os
import logging
from pathlib import Path

# Setup basic logging
logger = logging.getLogger(__name__)
# logging.getLogger(__name__).addHandler(logging.NullHandler()) # Optional null handler

def rename_target_like_source(source_folder, target_folder):
    """
    Renames files in the target folder based on the names (stem) of files
    in the source folder, preserving the target file extensions.
    Files are matched based on sorted order.

    Args:
        source_folder (str): Path to the folder containing source files for names.
        target_folder (str): Path to the folder containing target files to be renamed.

    Raises:
        FileNotFoundError: If either source_folder or target_folder does not exist or is not a directory.

    Returns:
        tuple: A tuple containing (renamed_count, skipped_count).
    """
    source_path = Path(source_folder)
    target_path = Path(target_folder)
    renamed_count = 0
    skipped_count = 0

    if not source_path.is_dir():
        raise FileNotFoundError(f"Source folder not found or is not a directory: {source_folder}")
    if not target_path.is_dir():
        raise FileNotFoundError(f"Target folder not found or is not a directory: {target_folder}")

    # Get sorted lists of files (not directories)
    source_files = sorted([f for f in source_path.glob('*') if f.is_file()])
    target_files = sorted([f for f in target_path.glob('*') if f.is_file()])

    if not source_files:
        logger.warning(f"Source folder is empty: {source_folder}")
        return 0, len(target_files) # No names to use, skip all target files
    if not target_files:
        logger.warning(f"Target folder is empty: {target_folder}")
        return 0, 0 # Nothing to rename

    num_source = len(source_files)
    num_target = len(target_files)

    if num_source != num_target:
        logger.warning(f"Mismatch in file counts: Source ({num_source}) vs Target ({num_target}). "
                       f"Renaming up to {min(num_source, num_target)} files based on sorted order.")

    num_to_rename = min(num_source, num_target)

    for i in range(num_to_rename):
        source_stem = source_files[i].stem
        old_target_path = target_files[i]
        target_extension = old_target_path.suffix

        new_target_name = f"{source_stem}{target_extension}"
        new_target_path = target_path / new_target_name

        # --- Crucial Check for Collision ---
        if new_target_path.exists():
            # Decide what to do: skip, add number, overwrite (risky)
            # Option: Skip and log warning
            logger.warning(f"Skipping rename for '{old_target_path.name}': "
                           f"Target name '{new_target_name}' already exists.")
            skipped_count += 1
            continue # Move to the next file
        # ------------------------------------

        if old_target_path == new_target_path:
             logger.debug(f"Skipping rename for '{old_target_path.name}': Name is already correct.")
             skipped_count += 1
             continue # Skip if name is already what we want

        try:
            os.rename(old_target_path, new_target_path)
            logger.debug(f"Renamed: '{old_target_path.name}' -> '{new_target_name}'")
            renamed_count += 1
        except OSError as e: # Catch specific OS errors like permission denied
            logger.error(f"Error renaming '{old_target_path.name}' to '{new_target_name}': {e}")
            skipped_count += 1
        except Exception as e: # Catch unexpected errors
            logger.error(f"Unexpected error renaming '{old_target_path.name}': {e}", exc_info=True)
            skipped_count += 1

    # Log files in the target folder that were not renamed due to count mismatch
    if num_target > num_source:
         skipped_due_to_count = num_target - num_source
         skipped_count += skipped_due_to_count
         logger.warning(f"{skipped_due_to_count} files in target folder were not renamed due to lack of corresponding source files.")


    logger.info(f"File renaming complete. Renamed: {renamed_count}, Skipped/Errors: {skipped_count}")
    return renamed_count, skipped_count


# DO NOT INCLUDE THIS EXAMPLE CALL IN YOUR LIBRARY FILE
# Example usage (put this in a separate file, e.g., examples/rename_example.py)
# if __name__ == "__main__":
#     import logging
#     logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
#     try:
#         renamed, skipped = rename_target_like_source(
#             source_folder="path/to/source_names",
#             target_folder="path/to/files_to_rename"
#         )
#         print(f"Finished. Renamed {renamed} files, skipped {skipped}.")
#     except FileNotFoundError as e:
#         logging.error(e)