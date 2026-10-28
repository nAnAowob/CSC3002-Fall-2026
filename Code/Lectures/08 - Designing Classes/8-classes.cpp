#include<iostream>
#include <string>
using namespace std;

class Student {
    
    public:
        string Name;
        string College;
        string School;
        int ClassOf;
        double cGPA;
        //Rating(int B35, int B15);
        //int getRating();
    private:
        int Rating = 0;
        // 1. Store the credits already included in this student's cGPA.
        int totalCredits = 0;

    public:
        // 2. Declare the method here so main() can call it.
        // GPA is one course's grade point; credit is that course's credits.
        void calculateCGPA(double GPA, int credit);

        Student(string Name) {
            this->Name = Name;
            College = "N/A";
            ClassOf = 0;
            cGPA = 0.00;
        }

    void GetInfo() {
        cout << Name << endl;
        cout << College << endl;
        cout << "----------\n"; 
    }

    void SetCollege(string college) {
        College = college;
    }
    void GetRating() {
        cout << Rating;
    }
};

// 3. Define the method outside the class using Student::.
// The return type and parameters must match the declaration above.
void Student::calculateCGPA(double GPA, int credit) {
    if (credit <= 0) {
        cout << "Course credits must be positive." << endl;
        return;
    }

    // Use the OLD totalCredits to recover the previous weighted total.
    cGPA = (cGPA * totalCredits + GPA * credit)
         / (totalCredits + credit);
    totalCredits += credit;
}
int main() {
    Student student("AnnAnn");
    cout << student.Name << endl;
    student.GetInfo();
    student.SetCollege("Diligentia");
    student.GetInfo();

    // 4. Call once per course; each call includes another course in cGPA.
    student.calculateCGPA(4.0, 3);
    cout << "After course 1: " << student.cGPA << endl; // 4
    student.calculateCGPA(3.0, 2);
    cout << "After course 2: " << student.cGPA << endl; // 3.6
}

// class Maimai{
//     public:
//         int scorelist[1000] = {};
//         int
//     private:
// };

// class Songs {
//     public:
//         string Difficulty;
//         double level;
//         string Version;
//         double Accuracy;
// };
