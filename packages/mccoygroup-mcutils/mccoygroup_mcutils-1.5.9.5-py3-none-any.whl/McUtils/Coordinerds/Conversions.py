import numpy as np
from .. import Numputils as nput


__all__ = [
    "convert_cartesian_to_zmatrix",
    "convert_zmatrix_to_cartesians"
]

def get_dists(points, centers):
    return nput.pts_norms(centers, points)

def get_angles(lefts, centers, rights):
    return nput.pts_angles(lefts, centers, rights, return_crosses=False)

def get_diheds(points, centers, seconds, thirds):
    return nput.pts_dihedrals(points, centers, seconds, thirds)


def tile_order_list(ol, ncoords):
    nol = len(ol)
    ncol = len(ol[0])
    fsteps = ncoords / nol
    steps = int(fsteps)
    if steps != fsteps:
        raise ValueError(
            "Number of coordinates {} and number of specifed elements {} misaligned".format(
                ncoords,
                nol
            )
        )
    # broadcasts a single order spec to be a multiple order spec
    base_tile = np.broadcast_to(ol[:, :4], (steps, nol, 4))
    shift = np.reshape(np.arange(0, ncoords, nol), (steps, 1, 1))
    ol_tiled = base_tile + shift
    # now we add on extra flags
    if ncol > 4:
        flags_tiled = np.broadcast_to(ol[:, 4:], (steps, nol, ncol - 4))
        ol_tiled = np.concatenate([ol_tiled, flags_tiled], axis=-1)
    return np.reshape(ol_tiled, (ncoords, ncol))

