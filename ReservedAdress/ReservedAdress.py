import ipaddress

# Définition des plages sous forme (adresse de départ, octets significatifs)
reserved_ranges = [
    ("127", 1),             # Bouclage
    ("169.254", 2),         # APIPA
    ("192.0.2", 3),         # TEST-NET-1
    ("198.51.100", 3),      # TEST-NET-2
    ("203.0.113", 3),       # TEST-NET-3
    ("224", 1),             # Multicast
]

def get_significant_octets(ip, num_octets):
    # Utilise l'objet ipaddress pour formater correctement l'IP
    ip_obj = ipaddress.ip_address(ip)
    return ".".join(str(ip_obj).split(".")[:num_octets])

def is_reserved(ip):
    ip_str = str(ip)
    for range_ip, octets in reserved_ranges:
        # Comparer les octets significatifs
        if get_significant_octets(ip_str, octets) == range_ip:
            return True
    return False
