/*
  ==============================================================================

    SpaceMouse.cpp
    Created: 4 Nov 2024 2:24:05pm
    Author:  GRoussel

  ==============================================================================
*/

#include "SpaceMouse.h"



SpaceMouse::SpaceMouse()
{
    this->sendProtocol = EsendProtocol::OSC;

    switch (this->sendProtocol)
    {
    case EsendProtocol::OSC:
        this->netInfos.ConnectOSC();
    case EsendProtocol::MIDI:
        break;
    default:
        break;
    }

}

SpaceMouse::~SpaceMouse()
{
}



void SpaceMouse::SendOSCData(EdataSelect dataSelect)
{
    juce::String Message;
    float data;

    Message = "/" + this->OSCParams.BaseMessage + "/";


    switch (dataSelect)
    {
    case EdataSelect::PITCH:
        Message += this->OSCParams.PitchMessage;
        data = values.data.PITCH;
        break;

    case EdataSelect::YAW:
        Message += this->OSCParams.YawMessage;
        data = values.data.YAW;
        break;

    case EdataSelect::ROLL:
        Message += this->OSCParams.RollMessage;
        data = values.data.ROLL;
        break;

    case EdataSelect::UD:
        Message += this->OSCParams.UDMessage;
        data = values.data.UD;
        break;

    case EdataSelect::LR:
        Message += this->OSCParams.LRMessage;
        data = values.data.LR;
        break;

    case EdataSelect::FB:
        Message += this->OSCParams.FBMessage;
        data = values.data.FB;
        break;

    default:
        break;
    }

    if (!this->netInfos.SM_OSCsender.send(Message, (float)data))
        netInfos.showConnectionErrorMessage("Error: could not send OSC message.");

}
