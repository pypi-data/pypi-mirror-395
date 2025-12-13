#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Date          : 2025-11-16
# Author        : Lancelot PINCET
# GitHub        : https://github.com/LancelotPincet
# Library       : plotLP
# Module        : color

"""
Gets a custom Color object.
"""



# %% Libraries
from dataclasses import dataclass
import matplotlib.colors as mcolors



colors = {

    #Greys
    'xxdarkgreyLP' : "#1A1A1AFF", 
    'xdarkgreyLP' : "#404040FF", 
    'darkgreyLP' : "#606060FF", 
    'greyLP' : "#808080FF", 
    'lightgreyLP' : "#9F9F9FFF", 
    'xlightgreyLP' : "#BFBFBFFF", 
    'xxlightgreyLP' : "#E6E6E6FF", 

    #Blue
    'darkblueLP' : "#1F4B5BFF",
    'blueLP' : "#2F7089FF", 
    'lightblueLP' :  "#598DA1FF",
    'xlightblueLP' : "#82A9B8FF", 
    'xxlightblueLP' : "#ACC6D0FF", 

    #Green
    'xxdarkgreenLP' : "#294C3AFF", 
    'xdarkgreenLP' : "#3E725BFF", 
    'darkgreenLP' : "#529878FF", 
    'greenLP' : "#68BE95FF", 
    'lightgreenLP' : "#9AD4B8FF", 

    #Red
    'darkredLP' : "#8F1E20FF", 
    'redLP' : "#D52D2FFF", 
    'lightredLP' : "#DE5758FF", 
    'xlightredLP' : "#E68181FF", 
    'xxlightredLP' : "#EFABADFF", 

    #Yellow
    'xxdarkyellowLP' : "#4D4212FF", 
    'xdarkyellowLP' : "#746317FF", 
    'darkyellowLP' : "#9A8420FF", 
    'yellowLP' : "#C1A529FF", 
    'lightyellowLP' : "#D6C36FFF", 

    #Cold
    'xdarkcoldLP' : "#264C46FF", 
    'darkcoldLP' : "#39716CFF", 
    'coldLP' : "#4C978FFF", 
    'lightcoldLP' : "#78B1AAFF", 
    'xlightcoldLP' : "#D3E5E4FF", 

    #Warm
    'xdarkwarmLP' : "#653517FF", 
    'darkwarmLP' : "#994F20FF", 
    'warmLP' : "#CB692CFF", 
    'lightwarmLP' : "#D88F60FF", 
    'xlightwarmLP' : "#E6B495FF", 

    }
mcolors.CSS4_COLORS.update(colors)
mcolors._colors_full_map.update(colors)



# %% Function
def color(*, name:str=None, hex:str=None, wl:float=None, gray:int=None, rgb:tuple=None, RGB:tuple=None, auto=None, alpha:float=None) :
    '''
    Gets a custom Color object.
    
    Parameters
    ----------
    name : str
        Name of color.
    hex : str
        hexadecimal string.
    wl : str
        wavelength [nm] float.
    gray : str
        gray luminosity [0-255].
    rgb : tuple
        rgb(a) tuple [0.-1.].
    RGB : tuple
        RGB(A) tuple [0-255].
    auto : str or tuple or int or float
        Defines what is asked automatically.
    

    Returns
    -------
    instance : Color
        Color object instance.

    Examples
    --------
    >>> from plotlp import color
    ...
    >>> color(name="blue") # from plt
    >>> color(name="blueLP") # from custom
    >>> color(hex="#2F7089") # from hexadecimals
    >>> color(wl=480) # from wavelenght
    >>> color(gray=180) # from grayscale
    >>> color(rgb=(0, 0, 255)) # from RGB
    ...
    >>> blued, greened = color(name="blueLP")
    >>> desaturated = blued.desaturate(0.5) # 1=completely gray
    >>> dark = blued.luminosity(-0.5) # <0 darker down to -1
    >>> light = blued.luminosity(+0.5) # >0 lighter up to +1
    >>> transparent = blued * 0.5 # color * alpha
    >>> opaque = +blued
    >>> invisible = -blued
    >>> mixed = blued.mix(greened, 0.5) # 50/50 mixing blue/green
    >>> complementary = ~blued # complementary color
    '''

    # Name
    if name is not None :
        r, g, b = mcolors.to_rgb(name)
        return color(rgb=(r*255, g*255, b*255), alpha=alpha)
    
    # Hexadecimals
    if hex is not None :
        if hex.startswith('#') :
            hex = hex[1:]
        _alpha = int(hex[6:8], 16)/255 if len(hex)==8 else None
        alpha = _alpha if alpha is None else alpha
        return color(rgb=(int(hex[0:2],16), int(hex[2:4],16), int(hex[4:6], 16)), alpha=alpha)

    # Wavelength
    if wl is not None :
        gamma = 0.8
        wl = min(max(float(wl),380.),750.) #Wavelength is put to borders
        if wl >= 380 and wl <= 440:
            attenuation = 0.3 + 0.7 * (wl - 380) / (440 - 380)
            r, g, b = ((-(wl - 440) / (440 - 380)) * attenuation) ** gamma, 0.0, (1.0 * attenuation) ** gamma
        elif wl >= 440 and wl <= 490:
            r, g, b = 0.0, ((wl - 440) / (490 - 440)) ** gamma, 1.0
        elif wl >= 490 and wl <= 510:
            r, g, b = 0.0, 1.0, (-(wl - 510) / (510 - 490)) ** gamma
        elif wl >= 510 and wl <= 580:
            r, g, b = ((wl - 510) / (580 - 510)) ** gamma, 1.0, 0.0
        elif wl >= 580 and wl <= 645:
            r, g, b = 1.0, (-(wl - 645) / (645 - 580)) ** gamma, 0.0
        elif wl >= 645 and wl <= 750:
            attenuation = 0.3 + 0.7 * (750 - wl) / (750 - 645)
            r, g, b = (1.0 * attenuation) ** gamma, 0.0, 0.0
        else:
            r, g, b = 0.0, 0.0, 0.0
        return color(rgb=(r*255, g*255, b*255), alpha=alpha)

    # gray
    if gray is not None :
        return color(rgb=(gray, gray, gray), alpha=alpha)

    # rgb
    if rgb is not None :
        _alpha = rgb[3] if len(rgb)==4 else 1.
        alpha = _alpha if alpha is None else alpha
        return Color(rgb[0]*255, rgb[1]*255, rgb[2]*255, alpha=alpha)

    # RGB
    if RGB is not None :
        _alpha = RGB[3]/255 if len(RGB)==4 else 1.
        alpha = _alpha if alpha is None else alpha
        return Color(RGB[0], RGB[1], RGB[2], alpha=alpha)

    # Auto
    if auto is not None :
        if isinstance(auto, str) :
            if auto.startswith('#') : return color(hex=auto, alpha=alpha)
            else : return color(name=auto, alpha=alpha)
        elif isinstance(auto, tuple) or isinstance(auto, list) :
            if max(*auto) <= 1 : return color(rgb=auto, alpha=alpha)
            else : return color(RGB=auto, alpha=alpha)
        else : # int/float
            if auto <= 255 : return color(gray=auto, alpha=alpha)
            else : return color(wl=auto, alpha=alpha)

    raise SyntaxError('No valid input was asked for color')



