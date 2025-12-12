from __future__ import annotations

"""
Provides analytic derivatives for some common base terms with the hope that we can reuse them elsewhere
"""

import itertools
import math
import numpy as np
from .VectorOps import *
from . import CoordinateFrames as frames
from . import TensorDerivatives as td
from . import Misc as misc
from . import SetOps as setops
from . import PermutationOps as pops
from . import Geometry as geom
from .Options import Options

__all__ = [
    'rot_deriv',
    'rot_deriv2',
    'cartesian_from_rad_derivatives',
    'dist_basis',
    'angle_basis',
    # 'dihed_bases',
    'internal_basis',
    'dist_deriv',
    'angle_deriv',
    'dihed_deriv',
    'book_deriv',
    'oop_deriv',
    'wag_deriv',
    'transrot_deriv',
    'com_dist_deriv',
    # "com_pos_diff_deriv",
    'orientation_deriv',
    "rotation_expansion_from_axis_angle",
    "dist_expansion",
    "dihed_expansion",
    "angle_expansion",
    'vec_norm_derivs',
    'vec_sin_cos_derivs',
    'vec_angle_derivs',
    'rock_deriv',
    'rock_vec',
    'dist_vec',
    'angle_vec',
    'dihed_vec',
    'book_vec',
    'oop_vec',
    'wag_vec',
    "internal_conversion_function",
    "internal_coordinate_tensors",
    "inverse_internal_coordinate_tensors",
    "inverse_coordinate_solve",
    "metric_tensor",
    "delocalized_internal_coordinate_transformation",
    "relocalize_coordinate_transformation",
    "transform_cartesian_derivatives"
]

def _prod_deriv(op, a, b, da, db):
    """
    Simple product derivative to make apply the product rule and its analogs
    a bit cleaner. Assumes a derivative that doesn't change dimension.
    Should be generalized at some point to handle arbitrary outer products and shit of that sort.
    :param op:
    :type op:
    :param a:
    :type a:
    :param b:
    :type b:
    :param da:
    :type da:
    :param db:
    :type db:
    :return:
    :rtype:
    """
    return op(a, db) + op(da, b)
def _prod_deriv_2(op, a, b, da1, da2, db1, db2, da12, db12):
    """
    2nd derivative of op(a, b) assuming it operates under a product-rule type ish
    """
    return op(da12, b) + op(da1, db2) + op(da2, db1) + op(a, db12)

def normalized_vec_deriv(v, dv):
    """
    Derivative of a normalized vector w/r/t some unspecified coordinate
    """
    norms = vec_norms(v)[..., np.newaxis]
    vh = v / norms
    i3 = np.broadcast_to(np.eye(3), dv.shape[:-1] + (3, 3))
    vXv = vec_outer(vh, vh)
    wat = np.matmul(i3 - vXv, dv[..., np.newaxis])[..., 0] # gotta add a 1 for matmul
    return wat / norms

def normalized_vec_deriv2(v, dv1, dv2, d2v):
    """
    Second derivative of a normalized vector w/r/t some unspecified coordinates
    """
    # derivative of inverse norm
    norms = vec_norms(v)[..., np.newaxis]
    vds2 = vec_dots(dv2, v)[..., np.newaxis]
    dnorminv = -1/(norms**3) * vds2
    vh = v / norms
    i3 = np.broadcast_to(np.eye(3), dv1.shape[:-1] + (3, 3))
    vXv = vec_outer(vh, vh)
    dvh2 = normalized_vec_deriv(v, dv2)
    dvXv2 = _prod_deriv(vec_outer, vh, vh, dvh2, dvh2)
    right = np.matmul(i3 - vXv, dv1[..., np.newaxis])[..., 0]  # gotta add a 1 for matmul
    dright = _prod_deriv(np.matmul, i3 - vXv, dv1[..., np.newaxis], -dvXv2, d2v[..., np.newaxis])[..., 0]
    der = _prod_deriv(np.multiply, 1/norms, right, dnorminv, dright)
    return der

def rot_deriv(angle, axis, dAngle, dAxis):
    """
    Gives a rotational derivative w/r/t some unspecified coordinate
    (you have to supply the chain rule terms)
    Assumes that axis is a unit vector.

    :param angle: angle for rotation
    :type angle: float
    :param axis: axis for rotation
    :type axis: np.ndarray
    :param dAngle: chain rule angle deriv.
    :type dAngle: float
    :param dAxis: chain rule axis deriv.
    :type dAxis: np.ndarray
    :return: derivatives of the rotation matrices with respect to both the angle and the axis
    :rtype: np.ndarray
    """

    # Will still need work to be appropriately vectorized (can't remember if I did this or not?)
    vdOdv = vec_outer(dAxis, axis) + vec_outer(axis, dAxis)
    c = np.cos(angle)[..., np.newaxis]
    s = np.sin(angle)[..., np.newaxis]
    i3 = np.broadcast_to(np.eye(3), axis.shape[:-1] + (3, 3))
    e3 = np.broadcast_to(pops.levi_cevita3, axis.shape[:-1] + (3, 3, 3))
    # e3 = pops.levi_cevita3
    # i3 = np.eye(3)
    ct = vdOdv*(1-c[..., np.newaxis])
    st = (i3-vec_outer(axis, axis))*s[..., np.newaxis]*dAngle
    wat = (dAxis*s + axis*c*dAngle)
    et = vec_tensordot(e3, wat, axes=[-1, 1]) # currently explicitly takes a stack of vectors...
    return ct - st - et

def rot_deriv2(angle, axis, dAngle1, dAxis1, dAngle2, dAxis2, d2Angle, d2Axis):
    """
    Gives a rotation matrix second derivative w/r/t some unspecified coordinate
    (you have to supply the chain rule terms)

    :param angle: angle for rotation
    :type angle: float
    :param axis: axis for rotation
    :type axis: np.ndarray
    :param dAngle: chain rule angle deriv.
    :type dAngle: float
    :param dAxis: chain rule axis deriv.
    :type dAxis: np.ndarray
    :return: derivatives of the rotation matrices with respect to both the angle and the axis
    :rtype: np.ndarray
    """

    from operator import mul

    # lots of duplication since we've got the same axis twice
    vXv = vec_outer(axis, axis)
    dvXv1 = _prod_deriv(vec_outer, axis, axis, dAxis1, dAxis1)
    dvXv2 = _prod_deriv(vec_outer, axis, axis, dAxis2, dAxis2)
    d2vXv = _prod_deriv_2(vec_outer, axis, axis, dAxis1, dAxis2, dAxis1, dAxis2, d2Axis, d2Axis)

    i3 = np.broadcast_to(np.eye(3), axis.shape[:-1] + (3, 3))
    e3 = np.broadcast_to(pops.levi_cevita3, axis.shape[:-1] + (3, 3, 3))

    c = np.cos(angle)
    s = np.sin(angle)

    dc1 = -s * dAngle1
    dc2 = -s * dAngle2
    d2c = -s * d2Angle - c * dAngle1 * dAngle2

    cos_term = _prod_deriv_2(mul,
                             i3 - vXv,
                             c[..., np.newaxis, np.newaxis],
                             dvXv1, dvXv2,
                             dc1[..., np.newaxis, np.newaxis], dc2[..., np.newaxis, np.newaxis],
                             d2vXv, d2c[..., np.newaxis, np.newaxis]
                             )

    ds1 = c * dAngle1
    ds2 = c * dAngle2
    d2s = c * d2Angle - s * dAngle1 * dAngle2
    fack = _prod_deriv_2(mul, axis, s[..., np.newaxis], dAxis1, dAxis2, ds1[..., np.newaxis], ds2[..., np.newaxis], d2Axis, d2s[..., np.newaxis])
    sin_term = vec_tensordot(e3, fack, axes=[-1, 1])

    return d2vXv + cos_term - sin_term

def _rad_d1(i, z, m, r, a, d, v, u, n, R1, R2, Q, rv, dxa, dxb, dxc):

    # derivatives of coordinates
    dr = 1 if (z == i and m == 0) else 0
    dq = 1 if (z == i and m == 1) else 0
    df = 1 if (z == i and m == 2) else 0

    dv_ = dxb - dxa
    dv = normalized_vec_deriv(v, dv_)
    v = vec_normalize(v)
    if a is None:
        # no derivative about any of the rotation shit
        drv = _prod_deriv(np.multiply, r[..., np.newaxis], v, dr, dv)
        du_ = dn_ = dR1 = dR2 = dQ = None
        der = dxa + drv
    else:
        # derivatives of axis system vectors
        du_ = dxc - dxb
        du = normalized_vec_deriv(u, du_)
        u = vec_normalize(u)
        dn_ = _prod_deriv(vec_crosses, v, u, dv, du)
        # we actually need the derivatives of the unit vectors for our rotation axes
        dn = normalized_vec_deriv(n, dn_)
        n = vec_normalize(n)
        # raise Exception(n.shape, dn.shape, dn_.shape)

        # derivatives of rotation matrices
        dR1 = rot_deriv(a, n, dq, dn)
        if d is not None:
            dR2 = rot_deriv(d, v, df, dv)
            # derivative of total rotation matrix
            dQ = _prod_deriv(np.matmul, R2, R1, dR2, dR1)
        else:
            dR2 = None
            dQ = dR1

        # derivative of vector along the main axis
        drv = _prod_deriv(np.multiply, r, v, dr, dv)
        der = dxa + _prod_deriv(np.matmul, Q, rv[..., np.newaxis], dQ, drv[..., np.newaxis])[..., 0]

    return der, (dr, dq, df, dv_, du_, dn_, dR1, dR2, dQ, drv)

def _rad_d2(i, z1, m1, z2, m2, # don't actually use these because all the coordinate 2nd derivatives are 0 :yay:
            r, a, d, v, u, n, R1, R2, Q, rv,
            dr1, dq1, df1, dv1, du1, dn1, dR11, dR21, dQ1, drv1,
            dr2, dq2, df2, dv2, du2, dn2, dR12, dR22, dQ2, drv2,
            d2xa, d2xb, d2xc):

    # second derivatives of embedding axes
    # fuck this is annoying...need to get the _unnormalized_ shit too to get the norm deriv as I have it...
    d2v = normalized_vec_deriv2(v, dv1, dv2, d2xb - d2xa)
    dv1 = normalized_vec_deriv(v, dv1)
    dv2 = normalized_vec_deriv(v, dv2)
    v = vec_normalize(v)
    if r.shape[-1] == 1: # shape hack for now... to flatten r I guess...
        r = r[..., 0]
    if a is None:
        d2rv = _prod_deriv_2(np.multiply, r[..., np.newaxis], v, dr1, dr2, dv1, dv2, 0, d2v)
        der = d2xa + d2rv
        d2u = d2n = d2R1 = d2R2 = d2Q = None
    else:
        d2u = normalized_vec_deriv2(u, du1, du2, d2xc - d2xb)
        du1 = normalized_vec_deriv(u, du1)
        du2 = normalized_vec_deriv(u, du2)
        u = vec_normalize(u)
        d2n_ = _prod_deriv_2(vec_crosses, v, u, dv1, dv2, du1, du2, d2v, d2u)
        d2n = normalized_vec_deriv2(v, dn1, dn2, d2n_)
        dn1 = normalized_vec_deriv(u, dn1)
        dn2 = normalized_vec_deriv(u, dn2)
        n = vec_normalize(n)

        # second derivatives of rotation matrices
        d2R1 = rot_deriv2(a, n, dq1, dn1, dq2, dn2, 0, d2n)
        if d is None:
            d2R2 = None
            d2Q = d2R1
        else:
            d2R2 = rot_deriv2(d, v, df1, dv1, df2, dv2, 0, d2v)
            d2Q = _prod_deriv_2(np.matmul, R2, R1, dR21, dR22, dR11, dR12, d2R1, d2R2)

        # second derivatives of r*v
        d2rv = _prod_deriv_2(np.multiply, r[..., np.newaxis], v, dr1, dr2, dv1, dv2, 0, d2v)

        # new derivative
        der = d2xa + _prod_deriv_2(np.matmul, Q, rv[..., np.newaxis], dQ1, dQ2, drv1[..., np.newaxis], drv2[..., np.newaxis], d2Q, d2rv[..., np.newaxis])[..., 0]

    # if der.shape == (7, 7, 3):
    #     raise ValueError(r.shape, d2v.shape, d2rv.shape)#, d2u.shape, d2n.shape, d2R1.shape, d2R2.shape, d2Q.shape, d2rv.shape)
    return der, (d2v, d2u, d2n, d2R1, d2R2, d2Q, d2rv)

class _dumb_comps_wrapper:
    """
    Exists solely to prevent numpy from unpacking
    """
    def __init__(self, comp):
        self.comp = comp
