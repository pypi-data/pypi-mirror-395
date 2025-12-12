from __future__ import annotations

"""
Provides analytic derivatives for some common base terms with the hope that we can reuse them elsewhere
"""

import collections
import itertools
import math
import enum
import warnings
import numpy as np
from .. import Devutils as dev
from .VectorOps import *
from . import TensorDerivatives as td
from . import Misc as misc

__all__ = [
    "triangle_convert",
    "triangle_converter",
    "triangle_area",
    "make_triangle",
    "make_symbolic_triangle",
    "triangle_property_specifiers",
    "triangle_completions",
    "triangle_completion_paths",
    "enumerate_triangle_completions",
    "triangle_is_complete",
    "triangle_property_function",
    "make_dihedron",
    "make_symbolic_dihedron",
    "dihedron_property_specifiers",
    "dihedral_completions",
    "dihedral_completion_paths",
    "dihedron_is_complete",
    "enumerate_dihedron_completions",
    "dihedron_property_function",
    "arcsin_deriv",
    "arccos_deriv",
    "arctan_deriv",
    "sin_deriv",
    "cos_deriv",
    "tan_deriv",
    "cot_deriv",
    "axis_rot_gen_deriv"
]


def law_of_cosines_cos(a, b, c):
    return ((a**2 + b**2) - c**2) / (2*a*b)
def law_of_sines_sin(a, b, A):
    return np.sin(A) * b / a
def law_of_sines_dist(a, B, A):
    return a * np.sin(B) / np.sin(A)
def law_of_cosines_dist(a, b, C):
    return np.sqrt(a**2 + b**2 - 2*a*b*np.cos(C))
def tri_sss_area(a, b, c):
    s = (a + b + c) / 2
    tris = np.sqrt(s * (s - a) * (s - b) * (s - c))
    return tris
def tri_sas_area(a, C, b):
    return 1/2 * (a * b * np.sin(C))
def tri_sss_to_sas(a, b, c):
    C = np.arccos(law_of_cosines_cos(a, b, c))
    return (a, C, b)
def tri_sss_to_ssa(a, b, c):
    A = np.arccos(law_of_cosines_cos(b, c, a))
    return (a, b, A)
def tri_sss_to_saa(a, b, c):
    A = np.arccos(law_of_cosines_cos(b, c, a))
    B = np.arccos(law_of_cosines_cos(a, c, b))
    return (a, B, A)
def tri_sss_to_asa(a, b, c):
    B = np.arccos(law_of_cosines_cos(a, c, b))
    C = np.arccos(law_of_cosines_cos(a, b, c))
    return (C, a, B)
def tri_sas_to_sss(a, C, b):
    c = law_of_cosines_dist(a, b, C)
    return (a, b, c)
def tri_sas_to_ssa(a, C, b):
    return tri_sss_to_ssa(*tri_sas_to_sss(a,C,b))
def tri_sas_to_saa(a, C, b):
    return tri_sss_to_saa(*tri_sas_to_sss(a,C,b))
def tri_sas_to_asa(a, C, b):
    return tri_sss_to_asa(*tri_sas_to_sss(a,C,b))
def _check_ssa(a, b, A):
    bs = b * np.sin(A)
    return np.logical_and(bs < a, a < b)
class SSAWarning(UserWarning):
    ...
def tri_ssa_to_sas(a, b, A):
    bad_pos = _check_ssa(a, b, A)
    if np.any(bad_pos):
        warnings.warn('SSA triangle provided non-unique solution, minimum chosen', SSAWarning)
    B = np.arcsin(law_of_sines_sin(a, b, A))
    C = np.pi - (A + B)
    return (a, C, b)
def tri_ssa_to_saa(a, b, A):
    bad_pos = _check_ssa(a, b, A)
    if np.any(bad_pos):
        warnings.warn('SSA triangle provided non-unique solution, minimum chosen', SSAWarning)
    B = np.arcsin(law_of_sines_sin(a, b, A))
    return (a, B, A)
def tri_ssa_to_asa(a, b, A):
    bad_pos = _check_ssa(a, b, A)
    if np.any(bad_pos):
        warnings.warn('SSA triangle provided non-unique solution, minimum chosen', SSAWarning)
    B = np.arcsin(law_of_sines_sin(a, b, A))
    C = np.pi - (A + B)
    return (C, a, B)
def tri_ssa_to_sss(a, b, A):
    return tri_sas_to_sss(*tri_ssa_to_sas(a, b, A))
def tri_saa_to_ssa(a, B, A):
    b = law_of_sines_dist(a, B, A)
    return (a, b, A)
def tri_saa_to_sas(a, B, A):
    b = law_of_sines_dist(a, B, A)
    C = np.pi - (A + B)
    return (a, C, b)
def tri_saa_to_asa(a, B, A):
    C = np.pi - (A + B)
    return (C, a, B)
def tri_saa_to_sss(a, B, A):
    return tri_sas_to_sss(*tri_saa_to_sas(a, B, A))
def tri_asa_to_saa(C, a, B):
    A = np.pi - (B + C)
    return (a, B, A)
def tri_asa_to_sas(C, a, B):
    A = np.pi - (B + C)
    b = law_of_sines_dist(a, B, A)
    return (a, C, b)
def tri_asa_to_ssa(C, a, B):
    A = np.pi - (B + C)
    b = law_of_sines_dist(a, B, A)
    return (a, b, A)
def tri_asa_to_sss(C, a, B):
    return tri_sas_to_sss(*tri_asa_to_sas(C, a, B))

def law_of_cosines_cos_deriv(a_expansion, b_expansion, c_expansion, order,
                             return_components=False,
                             a2_expansion=None,
                             b2_expansion=None,
                             c2_expansion=None,
                             abinv_expansion=None,
                             ab_expansion=None
                             ):
    if a2_expansion is None:
        a2_expansion = td.scalarprod_deriv(a_expansion, a_expansion, order)
    if b2_expansion is None:
        b2_expansion = td.scalarprod_deriv(b_expansion, b_expansion, order)
    if c2_expansion is None:
        c2_expansion = td.scalarprod_deriv(c_expansion, c_expansion, order)
    if abinv_expansion is None:
        if ab_expansion is None:
            ab_expansion = td.scalarprod_deriv(a_expansion, b_expansion, order)
        abinv_expansion = td.scalarinv_deriv(ab_expansion, order)
    term = td.scalarprod_deriv(
        (c2_expansion - (a2_expansion + b2_expansion)),
        abinv_expansion,
        order
    )
    if return_components:
        return term, (a2_expansion, b2_expansion, c2_expansion, abinv_expansion, ab_expansion)
    else:
        return term

def power_deriv(term, p, order):
    scaling = np.prod(p - np.arange(order))
    if scaling == 0:
        return np.zeros_like(term)
    else:
        return scaling * np.power(term, p - order)
def square_deriv(term, order):
    return power_deriv(term, 2, order)
def sqrt_deriv(term, order):
    return power_deriv(term, 1/2, order)
def cos_deriv(term, order):
    return np.cos(order*np.pi/2 + term)
def sin_deriv(term, order):
    return np.sin(order*np.pi/2 + term)
def legendre_scaling(n):
    if n > 1:
        rems, _ = integer_exponent(np.arange(1, n+1), 2)
        return np.prod(rems)
    else:
        return 1
def legendre_integer_coefficients(n):
    coeffs = np.zeros((n+1, n+1), dtype=int)
    coeffs[0, 0] = 1
    if n > 0:
        coeffs[1, 1] = 1
        if n > 1:
            ind_sets = np.arange(2, n+1)
            ind_sets = ind_sets - (ind_sets % 2)
            _, indicators = integer_exponent(ind_sets, 2)
            for i in range(n-2):
                m = (i+2)
                p1 = (2*m - 1) * np.roll(coeffs[i+1], 1)
                p2 = (m - 1) * coeffs[i]
                s2 = 2 ** indicators[i] # already shifted by a few bits
                s1 = s2 if i % 2 == 0 else 1
                coeffs[i+2] = (s1*p1 - s2*p2) // m
    return coeffs
def arcsin_deriv(term, order):
    #TODO: cache these
    coeffs = np.abs(legendre_integer_coefficients(order))
    scaling = legendre_scaling(order)
    sec_exp = np.cos(term)**(-(order+1))
    tan_exp = np.tan(term)**np.arange(order+1)
    return scaling*sec_exp*np.dot(tan_exp, coeffs[-1])
def arccos_deriv(term, order):
    #TODO: cache these
    coeffs = np.abs(legendre_integer_coefficients(order))
    scaling = legendre_scaling(order)
    s = np.sin(term)
    c = np.cos(term)
    csc_exp = np.sin(term)**(-(order+1))
    cot_exp = (c/s)**np.arange(order+1)
    return scaling*csc_exp*np.dot(cot_exp, coeffs[-1])
def tan_integer_coefficients(n):
    coeffs = np.zeros((n, n), dtype=int)
    coeffs[0, 0] = 1
    if n > 0:
        ind_sets = np.arange(2, n+1)
        _, indicators = integer_exponent(ind_sets[::2], 2)
        k_odd = np.arange(1, n+1)
        break_point = (n-(n%2))//2
        indicators = indicators - 1 # divided out a two from the scalings
        indicator_scalings = np.zeros_like(k_odd)
        indicator_scalings[::2] = indicators
        # used to figure out how many divisions the c_new terms can take
        indicator_subscalings = np.zeros_like(k_odd)
        k_rem, subscalings = integer_exponent(k_odd[:break_point], 2)
        k_even = np.zeros_like(k_odd)
        k_even[1::2] = k_rem
        indicator_subscalings[1::2] = subscalings
        for i in range(n-1):
            c = coeffs[i]
            c_new = np.roll(c, 1) + np.pad(c[1:], [0, 1])
            if i%2 == 1:
                coeffs[i + 1] = k_odd * c_new
            else:
                divs = indicator_scalings[i]
                div_diffs = indicator_subscalings - divs
                num = 2**np.clip(div_diffs, 0, np.inf)
                denom = 2**np.clip(-div_diffs, 0, np.inf)
                c_new = c_new // denom
                coeffs[i + 1] = k_even * num * c_new
    return coeffs
def tan_deriv(term, order):
    #TODO: cache these
    coeffs = tan_integer_coefficients(order)[-1]
    _, inds = integer_exponent(np.arange(1, order+1), 2)
    scaling = 2**np.sum(inds)
    t = np.tan(term)
    tan_exp = t**np.arange(order)
    return scaling*(1+t**2)*np.dot(tan_exp, coeffs)
def cot_deriv(term, order):
    return tan_deriv(np.pi/2 - term, order)
