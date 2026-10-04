# Performance Analysis

## Test Configuration

To ensure strict experimental validity and parity between environments, both virtual machines were provisioned with identical system hardware specifications:

| Parameter | Configuration Specification |
|---|---|
| Guest Operating System | Ubuntu 24.04 LTS (x86_64) |
| Virtual Processors (vCPU) | 2 Cores |
| System Memory (RAM) | 2 GB (2048 MB) |
| Storage Allocation | 20 GB Virtual Disk |

## Benchmark Command

The CPU prime calculation stress test was executed utilizing the standardized Sysbench benchmark tool across both virtual machines:

```bash
sysbench cpu --cpu-max-prime=20000 run
```

## Results

The recorded empirical metrics for the 10-second prime integer computation window:

| Metric | Proxmox VE (Type-1) | VMware Workstation (Type-2) |
|---|---|---|
| Total Execution Time | 10.0012 s | 10.0016 s |
| Total Events Completed | 17,169 | 13,650 |
| Events per Second (EPS) | 1,716.69 | 1,364.78 |
| Average Latency | 0.58 ms | 0.73 ms |

## Analysis

An analysis of the collected telemetry highlights distinct performance characteristics attributable to the architectural layers of each virtualization model:

1. **Duration Compliance:** Both benchmarking runs executed for precisely 10 seconds under the control of Sysbench's default time limit, guaranteeing identical testing intervals.
2. **Computational Throughput:** The bare-metal Type-1 hypervisor (Proxmox VE) finalized 17,169 prime calculation events compared to 13,650 events in VMware Workstation. This translates to an empirical throughput advantage of +25.78% (1,716.69 EPS vs 1,364.78 EPS), demonstrating higher instruction processing efficiency when running directly atop physical hardware without host OS interception.
3. **Execution Latency:** Proxmox VE registered a substantially reduced average latency of 0.58 ms per event relative to VMware Workstation's 0.73 ms per event—representing a 20.55% reduction in latency overhead. The hosted architecture of VMware Workstation experiences additional scheduling indirection due to the underlying Windows host OS kernel scheduler.

## Observation

The empirical evaluation confirms that under identical resource quotas (2 vCPUs, 2 GB RAM, 20 GB Disk), the Type-1 bare-metal hypervisor (Proxmox VE) delivers noticeably superior throughput and reduced processing latency over the Type-2 hosted hypervisor (VMware Workstation). The absence of an intermediate host operating system minimizes context-switching penalties, VM-exit latencies, and CPU scheduling contention.
