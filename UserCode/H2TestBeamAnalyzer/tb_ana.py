#!/usr/bin/env python

print "Importing modules"
import sys
import optparse
import os
import ROOT
import array
import time
import numpy

from math import exp, sqrt
from runlists import getBeamEtaFromRun
from runlists import getBeamPhiFromRun

HCAL_DET_ngHB = 21
HCAL_DET_ngHE = 22
HCAL_DET_HBHE = 26
HCAL_DET_HF   = 27

edges10_list = [
  1.58,   4.73,   7.88,   11.0,   14.2,   17.3,   20.5,   23.6,
  26.8,   29.9,   33.1,   36.2,   39.4,   42.5,   45.7,   48.8,
  53.6,   60.1,   66.6,   73.0,   79.5,   86.0,   92.5,   98.9,
  105,    112,    118,    125,    131,    138,    144,    151,
  157,    164,    170,    177,    186,    199,    212,    225,
  238,    251,    264,    277,    289,    302,    315,    328,
  341,    354,    367,    380,    393,    406,    418,    431,
  444,    464,    490,    516,    542,    568,    594,    620,
  645,    670,    695,    720,    745,
  771,    796,    821,    846,    871,    897,    922,    947,
  960,    1010,   1060,   1120,   1170,   1220,   1270,   1320,
  1370,   1430,   1480,   1530,   1580,   1630,   1690,   1740,
  1790,   1840,   1890,   1940,   2020,   2120,   2230,   2330,
  2430,   2540,   2640,   2740,   2850,   2950,   3050,   3150,
  3260,   3360,   3460,   3570,   3670,   3770,   3880,   3980,
  4080,   4240,   4450,   4650,   4860,   5070,   5280,   5490,
  5680,   5880,   6080,   6280,   6480,
  6680,   6890,   7090,   7290,   7490,   7690,   7890,   8090,
  8400,   8810,   9220,   9630,   10000,  10400,  10900,  11300,
  11700,  12100,  12500,  12900,  13300,  13700,  14100,  14500,
  15000,  15400,  15800,  16200,  16800,  17600,  18400,  19300,
  20100,  20900,  21700,  22500,  23400,  24200,  25000,  25800,
  26600,  27500,  28300,  29100,  29900,  30700,  31600,  32400,
  33200,  34400,  36100,  37700,  39400,  41000,  42700,  44300,
  45900,  47600,  49200,  50800,  52500,
  54100,  55700,  57400,  59000,  60600,  62200,  63900,  65500,
  68000,  71300,  74700,  78000,  81400,  84700,  88000,  91400,
  94700,  98100,  101000, 105000, 108000, 111000, 115000, 118000,
  121000, 125000, 128000, 131000, 137000, 145000, 152000, 160000,
  168000, 176000, 183000, 191000, 199000, 206000, 214000, 222000,
  230000, 237000, 245000, 253000, 261000, 268000, 276000, 284000,
  291000, 302000, 316000, 329000, 343000, 356000, 370000, 384000, 398000,
  410000, 430000, 450000, 470000, 520000, 550000, 580000, 640000, 680000
]
edgesChris_list = [
    -16.000000,    -12.875000,    -9.750000,     -6.625000,     -3.500000,     -0.375000,     2.750000,      5.875000,
    9.000000,      12.125000,     15.250000,     18.375000,     21.500000,     24.625000,     27.750000,     30.875000,
    34.000000,     40.200000,     46.400000,     52.600000,     58.800000,     65.000000,     71.200000,     77.400000,
    83.600000,     89.800000,     96.000000,     102.200000,    108.400000,    114.600000,    120.800000,    127.000000,
    133.200000,    139.400000,    145.600000,    151.800000,    158.000000,    170.428571,    182.857143,    195.285714,
    207.714286,    220.142857,    232.571429,    245.000000,    257.428571,    269.857143,    282.285714,    294.714286,
    307.142857,    319.571429,    332.000000,    344.428571,    356.857143,    369.285714,    381.714286,    394.142857,
    406.571429,    419.000000,    443.800000,    468.600000,    493.400000,    518.200000,    543.000000,    567.800000,
    592.600000,    617.400000,    642.200000,    667.000000,    691.800000,    716.600000,    741.400000,    766.200000,
    791.000000,    815.800000,    840.600000,    865.400000,    890.200000,    915.000000,    964.750000,    1014.500000,
    1064.250000,   1114.000000,   1163.750000,   1213.500000,   1263.250000,   1313.000000,   1362.750000,   1412.500000,
    1462.250000,   1512.000000,   1561.750000,   1611.500000,   1661.250000,   1711.000000,   1760.750000,   1810.500000,
    1860.250000,   1910.000000,   2009.047619,   2108.095238,   2207.142857,   2306.190476,   2405.238095,   2504.285714,
    2603.333333,   2702.380952,   2801.428571,   2900.476190,   2999.523810,   3098.571429,   3197.619048,   3296.666667,
    3395.714286,   3494.761905,   3593.809524,   3692.857143,   3791.904762,   3890.952381,   3990.000000,   4188.500000,
    4387.000000,   4585.500000,   4784.000000,   4982.500000,   5181.000000,   5379.500000,   5578.000000,   5776.500000,
    5975.000000,   6173.500000,   6372.000000,   6570.500000,   6769.000000,   6967.500000,   7166.000000,   7364.500000,
    7563.000000,   7761.500000,   7960.000000,   8357.000000,   8754.000000,   9151.000000,   9548.000000,   9945.000000,
    10342.000000,  10739.000000,  11136.000000,  11533.000000,  11930.000000,  12327.000000,  12724.000000,  13121.000000,
    13518.000000,  13915.000000,  14312.000000,  14709.000000,  15106.000000,  15503.000000,  15900.000000,  16695.238095,
    17490.476190,  18285.714286,  19080.952381,  19876.190476,  20671.428571,  21466.666667,  22261.904762,  23057.142857,
    23852.380952,  24647.619048,  25442.857143,  26238.095238,  27033.333333,  27828.571429,  28623.809524,  29419.047619,
    30214.285714,  31009.523810,  31804.761905,  32600.000000,  34185.000000,  35770.000000,  37355.000000,  38940.000000,
    40525.000000,  42110.000000,  43695.000000,  45280.000000,  46865.000000,  48450.000000,  50035.000000,  51620.000000,
    53205.000000,  54790.000000,  56375.000000,  57960.000000,  59545.000000,  61130.000000,  62715.000000,  64300.000000,
    67485.000000,  70670.000000,  73855.000000,  77040.000000,  80225.000000,  83410.000000,  86595.000000,  89780.000000,
    92965.000000,  96150.000000,  99335.000000,  102520.000000, 105705.000000, 108890.000000, 112075.000000, 115260.000000,
    118445.000000, 121630.000000, 124815.000000, 128000.000000, 134333.333333, 140666.666667, 147000.000000, 153333.333333,
    159666.666667, 166000.000000, 172333.333333, 178666.666667, 185000.000000, 191333.333333, 197666.666667, 204000.000000,
    210333.333333, 216666.666667, 223000.000000, 229333.333333, 235666.666667, 242000.000000, 248333.333333, 254666.666667,
    261000.000000, 273696.969697, 286393.939394, 299090.909091, 311787.878788, 324484.848485, 337181.818182, 349878.787879,
    362575.757576, 375272.727273, 387969.696970, 400666.666667, 413363.636364, 426060.606061, 438757.575758, 451454.545455,
    464151.515152, 476848.484848, 489545.454545, 502242.424242, 514939.393939, 527636.363636, 540333.333333, 553030.303030,
    565727.272727, 578424.242424, 591121.212121, 603818.181818, 616515.151515, 629212.121212, 641909.090909, 654606.060606,
    667303.030303, 680000.000000
]
#edgesChris_list = [0,
#  3.1,    6.2,    9.3,    12.4,   15.5,   18.6,   21.7,   24.8,
#  27.9,   31,     34.1,   37.2,   40.3,   43.4,   46.5,   49.6,
#  52.7,   55.8,   58.9,   62,     65.1,   68.2,   71.3,   74.4,   
#  77.5,   80.6,   83.7,   86.8,   89.9,   93,     96.1,   99.2,   
#  102.3,  105.4,  108.5,  111.6,  114.7,  117.8,  120.9,  124,    
#  127.1,  130.2,  133.3,  136.4,  139.5,  142.6,  145.7,  148.8,  
#  151.9,  155,    158.1,  161.2,  164.3,  167.4,  170.5,  173.6,  
#  176.7,  179.8,  182.9,  186,    189.1,  192.2,  195.3,  198.4,  
#  201.5,  204.6,  207.7,  210.8,  213.9,  217,    220.1,  223.2,  
#  226.3,  229.4,  232.5,  235.6,  238.7,  241.8,  244.9,  248,
#  251.1,  254.2,  257.3,  260.4,  263.5,  266.6,  269.7,  272.8,  
#  275.9,  279,    282.1,  285.2,  288.3,  291.4,  294.5,  297.6,
#  300.7,  303.8,  306.9,  310,    313.1,  316.2,  319.3,  322.4,
#  325.5,  328.6,  331.7,  334.8,  337.9,  341,    344.1,  347.2,
#  350.3,  353.4,  356.5,  359.6,  362.7,  365.8,  368.9,  372,
#  375.1,  378.2,  381.3,  384.4,  387.5,  390.6,  393.7,  396.8,
#  399.9,  403,    406.1,  418,    431,    444,    464,    
#  490,    516,    542,    568,    594,    620,    645,    670,
#  695,    720,    745,
#  771,    796,    821,    846,    871,    897,    922,    947,
#  960,    1010,   1060,   1120,   1170,   1220,   1270,   1320,
#  1370,   1430,   1480,   1530,   1580,   1630,   1690,   1740,
#  1790,   1840,   1890,   1940,   2020,   2120,   2230,   2330,
#  2430,   2540,   2640,   2740,   2850,   2950,   3050,   3150,
#  3260,   3360,   3460,   3570,   3670,   3770,   3880,   3980,
#  4080,   4240,   4450,   4650,   4860,   5070,   5280,   5490,
#  5680,   5880,   6080,   6280,   6480,
#  6680,   6890,   7090,   7290,   7490,   7690,   7890,   8090,
#  8400,   8810,   9220,   9630,   10000,  10400,  10900,  11300,
#  11700,  12100,  12500,  12900,  13300,  13700,  14100,  14500,
#  15000,  15400,  15800,  16200,  16800,  17600,  18400,  19300,
#  20100,  20900,  21700,  22500,  23400,  24200,  25000,  25800,
#  26600,  27500,  28300,  29100,  29900,  30700,  31600,  32400,
#  33200,  34400,  36100,  37700,  39400,  41000,  42700,  44300,
#  45900,  47600,  49200,  50800,  52500,
#  54100,  55700,  57400,  59000,  60600,  62200,  63900,  65500,
#  68000,  71300,  74700,  78000,  81400,  84700,  88000,  91400,
#  94700,  98100,  101000, 105000, 108000, 111000, 115000, 118000,
#  121000, 125000, 128000, 131000, 137000, 145000, 152000, 160000,
#  168000, 176000, 183000, 191000, 199000, 206000, 214000, 222000,
#  230000, 237000, 245000, 253000, 261000, 268000, 276000, 284000,
#  291000, 302000, 316000, 329000, 343000, 356000, 370000, 384000, 398000,
#  410000, 430000, 450000, 470000, 520000, 550000, 580000, 640000, 680000
#]

