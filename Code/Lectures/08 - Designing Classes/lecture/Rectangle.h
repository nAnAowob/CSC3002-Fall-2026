#pragma once
#include "BaseShape.h"

class Rectangle : public BaseShape
{
public:
    Rectangle(unsigned int id, ShapeType type = RECT) : BaseShape(id, type) {};
    Rectangle(unsigned int id, double width, double length, ShapeType type = RECT);
    int getLength() { return mLength; }
    int getWidth() { return mWidth; }
    // override four virrual functions
    double calcCircumference();
    double calcArea();
    std::string toString();
    ~Rectangle();

private:
    double mWidth = 0.0;
    double mLength = 0.0;
};