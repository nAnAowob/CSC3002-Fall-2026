#include <iostream>
#include <string>

using namespace std;

struct Student;
void printStudent(const Student &student);

struct Student
{
	string name;
	int id;
	double gpa;
	Student(string s, int n, double g) : name(s), id(n), gpa(g)
	{
		printStudent(*this);
	}
};

struct Course
{
	string name;
	Student studentInfo;
	Course(string s, Student n) : name(s), studentInfo(n) {}
};

void printStudent(const Student &student)
{
	cout << student.name << " (" << student.id << "): " << student.gpa << "\n";
}

void updateGpa(Student &student, double newGpa)

{
	if (newGpa <= 4.0 && newGpa >= 0.0)
	{
		student.gpa = newGpa;
	}
}

double averageGpa(const Student students[], int count)
{
	double sum = 0;
	for (int i = 0; i < count; i++)
	{
		sum += students[i].gpa;
	}
	return sum / count;
	// Return the average GPA. Assume count > 0.
}

void printCourse(const Course &course)
{
	cout << course.name << "\n";
	printStudent(course.studentInfo);
	// Print the course name, then its representative's information.
}

int main()
{
	Student alex("Alex", 1001, 3.8);
	Course course("CSC3002", alex);

	printCourse(course);
}