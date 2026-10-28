#include <iostream>
#include <sstream>
#include <string>
#include "Rectangle.h"

using namespace std;

Rectangle::Rectangle(unsigned int id, double length, double width, ShapeType type)
{
	mLength = length;
	mWidth = width;
	mType = type;
	mID = id;
}

double Rectangle::calcCircumference()
{
	mCircumference = (mLength + mWidth) * 2;
	return mCircumference;
}

double Rectangle::calcArea()
{
	mArea = mLength * mWidth;
	return mArea;
}

std::string Rectangle::toString()
{
	string sType = (mType == RECT) ? "RECT" : "SQAURE";
	std::ostringstream oss;
	oss << "ID=" << mID << std::endl
	    << "Type=" << sType << std::endl;
	oss << "Length=" << mLength << std::endl;
	 if(mType == RECT) oss  << "Width=" << mWidth << std::endl;
	oss << "Circumference=" << mCircumference << std::endl;
	oss << "Area=" << mArea << std::endl;
	return oss.str();
}

Rectangle::~Rectangle()
{
}