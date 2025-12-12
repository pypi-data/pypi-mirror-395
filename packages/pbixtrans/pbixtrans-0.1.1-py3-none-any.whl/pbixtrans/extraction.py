import os
import shutil
import zipfile


def pbix_to_folder(pbix_path: str, output_folder: str) -> None:
    """Extracts a Power BI PBIX file into a folder structure.

    Power BI PBIX files are ZIP archives. This function temporarily renames
    the PBIX file to a ZIP file, extracts its contents into a directory, and
    removes the temporary ZIP file.

    Args:
        pbix_path (str): Path to the PBIX file to extract.
        output_folder (str): Directory where the extracted contents will be saved.

    Raises:
        FileNotFoundError: If `pbix_path` does not exist.

    Notes:
        - Existing directory contents are not cleared automatically.
        - The PBIX file remains unchanged; only a temporary copy is used.
    """
    print(f"Extracting PBIX: '{pbix_path}' to folder: '{output_folder}'")
    
    if not os.path.isfile(pbix_path):
        raise FileNotFoundError(f"{pbix_path} not found")
    
    if not pbix_path.lower().endswith(".pbix"):
        raise ValueError(f"Invalid file extension for PBIX: '{pbix_path}'. Expected a .pbix file.")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    zip_path = pbix_path + ".zip"
    shutil.copy(pbix_path, zip_path)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_folder)
    
    os.remove(zip_path)


def remove_security_bindings(folder_path: str) -> None:
    """Removes the `SecurityBindings` file from an extracted PBIX folder if it exists.

    Power BI includes a `SecurityBindings` file that may cause issues when
    rebuilding PBIX files. Removing it ensures that the resulting PBIX can be opened
    without security-related errors.

    Args:
        folder_path (str): Path to the extracted PBIX directory.

    Notes:
        - If the file does not exist, the function does nothing.
        - This operation is safe and does not affect report contents.
    """
    print(f"Removing SecurityBindings from folder: '{folder_path}'")
    
    sec_bindings_path = os.path.join(folder_path, "SecurityBindings")
    if os.path.exists(sec_bindings_path):
        os.remove(sec_bindings_path)
        print("File removed")
    else:
        print("No SecurityBindings file found")


def folder_to_pbix(folder_path: str, output_pbix: str) -> None:
    """Rebuilds a PBIX file from an extracted folder structure.

    This function traverses the extracted folder, zips all files back into a
    PBIX-compatible ZIP archive, and renames the ZIP to a `.pbix` file.

    Args:
        folder_path (str): The root directory containing the extracted PBIX.
        output_pbix (str): The path where the rebuilt PBIX file will be saved.

    Notes:
        - Any existing file at `output_pbix` will be overwritten.
        - Automatically removes `SecurityBindings` before packaging.
        - The PBIX file is created via a temporary ZIP file.
    """
    print(f"Rebuilding PBIX from folder: '{folder_path}' to file: '{output_pbix}'")
    
    remove_security_bindings(folder_path)
    
    temp_zip = output_pbix + ".zip"
    with zipfile.ZipFile(temp_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
    
    if os.path.exists(output_pbix):
        os.remove(output_pbix)
    
    shutil.move(temp_zip, output_pbix)
    shutil.rmtree(folder_path)

    print(f"✅ PBIX rebuilt successfully → {output_pbix}")