import socket
import urllib.request
import uuid
import netifaces
import subprocess
import ipaddress
import requests
import platform
from typing import List, Optional, Dict, Tuple

# ---------------------------------------------------------------- GET FUNCTIONS ----------------------------------------------------------------

def get_private_ip() -> 'IP':
    """Get the primary private IP address of the system"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return IP(ip)
        except:
            s.close()
            
        interfaces = netifaces.interfaces()
        for iface in interfaces:
            if iface.startswith('lo'):
                continue
            addrs = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in addrs:
                for addr_info in addrs[netifaces.AF_INET]:
                    ip = addr_info['addr']
                    if ip != '127.0.0.1' and not ip.startswith('169.254.'):
                        return IP(ip)
        
        return IP(socket.gethostbyname(socket.gethostname()))
    except Exception as e:
        return IP("127.0.0.1")

def get_public_ip() -> 'IP':
    """Get the public IP address using multiple services"""
    services = [
        "https://api.ipify.org",
        "https://icanhazip.com",
        "https://ident.me",
        "https://checkip.amazonaws.com",
        "https://ipinfo.io/ip"
    ]
    
    for service in services:
        try:
            ip = urllib.request.urlopen(service, timeout=3).read().decode().strip()
            if ip and ip != "":
                return IP(ip)
        except:
            continue
    
    try:
        ip = requests.get("https://api.ipify.org", timeout=5).text.strip()
        if ip:
            return IP(ip)
    except:
        pass
    
    return IP("0.0.0.0")

def get_mac_address(interface: Optional[str] = None) -> 'MAC':
    """Get MAC address for specific interface or primary interface"""
    try:
        if interface:
            if interface in netifaces.interfaces():
                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_LINK in addrs:
                    mac = addrs[netifaces.AF_LINK][0]['addr']
                    return MAC(mac)
        
        primary_ip = str(get_private_ip())
        for iface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in addrs:
                for addr_info in addrs[netifaces.AF_INET]:
                    if addr_info['addr'] == primary_ip and netifaces.AF_LINK in addrs:
                        mac = addrs[netifaces.AF_LINK][0]['addr']
                        return MAC(mac)
        
        mac = uuid.getnode()
        mac_str = ':'.join(f'{(mac >> ele) & 0xff:02x}' for ele in range(40, -1, -8))
        return MAC(mac_str)
    except:
        return MAC("00:00:00:00:00:00")

def get_router_ip() -> Optional['IP']:
    """Get the router/gateway IP address"""
    try:
        gws = netifaces.gateways()
        default = gws.get('default')
        
        if default and netifaces.AF_INET in default:
            return IP(default[netifaces.AF_INET][0])
        
        if default and netifaces.AF_INET6 in default:
            return IP(default[netifaces.AF_INET6][0])
        
        if hasattr(subprocess, 'run'):
            try:
                if platform.system() == "Windows":
                    result = subprocess.run(['route', 'print', '0.0.0.0'], 
                                          capture_output=True, text=True)
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if '0.0.0.0' in line and len(line.split()) >= 3:
                            parts = line.split()
                            if parts[0] == '0.0.0.0' and parts[1] == '0.0.0.0':
                                return IP(parts[2])
                else:
                    result = subprocess.run(['ip', 'route'], 
                                          capture_output=True, text=True)
                    for line in result.stdout.split('\n'):
                        if 'default via' in line:
                            parts = line.split()
                            return IP(parts[2])
            except:
                pass
    except:
        pass
    
    return None

def get_router_mac() -> Optional['MAC']:
    """Get router MAC address using ARP"""
    router_ip = get_router_ip()
    if not router_ip:
        return None
    
    router_ip_str = str(router_ip)
    
    try:
        if platform.system() == "Windows":
            subprocess.run(['ping', '-n', '1', router_ip_str], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(['ping', '-c', '1', router_ip_str], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if platform.system() == "Windows":
            result = subprocess.run(['arp', '-a'], 
                                  capture_output=True, text=True)
            output = result.stdout
            for line in output.split('\n'):
                if router_ip_str in line:
                    parts = line.split()
                    for p in parts:
                        if '-' in p and len(p) == 17:
                            return MAC(p.replace('-', ':'))
                        elif ':' in p and len(p) >= 17:
                            return MAC(p)
        else:
            result = subprocess.run(['arp', '-n'], 
                                  capture_output=True, text=True)
            output = result.stdout
            for line in output.split('\n'):
                if router_ip_str in line:
                    parts = line.split()
                    if len(parts) >= 3:
                        mac = parts[2]
                        if ':' in mac or '-' in mac:
                            return MAC(mac.replace('-', ':'))
    except:
        pass
    
    return None

def get_all_private_ips() -> List['IP']:
    """Get all private IP addresses from all interfaces"""
    ips = []
    try:
        for iface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in addrs:
                for addr_info in addrs[netifaces.AF_INET]:
                    ip = addr_info.get("addr")
                    if ip:
                        ips.append(IP(ip))
    except:
        pass
    
    return ips

def get_dns_servers() -> List['IP']:
    """Get DNS server addresses"""
    dns_servers = []
    try:
        if platform.system() == "Windows":
            result = subprocess.run(['nslookup'], 
                                  input='\n', capture_output=True, text=True)
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Address:' in line and not '#' in line:
                    ip = line.split(':')[1].strip()
                    if ip != '127.0.0.1':
                        dns_servers.append(IP(ip))
        else:
            with open('/etc/resolv.conf', 'r') as f:
                content = f.read()
                for line in content.split('\n'):
                    if line.startswith('nameserver'):
                        ip = line.split()[1].strip()
                        dns_servers.append(IP(ip))
    except:
        dns_servers = [
            IP("8.8.8.8"),
            IP("1.1.1.1"),
            IP("9.9.9.9")
        ]
    
    return dns_servers

def get_subnet_mask() -> Optional['IP']:
    """Get subnet mask for primary interface"""
    try:
        primary_ip = str(get_private_ip())
        for iface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in addrs:
                for addr_info in addrs[netifaces.AF_INET]:
                    if addr_info['addr'] == primary_ip and 'netmask' in addr_info:
                        return IP(addr_info['netmask'])
    except:
        pass
    
    return None

def get_network_cidr() -> Optional[str]:
    """Get network CIDR notation"""
    try:
        ip = get_private_ip()
        mask = get_subnet_mask()
        if ip and mask:
            ip_obj = ipaddress.ip_interface(f"{ip}/{mask}")
            return str(ip_obj.network)
    except:
        pass
    
    return None

def get_ip_location(ip_address: Optional['IP'] = None) -> Dict:
    """Get geographical location for an IP address"""
    if not ip_address:
        ip_address = get_public_ip()
    
    services = [
        f"https://ipapi.co/{ip_address}/json/",
        f"http://ip-api.com/json/{ip_address}",
        f"https://geolocation-db.com/json/{ip_address}"
    ]
    
    for service in services:
        try:
            response = requests.get(service, timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                location_data = {
                    'ip': str(ip_address),
                    'city': data.get('city', 'Unknown'),
                    'region': data.get('region', data.get('region_name', 'Unknown')),
                    'country': data.get('country', data.get('country_name', 'Unknown')),
                    'country_code': data.get('country_code', 'Unknown'),
                    'latitude': data.get('latitude', 0),
                    'longitude': data.get('longitude', 0),
                    'isp': data.get('isp', data.get('org', 'Unknown')),
                    'timezone': data.get('timezone', 'Unknown')
                }
                return location_data
        except:
            continue
    
    return {
        'ip': str(ip_address),
        'city': 'Unknown',
        'region': 'Unknown',
        'country': 'Unknown',
        'country_code': 'Unknown',
        'latitude': 0,
        'longitude': 0,
        'isp': 'Unknown',
        'timezone': 'Unknown'
    }

def get_network_speed() -> Dict[str, float]:
    """Get network speed information"""
    try:
        import speedtest
        
        st = speedtest.Speedtest()
        
        print("  🔍 Suche besten Server...")
        st.get_best_server()
        
        print("  📥 Teste Download...")
        download_speed = st.download() / 1_000_000
        
        print("  📤 Teste Upload...")
        upload_speed = st.upload() / 1_000_000
        
        ping = st.results.ping
        
        return {
            'download_mbps': round(download_speed, 2),
            'upload_mbps': round(upload_speed, 2),
            'ping_ms': round(ping, 2),
            'server': st.results.server.get('name', 'Unknown'),
            'country': st.results.server.get('country', 'Unknown'),
            'sponsor': st.results.server.get('sponsor', 'Unknown')
        }
    except ImportError:
        return {'error': 'speedtest-cli nicht installiert. Installiere mit: pip install speedtest-cli'}
    except Exception as e:
        return {'error': f'Geschwindigkeitstest fehlgeschlagen: {str(e)}'}

def get_connection_type() -> str:
    """Determine connection type (Ethernet, WiFi, etc.)"""
    try:
        primary_ip = str(get_private_ip())
        
        if platform.system() == "Windows":
            try:
                import wmi
                c = wmi.WMI()
                for adapter in c.Win32_NetworkAdapter(NetEnabled=True):
                    if adapter.Name:
                        name_lower = adapter.Name.lower()
                        if 'wireless' in name_lower or 'wifi' in name_lower or '802.11' in name_lower:
                            return "WiFi"
                        elif 'ethernet' in name_lower or 'gigabit' in name_lower:
                            return "Ethernet"
                        elif 'bluetooth' in name_lower:
                            continue
            except:
                pass
        
        for iface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in addrs:
                for addr_info in addrs[netifaces.AF_INET]:
                    if addr_info['addr'] == primary_ip:
                        iface_lower = iface.lower()
                        
                        if 'wi-fi' in iface_lower or 'wlan' in iface_lower:
                            return "WiFi"
                        elif 'ethernet' in iface_lower or 'lan' in iface_lower:
                            return "Ethernet"
                        
                        if iface.startswith('wlan') or iface.startswith('wlp'):
                            return "WiFi"
                        elif iface.startswith('eth') or iface.startswith('enp'):
                            return "Ethernet"
                        
                        if iface.startswith('tun') or iface.startswith('tap'):
                            return "VPN/Tunnel"
        
        return "Ethernet/WiFi (nicht genau erkennbar)"
    except:
        return "Unbekannt"

def get_hostname() -> str:
    """Get system hostname"""
    return socket.gethostname()

def get_fqdn() -> str:
    """Get fully qualified domain name"""
    return socket.getfqdn()

def get_network_interfaces() -> List[Dict]:
    """Get detailed information about all network interfaces"""
    interfaces = []
    try:
        for iface in netifaces.interfaces():
            iface_info = {'name': iface, 'addresses': {}}
            
            if netifaces.AF_LINK in netifaces.ifaddresses(iface):
                mac = netifaces.ifaddresses(iface)[netifaces.AF_LINK][0]['addr']
                iface_info['mac'] = mac
            
            if netifaces.AF_INET in netifaces.ifaddresses(iface):
                ipv4_addrs = []
                for addr in netifaces.ifaddresses(iface)[netifaces.AF_INET]:
                    ipv4_addrs.append({
                        'address': addr.get('addr'),
                        'netmask': addr.get('netmask'),
                        'broadcast': addr.get('broadcast')
                    })
                iface_info['ipv4'] = ipv4_addrs
            
            if netifaces.AF_INET6 in netifaces.ifaddresses(iface):
                ipv6_addrs = []
                for addr in netifaces.ifaddresses(iface)[netifaces.AF_INET6]:
                    ipv6_addrs.append({
                        'address': addr.get('addr'),
                        'netmask': addr.get('netmask')
                    })
                iface_info['ipv6'] = ipv6_addrs
            
            interfaces.append(iface_info)
    except:
        pass
    
    return interfaces

def get_open_ports(start_port: int = 1, end_port: int = 1024, host: str = '127.0.0.1') -> List[Tuple[int, str]]:
    """Scan for open ports"""
    open_ports = []
    
    common_windows_ports = {
        135: "RPC",
        139: "NetBIOS",
        445: "SMB",
        80: "HTTP",
        443: "HTTPS",
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        67: "DHCP Server",
        68: "DHCP Client",
        88: "Kerberos",
        110: "POP3",
        123: "NTP",
        137: "NetBIOS Name Service",
        138: "NetBIOS Datagram",
        143: "IMAP",
        161: "SNMP",
        162: "SNMP Trap",
        389: "LDAP",
        443: "HTTPS",
        445: "SMB",
        636: "LDAPS",
        993: "IMAPS",
        995: "POP3S",
        1433: "MSSQL",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        5900: "VNC",
        8080: "HTTP Proxy"
    }
    
    try:
        if platform.system() == "Windows":
            for port, service in common_windows_ports.items():
                if start_port <= port <= end_port:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    result = sock.connect_ex((host, port))
                    sock.close()
                    if result == 0:
                        open_ports.append((port, service))
        
        for port in range(start_port, min(end_port + 1, 1000)):
            if port in [p for p, _ in open_ports]:
                continue
                
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex((host, port))
            sock.close()
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "unknown"
                open_ports.append((port, service))
        
        open_ports.sort(key=lambda x: x[0])
        
    except Exception as e:
        print(f"  ⚠️ Port-Scanning Fehler: {e}")
    
    return open_ports

# ---------------------------------------------------------------- PRIVATE CHECK FUNCTIONS ----------------------------------------------------------------

class _CheckIP:
    """Interne Klasse für IP-Prüfungen"""
    def __init__(self, value):
        self._value = str(value)

    def is_private(self) -> bool:
        try:
            return ipaddress.ip_address(self._value).is_private
        except ValueError:
            return False

    def is_public(self) -> bool:
        try:
            obj = ipaddress.ip_address(self._value)
            return not obj.is_private and not obj.is_reserved and not obj.is_loopback
        except ValueError:
            return False

    def is_ipv4(self) -> bool:
        try:
            return isinstance(ipaddress.ip_address(self._value), ipaddress.IPv4Address)
        except ValueError:
            return False

    def is_ipv6(self) -> bool:
        try:
            return isinstance(ipaddress.ip_address(self._value), ipaddress.IPv6Address)
        except ValueError:
            return False

    def is_loopback(self) -> bool:
        try:
            return ipaddress.ip_address(self._value).is_loopback
        except ValueError:
            return False

    def is_link_local(self) -> bool:
        try:
            return ipaddress.ip_address(self._value).is_link_local
        except ValueError:
            return False

    def is_multicast(self) -> bool:
        try:
            return ipaddress.ip_address(self._value).is_multicast
        except ValueError:
            return False

    def is_reserved(self) -> bool:
        try:
            return ipaddress.ip_address(self._value).is_reserved
        except ValueError:
            return False

    def get_ip_version(self) -> int:
        try:
            ip_obj = ipaddress.ip_address(self._value)
            return ip_obj.version
        except ValueError:
            return 0

    def belongs_to_network(self, network_cidr: str) -> bool:
        try:
            ip_obj = ipaddress.ip_address(self._value)
            network_obj = ipaddress.ip_network(network_cidr, strict=False)
            return ip_obj in network_obj
        except ValueError:
            return False

class _CheckMAC:
    """Interne Klasse für MAC-Adressen"""
    def __init__(self, value):
        self._value = str(value)

    def is_mac(self) -> bool:
        """Prüft, ob der Wert eine gültige MAC-Adresse ist"""
        v = self._value
        if len(v) != 17:
            return False
        sep = None
        if ":" in v:
            sep = ":"
        elif "-" in v:
            sep = "-"
        else:
            return False
        parts = v.split(sep)
        if len(parts) != 6:
            return False
        for p in parts:
            if len(p) != 2:
                return False
            try:
                int(p, 16)
            except ValueError:
                return False
        return True
    
    def is_unicast(self) -> bool:
        """Check if MAC is unicast (LSB of first byte is 0)"""
        if not self.is_mac():
            return False
        first_byte = int(self._value.split(':')[0], 16)
        return (first_byte & 1) == 0
    
    def is_multicast(self) -> bool:
        """Check if MAC is multicast (LSB of first byte is 1)"""
        if not self.is_mac():
            return False
        first_byte = int(self._value.split(':')[0], 16)
        return (first_byte & 1) == 1
    
    def is_global(self) -> bool:
        """Check if MAC is globally unique (second LSB of first byte is 0)"""
        if not self.is_mac():
            return False
        first_byte = int(self._value.split(':')[0], 16)
        return (first_byte & 2) == 0
    
    def is_local(self) -> bool:
        """Check if MAC is locally administered (second LSB of first byte is 1)"""
        if not self.is_mac():
            return False
        first_byte = int(self._value.split(':')[0], 16)
        return (first_byte & 2) == 2
    
    def get_manufacturer(self) -> str:
        """Try to get manufacturer from MAC (OUI lookup)"""
        if not self.is_mac():
            return "Unknown"
        
        oui = self._value[:8].upper().replace(':', '').replace('-', '')
        
        manufacturers = {
            "4CCC6A": "Samsung Electronics",
            "5056C0": "VMware",
            "000C29": "VMware",
            "080027": "VirtualBox",
            "A45E60": "Apple",
            "001B63": "Apple",
            "00155D": "Microsoft",
            "000D3A": "Microsoft",
            "001A11": "Google",
            "001C14": "Dell",
            "001DE1": "Dell",
            "0026B9": "Intel",
            "0022FA": "Intel",
            "001E67": "Intel",
            "001D09": "Intel",
            "50E6": "Microsoft",
            "001122": "Cisco",
            "00219B": "Cisco",
            "0050F2": "Microsoft",
            "002248": "Microsoft",
            "001451": "Apple",
            "0016CB": "Apple",
            "001E52": "Apple",
            "001EC2": "Apple",
            "001FF3": "Apple",
            "0021E9": "Apple",
            "00236C": "Apple",
            "002500": "Apple",
            "002545": "Apple",
            "00264A": "Apple",
            "0026BB": "Apple",
            "0026B0": "Apple",
            "001B10": "Google",
            "006440": "Google",
            "005056": "VMware",
            "001279": "HP",
            "002264": "HP",
            "00248C": "HP",
            "00E018": "HP",
            "000A95": "IBM",
            "001125": "IBM",
            "001A64": "IBM",
            "0050BA": "IBM",
        }
        
        for length in [6, 4, 3]:
            prefix = oui[:length]
            if prefix in manufacturers:
                return manufacturers[prefix]
        
        try:
            import requests
            response = requests.get(f"https://api.macvendors.com/{oui}", timeout=2)
            if response.status_code == 200:
                return response.text.strip()
        except:
            pass
        
        return "Unknown Manufacturer"

# ---------------------------------------------------------------- IP WRAPPER ----------------------------------------------------------------

class IP:
    """Wrapper um die IP als String + interne check-Funktionen"""
    def __init__(self, ip_str):
        self.ip = str(ip_str)
        self.check = _CheckIP(ip_str)

    def __str__(self):
        return self.ip

    def __repr__(self):
        return f"IP('{self.ip}')"
    
    def __eq__(self, other):
        if isinstance(other, IP):
            return self.ip == other.ip
        return False

# ---------------------------------------------------------------- MAC WRAPPER ----------------------------------------------------------------

class MAC:
    """MAC-Adress-Wrapper mit .check für is_mac()"""
    def __init__(self, mac_str):
        self.mac = str(mac_str)
        self.check = _CheckMAC(mac_str)

    def __str__(self):
        return self.mac

    def __repr__(self):
        return f"MAC('{self.mac}')"
    
    def __eq__(self, other):
        if isinstance(other, MAC):
            return self.mac.lower() == other.mac.lower()
        return False

# ---------------------------------------------------------------- LOCATION WRAPPER ----------------------------------------------------------------

class Location:
    """Wrapper für Standortinformationen"""
    def __init__(self, data: Dict):
        self.data = data
        self.ip = data.get('ip', 'Unknown')
        self.city = data.get('city', 'Unknown')
        self.region = data.get('region', 'Unknown')
        self.country = data.get('country', 'Unknown')
        self.country_code = data.get('country_code', 'Unknown')
        self.latitude = data.get('latitude', 0)
        self.longitude = data.get('longitude', 0)
        self.isp = data.get('isp', 'Unknown')
        self.timezone = data.get('timezone', 'Unknown')

    def __str__(self):
        return f"{self.city}, {self.region}, {self.country}"

    def __repr__(self):
        return f"Location('{self.city}, {self.country}')"

# ---------------------------------------------------------------- FORMAT TEMPLATE ----------------------------------------------------------------

class FormatTemplate:
    @staticmethod
    def _check_value(value):
        if callable(value):
            return value()
        return value

    @staticmethod
    def type_1(symbol, name, value):
        value = FormatTemplate._check_value(value)
        return f"[{symbol}] {name}: {value}"
    
    @staticmethod
    def type_2(symbol, name, value):
        value = FormatTemplate._check_value(value)
        return f"({symbol}) {name}: {value}"
    
    @staticmethod
    def type_3(symbol, name, value):
        value = FormatTemplate._check_value(value)
        return "{" + f"{symbol}" + "} " + f"{name}: {value}"
    
    @staticmethod
    def type_4(symbol, name, value):
        value = FormatTemplate._check_value(value)
        return f"{symbol} {name}: {value}"