def convert_cartesian_to_zmatrix(coords, *, ordering, use_rad=True, return_derivs=None, order=None,
            strip_embedding=False,
            derivative_method='new'):
    """The ordering should be specified like:

    [
        [n1],
        [n2, n1]
        [n3, n1/n2, n1/n2]
        [n4, n1/n2/n3, n1/n2/n3, n1/n2/n3]
        [n5, ...]
        ...
    ]

    :param coords:    array of cartesian coordinates
    :type coords:     np.ndarray
    :param use_rad:   whether to user radians or not
    :type use_rad:    bool
    :param ordering:  optional ordering parameter for the z-matrix
    :type ordering:   None or tuple of ints or tuple of tuple of ints
    :param kw:        ignored key-word arguments
    :type kw:
    :return: z-matrix coords
    :rtype: np.ndarray
    """

    if coords.ndim > 2:
        base_shape = coords.shape
        new_coords = np.reshape(coords, (np.prod(base_shape[:-1]),) + base_shape[-1:])
        new_coords, ops = convert_cartesian_to_zmatrix(new_coords,
                                                       ordering=ordering,
                                                       use_rad=use_rad,
                                                       return_derivs=return_derivs,
                                                       order=order,
                                                       strip_embedding=strip_embedding,
                                                       derivative_method=derivative_method)
        single_coord_shape = (base_shape[-2] - 1, new_coords.shape[-1])
        new_shape = base_shape[:-2] + single_coord_shape
        new_coords = np.reshape(new_coords, new_shape)
        if return_derivs:
            ders = ops['derivs']
            # we assume we get a list of derivatives?
            reshaped_ders = [None] * len(ders)
            for i, v in enumerate(ders):
                single_base_shape = (base_shape[-2], new_coords.shape[-1])
                ders_shape = coords.shape + single_base_shape * i + single_coord_shape
                v = v.reshape(ders_shape)
                reshaped_ders[i] = v
                ops['derivs'] = reshaped_ders
        return new_coords, ops

    else:
        if return_derivs is None and order is not None and order > 0:
            return_derivs = True

        ncoords = len(coords)
        orig_ol = np.asanyarray(ordering)#ZMatrixCoordinates.canonicalize_order_list(ncoords, ordering)
        ol = orig_ol
        nol = len(ol)
        ncol = len(ol[0])
        fsteps = ncoords / nol
        steps = int(round(fsteps))

        # print(">> c2z >> ordering:", ol)

        multiconfig = nol < ncoords
        if multiconfig:
            ol = tile_order_list(ol, ncoords)
            mc_ol = ol.copy()

        # we define an order map that we'll index into to get the new indices for a
        # given coordinate
        om = 1 + np.argsort(ol[:, 0])
        if return_derivs and derivative_method != "old":
            og_ord = None
            if order is None:
                order = 1
            elif isinstance(order, list):
                og_ord = order
                order = max(order)

            if strip_embedding:
                specs = [
                    p
                    for n, (i, j, k, l) in enumerate(ordering[1:])
                    for p in (
                        [(i, j), (i, j, k), (i, j, k, l)]
                        if n > 1 else
                        [(i, j), (i, j, k)]
                        if n > 0 else
                        [(i, j)]
                    )
                ]
                if len(specs) > 3:
                    ix = np.concatenate([[0, 1], np.arange(3, len(specs), 3)])
                    jx = np.concatenate([[2], np.arange(4, len(specs), 3)])
                    kx = np.arange(5, len(specs), 3)
                elif len(specs) > 1:
                    ix = np.array([0, 1])
                    jx = np.array([2])
                    kx = None
                else:
                    ix = np.array([0])
                    jx = None
                    kx = None
            else:
                specs = [
                    p
                    for n, (i, j, k, l) in enumerate(ordering[1:])
                    for p in (
                        [(i, j), (i, j, k), (i, j, k, l)]
                    )
                ]
                ix = np.arange(0, len(specs), 3)
                jx = np.arange(1, len(specs), 3)
                kx = np.arange(2, len(specs), 3)

            crd = coords.reshape((steps, nol, 3))
            base_conv = nput.internal_coordinate_tensors(crd, specs, order=order, angle_ordering='ijk')
            if strip_embedding:
                dists = base_conv[0][..., ix]
                if jx is None:
                    angles = np.zeros((len(base_conv), 1))
                else:
                    angles = np.array([
                        np.concatenate([[0], a])
                        for a in base_conv[0][..., jx]
                    ])
                if kx is None:
                    diheds = np.zeros((len(base_conv), 2))
                else:
                    diheds = np.array([
                        np.concatenate([[0], d])
                        for d in base_conv[0][..., kx]
                    ])
            else:
                dists = base_conv[0][..., ix]
                angles = base_conv[0][..., jx]
                diheds = base_conv[0][..., kx]

            base_derivs = base_conv[1:]
            derivs = []
            nats = nol
            for n, d in enumerate(base_derivs):
                deriv = np.zeros(
                    (steps,)
                    + ((nats) * 3,) * (n + 1)
                    + ((nats - 1) * 3,)
                )
                if strip_embedding:
                    deriv[..., np.arange(0, deriv.shape[-1], 3)] = d[..., ix]
                    if jx is not None:
                        deriv[..., np.arange(1, deriv.shape[-1], 3)] = np.pad(
                            d[..., jx],
                            [[0, 0]] * (d.ndim - 1) + [[1, 0]]
                        )
                    if kx is not None:
                        deriv[..., np.arange(2, deriv.shape[-1], 3)] = np.pad(
                            d[..., kx],
                            [[0, 0]] * (d.ndim - 1) + [[2, 0]]
                        )
                else:
                    deriv[..., np.arange(0, deriv.shape[-1], 3)] = d[..., ix]
                    if jx is not None:
                        deriv[..., np.arange(1, deriv.shape[-1], 3)] = d[..., jx]
                    if kx is not None:
                        deriv[..., np.arange(2, deriv.shape[-1], 3)] = d[..., kx]
                derivs.append(deriv)

            if og_ord is not None:
                derivs = [derivs[o - 1] for o in og_ord]
        else:
            # need to check against the cases of like 1, 2, 3 atom molecules
            # annoying but not hard
            if return_derivs:
                derivs = [
                    np.zeros(coords.shape + (nol - 1, 3)),
                    np.zeros(coords.shape + (nol, 3) + (nol - 1, 3))
                ]
            if not multiconfig:
                ix = ol[1:, 0]
                jx = ol[1:, 1]
                dists = get_dists(coords[ix], coords[jx])
                if return_derivs:
                    _dists, dist_derivs, dist_derivs_2 = nput.dist_deriv(coords, ix, jx, order=2)
                    drang = np.arange(len(ix))
                    derivs[0][ix, :, drang, 0] = dist_derivs[0]
                    derivs[0][jx, :, drang, 0] = dist_derivs[1]

                    for i, x1 in enumerate([ix, jx]):
                        for j, x2 in enumerate([ix, jx]):
                            # print(i, j, x1, x2,
                            #       # dist_derivs_2[i, j][0, 0],
                            #       drang
                            #       )
                            derivs[1][x1, :, x2, :, drang, 0] = dist_derivs_2[i, j]

                if len(ol) > 2:
                    ix = ol[2:, 0]
                    jx = ol[2:, 1]
                    kx = ol[2:, 2]
                    angles = np.concatenate((
                        [0], get_angles(coords[ix], coords[jx], coords[kx])
                    ))
                    if not use_rad:
                        angles = np.rad2deg(angles)
                    if return_derivs:
                        _angles, angle_derivs, angle_derivs_2 = nput.angle_deriv(coords, jx, ix, kx, order=2)
                        drang = 1 + np.arange(len(ix))
                        # print(">>>>", np.max(np.abs(angle_derivs)))
                        derivs[0][jx, :, drang, 1] = angle_derivs[0]
                        derivs[0][ix, :, drang, 1] = angle_derivs[1]
                        derivs[0][kx, :, drang, 1] = angle_derivs[2]

                        for i, x1 in enumerate([jx, ix, kx]):
                            for j, x2 in enumerate([jx, ix, kx]):
                                derivs[1][x1, :, x2, :, drang, 1] = angle_derivs_2[i, j]
                else:
                    angles = np.array([0.])
                if len(ol) > 3:
                    ix = ol[3:, 0]
                    jx = ol[3:, 1]
                    kx = ol[3:, 2]
                    lx = ol[3:, 3]
                    if ol.shape[1] == 5:
                        raise NotImplementedError("psi angles might be unnecessary")
                        ix = ix.copy()
                        jx = jx.copy()
                        kx = kx.copy()
                        lx = lx.copy()
                        fx = ol[3:, 4]
                        swap_pos = np.where(fx == 1)
                        swap_i = ix[swap_pos]
                        swap_j = jx[swap_pos]
                        swap_k = kx[swap_pos]
                        swap_l = lx[swap_pos]
                        ix[swap_pos] = swap_l
                        jx[swap_pos] = swap_i
                        kx[swap_pos] = swap_j
                        lx[swap_pos] = swap_k

                    diheds = np.concatenate((
                        [0, 0],
                        get_diheds(coords[ix], coords[jx], coords[kx], coords[lx])
                    ))
                    if not use_rad:
                        diheds = np.rad2deg(diheds)
                    if return_derivs:
                        _diheds, dihed_derivs, dihed_derivs_2 = nput.dihed_deriv(coords, ix, jx, kx, lx, order=2)
                        drang = 2 + np.arange(len(ix))
                        derivs[0][ix, :, drang, 2] = dihed_derivs[0]
                        derivs[0][jx, :, drang, 2] = dihed_derivs[1]
                        derivs[0][kx, :, drang, 2] = dihed_derivs[2]
                        derivs[0][lx, :, drang, 2] = dihed_derivs[3]

                        for i, x1 in enumerate([ix, jx, kx, lx]):
                            for j, x2 in enumerate([ix, jx, kx, lx]):
                                derivs[1][x1, :, x2, :, drang, 2] = dihed_derivs_2[i, j]
                else:
                    diheds = np.array([0, 0])
                ol = ol[1:]

            else:  # multiconfig

                # we do all of this stuff with masking operations in the multiconfiguration cases
                mask = np.repeat(True, ncoords)
                mask[np.arange(0, ncoords, nol)] = False
                ix = ol[mask, 0]
                jx = ol[mask, 1]
                dists = get_dists(coords[ix], coords[jx])
                if return_derivs:
                    _, dist_derivs, dist_derivs_2 = nput.dist_deriv(coords, ix, jx, order=2)
                    drang = np.arange(nol - 1)
                    nreps = int(len(ix) / (nol - 1))
                    drang = np.broadcast_to(drang[np.newaxis], (nreps,) + drang.shape).flatten()
                    derivs[0][ix, :, drang, 0] = dist_derivs[0]
                    derivs[0][jx, :, drang, 0] = dist_derivs[1]

                    for i, x1 in enumerate([ix, jx]):
                        for j, x2 in enumerate([ix, jx]):
                            derivs[1][x1, :, x2 % nol, :, drang, 0] = dist_derivs_2[i, j]

                if nol > 2:
                    # set up the mask to drop all of the first bits
                    mask[np.arange(1, ncoords, nol)] = False
                    ix = ol[mask, 0]
                    jx = ol[mask, 1]
                    kx = ol[mask, 2]
                    angles = get_angles(coords[ix], coords[jx], coords[kx])
                    angles = np.append(angles, np.zeros(steps))
                    insert_pos = np.arange(0, ncoords - 1 * steps - 1, nol - 2)
                    angles = np.insert(angles, insert_pos, 0)
                    angles = angles[:ncoords - steps]
                    if not use_rad:
                        angles = np.rad2deg(angles)
                    if return_derivs:
                        # we might need to mess with the masks akin to the insert call...
                        _, angle_derivs, angle_derivs_2 = nput.angle_deriv(coords, jx, ix, kx, order=2)
                        drang = 1 + np.arange(nol - 2)
                        nreps = int(len(ix) / (nol - 2))
                        drang = np.broadcast_to(drang[np.newaxis], (nreps,) + drang.shape).flatten()
                        derivs[0][jx, :, drang, 1] = angle_derivs[0]
                        derivs[0][ix, :, drang, 1] = angle_derivs[1]
                        derivs[0][kx, :, drang, 1] = angle_derivs[2]

                        for i, x1 in enumerate([ix, jx, kx]):
                            for j, x2 in enumerate([ix, jx, kx]):
                                derivs[1][x1, :, x2 % nol, :, drang, 0] = angle_derivs_2[i, j]
                else:
                    angles = np.zeros(ncoords - steps)

                if nol > 3:
                    # set up mask to drop all of the second atom bits (wtf it means 'second')
                    mask[np.arange(2, ncoords, nol)] = False
                    ix = ol[mask, 0]
                    jx = ol[mask, 1]
                    kx = ol[mask, 2]
                    lx = ol[mask, 3]
                    if ol.shape[1] == 5:
                        raise ValueError("Unclear if there is a difference between tau and psi")
                        ix = ix.copy()
                        jx = jx.copy()
                        kx = kx.copy()
                        lx = lx.copy()
                        fx = ol[mask, 4]
                        swap_pos = np.where(fx == 1)
                        swap_i = ix[swap_pos]
                        swap_j = jx[swap_pos]
                        swap_k = kx[swap_pos]
                        swap_l = lx[swap_pos]
                        ix[swap_pos] = swap_l
                        jx[swap_pos] = swap_i
                        kx[swap_pos] = swap_j
                        lx[swap_pos] = swap_k
                    # print(ol)

                    diheds = get_diheds(coords[ix], coords[jx], coords[kx], coords[lx])
                    # pad diheds to be the size of ncoords
                    diheds = np.append(diheds, np.zeros(2 * steps))

                    # insert zeros where undefined
                    diheds = np.insert(diheds, np.repeat(np.arange(0, ncoords - 2 * steps - 1, nol - 3), 2), 0)
                    # take only as many as actually used
                    diheds = diheds[:ncoords - steps]
                    if not use_rad:
                        diheds = np.rad2deg(diheds)
                    if return_derivs:
                        # Negative sign because my dihed_deriv code is for slightly different
                        # ordering than expected
                        _, dihed_derivs, dihed_derivs_2 = nput.dihed_deriv(coords, ix, jx, kx, lx, order=2)
                        drang = 2 + np.arange(nol - 3)
                        nreps = int(len(ix) / (nol - 3))
                        drang = np.broadcast_to(drang[np.newaxis], (nreps,) + drang.shape).flatten()
                        derivs[0][ix, :, drang, 2] = dihed_derivs[0]
                        derivs[0][jx, :, drang, 2] = dihed_derivs[1]
                        derivs[0][kx, :, drang, 2] = dihed_derivs[2]
                        derivs[0][lx, :, drang, 2] = dihed_derivs[3]

                        for i, x1 in enumerate([ix, jx, kx, lx]):
                            for j, x2 in enumerate([ix, jx, kx, lx]):
                                derivs[1][x1, :, x2 % nol, :, drang, 0] = dihed_derivs_2[i, j]

                else:
                    diheds = np.zeros(ncoords - steps)

                # after the np.insert calls we have the right number of final elements, but too many
                # ol and om elements and they're generally too large
                # so we need to shift them down and mask out the elements we don't want
                mask = np.repeat(True, ncoords)
                mask[np.arange(0, ncoords, nol)] = False
                ol = np.reshape(ol[mask], (steps, nol - 1, ncol)) - np.reshape(np.arange(steps), (steps, 1, 1))
                ol = np.reshape(ol, (ncoords - steps, ncol))
                om = np.reshape(om[mask], (steps, nol - 1)) - nol * np.reshape(np.arange(steps), (steps, 1)) - 1
                om = np.reshape(om, (ncoords - steps,))

        final_coords = np.array(
            [
                dists, angles, diheds
            ]
        ).T

        if multiconfig:
            # figure out what to use for the axes
            origins = coords[mc_ol[1::nol, 1]]
            x_axes = coords[mc_ol[1::nol, 0]] - origins  # the first displacement vector
            y_axes = coords[mc_ol[
                2::nol, 0]] - origins  # the second displacement vector (just defines the x-y plane, not the real y-axis)
            axes = np.array([x_axes, y_axes]).transpose((1, 0, 2))
        else:
            origins = coords[ol[0, 1]]
            axes = np.array([coords[ol[0, 0]] - origins, coords[ol[1, 0]] - origins])

        ol = orig_ol
        om = om - 1
        if ncol == 5:
            ordering = np.array([
                np.argsort(ol[:, 0]), om[ol[:, 1]], om[ol[:, 2]], om[ol[:, 3]], ol[:, 4]
            ]).T
        else:
            ordering = np.array([
                np.argsort(ol[:, 0]), om[ol[:, 1]], om[ol[:, 2]], om[ol[:, 3]]
            ]).T
        opts = dict(use_rad=use_rad, ordering=ordering, origins=origins, axes=axes)

        # if we're returning derivs, we also need to make sure that they're ordered the same way the other data is...
        if return_derivs:
            opts['derivs'] = derivs  # [:1]

        return final_coords, opts


