#pragma once
#include "Rectangle.h"

class Square : public Rectangle
{
public:
    Square(int id) : Rectangle(id, SQUARE) {};
    Square(unsigned int id, double sLen) : Rectangle(id, sLen, sLen, SQUARE){};
    int getSideLen() { return getLength(); } // call the basic class function.
    ~Square(){}
};