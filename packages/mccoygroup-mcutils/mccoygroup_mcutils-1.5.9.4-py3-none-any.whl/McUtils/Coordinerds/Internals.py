import collections
import functools
import itertools

import numpy as np
from .. import Devutils as dev
from .. import Numputils as nput

__all__ = [
    "canonicalize_internal",
    "get_canonical_internal_list",
    "is_coordinate_list_like",
    "is_valid_coordinate",
    "permute_internals",
    "find_internal",
    "coordinate_sign",
    "coordinate_indices",
    "get_internal_distance_conversion",
    "internal_distance_convert",
    "get_internal_triangles_and_dihedrons",
    "find_internal_conversion",
    "get_internal_cartesian_conversion",
    "validate_internals",
    # "InternalCoordinateSet"
]

def canonicalize_internal(coord, return_sign=False):
    sign = 1
    if len(coord) == 2:
        i, j = coord
        if i == j: return None # faster to just do the cases
        if i > j:
            j, i = i, j
            sign = -1
        coord = (i, j)
    elif len(coord) == 3:
        i, j, k = coord
        if i == j or j == k or i == k: return None
        if i > k:
            i, j, k = k, j, i
            sign = -1
        coord = (i, j, k)
    elif len(coord) == 4:
        i, j, k, l = coord
        if (
                i == j or j == k or i == k
                or i == l or j == l or k == l
        ): return None
        if i > l:
            i, j, k, l = l, k, j, i
            sign = -1
        coord = (i, j, k, l)
    else:
        if len(np.unique(coord)) < len(coord): return None
        if coord[0] > coord[-1]:
            coord = tuple(reversed(coord))
            sign = -1
        else:
            coord = tuple(coord)
    if return_sign:
        return coord, sign
    else:
        return coord

def is_valid_coordinate(coord):
    return (
        len(coord) > 1 and len(coord) < 5
        and all(nput.is_int(c) for c in coord)
    )

def is_coordinate_list_like(clist):
    return dev.is_list_like(clist) and all(
        is_valid_coordinate(c) for c in clist
    )

class InternalCoordinateSet:
    def __init__(self, coord_specs:'list[tuple[int]]', prepped_data=None, triangulation=None):
        self._specs = tuple(coord_specs) if coord_specs is not None else coord_specs
        if prepped_data is not None:
            self._indicator, self.coordinate_indices, self.ind_map, self.coord_map = prepped_data
        else:
            self._indicator, self.coordinate_indices, self.ind_map, self.coord_map = self.prep_coords(coord_specs)
        self._triangulation = triangulation

    @property
    def specs(self):
        if self._specs is None:
            self._specs = tuple(self._create_coord_list(self._indicator, self.ind_map, self.coord_map))
        return self._specs

    IndicatorMap = collections.namedtuple("IndicatorMap", ['primary', 'child'])
    IndsMap = collections.namedtuple("IndsMap", ['dists', 'angles', 'diheds'])
    InternalsMap = collections.namedtuple("InternalsMap", ['dists', 'angles', 'diheds'])
    @classmethod
    def prep_coords(cls, coord_specs):
        dist_inds = []
        dists = []
        angle_inds = []
        angles = []
        dihed_inds = []
        diheds = []
        indicator = []
        subindicator = []
        atoms = {}

        for i,c in coord_specs:
            c = canonicalize_internal(c)
            atoms.update(c)
            if len(c) == 2:
                indicator.append(0)
                subindicator.append(len(dists))
                dist_inds.append(i)
                dists.append(c)
            elif len(c) == 2:
                indicator.append(1)
                angle_inds.append(i)
                subindicator.append(len(angles))
                angles.append(c)
            elif len(c) == 4:
                indicator.append(2)
                subindicator.append(len(diheds))
                dihed_inds.append(i)
                diheds.append(c)
            else:
                raise ValueError(f"don't know what to do with coord spec {c}")

        return (
            cls.IndicatorMap(np.array(indicator), np.array(subindicator)),
            tuple(sorted(atoms)),
            cls.IndsMap(np.array(dist_inds), np.array(angle_inds), np.array(dihed_inds)),
            cls.InternalsMap(np.array(dists), np.array(angles), np.array(diheds))
        )

    @classmethod
    def _map_dispatch(cls, map, coord):
        if nput.is_int(coord):
            if coord == 0:
                return map.dists
            elif coord == 1:
                return map.angles
            else:
                return map.diheds
        else:
            if len(coord) == 2:
                return map.dists
            elif len(coord) == 3:
                return map.dists
            elif len(coord) == 4:
                return map.diheds
            else:
                raise ValueError(f"don't know what to do with coord spec {coord}")

    def _coord_map_dispatch(self, coord):
        return self._map_dispatch(self.coord_map, coord)
    def _ind_map_dispatch(self, i):
        return self._map_dispatch(self.ind_map, i)
    def find(self, coord, missing_val='raise'):
        return nput.find(self._coord_map_dispatch(coord), coord, missing_val=missing_val)

    @classmethod
    def get_coord_from_maps(cls, item, indicator:IndicatorMap, ind_map, coord_map):
        if nput.is_int(item):
            map = indicator.primary[item]
            subloc = indicator.child[item]
            c_map = cls._map_dispatch(coord_map, map)
            return c_map[subloc,]
        else:
            map = indicator.primary[item,]
            uinds = np.unique(map)
            if len(uinds) > 1:
                return [
                    cls.get_coord_from_maps(i, indicator, ind_map, coord_map)
                    for i in item
                ]
            else:
                subloc = indicator.child[item,]
                c_map = cls._map_dispatch(coord_map, uinds[0])
                return c_map[subloc,]

    def __getitem__(self, item):
        return self.get_coord_from_maps(item, self._indicator, self.ind_map, self.coord_map)

    @classmethod
    def _create_coord_list(cls, indicator, inds, vals:InternalsMap):
        #TODO: make this more efficient, just concat the sub
        map = np.argsort(indicator.child)
        full = vals.diheds.tolist() + vals.angles.tolist() + vals.diheds.tolist()
        return [ tuple(full[i]) for i in map ]
    def permute(self, perm, canonicalize=True):
        #TODO: handle padding this
        inv = np.argsort(perm)
        dists = self.coord_map.dists
        if len(dists) > 0:
            dists = inv[dists]
        angles = self.coord_map.angles
        if len(angles) > 0:
            angles = inv[angles]
        diheds = self.coord_map.diheds
        if len(diheds) > 0:
            diheds = inv[diheds]

        cls = type(self)
        int_map = self.InternalsMap(dists, angles, diheds)
        if canonicalize:
            return cls(self._create_coord_list(self._indicator, self.ind_map, int_map))
        else:
            return cls(None, prepped_data=[self._indicator, self.coordinate_indices, self.ind_map, int_map])

    def get_triangulation(self):
        return get_internal_triangles_and_dihedrons(self.specs, canonicalize=False)
    @property
    def triangulation(self):
        if self._triangulation is None:
            self._triangulation = self.get_triangulation()
        return self._triangulation


