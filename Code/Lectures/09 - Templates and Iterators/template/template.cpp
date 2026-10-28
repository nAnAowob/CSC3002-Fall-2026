#include <iostream>
#include "max.h"

using namespace std;

int main()
{
	Print(10, 3.14);
	Print("Age", 19);

	cout << Max(3, 5) << endl;
	cout << Max(2.5, 4.8) << endl;
	cout << Max('a', 'z') << endl;
	cout << Max<double>(3.0, 4) << endl;
	cout << Min<double>(3.0, 4);
}
