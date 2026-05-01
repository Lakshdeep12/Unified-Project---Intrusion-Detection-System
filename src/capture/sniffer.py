import ctypes
import sys

from scapy.all import conf, sniff

def start_sniffing(callback, iface=None):
    if sys.platform.startswith("win"):
        try:
            is_admin = bool(ctypes.windll.shell32.IsUserAnAdmin())
        except Exception:
            is_admin = False

        if not is_admin:
            raise PermissionError(
                "Packet capture on Windows normally requires an Administrator terminal. "
                "Restart PowerShell as Administrator and run the pipeline again."
            )

        if not conf.use_pcap:
            print(
                "Warning: Scapy did not find a libpcap/Npcap provider. "
                "Install Npcap with WinPcap-compatible mode if live capture does not receive packets."
            )

    try:
        sniff(
            prn=callback,
            store=False,
            iface=iface
        )
    except PermissionError:
        raise
    except OSError as exc:
        raise RuntimeError(
            "Packet capture failed. On Windows, install Npcap and run the terminal as Administrator. "
            "If multiple adapters exist, pass the correct interface name."
        ) from exc
