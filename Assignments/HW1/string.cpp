// ----- Chompunick Chieng | 125010008 | Assignment 1, CSC3002 Fall 2026 ----- //

#include "string.h"

namespace mystring
{

    str &str::operator=(const str &src)
    {
        int i = 0;
        while (src.data[i] != '\0' && i < maxlen)
        {
            data[i] = src.data[i];
            ++i;
        }
        data[i] = '\0';
        return *this;
    }

    str &str::operator=(const char *src)
    {
        int i = 0;
        while (src[i] != '\0' && i < maxlen)
        {
            data[i] = src[i];
            ++i;
        }
        data[i] = '\0';
        return *this;
    }

    void str_copy(str &dest, const str &src)
    {
        int i = 0;
        while (src.data[i] != '\0' && i < maxlen)
        {
            dest.data[i] = src.data[i];
            i++;
        }
        dest.data[i] = '\0';
    }

    void str_copy(str &dest, const char *src)
    {
        int i = 0;
        while (src[i] != '\0' && i < maxlen)
        {
            dest.data[i] = src[i];
            i++;
        }
        dest.data[i] = '\0';
    }

    void str_concat(str &dest, const str &src1, const str &src2)
    {
        int i = 0;
        int i2 = 0;
        while (src1.data[i] != '\0' && i < maxlen)
        {
            dest.data[i] = src1.data[i];
            i++;
        }
        while (src2.data[i2] != '\0' && i < maxlen)
        {
            dest.data[i] = src2.data[i2];
            i++;
            i2++;
        }
        dest.data[i] = '\0';
    }

    void str_concat(str &dest, const str &src, const char *cstr)
    {
        int i = 0, i2 = 0;
        while (src.data[i] != '\0' && i < maxlen)
        {
            dest.data[i] = src.data[i];
            i++;
        }
        while (cstr[i2] != '\0' && i < maxlen)
        {
            dest.data[i] = cstr[i2];
            i++;
            i2++;
        }
        dest.data[i] = '\0';
    }

    void str_concat(str &dest, const char *cstr, const str &src)
    {
        int i = 0, i2 = 0;
        while (cstr[i] != '\0' && i < maxlen)
        {
            dest.data[i] = cstr[i];
            i++;
        }
        while (src.data[i2] != '\0' && i < maxlen)
        {
            dest.data[i] = src.data[i2];
            i++;
            i2++;
        }
        dest.data[i] = '\0';
    }

    int str_len(const str &s)
    {
        int i = 0;
        while (s.data[i] != '\0' && i < maxlen)
        {
            i++;
        }
        return i;
    }

    void str_clear(str &s)
    {
        s.data[0] = '\0';
    }

    str upper(const str &src)
    {
        str result;
        int i = 0;
        while (src.data[i] != '\0' && i < maxlen)
        {
            char tmp = src.data[i];
            if (tmp >= 'a' && tmp <= 'z')
            {
                tmp -= ('a' - 'A');
            }
            result.data[i] = tmp;
            i++;
        }
        result.data[i] = '\0';
        return result;
    }

    str lower(const str &src)
    {
        str result;
        int i = 0;
        while (src.data[i] != '\0' && i < maxlen)
        {
            char tmp = src.data[i];
            if (tmp >= 'A' && tmp <= 'Z')
            {
                tmp += ('a' - 'A');
            }
            result.data[i] = tmp;
            i++;
        }
        result.data[i] = '\0';
        return result;
    }

    bool operator==(const str &lhs, const str &rhs)
    {
        int i = 0;
        if (str_len(lhs) != str_len(rhs))
        {
            return false;
        }
        while (lhs.data[i] != '\0' && i < maxlen)
        {
            if (lhs.data[i] != rhs.data[i])
            {
                return false;
            }
            i++;
        }
        return true;
    }
    bool operator!=(const str &lhs, const str &rhs)
    {
        int i = 0;
        if (str_len(lhs) != str_len(rhs))
        {
            return true;
        }
        while (lhs.data[i] != '\0' && i < maxlen)
        {
            if (lhs.data[i] != rhs.data[i])
            {
                return true;
            }
            i++;
        }
        return false;
    }

