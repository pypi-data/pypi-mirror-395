import numpy as np
cimport numpy as cnp
import cython
cnp.import_array()


@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cpdef make_histogram(
        double[:] times,
        cnp.int32_t[:] spec,
        int N_spec,
        int[:] periods,
        int[:] weight,
        double min_time=0,
        double max_time=30.,
        double width=0.5,
        double conversion=1.e-3):
    """
    This method creates histograms from a list of data.
    It produces a matrix of histograms for multiple periods
    and spectra.
    Strictly speaking these are not histograms as they
    are not normalised to bin width.
    This is the language used by the users and the
    analysis code applys the normalisation.
    :param times: the times for the data
    :param spec: the spectra for the corresponding time
    :param N_spec: the number of spectra
    :param periods: a list of the periods each event belongs to
    :param weight: the weight to give each event in the histogram ( 0 or 1)
    :param min_time: the first bin edge
    :param max_time: the last bin edge
    :param width: the bin width
    :param conversion: for unit conversions
    :returns: a matrix of histograms, the bin edges, the
    number of events in the histogram
    """

    cdef Py_ssize_t det, k, j_bin, p
    cdef int N = 0
    cdef int w_k
    cdef double time

    cdef cnp.ndarray[double, ndim=1] bins = np.arange(min_time, max_time + width, width, dtype=np.double)

    cdef cnp.ndarray[int, ndim=3] result = np.zeros((np.max(periods)+1, N_spec, len(bins)-1), dtype=np.int32)
    cdef int[:, :, :] mat = result
    for k in range(len(times)):
        det = spec[k]
        time = times[k] * conversion
        if time <= max_time and time >= min_time:
            p = periods[k]
            j_bin = int((time - min_time) // width)
            w_k = 1*weight[k]
            mat[p, det, j_bin] += w_k
            N += w_k
    return result, bins, N
