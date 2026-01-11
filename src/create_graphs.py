import os
import matplotlib.pyplot as plt
import numpy as np

# Creates graphs for performance analysis using hardcoded data
def create_charts():
    # Path setup
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_script_dir)
    RESULTS_FOLDER = os.path.join(project_root, "results")
    
    os.makedirs(RESULTS_FOLDER, exist_ok=True)
    print(f"Graphs will be saved to: {RESULTS_FOLDER}")


    # Test Data (Hardcoded from previous multiprocesing and concurrent futures runs)
    workers = [2, 4, 8]
    
    # Serial Benchmarks to count speedup
    serial_mp = 34.87
    serial_cf = 34.87

    # Parallel Execution Times
    mp_times = [17.91, 10.50, 7.82] 
    cf_times = [17.75, 9.35, 7.59]

    # Calculate Speedup and Efficiency
    # 1. Speedup = T_serial / T_parallel
    mp_speedup = [serial_mp / t for t in mp_times]
    cf_speedup = [serial_cf / t for t in cf_times]

    # 2. Efficiency = Speedup / Num_Workers
    mp_efficiency = [s / w for s, w in zip(mp_speedup, workers)]
    cf_efficiency = [s / w for s, w in zip(cf_speedup, workers)]
    
    c_mp = '#4e79a7' # Blue
    c_cf = '#f28e2b' # Orange
    c_ideal = 'gray'

    # CHART 1: Execution Time (Bar Chart)
    plt.figure(figsize=(10, 6))
    x = np.arange(len(workers))
    width = 0.35
    
    rects1 = plt.bar(x - width/2, mp_times, width, label='Multiprocessing', color=c_mp)
    rects2 = plt.bar(x + width/2, cf_times, width, label='Concurrent Futures', color=c_cf)
    
    # Reference Lines
    plt.axhline(y=serial_mp, color=c_mp, linestyle=':', alpha=0.7, label=f'Serial MP ({serial_mp:.2f}s)')
    plt.axhline(y=serial_cf, color=c_cf, linestyle=':', alpha=0.7, label=f'Serial CF ({serial_cf:.2f}s)')

    plt.ylabel('Time (Seconds)', fontweight='bold')
    plt.xlabel('Number of Workers', fontweight='bold')
    plt.title('Execution Time Comparison (Lower is Better)', fontweight='bold')
    plt.xticks(x, workers)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    
    plt.bar_label(rects1, padding=3, fmt='%.2fs')
    plt.bar_label(rects2, padding=3, fmt='%.2fs')
    
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_FOLDER, 'execution_time.png'), dpi=300)
    plt.close() # Close memory to start fresh for next graph

    # CHART 2: Speedup (Line Chart)
    plt.figure(figsize=(10, 6))
    plt.plot(workers, mp_speedup, marker='o', linewidth=2.5, label='Multiprocessing', color=c_mp)
    plt.plot(workers, cf_speedup, marker='s', linewidth=2.5, label='Concurrent Futures', color=c_cf)
    plt.plot(workers, workers, '--', color=c_ideal, label='Ideal Scaling', alpha=0.5)
    
    plt.ylabel('Speedup Factor (x times faster)', fontweight='bold')
    plt.xlabel('Number of Workers', fontweight='bold')
    plt.title('Speedup Analysis (Higher is Better)', fontweight='bold')
    plt.xticks(workers)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_FOLDER, 'speedup.png'), dpi=300)
    plt.close()

    # CHART 3: Efficiency (Line Chart)
    plt.figure(figsize=(10, 6))
    plt.plot(workers, mp_efficiency, marker='o', linewidth=2.5, label='Multiprocessing', color=c_mp)
    plt.plot(workers, cf_efficiency, marker='s', linewidth=2.5, label='Concurrent Futures', color=c_cf)
    
    # Ideal Efficiency Line (1.0)
    plt.axhline(y=1.0, color=c_ideal, linestyle='--', label='Ideal Efficiency (1.0)', alpha=0.5)
    
    plt.ylabel('Efficiency (Speedup / Workers)', fontweight='bold')
    plt.xlabel('Number of Workers', fontweight='bold')
    plt.title('Parallel Efficiency (Higher is Better, Max 1.0)', fontweight='bold')
    plt.xticks(workers)
    plt.ylim(0, 1.15) 
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.3)
    
    # Annotate points
    for i, txt in enumerate(mp_efficiency):
        plt.annotate(f"{txt:.2f}", (workers[i], mp_efficiency[i]), 
                     xytext=(0, 8), textcoords='offset points', ha='center', color=c_mp, fontweight='bold')

    for i, txt in enumerate(cf_efficiency):
        plt.annotate(f"{txt:.2f}", (workers[i], cf_efficiency[i]), 
                     xytext=(0, -15), textcoords='offset points', ha='center', color=c_cf, fontweight='bold')

    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_FOLDER, 'efficiency.png'), dpi=300)
    plt.close()
    
    print("Success! Created 3 separate graph files.")

if __name__ == "__main__":
    create_charts()