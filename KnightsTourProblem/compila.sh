base=$(basename $1 .cpp)

g++ -I/home/denis/gecode-4.3.1/include/ -c $base.cpp

g++ -Wl,-rpath,/home/denis/gecode-4.3.1/ -o $base -L/home/denis/gecode-4.3.1/lib $base.o  -lgecodedriver -lgecodegist -lgecodesearch -lgecodeminimodel -lgecodeint -lgecodekernel -lgecodesupport
