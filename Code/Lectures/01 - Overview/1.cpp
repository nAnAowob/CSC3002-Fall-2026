#include <iostream>
using namespace std;

int main()
{
	enum direction
	{
		NORTH,
		EAST,
		WEST,
		SOUTH
	};

	direction d = EAST;

	switch (d)
	{
	case NORTH:
		cout << "A";
	case EAST:
		cout << "B";
	case WEST:
		cout << "C";
	case SOUTH:
		cout << "D";
		break;
	default:
		cout << "E";
	}
}