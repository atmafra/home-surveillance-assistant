import socket
import ipaddress

COMMON_CAMERA_PORTS = [
    80,
    554,
    8080,
    88,
    443,
    8000,
    8008,
    8081,
]  # Common HTTP, RTSP, ONVIF ports


def get_local_ip_prefix():
    """Attempts to get the local IP address and derive the network prefix."""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        # Assuming a /24 subnet (e.g., 192.168.1.x)
        return ".".join(local_ip.split(".")[:3]) + "."
    except socket.gaierror:
        print(
            "Warning: Could not determine local IP address automatically. Using default 192.168.1."
        )
        return "192.168.1."  # Default if auto-detection fails


def discover_cameras(ip_prefix=None, ports=None, timeout=0.2):
    """
    Scans the local network for potential cameras by checking common ports.
    """
    if ip_prefix is None:
        ip_prefix = get_local_ip_prefix()
    if ports is None:
        ports = COMMON_CAMERA_PORTS

    found_devices = []
    print(f"Scanning network prefix: {ip_prefix}x for open ports: {ports}")

    for i in range(
        1, 255
    ):  # Scan typical local IP range (e.g., 192.168.1.1 to 192.168.1.254)
        ip = f"{ip_prefix}{i}"
        for port in ports:
            try:
                with socket.create_connection((ip, port), timeout=timeout):
                    print(f"Potential camera found at {ip}:{port}")
                    found_devices.append({"ip": ip, "port": port})
                    # For simplicity, we assume one open port means a potential device.
                    # We could break here if we only want one entry per IP.
            except (socket.timeout, ConnectionRefusedError, OSError):
                pass  # Host is not responding on this port or port is closed
    return found_devices