# %% Class
@dataclass(slots=True, frozen=True)
class Color(str) :
    '''
    Gets a custom Color object.
    
    Parameters
    ----------
    R : float
        Red value [0-255].
    G : float
        Green value [0-255].
    B : float
        Blue value [0-255].
    alpha : float
        Alpha value [0-1] (0: transparent, 1: opaque).

    Attributes
    ----------
    _attr : int or float
        TODO.

    Examples
    --------
    >>> from plotlp import color
    ...
    >>> instance = color(TODO)
    '''

    # Attributes
    R : int
    G : int
    B : int
    alpha : float = 1.



    # new
    def __new__(cls, R, G, B, alpha=1) :
        hex = '#{:02x}{:02x}{:02x}{:02x}'.format(int(R), int(G), int(B), int(alpha*255)).upper()
        instance = str.__new__(cls, hex)
        object.__setattr__(instance, 'R', int(R))
        object.__setattr__(instance, 'G', int(G))
        object.__setattr__(instance, 'B', int(B))
        object.__setattr__(instance, 'alpha', float(alpha))
        return instance

    # RGBA
    @property
    def RGB(self) :
        return (self.R, self.G, self.B)
    @property
    def RGBA(self) :
        return (self.R, self.G, self.B, int(self.alpha * 255))

    # rgba
    @property
    def r(self) :
        return self.R / 255
    @property
    def g(self) :
        return self.G / 255
    @property
    def b(self) :
        return self.B / 255
    @property
    def a(self) :
        return self.A / 255
    @property
    def rgb(self) :
        return (self.r, self.g, self.b)
    @property
    def rgba(self) :
        return (self.r, self.g, self.b, self.a)

    # greys
    @property
    def K(self) :
        return int(0.299 * self.R + 0.587 * self.G + 0.114 * self.B)
    @property
    def k(self) :
        return self.K / 255


    
    #Complementary color
    def __invert__(self) : # ~color
        return Color(255-self.R, 255-self.G, 255-self.B, alpha=self.alpha)

    #Play on transparency
    def __mul__(self, alpha) : # color * alpha
        return Color(*self.RGB, alpha=alpha)
    def __pos__(self) : # +color
        return Color(self.RGB, alpha=1)
    def __neg__(self) : # -color
        return Color(self.RGB, alpha=0)

    # color mixing
    def mix(self, other_color, other_fact=0.5) :
        self_fact = 1 - other_fact
        R = self.R * self_fact + other_color.R * other_fact
        G = self.G * self_fact + other_color.G * other_fact
        B = self.B * self_fact + other_color.B * other_fact
        return Color(R, G, B, alpha=self.alpha)
    #Desaturation
    def desaturate(self, fact) : # desat [0-1]
        gray = Color(self.K, self.K, self.K)
        return self.mix(gray, fact)
    #luminosity
    def luminosity(self, fact) : # desat [-1, +1]
        k = int(fact>=0) * 255
        lum = Color(k, k, k)
        return self.mix(lum, abs(fact))



# %% Test function run
if __name__ == "__main__":
    from corelp import test
    test(__file__)