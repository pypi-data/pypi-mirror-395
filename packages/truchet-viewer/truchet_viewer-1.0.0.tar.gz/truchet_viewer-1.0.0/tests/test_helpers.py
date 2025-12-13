from truchet_viewer.helpers import hex_to_rgb, make_bgfg


def test_hex_to_rgb():
    assert hex_to_rgb('#ffffff') == (1.0, 1.0, 1.0)
    assert hex_to_rgb('#000000') == (0.0, 0.0, 0.0)
    assert hex_to_rgb('#ff0000') == (1.0, 0.0, 0.0)
    assert hex_to_rgb('#00ff00') == (0.0, 1.0, 0.0)
    assert hex_to_rgb('#0000ff') == (0.0, 0.0, 1.0)
    assert hex_to_rgb('#123456') == (18 / 255, 52 / 255, 86 / 255)


def test_make_bgfg():
    result = make_bgfg(0.5, [0.2, 0.8], 1.0)
    assert 'bg' in result
    assert 'fg' in result
    assert isinstance(result['bg'], tuple) and len(result['bg']) == 3
    assert isinstance(result['fg'], tuple) and len(result['fg']) == 3
