import os
import time # To measure exactly how long the code takes to run
import concurrent.futures # A library that provides the ProcessPoolExecutor, which manages the worker processes
from filters import process_image # Imports function that does the actual work (blurring, edges, etc.) from filters.py
import csv
# Serial Benchmark Values Loader
def load_serial_baseline():
    """Load the serial baseline from CSV file."""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        baseline_path = os.path.join(project_root, "serial_baseline_value.csv")

        with open(baseline_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['metric'] == 'serial_baseline':
                    return float(row['value'])

    except FileNotFoundError:
        print("❌ Error: serial_baseline_value.csv not found!")
        print("Please run serial_baseline.py first!")
        exit(1)

    print("❌ Error: serial baseline not found in CSV!")
    exit(1)


# Runs the image processing pipeline with a specific number of workers.
# Returns the time taken.
def run_test_with_workers(num_workers, image_paths, output_folder):
    
    print(f"   Testing with {num_workers} worker(s)...", end=" ", flush=True)
    
    start_time = time.time() # start timer
    
    success_count = 0
    fail_count = 0
    worker_stats = {} # Track how many tasks each worker (PID) processed for load balancing analysis
    
    # concurrent.futures.ProcessPoolExecutor, hides the complexity of managing processes 
    # ProcessPoolExecutor creates a pool of worker processes
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        for img_path in image_paths:
            
            futures.append(executor.submit(process_image, img_path, output_folder))
            
    
        done, not_done = concurrent.futures.wait(futures) # Wait for all tasks to finish
        
        # Analyze results
        for f in done:
            try:
                result = f.result()
                
                # 1. Count Success/Fail
                if result.get("status") == "Success":
                    success_count += 1
                else:
                    fail_count += 1
                
                # 2. Track Worker PIDs (Collect the data)
                pid = result.get("pid")
                if pid:
                    if pid in worker_stats:
                        worker_stats[pid] += 1
                    else:
                        worker_stats[pid] = 1
                        
            except Exception:
                fail_count += 1

    end_time = time.time() # stop timer
    duration = end_time - start_time # calculate total duration taken to process all images
    
    print(f"Done! ({duration:.4f}s)")
    print(f"      [Stats] Success: {success_count} | Failed: {fail_count}")
    
    print(f"      [Load Balancing] Worker Breakdown:")
    for pid, count in worker_stats.items():
        print(f"         - Worker PID {pid}: Processed {count} images")
    print("") 
    
    return duration

def main():
    print(f"\n{'='*60}")
    print(f"Automated Performance Test: Concurrent Futures")
    print(f"{'='*60}")

    # Path setup
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_script_dir)
    INPUT_FOLDER = os.path.join(project_root, "input_images")
    OUTPUT_FOLDER = os.path.join(project_root, "output_concurrent")
    SERIAL_OUTPUT = os.path.join(project_root, "output_serial_bench")

    # Check if input folder exists
    if not os.path.exists(INPUT_FOLDER):
        print(f"Error: Could not find input folder at: {INPUT_FOLDER}")
        return

     # Create output folder if it doesn't exist
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(SERIAL_OUTPUT, exist_ok=True) 

    # Load input images using os.walk
    image_paths = []
    for root, dirs, files in os.walk(INPUT_FOLDER):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                full_path = os.path.join(root, file)
                image_paths.append(full_path)

    if not image_paths:
        print(f"No images found. Please add images to 'input_images' folder.")
        return

    print(f"Found {len(image_paths)} images.\n")

    # Get the serial baseline time
    serial_time = load_serial_baseline()
    print(f" Using serial baseline: {serial_time:.4f}s")

    # Run the parallel execution 
    print("Starting Parallel Tests...")
    # Use loop to test different worker amounts
    # We test 2, 4, and 8 workers
    worker_counts = [2, 4, 8] 
    results = {}  # To store the times

    for count in worker_counts:
        time_taken = run_test_with_workers(count, image_paths, OUTPUT_FOLDER) # Run test function
        results[count] = time_taken

    # Final report table 
    print(f"{'-'*60}")
    print(f"{'Workers':<10} | {'Time (s)':<15} | {'Speedup (x)':<15}")
    print(f"{'-'*60}")

    for count in worker_counts:
        time_taken = results[count]
        
        # Calculate Speedup using the Serial Baseline
        speedup = serial_time / time_taken 
        
        print(f"{count:<10} | {time_taken:<15.4f} | {speedup:<15.2f}") 
    
    print(f"{'='*60}")
    print("Test Complete.")

if __name__ == '__main__':
     # On Windows, multiprocessing requires the main guard
    main()