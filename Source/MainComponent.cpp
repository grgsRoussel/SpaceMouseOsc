#include "MainComponent.h"

//==============================================================================

// Some Functions -- Just for test 

void showConnectionErrorMessage(const juce::String& messageText)
{
    juce::AlertWindow::showMessageBoxAsync(juce::AlertWindow::WarningIcon,
        "Connection error",
        messageText,
        "OK");
}

// Main

MainComponent::MainComponent()
{
    int i = 0;
    for (auto slider : sm_viz.Sliders)
    {
        addAndMakeVisible(*slider);
        addAndMakeVisible(*sm_viz.Labels[i]);

        i++;
    }

    addAndMakeVisible(sm_viz.BaseLabel);
    addAndMakeVisible(sm_viz.SendAdress);
    addAndMakeVisible(sm_viz.STR_SendAdress);
    addAndMakeVisible(sm_viz.sendPort);
    addAndMakeVisible(sm_viz.STR_sendPort);

    linkSliders();
    linkLabels();


    // Window size
    setSize(sm_viz.totalWidth, sm_viz.totalHeight);
}

MainComponent::~MainComponent()
{
}

//==============================================================================
void MainComponent::paint (juce::Graphics& g)
{
    // (Our component is opaque, so we must completely fill the background with a solid colour)
    g.fillAll (getLookAndFeel().findColour (juce::ResizableWindow::backgroundColourId));

    //g.setFont (juce::FontOptions (16.0f));
    //g.setColour (juce::Colours::white);
    //g.drawText ("Hello You Mr OSC!", getLocalBounds(), juce::Justification::centred, true);
}

void MainComponent::resized()
{
    // This is called when the MainComponent is resized.
    // If you add any child components, this is where you should
    // update their positions.
}

void MainComponent::linkSliders()
{

    sm_viz.Sliders[0]->onValueChange = [this]
        {
            sm_hardware.values.data.LR = (float)sm_viz.Sliders[0]->getValue();
            sm_hardware.SendOSCData(EdataSelect::LR);
        };

    sm_viz.Sliders[1]->onValueChange = [this]
        {
            sm_hardware.values.data.FB = (float)sm_viz.Sliders[1]->getValue();
            sm_hardware.SendOSCData(EdataSelect::FB);
        };
    sm_viz.Sliders[2]->onValueChange = [this]
        {
            sm_hardware.values.data.UD = (float)sm_viz.Sliders[2]->getValue();
            sm_hardware.SendOSCData(EdataSelect::UD);
        };


    sm_viz.Sliders[3]->onValueChange = [this]
        {
            sm_hardware.values.data.PITCH = (float)sm_viz.Sliders[3]->getValue();
            sm_hardware.SendOSCData(EdataSelect::PITCH);
        };

    sm_viz.Sliders[4]->onValueChange = [this]
        {
            sm_hardware.values.data.YAW = (float)sm_viz.Sliders[4]->getValue();
            sm_hardware.SendOSCData(EdataSelect::YAW);
        };

    sm_viz.Sliders[5]->onValueChange = [this]
        {
            sm_hardware.values.data.ROLL = (float)sm_viz.Sliders[5]->getValue();
            sm_hardware.SendOSCData(EdataSelect::ROLL);
        };
}

void MainComponent::linkLabels()
{
    sm_viz.Labels[0]->onTextChange = [this]
        {
            sm_hardware.OSCParams.setMessage(EdataSelect::LR, sm_viz.Labels[0]->getTextValue().toString());
        };

    sm_viz.Labels[1]->onTextChange = [this]
        {
            sm_hardware.OSCParams.setMessage(EdataSelect::FB, sm_viz.Labels[1]->getTextValue().toString());
        };

    sm_viz.Labels[2]->onTextChange = [this]
        {
            sm_hardware.OSCParams.setMessage(EdataSelect::UD, sm_viz.Labels[2]->getTextValue().toString());
        };

    sm_viz.Labels[3]->onTextChange = [this]
        {
            sm_hardware.OSCParams.setMessage(EdataSelect::PITCH, sm_viz.Labels[3]->getTextValue().toString());
        };

    sm_viz.Labels[4]->onTextChange = [this]
        {
            sm_hardware.OSCParams.setMessage(EdataSelect::YAW, sm_viz.Labels[4]->getTextValue().toString());
        };

    sm_viz.Labels[5]->onTextChange = [this]
        {
            sm_hardware.OSCParams.setMessage(EdataSelect::ROLL, sm_viz.Labels[5]->getTextValue().toString());
        };

    sm_viz.BaseLabel.onTextChange = [this]
        {
            sm_hardware.OSCParams.setMessage(EdataSelect::ALL, sm_viz.BaseLabel.getTextValue().toString());
        };

    sm_viz.SendAdress.onTextChange = [this]
        {
            sm_hardware.netInfos.setSendAdress(sm_viz.SendAdress.getTextValue().toString());
            sm_hardware.netInfos.resetNetwork();
        };

    sm_viz.sendPort.onTextChange = [this]
        {
            sm_hardware.netInfos.setSentPort(sm_viz.sendPort.getTextValue().toString().getIntValue());
            sm_hardware.netInfos.resetNetwork();

        };

}

