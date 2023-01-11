from vbmc import vbmc
import numpy as np

def test_vbmc():
    model = vbmc(nPh = 1e5)
    assert model.build()
    assert model.start()
    Rd,Td = model.getRdTtRate()
    assert (Rd>0.0963)&(Rd<0.0990)
    assert (Td>0.658)&(Td<0.663)

def test_params_setting():
    model = vbmc(nPh = 100)
    params = {
            'n':[1.37,1.37,1.37],
            'n_air':1.,
            'ma':[1,1,2],
            'ms':[100,10,10],
            'g':[0.9,0.,0.7],
            'end_point':False,#Basically, set it to False.
            'voxel_space':0.1,
    }
    voxel_model = np.zeros((1001,1001,4))
    voxel_model[:,:,1] = 1
    voxel_model[:,:,2:] = 2

    assert model.set_model(voxel_model)
    assert model.set_params(**params)
    for i in params:
        assert model.model.params[i] == params[i]

    params = {
            'n':[1.37,1.,1.37],
            'n_air':1.,
            'ma':[1,1,1],
            'ms':[10,10,10],
            'g':[0.9,0.,0.7],
            'end_point':False,#Basically, set it to False.
            'voxel_space':0.1,
    }
    assert model.set_params(params)
    for i in params:
        assert model.model.params[i] == params[i]

    assert model.build()
    assert model.start()

def test_wbeam():
    w_beam = 0.5
    model = vbmc(w_beam = w_beam,nPh = 1e5)
    assert model.build()
    assert model.start()


def test_beam_angle():
    beam_angle = 0.174533

    model = vbmc(beam_angle = beam_angle,nPh = 100)
    assert model.build()
    assert model.start()

def test_first_layer_clear():
    first_layer_clear = 1
    model = vbmc(
        first_layer_clear = first_layer_clear,
        nPh = 100
        )
    params = {
            'n':[1.37,1.37,1.37],
            'n_air':1.,
            'ma':[1,1,2],
            'ms':[100,10,10],
            'g':[0.9,0.,0.7],
            'end_point':False,
            'voxel_space':0.1,
    }
    voxel_model = np.zeros((1001,1001,4))
    voxel_model[:,:,1] = 1
    voxel_model[:,:,2:] = 2
    assert model.set_model(voxel_model)
    assert model.set_params(**params)

    assert model.build()
    assert model.start()

def test_set_monte_params():
    model = vbmc(nPh = 100)
    params = {
            'n':[1.37,1.37,1.37],
            'n_air':1.,
            'ma':[1,1,2],
            'ms':[100,10,10],
            'g':[0.9,0.,0.7],
            'end_point':False, # Basically, set it to False.
            'voxel_space':0.1,
    }
    voxel_model = np.zeros((1001,1001,4))
    voxel_model[:,:,1] = 1
    voxel_model[:,:,2:] = 2

    nPh = 1e4
    w_beam = 0.01
    beam_angle = 0.174533
    first_layer_clear = 1

    assert model.set_monte_params(
        first_layer_clear = first_layer_clear,
        nPh = nPh,
        w_beam = w_beam,
        beam_angle = beam_angle,
        )

    assert model.nPh == nPh
    assert model.w_beam == w_beam
    assert model.beam_angle == beam_angle
    assert model.first_layer_clear == first_layer_clear

    assert model.set_model(voxel_model)
    assert model.set_params(**params)

    assert model.build()
    assert model.start()
