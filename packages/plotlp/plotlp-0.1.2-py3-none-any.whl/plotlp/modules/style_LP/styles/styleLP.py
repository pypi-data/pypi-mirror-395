base = "default"
style = {

    'agg.path.chunksize': 10000, #0 to disable; values in the range 10000 to 100000 can improve speed slightly and prevent an Agg rendering failure when plotting very large data sets, especially if they are very gappy. It may cause minor artifacts, though. A value of 20000 is probably a good starting point.
    'axes.axisbelow' : True, #whether axis gridlines and ticks are below the axes elements (lines, text, etc)
    'axes.edgecolor' : 'C7', #axes edge color
    'axes.facecolor' : 'C9', #axes background color
    'axes.labelcolor' : 'C7',
    'axes.formatter.use_mathtext' : True, #When True, use mathtext for scientific notation.
    'axes.formatter.useoffset' : False, #If True, the tick label formatter will default to labeling ticks relative to an offset when the data range is very small compared to the minimum absolute value of the data.
    'boxplot.boxprops.color' : 'C7',
    'boxplot.capprops.color' : 'C7',
    'boxplot.flierprops.color' : 'C7',
    'boxplot.flierprops.markeredgecolor' : 'C7',
    'boxplot.meanprops.markerfacecolor' : 'C2',
    'boxplot.meanprops.markeredgecolor' : 'C2',
    'boxplot.meanprops.color' : 'C2',
    'boxplot.medianprops.color' : 'C1',
    'boxplot.whiskerprops.color' : 'C7',
    'errorbar.capsize' : 2, #length of end cap on error bars in pixels
    'figure.dpi' : 50, #figure dots per inch
    'figure.facecolor' : 'C9', #figure facecolor
    'figure.figsize' : [6.4, 6.4 / (1 + 5 ** 0.5) * 2], #figure size in inches
    'figure.edgecolor' : 'C9', #figure edgecolor
    'grid.color' : 'C8', #grid color
    'hatch.color' : 'C7',
    'image.cmap' :'coldLP',
    'legend.edgecolor' : 'none', #legend edge color (when 'inherit' uses axes.edgecolor)
    'lines.color' : 'C0', #has no affect on plot(); see axes.prop_cycle
    'mathtext.default' : 'regular', # The default font to use for math.
    'patch.facecolor' : 'C0',
    'patch.edgecolor' : 'C7',
    'pdf.fonttype' : 42, #Output Type 3 (Type3) or Type 42 (TrueType)
    'ps.fonttype' : 42, #Output Type 3 (Type3) or Type 42 (TrueType
    'savefig.dpi' : 300, #figure dots per inch
    'savefig.transparent' : False, #setting that controls whether figures are saved with a transparent background by default
    'scatter.marker': '+', #The default marker type for scatter plots.
    'text.color' : 'C7',
    'xtick.color' : 'C7', #color of the tick labels
    'xtick.minor.visible' : True,
    'ytick.color' : 'C7', #color of the tick labels
    'ytick.minor.visible' : True,

    }