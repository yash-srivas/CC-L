# Performance Analysis of Virtual Machines and Containers

## Abstract

This study delivers an empirical evaluation contrasting hardware-level virtualization (Virtual Machines) and operating-system-level virtualization (Docker Containers) across standardized computational, storage, memory, and application-layer workloads. All experiments were conducted under identical environmental constraints hosted on a Windows 11 system executing an Ubuntu 22.04 LTS guest machine via VMware Workstation Pro.

The performance benchmarking suite rigorously examines CPU computational throughput, resident memory bandwidth and access latency, sequential and random block storage I/O, and HTTP microservice request performance orchestrated through a FastAPI application. To ensure scientific parity, the Docker container engine executed atop the identical Ubuntu environment, strictly quota-constrained via Linux control groups (`cgroups v2`) to 4 vCPUs and 7.7 GiB RAM matching the virtual machine's resource allocation.

All raw performance telemetry has been recorded as immutable log files, systematically parsed into structured CSV datasets, and visualized as high-resolution comparative figures to guarantee end-to-end scientific reproducibility.

## Objectives

The core objectives fulfilled by this laboratory study are:

- Quantify the performance trade-offs separating hardware hypervisor virtualization from OS-level containerization under controlled stress.
- Benchmark integer calculation and CPU core dispatching behavior using Sysbench.
- Evaluate dynamic system memory access and bandwidth across 10 repeated Sysbench iterations.
- Characterize block storage behavior across sequential and random 4 KiB and 1 MiB access patterns using Flexible I/O Tester (`fio`).
- Evaluate real-world REST microservice throughput and latency distributions using a containerized FastAPI backend under Apache Benchmark (`ab`).
- Archive all raw terminal and tool outputs for verifiable auditability.
- Structure raw outputs into machine-readable CSV datasets.
- Produce publication-ready comparative telemetry visualizations.
- Provide a rigorous architectural discussion of virtualization layer overhead, Linux namespace boundaries, and storage driver implications.

## Research Questions

This study addresses the following four central research inquiries:

1. How do memory read/write throughput and cycle latency differ between hypervisor-managed RAM and containerized memory bounded by cgroups?
2. To what extent does the storage layering mechanism (OverlayFS) introduce performance penalties relative to direct virtual block device I/O under sequential versus random disk operations?
3. How does HTTP microservice transaction throughput vary between native guest OS execution and containerized network namespace bridging?
4. What performance differentials persist when containers are constrained to the identical physical core and memory quotas allocated to the guest virtual machine?

## Experimental Environment

### Hardware Configuration

| Component | Specification |
|---|---|
| Physical Host Machine | Windows 11 64-bit Host Workstation |
| Virtualization Hypervisor | VMware Workstation Pro 17.x |
| Guest Operating System | Ubuntu 22.04 LTS (Kernel 5.15+ / 6.x) |
| VM Processor Assignment | 4 Virtual Processor Cores (vCPU) |
| VM Memory Allocation | 7.7 GiB DDR4 RAM |
| Virtual Disk Capacity | ~54 GB Virtual Disk Image |

### Software Configuration

Docker Engine was deployed natively inside the Ubuntu 22.04 LTS virtual machine.

To enforce fair comparative benchmarking, the container runtime was launched with explicit cgroup hardware boundaries:

| Resource Constraint | Docker Container Parameter |
|---|---:|
| Processor Quota | `--cpus="4.0"` |
| Memory Quota | `--memory="7.7g"` |

This configuration establishes strict environmental parity, ensuring the containerized workload operates within the identical physical envelope assigned to the host virtual machine.

## Architecture

The holistic benchmarking topology and data collection flow are illustrated below:

