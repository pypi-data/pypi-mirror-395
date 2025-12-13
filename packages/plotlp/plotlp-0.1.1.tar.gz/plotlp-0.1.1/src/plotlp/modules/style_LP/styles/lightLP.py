from cycler import cycler
from plotlp import color

base = "styleLP"
style = {
    'axes.prop_cycle' : cycler(color=[color(name=c) for c in ['blueLP','darkgreenLP','darkyellowLP','redLP','darkcoldLP','darkwarmLP','greyLP','black','xxlightgreyLP','white']]), #color cycle for plot lines as list of string colorspecs: single letter, long name, or web-style hex
    }