# wave_functions.py
# Copyright (c) 2013-2017 Pablo Acosta-Serafini
# See LICENSE for details
# pylint: disable=C0103,C0111,E1101,R0913,W0212

# Standard library imports
import copy
import math
# PyPI imports
import numpy
import pexdoc.exh
import pexdoc.pcontracts
# Intra-package imports imports
from .functions import remove_extra_delims
from .constants import FP_ATOL, FP_RTOL
from .wave_core import _interp_dep_vector, Waveform


###
# Exception tracing initialization code
###
"""
[[[cog
import os, sys
if sys.hexversion < 0x03000000:
    import __builtin__
else:
    import builtins as __builtin__
sys.path.append(os.environ['TRACER_DIR'])
import trace_ex_eng_wave_functions
exobj_eng = trace_ex_eng_wave_functions.trace_module(no_print=True)
]]]
[[[end]]]
"""



###
# Functions
###
def _barange(bmin, bmax, inc):
    vector = numpy.arange(bmin, bmax+inc, inc)
    vector = (
        vector
        if numpy.isclose(bmax, vector[-1], FP_RTOL, FP_ATOL) else
        vector[:-1]
    )
    return vector


def _bound_waveform(wave, indep_min, indep_max):
    """ Add independent variable vector bounds if they are not in vector """
    indep_min, indep_max = _validate_min_max(wave, indep_min, indep_max)
    indep_vector = copy.copy(wave._indep_vector)
    if ((isinstance(indep_min, float) or isinstance(indep_max, float)) and
        indep_vector.dtype.name.startswith('int')):
        indep_vector = indep_vector.astype(float)
    min_pos = numpy.searchsorted(indep_vector, indep_min)
    if not numpy.isclose(indep_min, indep_vector[min_pos], FP_RTOL, FP_ATOL):
        indep_vector = numpy.insert(indep_vector, min_pos, indep_min)
    max_pos = numpy.searchsorted(indep_vector, indep_max)
    if not numpy.isclose(indep_max, indep_vector[max_pos], FP_RTOL, FP_ATOL):
        indep_vector = numpy.insert(indep_vector, max_pos, indep_max)
    dep_vector = _interp_dep_vector(wave, indep_vector)
    wave._indep_vector = indep_vector[min_pos:max_pos+1]
    wave._dep_vector = dep_vector[min_pos:max_pos+1]


def _build_units(indep_units, dep_units, op):
    """ Build unit math operations """
    if (not dep_units) and (not indep_units):
        return ''
    if dep_units and (not indep_units):
        return dep_units
    if (not dep_units) and indep_units:
        return (
            remove_extra_delims('1{0}({1})'.format(op, indep_units))
            if op == '/' else
            remove_extra_delims('({0})'.format(indep_units))
        )
    return remove_extra_delims(
        '({0}){1}({2})'.format(dep_units, op, indep_units)
    )


def _operation(wave, desc, units, fpointer):
    """ Generic operation on a waveform object """
    ret = copy.copy(wave)
    ret.dep_units = units
    ret.dep_name = '{0}({1})'.format(desc, ret.dep_name)
    ret._dep_vector = fpointer(ret._dep_vector)
    return ret


def _running_area(indep_vector, dep_vector):
    """ Calculate running area under curve """
    rect_height = numpy.minimum(dep_vector[:-1], dep_vector[1:])
    rect_base = numpy.diff(indep_vector)
    rect_area = numpy.multiply(rect_height, rect_base)
    triang_height = numpy.abs(numpy.diff(dep_vector))
    triang_area = 0.5*numpy.multiply(triang_height, rect_base)
    return numpy.cumsum(
        numpy.concatenate((numpy.array([0.0]), triang_area+rect_area))
    )


def _validate_min_max(wave, indep_min, indep_max):
    """
    Validate that minimum and maximum bounds are within the waveform's
    independent variable vector
    """
    imin, imax = False, False
    if indep_min is None:
        indep_min = wave._indep_vector[0]
        imin = True
    if indep_max is None:
        indep_max = wave._indep_vector[-1]
        imax = True
    if imin and imax:
        return indep_min, indep_max
    exminmax = pexdoc.exh.addex(
        RuntimeError, 'Incongruent `indep_min` and `indep_max` arguments'
    )
    exmin = pexdoc.exh.addai('indep_min')
    exmax = pexdoc.exh.addai('indep_max')
    exminmax(bool(indep_min >= indep_max))
    exmin(
        bool(
            (indep_min < wave._indep_vector[0]) and
            (
                not numpy.isclose(
                    indep_min, wave._indep_vector[0], FP_RTOL, FP_ATOL
                )
            )
        )
    )
    exmax(
        bool(
            (indep_max > wave._indep_vector[-1]) and
            (
                not numpy.isclose(
                    indep_max, wave._indep_vector[-1], FP_RTOL, FP_ATOL
                )
            )
        )
    )
    return indep_min, indep_max


@pexdoc.pcontracts.contract(wave=Waveform)
def acos(wave):
    r"""
    Returns the arc cosine of a waveform's dependent variable vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.acos

    :raises:
     * RuntimeError (Argument \`wave\` is not valid)

     * ValueError (Math domain error)

    .. [[[end]]]
    """
    pexdoc.exh.addex(
        ValueError, 'Math domain error', bool(
            (min(wave._dep_vector) < -1) or (max(wave._dep_vector) > 1)
        )
    )
    return _operation(wave, 'acos', 'rad', numpy.arccos)


@pexdoc.pcontracts.contract(wave=Waveform)
def acosh(wave):
    r"""
    Returns the hyperbolic arc cosine of a waveform's dependent variable vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.acosh

    :raises:
     * RuntimeError (Argument \`wave\` is not valid)

     * ValueError (Math domain error)

    .. [[[end]]]
    """
    pexdoc.exh.addex(
        ValueError, 'Math domain error', bool(min(wave._dep_vector) < 1)
    )
    return _operation(wave, 'acosh', '', numpy.arccosh)


@pexdoc.pcontracts.contract(wave=Waveform)
def asin(wave):
    r"""
    Returns the arc sine of a waveform's dependent variable vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.asin

    :raises:
     * RuntimeError (Argument \`wave\` is not valid)

     * ValueError (Math domain error)

    .. [[[end]]]
    """
    pexdoc.exh.addex(
        ValueError, 'Math domain error', bool(
            (min(wave._dep_vector) < -1) or (max(wave._dep_vector) > 1)
        )
    )
    return _operation(wave, 'asin', 'rad', numpy.arcsin)


@pexdoc.pcontracts.contract(wave=Waveform)
def asinh(wave):
    r"""
    Returns the hyperbolic arc sine of a waveform's dependent variable vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.asinh

    :raises: RuntimeError (Argument \`wave\` is not valid)

    .. [[[end]]]
    """
    return _operation(wave, 'asinh', '', numpy.arcsinh)


