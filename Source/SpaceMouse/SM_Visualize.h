/*
  ==============================================================================

    SM_Visualize.h
    Created: 4 Nov 2024 7:17:47pm
    Author:  GRoussel

  ==============================================================================
*/

#pragma once
#include <JuceHeader.h>

class SM_Visualize
{

public :
    // Creates as much sliders as labels
    SM_Visualize();
    ~SM_Visualize();

    juce::Array<juce::String> STR_Labels{ "LR","FB","UD", "Pitch", "Yaw", "Roll" };
    juce::Array<juce::Slider*> Sliders;

    juce::Array<juce::Label*> Labels;

    juce::Label BaseLabel;

    juce::Label STR_SendAdress;
    juce::Label SendAdress;

    juce::Label STR_sendPort;
    juce::Label sendPort;



    int totalWidth;
    int totalHeight;
    
};

