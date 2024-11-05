/*
  ==============================================================================

    SpaceMouse.h
    Created: 4 Nov 2024 2:24:05pm
    Author:  GRoussel

  ==============================================================================
*/

#include "SM_Param.h"
#include "SM_Values.h"
#include "SM_Network.h"

#pragma once


class SpaceMouse {

public :

    SpaceMouse();
    ~SpaceMouse();

    OSC_SMParam OSCParams;
    SM_Values values;
    SM_Network netInfos;
    EsendProtocol sendProtocol;

    void SendOSCData(EdataSelect dataSelect);

    // CallBacks


};