@pexdoc.pcontracts.contract(wave=Waveform)
def atan(wave):
    r"""
    Returns the arc tangent of a waveform's dependent variable vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.atan

    :raises: RuntimeError (Argument \`wave\` is not valid)

    .. [[[end]]]
    """
    return _operation(wave, 'atan', 'rad', numpy.arctan)


@pexdoc.pcontracts.contract(wave=Waveform)
def atanh(wave):
    r"""
    Returns the hyperbolic arc tangent of a waveform's dependent variable
    vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.atanh

    :raises:
     * RuntimeError (Argument \`wave\` is not valid)

     * ValueError (Math domain error)

    .. [[[end]]]
    """
    pexdoc.exh.addex(
        ValueError, 'Math domain error', bool(
            (min(wave._dep_vector) < -1) or (max(wave._dep_vector) > 1)
        )
    )
    return _operation(wave, 'atanh', '', numpy.arctanh)


@pexdoc.pcontracts.contract(
    wave=Waveform, indep_min='None|number', indep_max='None|number'
)
def average(wave, indep_min=None, indep_max=None):
    r"""
    Returns the running average of a waveform's dependent variable vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param indep_min: Independent vector start point of computation
    :type  indep_min: integer or float

    :param indep_max: Independent vector stop point of computation
    :type  indep_max: integer or float

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc(raised=True)) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.average

    :raises:
     * RuntimeError (Argument \`indep_max\` is not valid)

     * RuntimeError (Argument \`indep_min\` is not valid)

     * RuntimeError (Argument \`wave\` is not valid)

     * RuntimeError (Incongruent \`indep_min\` and \`indep_max\`
       arguments)

    .. [[[end]]]
    """
    ret = copy.copy(wave)
    _bound_waveform(ret, indep_min, indep_max)
    area = _running_area(ret._indep_vector, ret._dep_vector)
    area[0] = ret._dep_vector[0]
    deltas = ret._indep_vector-ret._indep_vector[0]
    deltas[0] = 1.0
    ret._dep_vector = numpy.divide(area, deltas)
    ret.dep_name = 'average({0})'.format(ret._dep_name)
    return ret


@pexdoc.pcontracts.contract(wave=Waveform)
def ceil(wave):
    r"""
    Returns the ceiling of a waveform's dependent variable vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.ceil

    :raises: RuntimeError (Argument \`wave\` is not valid)

    .. [[[end]]]
    """
    return _operation(wave, 'ceil', wave.dep_units, numpy.ceil)


@pexdoc.pcontracts.contract(wave=Waveform)
def cos(wave):
    r"""
    Returns the cosine of a waveform's dependent variable vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for peng.wave_functions.cos

    :raises: RuntimeError (Argument \`wave\` is not valid)

    .. [[[end]]]
    """
    return _operation(wave, 'cos', '', numpy.cos)


@pexdoc.pcontracts.contract(wave=Waveform)
def cosh(wave):
    r"""
    Returns the hyperbolic cosine of a waveform's dependent variable vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.cosh

    :raises: RuntimeError (Argument \`wave\` is not valid)

    .. [[[end]]]
    """
    return _operation(wave, 'cosh', '', numpy.cosh)


@pexdoc.pcontracts.contract(wave=Waveform)
def db(wave):
    r"""
    Returns a waveform's dependent variable vector expressed in decibels

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for peng.wave_functions.db

    :raises:
     * RuntimeError (Argument \`wave\` is not valid)

     * ValueError (Math domain error)

    .. [[[end]]]
    """
    pexdoc.exh.addex(
        ValueError,
        'Math domain error',
        bool((numpy.min(numpy.abs(wave._dep_vector)) <= 0))
    )
    ret = copy.copy(wave)
    ret.dep_units = 'dB'
    ret.dep_name = 'db({0})'.format(ret.dep_name)
    ret._dep_vector = 20.0*numpy.log10(numpy.abs(ret._dep_vector))
    return ret


@pexdoc.pcontracts.contract(
    wave=Waveform, indep_min='None|number', indep_max='None|number'
)
def derivative(wave, indep_min=None, indep_max=None):
    r"""
    Returns the numerical derivative of a waveform's dependent variable vector
    using
    `backwards differences <https://en.wikipedia.org/wiki/
    Finite_difference#Forward.2C_backward.2C_and_central_differences>`_

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param indep_min: Independent vector start point of computation
    :type  indep_min: integer or float

    :param indep_max: Independent vector stop point of computation
    :type  indep_max: integer or float

    :rtype: float

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc(raised=True)) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.derivative

    :raises:
     * RuntimeError (Argument \`indep_max\` is not valid)

     * RuntimeError (Argument \`indep_min\` is not valid)

     * RuntimeError (Argument \`wave\` is not valid)

     * RuntimeError (Incongruent \`indep_min\` and \`indep_max\`
       arguments)

    .. [[[end]]]
    """
    ret = copy.copy(wave)
    _bound_waveform(ret, indep_min, indep_max)
    delta_indep = numpy.diff(ret._indep_vector)
    delta_dep = numpy.diff(ret._dep_vector)
    delta_indep = numpy.concatenate(
        (numpy.array([delta_indep[0]]), delta_indep)
    )
    delta_dep = numpy.concatenate(
        (numpy.array([delta_dep[0]]), delta_dep)
    )
    ret._dep_vector = numpy.divide(delta_dep, delta_indep)
    ret.dep_name = 'derivative({0})'.format(ret._dep_name)
    ret.dep_units = _build_units(ret.indep_units, ret.dep_units, '/')
    return ret


@pexdoc.pcontracts.contract(wave=Waveform)
def exp(wave):
    r"""
    Returns the natural exponent of a waveform's dependent variable vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for peng.wave_functions.exp

    :raises: RuntimeError (Argument \`wave\` is not valid)

    .. [[[end]]]
    """
    return _operation(wave, 'exp', '', numpy.exp)