#######################
# Get options
#######################

print "Getting options"

parser = optparse.OptionParser("usage: %prog [options] \n")

parser.add_option ('-o', '--o', dest='outfile', type='string',
                   default = None,
                   help="output file")
parser.add_option ('-i', '--i', dest='infile', type='string',
                   default = None,
                   help="input file")
parser.add_option ('-r', '--r', dest='runnum', type='int',
                   default = -1,
                   help="Run number")

parser.add_option ('--doRefTile', action="store_true",
                   dest="doRefTile", default=False)

parser.add_option ('-n', '--nevents', dest='nevents', type='int',
                   default = -1,
                   help="Number of events to process (default: all)")
parser.add_option ('--start', dest='start', type='int',
                   default = 0,
                   help="Event number to start at (default: %default)")
parser.add_option ('--sigTS', dest='sigTS', type='int',
                   default = 7,
                   help="Number of time samples to use as signal (default: %default)")
parser.add_option ('--adc', dest='adc',
                   action='store_true', default = False,
                   #action='store_true', default = True,
                   help="Turn off lineariziation of ADC counts")
parser.add_option ('--verbose', dest='verbose', 
                   action='store_true', default=False,
                   help="Turn on verbose mode")
parser.add_option ('-e', dest='emap',
                   default=None,
                   help="EMAP filename in order to read specific tb_chanmap")
parser.add_option ('--shunt', dest='shunt', type='float',
                   default=1.,
                   help="QIE shunt setting (default: %default)")


options, args = parser.parse_args()

infile = options.infile
outfile = options.outfile
runnum = options.runnum
doRefTile = options.doRefTile
verbose = options.verbose
nevents = options.nevents
sigTS = options.sigTS
start = options.start
adc = options.adc
emapFile = options.emap
shunt = options.shunt

#Get the Eta and Phi that the Beam is pointed at
beamEta = int(getBeamEtaFromRun(int(runnum)))
beamPhi = int(getBeamPhiFromRun(int(runnum)))

print "Run:%i Beam Pointed at Eta:%i Phi:%i" % (runnum,beamEta,beamPhi)

# Do some sanity checks
if infile is None: 
    print "You did not provide an input file! Exiting."
    sys.exit()
if outfile is None:
    print "You did not provide an output file! Exiting."
    sys.exit()
if runnum is None:
    print "You did not provide a run number! Exiting."
    sys.exit()

# The following is needed to get the chanmap and associated
# variables from a tb_chanmap_* file, where the filename
# is known only at runtime.  This could be improved.

chanmapFile = "tb_chanmap"
if emapFile:
    emapFileShort = emapFile.rsplit('.',1)[0].rsplit('/')[-1]
    chanmapFile = "tb_chanmap_"+emapFileShort
chanmapModule = __import__(chanmapFile, globals(), locals(), [], -1)
chanmap = chanmapModule.chanmap
chanlist = chanmapModule.chanlist
from tb_utils import initialize_chanmap_vars
initialize_chanmap_vars(chanmap, chanlist)
from tb_utils import *

# Scale bin edges according to shunt value
edges10_np = numpy.array(edges10_list)
edges10_np = edges10_np/shunt
edgesChris_np = numpy.array(edgesChris_list)
edgesChris_np = edgesChris_np/shunt

edges10 = array.array('d', edges10_np)
edgesChris = array.array('d', edgesChris_np)

#######################
#  Set ROOT options  
#######################

print "Setting ROOT options"
ROOT.gROOT.SetBatch()
ROOT.gROOT.SetStyle("Plain")
#ROOT.gStyle.SetOptStat(111111111)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetNdivisions(405,"x");
#ROOT.gStyle.SetEndErrorSize(0.)
#ROOT.gStyle.SetErrorX(0.001)

NCont = 255
#stops = [ 0.00, 0.02, 0.34, 0.51, 0.64, 1.00 ]
#red   = [ 1.00, 0.00, 0.00, 0.87, 1.00, 0.51 ]
#green = [ 1.00, 0.00, 0.81, 1.00, 0.20, 0.00 ]
#blue  = [ 1.00, 0.51, 1.00, 0.12, 0.00, 0.00 ]

