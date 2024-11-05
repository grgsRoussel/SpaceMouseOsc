/*
  ==============================================================================

    SM_Visualize.cpp
    Created: 4 Nov 2024 7:17:47pm
    Author:  GRoussel

  ==============================================================================
*/

#include "SM_Visualize.h"

SM_Visualize::SM_Visualize() : Sliders(juce::Array<juce::Slider*>()), Labels(juce::Array<juce::Label*>())
{
    //Initial Position of sliders
    int BaseX = 20;
    int BaseY = 20;

    int BaseLabelWidth = 150;
    int BaseLabelHeight = 20;


    int sliderWidth = 50;
    int sliderHeight = 180;

    int margin = 30;

    float SliderRange = 500.0f;

    int X = BaseX;
    int Y = BaseY;
    
    // Base Label

    this->BaseLabel.setText("spacemouse", juce::dontSendNotification);
    this->BaseLabel.setEditable(false, true, true);
    this->BaseLabel.setBounds(X, Y, BaseLabelWidth, BaseLabelHeight);

    Y += BaseLabelHeight + margin;

    // List of 6Dof Labels 

    for (auto label : this->STR_Labels)
    {
        

        // Sliders
        juce::Slider* NewSlider = new juce::Slider;
        this->Sliders.add(NewSlider);

        this->Sliders.getLast()->setRange(-SliderRange, SliderRange);
        this->Sliders.getLast()->setSliderStyle(juce::Slider::LinearBarVertical);
        this->Sliders.getLast()->setTitle(label);
        this->Sliders.getLast()->setBounds(X, Y, sliderWidth, sliderHeight);

        // Labels
        juce::Label* NewLabel = new juce::Label;
        this->Labels.add(NewLabel);

        this->Labels.getLast()->setText(label, juce::dontSendNotification);
        this->Labels.getLast()->attachToComponent(this->Sliders.getLast(), false);
        this->Labels.getLast()->setJustificationType(juce::Justification::centred);
        this->Labels.getLast()->setEditable(false, true, true);


        X += sliderWidth + margin;
       // Y += sliderHeight + margin;
    }

    // port and Adress Label

    Y += margin + sliderHeight + margin;

    this->SendAdress.setText("127.0.0.1", juce::dontSendNotification);
    this->SendAdress.setJustificationType(juce::Justification::centred);
    this->SendAdress.setBounds(BaseX, Y, BaseLabelWidth, BaseLabelHeight);
    this->SendAdress.setEditable(false, true, true);

    this->STR_SendAdress.setText("Send Address :", juce::dontSendNotification);
    this->STR_SendAdress.setEditable(false, false, true);
    this->STR_SendAdress.setBounds(BaseX, Y, BaseLabelWidth, BaseLabelHeight);
    this->STR_SendAdress.attachToComponent(&this->SendAdress, false);

    Y += margin + BaseLabelHeight;

    this->sendPort.setText("9001", juce::dontSendNotification);
    this->sendPort.setJustificationType(juce::Justification::centred);
    this->sendPort.setBounds(BaseX, Y, BaseLabelWidth, BaseLabelHeight);
    this->sendPort.setEditable(false, true, true);

    this->STR_sendPort.setText("Send Port :", juce::dontSendNotification);
    this->STR_sendPort.setEditable(false, false, true);
    this->STR_sendPort.setBounds(BaseX, Y, BaseLabelWidth, BaseLabelHeight);
    this->STR_sendPort.attachToComponent(&this->sendPort, false);


    // Total Size

    this->totalWidth = X + BaseX;
    this->totalHeight = Y + margin ;


}

SM_Visualize::~SM_Visualize()
{
    for (auto slider : this->Sliders)
    {
        delete slider;
    }

    for (auto label : this->Labels)
    {
        delete label;
    }
}