@pexdoc.pcontracts.contract(
    wave=Waveform, npoints='None|(int,>=1)',
    indep_min='None|number', indep_max='None|number'
)
def fft(wave, npoints=None, indep_min=None, indep_max=None):
    r"""
    Returns the Fast Fourier Transform of a waveform

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param npoints: Number of points to use in the transform. If **npoints**
                    is less than the size of the independent variable vector
                    the waveform is truncated; if **npoints** is greater than
                    the size of the independent variable vector, the waveform
                    is zero-padded
    :type  npoints: positive integer

    :param indep_min: Independent vector start point of computation
    :type  indep_min: integer or float

    :param indep_max: Independent vector stop point of computation
    :type  indep_max: integer or float

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc(raised=True)) ]]]
    .. Auto-generated exceptions documentation for peng.wave_functions.fft

    :raises:
     * RuntimeError (Argument \`indep_max\` is not valid)

     * RuntimeError (Argument \`indep_min\` is not valid)

     * RuntimeError (Argument \`npoints\` is not valid)

     * RuntimeError (Argument \`wave\` is not valid)

     * RuntimeError (Incongruent \`indep_min\` and \`indep_max\`
       arguments)

     * RuntimeError (Non-uniform sampling)

    .. [[[end]]]
    """
    ret = copy.copy(wave)
    _bound_waveform(ret, indep_min, indep_max)
    npoints = npoints or ret._indep_vector.size
    fs = (npoints-1)/float(ret._indep_vector[-1])
    spoints = min(ret._indep_vector.size, npoints)
    sdiff = numpy.diff(ret._indep_vector[:spoints])
    cond = not numpy.all(
        numpy.isclose(
            sdiff, sdiff[0]*numpy.ones(spoints-1), FP_RTOL, FP_ATOL
        )
    )
    pexdoc.addex(RuntimeError, 'Non-uniform sampling', cond)
    finc = fs/float(npoints-1)
    indep_vector = _barange(-fs/2.0, +fs/2.0, finc)
    dep_vector = numpy.fft.fft(ret._dep_vector, npoints)
    return Waveform(
        indep_vector=indep_vector,
        dep_vector=dep_vector,
        dep_name='fft({0})'.format(ret.dep_name),
        indep_scale='LINEAR',
        dep_scale='LINEAR',
        indep_units='Hz',
        dep_units=''
    )


@pexdoc.pcontracts.contract(
    wave=Waveform, npoints='None|(int,>=1)',
    indep_min='None|number', indep_max='None|number'
)
def fftdb(wave, npoints=None, indep_min=None, indep_max=None):
    r"""
    Returns the Fast Fourier Transform of a waveform with the dependent
    variable vector expressed in decibels

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param npoints: Number of points to use in the transform. If **npoints**
                    is less than the size of the independent variable vector
                    the waveform is truncated; if **npoints** is greater than
                    the size of the independent variable vector, the waveform
                    is zero-padded
    :type  npoints: positive integer

    :param indep_min: Independent vector start point of computation
    :type  indep_min: integer or float

    :param indep_max: Independent vector stop point of computation
    :type  indep_max: integer or float

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc(raised=True)) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.fftdb

    :raises:
     * RuntimeError (Argument \`indep_max\` is not valid)

     * RuntimeError (Argument \`indep_min\` is not valid)

     * RuntimeError (Argument \`npoints\` is not valid)

     * RuntimeError (Argument \`wave\` is not valid)

     * RuntimeError (Incongruent \`indep_min\` and \`indep_max\`
       arguments)

     * RuntimeError (Non-uniform sampling)

    .. [[[end]]]
    """
    return db(fft(wave, npoints, indep_min, indep_max))


@pexdoc.pcontracts.contract(
    wave=Waveform, npoints='None|(int,>=1)',
    indep_min='None|number', indep_max='None|number'
)
def ffti(wave, npoints=None, indep_min=None, indep_max=None):
    r"""
    Returns the imaginary part of the Fast Fourier Transform of a waveform

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param npoints: Number of points to use in the transform. If **npoints**
                    is less than the size of the independent variable vector
                    the waveform is truncated; if **npoints** is greater than
                    the size of the independent variable vector, the waveform
                    is zero-padded
    :type  npoints: positive integer

    :param indep_min: Independent vector start point of computation
    :type  indep_min: integer or float

    :param indep_max: Independent vector stop point of computation
    :type  indep_max: integer or float

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc(raised=True)) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.ffti

    :raises:
     * RuntimeError (Argument \`indep_max\` is not valid)

     * RuntimeError (Argument \`indep_min\` is not valid)

     * RuntimeError (Argument \`npoints\` is not valid)

     * RuntimeError (Argument \`wave\` is not valid)

     * RuntimeError (Incongruent \`indep_min\` and \`indep_max\`
       arguments)

     * RuntimeError (Non-uniform sampling)

    .. [[[end]]]
    """
    return imag(fft(wave, npoints, indep_min, indep_max))


@pexdoc.pcontracts.contract(
    wave=Waveform, npoints='None|(int,>=1)',
    indep_min='None|number', indep_max='None|number'
)
def fftm(wave, npoints=None, indep_min=None, indep_max=None):
    r"""
    Returns the magnitude of the Fast Fourier Transform of a waveform

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param npoints: Number of points to use in the transform. If **npoints**
                    is less than the size of the independent variable vector
                    the waveform is truncated; if **npoints** is greater than
                    the size of the independent variable vector, the waveform
                    is zero-padded
    :type  npoints: positive integer

    :param indep_min: Independent vector start point of computation
    :type  indep_min: integer or float

    :param indep_max: Independent vector stop point of computation
    :type  indep_max: integer or float

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc(raised=True)) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.fftm

    :raises:
     * RuntimeError (Argument \`indep_max\` is not valid)

     * RuntimeError (Argument \`indep_min\` is not valid)

     * RuntimeError (Argument \`npoints\` is not valid)

     * RuntimeError (Argument \`wave\` is not valid)

     * RuntimeError (Incongruent \`indep_min\` and \`indep_max\`
       arguments)

     * RuntimeError (Non-uniform sampling)

    .. [[[end]]]
    """
    return abs(fft(wave, npoints, indep_min, indep_max))


@pexdoc.pcontracts.contract(
    wave=Waveform, npoints='None|(int,>=1)',
    indep_min='None|number', indep_max='None|number',
    unwrap=bool, rad=bool
)
def fftp(
        wave, npoints=None, indep_min=None, indep_max=None,
        unwrap=True, rad=True
):
    r"""
    Returns the phase of the Fast Fourier Transform of a waveform

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param npoints: Number of points to use in the transform. If **npoints**
                    is less than the size of the independent variable vector
                    the waveform is truncated; if **npoints** is greater than
                    the size of the independent variable vector, the waveform
                    is zero-padded
    :type  npoints: positive integer

    :param indep_min: Independent vector start point of computation
    :type  indep_min: integer or float

    :param indep_max: Independent vector stop point of computation
    :type  indep_max: integer or float

    :param unwrap: Flag that indicates whether phase should change phase shifts
                   to their :code:`2*pi` complement (True) or not (False)
    :type  unwrap: boolean

    :param rad: Flag that indicates whether phase should be returned in radians
                (True) or degrees (False)
    :type  rad: boolean

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc(raised=True)) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.fftp

    :raises:
     * RuntimeError (Argument \`indep_max\` is not valid)

     * RuntimeError (Argument \`indep_min\` is not valid)

     * RuntimeError (Argument \`npoints\` is not valid)

     * RuntimeError (Argument \`rad\` is not valid)

     * RuntimeError (Argument \`unwrap\` is not valid)

     * RuntimeError (Argument \`wave\` is not valid)

     * RuntimeError (Incongruent \`indep_min\` and \`indep_max\`
       arguments)

     * RuntimeError (Non-uniform sampling)

    .. [[[end]]]
    """
    return phase(
        fft(wave, npoints, indep_min, indep_max), unwrap=unwrap, rad=rad
    )


