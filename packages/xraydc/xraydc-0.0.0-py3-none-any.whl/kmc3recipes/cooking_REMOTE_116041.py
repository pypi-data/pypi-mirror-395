from kmc3recipe.signal import QMapper

all = [
    "sRSM",
    "TRSM",
    "rocking",
    
    #"xRSS",
    #"tRSS",
]

# Recipe map to use for easy seeding of all herein supported types.
RecipeMap = {
    # static RSM    
    sRSM="pymod:///kmc3recipes.cooking#sRSM",

    # temperature-dependent RSM
    tRSM="pymod:///kmc3recipes.cooking#TRSM",

    # omega-2theta-scan (treat like RSM?)
    rocking="pymod:///kmc3recipes.cooking#sRSM",

    # some kind (?) of RSS
    xRSS=None,

    # time-dependent (?) RSS
    tRSS=None,
}

def _kmc3_recipe_helper_datamangle(data, **spice):
    # Helper for KMC3 recipes: changes data (mostly by applying offsets)
    # returns new dataset
    
    data2 = data.copy()
    
    if 'offsets' in spice:
        for k, v in spice['offsets'].items():
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


def sRSM(data, **spice):
    '''
    Generating static reciprocal space maps (RSMs).

    Requires `exp_info` spice. Also performs basic data mangling
    if appropriate spice types (`offsets`) available, and
    modifies exp_info if exp_info modifiers (`image`) also available.

    "Static" RSMs don't depend on any external parameters.
    '''
    data2 = _kmc3_recipe_helper_datamangle(data, **spice)
    expi2, qpar = _kmc3_recipe_helper_expimangle(spice['exp_info'], **spice)
    return QMapper(**expi2).qmap(data2, **qpar)


def TRSM(data, **spice):
    '''
    Generating temperature (T) dependent RSMs, uses 'temp' dataset
    '''
    from nx5d.xrd.signal import QMapper
    data2 = _kmc3_recipe_helper_datamangle(data, **spice)
    expi2, qpar = _kmc3_recipe_helper_expimangle(spice['exp_info'], **spice)

    data2['temp'] = data2.temp.round()
        
    return data2.groupby('temp').map(QMapper(**expi2).qmap, **qpar)


def rocking(data, **spice):
    raise RuntimeError('recipe for rocking data not implemented')

