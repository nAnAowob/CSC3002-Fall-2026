#include<iostream>

using namespace std;

int *createIndexArray(int n)
{
	int *array = new int[n];
	for (int i = 0; i < n; i++)
	{
		array[i] = i;
	}
	return array;
}
int main()
{
	int *digits = createIndexArray(10);
	int a = digits;
	cout << digits << " " << *(digits+1) << " " << *digits << endl;
	while (digits != a+10) 
	{
		cout << *(digits++);
	}
	delete[] digits;
}