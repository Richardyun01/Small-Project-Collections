#ifndef _INF_INT_H_
#define _INF_INT_H_

#include <iostream>
#include <string>

using namespace std;

class inf_int {
private :
    string digits;  // absolute value
    bool thesign;   // true if positive, false if negative
    // ex) 15311111111111111 -> digits="11111111111111351", thesign=true;
    // ex) -12345555555555 -> digits="55555555554321", thesign=false

    inf_int normalize(bool newsign); // remove tailing '0' if exist
    inf_int negative();              // negative sign

public :
    inf_int();               // assign 0 as a default value
    inf_int(int);
    inf_int(const string&);
    inf_int(const inf_int&); // copy constructor
    ~inf_int();              // destructor

    inf_int& operator=(const inf_int&); // assignment operator

    friend bool operator==(const inf_int&, const inf_int&);
    friend bool operator!=(const inf_int&, const inf_int&);
    friend bool operator>(const inf_int&, const inf_int&);
    friend bool operator<(const inf_int&, const inf_int&);

    friend inf_int operator+(const inf_int&, const inf_int&);
    friend inf_int operator-(const inf_int&, const inf_int&);
    friend inf_int operator*(const inf_int&, const inf_int&);
    // friend inf_int operator/(const inf_int& , const inf_int&); // not required

    friend ostream& operator<<(ostream&, const inf_int&);
    // friend istream& operator>>(istream&, inf_int&); // not required
};

#endif