def get_canonical_internal_list(coords):
    if isinstance(coords, InternalCoordinateSet):
        return coords.specs
    else:
        return [canonicalize_internal(c) for c in coords]

def find_internal(coords, coord, missing_val:'Any'='raise', canonicalize=True, allow_negation=False):
    if canonicalize:
        coord = canonicalize_internal(coord)
    if isinstance(coords, InternalCoordinateSet):
        return coords.find(coord, allow_negation=allow_negation)
    else:
        try:
            idx = coords.index(coord)
        except ValueError:
            idx = None

        sign = 1
        if idx is None and allow_negation and len(coord) == 4:
            test = (coord[0],coord[2],coord[1],coord[3])
            idx = find_internal(coords, test, missing_val=None, canonicalize=False, allow_negation=False)
            if idx is not None:
                sign = -1

        if idx is None:
            if dev.str_is(missing_val, 'raise'):
                raise ValueError("{} not in coordinate set".format(coord))
            else:
                idx = missing_val
        if allow_negation:
            return idx, sign
        else:
            return idx

def permute_internals(coords, perm, canonicalize=True):
    if isinstance(coords, InternalCoordinateSet):
        return coords.permute(perm, canonicalize=canonicalize)
    else:
        return [
            canonicalize_internal([perm[c] if c < len(perm) else c for c in coord])
                if canonicalize else
            tuple(perm[c] if c < len(perm) else c for c in coord)
            for coord in coords
        ]

def coordinate_sign(old, new, canonicalize=True):
    if len(old) != len(new): return 0
    if len(old) == 2:
        i,j = old
        m,n = new
        if i == n:
            return int(j == m)
        elif i == m:
            return int(i == n)
        else:
            return 0
    elif len(old) == 3:
        i,j,k = old
        m,n,o = new
        if j != n:
            return 0
        elif i == m:
            return int(k == o)
        elif i == o:
            return int(k == m)
        else:
            return 0
    elif len(old) == 4:
        # all pairwise comparisons now too slow
        if canonicalize:
            old = canonicalize_internal(old)
            new = canonicalize_internal(new)

        i,j,k,l = old
        m,n,o,p = new

        if i != m or l != p:
            return 0
        elif j == n:
            return int(k == o)
        elif j == o:
            return -int(k == n)
        else:
            return 0
    else:
        raise ValueError(f"can't compare coordinates {old} and {new}")

def coordinate_indices(coords):
    if isinstance(coords, InternalCoordinateSet):
        return coords.coordinate_indices
    else:
        return tuple(sorted(
            {x for c in coords for x in c}
        ))

dm_conv_data = collections.namedtuple("dm_conv_data",
                                      ['input_indices', 'pregen_indices', 'conversion', 'mapped_pos'])
tri_conv = collections.namedtuple("tri_conv", ['type', 'coords', 'val'])
dihed_conv = collections.namedtuple("dihed_conv", ['type', 'coords'])
def _get_input_ind(dm_data):
    return (
        dm_data.input_indices[0]
            if dm_data.conversion is None else
        None
    )
def _get_pregen_ind(dm_data):
    return (
        None
            if dm_data.conversion is None else
        dm_data.mapped_pos
    )