#stops = [ 0.00, 0.34, 0.61, 0.84, 0.92, 1.00]
#red   = [ 1.00, 0.00, 0.00, 0.87, 1.00, 0.51]
#green = [ 1.00, 0.00, 0.81, 1.00, 0.20, 0.00]
#blue  = [ 0.00, 0.51, 1.00, 0.12, 0.00, 0.00]

stops  = [ 0.00, 0.34, 0.61, 0.84, 1.00 ]
red    = [ 0.00, 0.00, 0.87, 1.00, 0.51 ]
green  = [ 0.00, 0.81, 1.00, 0.20, 0.00 ]
blue   = [ 0.51, 1.00, 0.12, 0.00, 0.00 ]

NRGBs = len(stops)

stopsArray = array.array('d', stops)
redArray   = array.array('d', red)
greenArray = array.array('d', green)
blueArray  = array.array('d', blue)
ROOT.TColor.CreateGradientColorTable(NRGBs, stopsArray, redArray, greenArray, blueArray, NCont)
ROOT.gStyle.SetNumberContours(NCont)

###############
# Choose
################
# Number of standard deviations for WC residuals cut
sigma_thold = 1.
# Channel to use as reference tile counter, currently 2x10 SCSN-81
refchan = 22  
#refchan = 23
# Energy to require to TS4 sum in reference tile counter (depends on channel):
refE = {}
refE[22] = 150.
refE[23] = 30.
# Chamber to use for location
#refchamb = "E"
refchamb = "C"

# Wire chamber means and standard deviations (xA-xC, xA-xC, yA-yC, etc.)
wc_res = {}
wc_res["x", "BC", "mean"] = -5.83e-01
wc_res["y", "BC", "mean"] = -1.75e+01
wc_res["x", "AC", "mean"] = -1.24e+00
wc_res["y", "AC", "mean"] = -8.78e+00
wc_res["x", "BC", "rms" ] =  3.96e+00
wc_res["y", "BC", "rms" ] =  3.88e+00
wc_res["x", "AC", "rms" ] =  4.30e+00
wc_res["y", "AC", "rms" ] =  5.08e+00

#wcList = ["A", "B", "C", "D", "E"]
wcList = ["A","B","C"]

adjust = {}
for iwc in wcList:
    for ixy in ["x", "y"]:
        for irun in runList:
            if ixy == "x" and iwc == "E":
                adjust[ixy, iwc, runnum] = -1.
            else:
                adjust[ixy, iwc, runnum] = 1.


#######################
# Read input data
#######################

file = ROOT.TFile(infile)
#ntp = file.Get("HFData/Events;3")
ntp = {}
ntp["hbhe"]  = file.Get("HBHEData/Events")
ntp["hf"]    = file.Get("HFData/Events")
ntp["qie11"] = file.Get("QIE11Data/Events")
ntp["hcal"]  = file.Get("HCALData/Events")
ntp["wc"]    = file.Get("WCData/Events")
ntp["time"]  = file.Get("Timing/Events")


############################
# Prepare for tree reading
############################           


# Each "vname" must contain the leaves that are used; order isn't important
vname = {}
vname["hbhe"] = ["numChs", "numTS", "iphi", "ieta", "depth", "pulse", "ped", "pulse_adc", "ped_adc"]
vname["hf"] = ["numChs", "numTS", "iphi", "ieta", "depth", "pulse", "pulse_adc", "ped", "ped_adc"]
vname["qie11"] = ["numChs", "numTS", "iphi", "ieta", "depth", "pulse", "ped", "pulse_adc", "ped_adc", "capid_error", "link_error", "soi", "TDC"]
vname["hcal"] = ["numChs", "detType", "numTS", "iphi", "ieta", "depth", "pulse", "ped", "adc", "tdc", "capid_error", "link_error", "soi"]
vname["wc"] = ["xA", "yA", "xB", "yB", "xC", "yC"]  #vname["wc"] = ["xA", "yA", "xB", "yB", "xC", "yC", "xD", "yD", "xE", "yE"]
vname["time"] = ["ttcL1Atime", "triggerTime"]

MAXDIGIS = 4000
MAXTS = 10
# Treat pulse and pulse_adc like 1D array of length MAXDIGIS*MAXTS

ROOT.gROOT.ProcessLine("struct hbhe_struct {Int_t numChs; Int_t numTS; Int_t iphi[%(dg)d]; Int_t ieta[%(dg)d]; Int_t depth[%(dg)d]; Float_t pulse[%(dg)d * %(ts)d]; Float_t ped[%(dg)d]; UChar_t pulse_adc[%(dg)d * %(ts)d]; Float_t ped_adc[%(dg)d];};" % {"dg": MAXDIGIS, "ts": MAXTS})
shbhe = ROOT.hbhe_struct()
for ivname in vname["hbhe"]:
    ntp["hbhe"].SetBranchAddress(ivname, ROOT.AddressOf(shbhe, ivname))

ROOT.gROOT.ProcessLine("struct hf_struct {Int_t numChs; Int_t numTS; Int_t iphi[%(dg)d]; Int_t ieta[%(dg)d]; Int_t depth[%(dg)d]; Float_t pulse[%(dg)d * %(ts)d];  UChar_t pulse_adc[%(dg)d * %(ts)d]; Float_t ped[%(dg)d]; Float_t ped_adc[%(dg)d];};" % {"dg": MAXDIGIS, "ts": MAXTS})
shf = ROOT.hf_struct()
for ivname in vname["hf"]:
    ntp["hf"].SetBranchAddress(ivname, ROOT.AddressOf(shf, ivname))

ROOT.gROOT.ProcessLine("struct qie11_struct {Int_t numChs; Int_t numTS; Int_t iphi[%(dg)d]; Int_t ieta[%(dg)d]; Int_t depth[%(dg)d]; Float_t pulse[%(dg)d * %(ts)d]; UChar_t pulse_adc[%(dg)d * %(ts)d]; Float_t ped[%(dg)d]; Float_t ped_adc[%(dg)d]; bool capid_error[%(dg)d]; bool link_error[%(dg)d]; bool soi[%(dg)d * %(ts)d]; Int_t TSn[%(dg)d * %(ts)d]; Int_t TDC[%(dg)d * %(ts)d];};" % {"dg": MAXDIGIS, "ts": MAXTS})
sqie11 = ROOT.qie11_struct()
for ivname in vname["qie11"]:
    ntp["qie11"].SetBranchAddress(ivname, ROOT.AddressOf(sqie11, ivname))

ROOT.gROOT.ProcessLine("struct hcal_struct {Int_t numChs; Int_t detType[%(dg)d]; Int_t numTS[%(dg)d]; Int_t iphi[%(dg)d]; Int_t ieta[%(dg)d]; Int_t depth[%(dg)d]; Float_t pulse[%(dg)d * %(ts)d]; Float_t ped[%(dg)d]; Int_t adc[%(dg)d * %(ts)d]; Int_t tdc[%(dg)d * %(ts)d]; bool capid_error[%(dg)d]; bool link_error[%(dg)d]; bool soi[%(dg)d * %(ts)d]; Int_t tsnum[%(dg)d * %(ts)d]; Int_t capid[%(dg)d * %(ts)d];};" % {"dg": MAXDIGIS, "ts": MAXTS})
shcal = ROOT.hcal_struct()
for ivname in vname["hcal"]:
    ntp["hcal"].SetBranchAddress(ivname, ROOT.AddressOf(shcal, ivname))


vec = {}
for ivname in vname["wc"]:
    vec[ivname] = ROOT.vector("double")()
    ntp["wc"].SetBranchStatus(ivname, 1)
    ntp["wc"].SetBranchAddress(ivname, vec[ivname])

tvar = {}
for ivname in vname["time"]:
    tvar[ivname] = array.array( 'd', [ 0 ] )
    ntp["time"].SetBranchStatus (ivname, 1)
    ntp["time"].SetBranchAddress(ivname, tvar[ivname])