@pexdoc.pcontracts.contract(
    wave=Waveform, npoints='None|(int,>=1)',
    indep_min='None|number', indep_max='None|number'
)
def fftr(wave, npoints=None, indep_min=None, indep_max=None):
    r"""
    Returns the real part of the Fast Fourier Transform of a waveform

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param npoints: Number of points to use in the transform. If **npoints**
                    is less than the size of the independent variable vector
                    the waveform is truncated; if **npoints** is greater than
                    the size of the independent variable vector, the waveform
                    is zero-padded
    :type  npoints: positive integer

    :param indep_min: Independent vector start point of computation
    :type  indep_min: integer or float

    :param indep_max: Independent vector stop point of computation
    :type  indep_max: integer or float

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc(raised=True)) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.fftr

    :raises:
     * RuntimeError (Argument \`indep_max\` is not valid)

     * RuntimeError (Argument \`indep_min\` is not valid)

     * RuntimeError (Argument \`npoints\` is not valid)

     * RuntimeError (Argument \`wave\` is not valid)

     * RuntimeError (Incongruent \`indep_min\` and \`indep_max\`
       arguments)

     * RuntimeError (Non-uniform sampling)

    .. [[[end]]]
    """
    return real(fft(wave, npoints, indep_min, indep_max))


@pexdoc.pcontracts.contract(
    wave=Waveform, dep_var='number', der='None|(int,>=-1,<=+1)', inst='int,>0',
    indep_min='None|number', indep_max='None|number'
)
def find(wave, dep_var, der=None, inst=1, indep_min=None, indep_max=None):
    r"""
    Returns the independent variable vector point that corresponds to a given
    dependent variable vector point. If the dependent variable point is not in
    the dependent variable vector the independent variable vector point is
    obtained by linear interpolation

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param dep_var: Dependent vector value to search for
    :type  dep_var: integer, float or complex

    :param der: Dependent vector derivative filter. If +1 only independent
                vector points that have positive derivatives when crossing
                the requested dependent vector point are returned; if -1 only
                independent vector points that have negative derivatives when
                crossing the requested dependent vector point are returned;
                if 0 only independent vector points that have null derivatives
                when crossing the requested dependent vector point are
                returned; otherwise if None all independent vector points are
                returned regardless of the dependent vector derivative. The
                derivative of the first and last point of the waveform is
                assumed to be null
    :type  der: integer, float or complex

    :param inst: Instance number filter. If, for example, **inst** equals 3,
                 then the independent variable vector point at which the
                 dependent variable vector equals the requested value for the
                 third time is returned
    :type  inst: positive integer

    :param indep_min: Independent vector start point of computation
    :type  indep_min: integer or float

    :param indep_max: Independent vector stop point of computation
    :type  indep_max: integer or float

    :rtype: integer, float or None if the dependent variable point is not found

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc(raised=True)) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.find

    :raises:
     * RuntimeError (Argument \`dep_var\` is not valid)

     * RuntimeError (Argument \`der\` is not valid)

     * RuntimeError (Argument \`indep_max\` is not valid)

     * RuntimeError (Argument \`indep_min\` is not valid)

     * RuntimeError (Argument \`inst\` is not valid)

     * RuntimeError (Argument \`wave\` is not valid)

     * RuntimeError (Incongruent \`indep_min\` and \`indep_max\`
       arguments)

    .. [[[end]]]
    """
    # pylint: disable=C0325,R0914,W0613
    ret = copy.copy(wave)
    _bound_waveform(ret, indep_min, indep_max)
    close_min = numpy.isclose(min(ret._dep_vector), dep_var, FP_RTOL, FP_ATOL)
    close_max = numpy.isclose(max(ret._dep_vector), dep_var, FP_RTOL, FP_ATOL)
    if (((numpy.amin(ret._dep_vector) > dep_var) and (not close_min)) or
       ((numpy.amax(ret._dep_vector) < dep_var) and (not close_max))):
        return None
    cross_wave = ret._dep_vector-dep_var
    sign_wave = numpy.sign(cross_wave)
    exact_idx = numpy.where(
        numpy.isclose(ret._dep_vector, dep_var, FP_RTOL, FP_ATOL)
    )[0]
    # Locations where dep_vector crosses dep_var or it is equal to it
    left_idx = numpy.where(numpy.diff(sign_wave))[0]
    # Remove elements to the left of exact matches
    left_idx = numpy.setdiff1d(left_idx, exact_idx)
    left_idx = numpy.setdiff1d(left_idx, exact_idx-1)
    right_idx = left_idx+1 if left_idx.size else numpy.array([])
    indep_var = (
        ret._indep_vector[exact_idx] if exact_idx.size else numpy.array([])
    )
    dvector = (
        numpy.zeros(exact_idx.size).astype(int)
        if exact_idx.size else
        numpy.array([])
    )
    if left_idx.size and (ret.interp == 'STAIRCASE'):
        idvector = 2.0*(
            ret._dep_vector[right_idx] > ret._dep_vector[left_idx]
        ).astype(int)-1
        if indep_var.size:
            indep_var = numpy.concatenate(
                (indep_var, ret._indep_vector[right_idx])
            )
            dvector = numpy.concatenate((dvector, idvector))
            sidx = numpy.argsort(indep_var)
            indep_var = indep_var[sidx]
            dvector = dvector[sidx]
        else:
            indep_var = ret._indep_vector[right_idx]
            dvector = idvector
    elif left_idx.size:
        y_left = ret._dep_vector[left_idx]
        y_right = ret._dep_vector[right_idx]
        x_left = ret._indep_vector[left_idx]
        x_right = ret._indep_vector[right_idx]
        slope = ((y_left-y_right)/(x_left-x_right)).astype(float)
        # y = y0+slope*(x-x0) => x0+(y-y0)/slope
        if indep_var.size:
            indep_var = numpy.concatenate(
                (indep_var, x_left+((dep_var-y_left)/slope))
            )
            dvector = numpy.concatenate(
                (dvector, numpy.where(slope > 0, 1, -1))
            )
            sidx = numpy.argsort(indep_var)
            indep_var = indep_var[sidx]
            dvector = dvector[sidx]
        else:
            indep_var = x_left+((dep_var-y_left)/slope)
            dvector = numpy.where(slope > 0, +1, -1)
    if der is not None:
        indep_var = numpy.extract(dvector == der, indep_var)
    return indep_var[inst-1] if inst <= indep_var.size else None


