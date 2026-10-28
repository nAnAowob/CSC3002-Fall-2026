#pragma once
#include "Ellipse.h"

class Circle : public Ellipse
{
public:
        Circle(unsigned int id) : Ellipse(id, CIRCLE) {};
        Circle(unsigned int id, double radius):Ellipse(id, radius, radius,CIRCLE){};
        int getRadius() { return getSemiMajor(); }
        ~Circle(){}
};