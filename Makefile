FC = gfortran
CPPFLAGS=-cpp -DPRECISION_=$(PRECISION)
FCFLAGS = -O0 -g -fcoarray="single"

OBJS = mod_diff.o mod_field.o mod_io.o mod_parallel.o

.PHONY: all clean
.SUFFIXES: .f90 .o

all: tsunami

tsunami: tsunami.f90 $(OBJS)
	$(FC) $(CPPFLAGS) $(FCFLAGS) $< $(OBJS) -o $@

.f90.o:
	$(FC) -c $(CPPFLAGS) $(FCFLAGS) $<

%.o: %.mod

mod_field.o: mod_field.f90 mod_diff.o mod_io.o mod_parallel.o

clean:
	$(RM) tsunami *.o *.mod

clean_files: $(RM) real4/*.dat real8/*.dat
