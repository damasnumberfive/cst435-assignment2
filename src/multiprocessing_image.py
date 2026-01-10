import os
import time
import multiprocessing
from filters import process_image 

# --- SERIAL BENCHMARK (To match concurrent_futures.py) ---
def run_serial_benchmark(image_paths, output_folder):
    print(f"    Speedup Benchmark: Running Serial Baseline -> ", end=" ", flush=True)
    start_time = time.time()
    
    for img_path in image_paths:
        process_image(img_path, output_folder)
        
    end_time = time.time()
    duration = end_time - start_time
    print(f"({duration:.4f}s)")
    return duration

# --- MULTIPROCESSING TEST FUNCTION ---
def run_test_with_processes(num_processes, image_paths, output_folder):
    # LOAD BALANCING: multiprocessing.Pool automatically distributes the 
    # tasks in the 'tasks' list across the available processes.
    print(f"    Testing with {num_processes} process(es)...", end=" ", flush=True)
    
    start_time = time.time()
    
    # Prepare arguments for process_image(file_path, output_folder)
    tasks = [(img_path, output_folder) for img_path in image_paths]
    
    success_count = 0
    fail_count = 0
    process_stats = {} # Dictionary to count tasks per worker (PID -> Count)

    # ✅ USES multiprocessing.Pool (The Classic Parallel Paradigm)
    with multiprocessing.Pool(processes=num_processes) as pool:
        # starmap applies the function to the list of tuples (tasks)
        results = pool.starmap(process_image, tasks)
        
        # --- ANALYZE RESULTS ---
        for result in results:
            if result.get("status") == "Success":
                success_count += 1
            else:
                fail_count += 1
            
            # Track Worker PIDs to demonstrate parallel execution
            pid = result.get("pid")
            if pid:
                # If PID exists in dict, add 1. If not, set to 1.
                process_stats[pid] = process_stats.get(pid, 0) + 1

    end_time = time.time()
    duration = end_time - start_time
    
    print(f"Done! ({duration:.4f}s)")
    print(f"      [Stats] Success: {success_count} | Failed: {fail_count}")
    
    # --- PRINT WORKER BREAKDOWN (Restored!) ---
    # This proves how the work was distributed (Load Balancing)
    print(f"      [Load Balancing] Process Breakdown:")
    for pid, count in process_stats.items():
        print(f"         - Process PID {pid}: Processed {count} images")
    print("") # Empty line for cleanliness
    
    return duration

def main():
    print(f"\n{'='*60}")
    print(f"Automated Performance Test: Multiprocessing")
    print(f"{'='*60}")

    # Path setup - Exactly tallied to Alin's paths
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_script_dir)
    INPUT_FOLDER = os.path.join(project_root, "input_images")
    OUTPUT_FOLDER = os.path.join(project_root, "output_multiprocessing")
    SERIAL_OUTPUT = os.path.join(project_root, "output_serial_bench")
    
    if not os.path.exists(INPUT_FOLDER):
        print(f"Error: Could not find input folder at: {INPUT_FOLDER}")
        return

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(SERIAL_OUTPUT, exist_ok=True)

    # Load images using os.walk
    image_paths = []
    for root, dirs, files in os.walk(INPUT_FOLDER):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_paths.append(os.path.join(root, file))

    if not image_paths:
        print(f"No images found. Please add images to 'input_images' folder.")
        return

    print(f"Found {len(image_paths)} images.\n")

    # --- STEP 1: GET THE SERIAL BASELINE ---
    serial_time = run_serial_benchmark(image_paths, SERIAL_OUTPUT)
    print(f"{'-'*60}\n")

    # --- STEP 2: RUN PARALLEL TESTS ---
    print("Starting Parallel Tests...")
    process_counts = [1, 2, 4, 8]
    results = {} 

    for count in process_counts:
        time_taken = run_test_with_processes(count, image_paths, OUTPUT_FOLDER)
        results[count] = time_taken

    print(f"{'-'*60}")
    print(f"{'Process':<10} | {'Time (s)':<15} | {'Speedup (x)':<15}")
    print(f"{'-'*60}")

    for count in process_counts:
        time_taken = results[count]
        speedup = serial_time / time_taken 
        print(f"{count:<10} | {time_taken:<15.4f} | {speedup:<15.2f}") 
    
    print(f"{'='*60}")
    print("Test Complete.")

if __name__ == '__main__':
    # On Windows, multiprocessing requires the main guard
    main()