def get_internal_distance_conversion_spec(internals, canonicalize=True):
    if isinstance(internals, InternalCoordinateSet):
        internals = internals.specs
    dists:dict[tuple[int,int], dm_conv_data] = {}
    # we do an initial pass to separate out dists, angles, and dihedrals
    # for checking
    angles:list[tuple[tuple[int,int,int], int]] = []
    dihedrals:list[tuple[tuple[int,int,int,int], int]] = []
    for n,coord in enumerate(internals):
        if canonicalize:
            coord = canonicalize_internal(coord)
            if coord is None: continue
        if len(coord) == 2:
            coord:tuple[int,int]
            dists[coord] = dm_conv_data([n], [None], None, len(dists))
        elif len(coord) == 3:
            coord:tuple[int,int,int]
            angles.append((coord, n))
        else:
            coord:tuple[int,int,int,int]
            dihedrals.append((coord, n))

    #TODO: add in multiple passes until we stop picking up new distances
    #TODO: prune out ssa rules...these are ambiguous
    for n,((i,j,k),m) in enumerate(angles):
        a = canonicalize_internal((i,j))
        b = canonicalize_internal((j,k))
        c = (i,k)
        if a in dists and b in dists:
            if c not in dists:
                C = (i,j,k)
                d1 = dists[a]
                d2 = dists[b]
                # sas triangle
                dists[c] = dm_conv_data(
                    (_get_input_ind(d1), m, _get_input_ind(d2)),
                    (_get_pregen_ind(d1), None, _get_pregen_ind(d2)),
                    tri_conv('sas', (a, C, b), 2),
                    len(dists)
                )
        # elif a in dists and c in dists:
        #     # ssa triangle, angle at `i`
        #     if b not in dists:
        #         C = (i,j,k)
        #         d1 = dists[c]
        #         d2 = dists[a]
        #         # sas triangle
        #         dists[b] = dm_conv_data(
        #             (_get_input_ind(d1), _get_input_ind(d2), m),
        #             (_get_pregen_ind(d1), _get_pregen_ind(d2), None),
        #             tri_conv('ssa', (c, a, C), 2),
        #             len(dists)
        #         )
        # elif b in dists and c in dists:
        #     # ssa triangle, angle at `k`
        #     if a not in dists:
        #         B = (i,j,k)
        #         d1 = dists[b]
        #         d2 = dists[c]
        #         # sas triangle
        #         dists[a] = dm_conv_data(
        #             (_get_input_ind(d1), _get_input_ind(d2), m),
        #             (_get_pregen_ind(d1), _get_pregen_ind(d2), None),
        #             tri_conv('ssa', (b, c, B), 2),
        #             len(dists)
        #         )
        else:
            # try to another angle triangle coordinates that can be converted back to sss form
            for (ii,jj,kk),m2 in angles[n+1:]:
                # all points must be shared
                if k == jj and (
                        i == ii and j == kk
                        or i == kk and j == ii
                ):
                    C = (i, j, k)
                    A = (i, k, j)
                    if a in dists: # (i,j)
                        # we have saa
                        d = dists[a]
                        if b not in dists:
                            dists[b] = dm_conv_data(
                                (_get_input_ind(d), m, m2),
                                (_get_pregen_ind(d), None, None),
                                tri_conv('saa', (a, C, A), 2),
                                len(dists)
                            )
                        if c not in dists:
                            dists[c] = dm_conv_data(
                                (_get_input_ind(d), m, m2),
                                (_get_pregen_ind(d), None, None),
                                tri_conv('saa', (a, C, A), 1),
                                len(dists)
                            )
                    elif b in dists: # (k, j)
                        d = dists[b]
                        if a not in dists:
                            dists[a] = dm_conv_data(
                                (m, _get_input_ind(d), m2),
                                (None, _get_pregen_ind(d), None),
                                tri_conv('asa', (C, b, A), 1),
                                len(dists)
                            )
                        if c not in dists:
                            dists[c] = dm_conv_data(
                                (m, _get_input_ind(d), m2),
                                (None, _get_pregen_ind(d), None),
                                tri_conv('asa', (C, b, A), 2),
                                len(dists)
                            )
                    elif c in dists: # (i, k)
                        d = dists[c]
                        if b not in dists:
                            dists[b] = dm_conv_data(
                                (_get_input_ind(d), m2, m),
                                (_get_pregen_ind(d), None, None),
                                tri_conv('saa', (c, A, C), 2),
                                len(dists)
                            )
                        if c not in dists:
                            dists[a] = dm_conv_data(
                                (_get_input_ind(d), m2, m),
                                (_get_pregen_ind(d), None, None),
                                tri_conv('saa', (c, A, C), 1),
                                len(dists)
                            )
                elif i == jj and (
                        k == ii and j == kk
                        or k == kk and j == ii
                ):
                    C = (i, j, k)
                    B = (j, i, k)
                    if a in dists: # (i,j)
                        d = dists[a]
                        if b not in dists:
                            dists[b] = dm_conv_data(
                                (m, _get_input_ind(d), m2),
                                (None, _get_pregen_ind(d), None),
                                tri_conv('asa', (C, a, B), 1),
                                len(dists)
                            )
                        if c not in dists:
                            dists[c] = dm_conv_data(
                                (m, _get_input_ind(d), m2),
                                (None, _get_pregen_ind(d), None),
                                tri_conv('asa', (C, a, B), 2),
                                len(dists)
                            )
                    elif b in dists: # (k, j)
                        d = dists[b]
                        if a not in dists:
                            dists[a] = dm_conv_data(
                                (_get_input_ind(d), m, m2),
                                (_get_pregen_ind(d), None, None),
                                tri_conv('saa', (b, C, B), 2),
                                len(dists)
                            )
                        if c not in dists:
                            dists[c] =  dm_conv_data(
                                (_get_input_ind(d), m, m2),
                                (_get_pregen_ind(d), None, None),
                                tri_conv('saa', (b, C, B), 1),
                                len(dists)
                            )
                    elif c in dists: # (i, k)
                        d = dists[c]
                        if a not in dists:
                            dists[a] = dm_conv_data(
                                (_get_input_ind(d), m2, m),
                                (_get_pregen_ind(d), None, None),
                                tri_conv('saa', (c, B, C), 2),
                                len(dists)
                            )
                        if b not in dists:
                            dists[b] = dm_conv_data(
                                (_get_input_ind(d), m2, m),
                                (_get_pregen_ind(d), None, None),
                                tri_conv('saa', (c, B, C), 1),
                                len(dists)
                            )
                # x = canonicalize_internal((ii, jj))
                # y = canonicalize_internal((jj, kk))
                # z = (ii, kk)
                # if x == a:
                #     ...

    angle_dict = dict(angles)
    for n,((i,j,k,l),m) in enumerate(dihedrals):
        d = canonicalize_internal((i,l))
        if d not in dists:
            a = canonicalize_internal((i,j))
            b = canonicalize_internal((j,k))
            c = canonicalize_internal((k,l))
            x = canonicalize_internal((i,k))
            y = canonicalize_internal((j,l))
            if (
                    a in dists
                    and b in dists
                    and c in dists
            ):
                A = canonicalize_internal((i,j,k))
                B = canonicalize_internal((j,k,l))
                if A in angle_dict:
                    if B in angle_dict:
                        d1 = dists[a]
                        d2 = dists[b]
                        d3 = dists[c]
                        m1 = angle_dict[A]
                        m2 = angle_dict[B]
                        dists[d] = dm_conv_data(
                            (_get_input_ind(d1), _get_input_ind(d2), _get_input_ind(d3), m1, m2, m),
                            (_get_pregen_ind(d1), _get_pregen_ind(d2), _get_pregen_ind(d3), None, None, None),
                            dihed_conv('sssaat', (a, b, c, A, B, (i,j,k,l))),
                            len(dists)
                        )
                    elif y in dists:
                        d1 = dists[c]
                        d2 = dists[b]
                        d3 = dists[a]
                        d4 = dists[y]
                        m1 = angle_dict[A]
                        dists[d] = dm_conv_data(
                            (_get_input_ind(d1), _get_input_ind(d2), _get_input_ind(d3), _get_input_ind(d4), m1, m),
                            (_get_pregen_ind(d1), _get_pregen_ind(d2), _get_pregen_ind(d3), _get_pregen_ind(d4), None, None, None),
                            dihed_conv('ssssat', (c, b, a, y, A, (i,j,k,l))),
                            len(dists)
                        )
                elif B in angle_dict:
                    if x in dists:
                        d1 = dists[a]
                        d2 = dists[b]
                        d3 = dists[c]
                        d4 = dists[x]
                        m1 = angle_dict[B]
                        dists[d] = dm_conv_data(
                            (_get_input_ind(d1), _get_input_ind(d2), _get_input_ind(d3), _get_input_ind(d4), m1, m),
                            (_get_pregen_ind(d1), _get_pregen_ind(d2), _get_pregen_ind(d3), _get_pregen_ind(d4), None, None),
                            dihed_conv('ssssat', (a, b, c, x, B, (i,j,k,l))),
                            len(dists)
                        )
                elif x in dists and y in dists:
                    d1 = dists[a]
                    d2 = dists[b]
                    d3 = dists[c]
                    d4 = dists[x]
                    d5 = dists[y]
                    dists[d] = dm_conv_data(
                        (_get_input_ind(d1), _get_input_ind(d2), _get_input_ind(d3), _get_input_ind(d4), _get_input_ind(d5), m),
                        (_get_pregen_ind(d1), _get_pregen_ind(d2), _get_pregen_ind(d3), _get_pregen_ind(d4), _get_pregen_ind(d5), None,
                         None),
                        dihed_conv('ssssst', (a, b, c, x, y, (i, j, k, l))),
                        len(dists)
                    )


    return dists

