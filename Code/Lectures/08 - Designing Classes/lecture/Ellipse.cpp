#include <iostream>
#include <sstream>
#include <string>
#include "BaseShape.h"
#include "Ellipse.h"

using namespace std;

Ellipse::Ellipse(unsigned int id, double a, double b, ShapeType type)
{
	mSemiMajor = a;
	mSemiMinor = b;
	mType = type;
	mID = id;
}

double Ellipse::calcCircumference()
{
	double a = mSemiMajor;
	double b = mSemiMinor;
	mCircumference = 3.1415926*sqrt(2*(a*a+b*b));
	return mCircumference;
}

double Ellipse::calcArea()
{
	mArea = 3.1415926 * mSemiMajor * mSemiMinor;
	return mArea;
}

std::string Ellipse::toString()
{
	string sType = (mType == ELLIPSE) ? "ELLIPSE" : "CIRCLE";
	std::ostringstream oss;

	oss << "ID=" << mID << std::endl
	    << "Type=" << sType << std::endl;
	if(mType == ELLIPSE)
	{
		oss << "SemiMajor=" << mSemiMajor << std::endl
	    << "SemiMinor=" << mSemiMinor << std::endl;
	}
	else
	{
		oss << "Radious=" << mSemiMajor << std::endl;
	}
	oss << "Circumference=" << mCircumference << std::endl;
	oss << "Area=" << mArea << std::endl;
	return oss.str();
}

Ellipse::~Ellipse()
{
}