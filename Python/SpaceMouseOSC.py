import hid
import struct
import numpy as np
from pythonosc import udp_client
from enum import Enum

class SMMode(Enum):
    RAW = 0
    ABSOLUTE = 1
    RELATIVE = 2

class SMOSC:
    def __init__(self, vendor_id = 0x256F, product_id = 0xC635, ip = "127.0.0.1", port = 12000, scale = 1, mode = SMMode.RAW):

        # SpaceMouse Parameters
        self.params = type('', (), {})()
        self.params.vendor_id = vendor_id
        self.params.product_id = product_id
        
        self.params.sendIP = ip
        self.params.sendPort = port

        self.params.scale = scale/350 # Scale factor for the translation and rotation values -- 350 is the maximum value for the SpaceMouse

        self.params.mode = mode

        # SpaceMouse Initialization
        self.device = hid.device()
        self.openSpaceMouse()

        #initialize OSC client
        self.client = udp_client.SimpleUDPClient( self.params.sendIP , self.params.sendPort)


        # SpaceMouse Internal Variables
        self.old = 0
        self.datas = [0, 0, 0, 0, 0, 0]
        self.Rdatas = []
        self.clicked = 0

        # CleanDatas
        self.data = type('', (), {})()
        self.resetAbsolute()

    def __del__(self, name):
        self.device.close()
        

    def openSpaceMouse(self):
        self.device.open(self.params.vendor_id, self.params.product_id)
        self.device.set_nonblocking(1)

    def sendOSC(self):

        self.client.send_message("/spacemouse/x", self.data.x)
        self.client.send_message("/spacemouse/y", self.data.y)
        self.client.send_message("/spacemouse/z", self.data.z)  
        self.client.send_message("/spacemouse/rx", self.data.rx)
        self.client.send_message("/spacemouse/ry", self.data.ry)
        self.client.send_message("/spacemouse/rz", self.data.rz)
        self.client.send_message("/spacemouse/clicked", self.data.clicked)

        #self.client.send_message("/spacemouse/mode", self.params.mode)


    def update(self):
        self.Rdatas = self.device.read(64)
        self.ParseDatas()
        self.ProcessData()
    
    def getDatas(self):
        return self.data

    def ParseDatas(self):

        if self.Rdatas:
            match self.Rdatas[0] :
                case 1 : # Translation

                    self.datas[0] = struct.unpack('<h',bytes([self.Rdatas[1], self.Rdatas[2]]))[0]  # memcpy is equivalent in C++ ?
                    self.datas[1] = struct.unpack('<h',bytes([self.Rdatas[3], self.Rdatas[4]]))[0]
                    self.datas[2] = struct.unpack('<h',bytes([self.Rdatas[5], self.Rdatas[6]]))[0]


                case 2 : # Rotation
                    
                    self.datas[3] = struct.unpack('<h',bytes([self.Rdatas[1], self.Rdatas[2]]))[0]
                    self.datas[4] = struct.unpack('<h',bytes([self.Rdatas[3], self.Rdatas[4]]))[0]
                    self.datas[5] = struct.unpack('<h',bytes([self.Rdatas[5], self.Rdatas[6]]))[0]

                case 3 : # Buttons
                    self.clicked = self.Rdatas[1]  # May be different depending on the device

    def ProcessData(self):


        self.data.clicked = self.clicked

        match self.params.mode:
            case SMMode.RAW:
                self.data.x = self.datas[0]
                self.data.y = self.datas[1]
                self.data.z = self.datas[2]
                self.data.rx = self.datas[3]
                self.data.ry = self.datas[4]
                self.data.rz = self.datas[5]

            case SMMode.ABSOLUTE:

                self.data.x += self.datas[0] * self.params.scale
                self.data.y += self.datas[1] * self.params.scale
                self.data.z += self.datas[2] * self.params.scale
                self.data.rx += self.datas[3] * self.params.scale
                self.data.ry += self.datas[4] * self.params.scale
                self.data.rz += self.datas[5] * self.params.scale
        
            case SMMode.RELATIVE:
                self.data.x = self.datas[0] * self.params.scale
                self.data.y = self.datas[1] * self.params.scale
                self.data.z = self.datas[2] * self.params.scale
                self.data.rx = self.datas[3] * self.params.scale
                self.data.ry = self.datas[4] * self.params.scale
                self.data.rz = self.datas[5] * self.params.scale

    def resetAbsolute(self):
        self.data.x = 0
        self.data.y = 0
        self.data.z = 0
        self.data.rx = 0
        self.data.ry = 0
        self.data.rz = 0
        self.datas = [0, 0, 0, 0, 0, 0]


