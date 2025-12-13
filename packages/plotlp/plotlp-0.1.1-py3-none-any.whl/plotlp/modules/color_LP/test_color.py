#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date          : 2025-11-16
# Author        : Lancelot PINCET
# GitHub        : https://github.com/LancelotPincet
# Library       : plotLP
# Module        : color

"""
This file allows to test color

color : Gets a custom Color object.
"""



# %% Libraries
from corelp import print, debug
import pytest
from plotlp import color
from matplotlib import pyplot as plt
import numpy as np
debug_folder = debug(__file__)



# %% Function test
def save_color(pos, name, color, prefix) :
    '''
    save a color
    '''
    figure = plt.figure()
    plt.imshow(np.asarray([[color.RGBA]]))
    plt.savefig(debug_folder / f'{prefix}_{pos:02}_{name}_[{color}={color.k*100:.1f}%].png')
    plt.close(figure)



# %% name test
@pytest.mark.parametrize("wl", [i for i in range(200, 1001, 25)])
def test_wl(wl) :
    '''
    Test color with name values
    '''
    c = color(wl=wl)
    save_color(wl, wl, c, "wl")



# %% name test
@pytest.mark.parametrize("gray", [i for i in range(0, 256, 32)])
def test_gray(gray) :
    '''
    Test color with name values
    '''
    c = color(gray=gray)
    save_color(gray, gray, c, "gray")



# %% name test
@pytest.mark.parametrize("hex, pos", [
    #(hex, pos),
    ("#808080FF", 0),
    ("#2F7089FF", 1),
    ("#68BE95FF", 2),
])
def test_hex(hex, pos) :
    '''
    Test color with name values
    '''
    c = color(hex=hex)
    save_color(pos, hex, c, "hex")



# %% Returns test
@pytest.mark.parametrize("name, pos", [
    #name,
    ('xxdarkgreyLP', 0), 
    ('xdarkgreyLP', 1),
    ('darkgreyLP', 2),
    ('greyLP', 3),
    ('lightgreyLP', 4),
    ('xlightgreyLP', 5),
    ('xxlightgreyLP', 6),
    ('darkblueLP', 7),
    ('blueLP', 8),
    ('lightblueLP', 9),
    ('xlightblueLP', 10),
    ('xxlightblueLP', 11),
    ('xxdarkgreenLP', 12),
    ('xdarkgreenLP', 13),
    ('darkgreenLP', 14),
    ('greenLP', 15),
    ('lightgreenLP', 16),
    ('darkredLP', 17),
    ('redLP', 18),
    ('lightredLP', 19),
    ('xlightredLP', 20),
    ('xxlightredLP', 21),
    ('xxdarkyellowLP', 22),
    ('xdarkyellowLP', 23),
    ('darkyellowLP', 24),
    ('yellowLP', 25),
    ('lightyellowLP', 26),
    ('xdarkcoldLP', 27),
    ('darkcoldLP', 28),
    ('coldLP', 29),
    ('lightcoldLP', 30),
    ('xlightcoldLP', 31),
    ('xdarkwarmLP', 32),
    ('darkwarmLP', 33),
    ('warmLP', 34),
    ('lightwarmLP', 35),
    ('xlightwarmLP', 36),
    ('r', 37),
    ('g', 38),
    ('b', 39),
    ('k', 40),
    ('w', 41),

])
def test_name(name, pos) :
    '''
    Test color with name values
    '''
    c = color(name=name)
    save_color(pos, name, c, "name")



# %% Test function run
if __name__ == "__main__":
    from corelp import test
    test(__file__)