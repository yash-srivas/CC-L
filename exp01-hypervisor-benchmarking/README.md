# Experiment 1: Performance Analysis of Type-1 and Type-2 Hypervisors

## Aim

To conduct a comprehensive, empirical comparative performance evaluation of a Type-1 bare-metal hypervisor (Proxmox VE / KVM) and a Type-2 hosted hypervisor (VMware Workstation Pro) under identical guest operating system parameters and standardized CPU computational benchmarking workloads.

## Objectives

- Examine the architectural and operational distinctions between Type-1 bare-metal and Type-2 hosted virtualization.
- Deploy and configure an Ubuntu 24.04 LTS guest virtual machine on Proxmox VE.
- Provision and configure an identical Ubuntu 24.04 LTS guest virtual machine within VMware Workstation.
- Execute standardized Sysbench prime computation workloads to stress virtual processor cores.
- Capture real-time computational throughput, request latencies, and resource consumption telemetry.
- Synthesize comparative data to evaluate virtualization overhead, kernel scheduling preemption, and execution efficiency.

## Introduction

**Virtualization** forms the cornerstone of modern cloud and datacenter architecture by abstracting physical compute resources into multiple independent, isolated virtual execution environments.

A **Hypervisor**, commonly designated as a Virtual Machine Monitor (VMM), is the core software or firmware abstraction layer that orchestrates the execution of virtual machines (VMs) by partitioning and multiplexing underlying CPU, memory, and storage hardware.

- **Type-1 Hypervisor (Bare-Metal)**: Operates directly upon the host physical hardware without requiring a host operating system. By managing CPU virtualization extensions (Intel VT-x / AMD-V) and physical RAM directly via a dedicated kernel, it eliminates intermediate abstraction penalties. Prominent examples include Proxmox VE (KVM), VMware ESXi, and Microsoft Hyper-V Server.
- **Type-2 Hypervisor (Hosted)**: Runs as an application layer on top of a general-purpose host operating system (e.g., Windows 11, macOS, or Linux). System calls and hardware requests from guest virtual machines must traverse both the hypervisor VMM and the host OS kernel scheduler, incurring measurable virtualization overhead. Leading examples include VMware Workstation Pro, Oracle VM VirtualBox, and Parallels Desktop.

## Technologies Used

| Component | Technology Stack |
|---|---|
| Type-1 Hypervisor | Proxmox VE 8.x (KVM Kernel) |
| Type-2 Hypervisor | VMware Workstation Pro 17.x |
| Guest Operating System | Ubuntu Server 24.04 LTS (x86_64) |
| Benchmark Engine | Sysbench 1.0.20+ |
| Analysis & Plotting | Python 3, Matplotlib, NumPy |

## Experimental Configuration

| Parameter | Proxmox VE | VMware Workstation |
|---|---|---|
| Hypervisor Classification | Type-1 (Bare Metal) | Type-2 (Hosted) |
| Guest Operating System | Ubuntu 24.04 LTS | Ubuntu 24.04 LTS |
| Virtual Cores (vCPU) | 2 Cores | 2 Cores |
| Allocated Memory (RAM) | 2 GB (2048 MB) | 2 GB (2048 MB) |
| Storage Allocation | 20 GB Virtual Disk | 20 GB Virtual Disk |
| Benchmark Engine | Sysbench CPU Stress | Sysbench CPU Stress |
| Workload Complexity | Prime Calculation up to 20,000 | Prime Calculation up to 20,000 |

## Hypervisor Architecture

```mermaid
flowchart TD
    subgraph Type1["Type-1 Bare-Metal (Proxmox VE)"]
        HW1["Physical Bare-Metal Hardware"] --> HYP1["Proxmox VE / KVM Hypervisor"]
        HYP1 --> VM1["Ubuntu 24.04 Guest VM"]
        VM1 --> SB1["Sysbench CPU Engine"]
        SB1 --> MET1["Throughput: 1,716.69 EPS | Latency: 0.58 ms"]
    end

    subgraph Type2["Type-2 Hosted (VMware Workstation)"]
        HW2["Physical Bare-Metal Hardware"] --> HOST2["Host OS (Windows 11)"]
        HOST2 --> HYP2["VMware Workstation VMM"]
        HYP2 --> VM2["Ubuntu 24.04 Guest VM"]
        VM2 --> SB2["Sysbench CPU Engine"]
        SB2 --> MET2["Throughput: 1,364.78 EPS | Latency: 0.73 ms"]
    end
```

## Methodology

