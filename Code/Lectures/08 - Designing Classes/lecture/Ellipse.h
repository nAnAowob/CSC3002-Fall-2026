#pragma once
#include "BaseShape.h"

class Ellipse : public BaseShape
{
public:
        Ellipse(unsigned int id, ShapeType type=ELLIPSE): BaseShape(id, type) {};
        Ellipse(unsigned int id, double a, double b, ShapeType type=ELLIPSE );
        int getSemiMajor() { return mSemiMajor; }
        int getSemiMinor() { return mSemiMinor; }

        // override four virrual functions
        double calcCircumference();
        double calcArea();
        std::string toString();
        ~Ellipse();

private:
        double mSemiMajor = 0.0;
        double mSemiMinor = 0.0;
};