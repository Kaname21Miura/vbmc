from vbmc import vbmc

def test_vbmc():
    model = vbmc()
    assert model.build()
    assert model.start()
    Rd,Td = model.getRdTtRate()
    assert (Rd>0.0963)&(Rd<0.0990)
    assert (Td>0.658)&(Td<0.663)
    