def cartesian_from_rad_derivatives(
        xa, xb, xc,
        r, a, d,
        i,
        ia, ib, ic,
        derivs,
        order=2,
        return_comps=False
):
    """
    Returns derivatives of the generated Cartesian coordinates with respect
    to the internals
    """

    if order > 2:
        raise NotImplementedError("bond-angle-dihedral to Cartesian derivatives only implemented up to order 2")

    coord, comps = cartesian_from_rad(xa, xb, xc, r, a, d, return_comps=True)
    v, u, n, R2, R1 = comps
    if R2 is not None:
        Q = np.matmul(R2, R1)
    elif R1 is not None:
        Q = R1
    else:
        Q = None
    if r.ndim < v.ndim:
        rv = r[..., np.newaxis] * vec_normalize(v)
    else:
        rv = r * vec_normalize(v)

    #TODO: I think I'm re-calculating terms I did for a previous value of i?
    #       ...except I'm not because _rad_d1 has some Kronecker delta terms...
    #       still, it could all be made way more efficient I bet by reusing stuff
    new_derivs = []
    new_derivs.append(coord)
    new_comps = []
    new_comps.append(comps)
    inds = np.arange(len(ia))
    if order > 0:
        if derivs[1].ndim != 5:
            raise ValueError("as implemented, derivative blocks have to look like (nconfigs, nzlines, 3, natoms, 3)")
        config_shape = derivs[1].shape[:-4]
        d1 = np.zeros(config_shape + (i+1, 3, 3)) # the next block in the derivative tensor
        d1_comps = np.full((i+1, 3), None) # the components used to build the derivatives
        for z in range(i + 1):  # Lower-triangle is 0 so we do nothing with it
            for m in range(3):
                # we'll need to do some special casing for z < 2
                # also we gotta pull o
                dxa = derivs[1][inds, z, m, ia, :]
                dxb = derivs[1][inds, z, m, ib, :]
                dxc = derivs[1][inds, z, m, ic, :]

                # raise Exception(dxa.shape, derivs[1].shape)
                der, comps1 = _rad_d1(i, z, m, r, a, d, v, u, n, R1, R2, Q, rv, dxa, dxb, dxc)
                d1_comps[z, m] = _dumb_comps_wrapper(comps1)

                d1[inds, z, m, :] = der
        new_derivs.append(d1)
        new_comps.append(d1_comps)
        if order > 1:
            d2 = np.zeros(config_shape + (i+1, 3, i+1, 3, 3)) # the next block in the 2nd derivative tensor
            d2_comps = np.full((i+1, 3, i+1, 3), None) # the components used to build the derivatives
            for z1 in range(i + 1):
                for m1 in range(3):
                    for z2 in range(i + 1):
                        for m2 in range(3):
                                d2xa = derivs[2][inds, z1, m1, z2, m2, ia, :]
                                d2xb = derivs[2][inds, z1, m1, z2, m2, ib, :]
                                d2xc = derivs[2][inds, z1, m1, z2, m2, ic, :]
                                dr1, dq1, df1, dv1, du1, dn1, dR11, dR21, dQ1, drv1 = d1_comps[z1, m1].comp
                                dr2, dq2, df2, dv2, du2, dn2, dR12, dR22, dQ2, drv2 = d1_comps[z2, m2].comp

                                # now we feed this in
                                der, comps2 = _rad_d2(i, z1, m1, z2, m2,
                                                      r, a, d, v, u, n, R1, R2, Q, rv,
                                                      dr1, dq1, df1, dv1, du1, dn1, dR11, dR21, dQ1, drv1,
                                                      dr2, dq2, df2, dv2, du2, dn2, dR12, dR22, dQ2, drv2,
                                                      d2xa, d2xb, d2xc
                                                      )
                                d2[inds, z1, m1, z2, m2, :] = der
                                d2_comps[z1, m1, z2, m2] = _dumb_comps_wrapper(comps2)
            new_derivs.append(d2)
            new_comps.append(d2_comps)

    if return_comps:
        return new_derivs, new_comps
    else:
        return new_derivs

def vec_norm_derivs(a, order=1, zero_thresh=None):
    """
    Derivative of the norm of `a` with respect to its components

    :param a: vector
    :type a: np.ndarray
    :param order: number of derivatives to return
    :type order: int
    :param zero_thresh:
    :type zero_thresh:
    :return: derivative tensors
    :rtype: list
    """

    if order > 2:
        raise NotImplementedError("derivatives currently only up to order {}".format(2))

    derivs = []

    na = vec_norms(a)
    derivs.append(np.copy(na)) # we return the value itself for Taylor-series reasons

    # print(a.shape)
    a, zeros = vec_handle_zero_norms(a, na, zero_thresh=zero_thresh)
    na = na[..., np.newaxis]
    na[zeros] = Options.zero_placeholder

    if order >= 1:
        d1 = a / na
        # print(a.shape, na.shape)

        derivs.append(d1)

    if order >= 2:
        n = a.shape[-1]
        extra_shape = a.ndim - 1
        if extra_shape > 0:
            i3 = np.broadcast_to(np.eye(n), (1,)*extra_shape + (n, n))
        else:
            i3 = np.eye(n)
        v = vec_outer(d1, d1)
        # na shold have most of the extra_shape needed
        d2 = (i3 - v) / na[..., np.newaxis]
        derivs.append(d2)

    return derivs

def vec_sin_cos_derivs(a, b, order=1,
                       up_vectors=None,
                       check_derivatives=False, zero_thresh=None):
    """
    Derivative of `sin(a, b)` and `cos(a, b)` with respect to both vector components

    :param a: vector
    :type a: np.ndarray
    :param a: other vector
    :type a: np.ndarray
    :param order: number of derivatives to return
    :type order: int
    :param zero_thresh: threshold for when a norm should be called 0. for numerical reasons
    :type zero_thresh: None | float
    :return: derivative tensors
    :rtype: list
    """

    if order > 2:
        raise NotImplementedError("derivatives currently only up to order {}".format(2))

    extra_dims = a.ndim - 1

    sin_derivs = []
    cos_derivs = []

    a, n_a = vec_apply_zero_threshold(a, zero_thresh=zero_thresh)
    b, n_b = vec_apply_zero_threshold(b, zero_thresh=zero_thresh)

    n = vec_crosses(a, b)
    n, n_n, bad_ns = vec_apply_zero_threshold(n, zero_thresh=zero_thresh, return_zeros=True)

    adb = vec_dots(a, b)[..., np.newaxis]

    zero_thresh = Options.norm_zero_threshold if zero_thresh is None else zero_thresh

    s = n_n / (n_a * n_b)
    # s[n_n <= zero_thresh] = 0.
    c = adb / (n_a * n_b)
    # c[adb <= zero_thresh] = 0.

    sin_derivs.append(s)
    cos_derivs.append(c)

    if order > 0:
        if bad_ns.any():  # ill-defined sin components need an "up" vector and then point perpendicular to this
            if up_vectors is None:
                if n.ndim > 1:
                    up_vectors = np.broadcast_to(
                        np.array([0, 0, 1])[np.newaxis],
                        a.shape[:-1] + (3,)
                    )
                else:
                    up_vectors = np.array([0, 0, 1])
            if n.ndim == 1:
                n = vec_normalize(up_vectors)
                n_n = 1
            else:
                n[bad_ns] = vec_normalize(up_vectors[bad_ns])
                n_n[bad_ns] = 1

        bxn_ = vec_crosses(b, n)
        bxn, n_bxn = vec_apply_zero_threshold(bxn_, zero_thresh=zero_thresh)

        nxa_ = vec_crosses(n, a)
        nxa, n_nxa = vec_apply_zero_threshold(nxa_, zero_thresh=zero_thresh)

        if order <= 1:
            _, na_da = vec_norm_derivs(a, order=1)
            _, nb_db = vec_norm_derivs(b, order=1)
        else:
            _, na_da, na_daa = vec_norm_derivs(a, order=2)
            _, nb_db, nb_dbb = vec_norm_derivs(b, order=2)
            _, nn_dn, nn_dnn = vec_norm_derivs(n, order=2)

        if order >= 1:
            s_da = (bxn / (n_b * n_n) - s * na_da) / n_a
            s_db = (nxa / (n_n * n_a) - s * nb_db) / n_b

            # now we build our derivs, but we also need to transpose so that the OG shape comes first
            d1 = np.array([s_da, s_db])
            d1_reshape = tuple(range(1, extra_dims+1)) + (0, extra_dims+1)
            meh = d1.transpose(d1_reshape)

            sin_derivs.append(meh)

            # print(
            #     nb_db.shape,
            #     na_da.shape,
            #     c.shape,
            #     n_a.shape
            # )

            c_da = (nb_db - c * na_da) / n_a
            c_db = (na_da - c * nb_db) / n_b

            d1 = np.array([c_da, c_db])
            meh = d1.transpose(d1_reshape)

            cos_derivs.append(meh)

        if order >= 2:

            extra_dims = a.ndim - 1
            extra_shape = a.shape[:-1]
            if check_derivatives:
                if extra_dims > 0:
                    bad_norms = n_n.flatten() <= zero_thresh
                    if bad_norms.any():
                        raise ValueError("2nd derivative of sin not well defined when {} and {} are nearly colinear".format(
                            a[bad_norms],
                            b[bad_norms]
                        ))
                else:
                    if n_n <= zero_thresh:
                        raise ValueError("2nd derivative of sin not well defined when {} and {} are nearly colinear".format(
                            a, b
                        ))

            if extra_dims > 0:
                e3 = np.broadcast_to(pops.levi_cevita3,  extra_shape + (3, 3, 3))
                # td = np.tensordot
                outer = vec_outer
                vec_td = lambda a, b, **kw: vec_tensordot(a, b, shared=extra_dims, **kw)
            else:
                e3 = pops.levi_cevita3
                # td = np.tensordot
                vec_td = lambda a, b, **kw: vec_tensordot(a, b, shared=0, **kw)
                outer = np.outer
                a = a.squeeze()
                b = b.squeeze()
                nb_db = nb_db.squeeze(); na_da = na_da.squeeze(); nn_dn = nn_dn.squeeze()
                na_daa = na_daa.squeeze(); nb_dbb = nb_dbb.squeeze(); nn_dnn = nn_dnn.squeeze()

            # print(na_da, s_da, s, na_daa, bxdna)

            # compute terms we'll need for various cross-products
            e3b = vec_td(e3, b, axes=[-1, -1])
            e3a = vec_td(e3, a, axes=[-1, -1])
            # e3n = vec_td(e3, n, axes=[-1, -1])

            e3nbdb = vec_td(e3, nb_db, axes=[-1, -1])
            e3nada = vec_td(e3, na_da, axes=[-1, -1])
            e3nndn = vec_td(e3, nn_dn, axes=[-1, -1])

            n_da = -vec_td(e3b,  nn_dnn, axes=[-1, -2])
            bxdna = vec_td(n_da, e3nbdb, axes=[-1, -2])

            s_daa = - (
                outer(na_da, s_da) + outer(s_da, na_da)
                + s[..., np.newaxis] * na_daa
                - bxdna
            ) / n_a[..., np.newaxis]

            ndaXnada = -vec_td(n_da, e3nada, axes=[-1, -2])
            nndnXnadaa = vec_td(na_daa, e3nndn, axes=[-1, -2])

            s_dab = (
                         ndaXnada + nndnXnadaa - outer(s_da, nb_db)
            ) / n_b[..., np.newaxis]

            n_db = vec_td(e3a, nn_dnn, axes=[-1, -2])

            nbdbXnda = vec_td(n_db, e3nbdb, axes=[-1, -2])
            nbdbbXnndn = -vec_td(nb_dbb, e3nndn, axes=[-1, -2])

            s_dba = (
                    nbdbXnda + nbdbbXnndn - outer(s_db, na_da)
            ) / n_a[..., np.newaxis]

            dnbxa = - vec_td(n_db, e3nada, axes=[-1, -2])

            s_dbb = - (
                outer(nb_db, s_db) + outer(s_db, nb_db) + s[..., np.newaxis] * nb_dbb - dnbxa
            ) / n_b[..., np.newaxis]

            s2 = np.array([
                [s_daa, s_dab],
                [s_dba, s_dbb]
            ])

            d2_reshape = tuple(range(2, extra_dims+2)) + (0, 1, extra_dims+2, extra_dims+3)
            s2 = s2.transpose(d2_reshape)

            sin_derivs.append(s2)

            # na_daa = np.zeros_like(na_daa)

            c_daa = - (
                outer(na_da, c_da) + outer(c_da, na_da)
                + c[..., np.newaxis] * na_daa
            ) / n_a[..., np.newaxis]
            c_dab = (na_daa - outer(c_da, nb_db)) / n_b[..., np.newaxis]
            c_dba = (nb_dbb - outer(c_db, na_da)) / n_a[..., np.newaxis]
            c_dbb = - (
                outer(nb_db, c_db) + outer(c_db, nb_db)
                + c[..., np.newaxis] * nb_dbb
            ) / n_b[..., np.newaxis]

            c2 = np.array([
                [c_daa, c_dab],
                [c_dba, c_dbb]
            ])

            c2 = c2.transpose(d2_reshape)

            cos_derivs.append(c2)

    return sin_derivs, cos_derivs

def coord_deriv_mat(nats, coords, axes=None, base_shape=None):
    if axes is None:
        axes = [0, 1, 2]
    if misc.is_numeric(coords):
        coords = [coords]
    z = np.zeros((nats, 3, nats, 3))
    row_inds = np.repeat(coords, len(axes), axis=0)
    col_inds = np.repeat(axes, len(coords), axis=0).flatten()
    z[row_inds, col_inds, row_inds, col_inds] = 1
    z = z.reshape(nats*3, nats*3)
    if base_shape is not None:
        sh = z.shape
        expax = list(range(len(base_shape)))
        z = np.broadcast_to(np.expand_dims(z, expax), base_shape + sh)
    return z

def jacobian_mat_inds(ind_lists, axes=None):
    if axes is None:
        axes = [0, 1, 2]

    smol = misc.is_numeric(ind_lists[0])
    ind_lists = [
        np.asanyarray([i] if smol else i).reshape(-1)
        for i in ind_lists
    ]

    nstruct = ind_lists[0].shape[0]
    struct_inds = np.repeat(np.arange(nstruct), len(axes), axis=0)

    inds = []
    for i in ind_lists:
        row_inds = np.repeat(i, len(axes), axis=0)
        col_inds = np.repeat(axes, len(i), axis=0).flatten()
        inds.append((struct_inds, row_inds, col_inds, col_inds))

    return inds

def jacobian_proj_inds(ind_lists, axes=None):
    if axes is None:
        axes = [0, 1, 2]
    axes = np.asanyarray(axes)

    smol = misc.is_numeric(ind_lists[0][0])
    ind_lists = [
        [
            np.asanyarray([i] if smol else i).reshape(-1),
            np.asanyarray([a] if smol else a).reshape(-1)
        ]
        for i,a in ind_lists
    ]

    nstruct = ind_lists[0][0].shape[0]
    struct_inds = np.repeat(np.arange(nstruct), len(axes), axis=0)

    inds = []
    for i,a in ind_lists:
        ax = axes + len(axes) * a
        row_inds = np.repeat(i, len(axes), axis=0)
        col_inds = np.repeat(axes, len(i), axis=0).flatten()
        scol_inds = ax
        inds.append((struct_inds, row_inds, col_inds, scol_inds))

    return inds

