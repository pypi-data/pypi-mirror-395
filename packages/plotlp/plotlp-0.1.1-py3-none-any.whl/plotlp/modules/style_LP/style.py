#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date          : 2025-11-16
# Author        : Lancelot PINCET
# GitHub        : https://github.com/LancelotPincet
# Library       : plotLP
# Module        : style

"""
This module defines style informations for matplotlib.
"""



# %% Libraries
import importlib
from pathlib import Path
import matplotlib.pyplot as plt



# %% Function
def style(name:str="plt") :
    '''
    This module defines style informations for matplotlib.
    
    Parameters
    ----------
    name : str
        Name of style to get.

    Returns
    -------
    style_dict : dict
        style dictionnary.

    Raises
    ------
    SyntaxError
        if asked style does not exist.

    Examples
    --------
    >>> from plotlp import style
    ...
    >>> lightstyle = style("lightLP) # dict
    >>> darkstyle = style("darkLP) # dict
    '''

    if name not in styles and name not in plt.style.library :
        raise SyntaxError(f'{name} was not recognized as a valid style, please chose in : {styles+list(plt.style.library.keys())}')
    
    dic = get_dict(name)

    # Update colors
    colors = list(dic['axes.prop_cycle'])
    for key, value in dic.items() :
        if isinstance(value,str) and value.startswith('C') and len(value) == 2 :
            dic[key] = colors[int(value[-1])]['color']
    return dic


styles = sorted([file.stem for file in (Path(__file__).parent / "styles").iterdir() if not file.name.startswith("__")])
def get_dict(name) :
    if name in styles :
        module = importlib.import_module(f".styles.{name}", package=__package__)
        base = getattr(module, "base")
        style = getattr(module, "style")
        main_dict = {} if base is None else get_dict(base)
        main_dict.update(style)
        return main_dict
    return dict(plt.style.library[name])



# %% Test function run
if __name__ == "__main__":
    from corelp import test
    test(__file__)