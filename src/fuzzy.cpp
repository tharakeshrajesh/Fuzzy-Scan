#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <fuzzy.h>

int main() {
    system("pause");

    FILE* file = fopen("test.txt", "rb");
    if (!file) {
        std::cerr << "Failed to open file." << std::endl;
        return 1;
    }

    char result[FUZZY_MAX_RESULT];
    int ret = fuzzy_hash_file(file, result);

    fclose(file);

    if (ret == 0) {
        std::cout << "Fuzzy hash: " << result << std::endl;
    } else {
        std::cerr << "Hashing failed with code: " << ret << std::endl;
    }

    system("pause");

    return 0;
}
