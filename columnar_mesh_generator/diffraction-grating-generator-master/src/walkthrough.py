import diffraction_grating_maker

print("Diffraction Grating Generator\n")
no_cols = int(input("Number of columns: "))
no_rows = int(input("Number of rows: "))
pitch = int(input("Pitch: "))
width = int(input("Slit length: "))

print("\nWorking... \n")

diffraction_grating_maker.create_grating(no_cols, no_rows, width, pitch)

print("\nFinished. \n")