@pexdoc.pcontracts.contract(wave=Waveform)
def floor(wave):
    r"""
    Returns the floor of a waveform's dependent variable vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.floor

    :raises: RuntimeError (Argument \`wave\` is not valid)

    .. [[[end]]]
    """
    return _operation(wave, 'floor', wave.dep_units, numpy.floor)


@pexdoc.pcontracts.contract(
    wave=Waveform, npoints='None|(int,>=1)',
    indep_min='None|number', indep_max='None|number'
)
def ifft(wave, npoints=None, indep_min=None, indep_max=None):
    r"""
    Returns the inverse Fast Fourier Transform of a waveform

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param npoints: Number of points to use in the transform. If **npoints**
                    is less than the size of the independent variable vector
                    the waveform is truncated; if **npoints** is greater than
                    the size of the independent variable vector, the waveform
                    is zero-padded
    :type  npoints: positive integer

    :param indep_min: Independent vector start point of computation
    :type  indep_min: integer or float

    :param indep_max: Independent vector stop point of computation
    :type  indep_max: integer or float

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc(raised=True)) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.ifft

    :raises:
     * RuntimeError (Argument \`indep_max\` is not valid)

     * RuntimeError (Argument \`indep_min\` is not valid)

     * RuntimeError (Argument \`npoints\` is not valid)

     * RuntimeError (Argument \`wave\` is not valid)

     * RuntimeError (Incongruent \`indep_min\` and \`indep_max\`
       arguments)

     * RuntimeError (Non-uniform frequency spacing)

    .. [[[end]]]
    """
    ret = copy.copy(wave)
    _bound_waveform(ret, indep_min, indep_max)
    npoints = npoints or ret._indep_vector.size
    spoints = min(ret._indep_vector.size, npoints)
    sdiff = numpy.diff(ret._indep_vector[:spoints])
    finc = sdiff[0]
    cond = not numpy.all(
        numpy.isclose(
            sdiff, finc*numpy.ones(spoints-1), FP_RTOL, FP_ATOL
        )
    )
    pexdoc.addex(RuntimeError, 'Non-uniform frequency spacing', cond)
    fs = (npoints-1)*finc
    tinc = 1/float(fs)
    tend = 1/float(finc)
    indep_vector = _barange(0, tend, tinc)
    dep_vector = numpy.fft.ifft(ret._dep_vector, npoints)
    return Waveform(
        indep_vector=indep_vector,
        dep_vector=dep_vector,
        dep_name='ifft({0})'.format(ret.dep_name),
        indep_scale='LINEAR',
        dep_scale='LINEAR',
        indep_units='sec',
        dep_units=''
    )


@pexdoc.pcontracts.contract(
    wave=Waveform, npoints='None|(int,>=1)',
    indep_min='None|number', indep_max='None|number'
)
def ifftdb(wave, npoints=None, indep_min=None, indep_max=None):
    r"""
    Returns the inverse Fast Fourier Transform of a waveform with the dependent
    variable vector expressed in decibels

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param npoints: Number of points to use in the transform. If **npoints**
                    is less than the size of the independent variable vector
                    the waveform is truncated; if **npoints** is greater than
                    the size of the independent variable vector, the waveform
                    is zero-padded
    :type  npoints: positive integer

    :param indep_min: Independent vector start point of computation
    :type  indep_min: integer or float

    :param indep_max: Independent vector stop point of computation
    :type  indep_max: integer or float

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc(raised=True)) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.ifftdb

    :raises:
     * RuntimeError (Argument \`indep_max\` is not valid)

     * RuntimeError (Argument \`indep_min\` is not valid)

     * RuntimeError (Argument \`npoints\` is not valid)

     * RuntimeError (Argument \`wave\` is not valid)

     * RuntimeError (Incongruent \`indep_min\` and \`indep_max\`
       arguments)

     * RuntimeError (Non-uniform frequency spacing)

    .. [[[end]]]
    """
    return db(ifft(wave, npoints, indep_min, indep_max))


@pexdoc.pcontracts.contract(
    wave=Waveform, npoints='None|(int,>=1)',
    indep_min='None|number', indep_max='None|number'
)
def iffti(wave, npoints=None, indep_min=None, indep_max=None):
    r"""
    Returns the imaginary part of the inverse Fast Fourier Transform of a
    waveform

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param npoints: Number of points to use in the transform. If **npoints**
                    is less than the size of the independent variable vector
                    the waveform is truncated; if **npoints** is greater than
                    the size of the independent variable vector, the waveform
                    is zero-padded
    :type  npoints: positive integer

    :param indep_min: Independent vector start point of computation
    :type  indep_min: integer or float

    :param indep_max: Independent vector stop point of computation
    :type  indep_max: integer or float

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc(raised=True)) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.iffti

    :raises:
     * RuntimeError (Argument \`indep_max\` is not valid)

     * RuntimeError (Argument \`indep_min\` is not valid)

     * RuntimeError (Argument \`npoints\` is not valid)

     * RuntimeError (Argument \`wave\` is not valid)

     * RuntimeError (Incongruent \`indep_min\` and \`indep_max\`
       arguments)

     * RuntimeError (Non-uniform frequency spacing)

    .. [[[end]]]
    """
    return imag(ifft(wave, npoints, indep_min, indep_max))


@pexdoc.pcontracts.contract(
    wave=Waveform, npoints='None|(int,>=1)',
    indep_min='None|number', indep_max='None|number'
)
def ifftm(wave, npoints=None, indep_min=None, indep_max=None):
    r"""
    Returns the magnitude of the inverse Fast Fourier Transform of a waveform

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param npoints: Number of points to use in the transform. If **npoints**
                    is less than the size of the independent variable vector
                    the waveform is truncated; if **npoints** is greater than
                    the size of the independent variable vector, the waveform
                    is zero-padded
    :type  npoints: positive integer

    :param indep_min: Independent vector start point of computation
    :type  indep_min: integer or float

    :param indep_max: Independent vector stop point of computation
    :type  indep_max: integer or float

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc(raised=True)) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.ifftm

    :raises:
     * RuntimeError (Argument \`indep_max\` is not valid)

     * RuntimeError (Argument \`indep_min\` is not valid)

     * RuntimeError (Argument \`npoints\` is not valid)

     * RuntimeError (Argument \`wave\` is not valid)

     * RuntimeError (Incongruent \`indep_min\` and \`indep_max\`
       arguments)

     * RuntimeError (Non-uniform frequency spacing)

    .. [[[end]]]
    """
    return abs(ifft(wave, npoints, indep_min, indep_max))


