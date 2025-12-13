#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date          : 2025-11-17
# Author        : Lancelot PINCET
# GitHub        : https://github.com/LancelotPincet
# Library       : plotLP
# Module        : cmap

"""
This file allows to test cmap

cmap : This module adds custom cmaps to matplotlib.
"""



# %% Libraries
from corelp import print, debug
import pytest
from plotlp import cmap
debug_folder = debug(__file__)



# %% Function test
def test_function() :
    '''
    Test cmap function
    '''
    print('Hello world!')



# %% Instance fixture
@pytest.fixture()
def instance() :
    '''
    Create a new instance at each test function
    '''
    return cmap()

def test_instance(instance) :
    '''
    Test on fixture
    '''
    pass


# %% Returns test
@pytest.mark.parametrize("args, kwargs, expected, message", [
    #([], {}, None, ""),
    ([], {}, None, ""),
])
def test_returns(args, kwargs, expected, message) :
    '''
    Test cmap return values
    '''
    assert cmap(*args, **kwargs) == expected, message



# %% Error test
@pytest.mark.parametrize("args, kwargs, error, error_message", [
    #([], {}, None, ""),
    ([], {}, None, ""),
])
def test_errors(args, kwargs, error, error_message) :
    '''
    Test cmap error values
    '''
    with pytest.raises(error, match=error_message) :
        cmap(*args, **kwargs)



# %% Test function run
if __name__ == "__main__":
    from corelp import test
    test(__file__)