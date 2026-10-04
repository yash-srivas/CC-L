import matplotlib.pyplot as plt
import numpy as np
import os

# ==============================================================================
# Empirical Benchmark Telemetry: Type-1 (Proxmox VE) vs Type-2 (VMware Workstation)
# Workload: Sysbench CPU prime calculation (max-prime=20,000, 2 vCPUs, 2 GB RAM)
# ==============================================================================

hypervisors = ['Proxmox VE (Type-1)', 'VMware Workstation (Type-2)']
total_events = [17169, 13650]
events_per_second = [1716.69, 1364.78]
avg_latency = [0.58, 0.73]
exec_time = [10.0012, 10.0016]

# Create output graphs directory
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphs')
os.makedirs(output_dir, exist_ok=True)

# Visual styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
colors = ['#1e40af', '#d97706']  # Classic Navy Blue and Amber Orange

# ------------------------------------------------------------------------------
# 1. 01_hypervisor_architecture.png
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 6), dpi=300)
ax.axis('off')
ax.text(0.5, 0.85, 'Type-1 Hypervisor Architecture (Proxmox VE / KVM)', 
        ha='center', va='center', fontsize=13, weight='bold', 
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#dbeafe', edgecolor='#1e40af', lw=1.5))
ax.text(0.5, 0.65, 'Physical Hardware  ──>  Bare-Metal Hypervisor (KVM)  ──>  Guest Ubuntu VM', 
        ha='center', va='center', fontsize=11, family='monospace',
        bbox=dict(boxstyle='square,pad=0.5', facecolor='#f8fafc', edgecolor='#cbd5e1'))

ax.text(0.5, 0.35, 'Type-2 Hypervisor Architecture (VMware Workstation)', 
        ha='center', va='center', fontsize=13, weight='bold', 
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#fef3c7', edgecolor='#d97706', lw=1.5))
ax.text(0.5, 0.15, 'Physical Hardware  ──>  Host OS (Win 11)  ──>  VMware VMM  ──>  Guest Ubuntu VM', 
        ha='center', va='center', fontsize=11, family='monospace',
        bbox=dict(boxstyle='square,pad=0.5', facecolor='#f8fafc', edgecolor='#cbd5e1'))

plt.title('Hypervisor Architecture & Layering Comparison', fontsize=15, weight='bold', pad=20)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '01_hypervisor_architecture.png'), dpi=300)
plt.close()

# ------------------------------------------------------------------------------
# 2. 02_events_per_second.png
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
bars = ax.bar(hypervisors, events_per_second, color=colors, width=0.45, edgecolor='#0f172a', linewidth=1.2)
ax.set_ylabel('Events per Second (Throughput)', fontsize=12, fontweight='bold')
ax.set_title('CPU Computational Throughput Comparison', fontsize=14, fontweight='bold', pad=15)
ax.set_ylim(0, 2100)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 35, f"{yval:,.2f} EPS", ha='center', va='bottom', fontsize=11, fontweight='bold')
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '02_events_per_second.png'), dpi=300)
plt.close()

# ------------------------------------------------------------------------------
# 3. 03_total_events_and_time_per_event.png
# ------------------------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(8.5, 6), dpi=300)
ax2 = ax1.twinx()
x = np.arange(len(hypervisors))
width = 0.35

bars1 = ax1.bar(x - width/2, total_events, width, label='Total Events Completed', color='#2563eb', edgecolor='#1e3a8a')
bars2 = ax2.bar(x + width/2, avg_latency, width, label='Mean Latency (ms)', color='#f59e0b', edgecolor='#b45309')

ax1.set_ylabel('Total Events Completed (in 10s)', color='#2563eb', fontsize=11, fontweight='bold')
ax2.set_ylabel('Average Latency (ms)', color='#d97706', fontsize=11, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(hypervisors, fontsize=11, fontweight='bold')
ax1.set_ylim(0, 22000)
ax2.set_ylim(0, 1.1)

for bar in bars1:
    h = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, h + 300, f"{int(h):,}", ha='center', va='bottom', fontsize=10, fontweight='bold', color='#1e3a8a')
for bar in bars2:
    h = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, h + 0.02, f"{h:.2f} ms", ha='center', va='bottom', fontsize=10, fontweight='bold', color='#b45309')

ax1.set_title('Total Workload Events vs Execution Latency', fontsize=14, fontweight='bold', pad=15)
fig.legend(loc='upper right', bbox_to_anchor=(0.88, 0.88))
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '03_total_events_and_time_per_event.png'), dpi=300)
plt.close()

# ------------------------------------------------------------------------------
# 4. 04_latency_comparison.png
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
bars = ax.bar(hypervisors, avg_latency, color=['#10b981', '#ef4444'], width=0.45, edgecolor='#0f172a', linewidth=1.2)
ax.set_ylabel('Average Latency (ms)', fontsize=12, fontweight='bold')
ax.set_title('Average Event Latency (Lower is Better)', fontsize=14, fontweight='bold', pad=15)
ax.set_ylim(0, 1.0)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.02, f"{yval:.2f} ms", ha='center', va='bottom', fontsize=11, fontweight='bold')
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '04_latency_comparison.png'), dpi=300)
plt.close()