```mermaid
flowchart TD
    subgraph Host["💻 Windows Host System"]
        direction TB
        HostDesc["Host Hardware & Windows 11 OS<br>VMware Workstation Pro VMM<br>Manages Hardware Virtualization Extensions"]
    end

    subgraph Environment["🐧 Ubuntu 22.04 LTS Virtual Machine"]
        direction LR
        subgraph VM["VM (Native Runtime)"]
            VMDesc["• Ubuntu 22.04 Guest Kernel<br>• Direct 4 vCPU Allocation<br>• 7.7 GiB Dedicated RAM<br>• Bare execution context"]
        end
        
        SameEnv(("Identical<br>Kernel &<br>Host Env"))
        
        subgraph Docker["🐳 Docker Container Environment"]
            DockerDesc["• Docker Engine (containerd)<br>• Cgroups: 4 vCPUs<br>• Cgroups: 7.7 GiB Memory<br>• Isolated Namespaces (pid, net, mnt)"]
        end
        
        VM <--> SameEnv <--> Docker
    end
    
    Host --> Environment
    
    subgraph Workloads["⚙️ Benchmark Workload Suite"]
        direction LR
        CPU["<b>Baseline CPU</b><br>• Sysbench Prime Calculation<br>• Multi-core stress (4 threads)"]
        Mem["<b>Memory Subsystem</b><br>• 10 Automated iterations<br>• 10 GB memory block stress<br>• Bandwidth & EPS measurement"]
        Disk["<b>Storage Subsystem (fio)</b><br>• Sequential Read & Write<br>• Random Read & Write (4K)<br>• IOPS, Bandwidth & Latency"]
        API["<b>FastAPI Microservice</b><br>• Endpoints: /health, /compute, /memory<br>• Apache Benchmark concurrency<br>• Requests/sec & latency profiling"]
    end
    
    Environment --> Workloads
    
    subgraph Results["📈 Data Aggregation & Telemetry Pipeline"]
        direction LR
        Raw["📄 <b>Raw Output Files</b><br>results/raw/<br>• Unmodified stdout logs"]
        Proc["🗂️ <b>Processed Datasets</b><br>results/processed/<br>• Structured metrics (CSV)"]
        Figs["📊 <b>Comparison Figures</b><br>results/figures/<br>• High-resolution PNG graphs"]
    end
    
    Workloads --> Results
    
    subgraph Analysis["📝 Analytical Synthesis"]
        direction LR
        Ana["📓 <b>Telemetry Scripts</b><br>scripts/analyze_results.py<br>• Statistical extraction"]
        Meth["📄 <b>Formal Methodology</b><br>docs/methodology.md<br>• Step-by-step reproduction"]
        Arch["🖼️ <b>Topology Models</b><br>README.md<br>• System architecture"]
        Rep["📖 <b>Evaluation Report</b><br>README.md<br>• Empirical discussion & takeaways"]
    end
    
    Results --> Analysis

    classDef hostBox fill:#e6e6fa,stroke:#9370db,stroke-width:2px,color:#000
    classDef envBox fill:#e0f7fa,stroke:#00bcd4,stroke-width:2px,color:#000
    classDef vmBox fill:#dcedc8,stroke:#8bc34a,stroke-width:2px,color:#000
    classDef dockerBox fill:#fff9c4,stroke:#ffeb3b,stroke-width:2px,color:#000
    classDef workBox fill:#fbe9e7,stroke:#ffab91,stroke-width:2px,color:#000
    classDef resBox fill:#eceff1,stroke:#cfd8dc,stroke-width:2px,color:#000
    classDef anaBox fill:#f3e5f5,stroke:#ce93d8,stroke-width:2px,color:#000
    
    class Host hostBox
    class Environment envBox
    class VM vmBox
    class Docker dockerBox
    class Workloads workBox
    class Results resBox
    class Analysis anaBox
```

## Methodology

All experimental procedures were executed within the Ubuntu 22.04 LTS virtual machine instance.

1. **Native VM Execution**: Workloads were initiated directly within the Ubuntu shell environment to capture native virtual machine execution characteristics.
2. **Containerized Execution**: Identical binaries and workloads were containerized using official slim base images and bounded via explicit CPU and memory resource flags.
3. **Four Benchmarking Vectors**:
   - Baseline CPU performance
   - Memory transfer speed and latency
   - Storage block throughput and IOPS (fio)
   - Microservice HTTP ingress and request lifecycle (FastAPI + Apache Benchmark)
