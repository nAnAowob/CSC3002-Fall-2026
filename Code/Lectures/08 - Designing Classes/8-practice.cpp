#include <iostream>
#include <string>

using namespace std;

class BankAccount
{
private:
	string owner;
	double balance;

public:
	BankAccount(string s, double b)
	{
		owner = s;
		balance = b;
	}
	BankAccount() 
	{
		owner = "NULL";
		balance = 0.00;
	}
	void deposit(double amount)
	{
		double temp = balance;
		temp += amount;
		balance = temp;
	}
	void withdraw(double amount)
	{
		balance -= amount;
	}
	double getBalance() const
	{
		return balance;
	}
	void display() const
	{
		cout << "Owner: " << owner << endl;
		cout << "Balance: " << getBalance() << endl;
	}
};

int main()
{
	BankAccount acc("AnnAnn", 1000);
	BankAccount acc2();
	
	cout << acc2.getbalance() << endl;
	
	acc.deposit(500);
	acc.withdraw(200);
	acc.display();

	cout << acc.getBalance() << endl;

	return 0;
}