1. Create a dedicated virtual machine instance in the Proxmox VE web management console.
2. Allocate exactly 2 vCPUs, 2048 MB RAM, and 20 GB virtual disk storage as mandated by laboratory constraints.
3. Install and boot Ubuntu 24.04 LTS Server within the virtual instance.
4. Perform an initial system audit to verify hardware allocation using standard diagnostic utilities.
5. Install and verify the Sysbench benchmarking package via the Ubuntu package repository.
6. Execute the prime integer search benchmark (`--cpu-max-prime=20000`) and capture terminal telemetry.
7. Monitor CPU and memory utilization trends during workload execution.
8. Replicate the identical hardware configuration inside VMware Workstation Pro running on a Windows 11 host.
9. Execute the identical Sysbench benchmarking workload within the VMware guest environment.
10. Aggregate all empirical outputs, compute variance deltas, and produce comparative analytical graphs.

## Sysbench Command

```bash
sysbench cpu --cpu-max-prime=20000 run # Runs CPU test calculating primes up to 20,000
```

This instruction commands Sysbench to perform computational stress by verifying prime numbers up to an upper boundary of 20,000 using standard integer arithmetic. The benchmark accurately quantifies CPU throughput (events per second), total processed events, and transaction latencies under 10 seconds of continuous computational stress.

## Type-1 Hypervisor: Proxmox VE

The guest virtual machine was deployed directly within Proxmox Virtual Environment (VE). Utilizing the Linux Kernel-based Virtual Machine (KVM) module, hardware access is orchestrated directly by the underlying bare-metal kernel. The VM was configured with 2 virtual processing cores, 2 GB of physical RAM allocation, and 20 GB of disk storage.

The guest environment was validated using standard Linux administrative diagnostics:
```bash
hostnamectl # Shows system hostname, OS details, and architecture
lscpu       # Displays CPU architecture information and number of cores
free -h     # Shows available and used RAM in human-readable format
df -h       # Displays disk space usage for all mounted filesystems
top         # Real-time view of running processes and resource usage
```

Sysbench was installed via the native Advanced Package Tool (APT):
```bash
sudo apt update              # Updates the package list for the APT package manager
sudo apt install sysbench -y # Installs the Sysbench tool automatically
sysbench --version           # Verifies the installation by checking the installed version
```

Following package verification, the CPU evaluation run was initiated:
```bash
sysbench cpu --cpu-max-prime=20000 run # Runs CPU test calculating primes up to 20,000
```

### Type-1 Screenshots

#### Proxmox Dashboard
![Proxmox Dashboard](screenshots/type1-proxmox/01-proxmox-dashboard.png)

#### VM Configuration
![VM Configuration](screenshots/type1-proxmox/02-proxmox-vm-configuration.png)

#### VM Running
![VM Running](screenshots/type1-proxmox/03-proxmox-vm-running.png)

#### Ubuntu Console
![Ubuntu Console](screenshots/type1-proxmox/04-proxmox-ubuntu-console.png)

#### System Configuration
![System Configuration](screenshots/type1-proxmox/05-proxmox-system-configuration.png)

#### Sysbench Result
![Sysbench Result](screenshots/type1-proxmox/06-proxmox-sysbench-result.png)

#### Resource Monitoring
![Resource Monitoring](screenshots/type1-proxmox/07-proxmox-resource-monitoring.png)

## Type-2 Hypervisor: VMware Workstation

An equivalent Ubuntu virtual machine was constructed within VMware Workstation Pro, hosted atop Windows 11. To preserve strict experimental parity, the guest machine received matching hardware allocations: 2 vCPUs, 2 GB RAM, and a 20 GB virtual disk. System configurations were verified with the identical Linux inspection utilities, and Sysbench was invoked using the exact same benchmark parameters.

### Type-2 Screenshots

#### VMware VM Configuration
![VMware VM Configuration](screenshots/type2-vmware/01-vmware-vm-configuration.png)

#### VMware VM Running
![VMware VM Running](screenshots/type2-vmware/02-vmware-vm-running.png)

#### VMware System Configuration
![VMware System Configuration](screenshots/type2-vmware/03-vmware-system-configuration.png)

#### VMware Sysbench Result
![VMware Sysbench Result](screenshots/type2-vmware/04-vmware-sysbench-result.png)

## Performance Results

| Metric | Proxmox VE (Type-1) | VMware Workstation (Type-2) |
|---|---|---|
| Total Execution Time | 10.0012 s | 10.0016 s |
| Total Events Completed | 17,169 | 13,650 |
| Events per Second (Throughput) | 1,716.69 | 1,364.78 |
| Average Latency | 0.58 ms | 0.73 ms |