# ------------------------------------------------------------------------------
# 5. 05_latency_consistency.png
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
ax.plot(hypervisors, avg_latency, marker='o', linestyle='-', color='#7c3aed', markersize=10, linewidth=2.5, label='Mean Latency')
ax.set_ylabel('Latency (ms)', fontsize=12, fontweight='bold')
ax.set_title('Latency Consistency & Trend', fontsize=14, fontweight='bold', pad=15)
ax.set_ylim(0.4, 0.9)
for i, txt in enumerate(avg_latency):
    ax.annotate(f"{txt:.2f} ms", (hypervisors[i], avg_latency[i] + 0.02), ha='center', fontsize=11, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '05_latency_consistency.png'), dpi=300)
plt.close()

# ------------------------------------------------------------------------------
# 6. 06_relative_performance.png
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
performance = [100.0, (events_per_second[1] / events_per_second[0]) * 100]
bars = ax.bar(hypervisors, performance, color=['#0284c7', '#f43f5e'], width=0.45, edgecolor='#0f172a', linewidth=1.2)
ax.set_ylabel('Relative Performance (%)', fontsize=12, fontweight='bold')
ax.set_title('Relative Performance Index (Proxmox VE as 100% Baseline)', fontsize=14, fontweight='bold', pad=15)
ax.set_ylim(0, 120)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 2, f"{yval:.1f}%", ha='center', va='bottom', fontsize=11, fontweight='bold')
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '06_relative_performance.png'), dpi=300)
plt.close()

# ------------------------------------------------------------------------------
# 7. 07_type2_vm_resources.png
# ------------------------------------------------------------------------------
resources = ['vCPU (Cores)', 'RAM (GB)', 'Virtual Disk (GB)']
values = [2, 2, 20]
fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
ax.pie(values, labels=resources, autopct='%1.1f%%', startangle=140, 
       colors=['#38bdf8', '#818cf8', '#94a3b8'], 
       wedgeprops={'edgecolor': 'white', 'linewidth': 2})
ax.axis('equal')
plt.title('Guest Virtual Machine Provisioned Resource Profile', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, '07_type2_vm_resources.png'), dpi=300)
plt.close()

# ------------------------------------------------------------------------------
# 8. 08_summary_dashboard.png
# ------------------------------------------------------------------------------
fig, axs = plt.subplots(2, 2, figsize=(14, 10), dpi=300)
fig.suptitle('Comprehensive Hypervisor Benchmark Dashboard', fontsize=16, fontweight='bold')

# Subplot 1: Total Events
bars1 = axs[0, 0].bar(hypervisors, total_events, color=colors, width=0.45)
axs[0, 0].set_title('Total Events Completed (10s Execution)', fontsize=12, fontweight='bold')
axs[0, 0].set_ylabel('Events Count')
for b in bars1:
    axs[0, 0].text(b.get_x() + b.get_width()/2, b.get_height() + 300, f"{int(b.get_height()):,}", ha='center', fontweight='bold')

# Subplot 2: Events per Second
bars2 = axs[0, 1].bar(hypervisors, events_per_second, color=colors, width=0.45)
axs[0, 1].set_title('Throughput (Events / Second)', fontsize=12, fontweight='bold')
axs[0, 1].set_ylabel('Events / Second')
for b in bars2:
    axs[0, 1].text(b.get_x() + b.get_width()/2, b.get_height() + 30, f"{b.get_height():,.2f}", ha='center', fontweight='bold')

# Subplot 3: Latency
bars3 = axs[1, 0].bar(hypervisors, avg_latency, color=['#10b981', '#ef4444'], width=0.45)
axs[1, 0].set_title('Average Latency (ms)', fontsize=12, fontweight='bold')
axs[1, 0].set_ylabel('Latency (ms)')
axs[1, 0].set_ylim(0, 1.0)
for b in bars3:
    axs[1, 0].text(b.get_x() + b.get_width()/2, b.get_height() + 0.02, f"{b.get_height():.2f} ms", ha='center', fontweight='bold')

# Subplot 4: Relative Performance
bars4 = axs[1, 1].bar(hypervisors, performance, color=['#0284c7', '#f43f5e'], width=0.45)
axs[1, 1].set_title('Relative Compute Efficiency (%)', fontsize=12, fontweight='bold')
axs[1, 1].set_ylabel('Efficiency Index (%)')
axs[1, 1].set_ylim(0, 120)
for b in bars4:
    axs[1, 1].text(b.get_x() + b.get_width()/2, b.get_height() + 2, f"{b.get_height():.1f}%", ha='center', fontweight='bold')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig(os.path.join(output_dir, '08_summary_dashboard.png'), dpi=300)
plt.close()

print("[+] All 8 hypervisor comparison graphs successfully generated in graphs/ directory!")
