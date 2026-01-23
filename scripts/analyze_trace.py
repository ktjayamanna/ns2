#!/usr/bin/env python3
import sys
import matplotlib.pyplot as plt
from collections import defaultdict

def parse_trace(filename):
    """Parse NS-2 trace file"""
    events = []
    with open(filename, 'r') as f:
        for line in f:
            parts = line.split()
            if len(parts) < 11:
                continue
            
            event = {
                'action': parts[0],
                'time': float(parts[1]),
                'from': parts[2],
                'to': parts[3],
                'type': parts[4],
                'size': int(parts[5]),
                'seq': parts[10] if len(parts) > 10 else '0'
            }
            events.append(event)
    return events

def analyze(events):
    """Calculate statistics"""
    sent = sum(1 for e in events if e['action'] == '+')
    received = sum(1 for e in events if e['action'] == 'r')
    dropped = sum(1 for e in events if e['action'] == 'd')
    
    # Throughput over time
    time_bytes = defaultdict(int)
    for e in events:
        if e['action'] == 'r':
            time_slot = int(e['time'])
            time_bytes[time_slot] += e['size']
    
    print(f"\n=== Simulation Results ===")
    print(f"Packets Sent:     {sent}")
    print(f"Packets Received: {received}")
    print(f"Packets Dropped:  {dropped}")
    print(f"Delivery Ratio:   {received/sent*100:.2f}%")
    
    # Plot
    if time_bytes:
        times = sorted(time_bytes.keys())
        throughput = [time_bytes[t] * 8 / 1000 for t in times]  # kbps
        
        plt.figure(figsize=(10, 4))
        plt.plot(times, throughput, marker='o')
        plt.xlabel('Time (s)')
        plt.ylabel('Throughput (kbps)')
        plt.title('Network Throughput')
        plt.grid(True)
        plt.savefig('throughput.png')
        print(f"\n✓ Plot saved to throughput.png")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_trace.py <trace_file>")
        sys.exit(1)
    
    events = parse_trace(sys.argv[1])
    analyze(events)