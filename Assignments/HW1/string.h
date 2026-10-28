#pragma once
#include <iostream>

namespace mystring {

const int maxlen = 1024;

struct str {
    char data[maxlen + 1] = {'\0'};
    // Function: Copy a str object.
    // Input: src - source string.
    // Returns: Reference to this object.

    str& operator=(const str& src);
    // Function: Copy a C-style string.
    // Input: src - source character array.
    // Returns: Reference to this object.

    str& operator=(const char* src);
    // Function: Copy constructor.
    // Input: other - source string.
    // Returns: None.

    str(const str& other) { *this = other; }
    // Function: Construct from a C-style string.
    // Input: src - source character array.
    // Returns: None.
    str(const char* src) { *this = src; }
    // Function: Default constructor.
    // Input: None.
    // Returns: None.
    str() = default;
};

// Function: Copy a str object.
// Input: dest - destination; src - source.
// Returns: None.
void str_copy(str& dest, const str& src);
// Function: Copy a C-style string.
// Input: dest - destination; src - source.
// Returns: None.
void str_copy(str& dest, const char* src);

// Function: Concatenate two str objects.
// Input: dest - destination; src1, src2 - inputs.
// Returns: None.
void str_concat(str& dest, const str& src1, const str& src2);
// Function: Concatenate str and C-style strings.
// Input: dest - destination; src, cstr - inputs.
// Returns: None.
void str_concat(str& dest, const str& src, const char* cstr);
// Function: Concatenate C-style and str strings.
// Input: dest - destination; cstr, src - inputs.
// Returns: None.
void str_concat(str& dest, const char* cstr, const str& src);

// Function: Get string length.
// Input: s - source string.
// Returns: Number of stored characters.
int str_len(const str& s);
// Function: Clear a string.
// Input: s - string to clear.
// Returns: None.
void str_clear(str& s);
// Function: Convert letters to uppercase.
// Input: src - source string.
// Returns: Converted copy of src.
str upper(const str& src);
// Function: Convert letters to lowercase.
// Input: src - source string.
// Returns: Converted copy of src.
str lower(const str& src);

// Function: Test string equality.
// Input: lhs, rhs - strings to compare.
// Returns: true when contents are equal.
bool operator==(const str& lhs, const str& rhs);
// Function: Test string inequality.
// Input: lhs, rhs - strings to compare.
// Returns: true when contents differ.
bool operator!=(const str& lhs, const str& rhs);
// Function: Test lexicographical order.
// Input: lhs, rhs - strings to compare.
// Returns: true when lhs precedes rhs.
bool operator<(const str& lhs, const str& rhs);
// Function: Test lexicographical order.
// Input: lhs, rhs - strings to compare.
// Returns: true when lhs follows rhs.
bool operator>(const str& lhs, const str& rhs);
// Function: Test lexicographical order.
// Input: lhs, rhs - strings to compare.
// Returns: true when lhs is not after rhs.
bool operator<=(const str& lhs, const str& rhs);
// Function: Test lexicographical order.
// Input: lhs, rhs - strings to compare.
// Returns: true when lhs is not before rhs.
bool operator>=(const str& lhs, const str& rhs);

// Function: Concatenate two str objects.
// Input: lhs, rhs - strings to concatenate.
// Returns: New concatenated string.
str operator+(const str& lhs, const str& rhs);
// Function: Concatenate str and C-style strings.
// Input: lhs, rhs - strings to concatenate.
// Returns: New concatenated string.
str operator+(const str& lhs, const char* rhs);
// Function: Concatenate C-style and str strings.
// Input: lhs, rhs - strings to concatenate.
// Returns: New concatenated string.
str operator+(const char* lhs, const str& rhs);
// Function: Append a str object.
// Input: lhs - destination; rhs - appended string.
// Returns: Reference to lhs.
str& operator+=(str& lhs, const str& rhs);
// Function: Append a C-style string.
// Input: lhs - destination; rhs - appended string.
// Returns: Reference to lhs.
str& operator+=(str& lhs, const char* rhs);
// Function: Write a string to a stream.
// Input: os - output stream; s - string to write.
// Returns: Reference to os.
std::ostream& operator<<(std::ostream& os, const str& s);
// Function: Read one word from a stream.
// Input: is - input stream; s - destination string.
// Returns: Reference to is.
std::istream& operator>>(std::istream& is, str& s);

} // namespace mystring