nevts    = ntp["hcal"].GetEntries()
nevts_wc = ntp["wc"].GetEntries()
if nevts != nevts_wc:
    print "HBHE ntuple = ", nevts
    print "WC ntuple = ", nevts_wc
    print "Mismatch in event counts.  Exiting."
    #sys.exit()

wc_counts = {}
for ivname in vname["wc"]:
    for isize in range(100):
        wc_counts[ivname, isize] = 0.
for iwc in wcList:
    wc_counts[iwc] = 0.
wc_counts["AB"] = 0.
wc_counts["ABC"] = 0.
#wc_counts["ABCD"] = 0.
#wc_counts["ABCE"] = 0.
wc_counts["clean"] = 0.
wc_counts["passXBCp"] = 0.
wc_counts["passXBCm"] = 0.
wc_counts["passYBCp"] = 0.
wc_counts["passYBCm"] = 0.
wc_counts["passXACp"] = 0.
wc_counts["passXACm"] = 0.
wc_counts["passYACp"] = 0.
wc_counts["passYACm"] = 0.
wc_counts["badEnergy"] = 1.

    
for ichan in chanlist:
    wc_counts["nIn", ichan] = 0.

####################################################
# Define histograms
####################################################

outtfile = ROOT.TFile(outfile, "recreate")

hist = {}

# Define wire chamber histograms
for ip0 in wcList:
   # 2D histos for x vs y in each chamber
    hist["x"+ip0+"_v_y"+ip0]          = ROOT.TH2F("h_x"+ip0+"_v_y"+ip0, "h_x"+ip0+"_v_y"+ip0, 
                                                  400, -100., 100., 400, -100., 100.)
    hist["x"+ip0+"_v_y"+ip0, "clean"] = ROOT.TH2F("h_x"+ip0+"_v_y"+ip0+"_clean", "h_x"+ip0+"_v_y"+ip0+"_clean", 
                                                  400, -100., 100., 400, -100., 100.)

    for ixy in ["x", "y"]:
       # 1D histos for x and y in all 4 chambers
        hist[ixy+ip0] = ROOT.TH1F("h_"+ixy+"_"+ip0, "h_"+ixy+"_"+ip0, 400, -100., 100.)
        hist[ixy+ip0, "clean"] = ROOT.TH1F("h_"+ixy+"_"+ip0+"_clean", "h_"+ixy+"_"+ip0+"_clean", 400, -100., 100.)
        # 2D histos for x and y correlations for all histo combinations
        
    for ip1 in wcList:
        if ((ip0 == "A" and ip1 == "B") or (ip0 == "A" and ip1 == "C") or (ip0 == "A" and ip1 == "D") or (ip0 == "A" and ip1 == "E") or 
            (ip0 == "B" and ip1 == "C") or (ip0 == "B" and ip1 == "D") or (ip0 == "B" and ip1 == "E") or
            (ip0 == "C" and ip1 == "D") or (ip0 == "C" and ip1 == "E") or
            (ip0 == "D" and ip1 == "E")):
            for ixy in ["x", "y"]:
                hist[ixy+ip0+"_v_"+ixy+ip1]          = ROOT.TH2F("h_"+ixy+"_"+ip0+"v"+ip1,
                                                                 "h_"+ixy+"_"+ip0+"v"+ip1, 
                                                                 400, -100., 100., 400, -100., 100.)
                hist[ixy+ip0+"_v_"+ixy+ip1, "clean"] = ROOT.TH2F("h_"+ixy+"_"+ip0+"v"+ip1+"_clean",
                                                                 "h_"+ixy+"_"+ip0+"v"+ip1+"_clean", 
                                                                 400, -100., 100., 400, -100., 100.)

hist["dx_BC"] = ROOT.TH1F("h_dx_BC", "h_dx_BC", 400, -100., 100.)
hist["dy_BC"] = ROOT.TH1F("h_dy_BC", "h_dy_BC", 400, -100., 100.)
hist["dx_AC"] = ROOT.TH1F("h_dx_AC", "h_dx_AC", 400, -100., 100.)
hist["dy_AC"] = ROOT.TH1F("h_dy_AC", "h_dy_AC", 400, -100., 100.)
#hist["dx_AE"] = ROOT.TH1F("h_dx_AE", "h_dx_AE", 400, -100., 100.)
#hist["dy_AE"] = ROOT.TH1F("h_dy_AE", "h_dy_AE", 400, -100., 100.)

hist["dx_BC", "clean"] = ROOT.TH1F("h_dx_BC_clean", "h_dx_BC_clean", 400, -100., 100.)
hist["dy_BC", "clean"] = ROOT.TH1F("h_dy_BC_clean", "h_dy_BC_clean", 400, -100., 100.)
hist["dx_AC", "clean"] = ROOT.TH1F("h_dx_AC_clean", "h_dx_AC_clean", 400, -100., 100.)
hist["dy_AC", "clean"] = ROOT.TH1F("h_dy_AC_clean", "h_dy_AC_clean", 400, -100., 100.)
#hist["dx_AE", "clean"] = ROOT.TH1F("h_dx_AE_clean", "h_dx_AE_clean", 400, -100., 100.)
#hist["dy_AE", "clean"] = ROOT.TH1F("h_dy_AE_clean", "h_dy_AE_clean", 400, -100., 100.)

# Trigger phase 
ntp["time"].GetEvent(1)
trigPhase = tvar["ttcL1Atime"][0]-tvar["triggerTime"][0]
hist["trigPhase"] = ROOT.TH1F("trigPhase", "trigPhase", 500, trigPhase-50., trigPhase+50.)

# Particle ID stuff (PID)
hist["pid"]        = ROOT.TH1F("pid", "pid",       3,  0.5, 3.5) # 1 = muon, 2 = pion, 3 = electron
hist["nPass"]      = ROOT.TH1F("nPass", "nPass",   7, -0.5, 6.5)
hist["fracBeam_dep2"] = ROOT.TH1F("fracBeam_dep2", "fracBeam_dep2", 100, 0.0, 1.0) 



# QIE11 histograms
for ichan in chanlist:
    ieta = chanmap[ichan][0]
    iphi = chanmap[ichan][1]
    depth = chanmap[ichan][2]
    label = "ieta" + str(ieta) + "_iphi" + str(iphi) + "_depth" + str(depth)
    label2 = str(ieta) + "_" + str(iphi) + "_" + str(depth)
    hist["avgpulse", ichan] = ROOT.TProfile("AvgPulse_"+label, "AvgPulse_"+label, 10, -0.5, 9.5)
    for its in range(10):
        hist["charge", ichan, its] = ROOT.TH1F("Charge_"+label+"_ts"+str(its),
                                               "Charge_"+label+"_ts"+str(its), 8000, 0., 8000.)

    hist["e_4TS_noPS", ichan]         = ROOT.TH1F("Energy_noPS_%s"%label, "Energy_noPS_%s"%label, 256, edges10)
    hist["adc_nosub_binChris",int(float(ieta)),int(float(iphi)),int(float(depth))] = ROOT.TH1F("adc_nosub_binChris_" +label2, "adc_nosub_binChris_" +label2, 273, edgesChris) #334
    hist["real_adc_nosub_binChris",int(float(ieta)),int(float(iphi)),int(float(depth))] = ROOT.TH1F("real_adc_nosub_binChris_" +label2, "real_adc_nosub_binChris_" +label2, 256, 0, 255) #334
    hist["e_4TS_PS"     , ichan]      = ROOT.TH1F("Energy_"             +label, "Energy_"             +label, 256, edges10)
    hist["TDC_v_charge" , ichan]      = ROOT.TH2F("TDC_v_charge_"       +label, "TDC_v_charge_"       +label, 8000, 0., 8000., 1001, -0.5, 1000.5)
    hist["time_v_charge", ichan]      = ROOT.TH2F("time_v_charge_"      +label, "time_v_charge_"      +label, 8000, 0., 8000.,   76, -0.5,   75.5) # 0 = start of TS3, 75 is end of TS5
    hist["time_v_etime" , ichan]      = ROOT.TH2F("time_v_etime_"       +label, "time_v_etime_"       +label, 251, -75.5,  175.5,   251, -75.5,  175.5)
    hist["time", ichan]               = ROOT.TH1F("time_"               +label, "time_"               +label, 76  , -0.5,   75.5) # 0 = start of TS3, 75 is end of TS5
    hist["TDC" , ichan]               = ROOT.TH1F("TDC_"                +label, "TDC_"                +label, 1001, -0.5, 1000.5) # 0 = start of TS3, 75 is end of TS5
    #print "Nbins: %i, lowedge: "%(hist["e_4TS_noPS", ichan].GetNbinsX())
    #print [hist["e_4TS_noPS", ichan].GetXaxis().GetBinLowEdge(i) for i in xrange(1,247)]



    hist["time_v_trigPhase" , ichan] = ROOT.TH2F("time_v_trigPhase_" +label, "time_v_trigPhase_" +label, 251, -75.5,  175.5,   500, trigPhase-50., trigPhase+50.)

