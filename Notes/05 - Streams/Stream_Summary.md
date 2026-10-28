{ Source } -- Input Stream --> Y {Variable} -- Output Stream --> {Destination}

![[Pasted image 20260923104349.png]]

```cpp
#include<iostream>
#include<string>
using namespace std;

int main() {
    string name;
    string tmp = "Enter a name: ";
    cout << tmp << endl;
    cin >> name;
    cout << "The name you entered: " << name << endl;
}
```
# C Stream

![[Pasted image 20260923110103.png|366]]![[Pasted image 20260923110336.png|317]]

# C++ Stream

- Stream = Object
- structure of the C++ stream classes as a representative example of inheritance hierarchies in an object-oriented language.

## Standard Output Stream *cout* and the Insertion Operator ( << )
```cpp
1. cout << "The total is " << total << endl;
2. <<(<<(<<(cout, "The total is "), total),endl);
```
![[Pasted image 20260923113035.png]]


## Standard Input Stream *cin* and the Extraction Operator ( >> )

| skipws<br>noskipws | skip whitespace<br>no skip whitespace | cin >> noskipws >> ch |
| ------------------ | ------------------------------------- | --------------------- |
|                    |                                       |                       |

```cpp
char a, b, c;
cout << "Enter at least 3 characters: ";
cin >> noskipws >> a >> ws >> b >> skipws >> c;
cout << a << b << c << endl;
```
## Overload the operators >> and << for user-defined data type
# Using Text Files
## Text files vs. String
| Text file                                                 | String                     |
| --------------------------------------------------------- | -------------------------- |
| permanent                                                 | temporary                  |
| exposed to all programs                                   | lives in a certain program |
| \<fstream>                                                | \<sstream>                 |
| accessed subsequently<br>(from beginning to end in order) |                            |
## String Streams





