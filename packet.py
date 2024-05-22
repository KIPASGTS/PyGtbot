import struct
import enet

def GetTextMessageFromPacket(packetData):
    if len(packetData) < 4: return ""
    return packetData[4:-1].decode('utf-8')

def GetNetMessageTypeFromPacket(packetData):
    if len(packetData) > 0: return packetData[0]
    else: return -1;

def SendPacket(peer, game_message_type, str_data):
    packet_size = 5 + len(str_data)
    net_packet = bytearray(packet_size)
    struct.pack_into('<I', net_packet, 0, game_message_type)
    if str_data != "":
        net_packet[4:4+len(str_data)] = str_data.encode('utf-8')
    net_packet[4+len(str_data)] = 0
    net_packet_bytes = bytes(net_packet)

    enetPacket = enet.Packet(data=net_packet_bytes, flags=1)
    peer.send(0, enetPacket)


class TankPacket:
    PacketType = 0
    NetID = 0
    CharacterState = 0
    Value = 0
    X = 0
    Y = 0
    XSpeed = 0
    YSpeed = 0
    PunchX = 0
    PunchY = 0

def PackTankPacket(packet: TankPacket) -> bytes:
    buffer = bytearray(56)
    struct.pack_into('<I', buffer, 0, packet.PacketType)
    struct.pack_into('<I', buffer, 4, packet.NetID)
    struct.pack_into('<I', buffer, 12, packet.CharacterState)
    struct.pack_into('<I', buffer, 20, packet.Value)
    struct.pack_into('<f', buffer, 24, packet.X)
    struct.pack_into('<f', buffer, 28, packet.Y)
    struct.pack_into('<f', buffer, 32, packet.XSpeed)
    struct.pack_into('<f', buffer, 36, packet.YSpeed)
    struct.pack_into('<I', buffer, 44, packet.PunchX)
    struct.pack_into('<I', buffer, 48, packet.PunchY)
    return bytes(buffer)

def GetTankPacketFromPacket(packet: bytes) -> TankPacket:
    tank = TankPacket()
    tank.PacketType     = struct.unpack_from('<I', packet, 0)[0]
    tank.NetID          = struct.unpack_from('<I', packet, 4)[0]
    tank.CharacterState = struct.unpack_from('<I', packet, 12)[0]
    tank.Value          = struct.unpack_from('<I', packet, 20)[0]
    tank.X              = struct.unpack_from('<f', packet, 24)[0]
    tank.Y              = struct.unpack_from('<f', packet, 28)[0]
    tank.XSpeed         = struct.unpack_from('<f', packet, 32)[0]
    tank.YSpeed         = struct.unpack_from('<f', packet, 36)[0]
    tank.PunchX         = struct.unpack_from('<I', packet, 44)[0]
    tank.PunchY         = struct.unpack_from('<I', packet, 48)[0]
    return tank

def SendTankPacket(peer, tank: TankPacket):
    tankData = bytearray(56 + 5)
    struct.pack_into('<I', tankData, 0, 4)
    tankData[4:] = PackTankPacket(tank)
    enetPacket = enet.Packet(data=tankData, flags=1)
    peer.send(0, enetPacket)
