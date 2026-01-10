import os
from PIL import Image, ImageFilter, ImageEnhance

def process_image(file_path, output_folder):
    """
    Applies 5 separate filters to an image and organizes them into subfolders.
    Returns a dictionary with status and worker PID for tracking.
    """
    # Initialize filename just in case an error occurs before it's set
    filename = "unknown"
    
    try:
        # 1. Get the category name from the folder (e.g., "apple_pie")
        category_name = os.path.basename(os.path.dirname(file_path))
        
        # 2. Get the original filename (e.g., "10293.jpg")
        original_name = os.path.basename(file_path)
        
        # 3. Create a unique name (e.g., "apple_pie_10293.jpg")
        # This prevents overwriting when different folders have images with the same name
        filename = f"{category_name}_{original_name}"
        
        # Open the original image ONCE
        original_img = Image.open(file_path).convert("RGB")
        
        # Helper function to save to specific subfolder
        def save_to_subfolder(img_obj, subfolder_name):
            # Create the subfolder (e.g., output/blur)
            target_dir = os.path.join(output_folder, subfolder_name)
            os.makedirs(target_dir, exist_ok=True) 
            
            # Save the image inside
            save_path = os.path.join(target_dir, filename)
            img_obj.save(save_path)

        # FILTER 1: Grayscale 
        img_gray = original_img.copy().convert("L")
        save_to_subfolder(img_gray, "grayscale")
        
        # FILTER 2: Blur 
        img_blur = original_img.copy()
        img_blur = img_blur.filter(ImageFilter.GaussianBlur(radius=3))
        save_to_subfolder(img_blur, "blur")
        
        # FILTER 3: Edge Detection
        img_edge = original_img.copy().convert("L")
        img_edge = img_edge.filter(ImageFilter.FIND_EDGES)
        save_to_subfolder(img_edge, "edge")
        
        # FILTER 4: Sharpening
        img_sharp = original_img.copy()
        enhancer = ImageEnhance.Sharpness(img_sharp)
        img_sharp = enhancer.enhance(3.0) 
        save_to_subfolder(img_sharp, "sharpen")
        
        # FILTER 5: Brightness
        img_bright = original_img.copy()
        enhancer = ImageEnhance.Brightness(img_bright)
        img_bright = enhancer.enhance(1.5) 
        save_to_subfolder(img_bright, "brightness")

        # Return Success and the Worker PID
        return {
            "status": "Success", 
            "filename": filename, 
            "pid": os.getpid() # Track which worker did this job
        }

    except Exception as e:
        # Return Error AND the Worker PID
        return {
            "status": "Error", 
            "filename": filename, 
            "error": str(e),
            "pid": os.getpid() # Track errors by worker too
        }