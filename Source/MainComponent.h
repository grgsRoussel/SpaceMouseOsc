#pragma once

#include <JuceHeader.h>
#include "SpaceMouse.h"
#include "SM_Visualize.h"

//==============================================================================
/*
    This component lives inside our window, and this is where you should put all
    your controls and content.
*/
class MainComponent  : public juce::Component
{
public:
    //==============================================================================
    MainComponent();
    ~MainComponent() override;

    juce::Slider rotaryKnob;
    juce::OSCSender sender;

    juce::IPAddress SendAdress{"127.0.0.1"};
    juce::uint16 SendPort{9001};

    SpaceMouse sm_hardware;
    SM_Visualize sm_viz;

    //==============================================================================
    void paint (juce::Graphics&) override;
    void resized() override;

    void linkSliders();
    void linkLabels();

private:
    //==============================================================================
    // Your private member variables go here...


    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (MainComponent)
};
