import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

def upload_to_cloudinary(filename, file_data):
    # Extract extension
    ext = os.path.splitext(filename)[1]  # e.g., '.pdf' or '.docx'
    if ext.startswith("."):
        ext = ext[1:]

    # Ensure filename includes extension for raw resource
    full_filename = f"{filename}.{ext}" if not filename.endswith(ext) else filename

    res = cloudinary.uploader.upload(
        BytesIO(file_data),
        public_id=full_filename,
        resource_type="raw",
        format=ext  # 👈 Force file format
    )
    return res["secure_url"]