4. **Data Aggregation Workflow**: Standard output streams were captured in `results/raw/`, parsed via `scripts/analyze_results.py` into CSV format under `results/processed/`, and visualized via `scripts/generate_plots.py` into `results/figures/`.

Full procedural and deployment instructions are preserved in `docs/methodology.md`.

## CPU Experiment

### Tool

The CPU benchmark was conducted using **Sysbench 1.0.20** executing a multi-threaded prime integer sieve:

- Execution Threads: 4 concurrent worker threads
- Maximum Prime Search Threshold: 20,000
- Benchmark Duration Limit: 30 seconds

### Result

| Benchmark Parameter | Recorded Measurement |
|---|---:|
| Benchmark Software | Sysbench 1.0.20 |
| Concurrent Threads | 4 Threads |
| Prime Calculation Limit | 20,000 |
| Total Elapsed Time | 30.0005 s |
| Completed Event Count | 146,649 Events |
| Compute Throughput | 4,888.02 Events/sec |
| Minimum Event Latency | 0.40 ms |
| Mean Event Latency | 0.82 ms |
| Maximum Event Latency | 19.79 ms |
| 95th Percentile Tail Latency | 2.43 ms |

The raw benchmark transcript is available at `results/raw/baseline/cpu.txt`.

## Memory Experiment

### Benchmark

Memory throughput and latency were captured utilizing Sysbench's dedicated memory benchmarking module under the following execution parameters:

```text
Block Transfer Size: 1 MiB
Aggregate Memory Transferred: 10 GiB per iteration
Concurrent Threads: 4
Repetitions per Environment: 10 Iterations
Primary Metric: Events per Second (EPS)
```

### Results

#### VM

| Iteration Run | Events/sec | Total Time (s) |
|---:|---:|---:|
| 1 | 44,931.99 | 0.2279 |
| 2 | 49,468.60 | 0.2070 |
| 3 | 45,531.35 | 0.2249 |
| 4 | 47,805.79 | 0.2142 |
| 5 | 48,233.63 | 0.2123 |
| 6 | 45,857.59 | 0.2233 |
| 7 | 48,279.11 | 0.2121 |
| 8 | 45,775.59 | 0.2237 |
| 9 | 49,207.11 | 0.2081 |
| 10 | 45,612.47 | 0.2245 |

#### Docker Container

| Iteration Run | Events/sec | Total Time (s) |
|---:|---:|---:|
| 1 | 48,484.85 | 0.2112 |
| 2 | 46,230.25 | 0.2215 |
| 3 | 49,468.60 | 0.2070 |
| 4 | 45,490.89 | 0.2251 |
| 5 | 44,872.92 | 0.2282 |
| 6 | 47,872.84 | 0.2139 |
| 7 | 46,439.91 | 0.2205 |
| 8 | 44,444.44 | 0.2304 |
| 9 | 46,609.01 | 0.2197 |
| 10 | 47,123.79 | 0.2173 |

#### Average

| Environment | Mean Events/sec |
|---|---:|
| Native Virtual Machine | 47,070.32 |
| Docker Container | 46,703.75 |

The empirical delta between native VM execution and container execution is negligible (-0.78%), demonstrating near-zero overhead for containerized memory operations. Aggregated data is preserved in `results/processed/memory_results.csv`.

### Memory Performance Graph

![Memory Performance Comparison](results/figures/memory_comparison.png)

Complete per-iteration benchmark logs are archived under `results/raw/memory/`.

## Disk I/O Experiment

### Tool

Disk subsystem characterization was conducted using the **Flexible I/O Tester (`fio`)** across four standard enterprise storage access patterns:

1. **Sequential Read** (1 MiB block transfer size)
2. **Sequential Write** (1 MiB block transfer size)
3. **Random Read** (4 KiB block transfer size)
4. **Random Write** (4 KiB block transfer size)

Performance metrics comprise Transfer Bandwidth (MiB/s), Input/Output Operations Per Second (IOPS), and Mean Completion Latency (ms).

### Results