@pexdoc.pcontracts.contract(
    wave=Waveform, npoints='None|(int,>=1)',
    indep_min='None|number', indep_max='None|number',
    unwrap=bool, rad=bool
)
def ifftp(
        wave, npoints=None, indep_min=None, indep_max=None,
        unwrap=True, rad=True
):
    r"""
    Returns the phase of the inverse Fast Fourier Transform of a waveform

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param npoints: Number of points to use in the transform. If **npoints**
                    is less than the size of the independent variable vector
                    the waveform is truncated; if **npoints** is greater than
                    the size of the independent variable vector, the waveform
                    is zero-padded
    :type  npoints: positive integer

    :param indep_min: Independent vector start point of computation
    :type  indep_min: integer or float

    :param indep_max: Independent vector stop point of computation
    :type  indep_max: integer or float

    :param unwrap: Flag that indicates whether phase should change phase shifts
                   to their :code:`2*pi` complement (True) or not (False)
    :type  unwrap: boolean

    :param rad: Flag that indicates whether phase should be returned in radians
                (True) or degrees (False)
    :type  rad: boolean

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc(raised=True)) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.ifftp

    :raises:
     * RuntimeError (Argument \`indep_max\` is not valid)

     * RuntimeError (Argument \`indep_min\` is not valid)

     * RuntimeError (Argument \`npoints\` is not valid)

     * RuntimeError (Argument \`rad\` is not valid)

     * RuntimeError (Argument \`unwrap\` is not valid)

     * RuntimeError (Argument \`wave\` is not valid)

     * RuntimeError (Incongruent \`indep_min\` and \`indep_max\`
       arguments)

     * RuntimeError (Non-uniform frequency spacing)

    .. [[[end]]]
    """
    return phase(
        ifft(wave, npoints, indep_min, indep_max), unwrap=unwrap, rad=rad
    )


@pexdoc.pcontracts.contract(
    wave=Waveform, npoints='None|(int,>=1)',
    indep_min='None|number', indep_max='None|number'
)
def ifftr(wave, npoints=None, indep_min=None, indep_max=None):
    r"""
    Returns the real part of the inverse Fast Fourier Transform of a waveform

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param npoints: Number of points to use in the transform. If **npoints**
                    is less than the size of the independent variable vector
                    the waveform is truncated; if **npoints** is greater than
                    the size of the independent variable vector, the waveform
                    is zero-padded
    :type  npoints: positive integer

    :param indep_min: Independent vector start point of computation
    :type  indep_min: integer or float

    :param indep_max: Independent vector stop point of computation
    :type  indep_max: integer or float

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc(raised=True)) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.ifftr

    :raises:
     * RuntimeError (Argument \`indep_max\` is not valid)

     * RuntimeError (Argument \`indep_min\` is not valid)

     * RuntimeError (Argument \`npoints\` is not valid)

     * RuntimeError (Argument \`wave\` is not valid)

     * RuntimeError (Incongruent \`indep_min\` and \`indep_max\`
       arguments)

     * RuntimeError (Non-uniform frequency spacing)

    .. [[[end]]]
    """
    return real(ifft(wave, npoints, indep_min, indep_max))


@pexdoc.pcontracts.contract(wave=Waveform)
def imag(wave):
    r"""
    Returns the imaginary part of a waveform's dependent variable vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.imag

    :raises: RuntimeError (Argument \`wave\` is not valid)

    .. [[[end]]]
    """
    return _operation(wave, 'imag', wave.dep_units, numpy.imag)


@pexdoc.pcontracts.contract(
    wave=Waveform, indep_min='None|number', indep_max='None|number'
)
def integral(wave, indep_min=None, indep_max=None):
    r"""
    Returns the running integral of a waveform's dependent variable vector
    using the
    `trapezoidal method <https://en.wikipedia.org/wiki/Trapezoidal_rule>`_

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param indep_min: Independent vector start point of computation
    :type  indep_min: integer or float

    :param indep_max: Independent vector stop point of computation
    :type  indep_max: integer or float

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc(raised=True)) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.integral

    :raises:
     * RuntimeError (Argument \`indep_max\` is not valid)

     * RuntimeError (Argument \`indep_min\` is not valid)

     * RuntimeError (Argument \`wave\` is not valid)

     * RuntimeError (Incongruent \`indep_min\` and \`indep_max\`
       arguments)

    .. [[[end]]]
    """
    ret = copy.copy(wave)
    _bound_waveform(ret, indep_min, indep_max)
    ret._dep_vector = _running_area(ret._indep_vector, ret._dep_vector)
    ret.dep_name = 'integral({0})'.format(ret._dep_name)
    ret.dep_units = _build_units(ret.indep_units, ret.dep_units, '*')
    return ret


@pexdoc.pcontracts.contract(wave=Waveform)
def group_delay(wave):
    r"""
    Returns the group delay of a waveform

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc(raised=True)) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.group_delay

    :raises: RuntimeError (Argument \`wave\` is not valid)

    .. [[[end]]]
    """
    ret = -derivative(phase(wave, unwrap=True)/(2*math.pi))
    ret.dep_name = 'group_delay({0})'.format(wave.dep_name)
    ret.dep_units = 'sec'
    return ret


@pexdoc.pcontracts.contract(wave=Waveform)
def log(wave):
    r"""
    Returns the natural logarithm of a waveform's dependent variable vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for peng.wave_functions.log

    :raises:
     * RuntimeError (Argument \`wave\` is not valid)

     * ValueError (Math domain error)

    .. [[[end]]]
    """
    pexdoc.exh.addex(
        ValueError, 'Math domain error', bool((min(wave._dep_vector) <= 0))
    )
    return _operation(wave, 'log', '', numpy.log)


@pexdoc.pcontracts.contract(wave=Waveform)
def log10(wave):
    r"""
    Returns the base 10 logarithm of a waveform's dependent variable vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.log10

    :raises:
     * RuntimeError (Argument \`wave\` is not valid)

     * ValueError (Math domain error)

    .. [[[end]]]
    """
    pexdoc.exh.addex(
        ValueError, 'Math domain error', bool((min(wave._dep_vector) <= 0))
    )
    return _operation(wave, 'log10', '', numpy.log10)


