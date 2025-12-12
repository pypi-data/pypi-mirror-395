#!/usr/bin/python3

# Date:
# 20220628

import os
import argparse
import math

cell = []


print("""
##############################################################
#
# Correction for MULTI-LATTICE TRANSLOCATION defects
#
# https://github.com/kolenpe1/translocation - source
# https://kmlinux.fjfi.cvut.cz/~kolenpe1/translocation - doc
##############################################################
""")




##################################################
#
# PARSING ARGUMENTS
#
##################################################


parser=argparse.ArgumentParser(
	prog='python3 -m translocation',
	formatter_class=argparse.RawDescriptionHelpFormatter,
	)

parser.add_argument("-c", "--cell", type=int, help="unit cell parameters",     \
    nargs='+')
# PARSING OF THE INPUT FILES
parser.add_argument("--mtz_I", type=str, help="input MTZ file with intensities")
parser.add_argument("--I_label", type=str, help="label for intensities")
parser.add_argument("--SIGI_label", type=str, help="label for sigmas")
parser.add_argument("--mtz_F", type=str,                                       \
	help="input MTZ file with structure factors")
parser.add_argument("--F_label", type=str, help="label for structure factors")
parser.add_argument("--SIGF_label", type=str, help="label for sigmas")
parser.add_argument("--hkl", type=str,                                         \
	help="input file with SHELX-like structure factors")
parser.add_argument("--HKL", type=str, help="XDS_ASCII.HKL input file from XDS")
parser.add_argument("--sca", type=str, help="input SCA file with intensities")
parser.add_argument("--sca_ignore", type=int,                                  \
	help="how many initial lines should be ignored (do not contain data)")
# PARSING OF THE TRANSLOCATION FRACTIONS
parser.add_argument("--k1", type=float,                                        \
	help="fraction of the 1st translocation disorder")
parser.add_argument("--fc1", type=float, nargs='+', 
    help="fractional coordinates of the 1st translocation disorder")
parser.add_argument("--k2", type=float,                                        \
	help="fraction of the 2nd translocation disorder")
parser.add_argument("--fc2", type=float, nargs='+', 
    help="fractional coordinates of the 2nd translocation disorder")
parser.add_argument("--k3", type=float,                                        \
	help="fraction of the 3rd translocation disorder")
parser.add_argument("--fc3", type=float, nargs='+', 
    help="fractional coordinates of the 3rd translocation disorder")
parser.add_argument("--k4", type=float,                                        \
	help="fraction of the 4th translocation disorder")
parser.add_argument("--fc4", type=float, nargs='+', 
    help="fractional coordinates of the 4th translocation disorder")
parser.add_argument("--k5", type=float,                                        \
	help="fraction of the 5th translocation disorder")
parser.add_argument("--fc5", type=float, nargs='+', 
    help="fractional coordinates of the 5th translocation disorder")
parser.add_argument("--force", "-f", action='store_true',                      \
    help="forcing output file")
parser.add_argument("-o", "--output_file", type=str,                           \
    help="defines the output file")
parser.add_argument("-d", "--division", type=float,                            \
    help="divides structure factors or intensities by a defined factor")
args = parser.parse_args()



##################################################
#
# SET AND ASSIGN VARIABLES
#
##################################################

if not args.output_file:
    args.output_file = 'output.txt'

k1, k2, k3, k4, k5 = 0, 0, 0, 0, 0
t1, t2, t3, t4, t5 = [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]

if not args.sca_ignore:
    ignore = 3
else:
    ignore = args.sca_ignore


# Assigning the fractions
if args.k1:
    k1 = args.k1
if args.k2:
    k2 = args.k2
if args.k3:
    k3 = args.k3
if args.k4:
    k4 = args.k4
if args.k5:
    k5 = args.k5

# Assigning the fractional coordinates
if args.fc1:
    if len(args.fc1) != 3:
        print('Coordinates for the first translocation disorder are defined'   \
            + ' incorrectly. Please correct the input. Exiting ...')
        exit()
    else:
        t1[0] = args.fc1[0]
        t1[1] = args.fc1[1]
        t1[2] = args.fc1[2]