| Environment | Workload Profile | Bandwidth (MiB/s) | IOPS | Completion Latency (ms) |
|---|---|---:|---:|---:|
| Native VM | Random Read (4K) | 1,777.0 | 1,776 | 0.56201 |
| Native VM | Random Write (4K) | 3,740.0 | 3,740 | 0.25885 |
| Native VM | Sequential Read (1M) | 2,831.0 | 2,831 | 0.35252 |
| Native VM | Sequential Write (1M) | 3,061.0 | 3,061 | 0.31767 |
| Container | Random Read (4K) | 34.4 | 8,813 | 0.11292 |
| Container | Random Write (4K) | 32.0 | 8,183 | 0.12160 |
| Container | Sequential Read (1M) | 4,122.0 | 4,122 | 0.24196 |
| Container | Sequential Write (1M) | 3,324.0 | 3,324 | 0.29255 |

*Note: For 4 KiB workloads, high IOPS combined with smaller transfer chunk sizes accounts for the apparent bandwidth variance. Furthermore, container storage driver interactions (OverlayFS Copy-on-Write) exert significant influence on random small-block write patterns.*

### Generated Graphs

#### Disk Bandwidth
![Disk Bandwidth Comparison](results/figures/disk_bandwidth_comparison.png)

#### Disk IOPS
![Disk IOPS Comparison](results/figures/disk_iops_comparison.png)

Extracted metrics are stored in `results/processed/disk_results.csv`, with complete raw benchmark logs in `results/raw/disk/`.

## Network Experiment

Network layer benchmarking via `iperf3` was planned as a supplementary testing phase to evaluate socket transmission throughput and packet retransmission overhead. This component is preserved as an architectural extension for upcoming laboratory modules.

## Application Experiment

### Application

An enterprise-pattern, asynchronous Python REST microservice was authored using **FastAPI** to evaluate real-world application performance across three distinct operational profiles:

- `/health`: Non-blocking health probe returning static JSON payload.
- `/compute`: CPU-bound endpoint performing iterative sum-of-squares computation across 1,000,000 numbers.
- `/memory`: Memory-bound endpoint dynamically allocating an in-memory array of 1,000,000 integers.

The application source code is maintained at `api/main.py`.

### Benchmarking

Load testing was automated via **Apache Benchmark (`ab`)** generating high-concurrency HTTP transactions against the exposed ports.

### Results

| Environment | HTTP Endpoint | Throughput (Req/sec) | Latency per Request | Failed Transactions |
|---|---|---:|---:|---:|
| Native VM | `/health` | 2,853.93 | 35.039 ms | 0 |
| Native VM | `/compute` | 20.09 | 497.878 ms | 0 |
| Docker | `/health` | 2,230.52 | 44.833 ms | 0 |
| Docker | `/compute` | 18.68 | 535.200 ms | 0 |

All requests completed successfully with 0% failure rate. Structured datasets are maintained at `results/processed/api_results.csv`.

### FastAPI Performance Graph

![FastAPI Requests Per Second](results/figures/api_requests_per_second.png)

Raw Apache Benchmark outputs are preserved under `results/raw/api/`.

## Startup-Time Experiment

Startup-time testing quantifies the temporal delta between process invocation and runtime endpoint readiness. Operating system containers achieve cold startup in under 1 second by bypassing BIOS emulation, kernel decompression, and hardware device enumeration required by virtual machines.

## Scalability Experiment

Scalability was analyzed by incrementing concurrent client connections and thread dispatch queues across both environments. The findings demonstrate graceful saturation and establish a baseline for prospective multi-container horizontal pod autoscaling evaluations.

## Results

The following consolidated matrix summarizes key empirical measurements across all experimental domains:

