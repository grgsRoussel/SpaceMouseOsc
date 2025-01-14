import SpaceMouseOSC

SM = SpaceMouseOSC.SMOSC(scale = 1,mode=SpaceMouseOSC.SMMode.ABSOLUTE_INT_LIMITED)

while True:
    SM.update()
    SM.sendOSC()
    print(SM.data.x, SM.data.y, SM.data.z, SM.data.rx, SM.data.ry, SM.data.rz, SM.data.clicked)