def fill_disp_jacob_atom(mat, ind_val_pairs, base_shape=None, axes=None):
    ind_lists = [i for i,v in ind_val_pairs]
    vals = [v for i,v in ind_val_pairs]
    smol = misc.is_numeric(ind_lists[0])
    ind_lists = [
        np.asanyarray([i] if smol else i)
        for i in ind_lists
    ]

    i_shape = ind_lists[0].shape
    nnew = len(i_shape)
    if base_shape is None:
        base_shape = mat.shape[:-3]
    target_shape = base_shape + i_shape + mat.shape[-3:]
    if target_shape != mat.shape:
        nog = len(base_shape)
        mat = np.broadcast_to(
            np.expand_dims(mat, np.arange(nog, nog+nnew).tolist()),
            target_shape
        ).copy()
    else:
        base_shape = mat.shape[:-(3+nnew)]
        # target_shape = base_shape + i_shape + mat.shape[-3:]

    mat = np.reshape(mat, base_shape + (np.prod(i_shape, dtype=int),) + mat.shape[-3:])
    for idx_tup,val in zip(jacobian_mat_inds(ind_lists, axes=axes), vals):
        idx_tup = (...,) + idx_tup
        mat[idx_tup] = val
    mat = mat.reshape(target_shape)

    if smol:
        mat = mat.reshape(base_shape + mat.shape[-3:])
    return mat

def fill_proj_jacob_atom(mat, ind_val_pairs, base_shape=None, axes=None):
    ind_lists = [[i,a] for i,a,v in ind_val_pairs]
    vals = [v for i,a,v in ind_val_pairs]
    smol = misc.is_numeric(ind_lists[0][0])
    ind_lists = [
        [
            np.asanyarray([i] if smol else i),
            np.asanyarray([a] if smol else a),
        ]
        for i,a in ind_lists
    ]

    i_shape = ind_lists[0][0].shape
    nnew = len(i_shape)
    if base_shape is None:
        base_shape = mat.shape[:-3]
    target_shape = base_shape + i_shape + mat.shape[-3:]
    if target_shape != mat.shape:
        nog = len(base_shape)
        mat = np.broadcast_to(
            np.expand_dims(mat, np.arange(nog, nog+nnew).tolist()),
            target_shape
        ).copy()
    else:
        base_shape = mat.shape[:-(3+nnew)]
        # target_shape = base_shape + i_shape + mat.shape[-3:]

    mat = np.reshape(mat, base_shape + (np.prod(i_shape, dtype=int),) + mat.shape[-3:])
    for idx_tup,val in zip(jacobian_proj_inds(ind_lists, axes=axes), vals):
        idx_tup = (...,) + idx_tup
        mat[idx_tup] = val
    mat = mat.reshape(target_shape)

    if smol:
        mat = mat.reshape(base_shape + mat.shape[-3:])
    return mat

fast_proj = True
def disp_deriv_mat(coords, i, j, at_list, axes=None):
    if not fast_proj:
        mats = np.zeros(coords.shape + (3,))
        return None, fill_disp_jacob_atom(
            mats,
            [[i, 1], [j, -1]],
            axes=axes,
            base_shape=coords.shape[:-2]
        )
    else:
        proj = np.zeros(coords.shape + (3 * len(at_list),))
        mats = np.zeros(coords[..., at_list, :].shape + (3,))
        _, (a, b), ord = np.intersect1d(at_list, [i, j], return_indices=True)
        inv = np.argsort(ord)
        a, b = np.array([a, b])[inv,]
        mats = fill_disp_jacob_atom(
            mats,
            [[a, 1], [b, -1]],
            axes=axes,
            base_shape=coords.shape[:-2]
        )
        proj = fill_proj_jacob_atom(
            proj,
            [[x, n, 1] for n,x in enumerate(at_list)],
            axes=axes,
            base_shape=coords.shape[:-2]
        )
        proj = proj.reshape(proj.shape[:-3] + (-1, proj.shape[-1]))
        return proj, mats

def prep_disp_expansion(coords, i, j, at_list, fixed_atoms=None, expand=True):
    a = coords[..., j, :] - coords[..., i, :]

    if expand:
        proj, A_d = disp_deriv_mat(coords, j, i, at_list)
        if fixed_atoms is not None:
            if fast_proj:
                _, fixed_atoms, _ = np.intersect1d(at_list, fixed_atoms, return_indices=True)
            if len(fixed_atoms) > 0:
                A_d = fill_disp_jacob_atom(A_d, [[x, 0] for x in fixed_atoms], base_shape=coords.shape[:-2])

        return proj, [a, misc.flatten_inds(A_d, [-3, -2])]
    else:
        return [a]

def prep_expanded_mats_from_cache(expansion, i, j, at_list, root_dim=1, core_dim=0):
    _, (a, b), ord = np.intersect1d(at_list, [i, j], return_indices=True)
    inv = np.argsort(ord)
    a, b = np.array([a, b])[inv,]
    # a, b = np.sort([a,b])
    # print(at_list, (i, j), a, b)
    natl = len(at_list) * 3
    subpos = (np.array([a, b])[:, np.newaxis] * 3 + np.arange(3)[np.newaxis, :]).flatten()
    new = []
    if core_dim > 0:
        core_shape = expansion[0].shape[-core_dim:]
    else:
        core_shape = ()
    pad_dim = expansion[0].ndim - (root_dim + core_dim)
    base_shape = expansion[0].shape[:pad_dim]
    for n,e in enumerate(expansion):
        n = n + root_dim
        if n > 0:
            block = np.ix_(*[subpos]*n)
            idx = (...,) + block + (slice(None),)*core_dim
            new_sub = np.zeros(base_shape + (natl,) * n + core_shape)
            new_sub[idx] = e
        else:
            new_sub = e
        new.append(new_sub)
    return new

def prep_unit_vector_expansion_from_cache(cache, coords, i, j, at_list, *, expand, fixed_atoms):

    if cache is None or fixed_atoms is not None or not expand:
        proj, A_expansion = prep_disp_expansion(coords, i, j, at_list,
                                                fixed_atoms=fixed_atoms,
                                                expand=expand)
        A_norms, A_expansion = td.vec_norm_unit_deriv(A_expansion, len(A_expansion))
    else:
        proj, A_base = prep_disp_expansion(coords, i, j, at_list,
                                                fixed_atoms=None,
                                                expand=True)

        # if i > j:
        #     j, i = i, j
        #     sign = -1
        # else:
        #     sign = 1
        sign = 1

        key = ((i, j), expand, fixed_atoms)
        if key in cache:
            (A_raw, A_norms, A_expansion) = cache[key]
        else:
            _, A_raw = prep_disp_expansion(coords, i, j, [i, j],
                                                    fixed_atoms=None,
                                                    expand=True)
            A_norms, A_expansion = td.vec_norm_unit_deriv(A_raw, len(A_raw))
            cache[key] = (A_raw, A_norms, A_expansion)

        # print(sign, i, j, at_list)
        # print(sign*A_norms[1])
        A_norms = prep_expanded_mats_from_cache(
            [A_norms[0]] + [(sign ** (n + 1)) * a for n, a in enumerate(A_norms[1:])],
            i, j, at_list,
            root_dim=0,
            core_dim=0
        )
        # print(A_norms[1])
        # print("-"*50)
        A_expansion = prep_expanded_mats_from_cache(
            [(sign ** (n + 1)) * a for n, a in enumerate(A_expansion)], i, j, at_list,
            root_dim=0,
            core_dim=1
        )
        # A_raw = prep_expanded_mats_from_cache(A_raw, i, j, at_list,
        #                                       root_dim=0,
        #                                       core_dim=1
        #                                       )
        # if np.max(np.abs(A_raw[1] - A_base[1])) > 1e-12:
        #     print(A_raw[1])
        #     print(A_base[1])
        #     raise ValueError(sign, i, j, at_list)
        # A_norms2, A_expansion2 = td.vec_norm_unit_deriv(A_base, len(A_base))
        # if np.max(np.abs(A_norms[1] - A_norms2[1])) > 1e-12:
        #     print(A_norms[1])
        #     print(A_norms2[1])
        #     raise ValueError(sign, i, j, at_list)
        # if np.max(np.abs(A_norms[2] - A_norms2[2])) > 1e-12:
        #     print(A_norms[2])
        #     print(A_norms2[2])
        #     raise ValueError(sign, i, j, at_list)
        # if np.max(np.abs(A_expansion[1] - A_expansion2[1])) > 1e-12:
        #     print(A_expansion[1])
        #     print(A_expansion2[1])
        #     raise ValueError(sign, i, j, at_list)
        # if np.max(np.abs(A_expansion[2] - A_expansion2[2])) > 1e-12:
        #     print(A_expansion[2])
        #     print(A_expansion2[2])
        #     raise ValueError(sign, i, j, at_list)
        # # (A_norms, A_expansion) = (A_norms2, A_expansion2)
    return proj, (A_norms, A_expansion)

def vec_angle_derivs(a, b, order=1, up_vectors=None, zero_thresh=None, return_comps=False):
    """
    Returns the derivatives of the angle between `a` and `b` with respect to their components

    :param a: vector
    :type a: np.ndarray
    :param b: vector
    :type b: np.ndarray
    :param order: order of derivatives to go up to
    :type order: int
    :param zero_thresh: threshold for what is zero in a vector norm
    :type zero_thresh: float | None
    :return: derivative tensors
    :rtype: list
    """

    if order > 2:
        raise NotImplementedError("derivatives currently only up to order {}".format(2))

    derivs = []

    sin_derivs, cos_derivs = vec_sin_cos_derivs(a, b,
                                                up_vectors=up_vectors,
                                                order=order, zero_thresh=zero_thresh)
    # cos_expansion = [0] + [block_array(c, i+1) for i,c in enumerate(cos_derivs[1:])]
    # sin_expansion = [0] + [block_array(c, i+1) for i,c in enumerate(sin_derivs[1:])]
    # print(
    #     (cos_expansion[1][:, np.newaxis, np.newaxis] * sin_expansion[2][np.newaxis, :, :])[2][:3, :3]
    # )
    # print(
    #     (sin_expansion[1][:, np.newaxis, np.newaxis] * cos_expansion[2][np.newaxis, :, :])[2][:3, :3]
    # )

    s = sin_derivs[0]
    c = cos_derivs[0]

    q = np.arctan2(s, c)
    # # force wrapping if near to pi
    # if isinstance(q, np.ndarray):
    #     sel = np.abs(q) > np.pi - 1e-10
    #     q[sel] = np.abs(q[sel])
    # elif np.abs(q) > np.pi - 1e-10:
    #     q = np.abs(q)

    if up_vectors is not None:
        n = vec_crosses(a, b)
        if up_vectors.ndim < n.ndim:
            up_vectors = np.broadcast_to(up_vectors, n.shape[:-len(up_vectors.shape)] + up_vectors.shape)

        # zero_thresh = Options.norm_zero_threshold if zero_thresh is None else zero_thresh
        up = vec_dots(up_vectors, n)
        # up[np.abs(up) < zero_thresh] = 0.
        sign = np.sign(up)
    else:
        sign = np.ones(a.shape[:-1])

    if isinstance(sign, np.ndarray):
        sign[sign == 0] = 1.
    elif sign == 0:
        sign = np.array(1)

    derivs.append(sign*q)

    if order >= 1:
        # d = sin_derivs[1]
        # s_da = d[..., 0, :]; s_db = d[..., 1, :]
        # d = cos_derivs[1]
        # c_da = d[..., 0, :]; c_db = d[..., 1, :]
        #
        # q_da = c * s_da - s * c_da
        # q_db = c * s_db - s * c_db

        # we can do some serious simplification here
        # if we use some of the analytic work I've done
        # to write these in terms of the vector tangent
        # to the rotation

        a, na = vec_apply_zero_threshold(a, zero_thresh=zero_thresh)
        b, nb = vec_apply_zero_threshold(b, zero_thresh=zero_thresh)

        ha = a / na
        hb = b / nb

        ca = hb - (vec_dots(ha, hb)[..., np.newaxis]) * ha
        cb = ha - (vec_dots(hb, ha)[..., np.newaxis]) * hb

        ca, nca = vec_apply_zero_threshold(ca, zero_thresh=zero_thresh)
        cb, ncb = vec_apply_zero_threshold(cb, zero_thresh=zero_thresh)

        ca = ca / nca
        cb = cb / ncb

        q_da = -ca/na
        q_db = -cb/nb

        extra_dims = a.ndim - 1
        extra_shape = a.shape[:-1]

        d1 = (
            sign[np.newaxis, ..., np.newaxis] *
            np.array([q_da, q_db])
        )
        d1_reshape = tuple(range(1, extra_dims + 1)) + (0, extra_dims + 1)
        derivs.append(d1.transpose(d1_reshape))

    if order >= 2:

        d = sin_derivs[1]
        s_da = d[..., 0, :]; s_db = d[..., 1, :]
        d = cos_derivs[1]
        c_da = d[..., 0, :]; c_db = d[..., 1, :]

        d = sin_derivs
        s_daa = d[2][..., 0, 0, :, :]; s_dab = d[2][..., 0, 1, :, :]
        s_dba = d[2][..., 1, 0, :, :]; s_dbb = d[2][..., 1, 1, :, :]

        d = cos_derivs
        c_daa = d[2][..., 0, 0, :, :]; c_dab = d[2][..., 0, 1, :, :]
        c_dba = d[2][..., 1, 0, :, :]; c_dbb = d[2][..., 1, 1, :, :]

        c = c[..., np.newaxis]
        s = s[..., np.newaxis]
        q_daa = vec_outer(c_da, s_da) + c * s_daa - vec_outer(s_da, c_da) - s * c_daa
        q_dba = vec_outer(c_da, s_db) + c * s_dba - vec_outer(s_da, c_db) - s * c_dba
        q_dab = vec_outer(c_db, s_da) + c * s_dab - vec_outer(s_db, c_da) - s * c_dab
        q_dbb = vec_outer(c_db, s_db) + c * s_dbb - vec_outer(s_db, c_db) - s * c_dbb

        d2 = (
                sign[np.newaxis, np.newaxis, ..., np.newaxis, np.newaxis] *
                np.array([
                    [q_daa, q_dab],
                    [q_dba, q_dbb]
                ])
        )

        d2_reshape = tuple(range(2, extra_dims+2)) + (0, 1, extra_dims+2, extra_dims+3)

        derivs.append(
            d2.transpose(d2_reshape)
        )

    if return_comps:
        return derivs, (sin_derivs, cos_derivs)
    else:
        return derivs