for depth in valid_depth:

    valid_ieta_max = valid_ieta[-1]
    valid_ieta_min = valid_ieta[0]
    valid_iphi_max = valid_iphi[-1]
    valid_iphi_min = valid_iphi[0]

    if valid_ieta_max - valid_ieta_min < 8:  valid_ieta_max = valid_ieta_min + 8 
    if valid_iphi_max - valid_iphi_min < 8:  valid_iphi_max = valid_iphi_min + 8

    valid_depth_max = valid_depth[-1]
    valid_depth_min = valid_depth[0]

    hist["e_4TS_etaphi",depth] = ROOT.TProfile2D("Energy_Avg_depth"+str(depth),"Average Energy per event in each ieta,iphi for depth "+str(depth), 
                                                 (valid_ieta_max - valid_ieta_min)+3, valid_ieta_min-1.5, valid_ieta_max+1.5, 
                                                 (valid_iphi_max - valid_iphi_min)+3, valid_iphi_min-1.5, valid_iphi_max+1.5)
    hist["occupancy_event_etaphi",depth] = ROOT.TH2F("Occ_Event_depth_"+str(depth),"Fraction of Events with a hit in each ieta,iphi for depth "+str(depth), 
                                                     (valid_ieta_max - valid_ieta_min)+3, valid_ieta_min-1.5, valid_ieta_max+1.5,
                                                     (valid_iphi_max - valid_iphi_min)+3, valid_iphi_min-1.5, valid_iphi_max+1.5)

for iphi in valid_iphi:
    hist["e_4TS_etadepth",iphi] = ROOT.TProfile2D("Energy_Avg_phi"+str(iphi),"Average Energy per event in each ieta,depth for iphi "+str(iphi), 
                                                  (valid_ieta_max - valid_ieta_min)+3, valid_ieta_min-1.5, valid_ieta_max+1.5, 
                                                  (valid_depth_max - valid_depth_min)+3, valid_depth_min-1.5, valid_depth_max+1.5)

    
#Plot average 4TS energy sum (z-axis) in plane of track coords from WC C
for ichan in chanlist:
    ieta = chanmap[ichan][0]
    iphi = chanmap[ichan][1]
    depth = chanmap[ichan][2]
    label = "ieta" + str(ieta) + "_iphi" + str(iphi) + "_depth" + str(depth)
    hist["e_wcC"  , ichan] = ROOT.TH2F("h_e_wcC_"+label, "h_e_wcC_"+label  , 100 , -100., 100., 100, -100., 100.)
    hist["e_wcC_x", ichan] = ROOT.TH1F("h_e_wcC_x_"+label, "h_e_wcC_x_"+label, 400 , -100., 100.)
    hist["e_wcC_y", ichan] = ROOT.TH1F("h_e_wcC_y_"+label, "h_e_wcC_y_"+label, 400 , -100., 100.)
    hist["e_wcC_noTScut"  , ichan] = ROOT.TH2F("h_e_wcC_noTScut_"+label, "h_e_wcC_noTScut_"+label  , 100 , -100., 100., 100, -100., 100.)
    hist["e_wcC_x_noTScut", ichan] = ROOT.TH1F("h_e_wcC_x_noTScut_"+label, "h_e_wcC_x_noTScut_"+label, 400 , -100., 100.)
    hist["e_wcC_y_noTScut", ichan] = ROOT.TH1F("h_e_wcC_y_noTScut_"+label, "h_e_wcC_y_noTScut_"+label, 400 , -100., 100.)
    hist["e_wcC_ratio"  , ichan] = ROOT.TH2F("h_e_wcC_ratio_"+label, "h_e_wcC_ratio_"+label  , 100 , -100., 100., 100, -100., 100.)
    hist["e_wcC_x_ratio", ichan] = ROOT.TH1F("h_e_wcC_x_ratio_"+label, "h_e_wcC_x_ratio_"+label, 400 , -100., 100.)
    hist["e_wcC_y_ratio", ichan] = ROOT.TH1F("h_e_wcC_y_ratio_"+label, "h_e_wcC_y_ratio_"+label, 400 , -100., 100.)
#    hist["e_4TS"  , ichan] = ROOT.TH1F("h_e_4TS_chan"+str(chanmap[ichan])  , "h_e_4TS_chan"+str(chanmap[ichan])  , 4002,  -0.5, 2000.5)
#
#    hist["e_4TS_withSCSN", ichan] = ROOT.TH1F("h_e_4TS_withSCSN_chan"+str(chanmap[ichan]),
#                                              "h_e_4TS_withSCSN_chan"+str(chanmap[ichan]),
#                                              4002,  -0.5, 2000.5)

esum = {}
        
####################################################
# Event Loop
####################################################

fillEplots = True

print "Run %5i has %7i total events. " % (runnum, nevts)

# Run over all events starting from event 'start'
nevts_to_run = nevts - start
# If not running over all events (nevents != -1), check that there are a sufficient number, otherwise just run over all of it.
if nevents != -1 and nevents <= (nevts - start):
    nevts_to_run = nevents