if args.fc2:
    if len(args.fc2) != 3:
        print('Coordinates for the second translocation disorder are defined'  \
            + ' incorrectly. Please correct the input. Exiting ...')
        exit()
    else:
        t2[0] = args.fc2[0]
        t2[1] = args.fc2[1]
        t2[2] = args.fc2[2]

if args.fc3:
    if len(args.fc3) != 3:
        print('Coordinates for the third translocation disorder are defined'   \
            + ' incorrectly. Please correct the input. Exiting ...')
        exit()
    else:
        t3[0] = args.fc3[0]
        t3[1] = args.fc3[1]
        t3[2] = args.fc3[2]

if args.fc4:
    if len(args.fc4) != 3:
        print('Coordinates for the fourth translocation disorder are defined'   \
            + ' incorrectly. Please correct the input. Exiting ...')
        exit()
    else:
        t4[0] = args.fc4[0]
        t4[1] = args.fc4[1]
        t4[2] = args.fc4[2]

if args.fc5:
    if len(args.fc5) != 3:
        print('Coordinates for the third translocation disorder are defined'   \
            + ' incorrectly. Please correct the input. Exiting ...')
        exit()
    else:
        t5[0] = args.fc5[0]
        t5[1] = args.fc5[1]
        t5[2] = args.fc5[2]





##################################################
#
#  MAIN CALCULATION PROCEDURE
#
##################################################

# Scalar product of two vectors
def vec_fact(vektor1, vektor2):
    a = (vektor1[0] * vektor2[0]) + (vektor1[1] * vektor2[1])                  \
        + (vektor1[2] * vektor2[2])
    return a

# Difference vector calculation
def vec_diff(vektor1, vektor2):
    a = [vektor1[0]-vektor2[0], vektor1[1]-vektor2[1], vektor1[2]-vektor2[2]]
    return a


def factor(h, k, l):
#    print('Kontrola:')
    vecH = [h, k, l]
    A = 1 - k1 - k2 - k3 - k4 - k5
    # First aproximation
    ef = ( (A ** 2)                                                            \
        + (k1 ** 2) + (k2 ** 2) + (k3 ** 2) + (k4 ** 2) + (k5 ** 2)            \
        + (2 * A * k1 * math.cos(2 * math.pi * vec_fact(vecH, t1 )) )          \
        + (2 * A * k2 * math.cos(2 * math.pi * vec_fact(vecH, t2 )) )          \
        + (2 * A * k3 * math.cos(2 * math.pi * vec_fact(vecH, t3 )) )          \
        + (2 * A * k4 * math.cos(2 * math.pi * vec_fact(vecH, t4 )) )          \
        + (2 * A * k5 * math.cos(2 * math.pi * vec_fact(vecH, t5 )) )          \
        )
    # Exact value
    eff = ( (A ** 2)                                                           \
        + (k1 ** 2) + (k2 ** 2) + (k3 ** 2) + (k4 ** 2) + (k5 ** 2)            \
        + (2 * A * k1 * math.cos(2 * math.pi * vec_fact(vecH, t1 )) )          \
        + (2 * A * k2 * math.cos(2 * math.pi * vec_fact(vecH, t2 )) )          \
        + (2 * A * k3 * math.cos(2 * math.pi * vec_fact(vecH, t3 )) )          \
        + (2 * A * k4 * math.cos(2 * math.pi * vec_fact(vecH, t4 )) )          \
        + (2 * A * k5 * math.cos(2 * math.pi * vec_fact(vecH, t5 )) )          \
        # small corrections
        + (2 * k1 * k2 * math.cos(2 * math.pi                                  \
            * vec_fact(vecH, vec_diff(t1, t2) ) ) )                            \
        + (2 * k1 * k3 * math.cos(2 * math.pi                                  \
            * vec_fact(vecH, vec_diff(t1, t3) ) ) )                            \
        + (2 * k1 * k4 * math.cos(2 * math.pi                                  \
            * vec_fact(vecH, vec_diff(t1, t4) ) ) )                            \
        + (2 * k1 * k5 * math.cos(2 * math.pi                                  \
            * vec_fact(vecH, vec_diff(t1, t5) ) ) )                            \
        + (2 * k2 * k3 * math.cos(2 * math.pi                                  \
            * vec_fact(vecH, vec_diff(t2, t3) ) ) )                            \
        + (2 * k2 * k4 * math.cos(2 * math.pi                                  \
            * vec_fact(vecH, vec_diff(t2, t4) ) ) )                            \
        + (2 * k2 * k5 * math.cos(2 * math.pi                                  \
            * vec_fact(vecH, vec_diff(t2, t5) ) ) )                            \
        + (2 * k3 * k4 * math.cos(2 * math.pi                                  \
            * vec_fact(vecH, vec_diff(t3, t4) ) ) )                            \
        + (2 * k3 * k5 * math.cos(2 * math.pi                                  \
            * vec_fact(vecH, vec_diff(t3, t5) ) ) )                            \
        + (2 * k4 * k5 * math.cos(2 * math.pi                                  \
            * vec_fact(vecH, vec_diff(t4, t5) ) ) )                            \
        )