def dist_deriv(coords, i, j, /, order=1, method='expansion', fixed_atoms=None,
               cache=None,
               expanded_vectors=None,
               reproject=True,
               zero_thresh=None):
    """
    Gives the derivative of the distance between i and j with respect to coords i and coords j

    :param coords:
    :type coords: np.ndarray
    :param i: index of one of the atoms
    :type i: int | Iterable[int]
    :param j: index of the other atom
    :type j: int | Iterable[int]
    :return: derivatives of the distance with respect to atoms i, j, and k
    :rtype: list
    """

    if method == 'expansion':
        proj, (base_deriv, _) = prep_unit_vector_expansion_from_cache(
            cache,
            coords, j, i, [i, j], fixed_atoms=fixed_atoms, expand=True
        )
        # proj, A_expansion = prep_disp_expansion(coords, j, i, [i, j], fixed_atoms=fixed_atoms, expand=True)
        # base_deriv = td.vec_norm_unit_deriv(A_expansion, order=order)[0]
        if proj is None: return base_deriv
        if reproject:
            base_deriv = [base_deriv[0]] + td.tensor_reexpand([proj], base_deriv[1:])
        return base_deriv
    else:

        if order > 2:
            raise NotImplementedError("derivatives currently only up to order {}".format(2))

        a = coords[..., j, :] - coords[..., i, :]
        d = vec_norm_derivs(a, order=order, zero_thresh=zero_thresh)

        derivs = []

        derivs.append(d[0])

        if order >= 1:
            da = d[1]
            derivs.append(np.array([-da, da]))

        if order >= 2:
            daa = d[2]
            # ii ij
            # ji jj
            derivs.append(np.array([
                [ daa, -daa],
                [-daa,  daa]
            ]))

        return derivs

def angle_deriv(coords, i, j, k, /, order=1, method='expansion',
                cache=None,
                angle_ordering='jik',
                fixed_atoms=None,
                expanded_vectors=None,
                reproject=True,
                zero_thresh=None
                ):
    """
    Gives the derivative of the angle between i, j, and k with respect to the Cartesians

    :param coords:
    :type coords: np.ndarray
    :param i: index of the central atom
    :type i: int | Iterable[int]
    :param j: index of one of the outside atoms
    :type j: int | Iterable[int]
    :param k: index of the other outside atom
    :type k: int | Iterable[int]
    :return: derivatives of the angle with respect to atoms i, j, and k
    :rtype: np.ndarray
    """

    if method == 'expansion':
        if expanded_vectors is None:
            expanded_vectors = [0, 1]
        if angle_ordering == 'ijk':
            proj, (A_norms, A_expansion) = prep_unit_vector_expansion_from_cache(
                cache,
                coords, i, j, [j, i, k], fixed_atoms=fixed_atoms, expand=0 in expanded_vectors
            )
            _, (B_norms, B_expansion) = prep_unit_vector_expansion_from_cache(
                cache,
                coords, k, j, [j, i, k], fixed_atoms=fixed_atoms, expand=1 in expanded_vectors
            )
        else:
            proj, (A_norms, A_expansion) = prep_unit_vector_expansion_from_cache(
                cache,
                coords, j, i, [i, j, k], fixed_atoms=fixed_atoms, expand=0 in expanded_vectors
            )
            _, (B_norms, B_expansion) = prep_unit_vector_expansion_from_cache(
                cache,
                coords, k, i, [i, j, k], fixed_atoms=fixed_atoms, expand=1 in expanded_vectors
            )

        # A_expansion = [A_expansion[0], np.concatenate([np.eye(3), np.zeros((3, 3))], axis=0)]
        # B_expansion = [B_expansion[0], np.concatenate([np.zeros((3, 3)), np.eye(3)], axis=0)]
        base_deriv = td.vec_angle_deriv(A_expansion, B_expansion, order=order, unitized=True)
        if proj is None: return base_deriv
        if reproject:
            base_deriv = [base_deriv[0]] + td.tensor_reexpand([proj], base_deriv[1:])
        return base_deriv
    else:
        if angle_ordering == 'ijk':
            # derivs = angle_deriv(coords, j, i, k, order=order, angle_ordering='jik',
            #                      method=method,
            #                      fixed_atoms=fixed_atoms,
            #                      expanded_vectors=expanded_vectors,
            #                      zero_thresh=zero_thresh
            #                      )
            # change signs if necessary
            raise NotImplementedError('too annoying')


        if order > 2:
            raise NotImplementedError("derivatives currently only up to order {}".format(2))

        a = coords[..., j, :] - coords[..., i, :]
        b = coords[..., k, :] - coords[..., i, :]
        d = vec_angle_derivs(a, b, order=order, zero_thresh=zero_thresh)

        derivs = []

        base_shape = coords.shape[:-2]
        derivs.append(d[0].reshape(base_shape))

        if order >= 1:
            da = d[1][..., 0, :]; db = d[1][..., 1, :]
            derivs.append(np.array([-(da + db), da, db]))

        if order >= 2:
            daa = d[2][..., 0, 0, :, :]; dab = d[2][..., 0, 1, :, :]
            dba = d[2][..., 1, 0, :, :]; dbb = d[2][..., 1, 1, :, :]
            # ii ij ik
            # ji jj jk
            # ki kj kk
            derivs.append(np.array([
                [daa + dba + dab + dbb, -(daa + dab), -(dba + dbb)],
                [         -(daa + dba),          daa,   dba       ],
                [         -(dab + dbb),          dab,   dbb       ]
            ]))

        return derivs

def rock_deriv(coords, i, j, k, /, order=1, method='expansion', angle_ordering='ijk', zero_thresh=None, fixed_atoms=None, expanded_vectors=None):
    """
    Gives the derivative of the rocking motion (symmetric bend basically)

    :param coords:
    :type coords: np.ndarray
    :param i: index of the central atom
    :type i: int | Iterable[int]
    :param j: index of one of the outside atoms
    :type j: int | Iterable[int]
    :param k: index of the other outside atom
    :type k: int | Iterable[int]
    :return: derivatives of the angle with respect to atoms i, j, and k
    :rtype: np.ndarray
    """


    if method == 'expansion':
        if expanded_vectors is None:
            expanded_vectors = [0, 1]

        if angle_ordering == 'ijk':
            proj, A_expansion = prep_disp_expansion(coords, i, j, [i, j, k], fixed_atoms=fixed_atoms, expand=0 in expanded_vectors)
            _, B_expansion = prep_disp_expansion(coords, k, j, [i, j, k], fixed_atoms=fixed_atoms, expand=1 in expanded_vectors)
        else:
            proj, A_expansion = prep_disp_expansion(coords, j, i, [i, j, k], fixed_atoms=fixed_atoms, expand=0 in expanded_vectors)
            _, B_expansion = prep_disp_expansion(coords, k, i, [i, j, k], fixed_atoms=fixed_atoms, expand=1 in expanded_vectors)

        A_deriv = td.vec_angle_deriv(A_expansion, B_expansion[:1], order=order)
        B_deriv = td.vec_angle_deriv(A_expansion[:1], B_expansion, order=order)
        base_deriv = [A_deriv[0]] + [ad - bd for ad,bd in zip(A_deriv[1:], B_deriv[1:])]
        if proj is None: return base_deriv
        return [base_deriv[0]] + td.tensor_reexpand([proj], base_deriv[1:])

    else:

        if angle_ordering == 'ijk':
            raise NotImplementedError("too annoying")

        if order > 2:
            raise NotImplementedError("derivatives currently only up to order {}".format(2))
        a = coords[..., j, :] - coords[..., i, :]
        b = coords[..., k, :] - coords[..., i, :]

        d = vec_angle_derivs(a, b, order=order, zero_thresh=zero_thresh)

        derivs = []

        derivs.append(d[0])

        if order >= 1:
            da = d[1][..., 0, :]; db = d[1][..., 1, :]
            derivs.append(np.array([-(da - db), da, -db]))

        if order >= 2:
            daa = d[2][..., 0, 0, :, :]; dab = d[2][..., 0, 1, :, :]
            dba = d[2][..., 1, 0, :, :]; dbb = d[2][..., 1, 1, :, :]
            # ii ij ik
            # ji jj jk
            # ki kj kk
            derivs.append(np.array([
                [daa + dba + dab + dbb, -(daa + dab), -(dba + dbb)],
                [         -(daa + dba),          daa,   dba       ],
                [         -(dab + dbb),          dab,   dbb       ]
            ]))

        return derivs

def dihed_deriv(coords, i, j, k, l, /, order=1, zero_thresh=None, method='expansion',
                fixed_atoms=None,
                cache=None,
                reproject=True,
                expanded_vectors=None):
    """
    Gives the derivative of the dihedral between i, j, k, and l with respect to the Cartesians
    Currently gives what are sometimes called the `psi` angles.
    Can also support more traditional `phi` angles by using a different angle ordering

    :param coords:
    :type coords: np.ndarray
    :param i:
    :type i: int | Iterable[int]
    :param j:
    :type j: int | Iterable[int]
    :param k:
    :type k: int | Iterable[int]
    :param l:
    :type l: int | Iterable[int]
    :return: derivatives of the dihedral with respect to atoms i, j, k, and l
    :rtype: np.ndarray
    """

    if method == 'expansion':
        if expanded_vectors is None:
            expanded_vectors = [0, 1, 2]
        proj, A_expansion = prep_disp_expansion(coords, j, i, [i, j, k, l], fixed_atoms=fixed_atoms, expand=0 in expanded_vectors)
        _, (B_norms, B_expansion) = prep_unit_vector_expansion_from_cache(
            cache,
            coords, j, k, [i, j, k, l], fixed_atoms=fixed_atoms, expand=1 in expanded_vectors
        )
        _, C_expansion = prep_disp_expansion(coords, l, k, [i, j, k, l], fixed_atoms=fixed_atoms, expand=2 in expanded_vectors)
        base_deriv = td.vec_dihed_deriv(A_expansion, B_expansion, C_expansion,
                                        B_norms=B_norms,
                                        order=order)
        if proj is None: return base_deriv
        if reproject:
            base_deriv = [base_deriv[0]] + td.tensor_reexpand([proj], base_deriv[1:])
        return base_deriv

    else:
        if fixed_atoms is not None:
            raise NotImplementedError("direct derivatives with specified fixed atoms not implemented")
        if order > 2:
            raise NotImplementedError("derivatives currently only up to order {}".format(2))

        a = coords[..., j, :] - coords[..., i, :]
        b = coords[..., k, :] - coords[..., j, :]
        c = coords[..., l, :] - coords[..., k, :]

        n1 = vec_crosses(a, b)
        n2 = vec_crosses(b, c)

        # coll = vec_crosses(n1, n2)
        # coll_norms = vec_norms(coll)
        # bad = coll_norms < 1.e-17
        # if bad.any():
        #     raise Exception([
        #         bad,
        #         i, j, k, l,
        #         a[bad], b[bad], c[bad]])

        # zero_thresh = Options.norm_zero_threshold if zero_thresh is None else zero_thresh

        cnb = vec_crosses(n1, n2)

        cnb, n_cnb, bad_friends = vec_apply_zero_threshold(cnb, zero_thresh=zero_thresh, return_zeros=True)
        bad_friends = bad_friends.reshape(cnb.shape[:-1])
        orient = vec_dots(b, cnb)
        # orient[np.abs(orient) < 1.0] = 0.
        sign = np.sign(orient)

        d, (sin_derivs, cos_derivs) = vec_angle_derivs(n1, n2, order=order,
                                                       up_vectors=vec_normalize(b),
                                                       zero_thresh=zero_thresh, return_comps=True)

        derivs = []

        base_shape = coords.shape[:-2]
        derivs.append(d[0].reshape(base_shape))

        if order >= 1:
            dn1 = d[1][..., 0, :]; dn2 = d[1][..., 1, :]
            if dn1.ndim == 1:
                if bad_friends:
                    dn1 = sin_derivs[1][0]
                    dn2 = sin_derivs[1][1]
                    sign = np.array(1)
            else:
                dn1[bad_friends] = sin_derivs[1][bad_friends, 0, :] # TODO: clean up shapes I guess...
                dn2[bad_friends] = sin_derivs[1][bad_friends, 1, :]
                sign[bad_friends] = 1

            di = vec_crosses(b, dn1)
            dj = vec_crosses(c, dn2) - vec_crosses(a+b, dn1)
            dk = vec_crosses(a, dn1) - vec_crosses(b+c, dn2)
            dl = vec_crosses(b, dn2)

            deriv_tensors = sign[np.newaxis, ..., np.newaxis]*np.array([di, dj, dk, dl])

            # if we have problem points we deal with them via averaging
            # over tiny displacements since the dihedral derivative is
            # continuous
            # if np.any(bad_friends):
            #     raise NotImplementedError("planar dihedral angles remain an issue for me...")
            #     if coords.ndim > 2:
            #         raise NotImplementedError("woof")
            #     else:
            #         bad_friends = bad_friends.flatten()
            #         bad_i = i[bad_friends]
            #         bad_j = j[bad_friends]
            #         bad_k = k[bad_friends]
            #         bad_l = l[bad_friends]
            #         bad_coords = np.copy(coords)
            #         if isinstance(i, (int, np.integer)):
            #             raise NotImplementedError("woof")
            #         else:
            #             # for now we do this with finite difference...
            #             for which,(bi,bj,bk,bl) in enumerate(zip(bad_i, bad_j, bad_k, bad_l)):
            #                 for nat,at in enumerate([bi, bj, bk, bl]):
            #                     for x in range(3):
            #                         bad_coords[at, x] += zero_point_step_size
            #                         d01, = dihed_deriv(bad_coords, bi, bj, bk, bl, order=0, zero_thresh=-1.0)
            #                         bad_coords[at, x] -= 2*zero_point_step_size
            #                         d02, = dihed_deriv(bad_coords, bi, bj, bk, bl, order=0, zero_thresh=-1.0)
            #                         bad_coords[at, x] += zero_point_step_size
            #                         deriv_tensors[nat, which, x] = (d01[0] + d02[0])/(2*zero_point_step_size)
            #                         # print(
            #                         #     "D1", d1[nat, x]
            #                         #
            #                         # )
            #                         # print(
            #                         #     "D2", d2[nat, x]
            #                         #
            #                         # )
            #                         # print("avg", (d1[nat, x] + d2[nat, x])/2)
            #                         # print("FD", (d01[0], d02[0]))#/(2*zero_point_step_size))
            #                         # raise Exception(
            #                         #  "wat",
            #                         #     di,
            #                         # d01.shape
            #                         # )

            derivs.append(deriv_tensors)


        if order >= 2:

            d11 = d[2][..., 0, 0, :, :]; d12 = d[2][..., 0, 1, :, :]
            d21 = d[2][..., 1, 0, :, :]; d22 = d[2][..., 1, 1, :, :]

            # explicit write out of chain-rule transformations to isolate different Kron-delta terms
            extra_dims = a.ndim - 1
            extra_shape = a.shape[:-1]
            dot = lambda x, y, axes=(-1, -2) : vec_tensordot(x, y, axes=axes, shared=extra_dims)
            if extra_dims > 0:
                e3 = np.broadcast_to(pops.levi_cevita3,  extra_shape + pops.levi_cevita3.shape)
            else:
                e3 = pops.levi_cevita3

            Ca = dot(e3, a, axes=[-1, -1])
            Cb = dot(e3, b, axes=[-1, -1])
            Cc = dot(e3, c, axes=[-1, -1])
            Cab = Ca+Cb
            Cbc = Cb+Cc

            CaCa, CaCb, CaCc, CaCab, CaCbc = [dot(Ca, x) for x in (Ca, Cb, Cc, Cab, Cbc)]
            CbCa, CbCb, CbCc, CbCab, CbCbc = [dot(Cb, x) for x in (Ca, Cb, Cc, Cab, Cbc)]
            CcCa, CcCb, CcCc, CcCab, CcCbc = [dot(Cc, x) for x in (Ca, Cb, Cc, Cab, Cbc)]
            CabCa, CabCb, CabCc, CabCab, CabCbc = [dot(Cab, x) for x in (Ca, Cb, Cc, Cab, Cbc)]
            CbcCa, CbcCb, CbcCc, CbcCab, CbcCbc = [dot(Cbc, x) for x in (Ca, Cb, Cc, Cab, Cbc)]

            dii = dot(CbCb, d11)
            dij = dot(CcCb, d12) - dot(CabCb, d11)
            dik = dot(CaCb, d11) - dot(CbcCb, d12)
            dil = dot(CbCb, d12)

            dji = dot(CbCc, d21) - dot(CbCab, d11)
            djj = dot(CabCab, d11) - dot(CabCc, d21) - dot(CcCab, d12) + dot(CcCc, d22)
            djk = dot(CbcCab, d12) - dot(CbcCc, d22) - dot(CaCab, d11) + dot(CaCc, d21)
            djl = dot(CbCc, d22) - dot(CbCab, d12)

            dki = dot(CbCa, d11) - dot(CbCbc, d21)
            dkj = dot(CabCbc, d21) - dot(CcCbc, d22) - dot(CabCa, d11) + dot(CcCa, d12)
            dkk = dot(CaCa, d11) - dot(CaCbc, d21) - dot(CbcCa, d12) + dot(CbcCbc, d22)
            dkl = dot(CbCa, d12) - dot(CbCbc, d22)

            dli = dot(CbCb, d21)
            dlj = dot(CcCb, d22) - dot(CabCb, d21)
            dlk = dot(CaCb, d21) - dot(CbcCb, d22)
            dll = dot(CbCb, d22)

            derivs.append(
                -sign[np.newaxis, np.newaxis, ..., np.newaxis, np.newaxis] *
                np.array([
                    [dii, dij, dik, dil],
                    [dji, djj, djk, djl],
                    [dki, dkj, dkk, dkl],
                    [dli, dlj, dlk, dll]
                ])
            )

    return derivs

