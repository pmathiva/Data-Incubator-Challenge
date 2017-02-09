import numpy
import itertools

die = [1,2,3,4,5,6]
N = 8
M = 24
res = []

for r in itertools.product(die, repeat=N):
    if sum(r) == M:
        res.append(numpy.prod(r))

expval = numpy.mean(res)
stdev = numpy.std(res)

print expval
print stdev
