import os # Handle file paths
import time # Measure execution time for benchmarking
import threading # For TID retrieval
import pandas as pd  # CSV report
from filters import process_image # For image processing

# This section used for current Process ID and Thread ID retrieval
# Ensure that the process is executing in serial sequence
def get_thread_info():
   """Returns the current Process ID (PID) and Thread ID (TID)."""
   pid = os.getpid()
   tid = threading.get_ident()
   return f"PID: {pid} | TID: {tid}"


# The header of the output 
def main():
   print(f"\n{'='*60}")
   print(f"Serial Baseline (No Parallelism)")
   print(f"{'='*60}")
   print(f"Main Process Info: {get_thread_info()}")


   # This is to detemine the project path, ensure script run correctly
   current_script_dir = os.path.dirname(os.path.abspath(__file__))
   project_root = os.path.dirname(current_script_dir)
   INPUT_FOLDER = os.path.join(project_root, "input_images")
   OUTPUT_FOLDER = os.path.join(project_root, "output_serial")


   # For input dataset validation
   if not os.path.exists(INPUT_FOLDER):
       print(f"Error: Could not find input folder at: {INPUT_FOLDER}")
       return


    # For oupout file validation
   os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Get dataset from the input directory
    # Find files in the sub folder
   image_paths = []
   for root, dirs, files in os.walk(INPUT_FOLDER):
       for file in files:
           if file.lower().endswith(('.png', '.jpg', '.jpeg')):
               full_path = os.path.join(root, file)
               image_paths.append(full_path)


    # If no image is found, the execution will automatically abort
   if not image_paths:
       print(f"No images found in {INPUT_FOLDER}.")
       return


   print(f"Found {len(image_paths)} images. Starting Serial Execution...")
   print(f"{'-'*60}")


   # Serial Processing Loop
   results_data = []
  
   global_start_time = time.time() # Global start time. This is for the total executaion of benchmark
  
   # Indicate that image is processed one after another
   for index, img_path in enumerate(image_paths):
       # Start timer
       start_time = time.time()
      
       # Process the image
       result = process_image(img_path, OUTPUT_FOLDER)
      
       # Stop timer
       duration = time.time() - start_time
      

       real_name = result.get("filename", os.path.basename(img_path))
      
       # Print execution status including PID and TID
       print(f"[{index+1}/{len(image_paths)}] {real_name:<30} | Time: {duration:.4f}s | {get_thread_info()}")
      
       # Collect data for CSV
       results_data.append({
           "filename": real_name, # Save the new name to CSV too
           "duration_seconds": duration,
           "status": result.get("status"),
           "pid": os.getpid(),
           "tid": threading.get_ident()
       })
   
   # Used for total execution time calculation
   total_time = time.time() - global_start_time


   # Serial Execution Summarisation
   print(f"{'='*60}")
   print(f"Serial Processing Complete!")
   print(f"Total Execution Time: {total_time:.4f} seconds")
   print(f"{'='*60}")


   # Save result to CSV
   # Enabling performance comparison with parallel implementations
   csv_path = os.path.join(project_root, "serial_results.csv")
   try:
       df = pd.DataFrame(results_data)
       df.to_csv(csv_path, index=False)
       print(f"Detailed results saved to: {csv_path}")
   except Exception as e:
       print(f"Warning: Could not save CSV report. Error: {e}")


if __name__ == "__main__":
   main()
