/*
  ==============================================================================

    SM_Network.cpp
    Created: 4 Nov 2024 10:42:01pm
    Author:  GRoussel

  ==============================================================================
*/

#include "SM_Network.h"

SM_Network::SM_Network()
{
}

void SM_Network::setSendAdress(juce::String InAddress)
{
    this->sendAddress = juce::IPAddress(InAddress);
}

void SM_Network::setSentPort(juce::uint16 InPort)
{
    this->sendPort = InPort;
}

void SM_Network::ConnectOSC()
{
    if (!this->SM_OSCsender.connect(this->sendAddress.toString(), this->sendPort))  
        showConnectionErrorMessage("Error: could not connect to UDP port 9001."); // MODIFY TO FIT REAL PORT VALUE with this->netInfos.sendPort
}

void SM_Network::resetNetwork()
{
    this->SM_OSCsender.disconnect();
    this->ConnectOSC();
}

void SM_Network::showConnectionErrorMessage(const juce::String& messageText)
{
    juce::AlertWindow::showMessageBoxAsync(juce::AlertWindow::WarningIcon,
        "Connection error",
        messageText,
        "OK");
}

