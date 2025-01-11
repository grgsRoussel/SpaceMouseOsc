import hid
import struct
import matplotlib.pyplot as plt
import numpy as np
from pythonosc import udp_client


class ov:
    def __init__(self):
        self.overflowVal = 30
        self.threshold = 1
        self.old = 0

    def outf(self, x):
        diff = x - self.old
        # Adjust for the overflow value
        if diff < -self.overflowVal / 2:
            diff += self.overflowVal
        elif diff > self.overflowVal / 2:
            diff -= self.overflowVal

        self.old = x  # Update the old value for the next iteration
        return diff

def openSpaceMouse():

    vendor_id = 0x256F
    product_id = 0xC635

    device = hid.device()
    device.open(vendor_id, product_id)
    device.set_nonblocking(1)

    return device

def convertDatas(Rdatas):

    clicked = 0

    if Rdatas:
        match Rdatas[0] :
            case 1 : # Translation

                datas[0] = struct.unpack('<h',bytes([Rdatas[1], Rdatas[2]]))[0]  # memcpy is equivalent in C++ ?
                datas[1] = struct.unpack('<h',bytes([Rdatas[3], Rdatas[4]]))[0]
                datas[2] = struct.unpack('<h',bytes([Rdatas[5], Rdatas[6]]))[0]


            case 2 : # Rotation
                
                datas[3] = struct.unpack('<h',bytes([Rdatas[1], Rdatas[2]]))[0]
                datas[4] = struct.unpack('<h',bytes([Rdatas[3], Rdatas[4]]))[0]
                datas[5] = struct.unpack('<h',bytes([Rdatas[5], Rdatas[6]]))[0]

            case 3 : # Buttons
                clicked = Rdatas[1]  # May be different depending on the device

    return datas, clicked

def sendOSC(client,datas):

    client.send_message("/spacemouse/x", datas[0])
    client.send_message("/spacemouse/y", datas[1])
    client.send_message("/spacemouse/z", datas[2])  
    client.send_message("/spacemouse/rx", datas[3])
    client.send_message("/spacemouse/ry", datas[4])
    client.send_message("/spacemouse/rz", datas[5])

    client.send_message("/spacemouse/mode", "RAW")

dev = openSpaceMouse()
client = udp_client.SimpleUDPClient("127.0.0.1", 12000)

clicked = []

Rdatas = np.zeros(7)
datas = np.zeros(6)

# axes = ["x", "y", "z", "rx", "ry", "rz"]

# plt.ion()
# fig, ax = plt.subplots()
# bars  = ax.bar(axes, datas)
# ax.set_ylim(-400, 400)

while clicked !=1:
    
    Rdatas = dev.read(64)

    datas, clicked = convertDatas(Rdatas)
    sendOSC(client,datas)
   # print(datas, "\r")
           
    # for bar, new_height in zip(bars, datas):
    #     bar.set_height(new_height)

    #     fig.canvas.draw()
    #     fig.canvas.flush_events()

dev.close()

