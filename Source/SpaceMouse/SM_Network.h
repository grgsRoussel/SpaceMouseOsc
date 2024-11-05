/*
  ==============================================================================

    SM_Network.h
    Created: 4 Nov 2024 10:42:01pm
    Author:  GRoussel

  ==============================================================================
*/

#include <JuceHeader.h>
#pragma once

class SM_Network {

public :

    SM_Network();

    juce::OSCSender SM_OSCsender;

    juce::IPAddress sendAddress{ "127.0.0.1" };
    juce::uint16 sendPort{ 9001 };

    void setSendAdress(juce::String InAddress);
    void setSentPort(juce::uint16 InPort);

    void ConnectOSC();

    void resetNetwork();

    void showConnectionErrorMessage(const juce::String& messageText);


};