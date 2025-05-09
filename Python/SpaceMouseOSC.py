import hid
import struct
import numpy as np
from pythonosc import udp_client
from enum import Enum

class SMMode(Enum):
    RAW = 0                                 # Raw values from the SpaceMouse -- With Byte conversion -- Betwenn -350 and 350
    RAW_B = 1                               # Raw values from the SpaceMouse -- Binary data
    ABSOLUTE_FLOAT = 2                      # Absolute values from the SpaceMouse -- Float values
    ABSOLUTE_FLOAT_LIMITED = 3              # Absolute values from the SpaceMouse -- Float values -- Limited with intLimits
    ABSOLUTE_INT = 4                        # Absolute values from the SpaceMouse -- Int values
    ABSOLUTE_INT_LIMITED = 5                # Absolute values from the SpaceMouse -- Int values -- Limited with intLimits
    RELATIVE_FLOAT = 6                      # Relative values from the SpaceMouse -- Float values -- Betwwen 0 and 1
    RELATIVE_INT_LIMITED = 7                # Relative values from the SpaceMouse -- Int values -- Limited with intLimits


class SMOSC:
    def __init__(self, vendor_id = 0x256F, product_id = 0xC635, ip = "127.0.0.1", port = 12000, scale = 1, mode = SMMode.RAW, intLimits = [0,127]):


        self.params = type('', (), {})()
        self.params.priv = type('', (), {})()


        # Internal Non modifiable values Values
        self.params.priv.overflowVal = 1
        self.params.priv.baseScale = 350

        # SpaceMouse Parameters
        self.params.vendor_id = vendor_id
        self.params.product_id = product_id
        
        self.params.sendIP = ip
        self.params.sendPort = port

        self.params.mode = mode
        self.params.intLimits = intLimits
        self.params.scale = scale/self.params.priv.baseScale # Scale factor for the translation and rotation values -- 350 is the maximum value for the SpaceMouse

        # SpaceMouse Initialization
        self.device = hid.device()
        self.openSpaceMouse()

        #initialize OSC client
        self.client = udp_client.SimpleUDPClient( self.params.sendIP , self.params.sendPort)


        # SpaceMouse Internal Variables
        self.datas = [0, 0, 0, 0, 0, 0]
        self.Rdatas = []
        self.clicked = 0

        # CleanDatas
        self.data = type('', (), {})()
        self.data.old = type('', (), {})()

        self.resetAbsolute()


    def __del__(self):
        try :
            self.device.close()
        except Exception as e:
            print("Device Cannot be closed !")
    
    def openSpaceMouse(self):

        try :
            self.device.open(self.params.vendor_id, self.params.product_id)
        except Exception as e:
            print("SpaceMouse not found !")
            raise SystemExit(0)

        self.device.set_nonblocking(1)

    def sendOSC(self):

