#!/usr/bin/python3

import pytest, h5py, numpy, xarray, random, math
from xraydc.signal import QMapper
    
# It's difficult (impossible?) to actually test whether QMapper
# truly delivers physically correct results. What we're focusing
# on here primarily is testing whether the interface behaves as
# expected, and data dimensionality is as we want it to be.

@pytest.fixture
def num_imgs():
    return random.randint(50, 100)

@pytest.fixture
def img_size():
    return (random.randint(128, 256),
            random.randint(256, 512))

@pytest.fixture
def raw_rsm_data(num_imgs, img_size):
    # Returns a Dataset with image and angle data as if for
    # static RSMs. 

    # This is to create a more interesting test pattern using
    # 3D trigonometric functions. (Note that these are intensities,
    # so we might want to go for positive-only values?...)
    # Adjust stat/stop points to change frequencies in each dimension.
    coords = numpy.meshgrid(numpy.linspace(0, math.pi, num_imgs),
                            numpy.linspace(0, math.pi, img_size[0]),
                            numpy.linspace(0, math.pi, img_size[1]),
                            indexing='ij')

    s = 1e3*\
        numpy.sin(coords[0])*\
        numpy.sin(coords[1])*\
        numpy.sin(coords[2])

    return xarray.Dataset({
        'images': (('index', 'images_w', 'images_h'), s),
        'phi':    ('index', numpy.array([.0]*num_imgs)),
        'chi':    ('index', numpy.array([.0]*num_imgs)),
        'theta':  ('index', numpy.array(range(num_imgs))*0.01 + 12.0),
        'tth':    ('index', numpy.array(range(num_imgs))*0.01 + 24.0)
    })

@pytest.fixture
def exp_info_yxz(img_size):
    # Returns an experimental setup dict with a coordinate system
    # similar to KMC3-XPP, i.e. the following coordinates
    #  - x: sample in-plane axis
    #  - y: x-ray direction    
    #  - z: sample normal axis
    #
    # 4-circle goniometer (theta, chi, phi from outer to inner)

    return {
        # All the axes -- goniometer first (outer to inner), then detector.
        "goniometerAxes": {  'theta': 'x+',  'chi': 'y+',  'phi': 'z+'  },
        "detectorAxes": { 'tth': 'x+', },
        "detectorTARAlign": (0.0, 0.0, 0.0),
        "imageAxes": ("x-", "z-"),
        "imageSize": img_size,
        "imageCenter": (int(img_size[0]/2), int(img_size[1]/2)),
        "imageDistance": 680.0,
        "imageChannelSize": (0.172, 0.172),
        "sampleFaceUp": 'z+',
        "beamDirection": (0, 1, 0),
        "sampleNormal": (0, 0, 1),
        "beamEnergy": 10000.0,
    }


@pytest.fixture
def exp_info_xyz(img_size):
    # Returns an experimental setup dict with a coordinate system
    # configuration similar to UDKM:
    #   - x: x-ray axis
    #   - y: sample in-plane axis
    #   - z: sample normal axis
    #
    # 2-circle goniometer (i.e. only theta / 2-theta, no chi/phi)
    #
    # Beam energy is set to 10 kV, same as the other exp_info fixture(s)
    # for better comparison.
    #
    # This is needed to test Q-axis assignment of QMapper after
    # gridding. (Yes, there was a bug concerning this once upon a
    # time...)

    return {
        "goniometerAxes": { 'theta': 'y-', },
        "detectorAxes": {  'ttheta': 'y-',  },
        "detectorTARAlign": (0.0, 0.0, 0.0),
        "imageAxes": ("y-", "z+"),
        "imageSize": img_size,
        "imageCenter": (int(img_size[0]/2), int(img_size[1]/2)),
        "imageDistance": 680.0,
        "imageChannelSize": (0.172, 0.172),
        "sampleFaceUp": 'z-',
        "beamDirection": (1, 0, 0),
        "sampleNormal": (0, 0, -1),
        "beamEnergy": 10000.0,
    }


def test_qmapper(raw_rsm_data, exp_info_yxz, exp_info_xyz):

    ## full image
    q1 = QMapper(**exp_info_yxz)\
        .qmap(raw_rsm_data)

    ## only ROI
    q2 = QMapper(**exp_info_yxz, roi=(0, 100, 0, 200))\
        .qmap(raw_rsm_data.isel(images_w=slice(0,100),
                                images_h=slice(0,200)))

    #print(rsm)
