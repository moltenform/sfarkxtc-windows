
# to build,
# run "make"
# to build with duma,
# run "make USE_DUMA=1"

# to build with duma and stack protection,
# run "make USE_DUMA=1 STACK_PROTECT=1"

CC=gcc
CXX=g++
RM=rm -f
ENDIANNESS=LITTLE_ENDIAN
CXXFLAGS+=-fPIC -D__$(ENDIANNESS)__ -Wall -Wextra

# add security flags
CXXFLAGS+= -Wformat-security -mmitigate-rop

# add more security flags, at the cost of some performance (only 7.1% slower in my tests)
CXXFLAGS+= -pie -fPIE -D_FORTIFY_SOURCE=2
CXXFLAGS+= -Wl,-z,relro,-z,now -Wl,-z,noexecstack
CXXFLAGS+= -Wl,dynamicbase -Wl,nxcompat
ifeq ($(PROTECT_STACK),1)
        CXXFLAGS+= -fstack-clash-protection -fstack-protector-strong
endif

SRCS=sfklCoding.cpp sfklCrunch.cpp sfklDiff.cpp sfklFile.cpp sfklLPC.cpp sfklString.cpp sfklZip.cpp sfarkxtc.cpp
OBJS=$(subst .cpp,.o,$(SRCS))

# add a reference to zlib, and optionally duma
ifeq ($(USE_DUMA),1)
        LDLIBS=-lz ./duma/libduma.a
else
        LDLIBS=-lz
endif

ifeq ($(PROTECT_STACK),1)
        LDLIBS+= -lssp
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
