#!/usr/bin/python3

#***
#*
#* Written by Melanie Cornelius (nee Dooley)
#* October 2015
#*
#* Written for IIT IPRO: Developing an Antimatter Gravity Interferometer
#*
#* Licensed under the GNU General Public License version 3, Copyright 2015
#* Please see official GNU web listing for more information
#*
#* PROGRAM FUNCTIONALITY:
#*      This program takes user input and uses it to call structure_methods.py.
#*      From there, a *.stl file is generated in accordance with the user's 
#*      stated preferences.
#***

import stl_tools
import numpy
import math
import structure_methods
import argparse

def create_grating(col, row, width, pitch):
    height = pitch // 2
    columnar_matrix = structure_methods.columnar_generator(col, row, width, height)

    # Make a numpy array    
    columnar_matrix_numpy =  numpy.array(columnar_matrix)

    # This line sets the threshold to NaN rather than 0 (flat grating)
    numpy.set_printoptions(threshold = numpy.nan)

    #print(columnar_matrix_numpy)

    # Making the .stl file
    fn = "default.stl"
    stl_tools.numpy2stl(columnar_matrix_numpy, fn, scale=1, mask_val = 1, force_python=True, square_corners=True)


if __name__ == '__main__':

    # Processing user input
    parser = argparse.ArgumentParser()
    parser.add_argument("no_columns", type = int, help = "Number of columns in total structure")
    parser.add_argument("no_rows", type = int, help = "Number of rows in total structure")
    parser.add_argument("slit_width", type = int, help = "Width of one slit")
    parser.add_argument("pitch", type = int, help = "Diffraction grating pitch")
    parser.add_argument("--strut_width", type = int, help = "Specifies slit width, defaults to 1 unit")
    parser.add_argument("--frame_boarder", type = int, help = "Specifies frame boarder width, defaults to 1 unit")
    parser.add_argument("--file_name", help = "Specifies output file name, defaults to 'default.stl'")
    args = parser.parse_args()

    create_grating(args.no_columns, args.no_rows, args.slit_width, args.pitch)
