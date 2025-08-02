cd /d/Tharakesh/Scripts/Fuzzy\ Scan/build
cmake -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release ..
mingw32-make
cp /d/Tharakesh/Scripts/Fuzzy\ Scan/third_party/ssdeep/build/fuzzy.dll /d/Tharakesh/Scripts/Fuzzy\ Scan/build