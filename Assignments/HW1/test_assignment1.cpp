// Public self-test for Assignment 1.  Compile this file with string.cpp.

/*
g++ -std=c++17 -Wall -Wextra -pedantic string.cpp test_assignment1.cpp -o test_assignment1
*/

#include <iostream>
#include <sstream>
#include <string>
#include "string.h"

using mystring::str;

namespace {
int passed = 0;
int total = 0;

void check(bool condition, const char* label) {
    ++total;
    if (condition) {
        ++passed;
        std::cout << "PASS | " << label << '\n';
    } else {
        std::cout << "FAIL | " << label << '\n';
    }
}

std::string value(const str& s) { return std::string(s.data); }
str make(const char* text) { return str(text); }

void test_construction_and_copy() {
    str empty;
    check(value(empty).empty(), "default construction");
    str a = "Alpha", b(a), c;
    c = a;
    str d; d = "Delta";
    check(value(a) == "Alpha" && value(b) == "Alpha" && value(c) == "Alpha" && value(d) == "Delta",
          "constructors and assignment");
    mystring::str_copy(c, d);
    mystring::str_copy(d, "Omega");
    check(value(c) == "Delta" && value(d) == "Omega", "str_copy overloads");
}

void test_functions() {
    str a = "Hello", b = " world", out;
    mystring::str_concat(out, a, b);
    check(value(out) == "Hello world", "str_concat(str, str)");
    mystring::str_concat(out, a, "!");
    check(value(out) == "Hello!", "str_concat(str, const char*)");
    mystring::str_concat(out, "Say: ", a);
    check(value(out) == "Say: Hello", "str_concat(const char*, str)");
    check(mystring::str_len(out) == 10 && mystring::str_len(make("")) == 0, "str_len");
    mystring::str_clear(out);
    check(value(out).empty(), "str_clear");
    check(value(mystring::upper(make("aZ 09!"))) == "AZ 09!" &&
          value(mystring::lower(make("aZ 09!"))) == "az 09!", "upper and lower");
}

void test_operators_and_streams() {
    str apple = "apple", apple2 = "apple", banana = "banana";
    check(apple == apple2 && apple != banana && apple < banana && banana > apple &&
          apple <= apple2 && banana >= apple2, "comparison operators");
    check(value(apple + banana) == "applebanana" && value(apple + " pie") == "apple pie" &&
          value("green " + apple) == "green apple", "operator+ overloads");
    str text = "start", suffix = " middle";
    str& first = (text += suffix);
    str& second = (text += " end");
    check(value(text) == "start middle end" && &first == &text && &second == &text,
          "operator+= overloads and return");
    std::ostringstream output;
    output << make("stream test");
    std::istringstream input("one two");
    str word;
    input >> word;
    check(output.str() == "stream test" && value(word) == "one", "stream operators");
}

void test_capacity() {
    const std::string long_text(static_cast<std::size_t>(mystring::maxlen) + 20, 'x');
    str truncated = long_text.c_str();
    check(mystring::str_len(truncated) == mystring::maxlen && truncated.data[mystring::maxlen] == '\0',
          "maxlen truncation and terminator");
    str left = "ab", right = long_text.c_str(), joined;
    mystring::str_concat(joined, left, right);
    check(mystring::str_len(joined) == mystring::maxlen && value(joined).substr(0, 2) == "ab",
          "bounded concatenation");
}
}

int main() {
    test_construction_and_copy();
    test_functions();
    test_operators_and_streams();
    test_capacity();
    const double score = total == 0 ? 0.0 : 10.0 * passed / total;
    std::cout << "SUMMARY | " << passed << " / " << total << " tests passed\n";
    std::cout << "PUBLIC SELF-TEST SCORE | " << score << " / 10.0\n";
    return passed == total ? 0 : 1;
}