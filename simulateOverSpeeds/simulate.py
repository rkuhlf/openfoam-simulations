# I've decided that I actually just got lucky with the first nose cone, and it didn't actually work. I think I was using the wrong speed and reference values, so it just happened to be right. I need to test that again

# It's because the relative pressure is negative
# Should it really be
# Research what values of pRef make sense
# For some reason, the middle of the cone is causing negative drag, i.e. forward force
# Well it really didn't help that I had the wrong Aref value

# Maybe there is too much turbulence and it only gets worse as the speed goes up?
# If rasaero doesn't really simulate behind the nose cone since that is just where the rocket is, that would be an issue
# I don't know how jiggling the surface roughness would affect things
# Maybe it is total drag and rasaero is only pressure drag or viscous drag or friction drag or something
# I think that the best option is just to keep fiddling
# Try and figure out if there is a region where it is pretty close
# Maybe everythin has to be ico or picoFoam for CD sims
# calc in paraview

import numpy as np
import subprocess
import os
import shutil


target_path = "./results.csv"
# the forceCoeffs1 comes from the name in forceCoeffs dict
forceCoeffs = 'postProcessing/forceCoeffs1/0/'
forceCoeffsCalc = 'system/forceCoeffs'


# Eventually build in the capability to start from where it was left off last time
target = open(target_path, 'w')
target.write('speed,CD\n')


def cplusplus_format_vector(vector_tuple):
    ans = "("
    for val in vector_tuple:
        ans += str(val) + " "
        
    return ans + ")"




# Really need to be changing the reynolds number, but I need to figure out how to make that an input to openFoam. Oh wait actually you can't do that with simpleFoam because the air is incompressible
for speed in np.linspace(1, 3000, 20): # 20 sims
    # Change the speed (eventually this will be a nested for loop that also changes the angle)
    # Should only ever need two of these axes
    vel = (speed, 0, 0)
    
    initialConditions = '0/include/initialConditions'
    f = open(initialConditions, "r+")
    
    lines = f.readlines()
    # readlines moves it to the end
    f.seek(0)
    
    output = ""
    for line in lines:
        if line.startswith('flowVelocity'):
            output += 'flowVelocity    ' + cplusplus_format_vector(vel) + ";\n"
        else:
            output += line
            
    f.write(output)
    # Important in an application that will open and close the file multiple times
    f.close()
    

    f = open(forceCoeffsCalc, "r+")
    
    lines = f.readlines()
    f.seek(0)
    
    output = ""
    for line in lines:
        if line.strip().startswith('magUInf'):
            output += 'magUInf    ' + str(speed) + ";\n"
        else:
            output += line
            
    f.write(output)
    f.close()
    
    
    # Reset the drag coefficients folder so I can generate new ones
    shutil.rmtree(forceCoeffs, onerror=lambda a,b,c: print("Ignoring error in removing coeffs/0", a, b, c))
    
    
    # Run the simulation
    subprocess.call("simpleFoam")


    # Extract the drag coefficient as the average of the last 100 drag coefficients
    # Hopefully there should only be one file in here.
    num_files = len([name for name in os.listdir(forceCoeffs)])
    
    if num_files == 1:
        data = np.genfromtxt(os.path.join(forceCoeffs, 'forceCoeffs.dat'), delimiter='\t', skip_header=8, dtype=float)
    else:
        target.close()
        raise FileExistsError("There are more than one files/directories in " + forceCoeffs + ". This may be okay, but it could also indicate that the simulation is not outputting coefficients to the expected location.")
    
    
    num_to_average = 50
    # Hopefully there is always more than 50, should probably add some handling if there isn't
    coefficient_data = data[-num_to_average:, 2]
    average_CD = sum(coefficient_data) / num_to_average
    
    # This isn't really how you write to a CSV file, but since I only have one column idc
    target.write(str(speed) + "," + str(average_CD) + "\n")


    # Reset the simulation folder (delete all of the simulated frames other than 0
    # might have to say bash -c '<stuff>' but this might be better
    # subprocess('rm -r *00')
    for name in os.listdir('.'):
        if name.isnumeric():
            if not name == '0':
                shutil.rmtree(name)


target.close()



