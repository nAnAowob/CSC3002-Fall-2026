#include <iostream>
#include <string>
#include <sstream>
using namespace std;

// int main() {
//     string name;
//     string tmp = "Enter a name: ";
//     cout << tmp << endl;
//     cin >> name;
//     cout << "The name you entered: " << name << endl;
// }

// #include <fstream>
// #include <cctype>

// int main() {
//     ifstream ifile;
//     ofstream ofile;
//     string instr;
//     ifile.open("Myfile.txt"); //open the input filestream
//     ofile.open("Output.txt",ios::out);
//     while (!ifile.eof())  {
//         getline(ifile, instr);
//         cout << instr << endl;
//         ofile << instr << endl;
//     }

//     //you need to close the file every time, otherwise other ppl cannot use it.
// }
int main()
{
	// char a, b, c;
	// cout << "Enter at least 3 characters: ";
	// cin >> noskipws >> a >> ws >> b >> skipws >> c;
	// cout << a << b << c << endl;
	// cin >> data;
	// cout << data;

	// cin >> data;
	// cout << data;

	// read from in object, put it into data
	istringstream in("24\nAda Lovelace\n");
	int id;
	string line;
	in >> id;
	getline(in, line);
	cout << id << ":[" << line << "]\n";
	getline(in, line);
	cout << '[' << line << "]\n";
}