#    print("Delici faktor je: " + str(eff))
    return eff


##################################################
#
# DEFINITION OF ALL CALCULATION FUNCTIONS
#
##################################################


##################################################
# CALCULATION USING SHELX hkl FILE

def shelx_hkl():
    global cell
    global hklin
    # read the file
    with open(hklin, "r") as file:
   	    lines = file.readlines()
   	# assign Miller indices and structure factors
    for i in range(len(lines)):
        h = int(lines[i][0:4])
        k = int(lines[i][4:8])
        l = int(lines[i][8:12])
        intensity = float(lines[i][12:20])
        sigi = float(lines[i][20:28])
        # calculation of new structure factors
        fac = factor(h, k, l)
        # check if division argument is available
        if args.division:
            intensity = intensity  / (fac * args.division)
            sigi = sigi / (fac * args.division)
        else:
            intesnity = intensity / fac
            sigi = sigi / fac
        # transformation to two decimals
        intensity = "{:.2f}".format(intensity)
        sigi = "{:.2f}".format(sigi)
#        print(lines[i])
        if len(str(intensity)) > 8:
            if args.force:            
                print('Exceeding the format line. The result may be wrong.')
                print('Consider division by factor 10 or even more.')
            else:
                print('Exceeding the format line. Exiting ...')
                print('Consider division by factor 10 or even more. Use parameter \"-d 10\".')
                exit()
        if len(str(sigi)) > 8:
            if args.force:
                print('Exceeding the format line. The result may be wrong.')
            else:
                print('Exceeding the format line. Exiting ...')
                exit()
        vloz_i = (8 - len(str(intensity))) * ' ' + str(intensity)
        vloz_sigi = (8 - len(str(sigi))) * ' ' + str(sigi)
        # Puts the things into the line
        lines[i] = lines[i][:12] + str(vloz_i) + vloz_sigi + lines[i][28:]
#        print(lines[i])
    with open(args.output_file, "w") as file:
    	file.writelines(lines)




# READING FROM XDS *.HKL FILE
def read_HKL_file():
    global cell
    global hklin
    # reading unit cell parameters
    with open(hklin, 'r') as file:
        lines = file.readlines()
    for i in range(len(lines)):
        if '!UNIT_CELL_CONSTANTS' in lines[i]:
            for j in range(6):
                cell.append(float(lines[i].split()[j+1]))
    # checking for correct number of unit cell parameters
    if len(cell) != 6:
        print('Incorrect number of unit-cell parameters. Exiting ...')
        exit()
    else:
        print(cell)
        
    with open(hklin, "r") as file:
   	    lines = file.readlines()
   	# assign Miller indices and structure factors
    for i in range(len(lines)):
        if lines[i][0:1] != '!':
            h = int(lines[i][0:6])
            k = int(lines[i][6:12])
            l = int(lines[i][12:18])
            I = float(lines[i][18:29])
            sigI = float(lines[i][29:40])
            # testing function
            fac = factor(h, k, l)
            I = I / fac
            sigI = sigI / fac
            I = "{:.3E}".format(I)
            sigI = "{:.3E}".format(sigI)