print "Processing ",nevts_to_run," events."    
for ievt in xrange(start, start + nevts_to_run):
    if (ievt+1) % 1000 == 0: print "Processing Run %5i Event %7i" % (runnum, (ievt+1))

    #########################
    # Trigger time
    #########################
    ntp["time"].GetEvent(ievt)
    trigPhase = tvar["ttcL1Atime"][0]-tvar["triggerTime"][0]
    hist["trigPhase"].Fill(trigPhase)

    #######################
    # WC Analysis
    #######################
    ntp["wc"].GetEvent(ievt)

    # Count events with hits in each view of all WC
    # and determine cleaning
    ###############################################
    has = {}
    for ivname in vname["wc"]:
        has[ivname] = False
        isize = int(vec[ivname].size())
        wc_counts[ivname, isize] += 1.
        #  KeyError: ('yC', 20)
        if isize == 1: has[ivname] = True

    for iwc in wcList:
        has[iwc] = has["x"+iwc] and has["y"+iwc]
        if has[iwc]: wc_counts[iwc] += 1.
    has["AB"]   = has["A"]   and has["B"]
    has["ABC"]  = has["AB"]  and has["C"]
    #has["ABCD"] = has["ABC"] and has["D"]
    #has["ABCE"] = has["ABC"] and has["E"]
    #for iwc in ["AB", "ABC", "ABCD", "ABCE"]:
    for iwc in ["AB","ABC"]:
        if has[iwc]: wc_counts[iwc] += 1.

    #clean = False  #This is commented to be able to run analysis over LED runs
    clean = True
    if has["ABC"]: 
        xA = vec["xA"].at(0); yA = vec["yA"].at(0)
        xB = vec["xB"].at(0); yB = vec["yB"].at(0)
        xC = vec["xC"].at(0); yC = vec["yC"].at(0)
        #xD = vec["xD"].at(0); yD = vec["yD"].at(0)
        #xE = -1.*vec["xE"].at(0); yE = vec["yE"].at(0)
        
        hist["dx_BC"].Fill(xB-xC)
        hist["dy_BC"].Fill(yB-yC)
        hist["dx_AC"].Fill(xA-xC)
        hist["dy_AC"].Fill(yA-yC)
        #hist["dx_AE"].Fill(xA-xE)
        #hist["dy_AE"].Fill(yA-yE)

        passXBCp = False; passXBCm = False; passYBCp = False; passYBCm = False;
        passXACp = False; passXACm = False; passYACp = False; passYACm = False;
        
        if xB-xC < wc_res["x", "BC", "mean"]+sigma_thold*wc_res["x", "BC", "rms" ]: passXBCp = True
        if xB-xC > wc_res["x", "BC", "mean"]-sigma_thold*wc_res["x", "BC", "rms" ]: passXBCm = True
        if yB-yC < wc_res["y", "BC", "mean"]+sigma_thold*wc_res["y", "BC", "rms" ]: passYBCp = True
        if yB-yC > wc_res["y", "BC", "mean"]-sigma_thold*wc_res["y", "BC", "rms" ]: passYBCm = True
        if xA-xC < wc_res["x", "AC", "mean"]+sigma_thold*wc_res["x", "AC", "rms" ]: passXACp = True
        if xA-xC > wc_res["x", "AC", "mean"]-sigma_thold*wc_res["x", "AC", "rms" ]: passXACm = True
        if yA-yC < wc_res["y", "AC", "mean"]+sigma_thold*wc_res["y", "AC", "rms" ]: passYACp = True
        if yA-yC > wc_res["y", "AC", "mean"]-sigma_thold*wc_res["y", "AC", "rms" ]: passYACm = True

        if passXBCp: wc_counts["passXBCp"] += 1.
        if passXBCm: wc_counts["passXBCm"] += 1.
        if passYBCp: wc_counts["passYBCp"] += 1.
        if passYBCm: wc_counts["passYBCm"] += 1.
        if passXACp: wc_counts["passXACp"] += 1.
        if passXACm: wc_counts["passXACm"] += 1.
        if passYACp: wc_counts["passYACp"] += 1.
        if passYACm: wc_counts["passYACm"] += 1.

        if passXBCp and passXBCm and passYBCp and passYBCm and passXACp and passXACm and passYACp and passYACm:
            clean = True

            hist["dx_BC", "clean"].Fill(xB-xC)
            hist["dy_BC", "clean"].Fill(yB-yC)
            hist["dx_AC", "clean"].Fill(xA-xC)
            hist["dy_AC", "clean"].Fill(yA-yC)
            #hist["dx_AE", "clean"].Fill(xA-xE)
            #hist["dy_AE", "clean"].Fill(yA-yE)
        


    # Select events with straight tracks by requiring that 
    # events have one and only one x hit and 1-and-only-1 y hit in WC A, B, C, E
    # and events are within N standard deviations of xWC1 - xWC2 residuals

    if not clean: continue
    wc_counts["clean"] += 1.

    # Fill histograms
    ########################
    for iwc in wcList:
        if has[iwc] and vec["x"+refchamb].size() and vec["y"+refchamb].size(): 
            x = adjust["x", iwc, runnum]*vec["x"+iwc].at(0)
            y = adjust["y", iwc, runnum]*vec["y"+iwc].at(0)
            hist["x"+iwc+"_v_y"+iwc].Fill(x, y)   # x vs y within WC
            hist["x"+iwc]           .Fill(x) # x within WC
            hist["y"+iwc]           .Fill(y) # y within WC
            if clean: 
                hist["x"+iwc+"_v_y"+iwc, "clean"].Fill(x, y) # x vs y within WC
                hist["x"+iwc, "clean"]           .Fill(x) # x within WC
                hist["y"+iwc, "clean"]           .Fill(y) # y within WC

        for ip1 in wcList:
            if not has[iwc] or not has[ip1]: continue
            if ((iwc == "A" and ip1 == "B") or (iwc == "A" and ip1 == "C") or (iwc == "A" and ip1 == "D") or (iwc == "A" and ip1 == "E") or 
                (iwc == "B" and ip1 == "C") or (iwc == "B" and ip1 == "D") or (iwc == "B" and ip1 == "E") or
                (iwc == "C" and ip1 == "D") or (iwc == "C" and ip1 == "E") or
                (iwc == "D" and ip1 == "E")):
                
                for ixy in ["x", "y"]:
                    xy_iwc = adjust[ixy, iwc, runnum]*vec[ixy+iwc].at(0)
                    xy_ip1 = adjust[ixy, ip1, runnum]*vec[ixy+ip1].at(0)
                    
                    hist[ixy+iwc+"_v_"+ixy+ip1].Fill(xy_iwc, xy_ip1) # xWC1 vs xWC2 and yWC1 vs yWC2
                    if clean: hist[ixy+iwc+"_v_"+ixy+ip1, "clean"].Fill(xy_iwc, xy_ip1) # xWC1 vs xWC2 and yWC1 vs yWC2
                        

    # Check if beam is within edges of sample
    isIn = {}
    for ichan in chanlist:
	if vec["x"+refchamb].size() and vec["y"+refchamb].size():
        	xL = edges[ichan, runnum][0]
        	xH = edges[ichan, runnum][1]
        	yL = edges[ichan, runnum][2]
        	yH = edges[ichan, runnum][3]
        	ix = adjust["x", refchamb, runnum]*vec["x"+refchamb].at(0)
        	iy = adjust["y", refchamb, runnum]*vec["y"+refchamb].at(0)
        	if ix<xH and ix>xL and iy<yH and iy>yL: 
            		isIn[ichan] = True
        	else:
            		isIn[ichan] = False
            	if isIn[ichan]: wc_counts["nIn", ichan] += 1.
 
    #######################
    # QIE Analysis
    #######################
    ntp["hcal"].GetEvent(ievt)

    # Find the channels 
    ########################
    
    # ichan is the channel number (a single integer index) defined in tb_chanmap.py
    # corresponding to a specific ieta,iphi,depth.
    #
    # chanlist contains a list of the channel numbers to process.
    
    # create chansToFind, a list of [(ieta1,iphi1,depth1), (ieta2,iphi2,depth2), ...]
    # for processing
    
    chansToFind = []
    for ichan in chanlist: chansToFind.append(chanmap[ichan])

    if verbose: print "chansToFind:", chansToFind
    
    # rchan is the channel number associated with (ieta,iphi,depth) in the data
    # rchan probably doesn't equal ichan, which is just an index

    # By matching (ieta,iphi,depth), we create a mapping of fchan[ichan] = rchan
    # fchan contains the found channels    
            
    fchan = {}
    fread = {}
    for rchan in xrange(shcal.numChs):
        test_chan = (shcal.ieta[rchan], shcal.iphi[rchan], shcal.depth[rchan])
        if test_chan in chansToFind:
            chansToFind.remove(test_chan)
            fchan[chanmap[test_chan]] = rchan
            fread[test_chan] = shcal

    if verbose:
        print "fchan:", fchan

    # these are the (ieta,iphi,depth) that we expected to find
    # (from chanlist/chanmap) that never appeared in the data
    
    #if len(chansToFind) > 0:
    #    print "Did not find channels ", chansToFind
        
    # Skip events with anomalously large pulses
    clean = True
    #for rchan in fchan.itervalues():
    #    for its in range(2): #for now, only check lowest two ts (0-1)
    #        if fread[rchan].pulse[rchan*MAXTS+its] > 90:
    #            clean = False
    #            break
    #    #for its in range(8,10): #for now, only check highest two ts (8-9)
    #    #    if fread[rchan].pulse[rchan*MAXTS+its] > 90: 
    #    #        clean = False
    #    #        break
    #if not clean: continue

    # Skip events with anomalous energy
    #for rchan in fchan.itervalues():
    #    for its in range(10):  #ts (0-9)
    #        if fread[rchan].pulse[rchan*MAXTS+its] > 1500:
    #            clean = False
    #            break
    #if not clean: continue

    charge = {} 
    charge_adc = {}
    energy = {}   
    tdc    = {}

    # PID variables
    ################
    eBeam = {} # dictionary for holding energies of depths for tower the beam is pointed at
    for idep in range(2,7):
        eBeam[idep] = 0.

    showerE = 0.  # shower energy
    showerChans = []  # channels in which to sum shower energy
    for ieta in range(beamEta-1,beamEta+2):
        for iphi in range(beamPhi-1,beamPhi+2):            
            for idep in range(2,7):
                showerChans.append((ieta, iphi, idep))

    for ichan,rchan in fchan.iteritems():
        ieta, iphi, depth = chanmap[ichan]
        detType = fread[(ieta,iphi,depth)].detType[rchan]
        isPhase1 = True if detType == HCAL_DET_ngHE else False

        if verbose:
            print "processing ichan %s, rchan %s" % (ichan, rchan)
            print "corresponding to ieta %s, iphi %s, depth %s" % (ieta, iphi, depth)

        # Pull charges and energies for each time sample, convert to fC when appropriate
        nts = fread[(ieta,iphi,depth)].numTS[rchan]
        for its in xrange(nts):
            if adc:
                charge[ichan,its] = fread[(ieta,iphi,depth)].pulse_adc[rchan*MAXTS+its]  #[row][col] -> [row*n_cols + col]
                energy[ichan,its] = charge[ichan,its]
            else:
                charge[ichan,its] = fread[(ieta,iphi,depth)].pulse[rchan*MAXTS+its]  #[row][col] -> [row*n_cols + col]
                charge_adc[ichan,its] = fread[(ieta,iphi,depth)].adc[rchan*MAXTS+its]
                energy[ichan,its] = charge[ichan,its]*calib[ichan]

            # TDC only available for QIE11 not HBHE
            if isPhase1:  tdc[ichan,its]   = fread[(ieta,iphi,depth)].tdc[rchan*MAXTS+its]  #[row][col] -> [row*n_cols + col]

        if verbose:
            print "charge: ", ",".join([str(charge[ichan,its]) for its in xrange(nts)])

        # Pedestals are stored in the output for h2testbeamanalyzer
        #ped_ts_list = [1,2]   #time samples in which to sum charge for pedestals (1-2)    
        #ped_esum = 0.
        #for its in ped_ts_list:   
        #    ped_esum += energy[ichan,its]
        #ped_avg = ped_esum/len(ped_ts_list)    
        esum[ichan, "PED"] = fread[(ieta,iphi,depth)].ped[rchan]*calib[ichan]

        if verbose:
            print "Pedestal (fC) = %s" % (fread[(ieta,iphi,depth)].ped[rchan])

        # Compute signal and pedestal-subtracted signal
        ts_list = xrange(3,3+sigTS) # [3,4,5,6,7,8,9]   #time samples in which to sum charge for signal
        ###if (nts == 8): ts_list = range(2,7)             #temporary use for HB
        if (nts == 8): ts_list = 7             #temporary use for HB
        sig_esum = 0.
        sig_esum_ps = 0.
        adc_sig_esum = 0
        ###for its in ts_list:  
        if(ts_list == 7): 
            its = ts_list  
            if adc:
                sig_esum    += charge_adc[ichan,its]
            else:
                sig_esum    += energy[ichan,its]
                sig_esum_ps += energy[ichan,its] - esum[ichan, "PED"]  #pedestal-subtracted energy  
                adc_sig_esum    += charge_adc[ichan,its]
        esum[ichan, "4TS_noPS"] = sig_esum
        esum[ichan, "4TS_PS"] = sig_esum_ps          
        esum[int(float(ieta)),int(float(iphi)),int(float(depth)),"noPS"] = sig_esum
        esum[int(float(ieta)),int(float(iphi)),int(float(depth)),"PS"] = sig_esum_ps
        esum[int(float(ieta)),int(float(iphi)),int(float(depth)),"adc_noPS"] = adc_sig_esum
        
        # fill pid vars
        if (ieta,iphi,depth) in showerChans:
            #print "(ieta,iphi,depth,energy) =",ieta,iphi,depth,esum[ichan, "4TS_PS"]    #JRD
            showerE += esum[ichan, "4TS_PS"]
            
        if ieta == beamEta and iphi == beamPhi and depth in range(2,7):
            eBeam[depth] = esum[ichan, "4TS_PS"]

        # Fill histograms
        ####################

        # Fill LinkError plot
        if fillEplots:
            # Only make link error plot if we have the information
            if hasattr(fread[(ieta,iphi,depth)], 'link_error'):
                if ("link_error", ichan) not in hist:
                    label = "ieta%s_iphi%s_depth%s" % (ieta, iphi, depth)
                    hist["link_error", ichan] = ROOT.TH1F("Link_Error_" +label, "Link Errors for "+label,   2, 0, 2)

                hist["link_error", ichan].Fill(fread[(ieta,iphi,depth)].link_error[rchan])


        # Fill pulse shape plot
        if fillEplots: 
            for its in range(nts):
                hist["avgpulse", ichan].Fill(its,energy[ichan,its])

        # Fill 4TS energy sum plot
        if fillEplots: hist["e_4TS_noPS", ichan].Fill(esum[ichan, "4TS_noPS"])

        # Fill 4TS pedestal-corrected energy sum plot
        if fillEplots: hist["e_4TS_PS", ichan].Fill(esum[ichan, "4TS_PS"])
        
        # Fill time vs. charge plots
        if fillEplots and isPhase1:
            time  = 0.
            tsoi  = -9
            esum10 = 0.
            for its in range(nts):
                hist["TDC_v_charge" , ichan].Fill(charge[ichan,its], tdc[ichan,its]+its*100.)
                hist["TDC" , ichan].Fill(tdc[ichan,its]+its*100.)
                # Find sample of interest as sample before first with TDC=62 (started above threshold)
                if tdc[ichan,its] == 62 and tsoi<0: tsoi = its-1
                esum10 += charge[ichan,its]

            # convert to units of ns since start of TS3
            if tsoi>0: time = tdc[ichan,tsoi]*0.5 + 25.*(tsoi-3.)

            # Find energy weighted time for comparison
            etime_ts = 0.
            for its in range(nts):
                etime_ts += its * charge[ichan,its]/esum10  # E-weighted time in units of TS
            # convert to units of ns since start of TS3
            etime = 25.*(etime_ts-3.)
            
            if tsoi > 0:
                hist["time_v_charge", ichan].Fill(charge[ichan,its], time)
                hist["time", ichan]  .Fill(time)
                hist["time_v_etime" , ichan].Fill(etime, time)
                hist["time_v_trigPhase" , ichan].Fill(time, trigPhase)
                
        # Fill energy profile in ieta, iphi
        if fillEplots:            
            ieta = chanmap[ichan][0]
            iphi = chanmap[ichan][1]
            depth = chanmap[ichan][2]
            multip = 1.0
            if (not isPhase1):
		  multip = 280.0
            hist["e_4TS_etaphi", depth].Fill(ieta, iphi, esum[ichan, "4TS_PS"]*multip)
            hist["e_4TS_etadepth", iphi].Fill(ieta, depth, esum[ichan, "4TS_PS"]*multip)
            hist["occupancy_event_etaphi", depth].Fill(ieta,iphi,1./nevts)  #a bit ugly
            
            x_25=0
            y_25=0
            # Fill plot of wire chamber position for events with sufficient energy
            if esum[ichan, "4TS_PS"]>25. and vec["x"+refchamb].size() and vec["y"+refchamb].size():
                x = adjust["x", refchamb, runnum]*vec["x"+refchamb].at(0)
                y = adjust["y", refchamb, runnum]*vec["y"+refchamb].at(0)
                hist["e_wcC"  , ichan].Fill(x,y)
                hist["e_wcC_x", ichan].Fill(x)
                hist["e_wcC_y", ichan].Fill(y)
                x_25 = adjust["x", refchamb, runnum]*vec["x"+refchamb].at(0)
                y_25 = adjust["y", refchamb, runnum]*vec["y"+refchamb].at(0)
            
            # Fill plot of wire chamber position for all events added by Abdollah
            if esum[ichan, "4TS_PS"]>-100000 and vec["x"+refchamb].size() and vec["y"+refchamb].size(): # Fill all events
                x = adjust["x", refchamb, runnum]*vec["x"+refchamb].at(0)
                y = adjust["y", refchamb, runnum]*vec["y"+refchamb].at(0)
                hist["e_wcC_noTScut"  , ichan].Fill(x,y)
                hist["e_wcC_x_noTScut", ichan].Fill(x)
                hist["e_wcC_y_noTScut", ichan].Fill(y)

    # Fill Chris' noPS charge plots 
    ###############################
    if fillEplots:         
        for eta in range(1,26):
            for phi in range(3,7):
                for idepth in range(1,8):
                    #Cut for isolated muon
                    e_neighbor = 0.
                    if (eta,phi,idepth,'noPS') in esum:
                        hist["real_adc_nosub_binChris",eta,phi,idepth].Fill(esum[eta,phi,idepth, "adc_noPS"])
                        for e in range(eta-1,eta+2):
                            for p in range(phi-1,phi+2):
                                if (e,p,idepth,'noPS') in esum:
                                    e_neighbor += esum[e,p,idepth,"noPS"]
                        e_neighbor -= esum[eta,phi,idepth,"noPS"]
                        if e_neighbor < 6*41:            
                        #Cut for muon in whole tower
                            #print e_neighbor
                            #print esum[eta,phi,idepth, "noPS"]
                            if idepth == 2 and (esum[eta,phi,3,"noPS"] > 2*41):                    
                                if (eta,phi,2,'noPS') in esum:
                                    #print esum[eta,phi,idepth, "noPS"]
                                    hist["adc_nosub_binChris",eta,phi,idepth].Fill(esum[eta,phi,idepth, "noPS"])
                                    #hist["real_adc_nosub_binChris",eta,phi,idepth].Fill(esum[eta,phi,idepth, "adc_noPS"])                                    
                            if idepth == 3 and (esum[eta,phi,2,"noPS"] > 2*41):                    
                                if (eta,phi,3,'noPS') in esum:
                                    hist["adc_nosub_binChris",eta,phi,idepth].Fill(esum[eta,phi,idepth, "noPS"])
                                    #hist["real_adc_nosub_binChris",eta,phi,idepth].Fill(esum[eta,phi,idepth, "adc_noPS"])
    
    # Do PID
    ##############
    isMuon = False; 
    isElectron = False; 

    # muon
    nPass = 0
    for idep in range(2,7):
        if shunt == 6:
            if eBeam[idep] > 20. and eBeam[idep] < 600.: nPass += 1
        elif shunt == 1:
            if eBeam[idep] > 120. and eBeam[idep] < 3600.: nPass += 1

    if nPass >= 4: isMuon = True

    #electron
    eBeam_dep2_frac = 0.
    if showerE > 0.:
	 eBeam_dep2_frac = eBeam[2]/showerE

    if not isMuon and eBeam_dep2_frac > 0.9: isElectron = True

    if isMuon       : hist["pid"].Fill(1)
    elif isElectron : hist["pid"].Fill(2)
    else            : hist["pid"].Fill(3)

    hist["nPass"].Fill(nPass)
    hist["fracBeam_dep2"].Fill(eBeam_dep2_frac)

