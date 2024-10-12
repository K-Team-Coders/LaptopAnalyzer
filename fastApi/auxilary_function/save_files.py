# Function to save uploaded files and return file paths
import uuid
from typing import List

from fastapi import UploadFile

import os

directory_path = "uploads/"

# Check if the directory exists
if not os.path.exists(directory_path):
    # Create the directory if it doesn't exist
    os.makedirs(directory_path)
    print(f"Directory created: {directory_path}")
else:
    print(f"Directory already exists: {directory_path}")


async def save_files(files: List[UploadFile], appeal_uuid: uuid.UUID):
    saved_paths = []
    for file in files:
        file_extension = file.filename.split(".")[-1]
        # Generate a unique file name using the appeal UUID and the file name
        file_path = os.path.join(directory_path, f"{appeal_uuid}_{file.filename}")
        saved_paths.append(file_path)
        # Save file to disk
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
    return saved_paths
