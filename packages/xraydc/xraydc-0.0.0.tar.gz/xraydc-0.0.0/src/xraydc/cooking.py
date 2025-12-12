from xraydc.signal import QMapper

all = [
    "sRSM",
    "TRSM",
    "rocking"
]

def _kmc3_recipe_helper_datamangle(data, **spice):
    # Helper for KMC3 recipes: changes data (mostly by applying offsets)
    # returns new dataset
    
    data2 = data.copy()
    
    if 'offsets' in spice:
        for k, v in spice['offsets'].items():
            if k not in data:
                continue
            data2[k] = data[k] + spice['offsets'][k]

    return data2


def _kmc3_recipe_helper_expimangle(expi, **spice):
    # Helper for KMC3 recipes: changes experimental info
    # using spice info from 'image', 'energy', and possibly others.
    # Returns new experimental info, and a qmap parameters dict.
    expi2 = expi.copy()

    #if 'energy' in spice:
    #    expi2['beamEnergy'] = spice['energy']['energy']    

    if 'image' in spice:
        expi2['imageCenter'] = spice['image']['imageCenter']
        expi2['imageDistance'] = spice['image']['imageDistance']

    return expi2, {}


def _kmc3_recipe_helper_qargs(qpar, **spice):
    '''
    Updates q-transformation parameters "qpar" by the values specified
    in a spice type called "qargs", which has the following fields:
      - dims: None or list of dimensions to transform
      - qsize: None or gridding size for each dimension
      - groupby: None or groupby field to pass to the xarray gridder
        (only applies to recipes which do a .groupby() call)
      - gridargs: None or extra arguments to pass to the xru gridder
    '''
    ret = qpar.copy()
    if 'qargs' in spice:
        qargs = spice['qargs']
        for p in ('dims', 'qsize'):
            if qargs[p] is not None:
                ret[p] = qargs[p]
        for p in ('gridargs',):
            if qargs[p] is not None:
                ret[p].update(qargs[p])
    return ret


def _make_mapper(expi, qpar):
    '''
    Creates and sets up a mapper.
    '''
    mapper = QMapper(**expi)
    ga = qpar.get('gridargs', None)
    if ga is not None:
        mapper.setupGridder(**ga)
    return mapper


def _kmc3_data_hotfix(idata):    
    ## This is a _VERY_ dirty solution to analyzing KMC3 data, which is 4-dimensional with Eiger
    if 'eiger_image' in idata:
        tmp = idata.sum('eiger_image_1')
    else:
        tmp = idata
    
    return tmp



def sRSM(stype, data, **spice):
    '''
    Generating static RSMs.

    Requires `exp_info` spice. Also performs basic data mangling
    if appropriate spice types (`offsets`) available, and
    modifies exp_info if exp_info modifiers (`image`) also available.
    '''
    data2 = _kmc3_recipe_helper_datamangle(data, **spice)
    expi2, qpar = _kmc3_recipe_helper_expimangle(spice['exp_info'], **spice)

    tmp = _kmc3_data_hotfix(data2)

    qpar = _kmc3_recipe_helper_qargs(qpar, **spice)
    
    mapper = _make_mapper(expi2, qpar)
    
    return mapper.qmap(tmp, **qpar)


def TRSM(stype, data, **spice):
    '''
    Generic RSM grouping cooking. Generally we'd have a specific
    parameter to group by (temperature or delay), but it all boils
    down to the same algorithm.

    The most generic "thing" to group by would be specific scans.

    For specific groupby parameters ("temp") we'd actually want
    to round before grouping.
    '''
    from nx5d.xrd.signal import QMapper
    data2 = _kmc3_recipe_helper_datamangle(data, **spice)
    expi2, qpar = _kmc3_recipe_helper_expimangle(spice['exp_info'], **spice)

    tmp = _kmc3_data_hotfix(data2)
    qpar = _kmc3_recipe_helper_qargs(qpar, **spice)
    mapper = _make_mapper(expi2, qpar)

    groupby = spice.get('qargs', {}).get('groupby', None)
    if groupby is None:
        groupby = "temp" # compatibility with earlier API / spice structure

    if groupby in ('temp',) and groupby in tmp:
        tmp[groupby] = tmp[groupby].round()

    return tmp.groupby(groupby).map(mapper.qmap, **qpar)


def rocking(stype, data, **spice):
    raise RuntimeError('recipe for rocking data not implemented')

