#include <iostream>

using namespace std;

int update(int x, int &y)
{
	x += 2;
	y += x;
	return x + y;
}

int main()
{
	int a = 3;
	int b = 4;
	int c = update(a, b);

	cout << a << " " << b << " " << c << "\n";

	int &r = a;
	r = b;
	r++;

	cout << a << " " << b << " " << r << "\n";
}
int x = 1; // Global
void f()
{
	int x = 2; // Hides global x
	{
		int y = x;
	} // y's scope/lifetime end here
}