# Step 1: Create simulator
set ns [new Simulator]

# Step 2: Open trace file to record what happens
set tracefile [open out.tr w]
$ns trace-all $tracefile

# Step 3: Create two computers (nodes)
set node0 [$ns node]
set node1 [$ns node]

# Step 4: Connect them with a cable
# Speed: 1Mb, Delay: 10ms
$ns duplex-link $node0 $node1 1Mb 10ms DropTail

# Step 5: Create a sender on node0
set udp [new Agent/UDP]
$ns attach-agent $node0 $udp

# Step 6: Create a receiver on node1
set receiver [new Agent/Null]
$ns attach-agent $node1 $receiver

# Step 7: Connect sender to receiver
$ns connect $udp $receiver

# Step 8: Create traffic (sends packets)
set traffic [new Application/Traffic/CBR]
$traffic set packetSize_ 500
$traffic set interval_ 0.01
$traffic attach-agent $udp

# Step 9: Schedule when things happen
$ns at 1.0 "$traffic start"
$ns at 4.0 "$traffic stop"
$ns at 5.0 "finish"

# Step 10: What to do when finished
proc finish {} {
    global ns tracefile
    $ns flush-trace
    close $tracefile
    puts "Simulation complete!"
    exit 0
}

# Step 11: Run the simulation
$ns run