def convert_zmatrix_to_cartesians(
        coordlist,
        *,
        ordering,
        origins=None,
        axes=None,
        use_rad=True,
        return_derivs=None,
        order=None
):
    """Expects to get a list of configurations
    These will look like:
        [
            [dist, angle, dihedral]
            ...
        ]
    and ordering will be
        [
            [pos, point, line, plane]
            ...
        ]
    **For efficiency it is assumed that all configurations have the same length**

    :param coordlist:
    :type coordlist:
    :param origins:
    :type origins:
    :param axes:
    :type axes:
    :param use_rad:
    :type use_rad:
    :param kw:
    :type kw:
    :param ordering:
    :type ordering:
    :param return_derivs:
    :type return_derivs:
    :return:
    :rtype:
    """
    # TODO: introduce fast derivs back into this coordinate system by extracting "specs" from the ordering
    #      and then partially inverting
    if return_derivs: raise NotImplementedError("analytic derivatives need maintenance")

    # make sure we have the ordering stuff in hand
    ordering = np.asanyarray(ordering)
    coordlist = np.asanyarray(coordlist)

    # if np.min(ordering) > 0:
    #     ordering = ordering - 1
    # dim_diff = coordlist.ndim - ordering.ndim
    # if dim_diff > 0:
    #     missing = coordlist.shape[:dim_diff]
    #     ordering = np.broadcast_to(ordering, missing + ordering.shape )

    sysnum = len(coordlist)
    coordnum = len(coordlist[0])
    if ordering.ndim == 2:
        ordering = np.repeat(ordering[np.newaxis], sysnum, axis=0)

    if ordering.shape[-1] > 3:
        atom_ordering = ordering[:, :, 0]
        ordering = ordering[:, 1:, 1:]
    else:
        atom_ordering = None

    total_points = np.empty((sysnum, coordnum + 1, 3))
    return_deriv_order = order
    if return_deriv_order is None:
        if return_derivs is not True and return_derivs is not False and isinstance(return_derivs, int):
            return_derivs = True
            return_deriv_order = return_derivs
        elif return_derivs:
            return_deriv_order = 2
    if return_derivs is None:
        return_derivs = return_deriv_order is not None

    if return_derivs:
        derivs = [
            None,  # no need to stoare a copy of total_points here...
            np.zeros((sysnum, coordnum, 3, coordnum + 1, 3)),
            np.zeros((sysnum, coordnum, 3, coordnum, 3, coordnum + 1, 3))
        ]

    # first we put the origin whereever the origins are specified
    if origins is None:
        origins = [0, 0, 0]
    origins = np.asarray(origins)
    if len(origins.shape) < 2:
        origins = np.broadcast_to(origins, (sysnum, 3))
    total_points[:, 0] = origins

    # set up the next points by just setting them along the x-axis by default
    if axes is None:
        axes = [1, 0, 0]
    axes = np.asarray(axes)
    if axes.ndim == 1:
        axes = np.array([
            axes,
            [0, 1, 0]
        ])  # np.concatenate((np.random.uniform(low=.5, high=1, size=(2,)), np.zeros((1,)) ))])
    if axes.ndim == 2:
        axes = np.broadcast_to(axes[np.newaxis], (sysnum, 2, 3))
    x_pts = origins + nput.vec_normalize(axes[:, 0])
    y_pts = origins + nput.vec_normalize(axes[:, 1])

    dists = coordlist[:, 0, 0]
    if return_derivs:
        raise NotImplementedError('old Z-matrix derivatives disabled for instabilities')
        der_stuff = cartesian_from_rad_derivatives(origins,
                                                   x_pts, y_pts, dists,
                                                   None, None,
                                                   0,
                                                   np.full((len(dists),), -1, dtype=int),
                                                   np.full((len(dists),), -1, dtype=int),
                                                   np.full((len(dists),), -1, dtype=int),
                                                   derivs,
                                                   order=return_deriv_order
                                                   )
        total_points[:, 1] = der_stuff[0]
        if return_deriv_order > 0:
            derivs[1][np.arange(sysnum), :1, :, 1, :] = der_stuff[1]
        if return_deriv_order > 1:
            derivs[2][np.arange(sysnum), :1, :, :1, :, 1, :] = der_stuff[2]

    else:
        ref_points_1, _ = nput.cartesian_from_rad(origins, x_pts, y_pts, dists, None, None)
        total_points[:, 1] = ref_points_1

    # print(">> z2c >> ordering", ordering[0])

    # iteratively build the rest of the coords with one special cases for n=2
    for i in range(1, coordnum):
        # Get the distances away

        ref_coords1 = ordering[:, i, 0]  # reference atom numbers for first coordinate
        refs1 = total_points[np.arange(sysnum), ref_coords1.astype(int)]  # get the actual reference coordinates
        dists = np.reshape(coordlist[:, i, 0], (sysnum, 1))  # pull the requisite distances

        ref_coords2 = ordering[:, i, 1]  # reference atom numbers for second coordinate
        refs2 = total_points[
            np.arange(sysnum), ref_coords2.astype(int)]  # get the actual reference coordinates for the angle
        angle = coordlist[:, i, 1]  # pull the requisite angle values
        if not use_rad:
            angle = np.deg2rad(angle)

        if i == 1:
            refs3 = y_pts
            dihed = None
            ref_coords3 = np.full((len(dists),), -1, dtype=int)
            psi_flag = False
        else:
            ref_coords3 = ordering[:, i, 2]  # reference atom numbers for dihedral ref coordinate
            refs3 = total_points[
                np.arange(sysnum), ref_coords3.astype(int)]  # get the actual reference coordinates for the dihed
            dihed = coordlist[:, i, 2]  # pull proper dihedral values
            if not use_rad:
                dihed = np.deg2rad(dihed)
            if ordering.shape[-1] == 4:
                raise ValueError("Unclear if there is a difference between tau and psi")
                psi_flag = ordering[:, i, 3] == 1
                # dihed[psi_flag] = -dihed[psi_flag]
            else:
                psi_flag = False

        if return_derivs:
            if ordering.shape[-1] == 4:
                raise NotImplementedError("don't have derivatives for case with psi angles")
            der_stuff = nput.cartesian_from_rad_derivatives(
                refs1, refs2, refs3,
                dists, angle, dihed,
                i,
                ref_coords1,
                ref_coords2,
                ref_coords3,
                derivs,
                order=return_deriv_order
            )
            # crd, d1, d2 = stuff

            total_points[:, i + 1] = der_stuff[0]
            if return_deriv_order > 0:
                derivs[1][np.arange(sysnum), :i + 1, :, i + 1, :] = der_stuff[1]
            if return_deriv_order > 1:
                derivs[2][np.arange(sysnum), :i + 1, :, :i + 1, :, i + 1, :] = der_stuff[2]
        else:
            ref_points_1, _ = nput.cartesian_from_rad(refs1, refs2, refs3, dists, angle, dihed, psi=psi_flag)
            total_points[:, i + 1] = ref_points_1

    if atom_ordering is not None:
        rev_ord = atom_ordering  # np.argsort(atom_ordering, axis=1)
        total_points = total_points[np.arange(len(atom_ordering))[:, np.newaxis], rev_ord]  # wat?

    converter_opts = dict(use_rad=use_rad, ordering=ordering)
    if return_derivs:
        if return_deriv_order > 0:
            converter_opts['derivs'] = derivs[1:][:return_deriv_order]

    return total_points, converter_opts