def book_deriv(coords, i, j, k, l, /, order=1, zero_thresh=None, method='expansion',
               fixed_atoms=None,
               expanded_vectors=None):
    if method == 'expansion':
        if expanded_vectors is None:
            expanded_vectors = [0, 1, 2]
        proj, A_expansion = prep_disp_expansion(coords, j, i, [i, j, k, l], fixed_atoms=fixed_atoms, expand=0 in expanded_vectors)
        _, B_expansion = prep_disp_expansion(coords, k, j, [i, j, k, l], fixed_atoms=fixed_atoms, expand=1 in expanded_vectors)
        _, C_expansion = prep_disp_expansion(coords, l, j, [i, j, k, l], fixed_atoms=fixed_atoms, expand=2 in expanded_vectors)

        base_deriv = td.vec_dihed_deriv(A_expansion, B_expansion, C_expansion, order=order)
        if proj is None: return base_deriv
        return [base_deriv[0]] + td.tensor_reexpand([proj], base_deriv[1:])
    else:
        raise NotImplementedError("too annoying")

def oop_deriv(coords, i, j, k, /, order=1, method='expansion',
               fixed_atoms=None,
               expanded_vectors=None):
    if method == 'expansion':
        if fixed_atoms is None: fixed_atoms = []
        fixed_atoms = list(fixed_atoms) + [j]
        if expanded_vectors is None:
            expanded_vectors = [0, 1]
        proj, A_expansion = prep_disp_expansion(coords, j, i, [i, j, k], fixed_atoms=fixed_atoms, expand=0 in expanded_vectors)
        _, B_expansion = prep_disp_expansion(coords, k, j, [i, j, k], fixed_atoms=fixed_atoms, expand=1 in expanded_vectors)
        _, C_expansion = prep_disp_expansion(coords, i, k, [i, j, k], fixed_atoms=fixed_atoms, expand=2 in expanded_vectors)

        base_deriv = td.vec_dihed_deriv(A_expansion, B_expansion, C_expansion, order=order)
        if proj is None: return base_deriv
        return [base_deriv[0]] + td.tensor_reexpand([proj], base_deriv[1:])
    else:
        raise NotImplementedError("too annoying")

def plane_angle_deriv(coords, i, j, k, l, m, n, /, order=1,
                      method='expansion',
                      fixed_atoms=None,
                      expanded_vectors=None,

                      ):
    if method == 'expansion':
        if expanded_vectors is None:
            expanded_vectors = [0, 1, 2, 3]
        proj, A_expansion = prep_disp_expansion(coords, j, i, [i, j, k, l, m], fixed_atoms=fixed_atoms, expand=0 in expanded_vectors)
        _, B_expansion = prep_disp_expansion(coords, k, j, [i, j, k, l, m], fixed_atoms=fixed_atoms, expand=1 in expanded_vectors)
        _, C_expansion = prep_disp_expansion(coords, m, l, [i, j, k, l, m], fixed_atoms=fixed_atoms, expand=2 in expanded_vectors)
        _, D_expansion = prep_disp_expansion(coords, n, m, [i, j, k, l, m], fixed_atoms=fixed_atoms, expand=3 in expanded_vectors)

        base_deriv = td.vec_plane_angle_deriv(A_expansion, B_expansion, C_expansion, D_expansion, order=order)
        if proj is None: return base_deriv
        return [base_deriv[0]] + td.tensor_reexpand([proj], base_deriv[1:])
    else:
        raise NotImplementedError("too annoying")

def wag_deriv(coords, i, j, k, l=None, m=None, n=None, /, order=1, method='expansion',
               fixed_atoms=None,
               expanded_vectors=None):
    if method == 'expansion':
        if fixed_atoms is None: fixed_atoms = []
        fixed_atoms = list(fixed_atoms) + [j]
        if expanded_vectors is None:
            expanded_vectors = [0, 1]
        if l is None: l = i
        if m is None: m = j
        if n is None: n = k
        proj, A_expansion = prep_disp_expansion(coords, j, i, [i, j, k, l, m, n], fixed_atoms=fixed_atoms, expand=0 in expanded_vectors)
        _, B_expansion = prep_disp_expansion(coords, k, j, [i, j, k, l, m, n], fixed_atoms=fixed_atoms, expand=1 in expanded_vectors)
        _, C_expansion = prep_disp_expansion(coords, m, l, [i, j, k, l, m, n], fixed_atoms=fixed_atoms, expand=2 in expanded_vectors)
        _, D_expansion = prep_disp_expansion(coords, n, m, [i, j, k, l, m, n], fixed_atoms=fixed_atoms, expand=2 in expanded_vectors)

        i_deriv = td.vec_dihed_deriv(A_expansion, B_expansion[:1], C_expansion, order=order)
        k_deriv = td.vec_dihed_deriv(A_expansion[:1], B_expansion, C_expansion, order=order)
        base_deriv = [i_deriv[0]] + [ad - bd for ad, bd in zip(i_deriv[1:], k_deriv[1:])]
        if proj is None: return base_deriv
        return [base_deriv[0]] + td.tensor_reexpand([proj], base_deriv[1:])
    else:
        raise NotImplementedError("too annoying")

def transrot_deriv(coords, *pos, order=1, masses=None, return_rot=True, return_frame=False, fixed_atoms=None):
    coords = np.asanyarray(coords)
    if len(pos) > 0:
        if masses is not None:
            masses = np.asanyarray(masses)[pos,]
        subcoords = coords[..., pos, :]
    else:
        subcoords = coords
    (com, eigs), axes = frames.translation_rotation_eigenvectors(
        subcoords,
        masses,
        mass_weighted=False,
        return_com=True,
        return_rot=return_rot,
        return_principle_axes=True
    )

    nc = com.shape[-1]
    expansion = [com]
    if order > 0:
        n = coords.shape[-2] * 3
        if len(pos) > 0:
            subpos = (np.asanyarray(pos)[:, np.newaxis] * 3 + np.arange(3)[np.newaxis, :]).flatten()
            _ = np.zeros(coords.shape[:-2] + (n, nc))
            _[..., subpos, :] = eigs
            eigs = _
        if fixed_atoms is not None:
            fixed_pos = (np.asanyarray(fixed_atoms)[:, np.newaxis] * 3 + np.arange(3)[np.newaxis, :]).flatten()
            eigs[..., fixed_pos, :] = 0
        expansion.append(eigs)

        for o in range(1, order):
            # is this right? I guess probably given the form of the rotation generator...
            expansion.append(
                np.zeros(coords.shape[:-2] + (n,) * (o+1) + (nc,))
            )

    if return_frame:
        return expansion, axes
    else:
        return expansion

def com_dist_deriv(coords, frame_pos_1, frame_pos_2, *, order=1, masses=None, fixed_atoms=None):
    #TODO: could also include the com vec if that was useful...
    coords = np.asanyarray(coords)
    com_deriv1 = transrot_deriv(coords, *frame_pos_1, masses=masses, order=order,
                             return_rot=False,
                             fixed_atoms=fixed_atoms)
    com_deriv2 = transrot_deriv(coords, *frame_pos_2, masses=masses, order=order,
                             return_rot=False,
                             fixed_atoms=fixed_atoms)

    #TODO: restrict the number of displaced positions for efficiency
    disp_exp = [cd1 - cd2 for cd1, cd2 in zip(com_deriv1, com_deriv2)]

    norm_deriv, _ = td.vec_norm_unit_deriv(disp_exp, order=order)
    return norm_deriv

def moment_of_inertia_expansion_deriv(coords, *pos, order=1, masses=None, fixed_atoms=None):
    coords = np.asanyarray(coords)
    if len(pos) > 0:
        if masses is not None:
            masses = np.asanyarray(masses)[pos,]
        subcoords = coords[..., pos, :]
    else:
        subcoords = coords
    vals, vecs = frames.moments_of_inertia_expansion(subcoords, order=order, masses=masses, mass_weighted=False)
    if len(pos) > 0 and order > 0:
        val_expansion = [vals[0]]
        vec_expansion = [vecs[0]]

        n = coords.shape[-2] * 3
        subpos = (np.asanyarray(pos)[:, np.newaxis] * 3 + np.arange(3)[np.newaxis, :]).flatten()
        for i,(val_set, vec_set) in enumerate(zip(vals[1:], vecs[1:])):
            new_vals = np.zeros(val_set.shape[:-(i+2)] + (n,)*(i+1) + val_set.shape[-1:])
            idx = (...,) + np.ix_(*[subpos]*(i+1)) + (slice(None),)
            new_vals[idx] = val_set
            val_expansion.append(new_vals)

            new_vecs = np.zeros(vec_set.shape[:-(i+3)] + (n,)*(i+1) + vec_set.shape[-2:])
            idx = (...,) + np.ix_(*[subpos]*(i+1)) + (slice(None), slice(None),)
            new_vecs[idx] = vec_set
            vec_expansion.append(new_vecs)

        vals = val_expansion
        vecs = vec_expansion

    if fixed_atoms is not None:
        subpos = (np.asanyarray(fixed_atoms)[:, np.newaxis] * 3 + np.arange(3)[np.newaxis, :]).flatten()
        for i, (val_set, vec_set) in enumerate(zip(vals[1:], vecs[:1])):
            idx = (...,) + np.ix_(*[subpos] * (i + 1)) + (slice(None),)
            val_set[idx] = 0

            idx = (...,) + np.ix_(*[subpos] * (i + 1)) + (slice(None),)
            vec_set[idx] = 0

    return vals, vecs

def _frame_data(coords, *pos, masses=None):
    coords = np.asanyarray(coords)
    if len(pos) > 0:
        if masses is not None:
            masses = np.asanyarray(masses)[pos,]
        subcoords = coords[..., pos, :]
    else:
        subcoords = coords
    return frames.moments_of_inertia(subcoords, masses=masses, return_com=True)

def orientation_deriv(coords, frame_pos_1, frame_pos_2, *, order=1, masses=None,
                      fixed_atoms=None,
                      return_frame=False
                      ):
    #TODO: could also include the com vec if that was useful...
    coords = np.asanyarray(coords)
    disps1, axes1 = transrot_deriv(coords, *frame_pos_1,
                                   order=order,
                                   masses=masses,
                                   fixed_atoms=fixed_atoms,
                                   return_frame=True
                                   )
    disps2, axes2 = transrot_deriv(coords, *frame_pos_2,
                                   order=order,
                                   masses=masses,
                                   fixed_atoms=fixed_atoms,
                                   return_frame=True
                                   )

    angle_expansion = []
    for i in range(3):
        vecs1 = [axes1[..., i]]
        for d in disps1[1:]:
            base_vec = d[..., 3+i]
            new_tensor = np.zeros(base_vec.shape + (3,))
            new_tensor[..., ::3, 0] = base_vec[..., ::3]
            new_tensor[..., 1::3, 1] = base_vec[..., 1::3]
            new_tensor[..., 2::3, 2] = base_vec[..., 2::3]
            vecs1.append(new_tensor)

        vecs2 = [axes2[..., i]]
        for d in disps2[1:]:
            base_vec = d[:, 3+i]
            new_tensor = np.zeros(base_vec.shape + (3,))
            new_tensor[..., ::3, 0] = base_vec[..., ::3]
            new_tensor[..., 1::3, 1] = base_vec[..., 1::3]
            new_tensor[..., 2::3, 2] = base_vec[..., 2::3]
            vecs2.append(new_tensor)

        angle_expansion.append(
            td.vec_angle_deriv(
                vecs1,
                vecs2,
                up_vector=axes1[..., (i+2)%3],
                order=order
            )
        )

    xyz_expansion = [
        (cd1[..., :3] - cd2[..., :3])
        for cd1, cd2 in zip(disps1, disps2)
    ]

    total_expansion = [
        np.concatenate([xyz, a[..., np.newaxis], b[..., np.newaxis], c[..., np.newaxis]], axis=-1)
        for a,b,c,xyz in zip(*angle_expansion, xyz_expansion)
    ]

    if return_frame:
        return total_expansion, ((disps1[0], axes1), (disps2[0], axes2))
    else:
        return total_expansion

