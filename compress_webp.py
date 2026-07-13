import os
import glob
from PIL import Image

def compress_frames():
    input_dir = "ezgif-74dc65c3b7383343-jpg (1)"
    output_dir = "frames-webp"
    os.makedirs(output_dir, exist_ok=True)
    
    files = sorted(glob.glob(f"{input_dir}/*.jpg"))
    for file in files:
        img = Image.open(file)
        basename = os.path.basename(file).replace(".jpg", ".webp")
        out_path = os.path.join(output_dir, basename)
        # WebP compression
        img.save(out_path, 'webp', quality=50, method=4)
        
    print(f"Compressed {len(files)} frames to WebP.")

if __name__ == "__main__":
    compress_frames()
