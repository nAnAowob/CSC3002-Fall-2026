#include <iostream>
#include <string>

using namespace std;

struct Vehicle {
	string model, owner, license;

	Vehicle(string model = "Unknown") : model(model), owner("NULL"), license("NULL") {}

	void ride() const {
		cout << "Riding a " << model << endl;
	}
};

struct eBike : public Vehicle {
	int speedLimit;

	eBike() : Vehicle("eBike"), speedLimit(0) {}
};

int main() {
	eBike myBike;
	myBike.ride();
	cout << "Speed limit: " << myBike.speedLimit << endl;

	return 0;
}