def _prep_interal_distance_conversion(conversion_spec:dm_conv_data):
    if conversion_spec.conversion is None:
        def convert(internal_values, _, n=conversion_spec.input_indices[0]):
            return internal_values[..., n]
    elif hasattr(conversion_spec.conversion, 'val'):
        # a triangle to convert
        #TODO: allow triangle conversions to share context
        conversion:tri_conv = conversion_spec.conversion
        triangle_converter = nput.triangle_converter(conversion.type, 'sss')
        val = conversion.val
        int_args = conversion_spec.input_indices
        dist_args = conversion_spec.pregen_indices
        def convert(internal_values, distance_values,
                    order=None,
                    int_args=int_args,
                    dist_args=dist_args,
                    converter=triangle_converter,
                    val=val,
                    **kwargs):
            args = [
                internal_values[..., n]
                    if n is not None else
                distance_values[..., m]
                for n,m in zip(int_args, dist_args)
            ]
            if order is None:
                return converter[0](*args)[val]
            else:
                return converter[1](*args, order=order, **kwargs)[val]
    else:
        # a dihedral to convert
        conversion:dihed_conv = conversion_spec.conversion
        dist_converter = nput.dihedral_distance_converter(conversion.type)
        int_args = conversion_spec.input_indices
        dist_args = conversion_spec.pregen_indices
        def convert(internal_values, distance_values,
                    order=None,
                    *,
                    int_args=int_args,
                    dist_args=dist_args,
                    converter=dist_converter,
                    **kwargs):
            args = [
                internal_values[..., n]
                    if n is not None else
                distance_values[..., m]
                for n,m in zip(int_args, dist_args)
            ]
            if order is None:
                return converter[0](*args)[val]
            else:
                return converter[1](*args, order=order, **kwargs)[val]
    return convert
def _get_internal_distance_conversion(internals, canonicalize=True, shift_dihedrals=True, abs_dihedrals=True):
    base_conv = get_internal_distance_conversion_spec(internals, canonicalize=canonicalize)
    final_inds = list(sorted(base_conv.keys(), key=lambda k:base_conv[k].mapped_pos))
    rordered_conversion = list(sorted(base_conv.values(), key=lambda v:v.mapped_pos))
    convs = [
        _prep_interal_distance_conversion(v) for v in rordered_conversion
    ]
    dihedral_pos = [i for i,v in enumerate(internals) if len(v) == 4]
    def convert(internal_values,
                inds=final_inds, convs=convs,
                dihedral_pos=dihedral_pos,
                shift_dihedrals=shift_dihedrals):
        internal_values = np.asanyarray(internal_values)
        if shift_dihedrals:
            internal_values = internal_values.copy()
            # force to be positive, push back onto appro
            internal_values[..., dihedral_pos] = np.pi - np.abs(internal_values[..., dihedral_pos])
        elif abs_dihedrals:
            internal_values = internal_values.copy()
            # force to be positive, push back onto appro
            internal_values[..., dihedral_pos] = np.abs(internal_values[..., dihedral_pos])
        dists = np.zeros(internal_values.shape[:-1] + (len(convs),))
        for n,c in enumerate(convs):
            dists[..., n] = c(internal_values, dists)

        return dists

    return final_inds, convert