#            print(lines[i])
            vloz_i = (11 - len(str(I))) * ' ' + str(I)
            vloz_sigi = (11 - len(str(sigI))) * ' ' + str(sigI)
            # Puts the things into the line
            lines[i] = lines[i][:18] + vloz_i + vloz_sigi + lines[i][40:]
#            print(lines[i])
    with open(args.output_file, "w") as file:
    	file.writelines(lines)









##################################################
# CHECK FOR THE INPUT SCA FILE

# READING FROM SCALEPACK *.sca FILE
def read_SCA_file():
    global cell
    global hklin
    # reading unit cell parameters
    with open(hklin, 'r') as file:
        lines = file.readlines()
   	# assign Miller indices and structure factors
    for i in range(ignore, len(lines)):
        h = int(lines[i][0:4])
        k = int(lines[i][4:8])
        l = int(lines[i][8:12])
        I = float(lines[i][12:20])
        sigI = float(lines[i][20:28])
        # Calculation of factor
        fac = factor(h, k, l)
        if args.division:
            I = I / ( fac * args.division )
        else:
            I = I / fac
        I = "{:.1f}".format(I)
        if args.division:
            sigI = sigI / (fac * args.division)
        else:
            sigI = sigI / fac
        sigI = "{:.1f}".format(sigI)
#        print(lines[i])
        if len(str(I)) > 7:
            if args.force:
                print('Exceeding the format line. The result may be wrong.')
                print('Consider division by factor 10 or even more.')
            else:
                print('Exceeding the format line. The result may be wrong. Exiting ...')
                print('Consider division by factor 10 or even more. Use parameter \"-d 10\".')
                exit()
        if len(str(sigI)) > 7:
            if args.force:
                print('Exceeding the format line. The result may be wrong.')
                print('Consider division by factor 10 or even more.')
            else:
                print('Exceeding the format line. The result may be wrong. Exiting ...')
                print('Consider division by factor 10 or even more. Use parameter \"-d 10\".')
                exit()
        vloz_i = (8 - len(str(I))) * ' ' + str(I)
        vloz_sigi = (8 - len(str(sigI))) * ' ' + str(sigI)
        # Puts the things into the line
        lines[i] = lines[i][:12] + str(vloz_i) + vloz_sigi + '\n'
#        print(lines[i])
    with open(args.output_file, "w") as file:
    	file.writelines(lines)


##################################################
# WORKING WITH MTZ-I DATA 
def mtz_I():
    global cell
    global hklin
    # testing for modules
    try:
        import gemmi
    except ModuleNotFoundError:
        print("The module GEMMI is not installed.\n") 
        quit()
    else:
        pass
    try:
        import numpy
    except ModuleNotFoundError:
        print("The module Numpy is not installed.\n") 
        quit()
    else:
        pass
    # import of modules
    import gemmi
    import numpy
    import math
    mtz = gemmi.read_mtz_file(args.mtz_I)
    # Adds empty column to the file
    mtz.add_column('I_new', 'J')
    mtz.add_column('SIGI_new', 'Q')
    
    # addition of new columns
    i_col = mtz.column_with_label(str(args.I_label))
    sigi_col = mtz.column_with_label(str(args.SIGI_label))
    # reading the mtz content to the array
    data = mtz.array
    fac = []
    for i in range(len(data[:,0])):
        h = int(data[i,0])
        k = int(data[i,1])
        l = int(data[i,2])
        fac.append(factor(h, k, l))
        #i_col[i] = i_col[i] / fac
        #sigi_col[i] = sigi_col[i] / fac
    # assigning new values to the mtz file array
    data[:,-2] = data[:,i_col.idx] / fac[:] 
    data[:,-1] = data[:,sigi_col.idx] / fac[:]
    mtz.write_to_file(args.output_file)


