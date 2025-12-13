import importlib
import pytest

def _ensure_dependencies():
    is_mpl = importlib.util.find_spec("matplotlib") is not None
    is_scilightcon = importlib.util.find_spec("scilightcon") is not None

    if not is_mpl:
        print("matplotlib package must be installed for lightcon.style routines. Alternatively, use scilightcon.plot")
    
    if not is_scilightcon:
        print("scilightcon package must be installed for lightcon.style routines. Alternatively, use scilightcon.plot")

    if is_mpl and not is_scilightcon:
        print("setting all scilightcon style cmaps to viridis")
        try:
            _apply_fallback_cmaps()
        except:
            pass

    return is_mpl and is_scilightcon

def _apply_fallback_cmaps():
    import matplotlib as mpl

    if hasattr(mpl.colormaps, 'get_cmap'):
        viridis = mpl.colormaps.get_cmap('viridis')
    else:
        viridis = mpl.cm.get_cmap('viridis')
    
    names = ["RdYlGnBu", "beam_profile", "LCBeamProfiler", "morgenstemning"]

    for name in names:
        if hasattr(mpl.colormaps, 'register'):
            mpl.colormaps.register(viridis, name=name)
        else:
            mpl.cm.register_cmap(name, viridis)

def apply_style():
    if not _ensure_dependencies():
        return
    
    import matplotlib.pyplot as plt
    import scilightcon.plot
    scilightcon.plot.apply_style()

def reset():
    if not _ensure_dependencies():
        return
    
    import matplotlib.pyplot as plt
    import scilightcon.plot
    scilightcon.plot.reset_style()

def add_watermarks():
    """Adds watermarks to all subplots of the current figure"""
    if not _ensure_dependencies():
        return
    
    import matplotlib.pyplot as plt
    import scilightcon.plot
    scilightcon.plot.add_watermarks(plt.gcf())

def add_watermark(ax, target='axis', loc='lower left'):
    """Add watermark to current axis or figure

    Args:
        ax (:obj:`str`): Axis object (not relevant if target=='figure')
        target (:obj:`str`): Draw axis for the whole 'figure' (default) or 'axis'
        loc (:obj:`str`): Location of the watermark ('upper right'|'upper left'|'lower left'|'lower right'|'center left'|'center right'|'lower center'|'upper center'|'center').
            Default value is 'center' when target=='figure' and 'lower left' for target=='axis'
    """
    if not _ensure_dependencies():
        return
    
    import matplotlib.pyplot as plt
    import scilightcon.plot

    if target == 'axis':
        scilightcon.plot.add_watermark(ax)
        
    if target == 'figure':
        scilightcon.plot.add_watermark(plt.gcf())