def _check_complete_distances(final_dists):
    ds = set(final_dists)
    final_dists = list(final_dists)
    inds = np.unique([x for y in final_dists for x in y])
    targs = list(itertools.combinations(inds, 2))
    missing = []
    ord = []
    for i,j in targs:
        if (i,j) in ds:
            ord.append(final_dists.index((i,j)))
        elif (j,i) in ds:
            ord.append(final_dists.index((j,i)))
        else:
            missing.append((i,j))

    if len(missing) > 0:
        raise ValueError(f"distance set missing: {missing}")

    return ord
def internal_distance_convert(coords, specs,
                              canonicalize=True,
                              shift_dihedrals=True,
                              abs_dihedrals=True,
                              check_distance_spec=True):
    final_dists, converter = get_internal_distance_conversion(specs,
                                                              canonicalize=canonicalize,
                                                              shift_dihedrals=shift_dihedrals,
                                                              abs_dihedrals=abs_dihedrals
                                                              )
    if check_distance_spec:
        ord = _check_complete_distances(final_dists)
    else:
        ord = None
    conv = converter(coords)
    if ord is not None:
        conv = conv[..., ord]
        final_dists = [final_dists[i] for i in ord]
    return final_dists, conv

def _find_coord_comp(coord, a, internals, prior_coords, missing_val):
    a_idx = find_internal(internals, a, missing_val=None)
    found_main = True
    if a_idx is None:
        found_main = False
        a_idx = find_internal(prior_coords, a, missing_val=None)
    if a_idx is None:
        if dev.str_is(missing_val, 'raise'):
            raise ValueError(f"can't construct {coord} from internals (requires {a})")
    return a_idx, found_main

def _get_dihedron_bond_key_name(mod_sets, a,b,c,d, i, j):
    base = (a, b, c, d)
    for perm in [
        (0, 1, 2, 3),
        (0, 2, 1, 3),
        (0, 2, 3, 1),
        (0, 3, 2, 1),
        (0, 1, 3, 2),
        (0, 3, 1, 2),
        (1, 0, 2, 3),
        (1, 2, 0, 3),
        (1, 0, 3, 2),
        (1, 3, 0, 2),
        (2, 0, 1, 3),
        (2, 1, 0, 3)
    ]:
        key = [base[_] for _ in perm]
        key, sign = canonicalize_internal(key, return_sign=True)
        if key in mod_sets:
            break
    else:
        key = canonicalize_internal((a, b, c, d))

    b = tuple(sorted(key.index(_) for _ in [i,j]))
    return key, nput.dihedron_property_specifiers(b)["name"]
def _get_dihedron_angle_key_name(mod_sets, a,b,c,d, i, j, k):
    base = (a, b, c, d)
    for perm in [
        (0, 1, 2, 3),
        (0, 2, 1, 3),
        (0, 2, 3, 1),
        (0, 3, 2, 1),
        (0, 1, 3, 2),
        (0, 3, 1, 2),
        (1, 0, 2, 3),
        (1, 2, 0, 3),
        (1, 0, 3, 2),
        (1, 3, 0, 2),
        (2, 0, 1, 3),
        (2, 1, 0, 3)
    ]:
        key = [base[_] for _ in perm]
        key, sign = canonicalize_internal(key, return_sign=True)
        if key in mod_sets:
            break
    else:
        key = canonicalize_internal((a, b, c, d))

    b = canonicalize_internal(tuple(key.index(_) for _ in [i,j,k]))
    z = nput.dihedron_property_specifiers(b)["name"]
    return key, z
def _get_dihedron_dihed_key_name(mod_sets, a,b,c,d, i, j, k, l):
    base = (a, b, c, d)
    for perm in [
        (0, 1, 2, 3),
        (0, 2, 1, 3),
        (0, 2, 3, 1),
        (0, 3, 2, 1),
        (0, 1, 3, 2),
        (0, 3, 1, 2),
        (1, 0, 2, 3),
        (1, 2, 0, 3),
        (1, 0, 3, 2),
        (1, 3, 0, 2),
        (2, 0, 1, 3),
        (2, 1, 0, 3)
    ]:
        key = [base[_] for _ in perm]
        key, sign = canonicalize_internal(key, return_sign=True)
        if key in mod_sets:
            break
    else:
        key = canonicalize_internal((a, b, c, d))

    b = canonicalize_internal(tuple(key.index(_) for _ in [i,j,k,l]))
    z = nput.dihedron_property_specifiers(b)["name"]
    return key, z
