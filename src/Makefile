
# to build,
# run "make"
# to build with duma,
# run "make USE_DUMA=1"

CC=gcc
CXX=g++
RM=rm -f
ENDIANNESS=LITTLE_ENDIAN
CXXFLAGS+=-fPIC -D__$(ENDIANNESS)__ -Wall -Wextra

SRCS=sfklCoding.cpp sfklCrunch.cpp sfklDiff.cpp sfklFile.cpp sfklLPC.cpp sfklString.cpp sfklZip.cpp sfarkxtc.cpp
OBJS=$(subst .cpp,.o,$(SRCS))

# add a reference to zlib, and optionally duma
ifeq ($(USE_DUMA),1)
        LDLIBS=-lz ./duma/libduma.a
else
        LDLIBS=-lz
endif

all: sfarkxtc_out

sfarkxtc_out: $(OBJS)
	$(CXX) $(LDFLAGS) -o sfarkxtc_out $(OBJS) $(LDLIBS) 

depend: .depend

.depend: $(SRCS)
	$(RM) ./.depend
	$(CXX) $(CXXFLAGS) -MM $^>>./.depend;

clean:
	$(RM) $(OBJS)

distclean: clean
	$(RM) *~ .depend

include .depend