def _pop_bond_vecs(bond_tf, i, j, coords):
    bond_vectors = np.zeros(coords.shape)
    bond_vectors[..., i, :] = bond_tf[0]
    bond_vectors[..., j, :] = bond_tf[1]

    return bond_vectors.reshape(
        coords.shape[:-2] + (coords.shape[-2] * coords.shape[-1],)
    )
def _fill_derivs(coords, idx, derivs, method='old'):
    vals = []
    # nx = np.prod(coords.shape, dtype=int)
    nats = coords.shape[-2]
    subpos = (np.array(idx)[:, np.newaxis] * 3 + np.arange(3)[np.newaxis, :]).flatten()
    base_shape = coords.shape[:-2]
    for n, d in enumerate(derivs):
        if n == 0:
            vals.append(d)
            continue
        if method == 'old':
            tensor = np.zeros((nats, 3) * n)
            for pos in itertools.product(*[range(len(idx)) for _ in range(n)]):
                actual = ()
                for r in pos:
                    actual += (slice(None) if idx[r] is None else idx[r], slice(None))
                tensor[actual] = d[pos]
        else:
            tensor = np.zeros(base_shape + (nats*3,) * n)
            block = np.ix_(*[subpos] * n)
            idx = (...,) + block #+ (slice(None),)*core_dim
            tensor[idx] = d
        vals.append(tensor.reshape(base_shape + (nats * 3,) * n))
    return vals
def dist_vec(coords, i, j, order=None, method='expansion', cache=None, reproject=True, fixed_atoms=None):
    """
    Returns the full vectors that define the linearized version of a bond displacement

    :param coords:
    :param i:
    :param j:
    :return:
    """

    derivs = dist_deriv(coords, i, j, method=method, order=(1 if order is None else order),
                        cache=cache,
                        reproject=reproject,
                        fixed_atoms=fixed_atoms)
    if reproject and method == 'expansion':
        return derivs[1] if order is None else derivs
    else:
        if order is None:
            return _pop_bond_vecs(derivs[1], i, j, coords)
        else:
            return _fill_derivs(coords, (i,j), derivs, method=method)

def angle_vec(coords, i, j, k, order=None, method='expansion', angle_ordering='ijk',
              cache=None, reproject=True, fixed_atoms=None):
    """
    Returns the full vectors that define the linearized version of an angle displacement

    :param coords:
    :param i:
    :param j:
    :return:
    """

    if method != "expansion" and angle_ordering == 'ijk':
        i, j, k = j, i, k
        angle_ordering = 'jik'
    derivs = angle_deriv(coords, i, j, k, order=(1 if order is None else order), method=method,
                         cache=cache,
                         reproject=reproject,
                         angle_ordering=angle_ordering,
                         fixed_atoms=fixed_atoms)
    if reproject and method == 'expansion':
        return derivs[1] if order is None else derivs
    else:
        if angle_ordering == 'ijk':
            full = _fill_derivs(coords, (j, i, k), derivs, method=method)
        else:
            full = _fill_derivs(coords, (i, j, k), derivs, method=method)
        if order is None:
            return full[1]
        else:
            return full

def rock_vec(coords, i, j, k, order=None, method='expansion', fixed_atoms=None):
    """
    Returns the full vectors that define the linearized version of an angle displacement

    :param coords:
    :param i:
    :param j:
    :return:
    """

    derivs = rock_deriv(coords, i, j, k, order=(1 if order is None else order), fixed_atoms=fixed_atoms, method=method)
    if method == 'expansion':
        return derivs[1] if order is None else derivs
    else:
        full = _fill_derivs(coords, (i, j, k), derivs)
        if order is None:
            return full[1]
        else:
            return full

def dihed_vec(coords, i, j, k, l, order=None, method='expansion', cache=None, reproject=True, fixed_atoms=None):
    """
    Returns the full vectors that define the linearized version of a dihedral displacement

    :param coords:
    :param i:
    :param j:
    :return:
    """
    derivs = dihed_deriv(coords, i, j, k, l, method=method, order=(1 if order is None else order),
                         cache=cache,
                         reproject=reproject,
                         fixed_atoms=fixed_atoms)
    if reproject and method == 'expansion':
        return derivs[1] if order is None else derivs
    else:
        full = _fill_derivs(coords, (i, j, k, l), derivs, method=method)
        if order is None:
            return full[1]
        else:
            return full

def book_vec(coords, i, j, k, l, order=None, method='expansion', fixed_atoms=None):
    """
    Returns the full vectors that define the linearized version of a dihedral displacement

    :param coords:
    :param i:
    :param j:
    :return:
    """

    if method == 'expansion':
        derivs = book_deriv(coords, i, j, k, l, method=method, order=(1 if order is None else order), fixed_atoms=fixed_atoms)
        return derivs[1] if order is None else derivs
    else:
        derivs = dihed_deriv(coords, j, k, i, l, order=(1 if order is None else order), method=method,
                             fixed_atoms=fixed_atoms)
        full = _fill_derivs(coords, (i, j, k, l), derivs)
        if order is None:
            return full[1]
        else:
            return full

def oop_vec(coords, i, j, k, order=None, method='expansion', fixed_atoms=None):
    """
    Returns the full vectors that define the linearized version of an oop displacement

    :param coords:
    :param i:
    :param j:
    :return:
    """

    if method == 'expansion':
        derivs = oop_deriv(coords, i, j, k, order=(1 if order is None else order), method=method, fixed_atoms=fixed_atoms)
        return derivs[1] if order is None else derivs
    else:
        dihed_tf = dihed_deriv(coords, i, k, j, i, order=(1 if order is None else order), method=method,
                               fixed_atoms=fixed_atoms,
                               expanded_vectors=[0]
                               )
        full = _fill_derivs(coords, (i, j, k, None), dihed_tf)
        if order is None:
            return full[1]
        else:
            return full
        # if order is not None and order > 1:
        #     raise NotImplementedError("OOP deriv reshaping not done yet")
        # else:
        #     dihed_tf = dihed_tf[1]
        # dihed_vectors = np.zeros(coords.shape)
        # dihed_vectors[..., i, :] = dihed_tf[0]
        # dihed_vectors[..., j, :] = dihed_tf[1]
        # dihed_vectors[..., k, :] = dihed_tf[2]
        #
        # return dihed_vectors.reshape(
        #     coords.shape[:-2] + (coords.shape[-2] * coords.shape[-1],)
        # )

def wag_vec(coords, i, j, k, order=None, method='expansion', fixed_atoms=None):
    """
    Returns the full vectors that define the linearized version of an oop displacement

    :param coords:
    :param i:
    :param j:
    :return:
    """

    if method == 'expansion':
        derivs = wag_deriv(coords, i, j, k, order=(1 if order is None else order), method=method, fixed_atoms=fixed_atoms)
        return derivs[1] if order is None else derivs
    else:
        raise NotImplementedError("too annoying")

coord_type_map = {
    'dist':dist_vec,
    'bend':angle_vec,
    'rock':rock_vec,
    'dihed':dihed_vec,
    'book':book_vec,
    'oop':oop_vec,
    'wag':wag_vec
}
def internal_conversion_specs(specs, angle_ordering='ijk', coord_type_dispatch=None, **opts):
    if coord_type_dispatch is None:
        coord_type_dispatch = coord_type_map
    targets = []
    for idx in specs:
        if isinstance(idx, dict):
            for k in coord_type_dispatch.keys():
                if k in idx:
                    coord_type = k
                    subopts = idx.copy()
                    idx = idx[k]
                    del subopts[k]
                    break
            else:
                raise ValueError("can't parse coordinate spec {}".format(idx))
        else:
            nidx = len(idx)
            if nidx == 2:
                coord_type = 'dist'
            elif nidx == 3:
                coord_type = 'bend'
            elif nidx == 4:
                coord_type = 'dihed'
            else:
                raise ValueError("can't parse coordinate spec {}".format(idx))
            subopts = {}

        if coord_type in {'bend', 'rock'}: # very common to change
            subopts['angle_ordering'] = subopts.get('angle_ordering', angle_ordering)
        targets.append((coord_type_dispatch[coord_type], idx, dict(opts, **subopts)))

    return targets

def internal_conversion_function(specs,
                                 base_transformation=None,
                                 reference_internals=None,
                                 use_cache=True,
                                 reproject=False,
                                 **opts):
    base_specs = internal_conversion_specs(specs, **opts)
    def convert(coords, order=None,
                use_cache=use_cache,
                reference_internals=reference_internals, base_transformation=base_transformation):
        targets = []
        #
        if use_cache:
            cache = {}
        else:
            cache = None
        for f, idx, subopts in base_specs:
            res = f(coords, *idx, **dict(subopts, reproject=reproject, cache=cache, order=order))
            targets.append(res)

        if order is None:
            base = np.moveaxis(np.array(targets), 0, -1)
            if base_transformation is not None:
                base = td.tensor_reexpand(base, base_transformation) # del_XR * del_RQ
        else:
            base = [
                np.moveaxis(np.array(t), 0, -1)
                for t in zip(*targets)
            ]
            internals, expansion = base[0], base[1:]
            if reference_internals is not None:
                if reference_internals.ndim == 1 and internals.ndim > 1:
                    reference_internals = np.expand_dims(reference_internals, list(range(internals.ndim - 1)))
                internals = internals - reference_internals
            if base_transformation is not None:
                if base_transformation[0].ndim == 2 and len(expansion) > 0 and expansion[0].ndim > 2:
                    base_transformation = [
                        np.broadcast_to(
                            np.expand_dims(b, list(range(expansion[0].ndim - 2))),
                            expansion[0].shape[:-2] + b.shape
                        ) for b in base_transformation
                    ]
                internals = (internals[..., np.newaxis, :] @ base_transformation[0]).reshape(
                    internals.shape[:-1] + base_transformation[0].shape[-1:]
                )
                expansion = (
                    td.tensor_reexpand(expansion, base_transformation, order=len(expansion))
                        if len(expansion) > 0 else
                    expansion
                )
            base = [internals] + expansion
        return base
    return convert


def internal_coordinate_tensors(coords, specs, order=None, return_inverse=False, masses=None,
                                fixed_atoms=None,
                                fixed_cartesians=None,
                                fixed_coords=None,
                                remove_inverse_translation_rotation=True,
                                **opts):
    coords = np.asanyarray(coords)
    base_tensors = internal_conversion_function(specs, **opts)(
        coords,
        order=order
    )
    if order is None:
        bt = [base_tensors]
    else:
        bt = base_tensors[1:]
    bt = prep_internal_derivatives(bt,
                                   fixed_atoms=fixed_atoms,
                                   fixed_cartesians=fixed_cartesians,
                                   fixed_coords=fixed_coords
                                   )
    if order is None:
        base_tensors = bt[0]
    else:
        base_tensors = base_tensors[:1] + bt
    if return_inverse:
        if order is None:
            bt = [base_tensors]
        else:
            bt = base_tensors[1:]
        return base_tensors, inverse_internal_coordinate_tensors(bt, coords, masses=masses, order=order,
                                                                 fixed_atoms=fixed_atoms,
                                                                 fixed_coords=fixed_coords,
                                                                 fixed_cartesians=fixed_cartesians,
                                                                 remove_translation_rotation=remove_inverse_translation_rotation
                                                                 )
    else:
        return base_tensors

def prep_internal_derivatives(expansion, fixed_atoms=None, fixed_coords=None, fixed_cartesians=None):
    copied = False
    if fixed_atoms is not None:
        atom_pos = np.reshape(
            (np.array(fixed_atoms) * 3)[:, np.newaxis]
            + np.arange(3)[np.newaxis],
            -1
        )
        expansion = [e.copy() for e in expansion]
        copied = True
        for n, e in enumerate(expansion):
            idx = (...,) + np.ix_(*[atom_pos] * (n + 1)) + (slice(None),)
            e[idx] = 0
    if fixed_cartesians is not None:
        if not copied:
            expansion = [e.copy() for e in expansion]
            copied = True
        fc = np.array(fixed_cartesians)
        fc = 3*fc[:, 0] + fc[:, 1]
        for n, e in enumerate(expansion):
            idx = (...,) + np.ix_(*[fc] * (n + 1)) + (slice(None),)
            e[idx] = 0
    if fixed_coords is not None:
        if not copied:
            expansion = [e.copy() for e in expansion]
            copied = True
        for n, e in enumerate(expansion):
            e[..., fixed_coords] = 0

    return expansion

def prep_inverse_derivatives(expansion, fixed_atoms=None, fixed_coords=None, fixed_cartesians=None):
    copied = False
    if fixed_atoms is not None:
        atom_pos = np.reshape(
            (np.array(fixed_atoms) * 3)[:, np.newaxis]
            + np.arange(3)[np.newaxis],
            -1
        )
        expansion = [e.copy() for e in expansion]
        copied = True
        for n, e in enumerate(expansion):
            e[..., atom_pos] = 0
    if fixed_cartesians is not None:
        if not copied:
            expansion = [e.copy() for e in expansion]
            copied = True
        fc = np.array(fixed_cartesians)
        fc = 3*fc[:, 0] + fc[:, 1]
        for n, e in enumerate(expansion):
            e[..., fc] = 0
    if fixed_coords is not None:
        if not copied:
            expansion = [e.copy() for e in expansion]
            copied = True
        for n, e in enumerate(expansion):
            idx = (...,) + np.ix_(*[fixed_coords] * (n + 1)) + (slice(None),)
            e[idx] = 0

    return expansion

