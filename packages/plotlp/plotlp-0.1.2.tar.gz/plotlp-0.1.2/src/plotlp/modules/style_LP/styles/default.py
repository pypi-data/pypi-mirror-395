from cycler import cycler

base = None
style = {

    #Lines
    'lines.linewidth' : 1.5, #line width in points
    'lines.linestyle' : '-', #solid line
    'lines.color' : 'C0', #has no affect on plot(); see axes.prop_cycle
    'lines.marker' : 'None', #the default marker
    'lines.markerfacecolor' : 'auto', #the default markerfacecolor
    'lines.markeredgecolor' : 'auto', #the default markeredgecolor
    'lines.markeredgewidth' : 1.0, #the line width around the marker symbol
    'lines.markersize' : 6, #markersize, in points
    'lines.dash_joinstyle' : 'round', #miter|round|bevel
    'lines.dash_capstyle' : 'butt', #butt|round|projecting
    'lines.solid_joinstyle' : 'round', #miter|round|bevel
    'lines.solid_capstyle' : 'projecting', #butt|round|projecting
    'lines.antialiased' : True, #render lines in antialiased (no jaggies)
    'lines.dashed_pattern' : [3.7, 1.6],
    'lines.dashdot_pattern' : [6.4,1.6,1,1.6],
    'lines.dotted_pattern' : [1, 1.65],
    'lines.scale_dashes': True,

    #Markers
    'markers.fillstyle' : 'full', #'full', 'left', 'right', 'bottom', 'top', 'none'

    #pcolor
    'pcolor.shading' : 'auto',
    'pcolormesh.snap' : True, #whether to snap the mesh to pixel boundaries. This is provided solely to allow old test images to remain unchanged. Set to False to obtain the previous behavior.

    #Patches
    'patch.linewidth' : 1.0, #edge width in points
    'patch.facecolor' : 'C0',
    'patch.edgecolor' : 'black',
    'patch.force_edgecolor' : False,
    'patch.antialiased' : True, #render patches in antialiased (no jaggies)

    #Hatch
    'hatch.color' : 'black',
    'hatch.linewidth' : 1.0,

    #Boxplot
    'boxplot.notch' : False,
    'boxplot.vertical' : True,
    'boxplot.whiskers' : 1.5,
    'boxplot.bootstrap' : None,
    'boxplot.patchartist' : False,
    'boxplot.showmeans' : False,
    'boxplot.showcaps' : True,
    'boxplot.showbox' : True,
    'boxplot.showfliers' : True,
    'boxplot.meanline' : False,
    'boxplot.flierprops.color' : 'black',
    'boxplot.flierprops.marker' : 'o',
    'boxplot.flierprops.markerfacecolor' : 'none',
    'boxplot.flierprops.markeredgecolor' : 'black',
    'boxplot.flierprops.markeredgewidth' : 1.0,
    'boxplot.flierprops.markersize' : 6.0,
    'boxplot.flierprops.linestyle' : 'none',
    'boxplot.flierprops.linewidth' : 1.0,
    'boxplot.boxprops.color' : 'black',
    'boxplot.boxprops.linewidth' : 1.0,
    'boxplot.boxprops.linestyle' : '-',
    'boxplot.whiskerprops.color' : 'black',
    'boxplot.whiskerprops.linewidth' : 1.0,
    'boxplot.whiskerprops.linestyle' : '-',
    'boxplot.capprops.color' : 'black',
    'boxplot.capprops.linewidth' : 1.0,
    'boxplot.capprops.linestyle' : '-',
    'boxplot.medianprops.color' : 'C1',
    'boxplot.medianprops.linewidth' : 1.0,
    'boxplot.medianprops.linestyle' : '-',
    'boxplot.meanprops.color' : 'C2',
    'boxplot.meanprops.marker' : '^',
    'boxplot.meanprops.markerfacecolor' : 'C2',
    'boxplot.meanprops.markeredgecolor' : 'C2',
    'boxplot.meanprops.markersize' : 6.0,
    'boxplot.meanprops.linestyle' : '--',
    'boxplot.meanprops.linewidth' : 1.0,

    #Font
    'font.family' : ['sans-serif'], #'serif' (e.g., Times), 'sans-serif' (e.g., Helvetica), 'cursive' (e.g., Zapf-Chancery), 'fantasy' (e.g., Western), and 'monospace' (e.g., Courier)
    'font.style' : 'normal', #'normal' (or roman), 'italic' or 'oblique'
    'font.variant' : 'normal', #'normal' or 'small-caps'
    'font.weight' : 'normal', #'normal', 'bold', 'bolder', 'lighter', 100, 200, 300, ..., 900.  Normal is the same as 400, and bold is 700. bolder and lighter are relative values with respect to the current weight
    'font.stretch' : 'normal', #ultra-condensed, extra-condensed, condensed, semi-condensed, normal, semi-expanded, expanded, extra-expanded, ultra-expanded, wider, and narrower
    'font.size' : 10.0,
    'font.serif' : ['DejaVu Serif', 'Bitstream Vera Serif', 'Computer Modern Roman', 'New Century Schoolbook', 'Century Schoolbook L', 'Utopia', 'ITC Bookman', 'Bookman', 'Nimbus Roman No9 L', 'Times New Roman', 'Times', 'Palatino', 'Charter', 'serif'],
    'font.sans-serif' : ['DejaVu Sans', 'Bitstream Vera Sans', 'Computer Modern Sans Serif', 'Lucida Grande', 'Verdana', 'Geneva', 'Lucid', 'Arial', 'Helvetica', 'Avant Garde', 'sans-serif'],
    'font.cursive' : ['Apple Chancery', 'Textile', 'Zapf Chancery', 'Sand', 'Script MT', 'Felipa', 'Comic Neue', 'Comic Sans MS', 'cursive'],
    'font.fantasy' : ['Chicago', 'Charcoal', 'Impact', 'Western', 'Humor Sans', 'xkcd', 'fantasy'],
    'font.monospace' : ['DejaVu Sans Mono', 'Bitstream Vera Sans Mono', 'Computer Modern Typewriter', 'Andale Mono', 'Nimbus Mono L', 'Courier New', 'Courier', 'Fixed', 'Terminal', 'monospace'],

    #Text
    'text.color' : 'black',
    'text.hinting' : 'force_autohint', #'none' (False), 'auto' (True), 'native', 'either'
    'text.hinting_factor' : 8, #Specifies the amount of softness for hinting in the horizontal direction
    'text.kerning_factor' : 0, #Specifies the scaling factor for kerning values.
    'text.antialiased' : True,
    'text.parse_math' : True, #Use mathtext if there is an even number of unescaped dollar signs.

    #Latex
    'text.usetex' : False, #use latex for all text handling.
    'text.latex.preamble' : '', #single line of LaTeX code that will be passed on to the LaTeX system.

    #Mathtext
    'mathtext.fontset' : 'dejavusans', #Should be 'dejavusans' (default), 'dejavuserif', 'cm' (Computer Modern), 'stix', 'stixsans' or 'custom'
    'mathtext.bf'  : 'sans:bold',
    'mathtext.cal' : 'cursive',
    'mathtext.it'  : 'sans:italic',
    'mathtext.rm'  : 'sans',
    'mathtext.sf'  : 'sans',
    'mathtext.tt'  : 'monospace',
    'mathtext.fallback': 'cm', #'cm' (Computer Modern), 'stix', 'stixsans'
    'mathtext.default' : 'it', # The default font to use for math.

    #Axes
    'axes.axisbelow' : 'line', #whether axis gridlines and ticks are below the axes elements (lines, text, etc)
    'axes.facecolor' : 'white', #axes background color
    'axes.edgecolor' : 'black', #axes edge color
    'axes.linewidth' : 0.8, #edge linewidth
    'axes.grid' : False, #display grid or not
    'axes.grid.axis' : 'both',
    'axes.grid.which' : 'major',
    'axes.titlelocation' : 'center', #alignment of the title: {left, right, center}
    'axes.titlesize' : 'large', #fontsize of the axes title
    'axes.titleweight' : 'normal',#font weight for axes title
    'axes.titlecolor' : 'auto',#color of the axes title, auto falls back to text.color as default value
    'axes.titley' : None, #position title (axes relative units).  None implies auto
    'axes.titlepad' : 6.0, #pad between axes and title in points
    'axes.labelsize' : 'medium', #fontsize of the x any y labels
    'axes.labelpad' : 4.0, #space between label and axis
    'axes.labelweight' : 'normal', #weight of the x and y labels
    'axes.labelcolor' : 'black',
    'axes.formatter.limits' : [-5, 6], #use scientific notation if log10 of the axis range is smaller than the first or larger than the second
    'axes.formatter.use_locale' : False, #When True, format tick labels according to the user's locale. For example, use ',' as a decimal separator in the fr_FR locale.
    'axes.formatter.use_mathtext' : False, #When True, use mathtext for scientific notation.
    'axes.formatter.min_exponent' : 0, #minimum exponent to format in scientific notation
    'axes.formatter.useoffset' : True, #If True, the tick label formatter will default to labeling ticks relative to an offset when the data range is very small compared to the minimum absolute value of the data.
    'axes.formatter.offset_threshold' : 4, #When useoffset is True, the offset will be used when it can remove at least this number of significant digits from tick labels.
    'axes.spines.bottom' : True, #display axis spines
    'axes.spines.left' : True, #display axis spines
    'axes.spines.right' : True, #display axis spines
    'axes.spines.top' : True, #display axis spines
    'axes.unicode_minus' : True, #use Unicode for the minus symbol rather than hyphen
    'axes.prop_cycle' : cycler(color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']), #color cycle for plot lines as list of string colorspecs: single letter, long name, or web-style hex
    'axes.xmargin' : 0.05, #x margin
    'axes.ymargin' : 0.05, #y margin
    'axes.zmargin' : 0.05, #z margin
    'axes.autolimit_mode' : 'data', #If "data", use axes.xmargin and axes.ymargin as is. If "round_numbers", after application of margins, axis limits are further expanded to the nearest "round" number.

    #Polaraxe
    'polaraxes.grid' : True, #display grid on polar axes

    #Axes3d
    'axes3d.grid' : True, #display grid on 3d axes
    'axes3d.xaxis.panecolor' : (0.95, 0.95, 0.95, 0.5), #background pane on 3D axes
    'axes3d.yaxis.panecolor' : (0.90, 0.90, 0.90, 0.5), #background pane on 3D axes
    'axes3d.zaxis.panecolor': (0.925, 0.925, 0.925, 0.5), #background pane on 3D axes

    #Axis
    'xaxis.labellocation' : 'center', #alignment of the xaxis label: {left, right, center}
    'yaxis.labellocation' : 'center', #alignment of the yaxis label: {bottom, top, center}

    #Date
    'date.autoformatter.year' : '%Y',
    'date.autoformatter.month' : '%Y-%m',
    'date.autoformatter.day' : '%Y-%m-%d',
    'date.autoformatter.hour' : '%m-%d %H',
    'date.autoformatter.minute' : '%d %H:%M',
    'date.autoformatter.second' : '%H:%M:%S',
    'date.autoformatter.microsecond' : '%M:%S.%f',
    'date.converter' : 'auto', #'auto', 'concise'
    'date.interval_multiples' : True,

    #Xticks
    'xtick.top' : False, #draw ticks on the top side
    'xtick.bottom' : True, #draw ticks on the bottom side
    'xtick.labeltop' : False, #draw label on the top
    'xtick.labelbottom' : True, #draw label on the bottom
    'xtick.major.size' : 3.5, #major tick size in points
    'xtick.minor.size' : 2, #minor tick size in points
    'xtick.major.width' : 0.8, #major tick width in points
    'xtick.minor.width' : 0.6, #minor tick width in points
    'xtick.major.pad' : 3.5, #distance to major tick label in points
    'xtick.minor.pad' : 3.4, #distance to the minor tick label in points
    'xtick.color' : 'black', #color of the tick labels
    'xtick.labelcolor' : 'inherit', #color of the tick labels or inherit from xtick.color
    'xtick.labelsize' : 'medium', #fontsize of the tick labels
    'xtick.direction' : 'out', #direction: in, out, or inout
    'xtick.minor.visible' : False,
    'xtick.major.top' : True, #draw x axis top major ticks
    'xtick.major.bottom' : True, #draw x axis bottom major ticks
    'xtick.minor.top' : True, #draw x axis top minor ticks
    'xtick.minor.bottom' : True, #draw x axis bottom minor ticks
    'xtick.alignment' : 'center',

    #Yticks
    'ytick.left' : True, #draw ticks on the left side
    'ytick.right' : False, #draw ticks on the right side
    'ytick.labelleft' : True, #draw label on the left
    'ytick.labelright' : False, #draw label on the right
    'ytick.major.size' : 3.5, #major tick size in points
    'ytick.minor.size' : 2, #minor tick size in points
    'ytick.major.width' : 0.8, #major tick width in points
    'ytick.minor.width' : 0.6, #minor tick width in points
    'ytick.major.pad' : 3.5, #distance to major tick label in points
    'ytick.minor.pad' : 3.4, #distance to the minor tick label in points
    'ytick.color' : 'black', #color of the tick labels
    'ytick.labelcolor' : 'inherit', #color of the tick labels or inherit from ytick.color
    'ytick.labelsize' : 'medium', #fontsize of the tick labels
    'ytick.direction' : 'out', #direction: in, out, or inout
    'ytick.minor.visible' : False,
    'ytick.major.left' : True, #draw y axis left major ticks
    'ytick.major.right' : True, #draw y axis right major ticks
    'ytick.minor.left' : True, #draw y axis left minor ticks
    'ytick.minor.right' : True, #draw y axis right minor ticks
    'ytick.alignment' : 'center_baseline',

    #Grids
    'grid.color' : '#b0b0b0', #grid color
    'grid.linestyle' : '-', #solid
    'grid.linewidth' : 0.8, #in points
    'grid.alpha' : 1.0, #transparency, between 0.0 and 1.0

    #Legend
    'legend.loc' : 'best',
    'legend.frameon' : True, #whether or not to draw a frame around legend
    'legend.framealpha' : 0.8, #transparency of legend frame
    'legend.facecolor' : 'inherit', #legend background color (when 'inherit' uses axes.facecolor)
    'legend.edgecolor' : '0.8', #legend edge color (when 'inherit' uses axes.edgecolor)
    'legend.fancybox' : True, #if True, use a rounded box for the legend, else a rectangle
    'legend.shadow' : False,
    'legend.numpoints' : 1, #the number of points in the legend line
    'legend.scatterpoints' : 1, #number of scatter points
    'legend.markerscale' : 1.0, #the relative size of legend markers vs. original the following dimensions are in axes coords
    'legend.fontsize' : 'medium',
    'legend.labelcolor' : 'None',
    'legend.title_fontsize' : None, #None sets to the same as the default axes.
    'legend.borderpad' : 0.4, #border whitespace in fontsize units
    'legend.labelspacing' : 0.5, #the vertical space between the legend entries in fraction of fontsize
    'legend.handlelength' : 2., #the length of the legend lines in fraction of fontsize
    'legend.handleheight' : 0.7, #the height of the legend handle in fraction of fontsize
    'legend.handletextpad' : 0.8, #the space between the legend line and legend text in fraction of fontsize
    'legend.borderaxespad' : 0.5, #the border between the axes and legend edge in fraction of fontsize
    'legend.columnspacing' : 2., #the border between the axes and legend edge in fraction of fontsize

    #Figure
    'figure.titlesize' : 'large',#size of the figure title
    'figure.titleweight' : 'normal', #weight of the figure title
    'figure.labelsize' :   'large', #size of the figure label
    'figure.labelweight' : 'normal', #weight of the figure label
    'figure.figsize' : [6.4, 4.8], #figure size in inches
    'figure.dpi' : 100, #figure dots per inch
    'figure.facecolor' : 'white', #figure facecolor
    'figure.edgecolor' : 'white', #figure edgecolor
    'figure.frameon' : True,
    'figure.subplot.left' : 0.125, #the left side of the subplots of the figure
    'figure.subplot.right' : 0.9, #the right side of the subplots of the figure
    'figure.subplot.bottom' : 0.11, #the bottom of the subplots of the figure
    'figure.subplot.top' : 0.88, #the top of the subplots of the figure
    'figure.subplot.wspace' : 0.2, #the amount of width reserved for space between subplots, expressed as a fraction of the average axis width
    'figure.subplot.hspace'  : 0.2, #the amount of height reserved for space between subplots, expressed as a fraction of the average axis height
    'figure.autolayout' : False, #When True, automatically adjust subplot parameters to make the plot fit the figure
    'figure.constrained_layout.use' : False, #When True, automatically make plot elements fit on the figure. (Not compatible with `autolayout`, above).
    'figure.constrained_layout.h_pad' : 0.04167, #Padding around axes objects. Float representing inches. Default is 3/72 inches (3 points)
    'figure.constrained_layout.w_pad' : 0.04167, #Padding around axes objects. Float representing inches. Default is 3/72 inches (3 points)
    'figure.constrained_layout.hspace' : 0.02, #Space between subplot groups. Float representing a fraction of the subplot widths being separated
    'figure.constrained_layout.wspace' : 0.02, #Space between subplot groups. Float representing a fraction of the subplot widths being separated
    'figure.hooks' : [],

    #Image
    'image.aspect' : 'equal', #equal | auto | a number
    'image.interpolation' : 'antialiased', #see help(imshow) for options
    'image.cmap' : 'viridis',  #gray | jet | ...
    'image.lut' : 256, #the size of the colormap lookup table
    'image.origin' : 'upper', #lower | upper
    'image.resample' : True,
    'image.composite_image' : True, #When True, all the images on a set of axes are combined into a single composite image before saving a figure as a vector graphics file, such as a PDF.

    #Contour
    'contour.negative_linestyle' : 'dashed', # dashed | solid
    'contour.corner_mask' : True,
    'contour.linewidth' : None, #{float, None} Size of the contour line widths. If set to None, it falls back to `line.linewidth`.
    'contour.algorithm' : 'mpl2014', #{mpl2005, mpl2014, serial, threaded}

    #Errorbar
    'errorbar.capsize' : 0, #length of end cap on error bars in pixels

    #Hist
    'hist.bins' : 10, #The default number of histogram bins or 'auto'.

    #Scatter
    'scatter.marker': 'o', #The default marker type for scatter plots.
    'scatter.edgecolors': 'face', #The default edge colors for scatter plots.

    #Agg
    'agg.path.chunksize': 0, #0 to disable; values in the range 10000 to 100000 can improve speed slightly and prevent an Agg rendering failure when plotting very large data sets, especially if they are very gappy. It may cause minor artifacts, though. A value of 20000 is probably a good starting point.

    #Path
    'path.simplify' : True, #When True, simplify paths by removing "invisible" points to reduce file size and increase rendering speed
    'path.simplify_threshold' : 0.111111111111, #The threshold of similarity below which vertices will be removed in the simplification process
    'path.snap' : True, # When True, rectilinear axis-aligned paths will be snapped to the nearest pixel when certain criteria are met. When False, paths will never be snapped.
    'path.sketch' : None, # May be none, or a 3-tuple of the form (scale, length, randomness). *scale* is the amplitude of the wiggle perpendicular to the line (in pixels). *length* is the length of the wiggle along the line (in pixels). *randomness* is the factor by which the length is randomly scaled.
    'path.effects' : [],

    #Savefig
    'savefig.dpi' : 'figure', #figure dots per inch
    'savefig.facecolor' : 'auto', #figure facecolor when saving
    'savefig.edgecolor' : 'auto', #figure edgecolor when saving
    'savefig.format' : 'png', #png, ps, pdf, svg
    'savefig.bbox' : None, #'tight' or 'standard'
    'savefig.pad_inches'  : 0.1, #Padding to be used when bbox is set to 'tight'
    'savefig.transparent' : False, #setting that controls whether figures are saved with a transparent background by default
    'savefig.orientation' : 'portrait',

    #Ps
    'ps.papersize' : 'letter', #auto, letter, legal, ledger, A0-A10, B0-B10
    'ps.useafm' : False, #use of afm fonts, results in small files
    'ps.usedistiller' : None, #can be: None, ghostscript or xpdf
    'ps.distiller.res' : 6000, #dpi
    'ps.fonttype' : 3, #Output Type 3 (Type3) or Type 42 (TrueType)

    #Pdf
    'pdf.compression' : 6, #integer from 0 to 9, 0 disables compression (good for debugging)
    'pdf.fonttype' : 3, #Output Type 3 (Type3) or Type 42 (TrueType)
    'pdf.inheritcolor' : False,
    'pdf.use14corefonts' : False,

    #Svg
    'svg.image_inline' : True, #write raster image data directly into the svg file
    'svg.fonttype' : 'path', #How to handle SVG fonts, 'none': Assume fonts are installed on the machine where the SVG will be viewed, 'path': Embed characters as paths -- supported by most SVG renderers
    'svg.hashsalt' : None, #If not None, use this string as hash salt instead of uuid4

    #Pgf
    'pgf.rcfonts' : True,
    'pgf.preamble' : '',
    'pgf.texsystem' : 'xelatex',

    #Keymap
    'keymap.fullscreen' : ['f', 'ctrl+f'], #toggling
    'keymap.home' : ['h', 'r', 'home'], #home or reset mnemonic
    'keymap.back' : ['left', 'c', 'backspace', 'MouseButton.BACK'], #forward / backward keys to enable
    'keymap.forward' : ['right', 'v', 'MouseButton.FORWARD'], #left handed quick navigation
    'keymap.pan' : ['p'], #pan mnemonic
    'keymap.zoom' : ['o'], #zoom mnemonic
    'keymap.save' : ['s', 'ctrl+s'], #saving current figure
    'keymap.quit' : ['ctrl+w', 'cmd+w', 'q'], #close the current figure
    'keymap.quit_all' : [], #close the all figures
    'keymap.grid' : ['g'], #switching on/off a grid in current axes
    'keymap.grid_minor' : ['G'], #switching on/off minor grids in current axes
    'keymap.yscale' : ['l'], #toggle scaling of y-axes ('log'/'linear')
    'keymap.xscale' : ['k', 'L'], #toggle scaling of x-axes ('log'/'linear')
    'keymap.copy' : ['ctrl+c', 'cmd+c'], #copy figure to clipboard
    'keymap.help' : ['f1'], #help

    #Animation
    'animation.html' : 'none',
    'animation.writer' : 'ffmpeg', #MovieWriter 'backend' to use
    'animation.codec' : 'h264', #Codec to use for writing movie
    'animation.bitrate' : -1, #Controls size/quality tradeoff for movie. -1 implies let utility auto-determine
    'animation.frame_format' : 'png', # Controls frame format used by temp files
    'animation.ffmpeg_path' : 'ffmpeg', #Path to ffmpeg binary. Without full path, $PATH is searched
    'animation.ffmpeg_args' : [], #Additional arguments to pass to ffmpeg
    'animation.convert_path' : 'convert', #Path to ImageMagick's convert binary. On Windows use the full path since convert is also the name of a system tool.
    'animation.convert_args' : ['-layers', 'OptimizePlus'],
    'animation.embed_limit' : 20.0, #Limit, in MB, of size of base64 encoded animation in HTML (i.e. IPython notebook)

    #Internal
    '_internal.classic_mode' : False,

}