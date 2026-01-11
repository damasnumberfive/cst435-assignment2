# CST435 Assignment 2: Parallel Image Processing System

##  Project Overview

This project implements a parallel image processing system that applies various image filters using two different parallel programming paradigms in Python: **multiprocessing** and **concurrent.futures**. The system processes images from the Food-101 dataset and compares the performance characteristics of multiprocessing and concurrent.futures implementations.

### **Team Members**
1. **NURANYSA FATIHAH BINTI ISMAWADY** - 162756 - Serial Baseline & Report
2. **NURUL HAZLIN DAMASKA BINTI DARWIN** - 164390 - Concurrent.futures & Report
3. **NURAIN SYUHADA BINTI ADZHAR** - 162672 - Multiprocessing & Report
4. **SITI NUR IRDINA BINTI TURSE ZUHAIR** - 163854 - GCP Deployment & Video Presentation

### **Course Information**
- **Course:** CST435 - Parallel and Cloud Computing
- **Semester:** Semester 1 : 2025/2026
- **Submission Date:** 11 January 2026

---

##  Project Structure
```
CST435-ASSIGNMENT2/
├── input_images/              # Source images to be processed
├── output_concurrent/         # Images processed by Concurrent 
├── output_multiprocessing/    # Images processed by Multiprocessing
├── output_serial/             # Images processed by Serial Baseline
├── results/                   # Generated performance graphs
│   ├── efficiency.png
│   ├── execution_time.png
│   ├── performance_graphs.png
│   └── speedup.png
├── src/                       # Source code
│   ├── concurrent_futures.py
│   ├── create_graphs.py
│   ├── filters.py
│   ├── multiprocessing_image.py
│   └──serial_baseline.py
│
└── venv/
└──serial_baseline_value.csv
```

---

##  Image Filters Implemented

1. **Grayscale Conversion** - Converts RGB to grayscale using luminance formula
2. **Gaussian Blur** - Applies 3×3 Gaussian kernel for smoothing
3. **Edge Detection** - Sobel operator for edge detection
4. **Image Sharpening** - Enhances edges and details
5. **Brightness Adjustment** - Increases/decreases image brightness

---

##  Running on Google Cloud Platform

### **1. Create VM Instance**
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create VM: **e2-standard-8** (8 vCPUs, 32 GB RAM)
- OS: debian-12-bookworm-v20251209
- Region: us-central1-a

### **2. Set Up VM**
```bash

# Install dependencies
sudo apt update
sudo apt install -y python3-pip python3-numpy python3-pil python3-matplotlib unzip zip

# Create project directory
mkdir ~/cst435-assignment2
cd ~/cst435-assignment2
```
### **3. Upload Files**
- Use SSH window: Click **⚙️ gear icon** → **Upload file**
- Upload your code and images (as zip files)
- Extract: `unzip code.zip && unzip images.zip`

### **4. Run the Code**

**Important:** Always run the serial baseline first to generate the benchmark values:
```bash
# Step 1: Run serial baseline (MUST RUN FIRST)
python3 src/serial_baseline.py

# Step 2: Run multiprocessing (tests with 2, 4, 8 workers)
python3 src/multiprocessing_image.py

# Step 3: Run concurrent futures (tests with 2, 4, 8 workers)
python3 src/concurrent_futures.py

# Step 4: Generate performance graphs
python3 src/create_graphs.py
```

### **5. Download Results**
```bash
# Create zip of results
zip -r results.zip results/

```

---

##  Performance Results

### **Test Environment (GCP)**
- **Instance:** e2-standard-8
- **vCPUs:** 8
- **Memory:** 32 GB
- **OS:** debian-12-bookworm-v20251209
- **Images Tested:** 1,000 images (20 folders, 50 images per folder)
- **Total Tasks:** 5,000 (1,000 images × 5 filters)

### **Execution Time**

| Workers | Multiprocessing (s) | Concurrent Futures (s) |
|---------|---------------------|------------------------|
| Serial  | 34.87              | 34.87                 |
| 2       | 17.91              | 17.75                 |
| 4       | 10.50              | 9.34                  |
| 8       | 7.82               | 7.59                  |

### **Speedup Analysis**

Formula: `Speedup(N) = T_serial ÷ T_N`

| Workers | Multiprocessing | Concurrent Futures |
|---------|-----------------|-------------------|
| 2       | 1.95x          | 1.96x            | 
| 4       | 3.32x          | 3.73x            | 
| 8       | 4.46x          | 4.59x            | 

### **Parallel Efficiency**

Formula: `Efficiency(N) = [Speedup(N) ÷ N] × 100%`

| Workers | Multiprocessing | Concurrent Futures |
|---------|-----------------|-------------------|
| 2       | 97%            | 98%              |
| 4       | 83%            | 93%              |
| 8       | 56%            | 57%              |


---

## Implementation Details

### **Serial Baseline**
- Processes images sequentially without any parallelization
- Establishes benchmark performance (34.87s) for calculating speedup and efficiency
- Results saved to `serial_baseline_value.csv` for use by parallel implementations

### **Multiprocessing**
- Runs multiple processes simultaneously, bypassing Python's GIL (Global Interpreter Lock)
- Each process has its own independent memory space
- Uses `multiprocessing.Pool` to distribute tasks across workers
- Tests with 2, 4, and 8 workers
- Best suited for CPU-intensive operations like image processing

### **Concurrent.futures**
- Uses `ProcessPoolExecutor` for high-level process management
- Implements Future objects for asynchronous task execution
- Provides cleaner code structure and better error handling
- Tests with 2, 4, and 8 workers
- Slightly more efficient task scheduling than raw multiprocessing

### **Performance Comparison:** 
- **Concurrent Futures demonstrates better performance than Multiprocessing, especially at 4 workers (9.34s vs 10.50s)**
- **Both methods achieve strong speedup with 2-4 workers, with diminishing returns at 8 workers due to overhead and sequential code portions**

---

## Technologies Used

- **Python 3.8+**
- **Pillow (PIL)** - Image processing
- **NumPy** - Array operations
- **Matplotlib** - Performance graphs
- **Pandas** - Data analysis
- **Google Cloud Platform** - VM deployment

---

## References

1. Amdahl, G. M. (1967). Validity of the single processor approach to achieving large scale computing capabilities. Proceedings of the April 18-20, 1967, Spring Joint Computer Conference on - AFIPS '67 (Spring). https://doi.org/10.1145/1465482.1465560

2. Compute Engine documentation | Compute Engine Documentation. (n.d.). Google Cloud. https://cloud.google.com/compute/docs

3. concurrent.futures — Launching parallel tasks — Python 3.9.5 documentation. (n.d.). Docs.python.org. https://docs.python.org/3/library/concurrent.futures.html

4. Food 101. (n.d.). Kaggle. https://www.kaggle.com/datasets/dansbecker/food-101

5. Python. (n.d.). multiprocessing — Process-based parallelism — Python 3.8.3rc1 documentation. Docs.python.org. https://docs.python.org/3/library/multiprocessing.html

6. Python Software Foundation. (n.d.). os — Miscellaneous operating system interfaces — Python 3.8.0 documentation. Python.org. https://docs.python.org/3/library/os.html

7. Roberts, P. (2024, February 8). When linear scaling is too slow — Compress your data. Medium. https://medium.com/@paigeonthewing/when-linear-scaling-is-too-slow-compress-your-data-a6efd5452e73

---

## Video Demonstration

**YouTube Link:** https://youtu.be/S1dEaQNGDYo

---

##  License

This project is for academic purposes as part of CST435: Parallel and Cloud Computing course.

---