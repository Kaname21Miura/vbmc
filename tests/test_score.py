from vmc import vmc
from vmc import angularyResolved,spatiallyResolved
import numpy as np
import pandas as pa

#assert pa.read_csv('.docs/mcml_result_singlelyer_rda_tda.csv')
df = pa.read_csv('docs/mcml_result_singlelyer_rda_tda.csv')
df2 = pa.read_csv('docs/mcml_result_multilayer_rdr_tdr.csv')

def test_single():
    nPh = 1e6
    model = vbmc(nPh = nPh)
    assert model
    assert model.build()
    assert model.start()
    res = model.get_result()
    Rd_index = np.where(res['v'][:,2] < 0)[0]
    Td_index = np.where(res['v'][:,2] > 0)[0]
    alpha,rda = angularyResolved(
        res['v'][Rd_index],res['w'][Rd_index],nPh,30
    )
    alpha,tda = angularyResolved(
        res['v'][Td_index],res['w'][Td_index],nPh,30
    )
    assert rda.dtype == np.float64
    assert tda.dtype == np.float64
    assert abs(np.mean(df.Rd_a.values-rda)) < .002
    assert abs(np.mean(df.Td_a.values-tda)) < .002

def test_multiple():
    nPh = 1e6
    model = vbmc(nPh = nPh)
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

    model.build()
    model.start()

    res = model.get_result()
    Rd_index = np.where(res['v'][:,2] < 0)[0]
    Td_index = np.where(res['v'][:,2] > 0)[0]

    dr = 0.005
    nn = 100
    rr,Rd_r = spatiallyResolved(
        res['p'][Rd_index],res['w'][Rd_index],nPh,nn,dr
    )
    rr,Td_r = spatiallyResolved(
        res['p'][Td_index],res['w'][Td_index],nPh,nn,dr
    )
    assert abs(np.mean(np.log(df2.Rd_r.values)-np.log(Rd_r))) < .005
    assert abs(np.mean(np.log(df2.Td_r.values)-np.log(Td_r))) < .005
