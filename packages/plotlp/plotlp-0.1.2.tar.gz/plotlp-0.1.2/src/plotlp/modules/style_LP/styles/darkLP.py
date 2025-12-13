from cycler import cycler
from plotlp import color

base = "styleLP"
style = {
    'axes.prop_cycle' : cycler(color=[color(name=c) for c in ['lightblueLP','greenLP','yellowLP','lightredLP','lightcoldLP','lightwarmLP','greyLP','white','xxdarkgreyLP','black']]), #color cycle for plot lines as list of string colorspecs: single letter, long name, or web-style hex'
    }