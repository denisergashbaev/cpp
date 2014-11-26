TEMPLATE = app
CONFIG += console
CONFIG -= app_bundle
CONFIG -= qt
QMAKE_CXXFLAGS += -std=c++11
SOURCES += main.cpp
INCLUDEPATH += $HOME/gecode-4.3.1/include/
LIBS += -LD:$HOME/gecode-4.3.1/lib  -lgecodedriver -lgecodegist -lgecodesearch -lgecodeminimodel -lgecodeint -lgecodekernel -lgecodesupport
