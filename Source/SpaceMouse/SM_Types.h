/*
  ==============================================================================

    SM_Types.h
    Created: 4 Nov 2024 3:25:02pm
    Author:  GRoussel

  ==============================================================================
*/
#include <JuceHeader.h>
#pragma once

enum class EsendProtocol {

    OSC,
    MIDI // TO BE IMPLEMENTED
};

enum class EmodType {

    INCREMENTAL_LINEAR,
    ABSOLUTE

};

enum class EdataSelect {
    // Rotation
    PITCH,
    YAW,
    ROLL,
    // Translation
    UD,
    LR,
    FB,
    // Many
    ALL_ROT,
    ALL_TRANS,
    ALL
};

struct SM_Data {
    // TODO : Template this classe to make possible the ose of other than float

    float PITCH{ 0.0f };
    float YAW{ 0.0f };
    float ROLL{ 0.0f };

    float UD{ 0.0f };
    float LR{ 0.0f };
    float FB{ 0.0f };
};