def get_internal_triangles_and_dihedrons(internals,
                                         canonicalize=True,
                                         construct_shapes=True,
                                         prune_incomplete=True):
    tri_sets:dict[tuple[int],set] = {}
    dihed_sets:dict[tuple[int],set] = {}
    for coord in internals:
        if canonicalize:
            coord = canonicalize_internal(coord)
        if len(coord) == 2:
            i,j = coord
            for (k,l,m),v in tri_sets.items():
                if i == k:
                    if j == l:
                        v.add("a")
                        break
                    elif j == m:
                        v.add("c")
                        break
                    elif m is None:
                        tri_sets[(k,l,j)] = {"a", "c"}
                        break
                elif i == l:
                    if j == k:
                        v.add("a")
                        break
                    elif j == m:
                        v.add("b")
                        break
                    elif m is None:
                        c = canonicalize_internal((j,l,k))
                        tri_sets[c] = {"a", "b"}
                        break
                elif i == m and j == l:
                    tri_sets[(k,l,m)].add("b")
                    break
            else:
                tri_sets[(i,j,None)] = {"a"}

            mod_sets = dihed_sets.copy()
            for (k, l, m, n), v in dihed_sets.items():
                if i == k:
                    if j == l:
                        v.add("a")
                    elif j == m:
                        v.add("x")
                    elif j == n:
                        v.add("z")
                    elif m is None:
                        key = (k, l, j, None)
                        mod_sets[key] = mod_sets.get(key, v) | {"x"}
                    elif n is None:
                        key, z = _get_dihedron_bond_key_name(mod_sets, k,l,m,j, i, j)
                        mod_sets[key] = mod_sets.get(key, v) | {z}
                elif i == l:
                    if j == k:
                        v.add("a")
                    elif j == m:
                        v.add("b")
                    elif j == n:
                        v.add("y")
                    elif m is None:
                        key = (k,l,j,n)
                        mod_sets[key] = mod_sets.get(key, v) | {"b"}
                    elif n is None:
                        key, z = _get_dihedron_bond_key_name(mod_sets, k,l,m,j, i, j)
                        mod_sets[key] = mod_sets.get(key, v) | {z}
                elif i == m:
                    if j == l:
                        mod_sets[(k,l,m,n)].add("b")
                    elif j == n:
                        mod_sets[(k,l,m,n)].add("c")
                    elif n is None:
                        key = (k,l,m,j)
                        mod_sets[key] =mod_sets.get(key, v) | {"c"}
                elif i == n:
                    if j == l:
                        mod_sets[(k,l,m,n)].add("y")
                    elif j == m:
                        mod_sets[(k,l,m,n)].add("c")
                elif m is None:
                    if j == k:
                        key = (k,l,i,n)
                        mod_sets[key] = mod_sets.get(key, v) | {"x"}
                    elif j == l:
                        key = (k,l,i,n)
                        mod_sets[(k,l,i,n)] = mod_sets.get(key, v) | {"b"}
                    else:
                        key, z = _get_dihedron_bond_key_name(mod_sets, k, l, i, j, i, j)
                        mod_sets[key] = mod_sets.get(key, v) | {z}
                elif n is None:
                    if j in (k,l,m):
                        key, z = _get_dihedron_bond_key_name(mod_sets, k, l, m, i, i, j)
                        mod_sets[key] = mod_sets.get(key, v) | {z}
            else:
                if (i, j, None, None) not in mod_sets:
                    mod_sets[(i, j, None, None)] = {"a"}
            dihed_sets = mod_sets
        elif len(coord) == 3:
            i,j,k = coord
            C = i,j,k
            A = canonicalize_internal((i,k,j))
            B = canonicalize_internal((j,i,k))
            if C in tri_sets:
                tri_sets[C].add("C")
            elif A in tri_sets:
                tri_sets[A].add("A")
            elif B in tri_sets:
                tri_sets[B].add("B")
            elif (A[0],A[2], None) in tri_sets:
                if i < j:
                    tri_sets[C] = {"a" if i < k else "b", "C"}
                else:
                    tri_sets[B] = {"a" if j < k else "b", "C"}
            elif (B[0],B[2], None) in tri_sets:
                if j < k:
                    tri_sets[A] = {"b" if i < j else "a", "C"}
                else:
                    tri_sets[C] = ["b" if i < k else "a", "C"]
            elif (C[0],C[2], None) in tri_sets:
                if i < k:
                    tri_sets[A] = {"a" if i < j else "b", "C"}
                else:
                    tri_sets[B] = {"a" if j < k else "b", "C"}

            mod_sets = dihed_sets.copy()
            for (a, l, m, n), v in dihed_sets.items():
                if m is None:
                    if i == a:
                        if j == l:
                            key = (a, l, k, n)
                            mod_sets[key] = mod_sets.get(key, v) | {"X"}
                        elif k == l:
                            key = (a, l, j, n)
                            mod_sets[key] = mod_sets.get(key, v) | {"A"}
                        else:
                            key, z = _get_dihedron_angle_key_name(mod_sets, a,l,j,k, i, j, k)
                            mod_sets[key] = mod_sets.get(key, v) | {z}
                    elif i == l:
                        if j == a:
                            key = (a, l, k, n)
                            mod_sets[key] = mod_sets.get(key, v) | {"B1"}
                        elif k == a:
                            key = (a, l, j, n)
                            mod_sets[key] = mod_sets.get(key, v) | {"A"}
                        else:
                            key, z = _get_dihedron_angle_key_name(mod_sets, a,l,j,k, i, j, k)
                            mod_sets[key] = mod_sets.get(key, v) | {z}
                    elif j == a:
                        if k == l:
                            key = (a, l, i, n)
                            mod_sets[key] = mod_sets.get(key, v) | {"B1"}
                        else:
                            key, z = _get_dihedron_angle_key_name(mod_sets, a,l,i,k, i, j, k)
                            mod_sets[key] = mod_sets.get(key, v) | {z}
                    elif j == l:
                        if k == a:
                            key = (a, l, i, n)
                            mod_sets[key] = mod_sets.get(key, v) | {"X"}
                        else:
                            key, z = _get_dihedron_angle_key_name(mod_sets, a,l,i,k, i, j, k)
                            mod_sets[key] = mod_sets.get(key, v) | {z}
                    elif k in {a,l}:
                        key, z = _get_dihedron_angle_key_name(mod_sets, a,l,i,j, i, j, k)
                        mod_sets[key] = mod_sets.get(key, v) | {z}
                elif n is None:
                    C1 = canonicalize_internal((a, l, m))
                    if C == C1:
                        mod_sets[(a, l, m, n)].add("X")
                    elif A == C1: # i,k,j
                        mod_sets[(a, l, m, n)].add("A")
                    elif B == C1:
                        mod_sets[(a, l, m, n)].add("B1")
                    else:
                        for (aa,ll) in itertools.combinations([a, l, m], 2):
                            if i == aa:
                                if j == ll:
                                    key, z = _get_dihedron_angle_key_name(mod_sets, a, l, m, k, i, j, k)
                                    mod_sets[key] = mod_sets.get(key, v) | {z}
                                elif k == l:
                                    key, z = _get_dihedron_angle_key_name(mod_sets, a, l, m, j, i, j, k)
                                    mod_sets[key] = mod_sets.get(key, v) | {z}
                            elif i == l:
                                if j == a:
                                    key, z = _get_dihedron_angle_key_name(mod_sets, a, l, m, k, i, j, k)
                                    mod_sets[key] = mod_sets.get(key, v) | {z}
                                elif k == a:
                                    key, z = _get_dihedron_angle_key_name(mod_sets, a, l, m, j, i, j, k)
                                    mod_sets[key] = mod_sets.get(key, v) | {z}
                            elif j == a and k == l:
                                key, z = _get_dihedron_angle_key_name(mod_sets, a, l, m, i, i, j, k)
                                mod_sets[key] = mod_sets.get(key, v) | {z}
                            elif j == l and k == a:
                                key, z = _get_dihedron_angle_key_name(mod_sets, a, l, m, i, i, j, k)
                                mod_sets[key] = mod_sets.get(key, v) | {z}
                else:
                    for (x, y, z), (_, _, _, X, Y, Z) in [
                        [(a, l, m), ("a", "b", "x", "A", "B1", "X")],
                        [(l, m, n), ("b", "c", "y", "B2", "C", "Y")],
                        [(a, l, n), ("a", "y", "z", "A3", "Y3", "Z")],
                        [(a, m, n), ("x", "c", "z", "X4", "C4", "Z2")]
                    ]:
                        C1 = canonicalize_internal((x, y, z))
                        A1 = canonicalize_internal((x, z, y))
                        B1 = canonicalize_internal((y, x, z))
                        if C == C1:
                            mod_sets[(a, l, m, n)].add(Z)
                        elif C == A1:
                            mod_sets[(a, l, m, n)].add(X)
                        elif C == B1:
                            mod_sets[(a, l, m, n)].add(Y)

            else:
                if (i, j, k, None) not in mod_sets:
                    mod_sets[(i, j, k, None)] = {"X"}
            dihed_sets = mod_sets

        elif len(coord) == 4:
            mod_sets = dihed_sets.copy()
            skey = tuple(sorted(coord))
            for (a, l, m, n),v in dihed_sets.items():
                if m is None:
                    try:
                        ix = coord.index(a)
                    except:
                        continue
                    try:
                        jx = coord.index(l)
                    except:
                        continue
                    rem = np.setdiff1d([0, 1, 2, 3], [ix, jx])
                    key, z = _get_dihedron_dihed_key_name(dihed_sets, a, l, coord[rem[0]], coord[rem[1]], *coord)
                    mod_sets[key] = mod_sets.get(key, v) | {z}
                elif n is None:
                        try:
                            ix = coord.index(a)
                        except:
                            continue
                        try:
                            jx = coord.index(l)
                        except:
                            continue
                        try:
                            kx = coord.index(m)
                        except:
                            continue
                        rem = np.setdiff1d([0, 1, 2, 3], [ix, jx, kx])
                        key, z = _get_dihedron_dihed_key_name(dihed_sets, a, l, m, coord[rem[0]], *coord)
                        mod_sets[key] = mod_sets.get(key, v) | {z}
                elif skey == tuple(sorted([a, l, m, n])):
                    key, z = _get_dihedron_dihed_key_name(dihed_sets, a, l, m, n, *coord)
                    mod_sets[key] = mod_sets.get(key, v) | {z}
            dihed_sets = mod_sets

    if prune_incomplete:
        tri_sets, dihed_sets = (
                {k:v for k,v in tri_sets.items() if None not in k},
                # dihed_sets
                {k:v for k,v in dihed_sets.items() if None not in k}
            )
        if construct_shapes:
            _ = {}
            for k,s in tri_sets.items():
                vals = {}
                for a in s:
                    idx = nput.triangle_property_specifiers(a)["coord"]
                    vals[a] = tuple(k[i] for i in idx)
                _[k] = nput.make_triangle(**vals)
            tri_sets = _

            _ = {}
            for k,s in dihed_sets.items():
                vals = {}
                for a in s:
                    idx = nput.dihedron_property_specifiers(a)["coord"]
                    vals[a] = tuple(k[i] for i in idx)
                _[k] = nput.make_dihedron(**vals)
            dihed_sets = _
    return tri_sets, dihed_sets

