import random
import string
import time
import hashlib
import binascii
import os

def generate_char(length):
    chars = "abcdef1234567890"
    return ''.join(random.choice(chars) for _ in range(length))

def generate_rid(length):
    try:
        bytes_length = length // 2
        random_bytes = os.urandom(bytes_length)
        return binascii.hexlify(random_bytes).decode('utf-8')
    except Exception as e:
        return ''


def generate_gid():
    return f"{generate_char(8)}-{generate_char(4)}-{generate_char(4)}-{generate_char(4)}-{generate_char(12)}"
def sha256_hash(s):
    return hashlib.sha256(s.encode()).hexdigest()

def md5_hash(s):
    return hashlib.md5(s.encode()).hexdigest()

def GenerateKlv(protocol, version, rid):
    salts = [
        "e9fc40ec08f9ea6393f59c65e37f750aacddf68490c4f92d0d2523a5bc02ea63",
        "c85df9056ee603b849a93e1ebab5dd5f66e1fb8b2f4a8caef8d13b9f9e013fa4",
        "3ca373dffbf463bb337e0fd768a2f395b8e417475438916506c721551f32038d",
        "73eff5914c61a20a71ada81a6fc7780700fb1c0285659b4899bc172a24c14fc1",
    ]

    constantValues = [
        sha256_hash(md5_hash(sha256_hash(str(protocol)))),
        sha256_hash(sha256_hash(version)),
        sha256_hash(sha256_hash(str(protocol)) + salts[3]),
    ]

    hash_input = (
        constantValues[0] +
        salts[0] +
        constantValues[1] +
        salts[1] +
        sha256_hash(md5_hash(sha256_hash(rid))) +
        salts[2] +
        constantValues[2]
    )
    
    hash_result = sha256_hash(hash_input)
    
    return hash_result

def generate_login_packet(tank_id_name, tank_id_pass, requested_name, game_version, meta, protocol):
    random.seed(int(time.time() * 1000))
    
    rid = generate_rid(len("020D096B635AE07F0858E3C1BDC42AD2"))
    klv = GenerateKlv(207, "4.55", rid)  # Assuming generate_klv is implemented in utils as shown in the Go code
    packet = []
    if tank_id_name != 'user':
        packet.append(f"tankIDName|{tank_id_name}")
        packet.append(f"tankIDPass|{tank_id_pass}")

    packet.extend([
        f"requestedName|{requested_name}",
        "f|1",
        f"protocol|{protocol}",
        f"game_version|{game_version}",
        "lmode|0",
        "cbits|1024",
        "player_age|25",
        "GDPR|1",
        "category|_-5100",
        "totalPlaytime|0",
        f"klv|{klv}",
        f"gid|{generate_gid()}",
        "tr|4322",
        f"meta|{meta}",
        "fhash|-716928334",
        f"rid|{rid}",
        "platformID|4",
        "deviceVersion|0",
        "country|us",
        "hash|-12760733",
        "mac|02:00:00:00:00:00",
        "wk|NONE0"
    ])
    return '\n'.join(packet)

# Assuming the utils module
