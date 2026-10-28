// Shape.cpp : This file contains the 'main' function. Program execution begins and ends there.
#include <iostream>
#include <sstream>
#include <string>
#include "BaseShape.h"
#include "Ellipse.h"
#include "Circle.h"
#include "Rectangle.h"
#include "Square.h"

using namespace std;

BaseShape *CreateShape(int st);

int main()
{
    int st = 0;
    BaseShape *pShape = NULL;
    while (st != 4)
    {
        std::cout << "Enter the Shape Type: 0 = Ellipse 1 = Circle, 2=Rectangle, 3=Square , 4=Exit";
        std::cin >> st;
        pShape = CreateShape(st);
        if (pShape)
        {
            pShape->calcArea();
            pShape->calcCircumference();
            std::cout << *pShape << std::endl;
            delete pShape;
        }
    }

    return 0;
}

BaseShape *CreateShape(int st)
{
    BaseShape *bs = NULL;
    switch (st)
    {
    case ELLIPSE:
        bs = new Ellipse(0, 20.0, 10.0);
        break;
    case CIRCLE:
        bs = new Circle(1, 10);
        break;
    case RECT:
        bs = new Rectangle(2, 20.0, 10.0);
        break;
    case SQUARE:
        bs = new Square(3, 10.0);
        break;
    default:
        std::cout << "Undefined Shape\n";
    }
    return bs;
}