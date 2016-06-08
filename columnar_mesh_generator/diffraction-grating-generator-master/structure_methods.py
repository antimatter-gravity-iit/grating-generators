#***
#*
#* Written by Melanie Cornelius (nee Dooley)
#* 
#* Licensed under GNU General Public License version 3, Copyright 2015
#*
#* These methods are the companions to diffraction_grating_maker.py and specify
#* the geometry made.
#*
#***

import stl_tools
import numpy
import math

def columnar_generator(rows, slit_count, slit_height, slit_width, frame_dim = 1, strut_height = 0, strut_width = 1):

    depth = 2

    if strut_height == 0:
        strut_height = slit_height

    factor = math.gcd(slit_height, math.gcd(slit_width, math.gcd(frame_dim, math.gcd(strut_height, strut_width))))

    slit_height //= factor
    slit_width //= factor
    frame_dim //= factor
    strut_height //= factor
    strut_width //= factor

    if slit_height == 1 or slit_width == 1 or frame_dim == 1 or strut_height == 1 or strut_width == 1:
        slit_height *= 2
        slit_width *= 2
        frame_dim *= 2
        strut_height *= 2
        strut_width *= 2


    structure_width = 2 * frame_dim + slit_width + ((slit_width + strut_width)*(slit_count - 1))
    structure_height = 2 * frame_dim + slit_height + ((strut_height + slit_height)*(rows - 1))

    row_solid = []
    row_grid = []

    # Making solid row

    for i in range(0, structure_width):
        row_solid.append(depth)

    # Making row with bars and spaces

    # First, print left edge
    for j in range(0, frame_dim):
        row_grid.append(depth)

    # Print first slit
    for j in range(0, slit_width):
        row_grid.append(0)

    # Print alternating struts and slits as many times as user specified
    for i in range(0, slit_count -1):
        for j in range(0, strut_width):
            row_grid.append(depth)
        for j in range(0, slit_width):
            row_grid.append(0)

    # Print final right edge
    for j in range(0, frame_dim):
        row_grid.append(depth)


    # Making matrix

    columnar_matrix = []
    
    # First, a solid row for the top
    for k in range(0, frame_dim): 
        columnar_matrix.append(row_solid)

    # Next, alternate bar-and-space rows with solid rows as user specified
    for k in range(0, rows - 1):
        for m in range(0, slit_height):
            columnar_matrix.append(row_grid)
        for n in range(0, strut_height):
            columnar_matrix.append(row_solid)

    for m in range(0, slit_height):
        columnar_matrix.append(row_grid)

    # Finally, append a final row for the bottom
    for k in range(0, frame_dim): 
        columnar_matrix.append(row_solid)

    #for row in columnar_matrix:
    #    print(row)

    # return the array
    return columnar_matrix