def _triangle_conversion_function(inds, tri, coord):
    idx = []
    for i in coord:
        try:
            ix = inds.index(i)
        except:
            return None
        else:
            idx.append(ix)
    b = canonicalize_internal(idx)
    target = nput.triangle_property_specifiers(b)
    return nput.triangle_property_function(tri, target['name'], raise_on_missing=False)
def _dihedral_conversion_function(inds, dihed, coord):
    idx = []
    for i in coord:
        try:
            ix = inds.index(i)
        except:
            return None
        else:
            idx.append(ix)
    b = canonicalize_internal(idx)
    return nput.dihedron_property_function(dihed, b, raise_on_missing=False)

int_conv_data = collections.namedtuple("int_conv_data",
                                      ['input_indices', 'pregen_indices', 'conversion'])
def find_internal_conversion(internals, targets,
                             triangles_and_dihedrons=None,
                             # prior_coords=None,
                             canonicalize=True,
                             missing_val='raise'):
    smol = nput.is_int(targets[0])
    if smol: targets = [targets]
    if triangles_and_dihedrons is None:
        if isinstance(internals, InternalCoordinateSet):
            triangles_and_dihedrons = internals.triangulation
            internals = internals.specs
        else:
            if canonicalize:
                internals = [canonicalize_internal(c) for c in internals]
            triangles_and_dihedrons = get_internal_triangles_and_dihedrons(internals, canonicalize=False)
    triangles, dihedrals = triangles_and_dihedrons
    conversions = []
    for target_coord in targets:

        if canonicalize:
            target_coord = canonicalize_internal(target_coord)
        idx = find_internal(internals, target_coord, missing_val=None, canonicalize=False)
        if idx is not None:
            def convert(internal_list, idx=idx):
                internal_list = np.asanyarray(internal_list)
                return internal_list[..., idx]
            conversions.append(convert)
            continue

        conv = None
        tri = None
        dihed = None
        n = len(target_coord)
        if n < 2 or n > 4:
            raise ValueError(f"can't understand coordinate {target_coord}")
        if len(target_coord) in {2, 3}:
            for a, v in triangles.items():
                tri = v
                conv = _triangle_conversion_function(a, v, target_coord)
                if conv is not None:
                    break
                else:
                    tri = None
        if conv is None and len(target_coord) in {2, 3, 4}:
            for a, v in dihedrals.items():
                dihed = v
                conv = _dihedral_conversion_function(a, v, target_coord)
                if conv is not None:
                    break
                else:
                    dihed = None
        if conv is None:
            if dev.str_is(missing_val, "raise"):
                raise ValueError(f"can't find conversion for {target_coord}")
            else:
                conversions.append(missing_val)
        else:

            # prep conversion based on internal indices
            if tri is not None:
                args = {k:find_internal(internals, v) for k,v in tri._asdict().items() if v is not None}
                def convert(internal_list, args=args, conv=conv,  **kwargs):
                    internal_list = np.asanyarray(internal_list)
                    subtri = nput.make_triangle(
                        **{k:internal_list[..., i] for k,i in args.items()}
                    )
                    return conv(subtri)
                convert.__name__ = 'convert_' + conv.__name__
            else:
                args = {
                    k:find_internal(internals, v, allow_negation=True)
                        for k,v in dihed._asdict().items()
                    if v is not None
                }
                def convert(internal_list, args=args, conv=conv, **kwargs):
                    internal_list = np.asanyarray(internal_list)
                    subargs = {k:s*internal_list[..., i] for k,(i,s) in args.items()}
                    subdihed = nput.make_dihedron(**subargs)
                    return conv(subdihed)
                convert.__name__ = 'convert_' + conv.__name__
            conversions.append(convert)

    if smol:
        convert = conversions[0]
    else:
        def convert(internal_spec, order=None, conversions=conversions, **kwargs):
            convs = [
                c(internal_spec)
                for c in conversions
            ]
            if order is None:
                return np.moveaxis(np.array(convs), 0, -1)
            else:
                return [
                    np.moveaxis(np.array([c[i] for c in convs]), 0, -1)
                    for i in range(order + 1)
                ]
    return convert
