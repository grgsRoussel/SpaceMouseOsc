/*
  ==============================================================================

    SM_Param.h
    Created: 4 Nov 2024 2:32:19pm
    Author:  GRoussel

  ==============================================================================
*/

#include <JuceHeader.h>
#include "SM_Types.h"

#pragma once


class OSC_SMParam {

public:

    // An udp message from the space mouse is in the form of BaseMessage/Type/Message

    // Main Base Message
    juce::String BaseMessage{ "spacemouse" }; // Base OscMessage

    // Message for each axis

    // Rotations Axis

    juce::String PitchMessage{ "Pitch" };
    juce::String YawMessage{ "Yaw" };
    juce::String RollMessage{ "Roll" };


    // Translation Axis
    juce::String UDMessage{"UD"}; // Up Down
    juce::String LRMessage{"LR"}; // Left Right
    juce::String FBMessage{ "FB" };  // Forward  Backward


    // Increment or Absolute
    EmodType modType{ EmodType::INCREMENTAL_LINEAR};

    //

    void setMessage(EdataSelect dataselect, juce::String InMessage);

};

class MIDI_SMParam {

public:
    // TODO : To implement

};