##################################################
# WORKING WITH MTZ-F DATA 
def mtz_F():
    global cell
    global hklin
    # testing for modules
    try:
        import gemmi
    except ModuleNotFoundError:
        print("The module GEMMI is not installed.\n") 
        quit()
    else:
        pass
    try:
        import numpy
    except ModuleNotFoundError:
        print("The module Numpy is not installed.\n") 
        quit()
    else:
        pass
    # import of modules
    import gemmi
    import numpy
    import math
    mtz = gemmi.read_mtz_file(args.mtz_F)
    # Adds empty column to the file
    mtz.add_column('FP_new', 'F')
    mtz.add_column('SIGFP_new', 'Q')
    
    # addition of new columns
    f_col = mtz.column_with_label(str(args.F_label))
    sigf_col = mtz.column_with_label(str(args.SIGF_label))
    # reading the mtz content to the array
    data = mtz.array
    facf = []
    for i in range(len(data[:,0])):
        h = int(data[i,0])
        k = int(data[i,1])
        l = int(data[i,2])
        facf.append(math.sqrt(factor(h, k, l)))
    # assigning new values to the mtz file array
    data[:,-2] = data[:,f_col.idx] / facf[:] 
    data[:,-1] = data[:,sigf_col.idx] / facf[:] 
    mtz.write_to_file(args.output_file)





##################################################
#
#   MAIN ALGORITHM
#
##################################################

def check_output():
    if os.path.exists(args.output_file):
        hklout = os.path.exists(args.output_file)
        if args.force:
            print('Output file exists and will be overwritten.')
            print('Output file: ' + str(hklout))
        else:
            print('Output file exists. Please supply another file name.'      \
                + ' Exiting ...')
            exit()
    else:
        print('Output file: ' + str(args.output_file))


def main():
    global hklin

    ##################################################
    # CHECK FOR NUMBER OF UNIT CELL PARAMETERS
    if args.cell:
        if len(args.cell) != 6:
            print('Incorrect number of unit cell parameters (' 	                   \
                + str(len(args.cell)) + '). Please, check the input.')
            exit()
    
    
    ##################################################
    # CHECK FOR THE INPUT MTZ_I FILE
    if args.mtz_I:
        if os.path.exists(args.mtz_I):
            hklin = os.path.abspath(args.mtz_I)
            print('Input MTZ file: ' + str(hklin))
            check_output()
            mtz_I()
            print('Calculations finished.')
        else:
            print('MTZ file does not exist. Exiting ...')
            exit()
    
    ##################################################
    # CHECK FOR THE INPUT MTZ_F FILE
    if args.mtz_F:
        if os.path.exists(args.mtz_F):
            hklin = os.path.abspath(args.mtz_F)
            print('Input MTZ file: ' + str(hklin))
            check_output()
            mtz_F()
            print('Calculations finished.')
        else:
            print('MTZ file does not exist. Exiting ...')
            exit()
    
    ##################################################
    # CHECK FOR THE INPUT SHELX FILE
    if args.hkl:
        if os.path.exists(args.hkl):
            hklin = str(os.path.abspath(args.hkl))
            print('Input hkl file: ' + hklin)
            check_output()
            shelx_hkl()
            print('Calculations finished.')
        else:
            print('HKL file does not exist. Exiting ...')
            exit()
    
    ##################################################
    # CHECK FOR THE INPUT SCALEPACK FILE
    if args.sca:
        if os.path.exists(args.sca):
            hklin = str(os.path.abspath(args.sca))
            print('Input SCA file: ' + str(hklin))
            check_output()
            read_SCA_file()
            print('Calculations finished.')
        else:
            print('SCA file does not exist. Exiting ...')
            exit()
    
    
    ##################################################
    # CHECK FOR THE INPUT XDS FILE
    if args.HKL:
        if os.path.exists(args.HKL):
            hklin = str(os.path.abspath(args.HKL))
            print('Input HKL file: ' + hklin)
            check_output()
            read_HKL_file()
            print('Calculations finished.')
        else:
            print('HKL file does not exist. Exiting ...')
            exit()
