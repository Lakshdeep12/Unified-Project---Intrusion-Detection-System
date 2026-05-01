from scapy.all import IP, TCP, UDP

def extract_features(packet):
    protocol = 0
    flow_duration = 0
    fwd_packets = 1
    backward_packets = 0
    packet_len = len(packet)
    flow_bytes = float(packet_len)
    flow_packets = 1.0
    psh_flag = 0
    fin_flag = 0
    ack_flag = 0
    syn_flag = 0

    if packet.haslayer(IP):
        protocol = int(packet[IP].proto)
        packet_len = int(packet[IP].len or packet_len)
        flow_bytes = float(packet_len)

    if packet.haslayer(TCP):
        flags = packet[TCP].flags
        psh_flag = 1 if flags.P else 0
        fin_flag = 1 if flags.F else 0
        ack_flag = 1 if flags.A else 0
        syn_flag = 1 if flags.S else 0
    elif packet.haslayer(UDP):
        protocol = 17

    return [
        protocol,
        0,              # Fwd IAT Total is not available from a single packet.
        0,              # Flow IAT Mean
        0,              # Flow IAT Max
        0,              # Flow IAT Min
        psh_flag,
        fin_flag,
        ack_flag,
        syn_flag,
        packet_len,
        flow_duration,
        fwd_packets,
        backward_packets,
        flow_bytes,
        flow_packets,
    ]
