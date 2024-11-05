/*
  ==============================================================================

    SM_Param.cpp
    Created: 4 Nov 2024 2:32:19pm
    Author:  GRoussel

  ==============================================================================
*/

#include "SM_Param.h"

void OSC_SMParam::setMessage(EdataSelect dataselect, juce::String InMessage)
{
	// To change the base message use EdataSelect::ALL

	switch (dataselect)
	{
	case EdataSelect::PITCH:
		this->PitchMessage = InMessage;
		break;

	case EdataSelect::YAW:
		this->YawMessage = InMessage;
		break;

	case EdataSelect::ROLL:
		this->RollMessage = InMessage;
		break;

	case EdataSelect::UD:
		this->UDMessage = InMessage;
		break;

	case EdataSelect::LR:
		this->LRMessage = InMessage;
		break;

	case EdataSelect::FB:
		this->FBMessage = InMessage;
		break;

	case EdataSelect::ALL:
		this->BaseMessage = InMessage;
		break;
	default:
		break;
	}
}