###Sort the histograms
SortedHist = outtfile.mkdir("SortedHist")
wire_chamber_hist = SortedHist.mkdir("Wire_chamber_hist")
Charge_hist = SortedHist.mkdir("Charge_hist")
Link_Error_hist = SortedHist.mkdir("Link_Error_hist")
AvgPulse_hist = SortedHist.mkdir("AvgPulse_hist")
Energy_hist = SortedHist.mkdir("Energy_hist")
Chris_noPS_hist = SortedHist.mkdir("Chris_noPS_hist")
other_hist = SortedHist.mkdir("Other_hist")
#h_x_hist = SortedHist.mkdir("h_x_hist")
#h_y_hist = SortedHist.mkdir("h_y_hist")
#h_dx_hist = SortedHist.mkdir("h_dx_hist")
#h_dy_hist = SortedHist.mkdir("h_dy_hist")
SortedHist.cd()

#print hist.keys()

for key,val in hist.items():
    if key[0].find("wcC") >= 0:
        wire_chamber_hist.cd()
        val.Write()
    elif key[0].find("charge") >= 0:
        Charge_hist.cd()
        #print "Found Charge hist"
        val.Write()
    elif key[0].find("link") >= 0:
        Link_Error_hist.cd()
        val.Write()
    elif key[0].find("avgpulse") >= 0:
        AvgPulse_hist.cd()
        val.Write()
    elif key[0].find("e") >= 0:
        Energy_hist.cd()
        val.Write()
    elif key[0].find("binChris") >= 0:
        Chris_noPS_hist.cd()
        val.Write()
    elif key[0].find("real") >= 0:
        Chris_noPS_hist.cd()
        val.Write()        
    else:
        other_hist.cd()
        val.Write()
    #elif key[0].find("h_x") >= 0:
    #    h_x_hist.cd()
    #    val.Write()
    #elif key[0].find("h_y") >= 0:
    #    h_y_hist.cd()
    #    val.Write()
    #elif key[0].find("h_dx") >= 0:
    #    h_dx_hist.cd()
    #    val.Write()
    #elif key[0].find("h_dy") >= 0:
    #    h_dy_hist.cd()
    #    val.Write()