## Generated Graphs

Here are the visual representations of the performance data generated for this experiment:

### Architecture Comparison
![Hypervisor Architecture](graphs/01_hypervisor_architecture.png)

### Events per Second Comparison
![Events per Second](graphs/02_events_per_second.png)

### Total Events and Time per Event
![Total Events and Time per Event](graphs/03_total_events_and_time_per_event.png)

### Average Latency Comparison
![Average Latency Comparison](graphs/04_latency_comparison.png)

### Latency Consistency
![Latency Consistency](graphs/05_latency_consistency.png)

### Relative Performance
![Relative Performance](graphs/06_relative_performance.png)

### Type-2 VM Resources
![Type-2 VM Resources](graphs/07_type2_vm_resources.png)

### Performance Summary Dashboard
![Performance Summary Dashboard](graphs/08_summary_dashboard.png)

## Performance Analysis

A comparative review of the empirical measurements recorded across both virtualization engines reveals notable architectural consequences:

- **Execution Duration Parity:** Both testing environments strictly obeyed Sysbench's 10-second default benchmark run duration (~10.001s), providing a rigorous apples-to-apples basis for throughput comparison.
- **Throughput & Total Events:** The Type-1 hypervisor (Proxmox VE) achieved 17,169 total events, yielding a throughput of 1,716.69 events per second. In comparison, VMware Workstation recorded 13,650 events with 1,364.78 events per second. Proxmox demonstrated a **+25.78% throughput increase** over VMware Workstation.
- **Latency Distribution:** Proxmox VE maintained a lower mean processing latency of 0.58 ms compared to 0.73 ms on VMware Workstation, reflecting a **20.55% latency reduction**. This improvement stems from direct virtual processor execution without intervening Windows kernel thread preemption.

### Comparison Screenshot

![Hypervisor Performance Comparison](screenshots/comparison/01-hypervisor-performance-comparison.png)

## Observations

- The Type-1 hypervisor (Proxmox VE) exhibited substantial computational throughput advantages across prime number calculation tests.
- Proxmox VE achieved consistently faster turnaround per instruction event, with negligible scheduling jitter.
- The Type-2 hypervisor (VMware Workstation), while robust and successful in completing the full test workload, incurred noticeable latency overhead due to the dual scheduler hierarchy (host OS kernel plus VMM scheduler).
- The observed data illustrates the fundamental penalty of hosted virtualization: hardware virtualization traps and privileged guest operations must be intermediated through host OS APIs, creating CPU cycles lost to context switching.

## Conclusion

This experiment successfully established and validated a benchmark-driven performance comparison between Type-1 bare-metal (Proxmox VE) and Type-2 hosted (VMware Workstation) hypervisors. The empirical telemetry proves that the Type-1 architecture delivers approximately 25.78% higher computational throughput and 20.55% lower mean processing latency under identical virtual machine hardware allocations.

## Repository Structure

```text
exp01-hypervisor-benchmarking/
│
├── README.md
├── generate_graphs.py
│
├── screenshots/
│   ├── type1-proxmox/
│   │   ├── 01-proxmox-dashboard.png
│   │   ├── 02-proxmox-vm-configuration.png
│   │   ├── 03-proxmox-vm-running.png
│   │   ├── 04-proxmox-ubuntu-console.png
│   │   ├── 05-proxmox-system-configuration.png
│   │   ├── 06-proxmox-sysbench-result.png
│   │   └── 07-proxmox-resource-monitoring.png
│   │
│   ├── type2-vmware/
│   │   ├── 01-vmware-vm-configuration.png
│   │   ├── 02-vmware-vm-running.png
│   │   ├── 03-vmware-system-configuration.png
│   │   └── 04-vmware-sysbench-result.png
│   │
│   └── comparison/
│       └── 01-hypervisor-performance-comparison.png
│
├── graphs/
│   ├── 01_hypervisor_architecture.png
│   ├── 02_events_per_second.png
│   ├── 03_total_events_and_time_per_event.png
│   ├── 04_latency_comparison.png
│   ├── 05_latency_consistency.png
│   ├── 06_relative_performance.png
│   ├── 07_type2_vm_resources.png
│   └── 08_summary_dashboard.png
│
└── results/
    └── performance-analysis.md
```

## References

- Cloud Computing Laboratory Manual & Benchmark Guidelines
- Sysbench Manual: Automated System Performance Benchmarking
