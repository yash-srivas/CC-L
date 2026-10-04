# Cloud Computing Lab

A technical repository housing practical implementations, benchmark methodologies, and empirical performance evaluations conducted for the **Cloud Computing Laboratory** course.

---

## 🔬 Laboratory Experiments

| Experiment | Focus Area | Status |
|---|---|---|
| **Experiment 1** | Performance Analysis of Type-1 and Type-2 Hypervisors | `Completed` |
| **Experiment 2** | Performance Analysis of Virtual Machines and Containers | `Completed` |

- 📄 **[View Experiment 1 Details](exp01-hypervisor-benchmarking/README.md)**  
- 📄 **[View Experiment 2 Details](exp02-container-benchmarking/README.md)**  

---

## 📌 Executive Summary of Modules

### 1. [Experiment 1: Hypervisor Performance Benchmarking](exp01-hypervisor-benchmarking/README.md)
An empirical evaluation comparing bare-metal (**Type-1: Proxmox VE / KVM**) and hosted (**Type-2: VMware Workstation Pro on Windows 11**) virtualization architectures under standardized computational stress.
- **Workload**: CPU prime number computation (20,000 primes) using `sysbench`.
- **Guest Configuration**: Ubuntu 24.04 LTS, 2 vCPUs, 2 GB RAM, 20 GB Virtual Disk.
- **Key Finding**: Proxmox VE demonstrated a **+25.78% throughput increase** (1,716.69 vs 1,364.78 EPS) and a **20.55% reduction in mean processing latency** (0.58 ms vs 0.73 ms) due to direct hardware scheduling without intermediate host operating system preemption.

### 2. [Experiment 2: Virtual Machines vs. Containers](exp02-container-benchmarking/README.md)
A comparative investigation evaluating hardware virtualization (VMware) against operating-system-level virtualization (**Docker Engine**) across four critical performance vectors.
- **Workloads**: Multi-threaded CPU baseline, memory bandwidth and latency (10 repeated runs), sequential and random block storage I/O (`fio`), and REST microservice performance (`FastAPI` + `ab`).
- **Resource Constraints**: Identical 4 vCPUs and 7.7 GiB RAM quotas enforced via Linux `cgroups v2`.
- **Key Finding**: Docker achieved near-native memory execution parity (-0.78% delta) and higher sequential disk throughput (+45.6%), while small-block random write operations highlighted Union File System (OverlayFS) Copy-on-Write overhead.

---

## 📁 Repository Organization

```text
my-repo/
├── README.md                                  # Repository overview and master index
│
├── exp01-hypervisor-benchmarking/             # Module 01: Hypervisor Benchmarking
│   ├── README.md                              # Complete experiment write-up and analysis
│   ├── generate_graphs.py                     # Script generating 8 publication-grade figures
│   ├── graphs/                                # Rendered high-resolution performance plots
│   ├── results/                               # Technical performance analysis notes
│   └── screenshots/                           # Proxmox, VMware, and comparative screenshots
│
└── exp02-container-benchmarking/              # Module 02: VM vs. Container Benchmarking
    ├── README.md                              # Complete experiment write-up and analysis
    ├── api/                                   # FastAPI benchmark application & Dockerfile
    ├── docker/                                # Standalone container build manifest
    ├── docs/                                  # Architecture, hardware specs, and methodology
    ├── results/                               # Raw stdout logs, processed CSVs, and figures
    └── scripts/                               # Data aggregation and visualization scripts
```

---

## 🛠️ Technology Stack & Environment

- **Hypervisors**: Proxmox VE 8.x (Bare-Metal KVM) | VMware Workstation Pro 17.x
- **Container Engine**: Docker Engine 27+ / containerd (cgroups v2, OverlayFS)
- **Guest OS**: Ubuntu 22.04 / 24.04 LTS (x86_64)
- **Benchmark Tools**: `sysbench` (CPU, Memory), `fio` (Block Storage), `ab` (HTTP)
- **Application Stack**: Python 3.12, FastAPI, Uvicorn
- **Data & Telemetry**: Pandas, Matplotlib, NumPy
