import SpaceMouseOSC

SM = SpaceMouseOSC.SMOSC(mode=SpaceMouseOSC.SMMode.ABSOLUTE)

while True:
    SM.update()
    SM.sendOSC()
    print(SM.data.x, SM.data.y, SM.data.z, SM.data.rx, SM.data.ry, SM.data.rz, SM.data.clicked)
