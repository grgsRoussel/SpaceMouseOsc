import SpaceMouseOSC

SM = SpaceMouseOSC.SMOSC(scale = 0.005 ,mode=SpaceMouseOSC.SMMode.ABSOLUTE_INT_LIMITED, intLimits=[0,127])

while True:
    SM.update()
    SM.sendOSC()
    print(SM.data.x, SM.data.y, SM.data.z, SM.data.rx, SM.data.ry, SM.data.rz, SM.data.clicked)
 