/*
  ==============================================================================

    SM_Values.cpp
    Created: 4 Nov 2024 2:51:49pm
    Author:  GRoussel

  ==============================================================================
*/

#include "SM_Values.h"

void SM_Values::increment(EmodType modType, EdataSelect dataSelect)
{

    switch (dataSelect)
    {
    case EdataSelect::PITCH:
        break;
    case EdataSelect::YAW:
        break;
    case EdataSelect::ROLL:
        break;
    case EdataSelect::UD:
        break;
    case EdataSelect::LR:
        break;
    case EdataSelect::FB:
        break;
    case EdataSelect::ALL_ROT:
        break;
    case EdataSelect::ALL_TRANS:
        break;
    case EdataSelect::ALL:
        break;
    default:
        break;
    }

    switch (modType)
    {
    case EmodType::INCREMENTAL_LINEAR:
        break;
    case EmodType::ABSOLUTE:
        break;
    default:
        break;
    }
}