@pexdoc.pcontracts.contract(
    wave=Waveform, indep_min='None|number', indep_max='None|number'
)
def naverage(wave, indep_min=None, indep_max=None):
    r"""
    Returns the numerical average of a waveform's dependent variable vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param indep_min: Independent vector start point of computation
    :type  indep_min: integer or float

    :param indep_max: Independent vector stop point of computation
    :type  indep_max: integer or float

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc(raised=True)) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.naverage

    :raises:
     * RuntimeError (Argument \`indep_max\` is not valid)

     * RuntimeError (Argument \`indep_min\` is not valid)

     * RuntimeError (Argument \`wave\` is not valid)

     * RuntimeError (Incongruent \`indep_min\` and \`indep_max\`
       arguments)

    .. [[[end]]]
    """
    ret = copy.copy(wave)
    _bound_waveform(ret, indep_min, indep_max)
    delta_x = ret._indep_vector[-1]-ret._indep_vector[0]
    return numpy.trapz(ret._dep_vector, x=ret._indep_vector)/delta_x


@pexdoc.pcontracts.contract(
    wave=Waveform, indep_min='None|number', indep_max='None|number'
)
def nintegral(wave, indep_min=None, indep_max=None):
    r"""
    Returns the numerical integral of a waveform's dependent variable vector
    using the
    `trapezoidal method <https://en.wikipedia.org/wiki/Trapezoidal_rule>`_

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param indep_min: Independent vector start point of computation
    :type  indep_min: integer or float

    :param indep_max: Independent vector stop point of computation
    :type  indep_max: integer or float

    :rtype: float

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc(raised=True)) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.nintegral

    :raises:
     * RuntimeError (Argument \`indep_max\` is not valid)

     * RuntimeError (Argument \`indep_min\` is not valid)

     * RuntimeError (Argument \`wave\` is not valid)

     * RuntimeError (Incongruent \`indep_min\` and \`indep_max\`
       arguments)

    .. [[[end]]]
    """
    ret = copy.copy(wave)
    _bound_waveform(ret, indep_min, indep_max)
    return numpy.trapz(ret._dep_vector, ret._indep_vector)


@pexdoc.pcontracts.contract(
    wave=Waveform, indep_min='None|number', indep_max='None|number'
)
def nmax(wave, indep_min=None, indep_max=None):
    r"""
    Returns the maximum of a waveform's dependent variable vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param indep_min: Independent vector start point of computation
    :type  indep_min: integer or float

    :param indep_max: Independent vector stop point of computation
    :type  indep_max: integer or float

    :rtype: float

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc(raised=True)) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.nmax

    :raises:
     * RuntimeError (Argument \`indep_max\` is not valid)

     * RuntimeError (Argument \`indep_min\` is not valid)

     * RuntimeError (Argument \`wave\` is not valid)

     * RuntimeError (Incongruent \`indep_min\` and \`indep_max\`
       arguments)

    .. [[[end]]]
    """
    ret = copy.copy(wave)
    _bound_waveform(ret, indep_min, indep_max)
    return numpy.max(ret._dep_vector)


@pexdoc.pcontracts.contract(
    wave=Waveform, indep_min='None|number', indep_max='None|number'
)
def nmin(wave, indep_min=None, indep_max=None):
    r"""
    Returns the minimum of a waveform's dependent variable vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param indep_min: Independent vector start point of computation
    :type  indep_min: integer or float

    :param indep_max: Independent vector stop point of computation
    :type  indep_max: integer or float

    :rtype: float

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc(raised=True)) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.nmin

    :raises:
     * RuntimeError (Argument \`indep_max\` is not valid)

     * RuntimeError (Argument \`indep_min\` is not valid)

     * RuntimeError (Argument \`wave\` is not valid)

     * RuntimeError (Incongruent \`indep_min\` and \`indep_max\`
       arguments)

    .. [[[end]]]
    """
    ret = copy.copy(wave)
    _bound_waveform(ret, indep_min, indep_max)
    return numpy.min(ret._dep_vector)


@pexdoc.pcontracts.contract(wave=Waveform, unwrap=bool, rad=bool)
def phase(wave, unwrap=True, rad=True):
    r"""
    Returns the phase of a waveform's dependent variable vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param unwrap: Flag that indicates whether phase should change phase shifts
                   to their :code:`2*pi` complement (True) or not (False)
    :type  unwrap: boolean

    :param rad: Flag that indicates whether phase should be returned in radians
                (True) or degrees (False)
    :type  rad: boolean

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.phase

    :raises:
     * RuntimeError (Argument \`rad\` is not valid)

     * RuntimeError (Argument \`unwrap\` is not valid)

     * RuntimeError (Argument \`wave\` is not valid)

    .. [[[end]]]
    """
    ret = copy.copy(wave)
    ret.dep_units = 'rad' if rad else 'deg'
    ret.dep_name = 'phase({0})'.format(ret.dep_name)
    ret._dep_vector = (
        numpy.unwrap(numpy.angle(ret._dep_vector))
        if unwrap else
        numpy.angle(ret._dep_vector)
    )
    if not rad:
        ret._dep_vector = numpy.rad2deg(ret._dep_vector)
    return ret


@pexdoc.pcontracts.contract(wave=Waveform)
def real(wave):
    r"""
    Returns the real part of a waveform's dependent variable vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.real

    :raises: RuntimeError (Argument \`wave\` is not valid)

    .. [[[end]]]
    """
    return _operation(wave, 'real', wave.dep_units, numpy.real)



@pexdoc.pcontracts.contract(wave=Waveform, decimals='int,>=0')
def round(wave, decimals=0):
    r"""
    Rounds a waveform's dependent variable vector to a given number of decimal
    places

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param decimals: Number of decimals to round to
    :type  decimals: integer

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.round

    :raises:
     * RuntimeError (Argument \`decimals\` is not valid)

     * RuntimeError (Argument \`wave\` is not valid)

    .. [[[end]]]
    """
    # pylint: disable=W0622
    pexdoc.exh.addex(
        TypeError,
        'Cannot convert complex to integer',
        wave._dep_vector.dtype.name.startswith('complex')
    )
    ret = copy.copy(wave)
    ret.dep_name = 'round({0}, {1})'.format(ret.dep_name, decimals)
    ret._dep_vector = numpy.round(wave._dep_vector, decimals)
    return ret


@pexdoc.pcontracts.contract(wave=Waveform)
def sin(wave):
    r"""
    Returns the sine of a waveform's dependent variable vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for peng.wave_functions.sin

    :raises: RuntimeError (Argument \`wave\` is not valid)

    .. [[[end]]]
    """
    return _operation(wave, 'sin', '', numpy.sin)


@pexdoc.pcontracts.contract(wave=Waveform)
def sinh(wave):
    r"""
    Returns the hyperbolic sine of a waveform's dependent variable vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.sinh

    :raises: RuntimeError (Argument \`wave\` is not valid)

    .. [[[end]]]
    """
    return _operation(wave, 'sinh', '', numpy.sinh)


