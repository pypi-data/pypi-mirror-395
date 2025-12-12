from typing import Mapping
import io
import zipfile
import base64


def create_encoded_zip(files: Mapping[str, str | bytes]) -> str:
    # Create a BytesIO object to hold the zip file in memory
    zip_buffer = io.BytesIO()
    # Create a ZipFile object
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for path, content in files.items():
            # Add each file to the zip file
            zip_file.writestr(path, content)
    # Move to the beginning of the BytesIO buffer
    zip_buffer.seek(0)
    # Encode the zip file in Base64
    base64_zip = base64.b64encode(zip_buffer.read()).decode('utf-8')
    return base64_zip
