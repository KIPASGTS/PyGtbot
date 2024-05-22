import enet
import struct
import threading
import re
from packet import *
from utils import generate_login_packet
from variants import Variant

class Bot:
    def __init__(self, targetHost: str, targetPort: int, guestName = "BurpSiregar") -> None:
        self.targetHost = targetHost
        self.targetPort = targetPort
        self.host = None
        self.peer = None
        self.User = ['user', 'pw']
        self.GuestName = guestName
        self.netid = '0'
        self.currentWorld = ""
        self.usingNewPacket = False

    def set_user(self, username: str, password: str):
        self.User[0] = username
        self.User[1] = password

    def set_guest(self, username: str):
        self.GuestName = username

    def set_using_new_packet(self, value: bool):
        self.usingNewPacket = value

    def get_nick(self):
        if self.User[0] != 'user': return self.User[0]
        else: return self.GuestName

    def connect(self):
        self.host = enet.Host(None, 1, 2, 0, 0)
        self.host.checksum = enet.ENET_CRC32
        self.host.compress_with_range_coder()
        self.host.usingNewPacket = self.usingNewPacket
        self.peer = self.host.connect(enet.Address(self.targetHost.encode(), self.targetPort), 1)

    def detach(self):
        event = self.host.service(3000)
        if event.type == enet.EVENT_TYPE_CONNECT:
            self.OnConnected(event.peer, event.peer.address, self.host)
        elif event.type == enet.EVENT_TYPE_DISCONNECT:
            self.OnDisconnected(event.peer, event.peer.address, self.host)
        elif event.type == enet.EVENT_TYPE_RECEIVE:
            self.OnReceived(event.peer, event.peer.address, self.host, event.packet)

    def OnConnected(self, peer, address, host):
        print(f"[{self.get_nick()}] Connected to server!")

    def OnDisconnected(self, peer, address, host):
        print(f"[{self.get_nick()}] Disconnected from server!")
        self.connect() #Connect again

    def OnReceived(self, peer, address, host, packet):
        netMessage = packet.data[0]
        if netMessage == 1:
            SendPacket(peer, 2, generate_login_packet(self.User[0], self.User[1], self.GuestName, "4.56", "mafia", 207))
            pass
        elif netMessage == 2 or netMessage == 3:
            msg = GetTextMessageFromPacket(packet.data)
            replaced = msg.replace('\n', '\\n')
            print(f"[{self.get_nick()}][{netMessage}] Receive packet text: {replaced}")
            pass
        elif netMessage == 4:
            tank = GetTankPacketFromPacket(packet.data[4:])
            if tank.PacketType == 1:
                variant = Variant()
                variant.unpack(packet)
                func_name = variant.get_string(0)
                if func_name == "OnSuperMainStartAcceptLogonHrdxs47254722215a":
                    SendPacket(peer, 2, "action|enter_game\n")
                elif func_name == "OnRequestWorldSelectMenu":
                    SendPacket(peer, 3, "action|join_request\nname|VEND")
                elif func_name == "OnSpawn":
                    func_content = variant.get_string(1)
                    if 'type|local' in func_content:
                        self.netid = re.findall(r'netID\|(.*?)\n', func_content)[0]
                else:
                    print(str(variant.VariantData))
            elif tank.PacketType == 4:
                nameLen = packet.data[66]
                self.currentWorld = packet.data[68 : 68 + nameLen]
                print(f"World Name Len: {nameLen}, World Name: {self.currentWorld}")

            elif tank.PacketType == 16:
                data = packet.data[60:]
                item_data = open('items.dat', 'wb')
                item_data.write(data)
                item_data.close()
                pass
            else:
                print(f"[{self.get_nick()}] Unhandled tank packet type: {tank.PacketType}")
        else:
            print(f"[{self.get_nick()}] Unhandled net message: {netMessage}")
     
def main():
    bot = Bot("46.250.226.217", 17092, "BurpSiregar") #Example Target
    bot.set_user("DidYouKnowKKK", "mangeak23#")
    bot.set_using_new_packet(True)
    bot.connect()

    while True:
        bot.detach()
main()