_transrot_projection_method = 'addition'
_pre_mass_weight = False
def inverse_internal_coordinate_tensors(expansion,
                                        coords=None, masses=None, order=None,
                                        mass_weighted=True,
                                        remove_translation_rotation=True,
                                        fixed_atoms=None,
                                        fixed_coords=None,
                                        fixed_cartesians=None,
                                        ):
    from .CoordinateFrames import translation_rotation_invariant_transformation, translation_rotation_eigenvectors

    if order is None:
        order = len(expansion)

    expansion = prep_internal_derivatives(
        expansion,
        fixed_atoms=fixed_atoms,
        fixed_coords=fixed_coords,
        fixed_cartesians=fixed_cartesians
    )

    if coords is not None and remove_translation_rotation:
        # expansion = remove_translation_rotations(expansion, coords[opt_inds], masses)
        if _pre_mass_weight:
            g12 = np.expand_dims(
                np.repeat(
                    np.diag(np.repeat(1 / np.sqrt(masses), 3)),
                    coords.shape[0],
                    axis=0
                ),
                list(range(expansion[0].ndim - 2))
            )
            expansion = td.tensor_reexpand([g12], expansion, len(expansion))
        if _transrot_projection_method == 'projector':
            #TODO: is this the correct definition? Do we want to project out before or after the inverse?
            L_base, L_inv = translation_rotation_invariant_transformation(coords, masses,
                                                                        mass_weighted=True, strip_embedding=True)
            new_tf = td.tensor_reexpand([L_inv], expansion, order)
            inverse_tf = td.inverse_transformation(new_tf, order, allow_pseudoinverse=True)
            inverse_expansion = [
                vec_tensordot(j, np.moveaxis(L_inv, -1, -2), axes=[-1, -1], shared=L_base.ndim - 2)
                    if not misc.is_numeric(j) else
                j
                for j in inverse_tf
            ]
        else:
            _, tr = translation_rotation_eigenvectors(coords, masses, mass_weighted=_pre_mass_weight)
            tr_expansion = [tr]
            n = tr.shape[-1]
            for e in expansion[1:]:
                base_shape = e.shape[:-1]
                final_shape = base_shape + (n,)
                tr_expansion.append(np.zeros(final_shape))
            total_exp = [np.concatenate([t, e], axis=-1) for t,e in zip(tr_expansion, expansion)]
            inverse_tf = td.inverse_transformation(total_exp, order, allow_pseudoinverse=True)
            inverse_expansion = []
            for i,t in enumerate(inverse_tf):
                idx = (...,) + (slice(n, None),)*(i+1) + (slice(None),)
                inverse_expansion.append(t[idx])
        if _pre_mass_weight:
            inverse_expansion = td.tensor_reexpand(inverse_expansion, [g12], order)
    elif mass_weighted and masses is not None:
        sqrt_mass = np.expand_dims(
            np.repeat(
                np.diag(np.repeat(1 / np.sqrt(masses), 3)),
                coords.shape[0],
                axis=0
            ),
            list(range(expansion[0].ndim - 2))
        )
        expansion = td.tensor_reexpand([sqrt_mass], expansion, len(expansion))
        inverse_expansion = td.inverse_transformation(expansion, order=order, allow_pseudoinverse=True)
        inverse_expansion = td.tensor_reexpand(inverse_expansion, [sqrt_mass], order)
    else:
        inverse_expansion = td.inverse_transformation(expansion, order=order, allow_pseudoinverse=True)

    inverse_expansion = prep_inverse_derivatives(inverse_expansion,
                                                 fixed_atoms=fixed_atoms,
                                                 fixed_coords=fixed_coords,
                                                 fixed_cartesians=fixed_cartesians)

    return inverse_expansion

def rotation_expansion_from_axis_angle(coords, axis, order=1, *, angle=0, axis_order=0):
    axis = vec_normalize(axis)
    if axis.ndim > 1:
        raise NotImplementedError("multi-axis broadcasting is tedious")
    R_expansion = geom.axis_rot_gen_deriv(angle, axis, angle_order=order, axis_order=axis_order)
    if axis_order == 0:
        return [
            (coords[..., np.newaxis, :] @ np.moveaxis(R, -1, -2)).reshape(
                coords.shape
                    if i == 0 else
                (coords.shape[:-2] + (coords.shape[-2] * coords.shape[-1],))
            )
            for i,R in enumerate(R_expansion)
        ]
    else:
        extra = coords.ndim - 2
        base_expansion = [
            np.moveaxis(np.tensordot(coords, R, axes=[-1, -1]), extra, -2)
            for R in R_expansion
        ]
        return [
            np.reshape(
                e,
                e.shape[:-2] + (e.shape[-2] * e.shape[-1],)
            ) if i > 0 else e
            for i,e in enumerate(base_expansion)
        ]

def _handle_expansion_atom_exclusions(coords, left_expansion, right_expansion, left_atoms, right_atoms):
    rem_atoms = np.setdiff1d(np.arange(len(coords)), np.concatenate([left_atoms, right_atoms]))
    left_pos = block_broadcast_indices(left_atoms, 3)
    # right_pos = block_broadcast_indices(right_atoms, 3)
    rem_pos = block_broadcast_indices(rem_atoms, 3)
    for e,l in zip(right_expansion[1:], left_expansion[1:]):
        if len(left_pos) > 0:
            e[..., left_pos] = l[..., left_pos]
        if len(rem_pos) > 0:
            e[..., rem_pos] = 0
    return right_expansion

def dist_expansion(coords, i, j, order=1, left_atoms=None, right_atoms=None):
    coords = np.asanyarray(coords)
    vec = vec_normalize(coords[..., j, :] - coords[..., i, :]) / 2
    base_shape = coords.shape[:-2]
    targ_shape = base_shape + (coords.shape[-2] * coords.shape[-1],)
    right_expansion = [coords]
    for o in range(order):
        term = np.zeros(coords.shape)
        if o == 0:
            term[..., :] = vec
        right_expansion.append(term.reshape(targ_shape))
    left_expansion = [coords]
    for o in range(order):
        term = np.zeros(coords.shape)
        if o == 0:
            term[..., :] = -vec
        left_expansion.append(term.reshape(targ_shape))

    if left_atoms is None:
        left_atoms = [i]
    if right_atoms is None:
        right_atoms = [j]
    _handle_expansion_atom_exclusions(coords, left_expansion, right_expansion, left_atoms, right_atoms)
    return right_expansion

def angle_expansion(coords, i, j, k, order=1, left_atoms=None, right_atoms=None, *, angle=0, axis_order=0):
    coords = np.asanyarray(coords)
    shift_coords = coords - coords[..., (j,), :]
    axis = vec_crosses(coords[..., i, :] - coords[..., j, :],
                       coords[..., k, :] - coords[..., j, :],
                       normalize=True)
    right_expansion = rotation_expansion_from_axis_angle(shift_coords, axis, order=order, angle=angle, axis_order=axis_order)
    left_expansion = rotation_expansion_from_axis_angle(shift_coords, -axis, order=order, angle=angle, axis_order=axis_order)
    #TODO: fix this
    right_expansion[0] += coords[..., (j,), :] # shift back from origin
    if left_atoms is None:
        left_atoms = [i]
    if right_atoms is None:
        right_atoms = [k]
    _handle_expansion_atom_exclusions(coords, left_expansion, right_expansion, left_atoms, right_atoms)
    right_expansion = right_expansion[:1] + [e/2 for e in right_expansion[1:]]
    return right_expansion

def dihed_expansion(coords, i, j, k, l, order=1, left_atoms=None, right_atoms=None, *, angle=0, axis_order=0):
    coords = np.asanyarray(coords)
    shift_coords = coords - coords[..., (k,), :]
    axis = shift_coords[..., j, :]
    right_expansion = rotation_expansion_from_axis_angle(shift_coords, -axis, order=order, angle=angle, axis_order=axis_order)
    left_expansion = rotation_expansion_from_axis_angle(shift_coords, axis, order=order, angle=angle, axis_order=axis_order)
    # left might not always be the negation...I think
    right_expansion[0] += coords[..., (k,), :] # shift back from origin

    if left_atoms is None:
        left_atoms = [i]
    if right_atoms is None:
        right_atoms = [l]
    _handle_expansion_atom_exclusions(coords, left_expansion, right_expansion, left_atoms, right_atoms)
    right_expansion = right_expansion[:1] + [e/2 for e in right_expansion[1:]]
    return right_expansion

class _inverse_coordinate_conversion_caller:
    def __init__(self, conversion, target_internals,
                 remove_translation_rotation=True,
                 masses=None,
                 order=1,
                 gradient_function=None,
                 gradient_scaling=None,
                 fixed_atoms=None,
                 fixed_coords=None
                 ):
        self.conversion = conversion
        self.target_internals = target_internals
        self.masses = masses
        self.remove_translation_rotation = remove_translation_rotation
        self.gradient_function = gradient_function
        self.gradient_scaling = gradient_scaling
        self.last_call = None
        self.caller_order = order
        self.fixed_atoms = fixed_atoms
        self.fixed_coords = fixed_coords

    def func(self, coords, mask):
        coords = coords.reshape(coords.shape[0], -1, 3)
        internals = self.conversion(coords, order=0)[0]
        delta = internals - self.target_internals[mask]
        return np.sum(delta, axis=1)

    def jacobian(self, coords, mask):
        ord = self.caller_order
        coords = coords.reshape(coords.shape[0], -1, 3)
        expansion = self.last_call = self.conversion(coords, order=ord)
        internals, expansion = expansion[0], expansion[1:] # dr/dx
        delta = internals - self.target_internals[mask]
        fixed_coords = self.fixed_coords

        if self.fixed_atoms is not None:
            atom_pos = np.reshape(
                (np.array(self.fixed_atoms) * 3)[:, np.newaxis]
                + np.arange(3)[np.newaxis],
                -1
            )
            for n,e in enumerate(expansion):
                idx = (...,) + np.ix_(*[atom_pos] * (n + 1)) + (slice(None),)
                e[idx] = 0
        if fixed_coords is not None:
            for n,e in enumerate(expansion):
                e[..., fixed_coords] = 0

        if self.remove_translation_rotation: # dx/dr
            inverse_expansion = inverse_internal_coordinate_tensors(expansion, coords, self.masses, ord)
        else:
            sqrt_mass = np.expand_dims(
                np.repeat(
                    np.diag(np.repeat(1 / np.sqrt(self.masses), 3)),
                    coords.shape[0],
                    axis=0
                ),
                list(range(expansion[0].ndim - 2))
            )
            expansion = td.tensor_reexpand([sqrt_mass], expansion, len(expansion))
            inverse_expansion = td.inverse_transformation(expansion, order=ord, allow_pseudoinverse=True)
            inverse_expansion = td.tensor_reexpand(inverse_expansion, [sqrt_mass], ord)

        if self.fixed_atoms is not None:
            atom_pos = np.reshape(
                    (np.array(self.fixed_atoms) * 3)[:, np.newaxis]
                    + np.arange(3)[np.newaxis],
                -1
            )
            for n,e in enumerate(inverse_expansion):
                e[..., atom_pos] = 0
        if fixed_coords is not None:
            delta[..., fixed_coords] = 0
            for n,e in enumerate(inverse_expansion):
                idx = (...,) + np.ix_(*[fixed_coords]*(n+1)) + (slice(None),)
                e[idx] = 0

        nr_change = 0
        for n, e in enumerate(inverse_expansion):
            for ax in range(n + 1):
                e = vec_tensordot(e, delta, axes=[1, -1], shared=1)
            nr_change += (1 / math.factorial(n + 1)) * e

        if self.gradient_function is not None:
            if self.fixed_atoms is not None:
                subcrd = np.delete(coords, self.fixed_atoms, axis=-2).reshape(coords.shape[0], -1)
                subgrad = self.gradient_function(subcrd, mask)
                contrib = np.zeros((coords.shape[0], coords.shape[1]*coords.shape[2]), dtype=subgrad.dtype)
                atom_pos = np.reshape(
                    (np.array(self.fixed_atoms) * 3)[:, np.newaxis]
                    + np.arange(3)[np.newaxis],
                    -1
                )
                rem_pos = np.delete(np.arange(contrib.shape[1]), atom_pos)
                contrib[..., rem_pos] = subgrad
            else:
                contrib = self.gradient_function(coords.reshape(coords.shape[0], -1), mask)
            extra_gradient = -self.gradient_scaling * contrib
            nr_change = nr_change + extra_gradient

        return nr_change

