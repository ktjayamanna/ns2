import sys

# Track statistics per Flow ID (fid) matching packet size
stats = {
    16: {'s': 0, 'r': 0, 'd': 0}, 
    32: {'s': 0, 'r': 0, 'd': 0}, 
    512: {'s': 0, 'r': 0, 'd': 0}, 
    'total': {'s': 0, 'r': 0, 'd': 0}
}

try:
    with open('udp.tr', 'r') as f:
        for line in f:
            p = line.split()
            # Ensure it is a valid trace line for CBR traffic
            if len(p) < 8 or p[4] != 'cbr': 
                continue
            
            ev = p[0]
            src = p[2]
            dst = p[3]
            fid = int(p[7]) # Extract the flow id we set in tcl
            
            # '+' means packet queued for sending at the start node
            if ev == '+' and src in ['0', '1', '2']: 
                if fid in stats: stats[fid]['s'] += 1
                stats['total']['s'] += 1
                
            # 'r' means packet received at the destination
            elif ev == 'r' and dst == '5': 
                if fid in stats: stats[fid]['r'] += 1
                stats['total']['r'] += 1
                
            # 'd' means packet dropped (anywhere on the path)
            elif ev == 'd': 
                if fid in stats: stats[fid]['d'] += 1
                stats['total']['d'] += 1
except FileNotFoundError:
    print("Error: udp.tr not found. Run the ns simulation first.")
    sys.exit(1)

# Print matching output requested by the assignment
for k in [16, 32, 512, 'total']:
    s = stats[k]['s']
    r = stats[k]['r']
    d = stats[k]['d']
    ratio = (r / s) if s > 0 else 0.0
    name = f"cbr_{k}" if k != 'total' else "cbr_total"
    
    print(f"{name} s:{s} r:{r}, r/s Ratio:{ratio:.4f}, d:{d}")