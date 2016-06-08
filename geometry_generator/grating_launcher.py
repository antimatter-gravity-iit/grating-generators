import geometry_generator
import math

print("\n***************IPRO-204 Antimatter Interferometer***************")
print("*********This program generates two-dimensional geometry********")
print("***********of grating structure in a form of STEP file**********")
print("**********************Written by Soowon Kim*********************")
print("\nunits are micron\n")

slit_l = input("Slit length: ")
slit_h = input("Slit height: ")
slit_p = input("Slit vertical gap: ")
strut_w = input("Strut width: ")
num_col = input("Number of columns: ")
row_square = int(math.floor(((slit_l + strut_w) * num_col + slit_p - strut_w)/(slit_h + slit_p)))
print "If you want to make square, then use",row_square,"for the Number of rows\n"
num_row = input("Number of rows: ")
fillet = input("fillet intensity (0 to 1): ")
col_or_ash = input("Columnar (1) Ashlar (2) Pseudo (3): ")

print("\nWorking...\n")

geometry_generator.create_grating(slit_l,slit_h,slit_p,strut_w,num_col,num_row,fillet,col_or_ash)

print("\nFinished!")
print("\nFile directory: <C:/Users/Soowon Kim/Desktop/grating.step>\n")