DEFAULT_SOLVER_ORDER = 1
def inverse_coordinate_solve(specs, target_internals, initial_cartesians,
                             masses=None,
                             remove_translation_rotation=True,
                             order=None,
                             solver_order=None,
                             tol=1e-3, max_iterations=15,
                             max_displacement=.5,
                             gradient_function=None,
                             gradient_scaling=.1,
                             # method='quasi-newton',
                             method='gradient-descent',
                             optimizer_parameters=None,
                             line_search=False,
                             damping_parameter=None,
                             damping_exponent=None,
                             restart_interval=None,
                             raise_on_failure=False,
                             return_internals=True,
                             return_expansions=True,
                             base_transformation=None,
                             reference_internals=None,
                             fixed_atoms=None,
                             fixed_coords=None,
                             angle_ordering='ijk'):
    from . import Optimization as opt

    if method == 'quasi-newton':
        if optimizer_parameters is None: optimizer_parameters = {}
        optimizer_parameters['initial_beta'] = optimizer_parameters.get('initial_beta', 70)

    if order is None:
        order = DEFAULT_SOLVER_ORDER
    if solver_order is None:
        solver_order = order
    if not misc.is_numeric(solver_order):
        solver_order = max(solver_order)

    if callable(specs):
        conversion = specs
    else:
        conversion = internal_conversion_function(specs,
                                                  angle_ordering=angle_ordering,
                                                  base_transformation=base_transformation,
                                                  reference_internals=reference_internals
                                                  )
    target_internals = np.asanyarray(target_internals)
    initial_cartesians = np.asanyarray(initial_cartesians)

    base_shape = target_internals.shape[:-1]
    smol = len(base_shape) == 0
    if smol:
        target_internals = target_internals[np.newaxis]
        initial_cartesians = initial_cartesians[np.newaxis]
        base_shape = (1,)
    if initial_cartesians.ndim == 2:
        coords = np.expand_dims(initial_cartesians, list(range(len(base_shape))))
        coords = np.broadcast_to(coords, base_shape + coords.shape[-2:]).copy()
    else:
        coords = initial_cartesians.copy()
    coords = coords.reshape((-1,) + coords.shape[-2:])
    init_coords = coords
    target_internals = target_internals.reshape((-1,) + target_internals.shape[-1:])

    caller = _inverse_coordinate_conversion_caller(
        conversion,
        target_internals,
        remove_translation_rotation=remove_translation_rotation,
        masses=masses,
        gradient_function=gradient_function,
        gradient_scaling=gradient_scaling,
        fixed_atoms=fixed_atoms,
        fixed_coords=fixed_coords
    )

    coords, converged, (errors, its) = opt.iterative_step_minimize(
        coords.reshape(coords.shape[:1] + (-1,)),
        opt.get_step_finder(
            caller.func,
            method=method,
            jacobian=caller.jacobian,
            damping_parameter=damping_parameter,
            damping_exponent=damping_exponent,
            restart_interval=restart_interval,
            line_search=line_search,
            **({} if optimizer_parameters is None else optimizer_parameters)
        ),
        tol=tol,
        max_displacement=max_displacement,
        max_iterations=max_iterations,
        prevent_oscillations=True
        # termination_function=caller.terminate
    )

    coords = coords.reshape(coords.shape[:1] + (-1, 3))
    opt_internals = conversion(
        coords,
        order=0 if not return_expansions else order
    )
    if not converged:
        init_internals = conversion(
            init_coords,
            order=0 if not return_expansions else order
        )[0]
        if raise_on_failure:
            raise ValueError(
                f"failed to find coordinates after {max_iterations} iterations"
                f"\ntarget:{target_internals}\ninitial:{init_internals}"
                f"\nresidual:{target_internals - opt_internals[0]}"
                f"\n1-norm error: {errors}"
                f"\n1-norm error: {errors}"
                f"\nmax deviation error: {np.max(abs(target_internals - opt_internals[0]))}"
            )
        # else:
        #     print(
        #         f"failed to find coordinates after {max_iterations} iterations"
        #         f"\ntarget:{target_internals}\ninitial:{init_internals}"
        #         f"\nresidual:{target_internals - opt_internals[0]}"
        #         f"\n1-norm error: {errors}"
        #         f"\nmax deviation error: {np.max(abs(target_internals - opt_internals[0]))}"
        #     )
    if return_expansions:
        expansion = opt_internals[1:]
        if remove_translation_rotation:
            opt_expansions = inverse_internal_coordinate_tensors(expansion, coords, masses, order)
        else:
            opt_expansions = td.inverse_transformation(expansion, order=order, allow_pseudoinverse=True)
    else:
        opt_expansions = None

    coords = coords.reshape(base_shape + coords.shape[-2:])
    errors = errors.reshape(base_shape)
    if opt_expansions is not None:
        opt_expansions = [
            o.reshape(base_shape + o.shape[1:]) if isinstance(o, np.ndarray) else o
            for o in opt_expansions
        ]
    opt_internals = [o.reshape(base_shape + o.shape[1:]) for o in opt_internals]
    if smol:
        coords = coords[0]
        errors = errors[0]
        opt_internals = [o[0] for o in opt_internals]
        if opt_expansions is not None:
            opt_expansions = [
                o[0] if isinstance(o, np.ndarray) else o
                for o in opt_expansions
            ]


    if return_expansions:
        tf = [coords] + opt_expansions
    else:
        tf = coords
    if return_internals:
        return (tf, errors), opt_internals
    else:
        return tf, errors

def coordinate_projection_data(basis_mat, fixed_mat, inds, nonzero_cutoff=1e-8,
                               masses=None, coords=None,
                               project_transrot=False):
    from .CoordinateFrames import translation_rotation_projector

    if project_transrot and coords is not None:
        sub_projector, sub_tr_modes = translation_rotation_projector(
            coords[..., inds, :],
            masses=(
                [masses[i] for i in inds]
                    if masses is not None else
                masses
            ),
            mass_weighted=False,
            return_modes=True
        )
        cs = coords.shape[-1]
        ncoord = coords.shape[-2]*coords.shape[-1]
        projector = np.zeros(coords.shape[:-2] + (ncoord, ncoord))
        full_idx = sum(( tuple(i*3+j for j in range(cs)) for i in inds ), ())
        proj_sel = (...,) + np.ix_(full_idx, full_idx)
        projector[proj_sel] = sub_projector
        tr_modes = np.zeros(coords.shape[:-2] + (ncoord, sub_tr_modes.shape[-1]))
        tr_modes[..., full_idx, :] = sub_tr_modes
    else:
        projector, tr_modes = None, None
    if basis_mat is not None:
        if projector is not None:
            #TODO: handle broadcasting
            basis_mat = projector @ basis_mat
        nats = basis_mat.shape[-2] // 3
        basis_mat = find_basis(basis_mat, nonzero_cutoff=nonzero_cutoff)
        mat = np.zeros(basis_mat.shape[:-2] + (nats, 3, nats, 3))
    else:
        if projector is not None:
            #     #TODO: handle broadcasting
            #     fixed_mat = projector @ fixed_mat
            fixed_mat = np.concatenate([tr_modes, fixed_mat], axis=-1)
        nats = fixed_mat.shape[-2] // 3
        fixed_mat = find_basis(fixed_mat, nonzero_cutoff=nonzero_cutoff)
        mat = np.zeros(fixed_mat.shape[:-2] + (nats, 3, nats, 3))
    for x in range(3):
        for i in inds:
            mat[..., i, x, i, x] = 1
    mat = np.reshape(mat, mat.shape[:-4] + (nats*3, nats*3))

    if basis_mat is not None:
        return basis_mat, find_basis(mat - projection_matrix(basis_mat, orthonormal=True)), mat
    else:
        return find_basis(mat - projection_matrix(fixed_mat, orthonormal=True)), fixed_mat, mat

def dist_basis_mat(coords, i, j):
    coords = np.asanyarray(coords)
    mat = np.zeros(coords.shape + (3,))
    for x in range(3):
        mat[..., i, x, x] = 1
        mat[..., j, x, x] = -1

    mat = mat.reshape(mat.shape[:-3] + (-1, 3))
    return mat

def dist_basis(coords, i, j, **opts):
    basis_mat = dist_basis_mat(coords, i, j)
    return coordinate_projection_data(basis_mat, None, (i,j),
                                      coords=coords,
                                      **opts
                                      )

def fixed_angle_basis(coords, i, j, k):
    coords = np.asanyarray(coords)
    mat = np.zeros(coords.shape + (7,))
    for x in range(3):
        mat[..., i, x, x] = 1
        mat[..., j, x, x] = 1
        mat[..., k, x, x] = 1
    v1 = coords[..., i, :] - coords[..., j, :]
    mat[..., i, :, 3] = v1
    mat[..., j, :, 4] = -v1
    mat[..., k, :, 4] = -v1
    v2 = coords[..., k, :] - coords[..., j, :]
    mat[..., k, :, 5] = v2
    mat[..., j, :, 6] = -v2
    mat[..., i, :, 6] = -v2

    mat = mat.reshape(mat.shape[:-3] + (-1, 7))
    return mat

def angle_basis(coords, i, j, k, angle_ordering='ijk', **opts):
    if angle_ordering == 'jik':
        i,j,k = j,i,k
    fixed_mat = fixed_angle_basis(coords, i, j, k)
    return coordinate_projection_data(None, fixed_mat, (i,j,k),
                                      coords=coords,
                                      **opts
                                      )

def fixed_dihed_basis(coords, i, j, k, l):
    coords = np.asanyarray(coords)
    mat = np.zeros(coords.shape + (9,))
    for x in range(3):
        mat[..., i, x, x] = 1
        mat[..., j, x, x] = 1
        mat[..., k, x, x] = 1
        mat[..., l, x, x] = 1
    # basis for plane 1
    v1 = coords[..., i, :] - coords[..., j, :]
    v2 = coords[..., j, :] - coords[..., k, :]
    mat[..., i, :, 3] = v1
    mat[..., i, :, 4] = v2
    mat[..., j, :, 5] = v2
    # basis for plane 2
    v3 = coords[..., l, :] - coords[..., k, :]
    mat[..., l, :, 6] = v2
    mat[..., l, :, 7] = v3
    mat[..., k, :, 8] = v2

    mat = mat.reshape(mat.shape[:-3] + (-1, 9))
    return mat

def dihed_basis(coords, i, j, k, l, **opts):
    fixed_mat = fixed_dihed_basis(coords, i, j, k, l)
    return coordinate_projection_data(None, fixed_mat, (i,j,k,l),
                                      coords=coords,
                                      **opts
                                      )

basis_coord_type_map = {
    'dist':dist_basis,
    'bend':angle_basis,
    'dihed':dihed_basis,
}
def internal_basis_specs(specs, angle_ordering='ijk', **opts):
    return internal_conversion_specs(
        specs,
        angle_ordering=angle_ordering,
        coord_type_dispatch=basis_coord_type_map,
        **opts
    )
def internal_basis(coords, specs, **opts):
    base_specs = internal_basis_specs(specs, **opts)
    bases = []
    ortos = []
    subprojs = []
    for f, idx, subopts in base_specs:
        basis, orthog, subproj = f(coords, *idx, **subopts)
        bases.append(basis)
        ortos.append(orthog)
        subprojs.append(subproj)
    return bases, ortos, subprojs


def metric_tensor(internals_by_cartesians, masses=None):
    if misc.is_numeric_array_like(internals_by_cartesians):
        internals_by_cartesians = np.asanyarray(internals_by_cartesians)
        if internals_by_cartesians.ndim == 2:
            internals_by_cartesians = [internals_by_cartesians]
    transformation = np.asanyarray(internals_by_cartesians[0])
    if masses is not None:
        g12_base = np.diag(np.repeat(1/np.sqrt(masses), 3))
        transformation = np.moveaxis(
            np.tensordot(transformation, g12_base, axes=[-2, 0]),
            -1, -2
        )
    return np.moveaxis(transformation, -1, -2) @ transformation

def delocalized_internal_coordinate_transformation(
        internals_by_cartesians,
        untransformed_coordinates=None,
        masses=None,
        relocalize=False
):
    if misc.is_numeric_array_like(internals_by_cartesians):
        internals_by_cartesians = [internals_by_cartesians]
    conv = np.asanyarray(internals_by_cartesians[0])
    if masses is not None:
        g12_base = np.diag(np.repeat(1/np.sqrt(masses), 3))
        conv = np.moveaxis(
            np.tensordot(conv, g12_base, axes=[-2, 0]),
            -1, -2
        )

    if untransformed_coordinates is not None:
        transformed_coords = np.setdiff1d(np.arange(conv.shape[-1]), untransformed_coordinates)
        ut_conv = conv[..., untransformed_coordinates]
        conv = conv[..., transformed_coords]

        # project out contributions along untransformed coordinates to ensure
        # dimension of space remains unchanged
        ut_conv_norm = vec_normalize(np.moveaxis(ut_conv, -1, -2))
        proj = np.moveaxis(ut_conv_norm, -1, -2) @ ut_conv_norm
        proj = identity_tensors(proj.shape[:-2], proj.shape[-1]) - proj

        conv = np.concatenate([ut_conv, proj @ conv], axis=-1)

    G_internal = np.moveaxis(conv, -1, -2) @ conv
    redund_vals, redund_tf = np.linalg.eigh(G_internal)
    redund_pos = np.where(np.abs(redund_vals) > 1e-10)
    if redund_vals.ndim > 1:
        redund_tf = setops.take_where_groups(redund_tf, redund_pos)
    else:
        redund_tf = redund_tf[:, redund_pos[0]]
    if isinstance(redund_tf, np.ndarray):
        redund_tf = np.flip(redund_tf, axis=-1)
    else:
        redund_tf = [
            np.flip(tf, axis=-1)
            for tf in redund_tf
        ]

    if relocalize:
        if untransformed_coordinates is not None:
            perm = np.concatenate([untransformed_coordinates,
                                   np.delete(np.arange(redund_tf.shape[-2]), untransformed_coordinates)
                                   ])
            perm = np.argsort(perm)
            if isinstance(redund_tf, np.ndarray):
                redund_tf = redund_tf[..., perm, :]
            else:
                redund_tf = [
                    redund_tf[..., perm, :]
                    for tf in redund_tf
                ]


    return redund_tf

def relocalize_coordinate_transformation(redund_tf, untransformed_coordinates=None):
    n = redund_tf.shape[-1]
    if untransformed_coordinates is None:
        ndim = redund_tf.ndim - 2
        eye = identity_tensors(redund_tf.shape[:-2], n)
        target = np.pad(eye, ([[0, 0]] * ndim) + [[0, redund_tf.shape[-2] - n], [0, 0]])
    else:
        untransformed_coordinates = np.asanyarray(untransformed_coordinates)
        coords = np.concatenate([
            untransformed_coordinates,
            np.delete(np.arange(redund_tf.shape[-2]), untransformed_coordinates)
        ])[:n]
        target = np.moveaxis(np.zeros(redund_tf.shape), -1, -2)
        idx = setops.vector_ix(target.shape[:-1], coords[:, np.newaxis])
        target[idx] = 1
        target = np.moveaxis(target, -1, -2)
    loc = np.linalg.lstsq(redund_tf, target, rcond=None)
    U, s, V = np.linalg.svd(loc[0])
    R = U @ V
    return redund_tf @ R

def transform_cartesian_derivatives(
        derivs,
        tfs,
        axes=None
):
    if axes is None:
        axes = -1
    if misc.is_numeric(axes):
        axes = [-1, -2]
    derivs = [
        np.asanyarray(d) if not misc.is_numeric(d) else d
        for d in derivs
    ]

    tfs = np.asanyarray(tfs)
    d_ax, t_ax = axes
    if d_ax < 0:
        d_ax = derivs[0].ndim + d_ax
    if tfs.ndim > 2:
        shared = d_ax
    else:
        shared = None

    new_derivs = []
    for i,d in enumerate(derivs):
        if not misc.is_numeric(d):
            for j in range(i+1):
                d_shape = d.shape
                d = d.reshape(
                    d.shape[:d_ax+j] + (d.shape[d_ax+j]//3, 3) + d.shape[d_ax+j+1:]
                )
                if shared is not None:
                    d = vec_tensordot(d, tfs, axes=[d_ax+j+1, tfs], shared=shared)
                else:
                    d = np.tensordot(d, tfs, axes=[d_ax + j + 1, tfs])
                d = np.moveaxis(d, -1, d_ax + j + 1).reshape(d_shape)
            new_derivs.append(d)

    return new_derivs
