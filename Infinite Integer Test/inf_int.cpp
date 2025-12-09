#include "inf_int.h"
#include <algorithm>

inf_int::inf_int()
{
    this->digits = "0";
    this->thesign = true;
}

inf_int::inf_int(int n)
{
    int64_t nr = n; //signed integer(32bit) usage: 2^31 is not 32bit
    this->thesign = true;
    if (nr < 0) {
        nr = -nr;
        this->thesign = false;
    }
    digits = std::to_string(nr);
    std::reverse(digits.begin(), digits.end());
}

inf_int::inf_int(const string& str)
{
    this->thesign = (str[0] != '-');
    this->digits = this->thesign ? str : str.substr(1);
    std::reverse(digits.begin(), digits.end());
}

inf_int::inf_int(const inf_int& a)
{
    this->digits = a.digits;
    this->thesign = a.thesign;
}

inf_int::~inf_int() {}

inf_int& inf_int::operator=(const inf_int& a)
{
    this->digits = a.digits;
    this->thesign = a.thesign;
    return *this;
}

///////////////////////////////////////////////////////////////////////

inf_int inf_int::normalize(bool newsign)
{
    for (int i = this->digits.size()-1; i > 0 && this->digits[i] == '0'; i--)
        digits.pop_back();
    this->thesign = this->digits == "0" ? true : newsign;
    return *this;
}

inf_int inf_int::negative()
{
    inf_int result = *this;
    result.thesign = !result.thesign;
    return result;
}

///////////////////////////////////////////////////////////////////////

bool operator==(const inf_int& a, const inf_int& b)
{
    return (a.digits == b.digits && a.thesign == b.thesign);
}

bool operator!=(const inf_int& a, const inf_int& b) {
    return !(a == b);
}

bool operator<(const inf_int& a, const inf_int& b)
{
    if (a.thesign != b.thesign) return b.thesign;

    int an = a.digits.size(), bn = b.digits.size();
    if (an != bn) return a.thesign ? an < bn : an > bn;

    for (int i = an-1; i >= 0; i--) {
        if (a.digits[i] != b.digits[i])
            return a.thesign ? a.digits[i] < b.digits[i] : a.digits[i] > b.digits[i];
    }

    return false; //a == b
}

bool operator>(const inf_int& a, const inf_int& b)
{
    return !(a < b || a == b);
}

inf_int operator+(const inf_int& a, const inf_int& b)
{
    inf_int xa = a, xb = b;
    if (a.thesign != b.thesign) return xa - xb.negative();

    inf_int result("");
    int an = a.digits.size(), bn = b.digits.size();
    for (int i = 0, c = 0; i < an || i < bn || c; i++) {
        c += (i < an ? a.digits[i]-'0' : 0) + (i < bn ? b.digits[i]-'0' : 0);
        result.digits += c % 10 + '0';
        c /= 10; //carry
    }

    return result.normalize(a.thesign);
}

inf_int operator-(const inf_int& a, const inf_int& b)
{
    inf_int xa = a, xb = b;
    if (a.thesign != b.thesign) return xa + xb.negative();

    xa.thesign = xb.thesign = true;
    if (xa < xb) {
        inf_int result = xb - xa;
        result.thesign = !a.thesign;
        return result;
    }

    inf_int result("");
    int an = a.digits.size(), bn = b.digits.size();
    for (int i = 0, c = 0; i < an; i++) {
        c = a.digits[i] - (i < bn ? b.digits[i] : '0') - c;
        result.digits += c >= 0 ? c+'0' : c+'0'+10;
        c = (c >= 0) ? 0 : 1; //borrow
    }

    return result.normalize(a.thesign);
}

inf_int operator*(const inf_int& a, const inf_int& b)
{
    inf_int result("");
    inf_int xb = b;
    for (int i = 0; i < a.digits.size(); i++) {
        int n = a.digits[i] - '0';
        while (n--) result = result + xb;
        xb.digits.insert(xb.digits.begin(), '0');
    }
    return result.normalize(!(a.thesign ^ b.thesign));
}

ostream& operator<<(ostream& out, const inf_int& a)
{
    string str = a.digits;
    std::reverse(str.begin(), str.end());
    if (a.thesign == false) out << "-";
    out << str;
    return out;
}
