#include <iostream>

using namespace std;

struct Animal
{
public:
	virtual void MakeSound()
	{
		cout << "Animal make sound\n";
	}
};

struct Dog: public Animal
{
	public:
	void MakeSound() 
	{
		cout << "Dog is barking";
	}
};

int main() 
{
	Animal* d1 = new Dog();
	d1->MakeSound();
}