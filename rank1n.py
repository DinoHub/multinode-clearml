import multicast_expert
import socket

interfaces=multicast_expert.get_interface_ips(include_ipv4=True, include_ipv6=False)
#interfaceip=multicast_expert.get_default_gateway_iface_ip_v4()
interfaceip=interfaces[-1]
print(interfaces)

with multicast_expert.McastRxSocket(socket.AF_INET, mcast_ips=['239.1.2.3'], port=12345, iface_ip=interfaceip) as mcast_rx_sock:
    bytes, src_address = mcast_rx_sock.recvfrom()
    print(bytes)
    print(src_address)
