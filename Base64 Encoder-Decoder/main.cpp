#include <iostream>
#include <string>
#include <vector>

static const std::string base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

std::vector<int> base64_decode_table(256, -1);

void build_decode_table() {
    for (int i = 0; i < 64; ++i) {
        base64_decode_table[base64_chars[i]] = i;
    }
}

std::string base64_encode(const std::string &in) {
    std::string out;
    int val = 0, valb = -6;

    for (unsigned char c : in) {
        val = (val << 8) + c;
        valb += 8;
        while (valb >= 0) {
            out += base64_chars[(val >> valb) & 0x3F];
            valb -= 6;
        }
    }

    if (valb > -6)
        out += base64_chars[((val << 8) >> (valb + 8)) & 0x3F];

    while (out.size() % 4)
        out += '=';

    return out;
}

std::string base64_decode(const std::string &in) {
    static bool table_built = false;

    if (!table_built) {
        build_decode_table();
        table_built = true;
    }

    std::string out;
    int val = 0, valb = -8;

    for (unsigned char c : in) {
        if (base64_decode_table[c] == -1)
            break;

        val = (val << 6) + base64_decode_table[c];
        valb += 6;

        if (valb >= 0) {
            out += static_cast<char>((val >> valb) & 0xFF);
            valb -= 8;
        }
    }

    return out;
}

int main()
{
    std::string message = "This is a test message.";
    std::string encoded = base64_encode(message);
    std::string decoded = base64_decode(encoded);

    std::cout << "Original message: " << message << std::endl;
    std::cout << "Encoded message: " << encoded << std::endl;
    std::cout << "Decoded message: " << decoded << std::endl;

    return 0;
}
