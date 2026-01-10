# CST435 Assignment 2: Parallel Image Processing System

## 📋 Project Overview

This project implements a parallel image processing system that applies various image filters using two different parallel programming paradigms in Python: **multiprocessing** and **concurrent.futures**. The system processes images from the Food-101 dataset and compares the performance characteristics of multiprocessing and concurrent.futures implementations.

### **Team Members**
1. **NURANYSA FATIHAH BINTI ISMAWADY** - 162756 - Serial Baseline & Report
2. **NURUL HAZLIN DAMASKA BINTI DARWIN** - 164390 - Concurrent.futures & Report
3. **NURAIN SYUHADA BINTI ADZHAR** - 162672 - Multiprocessing & Report
4. **SITI NUR IRDINA BINTI TURSE ZUHAIR** - 163854 - GCP Deployment & Video Presentation

### **Course Information**
- **Course:** CST435 - Parallel and Cloud Computing
- **Semester:** Semester 1 : 2025/2026
- **Submission Date:** January 11, 2026

---

## 🏗️ Project Structure

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
│   ├── serial_baseline.py
│   └── serial_results.csv
└── venv/
```

---

##  Image Filters Implemented

1. **Grayscale Conversion** - Converts RGB to grayscale using luminance formula
2. **Gaussian Blur** - Applies 3×3 Gaussian kernel for smoothing
3. **Edge Detection** - Sobel operator for edge detection
4. **Image Sharpening** - Enhances edges and details
5. **Brightness Adjustment** - Increases/decreases image brightness

---

##  Installation

### **Clone Repository**
```bash
git clone https://github.com/damasnumberfive/cst435-assignment2.git
cd CST435-Assignment2
```

### **Install Dependencies**
```bash
pip install pillow matplotlib numpy pandas
```

---

##  Running on Google Cloud Platform

### **1. Create VM Instance**
- Go to [Google Cloud Console](https://console.cloud.google.com/)
- Create VM: **e2-standard-4** (4 vCPUs, 16 GB RAM)
- OS: Ubuntu 20.04 LTS, 50GB disk
- Region: us-central1-a

### **2. Set Up VM**
```bash
# SSH into VM
gcloud compute ssh parallel-processing-vm --zone=us-central1-a

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
```bash
# Run serial baseline
python3 src/serial_baseline.py

# Run multiprocessing
python3 src/multiprocessing_image.py

# Run concurrent futures
python3 src/concurrent_futures.py

# Generate graphs
python3 src/create_graphs.py
```

### **5. Download Results**
```bash
# Create zip of results
zip -r results.zip results/

```

---

## 📊 Performance Results

### **Test Environment (GCP)**
- **Instance:** e2-standard-4
- **vCPUs:** 4
- **Memory:** 16 GB
- **OS:** Ubuntu 20.04 LTS
- **Images Tested:** 1,000 images (20 folders, 50 images per folder)
- **Total Tasks:** 5,000 (1,000 images × 5 filters)

### **Execution Time**

| Workers | Multiprocessing (s) | Concurrent Futures (s) |
|---------|---------------------|------------------------|
| 1       | 33.79              | 34.41                 |
| 2       | 17.17              | 17.37                 |
| 4       | 14.08              | 14.42                 |
| 8       | 14.11              | 14.57                 |

### **Speedup Analysis**

Formula: `Speedup(N) = T₁ ÷ Tₙ`

| Workers | Multiprocessing | Concurrent Futures |
|---------|-----------------|-------------------|
| 1       | 1.00x          | 1.00x            | 
| 2       | 1.97x          | 1.98x            | 
| 4       | 2.40x          | 2.39x            | 
| 8       | 2.39x          | 2.36x            | 

### **Parallel Efficiency**

Formula: `Efficiency(N) = [Speedup(N) ÷ N] × 100%`

| Workers | Multiprocessing | Concurrent Futures |
|---------|-----------------|-------------------|
| 1       | 100.0%         | 100.0%           |
| 2       | 98.5%          | 99.0%            |
| 4       | 60.0%          | 59.8%            |
| 8       | 29.9%          | 29.5%            |

---


## Implementation Details

### **Multiprocessing**
- Runs multiple processes simultaneously, bypassing Python's GIL (Global Interpreter Lock)
- Each process has its own independent memory space
- Uses `multiprocessing.Pool` to distribute tasks across workers
- Best suited for CPU-intensive operations like image processing

### **Concurrent.futures**
- Uses `ProcessPoolExecutor` for high-level process management
- Implements Future objects for asynchronous task execution
- Provides cleaner code structure and better error handling
- Slightly more overhead but easier to work with

**Performance Comparison:** 
-Both approaches achieve similar results, with multiprocessing being marginally faster (~0.3-0.4s) due to lower abstraction overhead.
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

1. [Python Multiprocessing Documentation](https://docs.python.org/3/library/multiprocessing.html)
2. [Python Concurrent.futures Documentation](https://docs.python.org/3/library/concurrent.futures.html)
3. Amdahl, G. M. (1967). "Validity of the single processor approach"
4. [Google Cloud Platform Documentation](https://cloud.google.com/compute/docs)

---

## Video Demonstration

**YouTube Link:** [Insert link here]

---

## 📝 License

This project is for academic purposes as part of CST435: Parallel and Cloud Computing course.

---

