import numpy as np

ntimes = 5000
dt = 0.02
nxy = 30

def read_data(variable, ntimes, nsteps = 1):

    fieldlist4, fieldlist8 = [], []
    for i in range(0, ntimes, nsteps):
        input_file = 'real4/' + variable + '_%5.5i'%i + '.dat'
        fieldlist4.append(np.loadtxt(input_file).reshape(nxy, nxy))

        input_file = 'real8/' + variable + '_%5.5i'%i + '.dat'
        fieldlist8.append(np.loadtxt(input_file).reshape(nxy, nxy))

        if i%100 == 0: print(f"finished reading {i}")

    return fieldlist4, fieldlist8


def read_ddata(variable, ntimes, nsteps = 1):

    fieldlist = []
    for i in range(0, ntimes, nsteps):
        input_file = 'real8/' + variable + '_%5.5i'%i + '.dat'
        fieldlist.append(np.loadtxt(input_file).reshape(nxy, nxy))

        if i%100 == 0: print(f"finished reading {i}")

    return fieldlist

