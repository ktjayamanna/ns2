set ns [new Simulator]
set tf [open udp.tr w]
$ns trace-all $tf

# Create 6 nodes
for {set i 0} {$i < 6} {incr i} {
    set n($i) [$ns node]
}

# Create links based on the lab topology
$ns duplex-link $n(0) $n(3) 1Mb 1ms DropTail
$ns duplex-link $n(1) $n(3) 1Mb 1ms DropTail
$ns duplex-link $n(2) $n(3) 1Mb 1ms DropTail
$ns duplex-link $n(3) $n(4) 1Mb 10ms DropTail
$ns duplex-link $n(4) $n(5) 1Mb 1ms DropTail

# Buffer size limited to 5 between n3 and n4
$ns queue-limit $n(3) $n(4) 5

# Destination node n5
set null0 [new Agent/Null]
$ns attach-agent $n(5) $null0

# Helper procedure to set up UDP and CBR
proc setup_cbr {src dst size rate fid} {
    global ns
    set udp [new Agent/UDP]
    $ns attach-agent $src $udp
    $ns connect $udp $dst
    $udp set fid_ $fid 

    set cbr [new Application/Traffic/CBR]
    $cbr attach-agent $udp
    $cbr set packetSize_ $size
    $cbr set rate_ $rate
    return $cbr
}

# 3 Source nodes: n0, n1, n2 with requested packet sizes and rates
# Flow ID (fid) is set to 16, 32, and 512 to identify packets easily
set cbr0 [setup_cbr $n(0) $null0 16 80Kbps 16]
set cbr1 [setup_cbr $n(1) $null0 32 320Kbps 32]
set cbr2 [setup_cbr $n(2) $null0 512 800Kbps 512]

# Schedule simulation events
$ns at 0.1 "$cbr0 start"
$ns at 0.1 "$cbr1 start"
$ns at 0.1 "$cbr2 start"

$ns at 10.0 "$cbr0 stop"
$ns at 10.0 "$cbr1 stop"
$ns at 10.0 "$cbr2 stop"

$ns at 10.1 "finish"

proc finish {} {
    global ns tf
    $ns flush-trace
    close $tf
    exit 0
}

$ns run