def enumerate_dists(internals):
    for coord in internals:
        for c in itertools.combinations(coord, 2):
            yield canonicalize_internal(c)
def get_internal_distance_conversion(
        internals,
        triangles_and_dihedrons=None,
        # prior_coords=None,
        canonicalize=True,
        missing_val='raise'
):
    dist_set = list(sorted(set(enumerate_dists(internals)))) # remove dupes, sort
    return dist_set, find_internal_conversion(internals, dist_set,
                                    canonicalize=canonicalize,
                                    triangles_and_dihedrons=triangles_and_dihedrons,
                                    missing_val=missing_val
                                    )

def get_internal_cartesian_conversion(
        internals,
        triangles_and_dihedrons=None,
        # prior_coords=None,
        canonicalize=True,
        missing_val='raise'
):
    #TODO: add direct conversion through Z-matrix if can be enumerated
    dists, dist_conv = get_internal_distance_conversion(internals,
                                                        triangles_and_dihedrons=triangles_and_dihedrons,
                                                        canonicalize=canonicalize,
                                                        missing_val=missing_val)
    n = (1 + np.sqrt(1 + 8 * len(dists))) / 2
    if int(n) != n:
        raise ValueError("fbad number of distances {len(dists)}")
    n = int(n)
    rows, cols = np.triu_indices(n, k=1)
    def convert(internals):
        internals = np.asanyarray(internals)
        base_shape = internals.shape[:-1]
        internal_dists = dist_conv(internals)
        dm = np.zeros(base_shape + (n, n))
        dm[..., rows, cols] = internal_dists
        dm[..., cols, rows] = internal_dists
        new_points = nput.points_from_distance_matrix(dm)
        if new_points.shape[-1] < 3:
            pad_shape = new_points.shape[:-1] + (3-new_points.shape[-1],)
            new_points = np.concatenate([new_points, np.zeros(pad_shape, dtype=new_points.dtype)], axis=-1)
        return new_points
    return convert

def validate_internals(internals, triangles_and_dihedrons=None, raise_on_failure=True):
    # detect whether or not they may be interconverted freely
    if triangles_and_dihedrons is None:
        if isinstance(internals, InternalCoordinateSet):
            triangles_and_dihedrons = internals.triangulation
            internals = internals.specs
        else:
            triangles_and_dihedrons = get_internal_triangles_and_dihedrons(internals, canonicalize=False)
    triangle, dihedrons = triangles_and_dihedrons
    for k,t in triangle.items():
        if not nput.triangle_is_complete(t):
            if raise_on_failure:
                raise ValueError(f"triangle cannot be completed, {k}:{t}")
            else:
                return False, (k,t)
    for k,t in dihedrons.items():
        if not nput.dihedron_is_complete(t):
            if raise_on_failure:
                raise ValueError(f"dihedral tetrahedron cannot be completed, {k}:{t}")
            else:
                return False, (k,t)
    return True, None