@pexdoc.pcontracts.contract(wave=Waveform)
def sqrt(wave):
    r"""
    Returns the square root of a waveform's dependent variable vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.sqrt

    :raises: RuntimeError (Argument \`wave\` is not valid)

    .. [[[end]]]
    """
    dep_units = '{0}**0.5'.format(wave.dep_units)
    return _operation(wave, 'sqrt', dep_units, numpy.sqrt)


@pexdoc.pcontracts.contract(
    wave=Waveform, dep_name='str|None',
    indep_min='None|number', indep_max='None|number', indep_step='None|number'
)
def subwave(
        wave, dep_name=None, indep_min=None, indep_max=None, indep_step=None
):
    r"""
    Returns a waveform that is a sub-set of a waveform, potentially re-sampled

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param  dep_name: Independent variable name
    :type   dep_name: `NonNullString <http://pexdoc.readthedocs.io/en/stable/
                        ptypes.html#nonnullstring>`_

    :param indep_min: Independent vector start point of computation
    :type  indep_min: integer or float

    :param indep_max: Independent vector stop point of computation
    :type  indep_max: integer or float

    :param indep_step: Independent vector step
    :type  indep_step: integer or float

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc(raised=True)) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.subwave

    :raises:
     * RuntimeError (Argument \`dep_name\` is not valid)

     * RuntimeError (Argument \`indep_max\` is not valid)

     * RuntimeError (Argument \`indep_min\` is not valid)

     * RuntimeError (Argument \`indep_step\` is greater than independent
       vector range)

     * RuntimeError (Argument \`indep_step\` is not valid)

     * RuntimeError (Argument \`wave\` is not valid)

     * RuntimeError (Incongruent \`indep_min\` and \`indep_max\`
       arguments)

    .. [[[end]]]
    """
    ret = copy.copy(wave)
    if dep_name is not None:
        ret.dep_name = dep_name
    _bound_waveform(ret, indep_min, indep_max)
    pexdoc.addai(
        'indep_step', bool((indep_step is not None) and (indep_step <= 0))
    )
    exmsg = 'Argument `indep_step` is greater than independent vector range'
    cond = bool(
        (indep_step is not None) and
        (indep_step > ret._indep_vector[-1]-ret._indep_vector[0]))
    pexdoc.addex(RuntimeError, exmsg, cond)
    if indep_step:
        indep_vector = _barange(indep_min, indep_max, indep_step)
        dep_vector = _interp_dep_vector(ret, indep_vector)
        ret._set_indep_vector(indep_vector, check=False)
        ret._set_dep_vector(dep_vector, check=False)
    return ret


@pexdoc.pcontracts.contract(wave=Waveform)
def tan(wave):
    r"""
    Returns the tangent of a waveform's dependent variable vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for peng.wave_functions.tan

    :raises: RuntimeError (Argument \`wave\` is not valid)

    .. [[[end]]]
    """
    return _operation(wave, 'tan', '', numpy.tan)


@pexdoc.pcontracts.contract(wave=Waveform)
def tanh(wave):
    r"""
    Returns the hyperbolic tangent of a waveform's dependent variable vector

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.tanh

    :raises: RuntimeError (Argument \`wave\` is not valid)

    .. [[[end]]]
    """
    return _operation(wave, 'tanh', '', numpy.tanh)


@pexdoc.pcontracts.contract(wave=Waveform)
def wcomplex(wave):
    r"""
    Converts a waveform's dependent variable vector to complex

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.wcomplex

    :raises: RuntimeError (Argument \`wave\` is not valid)

    .. [[[end]]]
    """
    ret = copy.copy(wave)
    ret._dep_vector = ret._dep_vector.astype(numpy.complex)
    return ret


@pexdoc.pcontracts.contract(wave=Waveform)
def wfloat(wave):
    r"""
    Converts a waveform's dependent variable vector to float

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.wfloat

    :raises:
     * RuntimeError (Argument \`wave\` is not valid)

     * TypeError (Cannot convert complex to float)

    .. [[[end]]]
    """
    pexdoc.exh.addex(
        TypeError,
        'Cannot convert complex to float',
        wave._dep_vector.dtype.name.startswith('complex')
    )
    ret = copy.copy(wave)
    ret._dep_vector = ret._dep_vector.astype(numpy.float)
    return ret


@pexdoc.pcontracts.contract(wave=Waveform)
def wint(wave):
    r"""
    Converts a waveform's dependent variable vector to integer

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.wint

    :raises:
     * RuntimeError (Argument \`wave\` is not valid)

     * TypeError (Cannot convert complex to integer)

    .. [[[end]]]
    """
    pexdoc.exh.addex(
        TypeError,
        'Cannot convert complex to integer',
        wave._dep_vector.dtype.name.startswith('complex')
    )
    ret = copy.copy(wave)
    ret._dep_vector = ret._dep_vector.astype(numpy.int)
    return ret


@pexdoc.pcontracts.contract(wave=Waveform, indep_var='number')
def wvalue(wave, indep_var):
    r"""
    Returns the dependent variable value at a given independent variable point.
    If the independent variable point is not in the independent variable vector
    the dependent variable value is obtained by linear interpolation

    :param wave: Waveform
    :type  wave: :py:class:`peng.eng.Waveform`

    :param indep_var: Independent variable point for which the dependent
                      variable is to be obtained
    :type  indep_var: integer or float

    :rtype: :py:class:`peng.eng.Waveform`

    .. [[[cog cog.out(exobj_eng.get_sphinx_autodoc()) ]]]
    .. Auto-generated exceptions documentation for
    .. peng.wave_functions.wvalue

    :raises:
     * RuntimeError (Argument \`indep_var\` is not valid)

     * RuntimeError (Argument \`wave\` is not valid)

     * ValueError (Argument \`indep_var\` is not in the independent
       variable vector range)

    .. [[[end]]]
    """
    close_min = numpy.isclose(
        indep_var, wave._indep_vector[0], FP_RTOL, FP_ATOL
    )
    close_max = numpy.isclose(
        indep_var, wave._indep_vector[-1], FP_RTOL, FP_ATOL
    )
    pexdoc.exh.addex(
        ValueError,
        'Argument `indep_var` is not in the independent variable vector range',
        bool(((indep_var < wave._indep_vector[0]) and (not close_min))
        or
        ((indep_var > wave._indep_vector[-1]) and (not close_max)))
    )
    if close_min:
        return wave._dep_vector[0]
    if close_max:
        return wave._dep_vector[-1]
    idx = numpy.searchsorted(wave._indep_vector, indep_var)
    xdelta = wave._indep_vector[idx]-wave._indep_vector[idx-1]
    ydelta = wave._dep_vector[idx]-wave._dep_vector[idx-1]
    slope = ydelta/float(xdelta)
    return wave._dep_vector[idx-1]+slope*(indep_var-wave._indep_vector[idx-1])
