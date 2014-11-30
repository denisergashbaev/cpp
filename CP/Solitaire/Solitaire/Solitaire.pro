TEMPLATE = app
CONFIG += console
CONFIG -= app_bundle
CONFIG -= qt
QMAKE_CXXFLAGS += -std=c++11
SOURCES += main.cpp
INCLUDEPATH += $HOME/gecode-4.3.1/include/
LIBS += -LD:$HOME/gecode-4.3.1/lib  -lgecodedriver -lgecodegist -lgecodesearch -lgecodeminimodel -lgecodeint -lgecodekernel -lgecodesupport

OTHER_FILES += \
    Benchmark/Readme.txt \
    Benchmark/solit_4_4_9.txt \
    Benchmark/solit_4_4_8.txt \
    Benchmark/solit_4_4_7.txt \
    Benchmark/solit_4_4_6.txt \
    Benchmark/solit_4_4_5.txt \
    Benchmark/solit_4_4_4.txt \
    Benchmark/solit_4_4_3.txt \
    Benchmark/solit_4_4_2.txt \
    Benchmark/solit_4_4_1.txt \
    Benchmark/solit_4_4_0.txt \
    Benchmark/solit_4_7_9.txt \
    Benchmark/solit_4_7_8.txt \
    Benchmark/solit_4_7_7.txt \
    Benchmark/solit_4_7_6.txt \
    Benchmark/solit_4_7_5.txt \
    Benchmark/solit_4_7_4.txt \
    Benchmark/solit_4_7_3.txt \
    Benchmark/solit_4_7_2.txt \
    Benchmark/solit_4_7_1.txt \
    Benchmark/solit_4_7_0.txt \
    Benchmark/solit_4_13_9.txt \
    Benchmark/solit_4_13_8.txt \
    Benchmark/solit_4_13_7.txt \
    Benchmark/solit_4_13_6.txt \
    Benchmark/solit_4_13_5.txt \
    Benchmark/solit_4_13_4.txt \
    Benchmark/solit_4_13_3.txt \
    Benchmark/solit_4_13_2.txt \
    Benchmark/solit_4_13_1.txt \
    Benchmark/solit_4_13_0.txt \
    Benchmark/solit_4_10_0.txt \
    Benchmark/solit_4_10_9.txt \
    Benchmark/solit_4_10_8.txt \
    Benchmark/solit_4_10_7.txt \
    Benchmark/solit_4_10_6.txt \
    Benchmark/solit_4_10_5.txt \
    Benchmark/solit_4_10_4.txt \
    Benchmark/solit_4_10_3.txt \
    Benchmark/solit_4_10_2.txt \
    Benchmark/solit_4_10_1.txt
