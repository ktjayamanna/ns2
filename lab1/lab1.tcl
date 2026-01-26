# Create a Simulator object
set ns [new Simulator]

# Define different colors for data flows
$ns color 1 Blue
$ns color 2 Red

# Open the NAM trace file
set nf [open out.nam w]
$ns namtrace-all $nf

# Open the Trace file
set tf [open out.tr w]
$ns trace-all $tf

# Define a 'finish' procedure
proc finish {} {
    global ns nf tf
    $ns flush-trace
    # Close the trace files
    close $nf
    close $tf
    
    exit 0
}

# --- Create Nodes ---
set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]

# --- Create Links ---
# n0 <-> n2: 100Mbps, 5ms delay
$ns duplex-link $n0 $n2 100Mb 5ms DropTail
# n1 <-> n2: 100Mbps, 5ms delay
$ns duplex-link $n1 $n2 100Mb 5ms DropTail
# n2 <-> n3: 54Mbps, 10ms delay
$ns duplex-link $n2 $n3 54Mb 10ms DropTail
# n2 <-> n4: 54Mbps, 10ms delay
$ns duplex-link $n2 $n4 54Mb 10ms DropTail


# --- Link Orientation ---
$ns duplex-link-op $n0 $n2 orient right-down
$ns duplex-link-op $n1 $n2 orient right-up
$ns duplex-link-op $n2 $n3 orient right-down
$ns duplex-link-op $n2 $n4 orient right-up

# --- Setup UDP Connection (n0 -> n3) ---
# Create UDP Agent and attach to n0
set udp0 [new Agent/UDP]
$ns attach-agent $n0 $udp0
$udp0 set class_ 1

# Create Null Agent (Traffic Sink) and attach to n3
set null0 [new Agent/Null]
$ns attach-agent $n3 $null0

# Connect the agents
$ns connect $udp0 $null0

# Setup CBR Application over UDP
set cbr0 [new Application/Traffic/CBR]
$cbr0 attach-agent $udp0
$cbr0 set packetSize_ 1000
$cbr0 set rate_ 1Mb
$cbr0 set interval_ 0.005

# --- Setup TCP Connection (n1 -> n4) ---
# Create TCP Agent and attach to n1
set tcp0 [new Agent/TCP]
$ns attach-agent $n1 $tcp0
$tcp0 set class_ 2

# Create TCP Sink and attach to n4
set sink0 [new Agent/TCPSink]
$ns attach-agent $n4 $sink0

# Connect the agents
$ns connect $tcp0 $sink0

# Setup FTP Application over TCP
set ftp0 [new Application/FTP]
$ftp0 attach-agent $tcp0
$ftp0 set type_ FTP

# --- Schedule Events ---
# Start CBR at 0.5s, Stop at 4.5s
$ns at 0.5 "$cbr0 start"
$ns at 4.5 "$cbr0 stop"

# Start FTP at 1.0s, Stop at 4.0s
$ns at 1.0 "$ftp0 start"
$ns at 4.0 "$ftp0 stop"

# End simulation at 5.0s
$ns at 5.0 "finish"

# --- Run the Simulator ---
$ns run