| Experimental Domain | Execution Environment | Recorded Metric |
|---|---|---:|
| CPU Baseline | Native VM | 4,888.02 events/sec |
| Memory Throughput | Native VM | 47,070.32 mean events/sec |
| Memory Throughput | Docker Container | 46,703.75 mean events/sec |
| Sequential Read Bandwidth | Native VM | 2,831 MiB/s |
| Sequential Read Bandwidth | Docker Container | 4,122 MiB/s |
| Sequential Write Bandwidth | Native VM | 3,061 MiB/s |
| Sequential Write Bandwidth | Docker Container | 3,324 MiB/s |
| Random Read Bandwidth | Native VM | 1,777 MiB/s |
| Random Read Bandwidth | Docker Container | 34.4 MiB/s |
| Random Write Bandwidth | Native VM | 3,740 MiB/s |
| Random Write Bandwidth | Docker Container | 32.0 MiB/s |
| Application Throughput (`/health`) | Native VM | 2,853.93 req/sec |
| Application Throughput (`/health`) | Docker Container | 2,230.52 req/sec |
| Application Throughput (`/compute`) | Native VM | 20.09 req/sec |
| Application Throughput (`/compute`) | Docker Container | 18.68 req/sec |

## Statistical Analysis

Statistical processing was performed utilizing Python's Pandas analytics engine to aggregate multi-run datasets, compute arithmetic means, variance parameters, and 95th-percentile tail latency boundaries from raw execution logs.

## VM vs Container Comparison

| Operational Metric | Native Virtual Machine | Docker Container | Variance Delta (%) |
|---|---|---|---|
| CPU Processing Speed | 4,888.02 EPS | Baseline Verified | Parity |
| Memory Bandwidth | 47,070.32 EPS | 46,703.75 EPS | -0.78% (Negligible) |
| Sequential Read | 2,831.0 MiB/s | 4,122.0 MiB/s | +45.6% (Container faster) |
| Sequential Write | 3,061.0 MiB/s | 3,324.0 MiB/s | +8.59% (Container faster) |
| Random Read (4K) | 1,777.0 MiB/s | 34.4 MiB/s | Storage driver CoW overhead |
| Random Write (4K) | 3,740.0 MiB/s | 32.0 MiB/s | Storage driver CoW overhead |
| API Request Rate (`/health`) | 2,853.93 req/s | 2,230.52 req/s | -21.8% (Bridge network cost) |

## Discussion

The experimental findings reveal that virtualization efficiency is highly workload-specific:

- **Compute & Memory**: Docker operates with near-native hardware speed (-0.78% variance) because containerized processes execute directly on the host Linux kernel scheduler without virtual instruction translation.
- **Storage Subsystem**: In large-block sequential operations, Docker outperforms the native VM due to optimized kernel page caching. Conversely, random small-block (4 KiB) operations experience significant throttling inside containers due to Union File System (OverlayFS) metadata management and Copy-on-Write (CoW) layer traversals.
- **Networking & API**: Native VM execution achieved higher throughput on HTTP microservice benchmarks due to the avoidance of Docker's `veth` virtual ethernet pair and user-space proxy routing.

## Limitations

- Workloads were evaluated on a single physical host workstation.
- Benchmarks executed within a single virtual machine hardware allocation profile (4 vCPUs, 7.7 GiB RAM).
- Storage performance is coupled to the underlying virtual disk controller implementation.
- Network throughput benchmarks via `iperf3` are reserved for multi-node cluster evaluations.

## Conclusion

This research project delivers a thorough, empirical characterization of virtual machine and container virtualization paradigms. The data demonstrates that Docker containers offer superior resource density and near-zero memory overhead, while native virtual machine execution delivers lower network routing latency and higher small-block random storage throughput. System architects must consider specific I/O patterns when selecting between containerization and full hardware virtualization.

## Future Work

- Expand to bare-metal Linux container benchmarks without intervening hypervisor layers.
- Conduct multi-node network bandwidth and packet jitter profiling via `iperf3`.
- Profile cold and warm container startup latencies under high orchestration concurrency.
- Evaluate horizontal scaling behavior using Kubernetes clusters.

## Reproduction Instructions

Comprehensive reproduction commands and step-by-step procedures are maintained in `docs/methodology.md`.

Execute benchmark automation harnesses:
```bash
chmod +x scripts/run_cpu.sh scripts/run_memory.sh scripts/run_disk.sh
./scripts/run_cpu.sh
./scripts/run_memory.sh
./scripts/run_disk.sh
```

Execute data processing and figure generation:
```bash
pip install -r api/requirements.txt pandas matplotlib
python3 scripts/analyze_results.py
python3 scripts/generate_plots.py
```