# WARNING : OSC Messages can be skipped due to the frequency of the message sent -- Only Python Prototype pb or General OSC Problem ?

        # self.client.send_message("/spacemouse/all", [self.data.x, self.data.y, self.data.z, self.data.rx, self.data.ry, self.data.rz, self.data.clicked])
        
        self.client.send_message("/spacemouse/x", self.data.x)
        self.client.send_message("/spacemouse/y", self.data.y)
        self.client.send_message("/spacemouse/z", self.data.z)  
        self.client.send_message("/spacemouse/rx", self.data.rx)
        self.client.send_message("/spacemouse/ry", self.data.ry)
        self.client.send_message("/spacemouse/rz", self.data.rz)
        self.client.send_message("/spacemouse/clicked", self.data.clicked)

        # self.client.send_message("/spacemouse/mode", self.params.mode)


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

            case SMMode.RAW_B:
                print("Not implemented yet")

            case SMMode.ABSOLUTE_FLOAT:
                self.AbsoluteFloat()
            
            case SMMode.ABSOLUTE_FLOAT_LIMITED:
                self.AbsoluteFloat()
                self.limited()
                

            case SMMode.ABSOLUTE_INT:
                self.AbsoluteInt()

            case SMMode.ABSOLUTE_INT_LIMITED:
                
                self.AbsoluteInt()
                self.limited()
                self.data.x = int(self.data.x)
                self.data.y = int(self.data.y)  
                self.data.z = int(self.data.z)  
                self.data.rx = int(self.data.rx)    
                self.data.ry = int(self.data.ry)    
                self.data.rz = int(self.data.rz)    


            case SMMode.RELATIVE_FLOAT:

                self.relativeFloat()

            case SMMode.RELATIVE_INT_LIMITED:
                
                self.relativeFloat()

                self.data.x = int((self.data.x * self.params.intLimits[1]) - self.params.intLimits[0])
                self.data.y = int((self.data.y * self.params.intLimits[1]) - self.params.intLimits[0])
                self.data.z = int((self.data.z * self.params.intLimits[1]) - self.params.intLimits[0])
                self.data.rx = int((self.data.rx * self.params.intLimits[1]) - self.params.intLimits[0])
                self.data.ry = int((self.data.ry * self.params.intLimits[1]) - self.params.intLimits[0])
                self.data.rz = int((self.data.rz * self.params.intLimits[1]) - self.params.intLimits[0])


    def limited(self):

        self.data.x = np.clip(self.data.x, a_min = self.params.intLimits[0], a_max = self.params.intLimits[1])
        self.data.y = np.clip(self.data.y, a_min = self.params.intLimits[0], a_max = self.params.intLimits[1])
        self.data.z = np.clip(self.data.z, a_min = self.params.intLimits[0], a_max = self.params.intLimits[1])
        self.data.rx = np.clip(self.data.rx, a_min = self.params.intLimits[0], a_max = self.params.intLimits[1])
        self.data.ry = np.clip(self.data.ry, a_min = self.params.intLimits[0], a_max = self.params.intLimits[1])
        self.data.rz = np.clip(self.data.rz, a_min = self.params.intLimits[0], a_max = self.params.intLimits[1])

    def AbsoluteFloat(self):

        self.data.x += self.datas[0] * self.params.scale
        self.data.y += self.datas[1] * self.params.scale
        self.data.z += self.datas[2] * self.params.scale
        self.data.rx += self.datas[3] * self.params.scale
        self.data.ry += self.datas[4] * self.params.scale
        self.data.rz += self.datas[5] * self.params.scale

    def AbsoluteInt(self):

        x = np.sign(self.datas[0]) * self.params.scale * self.params.priv.baseScale
        y = np.sign(self.datas[1]) * self.params.scale * self.params.priv.baseScale
        z = np.sign(self.datas[2]) * self.params.scale * self.params.priv.baseScale
        rx = np.sign(self.datas[3]) * self.params.scale * self.params.priv.baseScale
        ry = np.sign(self.datas[4]) * self.params.scale * self.params.priv.baseScale
        rz = np.sign(self.datas[5]) * self.params.scale * self.params.priv.baseScale
        
        self.data.old.x += x
        self.data.old.y += y
        self.data.old.z += z
        self.data.old.rx += rx
        self.data.old.ry += ry
        self.data.old.rz += rz

        if(self.params.mode == SMMode.ABSOLUTE_INT_LIMITED):
            self.data.old.x = np.clip(self.data.old.x, a_min = self.params.intLimits[0], a_max = self.params.intLimits[1])
            self.data.old.y = np.clip(self.data.old.y, a_min = self.params.intLimits[0], a_max = self.params.intLimits[1])
            self.data.old.z = np.clip(self.data.old.z, a_min = self.params.intLimits[0], a_max = self.params.intLimits[1])
            self.data.old.rx = np.clip(self.data.old.rx, a_min = self.params.intLimits[0], a_max = self.params.intLimits[1])
            self.data.old.ry = np.clip(self.data.old.ry, a_min = self.params.intLimits[0], a_max = self.params.intLimits[1])
            self.data.old.rz = np.clip(self.data.old.rz, a_min = self.params.intLimits[0], a_max = self.params.intLimits[1])

        self.data.x = int(self.data.old.x)
        self.data.y = int(self.data.old.y)
        self.data.z = int(self.data.old.z)
        self.data.rx = int(self.data.old.rx)
        self.data.ry = int(self.data.old.ry)
        self.data.rz = int(self.data.old.rz)


    def relativeFloat(self):
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

        self.data.old.x = 0
        self.data.old.y = 0
        self.data.old.z = 0
        self.data.old.rx = 0
        self.data.old.ry = 0
        self.data.old.rz = 0



        self.datas = [0, 0, 0, 0, 0, 0]

