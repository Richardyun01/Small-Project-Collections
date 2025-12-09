#include "inf_int.h"
#include <iostream>

using namespace std;

int main()
{
    while (1) {
        string a, b, op;
        cout << "Input: ";
        cin >> a;
        if (a == "0") break;
        cin >> op >> b;

        if (op == "+")
            cout << "Output: " << inf_int(a) + inf_int(b) << endl;
        else if (op == "-")
            cout << "Output: " << inf_int(a) - inf_int(b) << endl;
        else if (op == "*")
            cout << "Output: " << inf_int(a) * inf_int(b) << endl;
        else
            cout << "Invalid operator" << endl;
    }

	return 0;
}
