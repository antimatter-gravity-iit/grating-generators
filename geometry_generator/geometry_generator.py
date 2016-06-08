import sys

# Add path to system #
FREECADPATH="C:\\Program Files\\FreeCAD 0.15\\bin"
sys.path.append(FREECADPATH)

import FreeCAD
import FreeCADGui
import Import
import Draft
import math
import random
from Draft import *

def cut_soowon(object1,object2):
    '''cut(oject1,object2): returns a cut object made from
    the difference of the 2 given objects.'''
    obj = FreeCAD.ActiveDocument.addObject("Part::Cut","Cut")
    obj.Base = object1
    obj.Tool = object2
    #object1.ViewObject.Visibility = False
    #object2.ViewObject.Visibility = False
    formatObject(obj,object1)
    FreeCAD.ActiveDocument.recompute()
    return obj


def create_grating(slit_l,slit_h,slit_p,strut_w,num_col,num_row,fillet,col_or_ash):
    # Input Dimensions #
    strut_h = slit_h
    film_mrgn = strut_w*10
    film_w = (slit_l + strut_w)*num_col-strut_w+2*film_mrgn
    film_h = (slit_h + slit_p)*num_row-strut_h+2*film_mrgn
    
    # Create new document #
    doc = FreeCAD.newDocument("myDoc")
    
    # Create Film #
    film = Draft.makeRectangle(film_w,film_h)
    film.Label = 'myFilm'
    move_film = FreeCAD.Vector(-film_mrgn,-film_mrgn,0)
    Draft.move(film,move_film)
    
    # Create single slit #
    slit = Draft.makeRectangle(slit_l,slit_h)
    slit.Label = 'mySlit'
    long_slit = (slit_l+strut_w)*num_col-strut_w
    
    # Fillet #
    slit.FilletRadius = slit_h/2.01*fillet
        
    if col_or_ash == 1:
        '''COLUMNAR FORM'''
        # Slit Matrix #
        array = Draft.makeArray(slit,FreeCAD.Vector(slit_l+strut_w,0,0),\
                                FreeCAD.Vector(0,slit_h+slit_p,0),num_col,num_row)
        grating = cut_soowon(film,array)
        
    elif col_or_ash == 2:
        '''ASHLAR FORM'''
        # Slit Matrix #
        row_arr1 = int(math.ceil(num_row/2.))
        row_arr2 = int(math.floor(num_row/2.))
        
        array1 = Draft.makeArray(slit,FreeCAD.Vector(slit_l+strut_w,0,0),\
                                 FreeCAD.Vector(0,2*(slit_h+slit_p),0),num_col,row_arr1)
        array2 = Draft.makeArray(slit,FreeCAD.Vector(slit_l+strut_w,0,0),\
                                 FreeCAD.Vector(0,2*(slit_h+slit_p),0),num_col-1,row_arr2)
        #edge_l = (slit_l-strut_w)/2
        #edge = Draft.makeRectangle(edge_l,slit_h)
        #edge.FilletRadius = slit_h/2.01*fillet
        #edge_array = Draft.makeArray(edge,FreeCAD.Vector(long_slit-edge_l,0,0),\
        #                             FreeCAD.Vector(0,2*(slit_h+slit_p),0),2,row_arr2)
        
        move_array2 = FreeCAD.Vector((slit_l+strut_w)/2,slit_h+slit_p,0)
        #move_edge_array = FreeCAD.Vector(0,slit_h+slit_p,0)
        Draft.move(array2,move_array2)
        #Draft.move(edge_array,move_edge_array)

        step1 = cut_soowon(film,array1)
        grating = cut_soowon(step1,array2)
        #step2 = cut_soowon(step1,array2)
        #grating = cut_soowon(step2,edge_array)

    elif col_or_ash == 3:
        num_strut = num_col - 1
        grating = film
        for x in xrange(1,num_row+1):
            
            pseudo_strut = random.randint(num_strut-int(math.ceil(num_strut/2.)),\
                                          num_strut+int(math.ceil(num_strut/2.)))
            new_slit_l = (long_slit- pseudo_strut*strut_w)/(pseudo_strut+1)
            new_slit = Draft.makeRectangle(new_slit_l,slit_h)
            new_slit.FilletRadius = slit_h/2.01*fillet

            move_new_slit = FreeCAD.Vector(0,(x-1)*(slit_h+slit_p),0)
            Draft.move(new_slit,move_new_slit)
            array = Draft.makeArray(new_slit,FreeCAD.Vector(new_slit_l+strut_w,0,0), \
                                             FreeCAD.Vector(0,slit_h+slit_p,0),(pseudo_strut+1),1)
            grating = cut_soowon(grating,array)

    elif col_or_ash == 4:
        '''This function randomize the starting point of the strut on columnar form but maintaining
        strut density'''
        sigma = 0.01 #Standard Deviation: 10 nm #
        for x in xrange(1,num_row+1):
            first_slit_l = random.gauss(slit_l, sigma)
            if first_slit_l < slit_l:
                last_slit_l = slit_l - first_slit_l
            else:
                last_slit_l = 2*slit_l - first_slit_l
                first_slit_l = first_slit_l - slit_l

            first_slit = Draft.makeRectangle(first_slit_l,slit_h)

            move_first = FreeCAD.Vector(0, (x-1)*(slit_h+slit_p) ,0)

            Draft.move(first_slit,move_first)
            
            middle_array = Draft.makeArray(slit,FreeCAD.Vector(slit_l+strut_w,0,0),\
                                 FreeCAD.Vector(0,1,0),num_col-1,1)

            move_middle = FreeCAD.Vector(first_slit_l+strut_w,(x-1)*(slit_h+slit_p),0)

            Draft.move(middle_array,move_middle)

            last_slit = Draft.makeRectangle(last_slit_l,slit_h)

            move_last = FreeCAD.Vector(first_slit_l+(strut_w+slit_l)*(num_col-1)+strut_w,\
                                       (x-1)*(slit_h+slit_p),0)

            Draft.move(last_slit,move_last)
            film = cut_soowon(film,first_slit)
            film = cut_soowon(film,middle_array)
            film = cut_soowon(film,last_slit)
        grating = film

    elif col_or_ash == 5:
        '''RANDOMIZED ASHLAR'''
        sigma = 0.01 #Standard Deviation: 10 nm #
        num_arr1 = int(math.ceil(num_row/2.))
        num_arr2 = num_row - num_arr1

        for x in xrange(1,num_arr1+1):