outtfile.cd()


#
#print "Fraction of events with N hits in each WC view"
#print "============================================================"
#print "view : N hits : fraction"
#for ivname in vname["wc"]:
#    for isize in range(5):
#        print "%2s : %1i : %5.2f" % (ivname, isize , wc_counts[ivname, isize]/nevts)
#    print " "
#
#print "Efficiency for requiring WC combinations in event"
#print "============================================================"
#for iwc in ["A","B", "C", "D", "E", "AB", "ABC", "ABCD", "ABCE"]:
#    print "WC %4s : %5.2f" % (iwc, wc_counts[iwc]/nevts)
#
#print " "
#print " "
#print "Track event cleaning efficiency for hitting each sample:"
#print "============================================================"
#print "WC quantity : efficiency "
#print "x_BC_p : %5.2f " % (wc_counts["passXBCp"]/nevts)
#print "x_BC_m : %5.2f " % (wc_counts["passXBCm"]/nevts)
#print "y_BC_p : %5.2f " % (wc_counts["passYBCp"]/nevts)
#print "y_BC_m : %5.2f " % (wc_counts["passYBCm"]/nevts)
#print "x_AC_p : %5.2f " % (wc_counts["passXACp"]/nevts)
#print "x_AC_m : %5.2f " % (wc_counts["passXACm"]/nevts)
#print "y_AC_p : %5.2f " % (wc_counts["passYACp"]/nevts)
#print "y_AC_m : %5.2f " % (wc_counts["passYACm"]/nevts)
#print "Total  : %5.2f " % (   wc_counts["clean"]/nevts)
#print " "
#print " "
#print "Geometric event cleaning efficiency for hitting each sample:"
#print "============================================================"
#print "Channel : description : efficiency for clean events : total efficiency"
#for ichan in chanlist:
#    print "%3i : %30s : %5.2f : %5.2f" % (ichan, chanType[ichan, runnum], wc_counts["nIn", ichan]/wc_counts["clean"], wc_counts["nIn", ichan]/nevts)

#if os.path.isfile(outfile):
#    method = "update"
#else:
#    method = "recreate"

outtfile.Write()
outtfile.Close()

print "Finished Run %5i." % runnum
