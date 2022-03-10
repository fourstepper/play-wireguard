from http import client
from diagrams import Cluster, Diagram
from diagrams.generic.device import Mobile
from diagrams.generic.os import LinuxGeneral
from diagrams.generic.network import VPN
from diagrams.generic.network import Router
from diagrams.outscale.network import NatService
from diagrams.generic.os import Windows
from diagrams.onprem.compute import Server

with Diagram("Topology", show=False):
    with Cluster("VPN 192.168.0.0/24"):
        clients = [LinuxGeneral(
            "192.168.0.100/32"), Windows("192.168.0.101/32"), Mobile("192.168.0.102/32")]

    with Cluster("VPN 192.168.1.0/24"):
        other_clients = [LinuxGeneral(
            "192.168.1.100/32"), Windows("192.168.1.101/32"), Mobile("192.168.1.102/32")]

    with Cluster("Server"):
        with Cluster("Wireguard Interfaces"):
            wg0 = VPN("wg0 - 192.168.0.2/32")
            wg1 = VPN("wg0 - 192.168.1.2/32")

    with Cluster("LAN 10.0.0.0/24"):
        nat = NatService("Carrier-Grade NAT")
        with Cluster("PersistentKeepalive = 15"):
            router = Router("192.168.0.3/32")
        nas = Server("NAS - 10.0.0.10/24")

    with Cluster("LAN 10.0.1.0/24"):
        other_nat = NatService("Carrier-Grade NAT")
        with Cluster("PersistentKeepalive = 15"):
            other_router = Router("192.168.1.3/32")
        other_nas = Server("NAS - 10.0.1.10/24")

    # connections LAN
    for client in clients:
        client >> wg0

    wg0 << nat
    nat << router
    router - nas

    # connections Other LAN
    for client in other_clients:
        client >> wg1

    wg1 << other_nat
    other_nat << other_router
    other_router - other_nas
