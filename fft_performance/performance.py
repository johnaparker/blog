import numpy as np
from timeit import default_timer as timer
from functools import partial
import matplotlib.pyplot as plt
from tqdm import tqdm
from fft import gpu_fft
import pyfftw
import matplotlib as mpl
mpl.rc('font', size=20)

def time_function(func, runtime=.1):
    """Time a function by running it repeatedly for at least 'runtime' seconds"""
    start = timer()
    t = 0
    count = 0

    while t < runtime:
        t0 = timer()
        func()
        tf = timer()
        t += tf - t0

        count += 1

    return t/count

nvals = 2**np.arange(5,12)

cuda_time = []
numpy_time = []
pyfftw_time = []

for n in tqdm(nvals):
    data = np.random.random(size=(n,n)).astype(np.float32)
    a = pyfftw.empty_aligned((n,n), dtype='float32')

    b = pyfftw.empty_aligned((a.shape[0], a.shape[1]//2 + 1),  dtype='complex64')
    a[...] = data

    fft_object = pyfftw.FFTW(a, b, threads=16)
    pyfftw_time.append(time_function(fft_object)*1e3)

    numpy_fft = partial(np.fft.rfft2, a=data)
    numpy_time.append(time_function(numpy_fft)*1e3)

    iterations = 10000
    cuda_fft = partial(gpu_fft, n, n, iterations)
    cuda_time.append(time_function(cuda_fft)*1e3/iterations)

numpy_time = np.array(numpy_time)
cuda_time = np.array(cuda_time)
pyfftw_time = np.array(pyfftw_time)

fig, axes = plt.subplots(figsize=(6,6))

axes.loglog(nvals, numpy_time, 'o-', label='NumPy', basex=2, lw=4, ms=10)
axes.loglog(nvals, cuda_time, 'o-',  label='CUDA', basex=2, lw=4, ms=10)
axes.loglog(nvals, pyfftw_time, 'o-',  label='PyFFTW', basex=2, lw=4, ms=10)
axes.grid(ls='--', color='gray')
axes.set_xlabel('image size', labelpad=20)
axes.set_ylabel('runtime', labelpad=20)
axes.tick_params(left=False, bottom=False, labelbottom=False, labelleft=False)

plt.tight_layout()
plt.savefig('out.svg')

plt.show()
