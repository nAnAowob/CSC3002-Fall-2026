#pragma once

enum ShapeType
{
	ELLIPSE = 0,
	CIRCLE = 1,
	RECT = 2,
	SQUARE = 3,
	BASE = 4
};

class BaseShape
{
public: // allow to access from anywhere
	unsigned int mID = 0;

protected: // allow to access from derived class and within class
	ShapeType mType = BASE;
	double mCircumference = 0.0;
	double mArea = 0.0;

private: // allow to access from this class only.
	int privateData = 0;

public:
	BaseShape();
	BaseShape(unsigned int id);
	BaseShape(unsigned int id, ShapeType type = BASE);

	double getCircumfenrence() { return mCircumference; }
	double getArea() { return mArea; }

	virtual std::string toString();
	virtual double calcCircumference() = 0; // pure virtural method
	virtual double calcArea() = 0;		// pure virtual method
	virtual ~BaseShape() = 0;

	friend std::ostream &operator<<(std::ostream &os, BaseShape &sp);
};