#            first_slit_l = random.uniform(slit_l-2*strut_w , slit_l+2*strut_w)
#            (long_slit - first_slit_l)
#            if first_slit_l < slit_l:
#                last_slit_l = slit_l - first_slit_l
#            else:
#                last_slit_l = 2*slit_l - first_slit_l
#                first_slit_l = first_slit_l - slit_l

#            first_slit = Draft.makeRectangle(first_slit_l,slit_h)

#            move_first = FreeCAD.Vector(0, (x-1)*2*(slit_h+slit_p) ,0)

#            Draft.move(first_slit,move_first)


            rand_start = random.uniform(-strut_w , strut_w)
            
            array = Draft.makeArray(slit,FreeCAD.Vector(slit_l+strut_w,0,0),\
                                FreeCAD.Vector(0,1,0),num_col,1)
            move_array = FreeCAD.Vector(rand_start,(x-1)*2*(slit_h+slit_p),0)
            Draft.move(array,move_array)
            film = cut_soowon(film,array)
            
#            middle_array = Draft.makeArray(slit,FreeCAD.Vector(slit_l+strut_w,0,0),\
#                                 FreeCAD.Vector(0,1,0),num_col-1,1)

#            middle = FreeCAD.Vector(0,(x-1)*2*(slit_h+slit_p),0)
#            move_middle = FreeCAD.Vector(first_slit_l+strut_w,(x-1)*2*(slit_h+slit_p),0)

#            Draft.move(middle_array,move_middle)

#            last_slit = Draft.makeRectangle(last_slit_l,slit_h)

#            move_last = FreeCAD.Vector(first_slit_l+(strut_w+slit_l)*(num_col-1)+strut_w,\
#                                       (x-1)*2*(slit_h+slit_p),0)

#            Draft.move(last_slit,move_last)
#            film = cut_soowon(film,first_slit)
#            film = cut_soowon(film,middle_array)
#            film = cut_soowon(film,last_slit)
            
            
        for x in xrange(1,num_arr2+1):
            '''edge_l = (slit_l-strut_w)/2
            
            first_slit_l = random.uniform(edge_l-2*strut_w, edge_l+2*strut_w)
            first_slit = Draft.makeRectangle(first_slit_l,slit_h)
            move_first = FreeCAD.Vector(0, (2*x-1)*(slit_h+slit_p) ,0) # move slit to the 2nd layer. Then, move up to every other layer.
            Draft.move(first_slit,move_first)
            
            middle_array = Draft.makeArray(slit,FreeCAD.Vector(slit_l+strut_w,0,0),\
                                 FreeCAD.Vector(0,1,0),num_col-1,1) # Number of slit is going to be one less then the number of column.
            move_middle = FreeCAD.Vector(first_slit_l+strut_w,(2*x-1)*(slit_h+slit_p),0)
            Draft.move(middle_array,move_middle)

            last_slit_l = slit_l - strut_w - first_slit_l
            last_slit = Draft.makeRectangle(last_slit_l,slit_h)
            move_last = FreeCAD.Vector(first_slit_l+(strut_w+slit_l)*(num_col-1)+strut_w,\
                                       (2*x-1)*(slit_h+slit_p),0)
            Draft.move(last_slit,move_last)
            film = cut_soowon(film,first_slit)
            film = cut_soowon(film,middle_array)
            film = cut_soowon(film,last_slit)'''
            rand_start = random.uniform(-strut_w , strut_w)
            
            array = Draft.makeArray(slit,FreeCAD.Vector(slit_l+strut_w,0,0),\
                                FreeCAD.Vector(0,1,0),num_col-1,1)
            move_array = FreeCAD.Vector(rand_start+(slit_l+strut_w)/2,(2*x-1)*(slit_h+slit_p),0)
            Draft.move(array,move_array)
            film = cut_soowon(film,array)
        grating = film

    # Generate geometry #
    FreeCAD.ActiveDocument.recompute()
    
    # Export #
    __objs__=[]
    __objs__.append(grating)
    Import.export(__objs__,"C:/Users/Soowon Kim/Desktop/grating.step")
    del __objs__
