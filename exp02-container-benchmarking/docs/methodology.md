# Experimental Methodology & Benchmarking Protocol

## 1. Scope & Objective

The objective of this experimental framework is to conduct a standardized, scientifically rigorous performance comparison between hardware-assisted virtualization (Virtual Machine) and operating-system-level virtualization (Docker Container) under identical compute, memory, and storage constraints.

## 2. Experimental Environment & Parity Controls

### Host Infrastructure
- **Operating System**: Windows 11 Enterprise (64-bit)
- **Virtualization Layer**: VMware Workstation Pro 17.x
- **Host Hardware**: x86_64 architecture with hardware-assisted virtualization (Intel VT-x / AMD-V) enabled

### Guest Virtual Machine (Baseline Environment)
- **Operating System**: Ubuntu 22.04 LTS (x86_64)
- **Allocated vCPUs**: 4 Virtual Processor Cores
- **Allocated RAM**: 7.7 GiB (DDR4)
- **Virtual Disk**: 54 GB virtual SCSI disk

### Container Runtime (Docker)
- **Engine**: Docker Engine 27+ / containerd
- **Base Image**: Python 3.12-slim / Debian-based runtime
- **Cgroup Resource Ceilings**:
  - CPU Ceiling: `--cpus="4.0"` (Enforced via `cpu.max` in cgroups v2)
  - Memory Ceiling: `--memory="7.7g"` (Enforced via `memory.max` in cgroups v2)

---

## 3. Workload Protocols & Execution Parameters

### 3.1 CPU Computational Stress
- **Benchmark Suite**: Sysbench 1.0.20
- **Stress Mode**: Prime integer calculation up to 20,000
- **Thread Count**: 4 concurrent execution threads
- **Execution Limit**: 30 seconds

### 3.2 Memory Bandwidth & Allocation
- **Benchmark Suite**: Sysbench Memory Engine
- **Block Transfer Unit**: 1 MiB
- **Workload Volume**: 10 GiB per iteration
- **Concurrency**: 4 parallel threads
- **Repetition Protocol**: 10 sequential iterations per environment (VM vs Container)
- **Extracted Metrics**: Events per second, total execution runtime

### 3.3 Storage Block I/O Characterization
- **Benchmark Suite**: Flexible I/O Tester (`fio`)
- **Execution Duration**: 30 seconds per workload mode
- **Direct I/O**: `direct=1` (Bypasses OS page buffer to isolate storage driver latency)
- **I/O Queue Depth**: `iodepth=16`
- **Workload Profiles**:
  1. *Sequential Read*: 1 MiB block size, 2 GiB file allocation
  2. *Sequential Write*: 1 MiB block size, 2 GiB file allocation
  3. *Random Read*: 4 KiB block size, 2 GiB file allocation
  4. *Random Write*: 4 KiB block size, 2 GiB file allocation

### 3.4 REST Microservice Application Load
- **Application Engine**: FastAPI (ASGI asynchronous runtime)
- **Endpoints Profiled**:
  - `/health`: Static JSON diagnostic ping
  - `/compute`: Iterative sum-of-squares calculation (1,000,000 elements)
  - `/memory`: In-memory array generation (1,000,000 integers)
- **Load Generation Engine**: Apache Benchmark (`ab`)
  - *Health Endpoint*: 10,000 total requests, concurrency level 100
  - *Compute Endpoint*: 1,000 total requests, concurrency level 10
  - *Memory Endpoint*: 1,000 total requests, concurrency level 10

---

## 4. Telemetry Processing & Data Pipeline

1. **Standard Output Capture**: Unmodified terminal outputs are streamed directly into `results/raw/<domain>/`.
2. **Parsing & Metric Extraction**: The Python script `scripts/analyze_results.py` ingests raw logs, computes mean metrics, and generates structured CSV datasets under `results/processed/`.
3. **Visualization Generation**: `scripts/generate_plots.py` utilizes Matplotlib and Pandas to render publication-grade comparison figures stored in `results/figures/`.
