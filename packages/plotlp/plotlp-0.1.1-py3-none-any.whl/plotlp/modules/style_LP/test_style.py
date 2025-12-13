#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date          : 2025-11-16
# Author        : Lancelot PINCET
# GitHub        : https://github.com/LancelotPincet
# Library       : plotLP
# Module        : style

"""
This file allows to test style

style : This module defines style informations for matplotlib.
"""



# %% Libraries
from corelp import print, debug
import pytest
from plotlp import style
from matplotlib import pyplot as plt
import numpy as np
debug_folder = debug(__file__)



# %% Returns test
@pytest.mark.parametrize("name, ", [
    #(name, ),
    "default",
    "ggplot",
    "lightLP",
    "darkLP",
])
def test_returns(name) :
    '''
    Test style return values on a plot
    '''
    x = np.linspace(0,4*np.pi,20)
    err = 0.1
    X,Y = np.meshgrid(x,x)

    with plt.style.context(style(name)):
        
        figure,axe = plt.subplots(nrows=2,ncols=2)
        figure.suptitle(name)
        #0,0
        plt.sca(axe[0,0])
        plt.errorbar(x,np.sin(x),xerr=err,yerr=err,linestyle='',label='errorbar')
        for xx in x :
            plt.scatter(xx,np.sin(xx))
        plt.xlabel('x param')
        plt.ylabel('y param')
        plt.grid(which='major',linestyle='-',color='C8')
        plt.grid(which='minor',linestyle=':',color='C8')
        plt.legend()
        plt.title('plot')
        #0,1
        plt.sca(axe[0,1])
        plt.grid(which='major',linestyle='-',color='C8')
        plt.grid(which='minor',linestyle=':',color='C8')
        plt.bar(x,np.sin(x))
        plt.xlabel('x param')
        plt.ylabel('y param')
        plt.title('barplot')
        #1,0
        plt.sca(axe[1,0])
        plt.imshow(X)
        plt.colorbar()
        plt.title('imshow')
        #1,1
        plt.sca(axe[1,1])
        plt.grid(which='major',linestyle='-',color='C8')
        plt.grid(which='minor',linestyle=':',color='C8')
        plt.fill_between(x,np.sin(x),0)
        plt.fill_between(x,np.cos(x),0)
        plt.title('fillbetween')
        plt.xlabel('x param')
        plt.ylabel('y param')
        #End
        plt.savefig(debug_folder/f'{name}.png',transparent=False)
        plt.close(figure)
    



# %% Test function run
if __name__ == "__main__":
    from corelp import test
    test(__file__)