    bool operator<(const str &lhs, const str &rhs)
    {
        int i = 0;
        while ((lhs.data[i] != '\0' || rhs.data[i] != '\0') && i < maxlen)
        {
            if (lhs.data[i] == rhs.data[i])
            {
                i++;
                continue;
            }
            else if (lhs.data[i] > rhs.data[i])
            {
                return false;
            }
            return true;
        }
        // example case: lhs = trees, rhs = tree
        return false;
    }

    bool operator>(const str &lhs, const str &rhs)
    {
        int i = 0;
        while ((lhs.data[i] != '\0' || rhs.data[i] != '\0') && i < maxlen)
        {
            if (lhs.data[i] == rhs.data[i])
            {
                i++;
                continue;
            }
            else if (lhs.data[i] < rhs.data[i])
            {
                return false;
            }
            return true;
        }
        return false;
    }

    bool operator<=(const str &lhs, const str &rhs)
    {
        int i = 0;
        while ((lhs.data[i] != '\0' || rhs.data[i] != '\0') && i < maxlen)
        {
            if (lhs.data[i] == rhs.data[i])
            {
                i++;
                continue;
            }
            else if (lhs.data[i] > rhs.data[i])
            {
                return false;
            }
            return true;
        }
        // example case: lhs = trees, rhs = tree
        return true;
    }

    bool operator>=(const str &lhs, const str &rhs)
    {
        int i = 0;
        while ((lhs.data[i] != '\0' || rhs.data[i] != '\0') && i < maxlen)
        {
            if (lhs.data[i] == rhs.data[i])
            {
                i++;
                continue;
            }
            else if (lhs.data[i] < rhs.data[i])
            {
                return false;
            }
            return true;
        }
        return true;
    }

    str operator+(const str &lhs, const str &rhs)
    {
        str result;
        int i1 = 0, i2 = 0;
        while (lhs.data[i1] != '\0' && i1 < maxlen)
        {
            result.data[i1] = lhs.data[i1];
            i1++;
        }
        while (rhs.data[i2] != '\0' && i1 < maxlen)
        {
            result.data[i1] = rhs.data[i2];
            i1++;
            i2++;
        }
        return result;
    }

    str operator+(const str &lhs, const char *rhs)
    {
        str result;
        int i1 = 0, i2 = 0;
        while (lhs.data[i1] != '\0' && i1 < maxlen)
        {
            result.data[i1] = lhs.data[i1];
            i1++;
        }
        while (rhs[i2] != '\0' && i1 < maxlen)
        {
            result.data[i1] = rhs[i2];
            i1++;
            i2++;
        }
        return result;
    }

    str operator+(const char *lhs, const str &rhs)
    {
        str result;
        int i1 = 0, i2 = 0;
        while (lhs[i1] != '\0' && i1 < maxlen)
        {
            result.data[i1] = lhs[i1];
            i1++;
        }
        while (rhs.data[i2] != '\0' && i1 < maxlen)
        {
            result.data[i1] = rhs.data[i2];
            i1++;
            i2++;
        }
        return result;
    }

    str &operator+=(str &lhs, const str &rhs)
    {
        str tmp = rhs;
        int len = str_len(lhs);
        int i = 0;
        while (rhs.data[i] != '\0' && len < maxlen)
        {
            lhs.data[len] = tmp.data[i];
            len++;
            i++;
        }
        lhs.data[len] = '\0';
        return lhs;
    }
    str &operator+=(str &lhs, const char *rhs)
    {
        str tmp = rhs;
        int len = str_len(lhs);
        int i = 0;
        while (rhs[i] != '\0' && len < maxlen)
        {
            lhs.data[len] = tmp.data[i];
            len++;
            i++;
        }
        lhs.data[len] = '\0';
        return lhs;
    }

    std::ostream &operator<<(std::ostream &os, const str &s)
    {
        int i = 0;
        while (s.data[i] != '\0' && i < maxlen)
        {
            os.put(s.data[i]);
            i++;
        }
        return os;
    }

    std::istream &operator>>(std::istream &is, str &s)
    {
        is >> std::ws;
        int i = 0;
        while (true)
        {
            int next = is.peek();
            if (next == EOF)
            {
                break;
            }
            if (next == ' ' || next == '\t' || next == '\n' || next == '\r' || next == '\f' || next == '\v')
            {
                break;
            }
            is.get();
            if (i < maxlen)
            {
                s.data[i] = next;
                i++;
            }
        }
        s.data[i] = '\0';
        return is;
    }
    // Implement all remaining declarations from string.h below.

} // namespace mystring