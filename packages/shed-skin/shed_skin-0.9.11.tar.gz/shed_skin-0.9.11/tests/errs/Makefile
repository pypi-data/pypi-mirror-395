# project variables
SHEDSKIN_LIBDIR=$(HOME)/shedskin/shedskin/lib
CPPFILES=$(GENERATED_CPPFILES) $(BUILTIN_CPPFILES)
HPPFILES=$(GENERATED_HPPFILES) $(BUILTIN_HPPFILES)

INCLUDEDIRS=-I$(CURDIR) -I$(SHEDSKIN_LIBDIR) -I/usr/include -I/usr/local/include
LINKDIRS=-L/usr/lib -L/usr/local/lib

CXX=g++
CXXFLAGS+=-O2 -std=c++20 -march=native $(CPPFLAGS) $(INCLUDEDIRS)
LDFLAGS+= $(LINKDIRS)
LDLIBS=-lgc -lgctba -lutil

BUILTIN_CPPFILES=$(SHEDSKIN_LIBDIR)/builtin.cpp
BUILTIN_HPPFILES=$(SHEDSKIN_LIBDIR)/builtin.hpp
GENERATED_CPPFILES=$(CURDIR)/46.cpp
GENERATED_HPPFILES=$(CURDIR)/46.hpp

.PHONY: all clean

46: $(CPPFILES) $(HPPFILES)
	$(CXX)  $(CXXFLAGS) $(CPPFILES) $(LDLIBS) $(LDFLAGS) -o 46

46_debug: $(CPPFILES) $(HPPFILES)
	$(CXX) -g -ggdb $(CXXFLAGS) $(CPPFILES) $(LDLIBS) $(LDFLAGS) -o 46_debug

46_prof: $(CPPFILES) $(HPPFILES)
	$(CXX) -pg -ggdb $(CXXFLAGS) $(CPPFILES) $(LDLIBS) $(LDFLAGS) -o 46_prof

all: 46

clean:
	@rm -rf 46 46_prof 46_debug

reset: clean
	@rm -f $(GENERATED_CPPFILES) $(GENERATED_HPPFILES)

