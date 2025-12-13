#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date          : 2025-11-17
# Author        : Lancelot PINCET
# GitHub        : https://github.com/LancelotPincet
# Library       : plotLP
# Module        : cmap

"""
This module adds custom cmaps to matplotlib.
"""



# %% Libraries
from corelp import selfkwargs, prop
from arrLP import normalize
from plotlp import color
from matplotlib.colors import LinearSegmentedColormap, to_rgba_array
import numpy as np
from scipy.special import erf,erfinv



# %% Function
def cmap(**kwargs) :
    '''
    This module adds custom cmaps to matplotlib.
    
    Parameters
    ----------
    a : int or float
        TODO.

    Returns
    -------
    b : int or float
        TODO.

    Raises
    ------
    TypeError
        TODO.

    Examples
    --------
    >>> from plotlp import cmap
    ...
    >>> cmap() # TODO
    '''

    return None



class Cmap(LinearSegmentedColormap) :
    name = 'cmapLP'

    def __init__(self, **kwargs) :
        selfkwargs(self,kwargs)
        r, g, b, a = to_rgba_array(self.colors).T
        nodes = self.nodes
        cdict = {
            "red": np.column_stack([nodes, r, r]),
            "green": np.column_stack([nodes, g, g]),
            "blue": np.column_stack([nodes, b, b]),
            "alpha": np.column_stack([nodes, a, a]),
        }
        super().__init__(self.name,cdict)

    _black = 'black'
    @prop(variable=True)
    def black(self) -> str :
        if self._black is None :
            return color(rgb=self(self.get_node(0.)))
        return color(auto=self._black)

    _white =  'white'
    @prop(variable=True)
    def white(self) -> str :
        if self._white is None :
            return color(rgb=self(self.get_node(1.)))
        return color(auto=self._white)

    _color = None
    @prop(variable=True)
    def color(self) :
        if self._color is None :
            return color(rgb=self(self.get_node(0.5)))
        return color(auto=self._color)

    _dark = None #dark color
    @prop(variable=True)
    def dark(self) -> str :
        if self._dark is None :
            return color(self(self.get_node(0.25)))
        return color(self._dark)

    _light = None #light color
    @prop(variable=True)
    def light(self) -> str :
        if self._light is None :
            return color(self(self.get_node(0.75)))
        return color(self._light)

    _colors = None #list of colors
    @prop()
    def colors(self) -> str :
        return [self.black,self.dark,self.color,self.light,self.white]
    @colors.setter
    def colors(self, value) -> float :
        self._colors = [color(auto=color) for color in value]
    @property
    def ncolors(self) :
        return len(self.colors)

    _nodes = None #nodes corresponding to colors
    @prop()
    def nodes(self) -> str :
        nodes = np.linspace(0.,1.,self.ncolors)
        return self.get_node(nodes)
    nodebase = 0 #Base defining distribution of colors around center based on erf function, when approching 0 the function tends towards linear distribution
    def get_node(self,node) :
        if self.nodebase == 0 : return node
        node = (erfinv(normalize(node,-erf(self.nodebase),erf(self.nodebase),offset=0,norm=1))/self.nodebase+1)/2
        return (np.round(node * 1000)).astype(int)/1000


# %% Test function run
if __name__ == "__main__":
    from corelp import test
    test(__file__)