def arctan_deriv(term, order):
    powers = 2*np.arange(order//2 + (order%2)) + ((order + 1) % 2)
    fac = math.factorial(order-1)
    coeffs = np.array([math.comb(order, p) for p in powers]) #TODO: could speed this up...
    signs = (-1)**((order+powers)//2)
    coeffs = signs * coeffs
    d = (1+term**2)
    exps = powers
    return fac * np.dot(term**exps, coeffs) / d**order
def law_of_cosines_dist_deriv(a_expansion, b_expansion, C_expansion, order,
                              return_components=False,
                              a2_expansion=None,
                              b2_expansion=None,
                              abcosC_expansion=None,
                              ab_expansion=None,
                              cosC_expansion=None,
                              return_square=False
                              ):
    if a2_expansion is None:
        a2_expansion = td.scalarfunc_deriv(square_deriv, a_expansion, order)
    if b2_expansion is None:
        b2_expansion = td.scalarfunc_deriv(square_deriv, b_expansion, order)
    if abcosC_expansion is None:
        if ab_expansion is None:
            ab_expansion = td.scalarprod_deriv(a_expansion, b_expansion, order)
        if cosC_expansion is None:
            cosC_expansion = td.scalarfunc_deriv(cos_deriv, C_expansion, order)
        abcosC_expansion = td.scalarprod_deriv(ab_expansion, cosC_expansion, order)
    term = [a+b-2*c for a,b,c in zip(a2_expansion, b2_expansion, abcosC_expansion)]
    if not return_square:
        term = td.scalarfunc_deriv(sqrt_deriv, term, order)
    if return_components:
        return term, (a2_expansion, b2_expansion, abcosC_expansion, ab_expansion, abcosC_expansion, cosC_expansion)
    else:
        return term

def law_of_sines_sin_deriv(a_expansion, b_expansion, A_expansion, order,
                           return_components=False,
                           sinA_expansion=None,
                           binva_expansion=None,
                           ainv_expansion=None
                           ):
    if binva_expansion is None:
        if ainv_expansion is None:
            ainv_expansion = td.scalarinv_deriv(a_expansion, order)
        binva_expansion = td.scalarprod_deriv(b_expansion, ainv_expansion, order)
    if sinA_expansion is None:
        sinA_expansion = td.scalarfunc_deriv(sin_deriv, A_expansion, order)
    term = td.scalarprod_deriv(sinA_expansion, binva_expansion, order)

    if return_components:
        return term, (sinA_expansion, binva_expansion, ainv_expansion)
    else:
        return term
def law_of_sines_dist_deriv(a_expansion, B_expansion, A_expansion, order,
                              return_components=False,
                              sinBinvsinA_expansion=None,
                              sinA_expansion=None,
                              sinB_expansion=None,
                              sinAinv_expansion=None
                              ):
    if sinBinvsinA_expansion is None:
        if sinB_expansion is None:
            sinB_expansion = td.scalarfunc_deriv(sin_deriv, B_expansion, order)
        if sinAinv_expansion is None:
            if sinA_expansion is None:
                sinA_expansion = td.scalarfunc_deriv(sin_deriv, A_expansion, order)
            sinAinv_expansion = td.scalarinv_deriv(sinAinv_expansion, order)
        sinBinvsinA_expansion = td.scalarprod_deriv(sinB_expansion, sinAinv_expansion, order)
    term = td.scalarprod_deriv(a_expansion, sinBinvsinA_expansion, order)

    if return_components:
        return term, (sinBinvsinA_expansion, sinA_expansion, sinB_expansion, sinAinv_expansion)
    else:
        return term

def _angle_complement_expansion(A_expansion, B_expansion):
    return td.shift_expansion(
        td.scale_expansion(td.add_expansions(A_expansion, B_expansion), -1),
        np.pi
    )

def tri_sss_to_sas_deriv(a_expansion, b_expansion, c_expansion, order,
                         return_components=False,
                         return_cos=False,
                         a2_expansion=None,
                         b2_expansion=None,
                         c2_expansion=None,
                         abinv_expansion=None,
                         ab_expansion=None,
                         cosC_expansion=None
                         ):
    if cosC_expansion is None:
        cosC_expansion, (a2_expansion, b2_expansion, c2_expansion, abinv_expansion, ab_expansion) = law_of_cosines_cos_deriv(
            a_expansion, b_expansion, c_expansion, order,
            return_components=True,
            a2_expansion=a2_expansion,
            b2_expansion=b2_expansion,
            c2_expansion=c2_expansion,
            abinv_expansion=abinv_expansion,
            ab_expansion=ab_expansion
        )

    bits = (a2_expansion, b2_expansion, c2_expansion, abinv_expansion, ab_expansion, cosC_expansion)
    if not return_cos:
        C_expansion = td.scalarfunc_deriv(arccos_deriv, cosC_expansion, order)
    else:
        C_expansion = cosC_expansion

    if return_components:
        return (a_expansion, C_expansion, b_expansion), bits
    else:
        return (a_expansion, C_expansion, b_expansion)
def tri_sss_to_ssa_deriv(a_expansion, b_expansion, c_expansion, order,
                         return_components=False,
                         return_cos=False,
                         a2_expansion=None,
                         b2_expansion=None,
                         c2_expansion=None,
                         bcinv_expansion=None,
                         bc_expansion=None,
                         cosA_expansion=None
                         ):
    if cosA_expansion is None:
        cosA_expansion, bits = law_of_cosines_cos_deriv(
            b_expansion, c_expansion, a_expansion, order,
            return_components=True,
            a2_expansion=a2_expansion,
            b2_expansion=b2_expansion,
            c2_expansion=c2_expansion,
            abinv_expansion=bcinv_expansion,
            ab_expansion=bc_expansion
        )
    else:
        bits = (a2_expansion, b2_expansion, c2_expansion, bcinv_expansion, bc_expansion)
    bits = bits + (cosA_expansion,)
    if not return_cos:
        A_expansion = td.scalarfunc_deriv(arccos_deriv, cosA_expansion, order)
    else:
        A_expansion = cosA_expansion

    if return_components:
        return (a_expansion, b_expansion, A_expansion), bits
    else:
        return (a_expansion, b_expansion, A_expansion)
def tri_sss_to_saa_deriv(a_expansion, b_expansion, c_expansion, order,
                         return_components=False,
                         return_cos=False,
                         a2_expansion=None,
                         b2_expansion=None,
                         c2_expansion=None,
                         acinv_expansion=None,
                         ac_expansion=None,
                         bcinv_expansion=None,
                         bc_expansion=None,
                         cosA_expansion=None,
                         cosB_expansion=None
                         ):
    if cosA_expansion is None:
        cosA_expansion, (b2_expansion, c2_expansion, a2_expansion, bcinv_expansion, bc_expansion) = law_of_cosines_cos_deriv(
            b_expansion, c_expansion, a_expansion, order,
            return_components=True,
            a2_expansion=a2_expansion,
            b2_expansion=b2_expansion,
            c2_expansion=c2_expansion,
            abinv_expansion=bcinv_expansion,
            ab_expansion=bc_expansion
        )
    if cosB_expansion is None:
        cosB_expansion, (a2_expansion, c2_expansion, b2_expansion, acinv_expansion, ac_expansion) = law_of_cosines_cos_deriv(
            a_expansion, c_expansion, b_expansion, order,
            return_components=True,
            a2_expansion=a2_expansion,
            b2_expansion=b2_expansion,
            c2_expansion=c2_expansion,
            abinv_expansion=acinv_expansion,
            ab_expansion=ac_expansion
        )

    bits = (
        a2_expansion,
        b2_expansion,
        c2_expansion,
        acinv_expansion,
        ac_expansion,
        bcinv_expansion,
        bc_expansion,
        cosA_expansion,
        cosB_expansion
    )

    if not return_cos:
        A_expansion = td.scalarfunc_deriv(arccos_deriv, cosA_expansion, order)
        B_expansion = td.scalarfunc_deriv(arccos_deriv, cosB_expansion, order)
    else:
        A_expansion = cosA_expansion
        B_expansion = cosB_expansion

    if return_components:
        return (a_expansion, B_expansion, A_expansion), bits
    else:
        return(a_expansion, B_expansion, A_expansion)
def tri_sss_to_asa_deriv(a_expansion, b_expansion, c_expansion, order,
                         return_components=False,
                         return_cos=False,
                         a2_expansion=None,
                         b2_expansion=None,
                         c2_expansion=None,
                         abinv_expansion=None,
                         ab_expansion=None,
                         acinv_expansion=None,
                         ac_expansion=None,
                         cosB_expansion=None,
                         cosC_expansion=None
                         ):
    if cosB_expansion is None:
        cosB_expansion, (a2_expansion, c2_expansion, b2_expansion, acinv_expansion, ac_expansion) = law_of_cosines_cos_deriv(
            a_expansion, c_expansion, b_expansion, order,
            return_components=True,
            a2_expansion=a2_expansion,
            b2_expansion=b2_expansion,
            c2_expansion=c2_expansion,
            abinv_expansion=acinv_expansion,
            ab_expansion=ac_expansion
        )
    if cosC_expansion is None:
        cosC_expansion, (a2_expansion, b2_expansion, c2_expansion, acinv_expansion, ac_expansion) = law_of_cosines_cos_deriv(
            a_expansion, b_expansion, c_expansion, order,
            return_components=True,
            a2_expansion=a2_expansion,
            b2_expansion=b2_expansion,
            c2_expansion=c2_expansion,
            abinv_expansion=abinv_expansion,
            ab_expansion=ab_expansion
        )

    bits = (
        a2_expansion,
        b2_expansion,
        c2_expansion,
        abinv_expansion,
        ab_expansion,
        acinv_expansion,
        ac_expansion,
        cosB_expansion,
        cosC_expansion
    )

    if not return_cos:
        C_expansion = td.scalarfunc_deriv(arccos_deriv, cosC_expansion, order)
        B_expansion = td.scalarfunc_deriv(arccos_deriv, cosB_expansion, order)
    else:
        C_expansion = cosC_expansion
        B_expansion = cosB_expansion

    if return_components:
        return (C_expansion, a_expansion, B_expansion), bits
    else:
        return (C_expansion, a_expansion, B_expansion)
def tri_sas_to_sss_deriv(a_expansion, C_expansion, b_expansion, order,
                         return_components=False,
                         a2_expansion=None,
                         b2_expansion=None,
                         abcosC_expansion=None,
                         ab_expansion=None,
                         cosC_expansion=None,
                         return_square=False
                         ):
    c_expansion, bits = law_of_cosines_dist_deriv(a_expansion, b_expansion, C_expansion, order,
                                                  a2_expansion=a2_expansion,
                                                  b2_expansion=b2_expansion,
                                                  abcosC_expansion=abcosC_expansion,
                                                  ab_expansion=ab_expansion,
                                                  cosC_expansion=cosC_expansion,
                                                  return_components=True,
                                                  return_square=return_square)
    if return_components:
        return (a_expansion, b_expansion, c_expansion), bits
    else:
        return (a_expansion, b_expansion, c_expansion)
def tri_sas_to_ssa_deriv(a_expansion, b_expansion, C_expansion, order,
                         return_components=False,
                         return_cos=False,
                         a2_expansion=None,
                         b2_expansion=None,
                         c2_expansion=None,
                         abcosC_expansion=None,
                         ab_expansion=None,
                         cosC_expansion=None,
                         bcinv_expansion=None,
                         bc_expansion=None,
                         cosA_expansion=None,
                         ):
    (a_expansion, b_expansion, c_expansion), (
        a2_expansion,
        b2_expansion,
        abcosC_expansion,
        ab_expansion,
        cosC_expansion
    ) = tri_sas_to_sss_deriv(a_expansion, b_expansion, C_expansion, order,
                                                                   return_components=True,
                                                                   a2_expansion=a2_expansion,
                                                                   b2_expansion=b2_expansion,
                                                                   abcosC_expansion=abcosC_expansion,
                                                                   ab_expansion=ab_expansion,
                                                                   cosC_expansion=cosC_expansion
                                                                   )
    (a_expansion, b_expansion, A_expansion), (
        a2_expansion,
        b2_expansion,
        c2_expansion,
        bcinv_expansion,
        bc_expansion,
        cosA_expansion
    ) = tri_sss_to_ssa_deriv(a_expansion, b_expansion, c_expansion, order,
                             return_components=False,
                             return_cos=return_cos,
                             a2_expansion=a2_expansion,
                             b2_expansion=b2_expansion,
                             c2_expansion=c2_expansion,
                             bcinv_expansion=bcinv_expansion,
                             bc_expansion=bc_expansion,
                             cosA_expansion=cosA_expansion
                             )
    if return_components:
        return (a_expansion, b_expansion, A_expansion), (
            a2_expansion,
            b2_expansion,
            c2_expansion,
            abcosC_expansion,
            ab_expansion,
            cosC_expansion,
            bcinv_expansion,
            bc_expansion,
            cosA_expansion
        )
    else:
        return (a_expansion, b_expansion, A_expansion)
def tri_sas_to_saa_deriv(a_expansion, b_expansion, C_expansion, order,
                         return_components=False,
                         return_cos=False,
                         a2_expansion=None,
                         b2_expansion=None,
                         c2_expansion=None,
                         abcosC_expansion=None,
                         ab_expansion=None,
                         cosC_expansion=None,
                         acinv_expansion=None,
                         ac_expansion=None,
                         bcinv_expansion=None,
                         bc_expansion=None,
                         cosA_expansion=None,
                         cosB_expansion=None
                         ):
    (a_expansion, b_expansion, c_expansion), (
        a2_expansion,
        b2_expansion,
        abcosC_expansion,
        ab_expansion,
        cosC_expansion
    ) = tri_sas_to_sss_deriv(a_expansion, b_expansion, C_expansion, order,
                                                                   return_components=True,
                                                                   a2_expansion=a2_expansion,
                                                                   b2_expansion=b2_expansion,
                                                                   abcosC_expansion=abcosC_expansion,
                                                                   ab_expansion=ab_expansion,
                                                                   cosC_expansion=cosC_expansion
                                                                   )
    (a_expansion, B_expansion, A_expansion), (
        a2_expansion,
        b2_expansion,
        c2_expansion,
        acinv_expansion,
        ac_expansion,
        bcinv_expansion,
        bc_expansion,
        cosA_expansion,
        cosB_expansion
    ) = tri_sss_to_saa_deriv(a_expansion, b_expansion, c_expansion, order,
                             return_components=True,
                             return_cos=return_cos,
                             a2_expansion=a2_expansion,
                             b2_expansion=b2_expansion,
                             c2_expansion=c2_expansion,
                             acinv_expansion=acinv_expansion,
                             ac_expansion=ac_expansion,
                             bcinv_expansion=bcinv_expansion,
                             bc_expansion=bc_expansion,
                             cosA_expansion=cosA_expansion,
                             cosB_expansion=cosB_expansion
                             )
    if return_components:
        return (a_expansion, B_expansion, A_expansion), (
            a2_expansion,
            b2_expansion,
            c2_expansion,
            abcosC_expansion,
            ab_expansion,
            cosC_expansion,
            acinv_expansion,
            ac_expansion,
            bcinv_expansion,
            bc_expansion,
            cosA_expansion,
            cosB_expansion
        )
    else:
        return (a_expansion, B_expansion, A_expansion)
def tri_sas_to_asa_deriv(a_expansion, b_expansion, C_expansion, order,
                         return_components=False,
                         return_cos=False,
                         a2_expansion=None,
                         b2_expansion=None,
                         c2_expansion=None,
                         abcosC_expansion=None,
                         ab_expansion=None,
                         cosC_expansion=None,
                         abinv_expansion=None,
                         acinv_expansion=None,
                         ac_expansion=None,
                         cosB_expansion=None
                         ):
    (a_expansion, b_expansion, c_expansion), (
        a2_expansion,
        b2_expansion,
        abcosC_expansion,
        ab_expansion,
        cosC_expansion
    ) = tri_sas_to_sss_deriv(a_expansion, b_expansion, C_expansion, order,
                                                                   return_components=True,
                                                                   a2_expansion=a2_expansion,
                                                                   b2_expansion=b2_expansion,
                                                                   abcosC_expansion=abcosC_expansion,
                                                                   ab_expansion=ab_expansion,
                                                                   cosC_expansion=cosC_expansion
                                                                   )
    (C_expansion, a_expansion, B_expansion), (
        a2_expansion,
        b2_expansion,
        c2_expansion,
        abinv_expansion,
        ab_expansion,
        acinv_expansion,
        ac_expansion,
        cosB_expansion,
        cosC_expansion
    ) = tri_sss_to_asa_deriv(a_expansion, b_expansion, c_expansion, order,
                             return_components=True,
                             return_cos=return_cos,
                             a2_expansion=a2_expansion,
                             b2_expansion=b2_expansion,
                             c2_expansion=c2_expansion,
                             abinv_expansion=abinv_expansion,
                             ab_expansion=ab_expansion,
                             acinv_expansion=acinv_expansion,
                             ac_expansion=ac_expansion,
                             cosB_expansion=cosB_expansion,
                             cosC_expansion=cosC_expansion
                             )

    if return_components:
        return (C_expansion, a_expansion, B_expansion), (
            a2_expansion,
            b2_expansion,
            c2_expansion,
            abcosC_expansion,
            ab_expansion,
            cosC_expansion,
            abinv_expansion,
            acinv_expansion,
            ac_expansion,
            cosB_expansion
        )
    else:
        return (C_expansion, a_expansion, B_expansion)
def tri_ssa_to_sas_deriv(a_expansion, b_expansion, A_expansion, order,
                         return_components=False,
                         sinA_expansion=None,
                         binva_expansion=None,
                         ainv_expansion=None,
                         B_expansion=None,
                         sinB_expansion=None
                         ):
    if B_expansion is None:
        if sinB_expansion is None:
            sinB_expansion = law_of_sines_sin_deriv(a_expansion, b_expansion, A_expansion, order,
                                                    return_components=True,
                                                    sinA_expansion=sinA_expansion,
                                                    binva_expansion=binva_expansion,
                                                    ainv_expansion=ainv_expansion
                                                    )
        B_expansion = td.scalarfunc_deriv(arcsin_deriv, sinB_expansion, order)

    bits = (
        sinA_expansion,
        binva_expansion,
        ainv_expansion,
        B_expansion,
        sinB_expansion
    )

    C_expansion = _angle_complement_expansion(A_expansion, B_expansion)

    if return_components:
        return (a_expansion, C_expansion, b_expansion), bits
    else:
        return (a_expansion, C_expansion, b_expansion)
def tri_ssa_to_saa_deriv(a_expansion, b_expansion, A_expansion, order,
                         return_components=False,
                         sinA_expansion=None,
                         binva_expansion=None,
                         ainv_expansion=None,
                         B_expansion=None,
                         sinB_expansion=None
                         ):
    if B_expansion is None:
        if sinB_expansion is None:
            sinB_expansion = law_of_sines_sin_deriv(a_expansion, b_expansion, A_expansion, order,
                                                    return_components=True,
                                                    sinA_expansion=sinA_expansion,
                                                    binva_expansion=binva_expansion,
                                                    ainv_expansion=ainv_expansion
                                                    )
        B_expansion = td.scalarfunc_deriv(arcsin_deriv, sinB_expansion, order)

    bits = (
        sinA_expansion,
        binva_expansion,
        ainv_expansion,
        B_expansion,
        sinB_expansion
    )

    if return_components:
        return (a_expansion, B_expansion, A_expansion), bits
    else:
        return (a_expansion, B_expansion, A_expansion)
def tri_ssa_to_asa_deriv(a_expansion, b_expansion, A_expansion, order,
                         return_components=False,
                         sinA_expansion=None,
                         binva_expansion=None,
                         ainv_expansion=None,
                         B_expansion=None,
                         sinB_expansion=None
                         ):
    if B_expansion is None:
        if sinB_expansion is None:
            sinB_expansion = law_of_sines_sin_deriv(a_expansion, b_expansion, A_expansion, order,
                                                    return_components=True,
                                                    sinA_expansion=sinA_expansion,
                                                    binva_expansion=binva_expansion,
                                                    ainv_expansion=ainv_expansion
                                                    )
        B_expansion = td.scalarfunc_deriv(arcsin_deriv, sinB_expansion, order)

    bits = (
        sinA_expansion,
        binva_expansion,
        ainv_expansion,
        B_expansion,
        sinB_expansion
    )

    C_expansion = _angle_complement_expansion(A_expansion, B_expansion)

    if return_components:
        return (C_expansion, a_expansion, B_expansion), bits
    else:
        return (C_expansion, a_expansion, B_expansion)
def tri_ssa_to_sss_deriv(
        a_expansion, b_expansion, A_expansion, order,
        return_components=False,
        sinA_expansion=None,
        binva_expansion=None,
        ainv_expansion=None,
        B_expansion=None,
        sinB_expansion=None,
        a2_expansion=None,
        b2_expansion=None,
        abcosC_expansion=None,
        ab_expansion=None,
        cosC_expansion=None,
):
    (a_expansion, C_expansion, b_expansion), (
        sinA_expansion,
        binva_expansion,
        ainv_expansion,
        B_expansion,
        sinB_expansion
    ) = tri_ssa_to_sas_deriv(a_expansion, b_expansion, A_expansion, order,
                             return_components=True,
                             sinA_expansion=sinA_expansion,
                             binva_expansion=binva_expansion,
                             ainv_expansion=ainv_expansion,
                             B_expansion=B_expansion,
                             sinB_expansion=sinB_expansion
                             )

    (a_expansion, b_expansion, c_expansion), (
        a2_expansion,
        b2_expansion,
        abcosC_expansion,
        ab_expansion,
        cosC_expansion,
    ) = tri_sas_to_sss_deriv(a_expansion, C_expansion, b_expansion, order,
                             return_components=True,
                             a2_expansion=a2_expansion,
                             b2_expansion=b2_expansion,
                             abcosC_expansion=abcosC_expansion,
                             ab_expansion=ab_expansion,
                             cosC_expansion=cosC_expansion,
                             return_square=False
                             )
    if return_components:
        return (a_expansion, b_expansion, c_expansion), (
            sinA_expansion,
            binva_expansion,
            ainv_expansion,
            B_expansion,
            sinB_expansion,
            a2_expansion,
            b2_expansion,
            abcosC_expansion,
            ab_expansion,
            cosC_expansion
        )
    else:
        return (a_expansion, b_expansion, c_expansion)
def tri_saa_to_ssa_deriv(a_expansion, B_expansion, A_expansion, order,
                         return_components=False,
                         sinBinvsinA_expansion=None,
                         sinA_expansion=None,
                         sinB_expansion=None,
                         sinAinv_expansion=None):
    b_expansion, bits = law_of_sines_dist_deriv(a_expansion, B_expansion, A_expansion, order,
                                                return_components=True,
                                                sinBinvsinA_expansion=sinBinvsinA_expansion,
                                                sinA_expansion=sinA_expansion,
                                                sinB_expansion=sinB_expansion,
                                                sinAinv_expansion=sinAinv_expansion
                                                )
    if return_components:
        return (a_expansion, b_expansion, A_expansion), bits
    else:
        return (a_expansion, b_expansion, A_expansion)
def tri_saa_to_sas_deriv(a_expansion, B_expansion, A_expansion, order,
                         return_components=False,
                         sinBinvsinA_expansion=None,
                         sinA_expansion=None,
                         sinB_expansion=None,
                         sinAinv_expansion=None):
    b_expansion, bits = law_of_sines_dist_deriv(a_expansion, B_expansion, A_expansion, order,
                                                return_components=True,
                                                sinBinvsinA_expansion=sinBinvsinA_expansion,
                                                sinA_expansion=sinA_expansion,
                                                sinB_expansion=sinB_expansion,
                                                sinAinv_expansion=sinAinv_expansion
                                                )

    C_expansion = _angle_complement_expansion(A_expansion, B_expansion)

    if return_components:
        return (a_expansion, C_expansion, b_expansion), bits
    else:
        return (a_expansion, C_expansion, b_expansion)
def tri_saa_to_asa_deriv(a_expansion, B_expansion, A_expansion, order):
    C_expansion = _angle_complement_expansion(A_expansion, B_expansion)
    return (C_expansion, a_expansion, B_expansion)
def tri_saa_to_sss_deriv(a_expansion, B_expansion, A_expansion, order,
                         return_components=False,
                         sinBinvsinA_expansion=None,
                         sinA_expansion=None,
                         sinB_expansion=None,
                         sinAinv_expansion=None,
                         a2_expansion=None,
                         b2_expansion=None,
                         abcosC_expansion=None,
                         ab_expansion=None,
                         cosC_expansion=None,
                         return_square=False
                         ):
    (a_expansion, C_expansion, b_expansion), (
        sinBinvsinA_expansion,
        sinA_expansion,
        sinB_expansion,
        sinAinv_expansion
    ) = tri_saa_to_sas_deriv(a_expansion, B_expansion, A_expansion,
                             order,
                             return_components=True,
                             sinBinvsinA_expansion=sinBinvsinA_expansion,
                             sinA_expansion=sinA_expansion,
                             sinB_expansion=sinB_expansion,
                             sinAinv_expansion=sinAinv_expansion,
                             )
    (a_expansion, b_expansion, c_expansion), (
        a2_expansion,
        b2_expansion,
        abcosC_expansion,
        ab_expansion,
        cosC_expansion,
    ) = tri_sas_to_sss_deriv(
        a_expansion, C_expansion, b_expansion, order,
        return_components=True,
        a2_expansion=a2_expansion,
        b2_expansion=b2_expansion,
        abcosC_expansion=abcosC_expansion,
        ab_expansion=ab_expansion,
        cosC_expansion=cosC_expansion,
        return_square=return_square
    )

    if return_components:
        return (a_expansion, b_expansion, c_expansion), (
            sinBinvsinA_expansion,
            sinA_expansion,
            sinB_expansion,
            sinAinv_expansion,
            a2_expansion,
            b2_expansion,
            abcosC_expansion,
            ab_expansion,
            cosC_expansion
        )
    else:
        return (a_expansion, b_expansion, c_expansion)
def tri_asa_to_saa_deriv(C_expansion, a_expansion, B_expansion, order):
    A_expansion = _angle_complement_expansion(C_expansion, B_expansion)
    return (a_expansion, B_expansion, A_expansion)
def tri_asa_to_sas_deriv(C_expansion, a_expansion, B_expansion, order,
                         return_components=False,
                         A_expansion=None,
                         sinBinvsinA_expansion=None,
                         sinA_expansion=None,
                         sinB_expansion=None,
                         sinAinv_expansion=None
                         ):
    if A_expansion is None:  # TODO: skip this if other components are supplied
        A_expansion = _angle_complement_expansion(C_expansion, B_expansion)
    b_expansion, (
        sinBinvsinA_expansion,
        sinA_expansion,
        sinB_expansion,
        sinAinv_expansion
    ) = law_of_sines_dist_deriv(a_expansion, B_expansion, A_expansion, order,
                                                sinBinvsinA_expansion=sinBinvsinA_expansion,
                                                sinA_expansion=sinA_expansion,
                                                sinB_expansion=sinB_expansion,
                                                sinAinv_expansion=sinAinv_expansion,
                                                return_components=True
                                                )
    if return_components:
        return (a_expansion, C_expansion, b_expansion), (
            A_expansion,
            sinBinvsinA_expansion,
            sinA_expansion,
            sinB_expansion,
            sinAinv_expansion
        )
    else:
        return (a_expansion, C_expansion, b_expansion)
def tri_asa_to_ssa_deriv(C_expansion, a_expansion, B_expansion, order,
                         return_components=False,
                         A_expansion=None,
                         sinBinvsinA_expansion=None,
                         sinA_expansion=None,
                         sinB_expansion=None,
                         sinAinv_expansion=None
                         ):
    if A_expansion is None:  # TODO: skip this if other components are supplied
        A_expansion = _angle_complement_expansion(C_expansion, B_expansion)
    b_expansion, (
        sinBinvsinA_expansion,
        sinA_expansion,
        sinB_expansion,
        sinAinv_expansion
    ) = law_of_sines_dist_deriv(a_expansion, B_expansion, A_expansion, order,
                                sinBinvsinA_expansion=sinBinvsinA_expansion,
                                sinA_expansion=sinA_expansion,
                                sinB_expansion=sinB_expansion,
                                sinAinv_expansion=sinAinv_expansion,
                                return_components=True
                                )
    if return_components:
        return (a_expansion, b_expansion, A_expansion), (
            sinBinvsinA_expansion,
            sinA_expansion,
            sinB_expansion,
            sinAinv_expansion
        )
    else:
        return (a_expansion, b_expansion, A_expansion)
def tri_asa_to_sss_deriv(C_expansion, a_expansion, B_expansion, order,
                   return_components=False,
                   A_expansion=None,
                   sinBinvsinA_expansion=None,
                   sinA_expansion=None,
                   sinB_expansion=None,
                   sinAinv_expansion=None,
                   a2_expansion=None,
                   b2_expansion=None,
                   abcosC_expansion=None,
                   ab_expansion=None,
                   cosC_expansion=None,
                   return_square=False
                   ):
    (a_expansion, C_expansion, b_expansion), bits = tri_asa_to_sas_deriv(C_expansion, a_expansion, B_expansion, order,
                         return_components=True,
                         A_expansion=A_expansion,
                         sinBinvsinA_expansion=sinBinvsinA_expansion,
                         sinA_expansion=sinA_expansion,
                         sinB_expansion=sinB_expansion,
                         sinAinv_expansion=sinAinv_expansion
                         )
    (a_expansion, b_expansion, c_expansion), bits2 = tri_sas_to_sss_deriv(
        a_expansion, C_expansion, b_expansion, order,
        return_components=True,
        a2_expansion=a2_expansion,
        b2_expansion=b2_expansion,
        abcosC_expansion=abcosC_expansion,
        ab_expansion=ab_expansion,
        cosC_expansion=cosC_expansion,
        return_square=return_square
    )
    if return_components:
        return (a_expansion, b_expansion, c_expansion), bits + bits2
    else:
        return (a_expansion, b_expansion, c_expansion)

class TriangleType(enum.Enum):
    SSS = "sss"
    SAS = "sas"
    SSA = "ssa"
    SAA = "saa"
    ASA = "asa"
def _echo_tri_args(x, y, z):
    return (x, y, z)
def _echo_tri_deriv_args(x_expansion, y_expansion, z_expansion, order, return_components=False, **kwargs):
    if return_components:
        return (x_expansion, y_expansion, z_expansion), kwargs
    else:
        return (x_expansion, y_expansion, z_expansion)
def triangle_converter(type1:str|TriangleType, type2:str|TriangleType):
    # only 9 possible conversions, let's just write them down
    type1 = TriangleType(type1)
    type2 = TriangleType(type2)
    if type1 == TriangleType.SSS:
        if type2 == TriangleType.SSS:
            return (_echo_tri_args, _echo_tri_deriv_args)
        elif type2 == TriangleType.SAS:
            return (tri_sss_to_sas, tri_sss_to_sas_deriv)
        elif type2 == TriangleType.SSA:
            return (tri_sss_to_ssa, tri_sss_to_ssa_deriv)
        elif type2 == TriangleType.SAA:
            return (tri_sss_to_saa, tri_sss_to_saa_deriv)
        elif type2 == TriangleType.ASA:
            return (tri_sss_to_asa, tri_sss_to_asa_deriv)
    elif type1 == TriangleType.SAS:
        if type2 == TriangleType.SSS:
            return (tri_sas_to_sss, tri_sas_to_sss_deriv)
        elif type2 == TriangleType.SAS:
            return (_echo_tri_args, _echo_tri_deriv_args)
        elif type2 == TriangleType.SSA:
            return (tri_sas_to_ssa, tri_sas_to_ssa_deriv)
        elif type2 == TriangleType.SAA:
            return (tri_sas_to_saa, tri_sas_to_saa_deriv)
        elif type2 == TriangleType.ASA:
            return (tri_sas_to_saa, tri_sas_to_asa_deriv)
    elif type1 == TriangleType.SSA:
        if type2 == TriangleType.SSS:
            return (tri_ssa_to_sss, tri_ssa_to_sss_deriv)
        elif type2 == TriangleType.SAS:
            return (tri_ssa_to_sas, tri_ssa_to_sas_deriv)
        elif type2 == TriangleType.SSA:
            return (_echo_tri_args, _echo_tri_deriv_args)
        elif type2 == TriangleType.SAA:
            return (tri_ssa_to_saa, tri_ssa_to_saa_deriv)
        elif type2 == TriangleType.ASA:
            return (tri_ssa_to_asa, tri_ssa_to_asa_deriv)
    elif type1 == TriangleType.SAA:
        if type2 == TriangleType.SSS:
            return (tri_saa_to_sss, tri_saa_to_sss_deriv)
        elif type2 == TriangleType.SAS:
            return (tri_saa_to_sas, tri_saa_to_sas_deriv)
        elif type2 == TriangleType.SSA:
            return (tri_saa_to_ssa, tri_saa_to_ssa_deriv)
        elif type2 == TriangleType.SAA:
            return (_echo_tri_args, _echo_tri_deriv_args)
        elif type2 == TriangleType.ASA:
            return (tri_ssa_to_sss, tri_ssa_to_sss_deriv)
    elif type1 == TriangleType.ASA:
        if type2 == TriangleType.SSS:
            return (tri_asa_to_sss, tri_asa_to_sss_deriv)
        elif type2 == TriangleType.SAS:
            return (tri_asa_to_sas, tri_asa_to_sas_deriv)
        elif type2 == TriangleType.SSA:
            return (tri_asa_to_ssa, tri_asa_to_ssa_deriv)
        elif type2 == TriangleType.SAA:
            return (tri_asa_to_saa, tri_asa_to_saa_deriv)
        elif type2 == TriangleType.ASA:
            return (_echo_tri_args, _echo_tri_deriv_args)
    return None
def triangle_convert(tri_spec, type1:str|TriangleType, type2:str|TriangleType, order=None, **kwargs):
    converter, deriv_converter = triangle_converter(type1, type2)
    if converter is None:
        raise ValueError(f"can't convert from triangle type {type1} to triangle type {type2}")
    b1,b2,b3 = tri_spec
    if order is None:
        b1 = np.asanyarray(b1)
        b2 = np.asanyarray(b2)
        b3 = np.asanyarray(b3)
        return converter(b1, b2, b3)
    else:
        b1 = [np.asanyarray(b) for b in b1]
        b2 = [np.asanyarray(b) for b in b2]
        b3 = [np.asanyarray(b) for b in b3]
        return deriv_converter(b1, b2, b3, order, **kwargs)
def triangle_area(tri_spec, type:str|TriangleType):
    type = TriangleType(type)
    b1,b2,b3 = tri_spec
    b1 = np.asanyarray(b1)
    b2 = np.asanyarray(b2)
    b3 = np.asanyarray(b3)
    if type == TriangleType.SSS:
        return tri_sss_area(b1, b2, b3)
    elif type == TriangleType.SAS:
        return tri_sas_area(b1, b2, b3)
    else:
        return tri_sas_area(*triangle_convert(tri_spec, type, TriangleType.SAS))


TriangleData = collections.namedtuple("TriangleData",
                                      ["a", "b", "c", "A", "B", "C"]
                                      )
_tdata_name_map = {'a':0,'b':1,'c':2,'A':3,'B':4,'C':5}
_triangle_point_map = {'a':(0,1),'b':(1,2),'c':(0,2),'A':(0,2,1),'B':(1,0,2),'C':(0,1,2)}
def triangle_property_specifiers(base_specifier=None):
    if base_specifier is None:
        return {
            k:triangle_property_specifiers(k)
            for k in _tdata_name_map
        }
    else:
        if isinstance(base_specifier, str):
            return {
                "name":base_specifier,
                "index":_tdata_name_map[base_specifier],
                "coord":_triangle_point_map[base_specifier]
            }
        elif misc.is_int(base_specifier):
            for k,v in _tdata_name_map.items():
                if v == base_specifier:
                    return triangle_property_specifiers(k)
            else:
                raise ValueError(f"can't interpret specifier {base_specifier}")
        else:
            for k,v in _triangle_point_map.items():
                if v == base_specifier:
                    return triangle_property_specifiers(k)
            else:
                raise ValueError(f"can't interpret specifier {base_specifier}")
def make_triangle(points=None, *, a=None, b=None, c=None, A=None, B=None, C=None):
    if points is not None:
        a,c,b = distance_matrix(points, return_triu=True)
    return TriangleData(a, b, c, A, B, C)
def _symbolic_triangle_field(val, field_name, triangle, inds, use_pos):
    if val is not None:
        return val
    elif triangle is not None:
        if _tri_prop(triangle, field_name) is not None:
            if use_pos is True:
                return _tdata_name_map[field_name]
            elif inds is True:
                return _triangle_point_map[field_name]
            elif inds is not None:
                return tuple(inds[p] for p in _triangle_point_map[field_name])
            elif use_pos is not None and use_pos is not False:
                return use_pos[_ddata_name_map[field_name]]
            else:
                return field_name
        else:
            return None
    elif use_pos is True:
        return _tdata_name_map[field_name]
    elif inds is True:
        return _triangle_point_map[field_name]
    elif inds is not None:
        return tuple(inds[p] for p in _triangle_point_map[field_name])
    elif use_pos is not None and use_pos is not False:
        return use_pos[_ddata_name_map[field_name]]
    else:
        return field_name
def make_symbolic_triangle(
        triangle=None,
        indices=None,
        positions=False,
        a=None, b=None, c=None,
        A=None, B=None, C=None
):
    return make_triangle(
        a=_symbolic_triangle_field(a, "a", triangle, indices, positions),
        b=_symbolic_triangle_field(b, "b", triangle, indices, positions),
        c=_symbolic_triangle_field(c, "c", triangle, indices, positions),
        A=_symbolic_triangle_field(A, "A", triangle, indices, positions),
        B=_symbolic_triangle_field(B, "B", triangle, indices, positions),
        C=_symbolic_triangle_field(C, "C", triangle, indices, positions),
    )
def _check_triangle_type(tdata, inds):
    return all(
        tdata[i if not isinstance(i, str) else _tdata_name_map[i]]
        is not None
        for i in inds
    )
def _check_bond_valid_triangle(td_1):
    bc_1 = sum(x is not None for x in [td_1.a, td_1.b, td_1.c])
    ac_1 = sum(x is not None for x in [td_1.A, td_1.B, td_1.C])
    return (
            bc_1 == 3
            or (bc_1 == 2 and ac_1 >= 1)
            or (bc_1 == 1 and ac_1 >= 2)
    )
def _check_angle_valid_triangle(td_1):
    bc_1 = sum(x is not None for x in [td_1.a, td_1.b, td_1.c])
    ac_1 = sum(x is not None for x in [td_1.A, td_1.B, td_1.C])
    return (
            ac_1 >= 2
            or bc_1 == 3
            or (bc_1 == 2 and ac_1 == 1)
    )
def _get_triangle_completions(tri:TriangleData):
    # omits the SSA triangles, should add in via flag
    bc_1 = sum(x is not None for x in [tri.a, tri.b, tri.c])
    ac_1 = sum(x is not None for x in [tri.A, tri.B, tri.C])
    if _check_bond_valid_triangle(tri): # TODO: reuse args
        return None
    elif bc_1 == 2: # ac_1 == 0
        if tri.a is not None:
            if tri.b is not None:
                return [('c',), ('C',)]
            else:
                return [('b',), ('B',)]
        else: # b and c are not none by exclusion
            return [('a',), ('A',)]
    elif bc_1 == 1: # ac_1 <= 1
        if tri.a is not None:
            if ac_1 == 0:
                return [('b', 'c'), ('b', 'C'), ('c','B'), ('B', 'C'), ('A', 'B'), ('C', 'A')]
            elif tri.A is not None:
                return [('B',), ('C',)]
            elif tri.B is not None:
                return [("c",), ('A',), ('C',)]
            else: #tri.C is not None
                return [("b",), ('A',), ('B',)]
        elif tri.b is not None:
            if ac_1 == 0:
                return [('a', 'c'), ('a', 'C'), ('c','A'), ('A', 'C'), ('A', 'B'), ('C', 'B')]
            elif tri.A is not None:
                return [('c',), ('B',), ('C',)]
            elif tri.B is not None:
                return [('A',), ('C',)]
            else: #tri.C is not None
                return [("a",), ('A',), ('B',)]
        else: #tri.c is not None
            if ac_1 == 0:
                return [('a', 'b'), ('a', 'B'), ('b','A'), ('A', 'B'), ('A', 'C'), ('B', 'C')]
            elif tri.A is not None:
                return [('b',), ('B',), ('C',)]
            elif tri.B is not None:
                return [('a',), ('A',), ('C',)]
            else: #tri.C is not None
                return [('A',), ('B',)]
    elif ac_1 == 2: # bc_1 == 0
        # any side length works, no angle works
        return [('a',), ('b',), ('c',)]
    elif ac_1 == 1:
        if tri.A is not None:
            return [('b', 'c'), ('b', 'B'), ('c', 'C'), ('a', 'B'), ('a', 'C'), ('b', 'C'), ('c', 'B')]
        elif tri.B is not None:
            return [('a', 'c'), ('a', 'A'), ('c', 'C'), ('b', 'A'), ('b', 'C'), ('a', 'C'), ('c', 'A')]
        else: # tri.C is not None
            return [('a', 'b'), ('a', 'A'), ('b', 'B'), ('c', 'A'), ('c', 'B'), ('a', 'B'), ('b', 'A')]
    else: # literally nothing supplied...we'll omit the ssa triangles
        return [
            ('a', 'b', 'c'), # sss
            ('a', 'b', 'C'), # sas
            ('a', 'B', 'c'),
            ('A', 'b', 'c'),
            ('a', 'B', 'C'), # asa
            ('A', 'b', 'C'),
            ('A', 'B', 'c'),
            ('a', 'B', 'A'), # saa
            ('a', 'C', 'A'),
            ('b', 'A', 'B'),
            ('b', 'C', 'B'),
            ('c', 'A', 'C'),
            ('c', 'B', 'C')
        ]
def triangle_is_complete(tri:TriangleData):
    return _check_bond_valid_triangle(tri)
def _permutation_trie(comb_lists):
    _ = []
    trie = {}
    for c,completion_func in comb_lists:
        for p in itertools.permutations(c):
            t = trie
            for k in p[:-1]:
                if k in t:
                    if not isinstance(t[k], dict): break
                else:
                    t[k] = {}
                t = t[k]
            else:
                t[p[-1]] = (c, completion_func)
    return trie
def _expand_trie(t):
    comps = {}
    queue = collections.deque()
    for k,v in t.items():
        queue.append([[k], v])
    while queue:
        prev, new = queue.pop()
        if not isinstance(new, dict):
            completion,function = new
            comps[tuple(completion)] = function
            continue
        queue.extend(
            [prev + [k], v]
            for k, v in new.items()
        )
    return comps
def _expand_trie_iter(t, sorting=None):
    queue = collections.deque()
    for k,v in t.items():
        queue.append([[k], v, -1])
    sort_map = {}
    while queue:
        prev, new, sort_max = queue.pop()
        if not isinstance(new, dict):
            if new is True:
                yield tuple(prev), None
            else:
                completion,function = new
                yield tuple(completion), function
            continue
        if sorting is None:
            queue.extend(
                [prev + [k], v, -1]
                for k, v in new.items()
            )
        else:
            for k, v in new.items():
                if k not in sort_map:
                    sort_map[k] = sorting.index(k)
                if sort_max < sort_map[k]:
                    queue.append([prev + [k], v, sort_map[k]])
def _completion_paths(dd, completions_trie, prop_func, return_trie=False):
    queue = collections.deque([[[], completions_trie]])
    fall_throughs = []
    res = None
    while res is None and queue:
        path, trie = queue.popleft()
        subpaths = []
        for k,v in trie.items():
            test_prop = prop_func(dd, k)
            if test_prop is not None:
                subpaths.append(k)
                if not isinstance(v, dict):
                    res = v
                    break
                queue.append([path+[k], v])
        else:
            fall_throughs.append([path, trie])
    if res is not None:
        return True, res
    else:
        return False, [
                (p, _expand_trie(t) if not return_trie else t)
                for p,t in fall_throughs
            ]
#TODO: move this Trie stuff into some other package
def _trie_delete(trie:dict, key):
    return {
        k:_trie_delete(v, key) if v is not True else v
        for k,v in trie.items()
        if k != key
    }
def _trie_add(trie:dict, key):
    t = {
        k:_trie_add(v, key) if v is not True else v
        for k,v in trie.items()
    }
    t[key] = trie
    return t
def _trie_replace(trie:dict, key1, key2):
    return {
        (key2 if k == key1 else k):_trie_replace(v, key1, key2) if v is not True else v
        for k,v in trie.items()
    }
def _trie_short_circuit(trie:dict, key):
    trie = _trie_delete(trie, key)
    trie[key] = True
    return trie
def _trie_join(trie1, trie2):
    return {
        k: _trie_join(v, trie2) if v is not True else trie2
        for k, v in trie1.items()
    }
def _trie_merge(trie1, trie2):
    return dev.merge_dicts(trie1, trie2)
    trie = trie1.copy()
    for k,v in trie2.items():
        trie[k] = v
    return trie
def _trie_del_add(trie1, key, key2):
    return _trie_add(_trie_delete(trie1, key), key2)
def _dist_completions_trie(b, c, A, B, C):
    return {
        b: {c: True, C: True},
        c: {b: True, B: True},
        B: {c: True, A: True, C: True},
        C: {b: True, A: True, B: True},
        A: {B: True, C: True}
    }
def _angle_completions_trie(a, b, c, B, C, angle_only=True):
    return {
        a: {B: True, C: True},
        b: {c: True, B:True, C: True},
        c: {b: True, B:True, C: True},
        B: (
            {a:True, b:True, c: True, C: True}
                if angle_only else
            {a:True, b:True, c: True}
        ),
        C: (
            {a:True, c:True, b: True, B: True}
                if angle_only else
            {a:True, c:True, b: True}
        )
    }
def _triangle_completable_trie(a, b, c, A, B, C, require_all=True):
    return {
            a: _dist_completions_trie(b, c, A, B, C),
            b: _dist_completions_trie(a, c, B, A, C),
            c: _dist_completions_trie(a, b, C, A, B),
            A: _angle_completions_trie(a, b, c, B, C, angle_only=not require_all),
            B: _angle_completions_trie(b, a, c, A, C, angle_only=not require_all),
            C: _angle_completions_trie(c, a, b, A, B, angle_only=not require_all)
        }
def enumerate_triangle_completions(tdata:TriangleData):
    if _check_bond_valid_triangle(tdata):
        yield ()
    else:
        order = ["a", "b", "c", "A", "B", "C"]
        base_trie = _triangle_completable_trie(*order)
        for var in order:
            if _tri_prop(tdata, var) is not None:
                base_trie = base_trie[var]
        for l, _ in _expand_trie_iter(base_trie, sorting=order):
            yield l

def _triangle_data_permute(tdata:TriangleData, perm):
    a,b,c,A,B,C = tdata
    bls = [a,b,c]
    ang = [A,B,C]
    bls = [bls[p] for p in perm]
    ang = [ang[p] for p in perm]
    return TriangleData(*bls, *ang)
def _triangle_property_c(tdata:TriangleData):
    if tdata.c is not None:
        return tdata.c, tdata
    else:
        updates = {}
        #TODO: support getting intermediate properties
        if _check_triangle_type(tdata, ['a','C','b']):
            c = triangle_convert([tdata.a,tdata.C,tdata.b], 'sas', 'sss')[2]
            updates['c'] = c
        elif _check_triangle_type(tdata, ['a','B','A']):
            _, b, c = triangle_convert([tdata.a,tdata.B,tdata.A], 'saa', 'sss')
            updates['b'] = b
            updates['c'] = c
        elif _check_triangle_type(tdata, ['b', 'A', 'B']):
            _, a, c = triangle_convert([tdata.b, tdata.A, tdata.B], 'saa', 'sss')
            updates['a'] = a
            updates['c'] = c
        elif _check_triangle_type(tdata, ['C', 'a', 'B']):
            _, b, c = triangle_convert([tdata.C, tdata.a, tdata.B], 'asa', 'sss')
            updates['b'] = b
            updates['c'] = c
        elif _check_triangle_type(tdata, ['C', 'b', 'A']):
            _, a, c = triangle_convert([tdata.C, tdata.b, tdata.A], 'asa', 'sss')
            updates['a'] = a
            updates['c'] = c
        elif _check_triangle_type(tdata, ['a', 'b', 'A']):
            c = triangle_convert([tdata.b, tdata.A, tdata.B], 'ssa', 'sss')[2]
            updates['c'] = c
        elif _check_triangle_type(tdata, ['b', 'a', 'B']):
            c = triangle_convert([tdata.b, tdata.A, tdata.B], 'ssa', 'sss')[2]
            updates['c'] = c
        else:
            raise ValueError("not enough information to complete triangle")
        return c, triangle_modify(tdata, updates)
def _triangle_property_a(tdata):
    c, tnew = _triangle_property_c(_triangle_data_permute(tdata, [2, 1, 0]))
    return c, _triangle_data_permute(tnew, [2, 1, 0])
def _triangle_property_b(tdata):
    c, tnew = _triangle_property_c(_triangle_data_permute(tdata, [0, 2, 1]))
    return c, _triangle_data_permute(tnew, [0, 2, 1])
def _triangle_property_C(tdata:TriangleData):
    if tdata.C is not None:
        return tdata.C, tdata
    else:
        updates = {}
        #TODO: support getting intermediate properties
        if _check_triangle_type(tdata, ['a','b','c']):
            C = triangle_convert([tdata.a,tdata.b,tdata.c], 'sss', 'sas')[1]
            updates['C'] = C
        elif _check_triangle_type(tdata, ['a','B','c']):
            _, C, A = triangle_convert([tdata.a,tdata.B,tdata.c], 'sas', 'saa')
            updates['A'] = A
            updates['C'] = C
        elif _check_triangle_type(tdata, ['b','A','c']):
            _, C, B = triangle_convert([tdata.b,tdata.A,tdata.c], 'sas', 'saa')
            updates['B'] = B
            updates['C'] = C
        elif _check_triangle_type(tdata, ['a','B','A']):
            _, C, b = triangle_convert([tdata.a,tdata.B,tdata.A], 'saa', 'sas')
            updates['b'] = b
            updates['C'] = C
        elif _check_triangle_type(tdata, ['b', 'A', 'B']):
            _, C, a = triangle_convert([tdata.b, tdata.A, tdata.B], 'saa', 'sas')
            updates['a'] = a
            updates['C'] = C
        elif _check_triangle_type(tdata, ['A', 'c', 'B']):
            _, _, C = triangle_convert([tdata.A, tdata.c, tdata.B], 'asa', 'saa')
            updates['C'] = C
        elif _check_triangle_type(tdata, ['a', 'b', 'A']):
            C = triangle_convert([tdata.b, tdata.A, tdata.B], 'ssa', 'sas')[1]
            updates['C'] = C
        elif _check_triangle_type(tdata, ['b', 'a', 'B']):
            C = triangle_convert([tdata.b, tdata.A, tdata.B], 'ssa', 'sas')[1]
            updates['C'] = C
        else:
            raise ValueError("not enough information to complete triangle")
        return C, triangle_modify(tdata, updates)
def _triangle_property_A(tdata):
    C, tnew = _triangle_property_C(_triangle_data_permute(tdata, [2, 1, 0]))
    return C, _triangle_data_permute(tnew, [2, 1, 0])
def _triangle_property_B(tdata):
    C, tnew = _triangle_property_C(_triangle_data_permute(tdata, [0, 2, 1]))
    return C, _triangle_data_permute(tnew, [0, 2, 1])
def triangle_modify(tdata:TriangleData, updates:dict):
    a, b, c, A, B, C = tdata
    new_data = [a, b, c, A, B, C]
    for k,v in updates.items():
        if isinstance(k, str):
            k = _tdata_name_map[k]
        new_data[k] = v
    return TriangleData(*new_data)
def _tri_prop(tdata:TriangleData, field_name):
    return tdata[_tdata_name_map[field_name]]
def _triangle_has_prop(tdata:TriangleData, field_name):
    return tdata[_tdata_name_map[field_name]] is not None
def triangle_property(tdata:TriangleData, field_name, allow_completion=True):
    if allow_completion:
        if field_name == "a":
            return _triangle_property_a(tdata)
        elif field_name == "b":
            return _triangle_property_b(tdata)
        elif field_name == "c":
            return _triangle_property_c(tdata)
        elif field_name == "A":
            return _triangle_property_A(tdata)
        elif field_name == "B":
            return _triangle_property_B(tdata)
        elif field_name == "C":
            return _triangle_property_C(tdata)
        else:
            raise ValueError(f"bad property name {field_name}")
    else:
        return _tri_prop(tdata, field_name)

def _triangle_property_c_from_sas(a, C, b):
    return tri_sas_to_sss(a, C, b)[2]
def _triangle_property_c_from_saa(a, B, A):
    return tri_saa_to_sss(a, B, A)[2]
def _triangle_property_c_from_asa(C, a, B):
    return tri_asa_to_sas(B, a, C)[2]
def _triangle_property_C_from_sss(a, b, c):
    return tri_sss_to_sas(a, b, c)[1]
def _triangle_property_C_from_sas(a, B, c):
    return tri_sas_to_saa(a, B, c)[1]
def _triangle_property_C_from_saa(a, B, A):
    return tri_saa_to_sas(a, B, A)[1]
def _triangle_property_C_from_asa(A, c, B):
    return tri_asa_to_sas(A, c, B)[1]
def triangle_completions_c(a, b, A, B, C):
    return _permutation_trie(
            [
                ([a, C, b], _triangle_property_c_from_sas),
                ([a, B, A], _triangle_property_c_from_saa),
                ([b, A, B], _triangle_property_c_from_saa),
                ([C, a, B], _triangle_property_c_from_asa),
                ([C, b, A], _triangle_property_c_from_asa)
            ]
        )
def triangle_completions_C(a, b, c, A, B):
    return _permutation_trie(
            [
                ([a, b, c], _triangle_property_C_from_sss),
                ([a, B, c], _triangle_property_C_from_sas),
                ([b, A, c], _triangle_property_C_from_sas),
                ([a, B, A], _triangle_property_C_from_saa),
                ([b, A, B], _triangle_property_C_from_saa),
                ([A, c, B], _triangle_property_c_from_asa)
            ]
        )
class TriangleCoordinateType(enum.Enum):
    Distance = "distance"
    Angle = "angle"
def triangle_completions_trie(tdata:TriangleData, field_name, return_args=False):
    if field_name == tdata.a:
        args = tdata.b, tdata.c, tdata.B, tdata.C, tdata.A
        type = TriangleCoordinateType.Distance
    elif field_name == tdata.b:
        args = tdata.a, tdata.c, tdata.A, tdata.C, tdata.B
        type = TriangleCoordinateType.Distance
    elif field_name == tdata.c:
        args = tdata.a, tdata.b, tdata.A, tdata.B, tdata.C
        type = TriangleCoordinateType.Distance
    elif field_name == tdata.A:
        args = tdata.b, tdata.c, tdata.a, tdata.B, tdata.C
        type = TriangleCoordinateType.Angle
    elif field_name == tdata.B:
        args = tdata.a, tdata.c, tdata.b, tdata.A, tdata.C
        type = TriangleCoordinateType.Angle
    elif field_name == tdata.C:
        args = tdata.a, tdata.b, tdata.c, tdata.A, tdata.B
        type = TriangleCoordinateType.Angle
    else:
        raise ValueError(f"can't interepret field name {field_name}")

    if type == TriangleCoordinateType.Distance:
        trie = triangle_completions_c(*args)
    else:
        trie = triangle_completions_C(*args)

    if return_args:
        return (args, type), trie
    else:
        return trie
def triangle_completions(field_name, return_trie=False, return_args=False, **triangle_values):
    dd = make_symbolic_triangle(**triangle_values)
    args, trie = triangle_completions_trie(dd, field_name, return_args=True)
    if not return_trie:
        completions = _expand_trie(trie)
    else:
        completions = trie
    if return_args:
        return args, completions
    else:
        return completions
def triangle_completion_paths(tdata: TriangleData, field_name,
                              return_trie=False,
                              indices=None,
                              positions=False,
                              return_args=False
                              ):
    field_name = _tri_prop(make_symbolic_triangle(indices=indices, positions=positions), field_name)
    args, completions_trie = triangle_completions(field_name,
                                                  return_trie=True,
                                                  return_args=True,
                                                  indices=indices,
                                                  positions=positions)

    tri = make_symbolic_triangle(tdata, indices=indices, positions=positions)
    res = _completion_paths(tri, completions_trie, _tri_prop, return_trie=return_trie)

    if return_args:
        return args, res
    else:
        return res
def triangle_property_function(sample_tri: TriangleData, field_name,
                               raise_on_missing=True
                               ):
    if _tri_prop(sample_tri, field_name) is not None:
        if isinstance(field_name, str):
            field_name = _tdata_name_map[field_name]

        ind = field_name
        def convert(tdata):
            return tdata[ind]
        return convert
    else:
        args, (complete, conversion_specs) = triangle_completion_paths(
            sample_tri,
            field_name,
            return_trie=True,
            return_args=True
        )
        if complete:
            args, func = conversion_specs
            inds = [
                _tdata_name_map[a]
                    if isinstance(a, str) else
                a
                for a in args
            ]
            def convert(tdata):
                return func(*(tdata[i] for i in inds))
            return convert
        else:
            if raise_on_missing:
                raise ValueError(f"can't get property '{field_name}' from {sample_tri}")
            else:
                return None
            # try to find conversions for subterms

def dihedral_z_from_abcXYt(a, b, c, X, Y, tau, use_cos=False):
    """
    a^2 + b^2 + c^2 - 2 (
        a b Cos[\[Alpha]] + b c Cos[\[Beta]]
        + a c (Cos[\[Tau]] Sin[\[Alpha]] Sin[\[Beta]] - Cos[\[Alpha]] Cos[\[Beta]])
       )
    """
    ca = np.cos(X)
    cb = np.cos(Y)
    sa = np.sin(X)
    sb = np.sin(Y)
    if use_cos:
        ct = tau
    else:
        ct = np.cos(tau)
    # distinct from just computing the missing triangle and applying the law of cosines, but very similar
    return np.sqrt(
        a**2+b**2+c**2
        - 2*(a*b*ca + b*c*cb + a*c*(ct*sa*sb-ca*cb))
    )

def dihedral_z_from_abcXYt_deriv(a_expansion, b_expansion, c_expansion,
                                 X_expansion, Y_expansion, tau_expansion,
                                 order,
                                 return_components=False,
                                 return_square=False,
                                 cos_X_expansion=None,
                                 cos_Y_expansion=None,
                                 sin_X_expansion=None,
                                 sin_Y_expansion=None,
                                 cos_tau_expansion=None,
                                 a2_expansion=None,
                                 b2_expansion=None,
                                 c2_expansion=None,
                                 ab_cos_X_expansion=None,
                                 ab_expansion=None,
                                 bc_cos_Y_expansion=None,
                                 bc_expansion=None,
                                 ac_expansion=None,
                                 cos_X_cos_Y_expansion=None,
                                 sin_X_sin_Y_expansion=None
                                 ):

    if ab_cos_X_expansion is None:
        if ab_expansion is None:
            ab_expansion = td.scalarprod_deriv(a_expansion, b_expansion, order)
        if cos_X_expansion is None:
            cos_X_expansion = td.scalarfunc_deriv(cos_deriv, X_expansion, order)
        ab_cos_X_expansion = td.scalarprod_deriv(
            ab_expansion,
            cos_X_expansion,
            order
        )

    if bc_cos_Y_expansion is None:
        if bc_expansion is None:
            bc_expansion = td.scalarprod_deriv(b_expansion, c_expansion, order)
        if cos_Y_expansion is None:
            cos_Y_expansion = td.scalarfunc_deriv(cos_deriv, Y_expansion, order)
        bc_cos_Y_expansion = td.scalarprod_deriv(
            bc_expansion,
            cos_Y_expansion,
            order
        )

    if cos_X_cos_Y_expansion is None:
        if cos_X_expansion is None:
            cos_X_expansion = td.scalarfunc_deriv(cos_deriv, X_expansion, order)
        if cos_Y_expansion is None:
            cos_Y_expansion = td.scalarfunc_deriv(cos_deriv, Y_expansion, order)
        cos_X_cos_Y_expansion = td.scalarprod_deriv(
            cos_X_expansion,
            cos_Y_expansion,
            order
        )

    if sin_X_sin_Y_expansion is None:
        if sin_X_expansion is None:
            sin_X_expansion = td.scalarfunc_deriv(sin_deriv, X_expansion, order)
        if sin_Y_expansion is None:
            sin_Y_expansion = td.scalarfunc_deriv(sin_deriv, Y_expansion, order)
        sin_X_sin_Y_expansion = td.scalarprod_deriv(
            sin_X_expansion,
            sin_Y_expansion,
            order
        )

    if cos_tau_expansion is None:
        cos_tau_expansion = td.scalarfunc_deriv(cos_deriv, tau_expansion, order)

    if a2_expansion is None:
        a2_expansion = td.scalarfunc_deriv(square_deriv, a_expansion, order)
    if b2_expansion is None:
        b2_expansion = td.scalarfunc_deriv(square_deriv, b_expansion, order)
    if c2_expansion is None:
        c2_expansion = td.scalarfunc_deriv(square_deriv, c_expansion, order)

    if ac_expansion is None:
        ac_expansion = td.scalarprod_deriv(a_expansion, c_expansion, order)
    extra_cos_term = td.scalarprod_deriv(
        ac_expansion,
        td.subtract_expansions(
            td.scalarprod_deriv(cos_tau_expansion, sin_X_sin_Y_expansion, order),
            cos_X_cos_Y_expansion
        ),
        order
    )

    r2_term = td.add_expansions(a2_expansion, b2_expansion, c2_expansion)
    radj_term = td.scale_expansion(
        td.add_expansions(
            ab_cos_X_expansion,
            bc_cos_Y_expansion,
            extra_cos_term
        ),
        2
    )

    # np.sqrt(
    #     a ** 2 + b ** 2 + c ** 2
    #     - 2 * (a * b * ca + b * c * cb + a * c * (ct * sa * sb - ca * cb))
    # )

    term = td.subtract_expansions(r2_term, radj_term)
    if not return_square:
        term = td.scalarfunc_deriv(sqrt_deriv, term, order)

    if return_components:
        return term, (
            cos_X_expansion,
            cos_Y_expansion,
            sin_X_expansion,
            sin_Y_expansion,
            cos_tau_expansion,
            a2_expansion,
            b2_expansion,
            c2_expansion,
            ab_cos_X_expansion,
            ab_expansion,
            bc_cos_Y_expansion,
            bc_expansion,
            ac_expansion,
            cos_X_cos_Y_expansion,
            sin_X_sin_Y_expansion
        )
    else:
        return term
def dihedral_z_from_abcxYt(a, b, c, x, Y, tau, use_cos=False):
    a2 = a**2
    b2 = b**2
    x2 = x**2
    ca = (a2+b2-x2)/(2*a*b)
    cb = np.cos(Y)
    sa = np.sqrt(1-ca**2)
    sb = np.sin(Y)
    if use_cos:
        ct = tau
    else:
        ct = np.cos(tau)
    return np.sqrt(
        x2+c**2 - 2*(b*c*cb + a*c*(ct*sa*sb-ca*cb))
    )
def _dist_cos_expansion(a2_expansion, b2_expansion, x2_expansion, ab_expansion, order):
    # (a2+b2-x2)/(2*a*b)
    return td.scale_expansion(
        td.scalarprod_deriv(
            td.subtract_expansions(td.add_expansions(a2_expansion, b2_expansion), x2_expansion),
            td.scalarinv_deriv(ab_expansion, order),
            order
        ),
        1 / 2
    )
def dihedral_z_from_abcxYt_deriv(a_expansion, b_expansion, c_expansion, x_expansion,
                                 Y_expansion, tau_expansion, order,
                                 return_components=False,
                                 return_square=False,
                                 cos_X_expansion=None,
                                 cos_Y_expansion=None,
                                 sin_X_expansion=None,
                                 sin_Y_expansion=None,
                                 cos_tau_expansion=None,
                                 a2_expansion=None,
                                 b2_expansion=None,
                                 c2_expansion=None,
                                 x2_expansion=None,
                                 ab_expansion=None,
                                 bc_cos_Y_expansion=None,
                                 bc_expansion=None,
                                 ac_expansion=None,
                                 cos_X_cos_Y_expansion=None,
                                 sin_X_sin_Y_expansion=None
                                 ):
    if a2_expansion is None:
        a2_expansion = td.scalarfunc_deriv(square_deriv, a_expansion, order)
    if b2_expansion is None:
        b2_expansion = td.scalarfunc_deriv(square_deriv, b_expansion, order)
    if c2_expansion is None:
        c2_expansion = td.scalarfunc_deriv(square_deriv, c_expansion, order)
    if x2_expansion is None:
        x2_expansion = td.scalarfunc_deriv(square_deriv, x_expansion, order)
    if cos_X_cos_Y_expansion is None:
        if cos_X_expansion is None:
            if ab_expansion is None:
                ab_expansion = td.scalarprod_deriv(a_expansion, b_expansion, order)
            cos_X_expansion = _dist_cos_expansion(a2_expansion, b2_expansion, x2_expansion, ab_expansion, order)
        if cos_Y_expansion is None:
            cos_Y_expansion = td.scalarfunc_deriv(cos_deriv, Y_expansion, order)
        cos_X_cos_Y_expansion = td.scalarprod_deriv(cos_X_expansion, cos_Y_expansion, order)
    if sin_X_sin_Y_expansion is None:
        if sin_X_expansion is None:
            ca2 = td.scalarfunc_deriv(square_deriv, cos_X_expansion, order)
            sin_X_expansion = td.scalarfunc_deriv(
                sqrt_deriv,
                td.shift_expansion(td.scale_expansion(ca2, -1), 1),
                order
            )
        if sin_Y_expansion is None:
            sin_Y_expansion = td.scalarfunc_deriv(sin_deriv, Y_expansion, order)
        sin_X_sin_Y_expansion = td.scalarprod_deriv(sin_X_expansion, sin_Y_expansion, order)
    if cos_tau_expansion is None:
        cos_tau_expansion = td.scalarfunc_deriv(cos_deriv, tau_expansion, order)

    if bc_cos_Y_expansion is None:
        if bc_expansion is None:
            bc_expansion = td.scalarprod_deriv(b_expansion, c_expansion, order)
        if cos_Y_expansion is None:
            cos_Y_expansion = td.scalarfunc_deriv(cos_deriv, Y_expansion, order)
        bc_cos_Y_expansion = td.scalarprod_deriv(bc_expansion, cos_Y_expansion, order)
    # x2+c**2 - 2*(b*c*cb + a*c*(ct*sa*sb-ca*cb))
    if ac_expansion is None:
        ac_expansion = td.scalarprod_deriv(a_expansion, c_expansion, order)
    extra_cos_term = td.scalarprod_deriv(
        ac_expansion,
        td.subtract_expansions(
            td.scalarprod_deriv(cos_tau_expansion, sin_X_sin_Y_expansion, order),
            cos_X_cos_Y_expansion
        ),
        order
    )
    r2_term = td.add_expansions(x2_expansion, c2_expansion)
    radj_term = td.scale_expansion(
        td.add_expansions(
            bc_cos_Y_expansion,
            extra_cos_term
        ),
        2
    )

    term = td.subtract_expansions(r2_term, radj_term)
    if not return_square:
        term = td.scalarfunc_deriv(sqrt_deriv, term, order)

    if return_components:
        return term, (
            cos_X_expansion,
            cos_Y_expansion,
            sin_X_expansion,
            sin_Y_expansion,
            cos_tau_expansion,
            a2_expansion,
            b2_expansion,
            c2_expansion,
            x2_expansion,
            ab_expansion,
            bc_cos_Y_expansion,
            bc_expansion,
            ac_expansion,
            cos_X_cos_Y_expansion,
            sin_X_sin_Y_expansion
        )
    else:
        return term
def dihedral_z_from_abcxyt(a,b, c, x, y, tau, use_cos=False):
    # potentially more stable than just computing the sin and cos in the usual way...
    xp = (a+b)**2
    xm = (a-b)**2
    yp = (b+c)**2
    ym = (b-c)**2
    x2 = x**2
    y2 = y**2
    a2 = a**2
    b2 = b**2
    c2 = c**2
    if use_cos:
        ct = tau
    else:
        ct = np.cos(tau)
    return np.sqrt(
        x2+y2-b2
        + (
                (a2+b2-x2)*(b2+c2-y2)
                -np.sqrt((xm - x2)*(xp - x2)*(ym - y2)*(yp - y2))*ct
        )/(2*b2)
    )

def dihedral_z_from_abcxyt_deriv(
        a_expansion, b_expansion, c_expansion, x_expansion, y_expansion, tau_expansion,
        order,
        return_components=False,
        return_square=False,
        a2_expansion=None,
        b2_expansion=None,
        c2_expansion=None,
        x2_expansion=None,
        y2_expansion=None,
        cos_tau_expansion=None,
        abplus_expansion=None,
        abminus_expansion=None,
        bcplus_expansion=None,
        bcminus_expansion=None,
        det_expansion=None,
):
    # potentially more stable than just computing the sin and cos in the usual way...
    if x2_expansion is None:
        x2_expansion = td.scalarpow_deriv(x_expansion, 2, order)
    if y2_expansion is None:
        y2_expansion = td.scalarpow_deriv(y_expansion, 2, order)
    if a2_expansion is None:
        a2_expansion = td.scalarpow_deriv(a_expansion, 2, order)
    if b2_expansion is None:
        b2_expansion = td.scalarpow_deriv(b_expansion, 2, order)
    if c2_expansion is None:
        c2_expansion = td.scalarpow_deriv(c_expansion, 2, order)
    if cos_tau_expansion is None:
        cos_tau_expansion = td.scalarfunc_deriv(cos_deriv, tau_expansion, order)

    if det_expansion is None:
        if abplus_expansion is None:
            abplus_expansion = td.scalarpow_deriv(td.add_expansions(a_expansion, b_expansion), 2, order)
        if abminus_expansion is None:
            abminus_expansion = td.scalarpow_deriv(td.subtract_expansions(a_expansion, b_expansion), 2, order)
        if bcplus_expansion is None:
            bcplus_expansion = td.scalarpow_deriv(td.add_expansions(b_expansion, c_expansion), 2, order)
        if bcminus_expansion is None:
            bcminus_expansion = td.scalarpow_deriv(td.subtract_expansions(b_expansion, c_expansion), 2, order)
        # np.sqrt((xm - x2)*(xp - x2)*(ym - y2)*(yp - y2))
        abp = td.subtract_expansions(abplus_expansion, x2_expansion)
        abm = td.subtract_expansions(abminus_expansion, x2_expansion)
        bcp = td.subtract_expansions(bcplus_expansion, y2_expansion)
        bcm = td.subtract_expansions(bcminus_expansion, y2_expansion)
        det_expansion = td.scalarfunc_deriv(sqrt_deriv,
                                            td.scalarprod_deriv(
                                                td.scalarprod_deriv(abm, abp, order),
                                                td.scalarprod_deriv(bcm, bcp, order),
                                                order
                                            ),
                                            order
                                            )
    det_cos_expansion = td.scalarprod_deriv(det_expansion, cos_tau_expansion, order)
    num_expansion = td.scalarprod_deriv(
        td.subtract_expansions(td.add_expansions(a2_expansion, b2_expansion), x2_expansion),
        td.subtract_expansions(td.add_expansions(b2_expansion, c2_expansion), y2_expansion),
        order
    )
    invb2_expansion = td.scale_expansion(td.scalarinv_deriv(b2_expansion, order), 1/2)
    r2_term = td.subtract_expansions(td.add_expansions(x2_expansion, y2_expansion), b2_expansion)

    term = td.add_expansions(
        r2_term,
        td.scalarprod_deriv(
            td.subtract_expansions(num_expansion, det_cos_expansion),
            invb2_expansion,
            order
        )
    )
    if not return_square:
        term = td.scalarfunc_deriv(sqrt_deriv, term, order)

    # x2+y2-b2
    #         + (
    #                 (a2+b2-x2)*(b2+c2-y2)
    #                 -np.sqrt((xm - x2)*(xp - x2)*(ym - y2)*(yp - y2))*ct
    #         )/(2*b2)

    if return_components:
        return term, (
            a2_expansion,
            b2_expansion,
            c2_expansion,
            x2_expansion,
            y2_expansion,
            cos_tau_expansion,
            abplus_expansion,
            abminus_expansion,
            bcplus_expansion,
            bcminus_expansion,
            det_expansion
        )
    else:
        return term
def dihedral_from_abcXYz(a, b, c, X, Y, r, use_cos=False):
    ca = np.cos(X)
    cb = np.cos(Y)
    sa = np.sin(X)
    sb = np.sin(Y)
    ct = ((a**2 + b**2 + c**2) - r**2 - 2*a*b*ca - 2*b*c*cb + 2*a*c*ca*cb) / (2*a*c*sa*sb)
    if use_cos:
        return ct
    else:
        return np.arccos(ct)
def dihedral_from_abcXYz_deriv(
        a_expansion, b_expansion, c_expansion,
        X_expansion, Y_expansion, r_expansion,
        order,
        return_components=False,
        return_cos=False,
        cos_X_expansion=None,
        cos_Y_expansion=None,
        sin_X_expansion=None,
        sin_Y_expansion=None,
        a2_expansion=None,
        b2_expansion=None,
        c2_expansion=None,
        r2_expansion=None,
        ab_cos_X_expansion=None,
        ab_expansion=None,
        bc_cos_Y_expansion=None,
        bc_expansion=None,
        ac_expansion=None,
        cos_X_cos_Y_expansion=None,
        sin_X_sin_Y_expansion=None
):
    if ab_cos_X_expansion is None:
        if ab_expansion is None:
            ab_expansion = td.scalarprod_deriv(a_expansion, b_expansion, order)
        if cos_X_expansion is None:
            cos_X_expansion = td.scalarfunc_deriv(cos_deriv, X_expansion, order)
        ab_cos_X_expansion = td.scalarprod_deriv(
            ab_expansion,
            cos_X_expansion,
            order
        )

    if bc_cos_Y_expansion is None:
        if bc_expansion is None:
            bc_expansion = td.scalarprod_deriv(b_expansion, c_expansion, order)
        if cos_Y_expansion is None:
            cos_Y_expansion = td.scalarfunc_deriv(cos_deriv, Y_expansion, order)
        bc_cos_Y_expansion = td.scalarprod_deriv(
            bc_expansion,
            cos_Y_expansion,
            order
        )

    if cos_X_cos_Y_expansion is None:
        if cos_X_expansion is None:
            cos_X_expansion = td.scalarfunc_deriv(cos_deriv, X_expansion, order)
        if cos_Y_expansion is None:
            cos_Y_expansion = td.scalarfunc_deriv(cos_deriv, Y_expansion, order)
        cos_X_cos_Y_expansion = td.scalarprod_deriv(
            cos_X_expansion,
            cos_Y_expansion,
            order
        )

    if sin_X_sin_Y_expansion is None:
        if sin_X_expansion is None:
            sin_X_expansion = td.scalarfunc_deriv(sin_deriv, X_expansion, order)
        if sin_Y_expansion is None:
            sin_Y_expansion = td.scalarfunc_deriv(sin_deriv, Y_expansion, order)
        sin_X_sin_Y_expansion = td.scalarprod_deriv(
            sin_X_expansion,
            sin_Y_expansion,
            order
        )

    if a2_expansion is None:
        a2_expansion = td.scalarfunc_deriv(square_deriv, a_expansion, order)
    if b2_expansion is None:
        b2_expansion = td.scalarfunc_deriv(square_deriv, b_expansion, order)
    if c2_expansion is None:
        c2_expansion = td.scalarfunc_deriv(square_deriv, c_expansion, order)
    if r2_expansion is None:
        r2_expansion = td.scalarfunc_deriv(square_deriv, r_expansion, order)

    if ac_expansion is None:
        ac_expansion = td.scalarprod_deriv(a_expansion, c_expansion, order)

    ac_cos_cos_expansion = td.scalarprod_deriv(ac_expansion, cos_X_cos_Y_expansion, order)
    ac_sin_sin_expansion = td.scalarprod_deriv(ac_expansion, sin_X_sin_Y_expansion, order)

    # ((a**2 + b**2 + c**2) - r**2 - 2*a*b*ca - 2*b*c*cb + 2*a*c*ca*cb)
    rd_expansion = td.subtract_expansions(
        td.add_expansions(a2_expansion, b2_expansion, c2_expansion),
        td.add_expansions(r2_expansion,
                          td.scale_expansion(
                              td.subtract_expansions(
                                  td.add_expansions(ab_cos_X_expansion, bc_cos_Y_expansion),
                                  ac_cos_cos_expansion
                              ),
                              2
                          )
                          )
    )
    ac_denom_expansion = td.scale_expansion(td.scalarinv_deriv(ac_sin_sin_expansion, order), 1 / 2 )
    term = td.scalarprod_deriv(
        rd_expansion,
        ac_denom_expansion
    )
    if not return_cos:
        term = td.scalarfunc_deriv(arccos_deriv, term, order)

    if return_components:
        return term, (
            cos_X_expansion,
            cos_Y_expansion,
            sin_X_expansion,
            sin_Y_expansion,
            a2_expansion,
            b2_expansion,
            c2_expansion,
            r2_expansion,
            ab_cos_X_expansion,
            ab_expansion,
            bc_cos_Y_expansion,
            bc_expansion,
            ac_expansion,
            cos_X_cos_Y_expansion,
            sin_X_sin_Y_expansion
        )
    else:
        return term

def dihedral_from_abcxYz(a, b, c, x, Y, r, use_cos=False):
    a2 = a**2
    b2 = b**2
    x2 = x**2
    ca = (a2+b2-x2)/(2*a*b)
    cb = np.cos(Y)
    sa = np.sqrt(1-ca**2)
    sb = np.sin(Y)
    r2 = r**2
    ct = ((x2+c**2) - r2 - 2*b*c*cb + 2*a*c*ca*cb) / (2*a*c*sa*sb)
    if use_cos:
        return ct
    else:
        return np.arccos(ct)
def dihedral_from_abcxYz_deriv(a_expansion, b_expansion, c_expansion, x_expansion,
                               Y_expansion, r_expansion, order,
                               return_components=False,
                               return_cos=False,
                               cos_X_expansion=None,
                               cos_Y_expansion=None,
                               sin_X_expansion=None,
                               sin_Y_expansion=None,
                               a2_expansion=None,
                               b2_expansion=None,
                               c2_expansion=None,
                               x2_expansion=None,
                               r2_expansion=None,
                               ab_expansion=None,
                               bc_cos_Y_expansion=None,
                               bc_expansion=None,
                               ac_expansion=None,
                               cos_X_cos_Y_expansion=None,
                               sin_X_sin_Y_expansion=None
                               ):
    if a2_expansion is None:
        a2_expansion = td.scalarfunc_deriv(square_deriv, a_expansion, order)
    if b2_expansion is None:
        b2_expansion = td.scalarfunc_deriv(square_deriv, b_expansion, order)
    if c2_expansion is None:
        c2_expansion = td.scalarfunc_deriv(square_deriv, c_expansion, order)
    if r2_expansion is None:
        r2_expansion = td.scalarfunc_deriv(square_deriv, r_expansion, order)
    if x2_expansion is None:
        x2_expansion = td.scalarfunc_deriv(square_deriv, x_expansion, order)
    if cos_X_cos_Y_expansion is None:
        if cos_X_expansion is None:
            if ab_expansion is None:
                ab_expansion = td.scalarprod_deriv(a_expansion, b_expansion, order)
            cos_X_expansion = _dist_cos_expansion(a2_expansion, b2_expansion, x2_expansion, ab_expansion, order)
        if cos_Y_expansion is None:
            cos_Y_expansion = td.scalarfunc_deriv(cos_deriv, Y_expansion, order)
        cos_X_cos_Y_expansion = td.scalarprod_deriv(cos_X_expansion, cos_Y_expansion, order)
    if sin_X_sin_Y_expansion is None:
        if sin_X_expansion is None:
            ca2 = td.scalarfunc_deriv(square_deriv, cos_X_expansion, order)
            sin_X_expansion = td.scalarfunc_deriv(
                sqrt_deriv,
                td.shift_expansion(td.scale_expansion(ca2, -1), 1),
                order
            )
        if sin_Y_expansion is None:
            sin_Y_expansion = td.scalarfunc_deriv(sin_deriv, Y_expansion, order)
        sin_X_sin_Y_expansion = td.scalarprod_deriv(sin_X_expansion, sin_Y_expansion, order)

    if bc_cos_Y_expansion is None:
        if bc_expansion is None:
            bc_expansion = td.scalarprod_deriv(b_expansion, c_expansion, order)
        if cos_Y_expansion is None:
            cos_Y_expansion = td.scalarfunc_deriv(cos_deriv, Y_expansion, order)
        bc_cos_Y_expansion = td.scalarprod_deriv(bc_expansion, cos_Y_expansion, order)
    # x2+c**2 - 2*(b*c*cb + a*c*(ct*sa*sb-ca*cb))
    if ac_expansion is None:
        ac_expansion = td.scalarprod_deriv(a_expansion, c_expansion, order)

    ac_cos_cos_expansion = td.scalarprod_deriv(ac_expansion, cos_X_cos_Y_expansion, order)
    ac_sin_sin_expansion = td.scalarprod_deriv(ac_expansion, sin_X_sin_Y_expansion, order)

    # ct = ((x2+c**2) - r2 - 2*b*c*cb + 2*a*c*ca*cb) / (2*a*c*sa*sb)
    numerator = td.subtract_expansions(
        td.add_expansions(x2_expansion, c2_expansion),
        td.add_expansions(
            r2_expansion,
            td.scale_expansion(
                td.subtract_expansions(bc_cos_Y_expansion, ac_cos_cos_expansion),
                2
            )
        )
    )
    denom = td.scale_expansion(
        td.scalarinv_deriv(ac_sin_sin_expansion),
        2
    )

    term = td.scalarprod_deriv(numerator, denom, order)
    if not return_cos:
        term = td.scalarfunc_deriv(arccos_deriv, term, order)

    if return_components:
        return term, (
            cos_X_expansion,
            cos_Y_expansion,
            sin_X_expansion,
            sin_Y_expansion,
            a2_expansion,
            b2_expansion,
            c2_expansion,
            x2_expansion,
            r2_expansion,
            ab_expansion,
            bc_cos_Y_expansion,
            bc_expansion,
            ac_expansion,
            cos_X_cos_Y_expansion,
            sin_X_sin_Y_expansion
        )
    else:
        return term

def dihedral_from_abcxyz(a, b, c, x, y, r, use_cos=False):
    xp = (a + b) ** 2
    xm = (a - b) ** 2
    yp = (b + c) ** 2
    ym = (b - c) ** 2
    x2 = x ** 2
    y2 = y ** 2
    a2 = a ** 2
    b2 = b ** 2
    c2 = c ** 2
    r2 = r ** 2
    ct = (
            (a2 + b2 - x2) * (b2 + c2 - y2)
            - ((r2 - (x2 + y2 - b2)) * (2 * b2))
    ) / np.sqrt((xm - x2) * (xp - x2) * (ym - y2) * (yp - y2))
    if use_cos:
        return ct
    else:
        return np.arccos(ct)
def dihedral_from_abcxyz_deriv(a_expansion, b_expansion, c_expansion, x_expansion,
                               y_expansion, r_expansion, order,
                               return_components=False,
                               return_cos=False,
                               a2_expansion=None,
                               b2_expansion=None,
                               c2_expansion=None,
                               x2_expansion=None,
                               y2_expansion=None,
                               r2_expansion=None,
                               abplus_expansion=None,
                               abminus_expansion=None,
                               bcplus_expansion=None,
                               bcminus_expansion=None,
                               det_expansion=None,
                               ):
    # potentially more stable than just computing the sin and cos in the usual way...
    if x2_expansion is None:
        x2_expansion = td.scalarpow_deriv(x_expansion, 2, order)
    if y2_expansion is None:
        y2_expansion = td.scalarpow_deriv(y_expansion, 2, order)
    if a2_expansion is None:
        a2_expansion = td.scalarpow_deriv(a_expansion, 2, order)
    if b2_expansion is None:
        b2_expansion = td.scalarpow_deriv(b_expansion, 2, order)
    if c2_expansion is None:
        c2_expansion = td.scalarpow_deriv(c_expansion, 2, order)
    if r2_expansion is None:
        r2_expansion = td.scalarpow_deriv(r_expansion, 2, order)

    if det_expansion is None:
        if abplus_expansion is None:
            abplus_expansion = td.scalarpow_deriv(td.add_expansions(a_expansion, b_expansion), 2, order)
        if abminus_expansion is None:
            abminus_expansion = td.scalarpow_deriv(td.subtract_expansions(a_expansion, b_expansion), 2, order)
        if bcplus_expansion is None:
            bcplus_expansion = td.scalarpow_deriv(td.add_expansions(b_expansion, c_expansion), 2, order)
        if bcminus_expansion is None:
            bcminus_expansion = td.scalarpow_deriv(td.subtract_expansions(b_expansion, c_expansion), 2, order)
        # np.sqrt((xm - x2)*(xp - x2)*(ym - y2)*(yp - y2))
        abp = td.subtract_expansions(abplus_expansion, x2_expansion)
        abm = td.subtract_expansions(abminus_expansion, x2_expansion)
        bcp = td.subtract_expansions(bcplus_expansion, y2_expansion)
        bcm = td.subtract_expansions(bcminus_expansion, y2_expansion)
        det_expansion = td.scalarfunc_deriv(sqrt_deriv,
                                            td.scalarprod_deriv(
                                                td.scalarprod_deriv(abm, abp, order),
                                                td.scalarprod_deriv(bcm, bcp, order),
                                                order
                                            ),
                                            order
                                            )

    #     ct = (
    #             (a2 + b2 - x2) * (b2 + c2 - y2)
    #             - ((r2 - (x2 + y2 - b2)) * (2 * b2))
    #     ) / np.sqrt((xm - x2) * (xp - x2) * (ym - y2) * (yp - y2))
    det_inv_expansion = td.scalarinv_deriv(det_expansion, order)
    num_expansion_1 = td.scalarprod_deriv(
        td.subtract_expansions(td.add_expansions(a2_expansion, b2_expansion), x2_expansion),
        td.subtract_expansions(td.add_expansions(b2_expansion, c2_expansion), y2_expansion),
        order

    )
    # ((r2 - (x2 + y2 - b2)) * (2 * b2))
    num_expansion_2 = td.scalarprod_deriv(
        td.subtract_expansions(
            td.add_expansions(r2_expansion, b2_expansion),
            td.add_expansions(x2_expansion, y2_expansion)
        ),
        td.scale_expansion(b2_expansion, 2),
        order
    )
    term = td.scalarprod_deriv(
        td.subtract_expansions(num_expansion_1, num_expansion_2),
        det_inv_expansion,
        order
    )

    if not return_cos:
        term = td.scalarfunc_deriv(arccos_deriv, term, order)

    if return_components:
        return term, (
            a2_expansion,
            b2_expansion,
            c2_expansion,
            x2_expansion,
            y2_expansion,
            r2_expansion,
            abplus_expansion,
            abminus_expansion,
            bcplus_expansion,
            bcminus_expansion,
            det_expansion
        )
    else:
        return term

def dihedral_from_XZC(X, Z, C, use_cos=False):
    """
    cos of dihedral with three angles defining a pyramid,
    X = theta_(i,j,k)
    Z = theta_(i,j,l)
    C = theta_(k,j,l)
    """
    cA, cB, cC = [np.cos(x) for x in [X, Z, C]]
    sA, sC = [np.sin(x) for x in [X, C]]
    cost = (cB - cA * cC) / (sA * sC)
    cost = cost * np.sign(np.sin(X) * np.sin(C))
    if use_cos:
        return cost
    else:
        return np.arccos(cost)
def dihedral_Z_from_XtC(X, t, C, use_cos=False):
    cA, cC = [np.cos(x) for x in [X, C]]
    sA, sC = [np.sin(x) for x in [X, C]]
    if use_cos:
        cost = t
    else:
        cost = np.cos(t)
    cost = cost * np.sign(np.sin(X) * np.sin(C))
    cB = cost * (sA * sC) + cA * cC
    return np.arccos(cB)

def dihedral_z_from_ayXCt(a, y, X, C, t, use_cos=False, return_square=False):
    if use_cos:
        cost = t
    else:
        cost = np.cos(t)

    z2 = a**2 + y**2 - 2*a*y*(cost*np.sin(X)*np.sin(C) + np.cos(X)*np.cos(C))
    if return_square:
        z = z2
    else:
        z = np.sqrt(z2)
    return z
def dihedral_z_from_bAXYCt(b, A, X, Y, C, t, use_cos=False, return_square=False):
    a = law_of_sines_dist(b, X+A, A)
    y = law_of_sines_dist(b, Y+C, Y)
    return dihedral_z_from_ayXCt(a, y, X, C, t, use_cos=use_cos, return_square=return_square)
def dihedral_from_ayXCz(a, y, X, C, z, use_cos=False):
    cost = ((a**2 + y**2 - z**2)/ (2*a*y) - np.cos(X)*np.cos(C)) / (np.sin(X)*np.sin(C))
    if use_cos:
        t = cost
    else:
        t = np.arccos(cost)
    return z
def dihedral_from_bAXYCz(b, A, X, Y, C, z, use_cos=False):
    a = law_of_sines_dist(b, X+A, A)
    y = law_of_sines_dist(b, Y+C, Y)
    return dihedral_from_ayXCz(a, y, X, C, z, use_cos=use_cos)

class DihedralSpecifierType(enum.Enum):
    SSSAAT = "sssaat"
    SSSSAT = "ssssat"
    SSSSST = "ssssst"
def dihedral_distance_converter(dihedral_type:str|DihedralSpecifierType):
    dihedral_type = DihedralSpecifierType(dihedral_type)
    if dihedral_type == DihedralSpecifierType.SSSSST:
        return (dihedral_z_from_abcxyt, dihedral_z_from_abcxyt_deriv)
    elif dihedral_type == DihedralSpecifierType.SSSSAT:
        return (dihedral_z_from_abcxYt, dihedral_z_from_abcxYt_deriv)
    else:
        return (dihedral_z_from_abcXYt, dihedral_z_from_abcXYt_deriv)
def dihedral_distance(spec, dihedral_type:str|DihedralSpecifierType,
                      order=None,
                      use_cos=False,
                      **deriv_kwargs
                      ) -> float|np.ndarray:
    converter, deriv_converter = dihedral_distance_converter(dihedral_type)
    if order is None:
        return converter(*spec, use_cos=use_cos)
    else:
        x,y,z,a,b,t = spec
        return deriv_converter(x,y,z,a,b,t, order, **deriv_kwargs)
def dihedral_from_distance_converter(dihedral_type:str|DihedralSpecifierType):
    dihedral_type = DihedralSpecifierType(dihedral_type)
    if dihedral_type == DihedralSpecifierType.SSSSST:
        return (dihedral_from_abcxyz, dihedral_from_abcxyz_deriv)
    elif dihedral_type == DihedralSpecifierType.SSSSAT:
        return (dihedral_from_abcxYz, dihedral_from_abcxYz_deriv)
    else:
        return (dihedral_from_abcXYz, dihedral_from_abcXYz_deriv)
def dihedral_from_distance(spec, dihedral_type:str|DihedralSpecifierType,
                           order=None,
                           use_cos=False,
                           **deriv_kwargs
                           ) -> float|np.ndarray:

    converter, deriv_converter = dihedral_from_distance_converter(dihedral_type)
    if order is None:
        return converter(*spec, use_cos=use_cos)
    else:
        x,y,z,a,b,r = spec
        return deriv_converter(x,y,z,a,b,r, order, **deriv_kwargs)

DihedralTetrahedronData = collections.namedtuple("DihedralTetrahedronData",
                                                 ["a", "b", "c", "x", "y", "z",
                                                  "X", "Y", "A", "B1", "B2", "C", "Z", "Z2",
                                                  "A3", "Y3", "C4", "X4",
                                                  "Ta", "Tb", "Tc", "Tx", "Ty", "Tz"
                                                  ])
_ddata_name_map = {
    "a":0, "b":1, "c":2, "x":3, "y":4, "z":5,
    "X":6, "Y":7, "A":8, "B1":9, "B2":10, "C":11, "Z":12, "Z2":13,
    "A3":14, "Y3":15, "C4":16, "X4":17,
    "Ta":18, "Tb":19, "Tc":20, "Tx":21, "Ty":22, "Tz":23
}
_dihedron_point_map = {
    'a': (0, 1),
    'b': (1, 2),
    'c': (2, 3),
    'x': (0, 2),
    'y': (1, 3),
    'z': (0, 3),
    'X': (0, 1, 2),
    'Y': (1, 2, 3),
    'A': (0, 2, 1),
    'B1': (1, 0, 2),
    'C': (2, 1, 3),
    'B2': (1, 3, 2),
    'Z': (0, 1, 3),
    'Z2': (0, 2, 3),
    'A3': (0, 3, 1),
    'Y3': (1, 0, 3),
    'C4': (2, 0, 3),
    'X4': (0, 3, 2),
    'Tb':(0, 1, 2, 3),
    'Tb_inv':(0, 2, 1, 3),
    'Ta':(2, 0, 1, 3),
    'Ta_inv':(2, 1, 0, 3),
    'Tc':(0, 2, 3, 1),
    'Tc_inv':(0, 3, 2, 1),
    'Tx':(1, 0, 2, 3),
    'Tx_inv':(1, 2, 0, 3),
    'Ty':(0, 1, 3, 2),
    'Ty_inv':(0, 3, 1, 2),
    'Tz':(1, 0, 3, 2),
    'Tz_inv':(1, 3, 0, 2)
}
def dihedron_property_specifiers(base_specifier=None):
    if base_specifier is None:
        return {
            k:dihedron_property_specifiers(k)
            for k in _ddata_name_map
        }
    else:
        if isinstance(base_specifier, str):
            if base_specifier.endswith("_inv"):
                spec = dihedron_property_specifiers(base_specifier.split("_")[0])
                spec['sign'] *= -1
                return spec
            else:
                return {
                    "name":base_specifier,
                    "index":_ddata_name_map[base_specifier],
                    "coord":_dihedron_point_map[base_specifier],
                    "sign":1
                }
        elif misc.is_int(base_specifier):
            for k,v in _ddata_name_map.items():
                if v == base_specifier:
                    return dihedron_property_specifiers(k)
            else:
                raise ValueError(f"can't interpret specifier {base_specifier}")
        else:
            for k,v in _dihedron_point_map.items():
                if v == base_specifier:
                    return dihedron_property_specifiers(k)
            else:
                raise ValueError(f"can't interpret specifier {base_specifier}")
def _check_dihedron_type(ddata, inds):
    return all(
        ddata[i if not isinstance(i, str) else _ddata_name_map[i]] is not None
        for i in inds
    )
def make_dihedron(points=None, *,
                  a=None, b=None, c=None, x=None, y=None, z=None,
                  X=None, Y=None, A=None, B1=None, B2=None, C=None,
                  Z=None, Z2=None, A3=None, Y3=None, C4=None, X4=None,
                  Ta=None, Tb=None, Tc=None, Tx=None, Ty=None, Tz=None
                  ):
    if points is not None:
        a, x, z, b, y, c = distance_matrix(points, return_triu=True)
    return DihedralTetrahedronData(
        a, b, c, x, y, z,
        X, Y, A, B1, B2, C,
        Z, Z2, A3, Y3, C4, X4,
        Ta, Tb, Tc, Tx, Ty, Tz
    )
def _symbolic_dihedron_field(val, field_name, inds, use_pos):
    if val is not None:
        return val
    elif use_pos is True:
        return _ddata_name_map[field_name]
    elif inds is True:
        return _dihedron_point_map[field_name]
    elif inds is not None:
        return tuple(inds[p] for p in _dihedron_point_map[field_name])
    elif use_pos is not None and use_pos is not False:
        return use_pos[_ddata_name_map[field_name]]
    else:
        return field_name
def make_symbolic_dihedron(
        indices=None,
        positions=False,
        a=None, b=None, c=None, x=None, y=None, z=None,
        X=None, Y=None, A=None, B1=None, B2=None, C=None,
        Z=None, Z2=None, A3=None, Y3=None, C4=None, X4=None,
        Ta=None, Tb=None, Tc=None, Tx=None, Ty=None, Tz=None
):
    return make_dihedron(
        a=_symbolic_dihedron_field(a, 'a', indices, positions),
        b=_symbolic_dihedron_field(b, 'b', indices, positions),
        c=_symbolic_dihedron_field(c, 'c', indices, positions),
        x=_symbolic_dihedron_field(x, 'x', indices, positions),
        y=_symbolic_dihedron_field(y, 'y', indices, positions),
        z=_symbolic_dihedron_field(z, 'z', indices, positions),
        X=_symbolic_dihedron_field(X, 'X', indices, positions),
        Y=_symbolic_dihedron_field(Y, 'Y', indices, positions),
        A=_symbolic_dihedron_field(A, 'A', indices, positions),
        B1=_symbolic_dihedron_field(B1, 'B1', indices, positions),
        B2=_symbolic_dihedron_field(B2, 'B2', indices, positions),
        C=_symbolic_dihedron_field(C, 'C', indices, positions),
        Z=_symbolic_dihedron_field(Z, 'Z', indices, positions),
        Z2=_symbolic_dihedron_field(Z2, 'Z2', indices, positions),
        A3=_symbolic_dihedron_field(A3, 'A3', indices, positions),
        Y3=_symbolic_dihedron_field(Y3, 'Y3', indices, positions),
        C4=_symbolic_dihedron_field(C4, 'C4', indices, positions),
        X4=_symbolic_dihedron_field(X4, 'X4', indices, positions),
        Ta=_symbolic_dihedron_field(Ta, 'Ta', indices, positions),
        Tb=_symbolic_dihedron_field(Tb, 'Tb', indices, positions),
        Tc=_symbolic_dihedron_field(Tc, 'Tc', indices, positions),
        Tx=_symbolic_dihedron_field(Tx, 'Tx', indices, positions),
        Ty=_symbolic_dihedron_field(Ty, 'Ty', indices, positions),
        Tz=_symbolic_dihedron_field(Tz, 'Tz', indices, positions)
    )
dihedron_triangle_fields = [
    ['a', 'b', 'x', 'A', 'B1', 'X'],
    ['y', 'b', 'c', 'Y', 'B2', 'C'],
    ['a', 'y', 'z', 'A3', 'Y3', 'Z'],
    ['x', 'z', 'c', 'X4', 'Z2', 'C4']
]
dihedron_angle_triples = {
    # the set (i,j,k), (k,j,l), and (i,j,l)
    # ordered so that if the angle without (i,j) is in the middle
    'a':(['X', 'C', 'Z'], ['B1', 'C4', 'Y3']),
    'b':(['X', 'Z', 'C'], ['A', 'Z2', 'Y']),
    'c':(['Y', 'A', 'Z2'], ['B2', 'A3', 'X4']),
    'x':(['A', 'Y', 'Z2'], ['B1', 'Y3', 'C4']),
    'y':(['Z', 'X', 'C'], ['A3', 'X4', 'B2']),
    'z':(['C4', 'B1', 'Y3'],['A3', 'B2', 'X4'])
}
dihedron_triangle_pair_dihedrals = {
    (0, 1): ("Tb", "z", "Z", "Z2"),
    (0, 2): ("Ta", "c", "C", "C4"),
    (0, 3): ("Tx", "y", "Y", "Y3"),
    (1, 2): ("Ty", "x", "X", "X4"),
    (1, 3): ("Tc", "a", "A", "A3"),
    (2, 3): ("Tz", "b", "B1", "B2"),
}
def dihedron_triangle_1(dd:DihedralTetrahedronData):
    return make_triangle(a=dd.a, b=dd.b, c=dd.x, A=dd.A, B=dd.B1, C=dd.X)
def dihedron_triangle_2(dd:DihedralTetrahedronData):
    return make_triangle(a=dd.y, b=dd.b, c=dd.c, A=dd.Y, B=dd.B2, C=dd.C)
def dihedron_triangle_3(dd:DihedralTetrahedronData):
    return make_triangle(a=dd.a, b=dd.y, c=dd.z, A=dd.A3, B=dd.Y3, C=dd.Z)
def dihedron_triangle_4(dd:DihedralTetrahedronData):
    return make_triangle(a=dd.x, b=dd.z, c=dd.c, A=dd.X4, B=dd.Z2, C=dd.C4)
def dihedron_triangle(dd:DihedralTetrahedronData, i):
    if i == 0:
        return dihedron_triangle_1(dd)
    elif i == 1:
        return dihedron_triangle_2(dd)
    elif i == 2:
        return dihedron_triangle_3(dd)
    else:
        return dihedron_triangle_4(dd)
def _dihedron_permutation_relabeling(perm):
    #TODO: cache the relabeling
    inv_map = {v:k for k,v in _dihedron_point_map.items()}
    inv_perm = np.argsort(perm)
    new_inds = []
    for c in _dihedron_point_map.values():
        c1 = c
        c = [inv_perm[k2] for k2 in c]
        if len(c) == 2:
            i,j = c
            if j < i:
                i,j = j,i
            c = (i,j)
        elif len(c) == 3:
            i,j,k = c
            if k < i:
                i,k = k,i
            c = (i,j,k)
        else:
            i,j,k,l = c
            if l < i:
                i,j,k,l = l,k,j,i
            c = (i,j,k,l)
        new_inds.append([inv_map[c1], c])
    return {
        inv_map[c]: _ddata_name_map[o.split("_inv")[0]]
        for o, c in new_inds
    }
def _dihedron_data_permute(dd, perm):
    updates = {
        #TODO: how to handle flipped dihedrals?
        k.split("_inv")[0]:dd[i] if not k.endswith("_inv") or dd[i] is None else (2*np.pi - dd[i])
        for k,i in _dihedron_permutation_relabeling(perm).items()
    }
    return make_dihedron(**updates)
def dihedron_modify(dd, updates):
    new_data = list(dd)
    for k, v in updates.items():
        if isinstance(k, str):
            k = _ddata_name_map[k]
        new_data[k] = v
    return DihedralTetrahedronData(*new_data)
def _dihedron_property_z(dd:DihedralTetrahedronData):
    if dd.z is not None:
        return dd.z, dd
    else:
        td_3 = dihedron_triangle_3(dd)
        td_4 = dihedron_triangle_4(dd)
        if _check_bond_valid_triangle(td_3):
            z, td_new = triangle_property(td_3, 'c')
            updates = dict(zip(['a', 'y', 'z', 'A3', 'Y3', 'Z'], td_new))
            return z, dihedron_modify(dd, updates)
        elif _check_bond_valid_triangle(td_4):
            z, td_new = triangle_property(td_4, 'b')
            updates = dict(zip(['x', 'z', 'c', 'X4', 'Z2', 'C4'], td_new))
            return z, dihedron_modify(dd, updates)
        elif _check_dihedron_type(dd, ['a', 'y', 'X', 'C', 'Tb']):
            z = dihedral_z_from_ayXCt(dd.a, dd.y, dd.X, dd.C, dd.Tb)
            return z, dihedron_modify(dd, {'z':z})
        elif _check_dihedron_type(dd, ['b', 'x', 'Y', 'A', 'Tb']):
            z = dihedral_z_from_ayXCt(dd.b, dd.x, dd.Y, dd.A, dd.Tb)
            return z, dihedron_modify(dd, {'z':z})
        elif _check_dihedron_type(dd, ['a', 'b', 'c', 'x', 'y', 'Tb']):
            z = dihedral_z_from_abcxyt(dd.a, dd.b, dd.c, dd.x, dd.y, dd.Tb)
            return z, dihedron_modify(dd, {'z':z})
        elif _check_dihedron_type(dd, ['a', 'b', 'c', 'x', 'Y', 'Tb']):
            z = dihedral_z_from_abcxYt(dd.a, dd.b, dd.c, dd.x, dd.Y, dd.Tb)
            return z, dihedron_modify(dd, {'z':z})
        elif _check_dihedron_type(dd, ['a', 'b', 'c', 'X', 'y', 'Tb']):
            z = dihedral_z_from_abcxYt(dd.a, dd.b, dd.c, dd.y, dd.X, dd.Tb)
            return z, dihedron_modify(dd, {'z':z})
        elif _check_dihedron_type(dd, ['a', 'b', 'c', 'X', 'Y', 'Tb']):
            z = dihedral_z_from_abcXYt(dd.a, dd.b, dd.c, dd.X, dd.Y, dd.Tb)
            return z, dihedron_modify(dd, {'z':z})
        elif _check_dihedron_type(dd, ['x', 'b', 'y', 'A', 'C', 'Tb']):
            z = dihedral_z_from_abcXYt(dd.x, dd.b, dd.y, dd.A, dd.C, dd.Tb)
            return z, dihedron_modify(dd, {'z':z})
        else:
            raise ValueError(f"can't get z from dihedral data {dd}")
def _dihedron_property_a(dd:DihedralTetrahedronData):
    if dd.a is not None:
        return dd.a, dd
    else:
        p = [0, 2, 3, 1]
        inv = np.argsort(p)
        dd = _dihedron_data_permute(dd, p)
        a, dd = _dihedron_property_z(dd)
        return a, _dihedron_data_permute(dd, inv)
def _dihedron_property_x(dd:DihedralTetrahedronData):
    if dd.x is not None:
        return dd.x, dd
    else:
        p = [0, 1, 3, 2]
        inv = np.argsort(p)
        dd = _dihedron_data_permute(dd, p)
        a, dd = _dihedron_property_z(dd)
        return a, _dihedron_data_permute(dd, inv)
def _dihedron_property_b(dd:DihedralTetrahedronData):
    if dd.b is not None:
        return dd.b, dd
    else:
        p = [1, 0, 3, 2]
        inv = np.argsort(p)
        dd = _dihedron_data_permute(dd, p)
        a, dd = _dihedron_property_z(dd)
        return a, _dihedron_data_permute(dd, inv)
def _dihedron_property_c(dd:DihedralTetrahedronData):
    if dd.c is not None:
        return dd.c, dd
    else:
        p = [2, 0, 1, 3]
        inv = np.argsort(p)
        dd = _dihedron_data_permute(dd, p)
        a, dd = _dihedron_property_z(dd)
        return a, _dihedron_data_permute(dd, inv)
def _dihedron_property_y(dd:DihedralTetrahedronData):
    if dd.y is not None:
        return dd.y, dd
    else:
        p = [1, 0, 2, 3]
        inv = np.argsort(p)
        dd = _dihedron_data_permute(dd, p)
        a, dd = _dihedron_property_z(dd)
        return a, _dihedron_data_permute(dd, inv)
def _dihedron_complete_dihedral_angle_data(Tb, X, C,
                                           td_1, names_1, field_1,
                                           td_2, names_2, field_2
                                           ):
    a2 = _check_angle_valid_triangle(td_2)
    a1 = _check_angle_valid_triangle(td_1)
    needs_C = C is None
    needs_X = X is None

    has_C = not needs_C or a2
    has_X = not needs_X or a1

    if has_C and has_X:
        updates = {}
        if needs_X:
            X, td_1 = triangle_property(td_1, field_1)
            updates.update(dict(zip(names_1, td_1)))
        if needs_C:
            C, td_2 = triangle_property(td_2, field_2)
            updates.update(dict(zip(names_2, td_2)))
        Z = dihedral_Z_from_XtC(X, Tb, C)
        return Z, updates
    else:
        return None, None
def _dihedron_complete_dihedral_angle_data_imp(dd, T, f, x, A, y, B):
    if T is not None:
        td_2 = dihedron_triangle(dd, x)
        td_4 = dihedron_triangle(dd, y)
        A3_test, updates = _dihedron_complete_dihedral_angle_data(
            T, _tri_prop(td_2, A), _tri_prop(td_4, B),
            td_2, dihedron_triangle_fields[x], A,
            td_4, dihedron_triangle_fields[y], B
        )
        if A3_test is not None:
            updates[f] = A3_test
            dd = dihedron_modify(dd, updates)
    return dd
def _dihedron_complete_dihedral_angle_Ta_C(dd:DihedralTetrahedronData):
    return _dihedron_complete_dihedral_angle_data_imp(
        dd, dd.Ta, 'C', 0, 'C', 2, 'C'
    )
def _dihedron_complete_dihedral_angle_Ta_C4(dd:DihedralTetrahedronData):
    return _dihedron_complete_dihedral_angle_data_imp(
        dd, dd.Ta, 'C4', 0, 'B', 2, 'B'
    )
def _dihedron_complete_dihedral_angle_Tb_Z(dd:DihedralTetrahedronData):
    return _dihedron_complete_dihedral_angle_data_imp(
        dd, dd.Tb, 'Z', 0, 'C', 1, 'C'
    )
def _dihedron_complete_dihedral_angle_Tb_Z2(dd:DihedralTetrahedronData):
    return _dihedron_complete_dihedral_angle_data_imp(
        dd, dd.Tb, 'Z2', 0, 'A', 1, 'A'
    )
def _dihedron_complete_dihedral_angle_Tc_A(dd:DihedralTetrahedronData):
    return _dihedron_complete_dihedral_angle_data_imp(
        dd, dd.Tc, 'A', 1, 'C', 3, 'B'
    )
def _dihedron_complete_dihedral_angle_Tc_A3(dd:DihedralTetrahedronData):
    return _dihedron_complete_dihedral_angle_data_imp(
        dd, dd.Tc, 'A3', 1, 'B', 3, 'A'
    )
def _dihedron_complete_dihedral_angle_Tx_Y(dd:DihedralTetrahedronData):
    return _dihedron_complete_dihedral_angle_data_imp(
        dd, dd.Tx, 'Y', 0, 'A', 3, 'B'
    )
def _dihedron_complete_dihedral_angle_Tx_Y3(dd:DihedralTetrahedronData):
    return _dihedron_complete_dihedral_angle_data_imp(
        dd, dd.Tx, 'Y3', 0, 'B', 3, 'C'
    )
def _dihedron_complete_dihedral_angle_Ty_X(dd:DihedralTetrahedronData):
    return _dihedron_complete_dihedral_angle_data_imp(
        dd, dd.Ty, 'X', 2, 'C', 1, 'C'
    )
def _dihedron_complete_dihedral_angle_Ty_X4(dd:DihedralTetrahedronData):
    return _dihedron_complete_dihedral_angle_data_imp(
        dd, dd.Ty, 'X4', 2, 'A', 1, 'B'
    )
def _dihedron_complete_dihedral_angle_Tz_B1(dd:DihedralTetrahedronData):
    return _dihedron_complete_dihedral_angle_data_imp(
        dd, dd.Tz, 'B1', 3, 'C', 2, 'B'
    )
def _dihedron_complete_dihedral_angle_Tz_B2(dd:DihedralTetrahedronData):
    return _dihedron_complete_dihedral_angle_data_imp(
        dd, dd.Tz, 'B2', 2, 'A', 3, 'A'
    )
def _dihedron_property_Z(dd:DihedralTetrahedronData):
    if dd.Z is not None:
        return dd.Z, dd
    else:
        td_1 = dihedron_triangle_1(dd)
        td_2 = dihedron_triangle_2(dd)
        td_3 = dihedron_triangle_3(dd)
        td_4 = dihedron_triangle_4(dd)
        if _check_bond_valid_triangle(td_3):
            Z, td_new = triangle_property(td_3, 'C')
            updates = dict(zip(['a', 'y', 'z', 'A3', 'Y3', 'Z'], td_new))
            return Z, dihedron_modify(dd, updates)
        elif _check_dihedron_type(dd, ['X', 'Tb', 'C']):
            Z = dihedral_Z_from_XtC(dd.X, dd.Tb, dd.C)
            return Z, dihedron_modify(dd, {'Z': Z})
        # check if we can complete triangle 3 using extra dihedral relations
        else:
            if dd.Tb is not None:
                Z_test, updates = _dihedron_complete_dihedral_angle_data(
                    dd.Tb, dd.X, dd.C,
                    td_1, ['a', 'b', 'x', 'A', 'B1', 'X'], 'C',
                    td_2, ['y', 'b', 'c', 'Y', 'B2', 'C'], 'C'
                )
                if Z_test is not None:
                    updates['Z'] = Z_test
                    return Z_test, dihedron_modify(dd, updates)
            # dihedron_triangle_fields = [
            #     ['a', 'b', 'x', 'A', 'B1', 'X'],
            #     ['y', 'b', 'c', 'Y', 'B2', 'C'],
            #     ['a', 'y', 'z', 'A3', 'Y3', 'Z'],
            #     ['x', 'z', 'c', 'X4', 'Z2', 'C4']
            # ]
            if dd.Tc is not None and dd.A3 is None:
                A3_test, updates = _dihedron_complete_dihedral_angle_data(
                    dd.Tc, dd.B2, dd.X4,
                    td_2, dihedron_triangle_fields[1], 'B',
                    td_4, dihedron_triangle_fields[3], 'A'
                )
                if A3_test is not None:
                    updates['A3'] = A3_test
                    dd = dihedron_modify(dd, updates)
            if dd.Tx is not None and dd.Y3 is None:
                Y3_test, updates = _dihedron_complete_dihedral_angle_data(
                    dd.Tx, dd.B1, dd.C4,
                    td_1, dihedron_triangle_fields[0], 'B',
                    td_4, dihedron_triangle_fields[3], 'C'
                )
                if Y3_test is not None:
                    updates['Y3'] = Y3_test
                    dd = dihedron_modify(dd, updates)

            if dd.y is None:
                td_2 = dihedron_triangle_2(dd)
                if _check_bond_valid_triangle(td_2):
                    _, td_2 = triangle_property(td_2, 'a')
                    dd = dihedron_modify(dd, dict(zip(dihedron_triangle_fields[1], td_2)))

            if dd.a is None:
                td_1 = dihedron_triangle_1(dd)
                if _check_bond_valid_triangle(td_1):
                    _, td_1 = triangle_property(td_1, 'a')
                    dd = dihedron_modify(dd, dict(zip(dihedron_triangle_fields[0], td_1)))

            if dd.z is None:
                td_4 = dihedron_triangle_4(dd)
                if _check_bond_valid_triangle(td_4):
                    _, td_4 = triangle_property(td_4, 'b')
                    dd = dihedron_modify(dd, dict(zip(dihedron_triangle_fields[3], td_4)))

            # check again after completing triangles
            td_3 = dihedron_triangle_3(dd)
            if _check_bond_valid_triangle(td_3):
                Z, td_new = triangle_property(td_3, 'C')
                updates = dict(zip(dihedron_triangle_fields[2], td_new))
                return Z, dihedron_modify(dd, updates)
            raise ValueError(f"can't get Z from dihedral data {dd}")
def _dihedron_property_A(dd:DihedralTetrahedronData):
    if dd.A is not None:
        return dd.A, dd
    else:
        p = [0, 2, 3, 1]
        inv = np.argsort(p)
        dd = _dihedron_data_permute(dd, p)
        Z, dd = _dihedron_property_Z(dd)
        return Z, _dihedron_data_permute(dd, inv)
def _dihedron_property_X(dd:DihedralTetrahedronData):
    if dd.X is not None:
        return dd.X, dd
    else:
        p = [0, 1, 3, 2]
        inv = np.argsort(p)
        dd = _dihedron_data_permute(dd, p)
        X, dd = _dihedron_property_Z(dd)
        return X, _dihedron_data_permute(dd, inv)
def _dihedron_property_B1(dd:DihedralTetrahedronData):
    if dd.B1 is not None:
        return dd.B1, dd
    else:
        p = [1, 0, 3, 2]
        inv = np.argsort(p)
        dd = _dihedron_data_permute(dd, p)
        a, dd = _dihedron_property_Z(dd)
        return a, _dihedron_data_permute(dd, inv)
def _dihedron_property_C(dd:DihedralTetrahedronData):
    if dd.C is not None:
        return dd.C, dd
    else:
        p = [2, 1, 0, 3]
        inv = np.argsort(p)
        dd = _dihedron_data_permute(dd, p)
        a, dd = _dihedron_property_Z(dd)
        return a, _dihedron_data_permute(dd, inv)
def _dihedron_property_Y(dd:DihedralTetrahedronData):
    if dd.Y is not None:
        return dd.Y, dd
    else:
        p = [1, 0, 2, 3]
        inv = np.argsort(p)
        dd = _dihedron_data_permute(dd, p)
        a, dd = _dihedron_property_Z(dd)
        return a, _dihedron_data_permute(dd, inv)
def _dihedron_property_B2(dd:DihedralTetrahedronData):
    if dd.B2 is not None:
        return dd.B2, dd
    else:
        p = [1, 3, 0, 2]
        inv = np.argsort(p)
        dd = _dihedron_data_permute(dd, p)
        a, dd = _dihedron_property_Z(dd)
        return a, _dihedron_data_permute(dd, inv)
def _dihedron_property_Z2(dd:DihedralTetrahedronData):
    if dd.Z2 is not None:
        return dd.Z2, dd
    else:
        p = [0, 2, 1, 3]
        inv = np.argsort(p)
        dd = _dihedron_data_permute(dd, p)
        a, dd = _dihedron_property_Z(dd)
        return a, _dihedron_data_permute(dd, inv)
def _dihedron_property_A3(dd:DihedralTetrahedronData):
    if dd.A3 is not None:
        return dd.A3, dd
    else:
        p = [0, 3, 2, 1]
        inv = np.argsort(p)
        dd = _dihedron_data_permute(dd, p)
        a, dd = _dihedron_property_Z(dd)
        return a, _dihedron_data_permute(dd, inv)
def _dihedron_property_Y3(dd:DihedralTetrahedronData):
    if dd.Y3 is not None:
        return dd.Y3, dd
    else:
        p = [1, 0, 2, 3]
        inv = np.argsort(p)
        dd = _dihedron_data_permute(dd, p)
        a, dd = _dihedron_property_Z(dd)
        return a, _dihedron_data_permute(dd, inv)
def _dihedron_property_C4(dd:DihedralTetrahedronData):
    if dd.C4 is not None:
        return dd.C4, dd
    else:
        p = [2, 0, 1, 3]
        inv = np.argsort(p)
        dd = _dihedron_data_permute(dd, p)
        a, dd = _dihedron_property_Z(dd)
        return a, _dihedron_data_permute(dd, inv)
def _dihedron_property_X4(dd:DihedralTetrahedronData):
    if dd.X4 is not None:
        return dd.X4, dd
    else:
        p = [0, 3, 1, 2]
        inv = np.argsort(p)
        dd = _dihedron_data_permute(dd, p)
        a, dd = _dihedron_property_Z(dd)
        return a, _dihedron_data_permute(dd, inv)
def _dihedron_complete_dihedral_from_angle_data(Z, X, C,
                                                 td_1, names_1, field_1,
                                                 td_2, names_2, field_2
                                                 ):
    a2 = _check_angle_valid_triangle(td_2)
    a1 = _check_angle_valid_triangle(td_1)
    needs_C = C is None
    needs_X = X is None

    has_C = not needs_C or a2
    has_X = not needs_X or a1

    if has_C and has_X:
        updates = {}
        if needs_X:
            X, td_1 = triangle_property(td_1, field_1)
            updates.update(dict(zip(names_1, td_1)))
        if needs_C:
            C, td_2 = triangle_property(td_2, field_2)
            updates.update(dict(zip(names_2, td_2)))
        Tb = dihedral_from_XZC(X, Z, C)
        return Tb, updates
    else:
        return None, None
def _get_dihedron_triangle_completions(tri,
                                       complements,
                                       fields,
                                       comps,
                                       properties
                                       ):
    updates = {}
    can_complete = set()
    for t,c,p in zip(complements, comps, properties):
        if _check_bond_valid_triangle(t) or _triangle_has_prop(t, p):
            can_complete.add(c)
    completions_list = _get_triangle_completions(tri)
    if completions_list is not None:
        for completions in completions_list:
            completions = set(completions)
            if len(completions - can_complete) == 0:  # TODO: use faster short circuiting
                for t,c,f,p in zip(complements, comps, fields, properties):
                    if c in completions:
                        v, t = triangle_property(t, p)
                        updates.update(dict(zip(f, t)))
                break
    return updates

def _complete_dihedron_triangle_1(dd):
    updates = _get_dihedron_triangle_completions(dihedron_triangle_1(dd),
                                       [dihedron_triangle_3(dd), dihedron_triangle_2(dd), dihedron_triangle_4(dd)],
                                       [dihedron_triangle_fields[2], dihedron_triangle_fields[1], dihedron_triangle_fields[3]],
                                       ['a', 'b', 'c'],
                                       ['a', 'b', 'a']
                                       )
    if len(updates) > 0:
        return dihedron_modify(dd, updates)
    else:
        return dd
def _complete_dihedron_triangle_2(dd):
    updates = _get_dihedron_triangle_completions(dihedron_triangle_2(dd),
                                       [dihedron_triangle_3(dd), dihedron_triangle_1(dd), dihedron_triangle_4(dd)],
                                       [dihedron_triangle_fields[2], dihedron_triangle_fields[0], dihedron_triangle_fields[3]],
                                       ['a', 'b', 'c'],
                                       ['b', 'b', 'c']
                                       )
    if len(updates) > 0:
        return dihedron_modify(dd, updates)
    else:
        return dd
def _complete_dihedron_triangle_3(dd):
    updates = _get_dihedron_triangle_completions(dihedron_triangle_3(dd),
                                       [dihedron_triangle_1(dd), dihedron_triangle_2(dd), dihedron_triangle_4(dd)],
                                       [dihedron_triangle_fields[0], dihedron_triangle_fields[1], dihedron_triangle_fields[3]],
                                       ['a', 'b', 'c'],
                                       ['a', 'a', 'b']
                                       )
    if len(updates) > 0:
        return dihedron_modify(dd, updates)
    else:
        return dd
def _complete_dihedron_triangle_4(dd):
    updates = _get_dihedron_triangle_completions(dihedron_triangle_4(dd),
                                       [dihedron_triangle_1(dd), dihedron_triangle_3(dd), dihedron_triangle_2(dd)],
                                       [dihedron_triangle_fields[0], dihedron_triangle_fields[2], dihedron_triangle_fields[1]],
                                       ['a', 'b', 'c'],
                                       ['c', 'c', 'c']
                                       )
    if len(updates) > 0:
        return dihedron_modify(dd, updates)
    else:
        return dd

def _dihedron_property_Tb(dd):
    if dd.Tb is not None:
        return dd.Tb, dd
    else:
        if dd.Z is not None:
            td_1 = dihedron_triangle_1(dd)
            td_2 = dihedron_triangle_2(dd)
            Tb_test, updates = _dihedron_complete_dihedral_from_angle_data(
                dd.Z, dd.X, dd.C,
                td_1, ['a', 'b', 'x', 'A', 'B1', 'X'], 'C',
                td_2, ['y', 'b', 'c', 'Y', 'B2', 'C'], 'C'
            )
            if Tb_test is not None:
                updates['Tb'] = Tb_test
                return Tb_test, dihedron_modify(dd, updates)

        if _check_dihedron_type(dd, ['a', 'y', 'X', 'C', 'z']):
            Tb = dihedral_from_ayXCz(dd.a, dd.y, dd.X, dd.C, dd.z)
            return Tb, dihedron_modify(dd, {'Tb':Tb})
        elif _check_dihedron_type(dd, ['b', 'x', 'Y', 'A', 'z']):
            Tb = dihedral_from_ayXCz(dd.b, dd.x, dd.Y, dd.A, dd.z)
            return Tb, dihedron_modify(dd, {'Tb': Tb})
        elif _check_dihedron_type(dd, ['a', 'b', 'c', 'x', 'y', 'z']):
            Tb = dihedral_from_abcxyz(dd.a, dd.b, dd.c, dd.x, dd.y, dd.z)
            return Tb, dihedron_modify(dd, {'Tb': Tb})
        elif _check_dihedron_type(dd, ['a', 'b', 'c', 'x', 'Y', 'z']):
            Tb = dihedral_from_abcxYz(dd.a, dd.b, dd.c, dd.x, dd.Y, dd.z)
            return Tb, dihedron_modify(dd, {'Tb': Tb})
        elif _check_dihedron_type(dd, ['a', 'b', 'c', 'X', 'y', 'z']):
            Tb = dihedral_from_abcxYz(dd.a, dd.b, dd.c, dd.y, dd.X, dd.z)
            return Tb, dihedron_modify(dd, {'Tb': Tb})
        elif _check_dihedron_type(dd, ['a', 'b', 'c', 'X', 'Y', 'z']):
            Tb = dihedral_from_abcXYz(dd.a, dd.b, dd.c, dd.X, dd.Y, dd.z)
            return Tb, dihedron_modify(dd, {'Tb': Tb})
        elif _check_dihedron_type(dd, ['x', 'b', 'y', 'A', 'C', 'z']):
            Tb = dihedral_from_abcXYz(dd.x, dd.b, dd.y, dd.A, dd.C, dd.z)
            return Tb, dihedron_modify(dd, {'Tb': Tb})
        else:
            # populate anything that can generate the necessary components
            #TODO: add short circuiting logic to make sure we add the minimal amount
            dd = _dihedron_complete_dihedral_angle_Ta_C(dd)
            dd = _dihedron_complete_dihedral_angle_Ta_C4(dd)
            dd = _dihedron_complete_dihedral_angle_Tc_A(dd)
            dd = _dihedron_complete_dihedral_angle_Tc_A3(dd)
            dd = _dihedron_complete_dihedral_angle_Tx_Y(dd)
            dd = _dihedron_complete_dihedral_angle_Tx_Y3(dd)
            dd = _dihedron_complete_dihedral_angle_Ty_X(dd)
            dd = _dihedron_complete_dihedral_angle_Ty_X4(dd)
            dd = _dihedron_complete_dihedral_angle_Tz_B1(dd)
            dd = _dihedron_complete_dihedral_angle_Tz_B2(dd)
            dd = _complete_dihedron_triangle_1(dd)
            dd = _complete_dihedron_triangle_2(dd)
            dd = _complete_dihedron_triangle_3(dd)
            dd = _complete_dihedron_triangle_4(dd)
            # dd = _complete_dihedron_triangle_3(dd)
            # dd = _complete_dihedron_triangle_4(dd)
            td_1 = dihedron_triangle_1(dd)
            if _check_angle_valid_triangle(td_1):
                _, td_1 = triangle_property(td_1, 'C')
                dd = dihedron_modify(dd, dict(zip(dihedron_triangle_fields[0], td_1)))
            else:
                dd = _complete_dihedron_triangle_1(dd)
            td_2 = dihedron_triangle_2(dd)
            if _check_angle_valid_triangle(td_2):
                _, td_2 = triangle_property(td_2, 'C')
                dd = dihedron_modify(dd, dict(zip(dihedron_triangle_fields[1], td_2)))
            else:
                dd = _complete_dihedron_triangle_2(dd)
            td_3 = dihedron_triangle_3(dd)
            if _check_angle_valid_triangle(td_3):
                _, td_3 = triangle_property(td_3, 'C')
                dd = dihedron_modify(dd, dict(zip(dihedron_triangle_fields[2], td_3)))
            else:
                dd = _complete_dihedron_triangle_3(dd)

            # dd = _complete_dihedron_triangle_1(dd)
            # dd = _complete_dihedron_triangle_2(dd)
            td_3 = dihedron_triangle_3(dd)
            if _check_angle_valid_triangle(td_3):
                _, td_3 = triangle_property(td_3, 'C')
                dd = dihedron_modify(dd, dict(zip(dihedron_triangle_fields[2], td_3)))

            if dd.Z is not None:
                td_1 = dihedron_triangle_1(dd)
                td_2 = dihedron_triangle_2(dd)
                Tb_test, updates = _dihedron_complete_dihedral_from_angle_data(
                    dd.Z, dd.X, dd.C,
                    td_1, dihedron_triangle_fields[0], 'C',
                    td_2, dihedron_triangle_fields[1], 'C'
                )
                if Tb_test is not None:
                    updates['Tb'] = Tb_test
                    return Tb_test, dihedron_modify(dd, updates)

            raise ValueError(f"can't get Tb from dihedral data {dd}")
def _dihedron_property_Ta(dd:DihedralTetrahedronData):
    if dd.Ta is not None:
        return dd.Ta, dd
    else:
        p = _dihedron_point_map['Ta']
        inv = np.argsort(p)
        dd = _dihedron_data_permute(dd, p)
        a, dd = _dihedron_property_Tb(dd)
        return a, _dihedron_data_permute(dd, inv)
def _dihedron_property_Tc(dd:DihedralTetrahedronData):
    if dd.Tc is not None:
        return dd.Tc, dd
    else:
        p = _dihedron_point_map['Tc']
        inv = np.argsort(p)
        dd = _dihedron_data_permute(dd, p)
        a, dd = _dihedron_property_Tb(dd)
        return a, _dihedron_data_permute(dd, inv)
def _dihedron_property_Tx(dd:DihedralTetrahedronData):
    if dd.Tx is not None:
        return dd.Tx, dd
    else:
        p = _dihedron_point_map['Tx']
        inv = np.argsort(p)
        dd = _dihedron_data_permute(dd, p)
        a, dd = _dihedron_property_Tb(dd)
        return a, _dihedron_data_permute(dd, inv)
def _dihedron_property_Ty(dd:DihedralTetrahedronData):
    if dd.Ty is not None:
        return dd.Ty, dd
    else:
        p = _dihedron_point_map['Ty']
        inv = np.argsort(p)
        dd = _dihedron_data_permute(dd, p)
        a, dd = _dihedron_property_Tb(dd)
        return a, _dihedron_data_permute(dd, inv)
def _dihedron_property_Tz(dd:DihedralTetrahedronData):
    if dd.Tz is not None:
        return dd.Tz, dd
    else:
        p = _dihedron_point_map['Tz']
        inv = np.argsort(p)
        dd = _dihedron_data_permute(dd, p)
        a, dd = _dihedron_property_Tb(dd)
        return a, _dihedron_data_permute(dd, inv)
def _dihed_prop(ddata:DihedralTetrahedronData, field):
    props = dihedron_property_specifiers(field)
    return ddata[props['index']]
def dihedron_property(ddata:DihedralTetrahedronData, field_name, allow_completion=True):
    if allow_completion:
        if field_name == "a":
            return _dihedron_property_a(ddata)
        elif field_name == "b":
            return _dihedron_property_b(ddata)
        elif field_name == "c":
            return _dihedron_property_c(ddata)
        elif field_name == "x":
            return _dihedron_property_x(ddata)
        elif field_name == "y":
            return _dihedron_property_y(ddata)
        elif field_name == "z":
            return _dihedron_property_z(ddata)
        elif field_name == "X":
            return _dihedron_property_X(ddata)
        elif field_name == "Y":
            return _dihedron_property_Y(ddata)
        elif field_name == "A":
            return _dihedron_property_A(ddata)
        elif field_name == "B1":
            return _dihedron_property_B1(ddata)
        elif field_name == "B2":
            return _dihedron_property_B2(ddata)
        elif field_name == "C":
            return _dihedron_property_C(ddata)
        elif field_name == "Z":
            return _dihedron_property_Z(ddata)
        elif field_name == "Z2":
            return _dihedron_property_Z2(ddata)
        elif field_name == "A3":
            return _dihedron_property_A3(ddata)
        elif field_name == "Y3":
            return _dihedron_property_Y3(ddata)
        elif field_name == "C4":
            return _dihedron_property_C4(ddata)
        elif field_name == "X4":
            return _dihedron_property_X4(ddata)
        elif field_name == "Ta":
            return _dihedron_property_Ta(ddata)
        elif field_name == "Tb":
            return _dihedron_property_Tb(ddata)
        elif field_name == "Tc":
            return _dihedron_property_Tc(ddata)
        elif field_name == "Tx":
            return _dihedron_property_Tx(ddata)
        elif field_name == "Ty":
            return _dihedron_property_Ty(ddata)
        elif field_name == "Tz":
            return _dihedron_property_Tz(ddata)
        else:
            raise ValueError(f"bad property name {field_name}")
    else:
        return _dihed_prop(ddata, field_name)
def dihedral_Tb_completions_trie(b, a, x, y, c, A, X, Y, C, z, Z, Z2):
    """
        elif field_name == dd.Tb:
        args = [dd.b, dd.a, dd.x, dd.y, dd.c, dd.A, dd.X, dd.Y, dd.C, dd.z, dd.Z, dd.Z2]
        completion_type = DihedronCoordinateType.Dihedral
    elif field_name == dd.Ta:
        args = [dd.a, dd.b, dd.x, dd.y, dd.z, dd.B1, dd.X, dd.Y3, dd.Z, dd.c, dd.C, dd.C4]
        completion_type = DihedronCoordinateType.Dihedral
    """
    return _permutation_trie(
        [
            ([X, Z, C], dihedral_from_XZC),
            ([A, Z2, Y], dihedral_from_XZC),
            ([a, y, X, C, z], dihedral_from_ayXCz),
            ([x, c, A, Y, z], dihedral_from_ayXCz),
            ([a, b, c, x, y, z], dihedral_from_abcxyz),
            ([a, b, c, x, Y, z], dihedral_from_abcxYz),
            ([c, b, a, y, X, z], dihedral_from_abcxYz),
            ([a, b, c, X, Y, z], dihedral_from_abcXYz),
            ([x, b, y, A, C, z], dihedral_from_abcXYz),
            ([x, b, y, a, C, z], dihedral_from_abcxYz),
            ([y, b, x, c, A, z], dihedral_from_abcxYz)
        ]
    )
def dihedral_b_completions_trie(a, x, A, X, B1,
                                y, c, Y, C, B2,
                                z, Y3, C4, A3, X4,
                                Tz):
    b = object()
    dihed_comps = _permutation_trie(
            [
                ([x, a, Y3, C4, Tz], dihedral_z_from_ayXCt),
                ([y, c, A3, X4, Tz], dihedral_z_from_ayXCt),
                # a b c X Y Tb -> z a c X4 Y3 T
                ([a, z, c, Y3, X4, Tz], dihedral_z_from_abcXYt),
                ([a, z, c, y, X4, Tz], dihedral_z_from_abcxYt),
                ([c, z, a, x, Y3, Tz], dihedral_z_from_abcxYt),
                ([a, z, c, y, x, Tz], dihedral_z_from_abcxyt),
                # x b y A C Tb -> x a y C4 Z2 T
                ([y, z, x, A3, C4, Tz], dihedral_z_from_abcXYt),
                ([y, z, x, a, C4, Tz], dihedral_z_from_abcxYt),
                ([x, z, y, c, A3, Tz], dihedral_z_from_abcxYt)
            ]
        )
    return _trie_merge(
        dihed_comps,
        _trie_merge(
            triangle_completions_trie(make_triangle(a=a, b=b, c=x, A=A, B=B1, C=X), b),
            triangle_completions_trie(make_triangle(a=y, b=b, c=c, A=Y, B=B2, C=C), b),
        )
    )
def dihedral_Z_completions_trie(X, C, Tb, z, a, y, A3, Y3):
    Z = object()
    return _trie_merge(
        _permutation_trie(
            [
                ([X, Tb, C], dihedral_Z_from_XtC),
            ]
        ),
        triangle_completions_trie(make_triangle(a=a, b=y, c=z, A=A3, B=Y3, C=Z), Z)
    )

class DihedronCoordinateType(enum.Enum):
    Distance = "distance"
    Angle = "angle"
    Dihedral = "dihedral"
def dihedral_completions_trie(dd, field_name, return_args=True):
    if field_name == 'a': # (01)
        #       (21)  (20)                     (31)  (30)
        args = [dd.b, dd.x, dd.B1, dd.X, dd.A, dd.y, dd.z, dd.Y3, dd.Z, dd.A3, dd.c, dd.Y, dd.Z2, dd.B2, dd.X4, dd.Tc]
        completion_type = DihedronCoordinateType.Distance
    elif field_name == 'b': # (1, 2)
        #      (01)   (02) (021)  (012) (102)  (13)  (23)  (123) (213) (132)  (03)  (103)  (203)
        args = [dd.a, dd.x, dd.A, dd.X, dd.B1, dd.y, dd.c, dd.Y, dd.C, dd.B2, dd.z, dd.Y3, dd.C4, dd.A3, dd.X4, dd.Tz]
        completion_type = DihedronCoordinateType.Distance
    elif field_name == 'c': # (2,3)
        #       (13)  (12)                     (03)  (02)
        args = [dd.y, dd.b, dd.Y, dd.B2, dd.C, dd.z, dd.x, dd.Z2, dd.X4, dd.C4, dd.a, dd.Z, dd.X, dd.Y3, dd.B1, dd.Ta]
        completion_type = DihedronCoordinateType.Distance
    elif field_name == 'x': # (0,2)
        #       (10)  (12)                     (30)  (32)
        args = [dd.a, dd.b, dd.A, dd.B1, dd.X, dd.z, dd.c, dd.Z2, dd.C4, dd.X4, dd.y, dd.Z, dd.C, dd.A3, dd.B2, dd.Ty]
        completion_type = DihedronCoordinateType.Distance
    elif field_name == 'y': # (13)
        #       (21)  (23)                     (01)  (03)
        args = [dd.b, dd.c, dd.B2, dd.C, dd.Y, dd.a, dd.z, dd.A3, dd.Z, dd.Y3, dd.x, dd.A, dd.Z2, dd.B1, dd.C4, dd.Tx]
        completion_type = DihedronCoordinateType.Distance
    elif field_name == 'z': # (03)
        #       (10)  (13)                      (20)  (23)
        args = [dd.a, dd.y, dd.A3, dd.Y3, dd.Z, dd.x, dd.c, dd.X4, dd.C4, dd.Z2, dd.b, dd.X, dd.C, dd.A, dd.Y, dd.Tb]
        completion_type = DihedronCoordinateType.Distance
    #TODO: check angle coordinate ordering is always clean...
    elif field_name == dd.Z:
        args = [dd.X, dd.C, dd.Tb, dd.z, dd.a, dd.y, dd.A3, dd.Y3]
        completion_type = DihedronCoordinateType.Angle
    elif field_name == dd.Z2:
        args = [dd.A, dd.Y, dd.Tb, dd.z, dd.x, dd.c, dd.X4, dd.C4]
        completion_type = DihedronCoordinateType.Angle
    elif field_name == dd.C:
        args = [dd.X, dd.Z, dd.Ta, dd.c, dd.y, dd.b, dd.Y, dd.B2]
        completion_type = DihedronCoordinateType.Angle
    elif field_name == dd.C4:
        args = [dd.B1, dd.Y3, dd.Ta, dd.c, dd.x, dd.z, dd.X4, dd.Z2]
        completion_type = DihedronCoordinateType.Angle
    elif field_name == dd.A3:
        args = [dd.B2, dd.X4, dd.Tc, dd.a, dd.y, dd.z, dd.Y3, dd.Z]
        completion_type = DihedronCoordinateType.Angle
    elif field_name == dd.A:
        args = [dd.Y, dd.Z2, dd.Tc, dd.a, dd.b, dd.x, dd.B1, dd.X]
        completion_type = DihedronCoordinateType.Angle
    elif field_name == dd.Y3:
        args = [dd.B1, dd.C4, dd.Tx, dd.y, dd.a, dd.z, dd.A3, dd.Z]
        completion_type = DihedronCoordinateType.Angle
    elif field_name == dd.Y:
        args = [dd.A, dd.Z2, dd.Tx, dd.y, dd.b, dd.c, dd.B2, dd.C]
        completion_type = DihedronCoordinateType.Angle
    elif field_name == dd.X:
        args = [dd.C, dd.Z, dd.Ty, dd.x, dd.a, dd.b, dd.A, dd.B1]
        completion_type = DihedronCoordinateType.Angle
    elif field_name == dd.X4:
        args = [dd.B2, dd.A3, dd.Ty, dd.x, dd.z, dd.c, dd.Z2, dd.C4]
        completion_type = DihedronCoordinateType.Angle
    elif field_name == dd.B1:
        args = [dd.Y3, dd.C4, dd.Tz, dd.b, dd.a, dd.x, dd.A, dd.X]
        completion_type = DihedronCoordinateType.Angle
    elif field_name == dd.B2:
        args = [dd.A3, dd.X4, dd.Tz, dd.b, dd.y, dd.c, dd.Y, dd.C]
        completion_type = DihedronCoordinateType.Angle
    elif field_name == dd.Tb:
        args = [dd.b, dd.a, dd.x, dd.y, dd.c, dd.A, dd.X, dd.Y, dd.C, dd.z, dd.Z, dd.Z2]
        completion_type = DihedronCoordinateType.Dihedral
    elif field_name == dd.Ta:
        args = [dd.a, dd.b, dd.x, dd.y, dd.z, dd.B1, dd.X, dd.Y3, dd.Z, dd.c, dd.C, dd.C4]
        completion_type = DihedronCoordinateType.Dihedral
    elif field_name == dd.Tc:
        args = [dd.c, dd.y, dd.b, dd.x, dd.z, dd.Y, dd.B2, dd.X4, dd.Z2, dd.a, dd.A3, dd.A]
        completion_type = DihedronCoordinateType.Dihedral
    elif field_name == dd.Tx:
        args = [dd.x, dd.a, dd.b, dd.z, dd.c, dd.A, dd.B1, dd.Z2, dd.C4, dd.y, dd.Y3, dd.Y]
        completion_type = DihedronCoordinateType.Dihedral
    elif field_name == dd.Ty:
        args = [dd.y, dd.b, dd.c, dd.a, dd.z, dd.B2, dd.C, dd.A3, dd.Z, dd.x, dd.X, dd.X4]
        completion_type = DihedronCoordinateType.Dihedral
    elif field_name == dd.Tz:
        args = [dd.z, dd.a, dd.y, dd.x, dd.c, dd.A3, dd.Y3, dd.X4, dd.C4, dd.b, dd.B1, dd.B2]
        completion_type = DihedronCoordinateType.Dihedral
    else:
        raise ValueError(f"can't interepret field name {field_name}")

    if completion_type == DihedronCoordinateType.Distance:
        trie = dihedral_b_completions_trie(*args)
    elif completion_type == DihedronCoordinateType.Angle:
        trie = dihedral_Z_completions_trie(*args)
    else:
        trie = dihedral_Tb_completions_trie(*args)

    if return_args:
        return (args, completion_type), trie
    else:
        return trie
def dihedral_completions(field_name, return_trie=False, return_args=False, **dihedron_values):
    dd = make_symbolic_dihedron(**dihedron_values)
    args, trie = dihedral_completions_trie(dd, field_name, return_args=True)
    if not return_trie:
        completions = _expand_trie(trie)
    else:
        completions = trie
    if return_args:
        return args, completions
    else:
        return completions
def dihedral_completion_paths(dd: DihedralTetrahedronData, field_name,
                              return_trie=False,
                              indices=None,
                              positions=False,
                              return_args=False
                              ):
    args, completions_trie = dihedral_completions(field_name,
                                                  return_trie=True,
                                                  return_args=True,
                                                  indices=indices,
                                                  positions=positions)

    res = _completion_paths(dd, completions_trie, _dihed_prop, return_trie=return_trie)


    if return_args:
        return args, res
    else:
        return res
def dihedron_is_complete(dd: DihedralTetrahedronData):
    tris = [
        dihedron_triangle_1(dd),
        dihedron_triangle_2(dd),
        dihedron_triangle_3(dd),
        dihedron_triangle_4(dd)
    ]
    comps = [triangle_is_complete(t) for t in tris]
    for i,j in itertools.combinations(range(4), 2):
        if comps[i] and comps[j]:
            for x in dihedron_triangle_pair_dihedrals[(i,j)]:
                if dihedron_property(dd, x, allow_completion=False) is not None:
                    return True
    return False
def enumerate_dihedron_completions(dd):
    if dihedron_is_complete(dd):
        yield ()
    else:
        # checks are getting duplicated, but they're cheap
        tris = [
            dihedron_triangle_1(dd),
            dihedron_triangle_2(dd),
            dihedron_triangle_3(dd),
            dihedron_triangle_4(dd)
        ]
        comps = [triangle_is_complete(t) for t in tris]
        pair_scoring = {
            (i,j): (1 if comps[i] else 0) + (1 if comps[j] else 0)
            for i,j in itertools.combinations(range(4), 2)
        }
        max_score = max(pair_scoring.values())
        pair_scoring = [k for k,v in pair_scoring.items() if v == max_score]
        for i,j in pair_scoring:
            subenums = [
                enumerate_triangle_completions(tris[i])
                    if not comps[i] else
                [[]],
                enumerate_triangle_completions(tris[j])
                    if not comps[j] else
                [[]],
                dihedron_triangle_pair_dihedrals[(i, j)]
            ]
            tri_map_1 = dict(zip(tris[i]._asdict().keys(), dihedron_triangle_fields[i]))
            tri_map_2 = dict(zip(tris[j]._asdict().keys(), dihedron_triangle_fields[j]))
            for c_i, c_j, p in itertools.product(*subenums):
                yield tuple(tri_map_1[x] for x in c_i) + tuple(tri_map_2[y] for y in c_j) + (p,)

def dihedron_property_function(sample_dihed: DihedralTetrahedronData, field_name,
                               disallowed_conversions=None,
                               allow_completion=True,
                               raise_on_missing=True,
                               return_depth=False):
    field_props = dihedron_property_specifiers(field_name)
    field_name = field_props['name']
    if sample_dihed[field_props['index']] is not None:
        ind = field_props['index']
        sign = field_props['sign']
        def convert(tdata, **kwargs):
            return sign*tdata[ind]
        convert.__name__ = 'convert_' + dihedron_property_specifiers(ind)['name']
        if return_depth:
            return 0, convert
        else:
            return convert
    else:
        args, (complete, conversion_specs) = dihedral_completion_paths(
            sample_dihed,
            field_name,
            return_trie=True,
            return_args=True
        )
        if complete:
            args, func = conversion_specs
            specs = [
                dihedron_property_specifiers(a)
                for a in args
            ]
            def convert(tdata, **kwargs):
                return field_props['sign']*func(*(s['sign']*tdata[s['index']] for s in specs))
            convert.__name__ = f'convert_{field_props["name"]}_{func.__name__}'
            if return_depth:
                return 1, convert
            else:
                return convert
        else:
            if allow_completion:
                possible_conversions = {}
                convertable_keys = {}
                for base_args, trie in conversion_specs:
                    for l,f in _expand_trie(trie).items():
                        props = [_dihed_prop(sample_dihed, ll) is not None for ll in l]
                        rem_inds = [i for i,j in enumerate(props) if not j]
                        base_inds = [i for i,j in enumerate(props) if j]
                        rem_list = tuple(sorted(l[i] for i in rem_inds))
                        base_args = tuple(sorted(base_args, key=lambda x:l.index(x)))
                        possible_conversions[rem_list] = (l, base_args, rem_inds, base_inds, f)
                # print(field_name, possible_conversions)
                pref_keys = list(sorted(possible_conversions.keys(), key=len))
                if disallowed_conversions is None:
                    disallowed_conversions = {field_name}
                else:
                    disallowed_conversions.add(field_name)
                complete_convs = []
                for kl in pref_keys:
                    for k in kl:
                        if k not in convertable_keys:
                            if k in disallowed_conversions: break
                            d2 = dihedron_property_function(sample_dihed, k,
                                                            disallowed_conversions=disallowed_conversions,
                                                            allow_completion=True,
                                                            raise_on_missing=False,
                                                            return_depth=True)
                            if d2 is None:
                                disallowed_conversions.add(k)
                                break
                            else:
                                convertable_keys[k] = d2
                    else:
                        # print(field_name, kl,
                        #       # possible_conversions[kl],
                        #       {c: possible_conversions.get(c, None) for c in kl}
                        #       )
                        complete_convs.append([sum(convertable_keys[k][0] for k in kl), kl])
                if len(complete_convs) > 0:
                    depth, kl = sorted(complete_convs, key=lambda c:c[0])[0]
                    full_args, base_args, rem_inds, base_inds, func = possible_conversions[kl]
                    # print('!', field_name, kl, sample_dihed)#convertable_keys)
                    completions = [convertable_keys[k][1] for k in kl]
                    base_arg_inds = [
                        _ddata_name_map[a]
                            if isinstance(a, str) else
                        a
                        for a in base_args
                    ]
                    nargs = len(full_args)
                    props = dihedron_property_specifiers(field_name)
                    def convert(tdata,
                                base_inds=base_inds,
                                rem_inds=rem_inds,
                                base_arg_inds=base_arg_inds,
                                completions=completions,
                                sign=props['sign'],
                                **kwargs):
                        args = [None] * nargs
                        for i,j in zip(base_inds, base_arg_inds):
                            args[i] = tdata[j]
                        for i,g in zip(rem_inds, completions):
                            args[i] = g(tdata)
                        # print(tdata)
                        # print(base_arg_inds, rem_inds, args)
                        return sign*func(*args)
                    convert.__name__ = f'convert_{props["name"]}_{func.__name__}'
                    if return_depth:
                        return depth + 1, convert
                    else:
                        return convert
            if raise_on_missing:
                raise ValueError(f"can't get property '{field_name}' from {sample_dihed}")
            else:
                return None
            # try to find conversions for subterms

def _rot_gen2(axis):
    axis = np.asanyarray(axis)

    # could be computed via Levi-Cevita connections, but why bother
    K = np.zeros(axis.shape[:-1] + (3, 3))
    for sign, (i,j,k) in [
        [-1, (0, 1, 2)],
        [1, (0, 2, 1)],
        [-1, (1, 2, 0)],
    ]:
        K[..., i, j] = sign*axis[..., k]
        K[..., j, i] = (-sign)*axis[..., k]

    # could be computed via Levi-Cevita connections, but why bother
    K2 = np.zeros(axis.shape[:-1] + (3, 3))
    for (i,j,k) in [(0, 1, 2), (0, 2, 1), (1, 2, 0)]:
        K2[..., k, k] = -(axis[..., i]**2 + axis[..., j]**2)
        K2[..., i, j] = axis[..., i] * axis[..., j]
        K2[..., j, i] = K2[..., i, j]

    return K, K2

def _rot_gen2_deriv(axis, order):
    axis = np.asanyarray(axis)

    # could be computed via Levi-Cevita connections, but why bother
    K0, K20 = _rot_gen2(axis)

    K_expansion = [K0]
    for o in range(order):
        K = np.zeros(axis.shape[:-1] + (3,) * (o+1) + (3, 3))
        if o == 0:
            for a in range(3):
                for sign, (i,j,k) in [
                    [-1, (0, 1, 2)],
                    [1, (0, 2, 1)],
                    [-1, (1, 2, 0)],
                ]:
                    if k == a:
                        K[..., a, i, j] = sign
                        K[..., a, j, i] = -sign
        K_expansion.append(K)

    # could be computed via Levi-Cevita connections, but why bother
    K2_expansion = [K20]
    for o in range(order):
        K2 = np.zeros(axis.shape[:-1] + (3,) * (o+1) + (3, 3))
        if o == 0:
            for a in range(3):
                for (i,j,k) in [(0, 1, 2), (0, 2, 1), (1, 2, 0)]:
                    if a == i:
                        K2[..., a, k, k] = -2*axis[..., i]
                        K2[..., a, i, j] = axis[..., j]
                    if a == j:
                        K2[..., a, k, k] = -2*axis[..., j]
                        K2[..., a, i, j] = axis[..., i]
                    K2[..., a, j, i] = K2[..., a, i, j]
        elif o == 1:
            for a in range(3):
                for (i, j, k) in [(0, 1, 2), (0, 2, 1), (1, 2, 0)]:
                    if a == i or a == j:
                        K2[..., a, k, k] = -2
            for a,b in itertools.combinations(range(3), 2):
                for (i, j, k) in [(0, 1, 2), (0, 2, 1), (1, 2, 0)]:
                    if (a == i and b == j) or (a == j and b == i):
                        K2[..., a, b, i, j] = 1
                        K2[..., a, b, j, i] = 1
        K2_expansion.append(K2)

    return K_expansion, K2_expansion


def axis_rot_gen_deriv(angle, axis, angle_order, axis_order=0, normalized=False):
    # if not normalized:
    #     axis = vec_normalize(axis)
    axis = np.asanyarray(axis)
    if axis_order == 0:
        sd = [sin_deriv(angle, n) for n in range(angle_order+1)]
        cd = [cos_deriv(angle, n) for n in range(angle_order+1)]
        K, K2 = _rot_gen2(axis)
        mom = vec_outer(axis, axis)
        return [
            (mom if i == 0 else 0) + s * K - c * K2
            for i,(s,c) in enumerate(zip(sd, cd))
        ]
    elif angle_order == 0:
        s = np.sin(angle)
        c = np.cos(angle)
        eye = identity_tensors(axis.shape[:-1], 3)
        mom_expansion = td.tensorprod_deriv([axis, eye], [axis, eye], axis_order)
        K_expansion, K2_expansion = _rot_gen2_deriv(axis, axis_order)
        return [m + s * K - c * K2 for m,K,K2 in zip(mom_expansion, K_expansion, K2_expansion)]
    else:
        raise NotImplementedError("cross terms are tedious")
