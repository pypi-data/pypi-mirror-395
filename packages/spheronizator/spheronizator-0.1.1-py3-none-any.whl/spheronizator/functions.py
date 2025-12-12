# Copyright (C) 2024 Matthew Richardson

import numpy as np
import math
from Bio.PDB.PDBParser import PDBParser
from Bio.PDB import vectors

def get_structureLimits(atomCoords):
    ''' 
    Get the upper and lower bounds for every dimension from the given set of coordinates.
    Used to get the ranges of cartesian coordiantes that describe the entire structure.
    
    Output array is in the following format:
            x y z
        min . . .
        max . . .
        
    '''
    
    structureLimits=np.array([
        [np.min(atomCoords[:,dimension]) for dimension in range(0,3)], 
        [np.max(atomCoords[:,dimension]) for dimension in range(0,3)]],
        dtype=np.float32
    )
    
    return structureLimits

def get_samplePoints(structureLimits,spacing=10):
    '''
    Given boundaries, generate a set of sample points spaced at regular intervals.
    Currently, we round to the nearest integer.
    
    Default spacing interval is 10 angstrom

    Output array is in the following format:

            x y z
    point 1 . . .
    point 2 . . .
    
    '''
    
    if not isinstance(spacing, int):
        raise ValueError("sampleRate is not a integer value!")

    # Round min and max to the nearest integer
    structureLimits[0]=np.floor(structureLimits[0])
    structureLimits[1]=np.ceil(structureLimits[1])
    
    # Generate an array of sample points for each dimension
    # Add one (1) to the end to include end-point
    x_points=np.arange(structureLimits[0,0],structureLimits[1,0]+1,spacing, dtype=int)
    y_points=np.arange(structureLimits[0,1],structureLimits[1,1]+1,spacing, dtype=int)
    z_points=np.arange(structureLimits[0,2],structureLimits[1,2]+1,spacing, dtype=int)

    # Verify ranges for debugging purposes
    if (x_points[-1]<structureLimits[1,0] or
        y_points[-1]<structureLimits[1,1] or
        z_points[-1]<structureLimits[1,2]):
        raise ValueError("One of the atoms is out of range!")

    '''
    Use numpy.meshgrid to generate the sample points.
    
    Equivalent to the following:
    
    samplePoints=[]
    for x in x_points
        for y in y_points
            for z in z_points
                samplePoints.append([x,y,z])
    '''
    
    x,y,z=np.meshgrid(x_points, y_points, z_points, indexing='ij')
    samplePoints=np.stack((x, y, z),axis=-1).reshape(-1,3)
    
    return samplePoints

def get_voxels(boxSize=20,spacing=1):

    '''
    Return a 3D array of regularly spaced sample points to serve as voxels for our model.

    '''
    
    if not isinstance(spacing, int):
        raise ValueError("spacing is not a integer value!")

    if not isinstance(boxSize, int):
        raise ValueError("boxSize is not a integer value!")

    if boxSize%2!=0:
        raise ValueError("boxSize is not divisible by 2!")

    delta=np.intc(boxSize>>1)
    
    x_points=np.arange(-delta, delta+spacing, spacing, dtype=int)
    y_points=np.arange(-delta, delta+spacing, spacing, dtype=int)
    z_points=np.arange(-delta, delta+spacing, spacing, dtype=int)

    x,y,z=np.meshgrid(x_points, y_points, z_points, indexing='ij')
    samplePoints=np.stack((x, y, z),axis=-1)

    return samplePoints

def get_floatVoxels(boxSize=20,spacing=1):

    '''
    Return a 3D array of regularly spaced sample points to serve as voxels for our model. Function is able to output voxels as floats,
    which enables the support of voxelSpacings less than 1. Supercedes above function, since calculations are all floating point anyways,
    and there is no performance loss.

    '''

    if not (np.isclose(np.mod(boxSize, spacing), 0, 1e-9) or
            np.isclose(np.mod(boxSize, spacing), spacing, 1e-9)):
        raise ValueError("spacing does not divide boxSize!")

    steps=np.rint(np.divide(boxSize, spacing) + 1).astype(int)
    delta=np.divide(boxSize, 2)
 
    x_points=np.linspace(-delta, delta, steps, endpoint=True)
    y_points=np.linspace(-delta, delta, steps, endpoint=True)
    z_points=np.linspace(-delta, delta, steps, endpoint=True)

    x,y,z=np.meshgrid(x_points, y_points, z_points, indexing='ij')
    samplePoints=np.stack((x, y, z),axis=-1)

    return samplePoints

def get_closestVoxel(point,voxels):

    '''
    Given a point and array of voxels, return the index of the voxel that lies closest to that point.

    '''
    # Compute the distance from every voxel to the specified point
    computedDistances=np.linalg.norm(voxels-point, axis=-1)

    # Find the smallest distance and return the 3D index of this point, not the flattened index
    minIndex=np.unravel_index(np.argmin(computedDistances), computedDistances.shape)

    return minIndex,voxels[minIndex]

def get_centralAA(samplePoints,atomCoords,boxSize=20):
    for sample in samplePoints:
        foundAtoms=buildBox(sample,atomCoords,boxSize)
        if len(foundAtoms)!=0:
            closestAtom=foundAtoms[0]
            x=np.subtract(atomCoords[closestAtom],sample)
            shortestDistance=np.dot(x,x)

            for atom in foundAtoms:
                x=np.subtract(atomCoords[atom],sample)
                d=np.dot(x,x) # We don't need the real distance, just d^2
                if d<shortestDistance:
                    shortestDistance=d
                    closestAtom=atom
    
def get_scanRange(origin,delta,size,voxel):
    scanRange=np.zeros((3,size),dtype=int)
    for dimension,component in enumerate(boxOrigin):
        # Add one (1) voxel to maximum to include endpoint
        scanMin,scanMax=component-delta,component+delta+voxel
        scanRange[dimension,:]=np.arange(scanMin,scanMax,voxel)
    return scanRange

def get_boxProjection(residue,atoms):
    '''
    Given a Biopython residue object to act as the center, and array of Biopython atom objects,
    return a new array of atom coordinates that have been projected onto a standard position.

    We may want to implement this as a matrix projection.
    
    Define new coordinate system as follows:
    Let N, CA, C be coplanar and parallel to the xy-plane.
    Let the vector i=N-CA be parallel to the x-axis.
    Then the vector k=ix(C-CA) is parallel to the z-axis,
    and the vector j=kxi is parallel to the y-axis.
    
    '''

    # Extract three vectors from the residue
    n=residue["N"].get_vector()
    ca=residue["CA"].get_vector()
    c=residue["C"].get_vector()

    # Create two vectors, i and v, in the xy-plane with the alpha carbon as the origin.
    i=n-ca
    v=c-ca
    
    # Create vector in the direction of the z-axis
    k=i**v # Cross Product

    # Create vector in the direction of the y-axis
    j=k**i

    # Make each a unit vector. This saves us from having to recompute later
    i=i/np.linalg.norm(i)
    j=j/np.linalg.norm(j)
    k=k/np.linalg.norm(k)

    # Sanity-check: See that i,j,k are orthagonal to each other
    if not (math.isclose(i*j, 0, abs_tol=1e-6) or
            math.isclose(i*k, 0, abs_tol=1e-6) or
            math.isclose(j*k, 0, abs_tol=1e-6)):
            raise ValueError("Something is wrong with our imposed coordinate system!")

    projectedCoordinates=[]
    for atom in atoms:
        u=atom.get_vector()-ca
        x,y,z=i*u,j*u,k*u # Dot product
        projection=np.array([x, y, z])

        # Sanity-check: distances to central atom should be the same in both coordinate systems
        if not math.isclose(np.linalg.norm(u),np.linalg.norm(projection), abs_tol=1e-6):
            raise ValueError("Something is wrong with our imposed coordinate system!")

        projectedCoordinates.append(projection)
        
    return projectedCoordinates

def buildBox(atomCoords, boxSize=20):

    delta=np.divide(boxSize, 2)
    boxOrigin=(0,0,0)

    # Get our scanning range for the algorithm from the origin point
    # We want to avoid recomputing this range every iteration because it is constant
    scanMin=[component-delta for component in boxOrigin]
    scanMax=[component+delta+1 for component in boxOrigin] # Add 1 to include endpoint

    foundAtoms=[]
    for index,atom in enumerate(atomCoords):
        if np.array_equal(atom,boxOrigin):
            continue # Exclude the central atom from atoms to search
        for dimension,component in enumerate(atom[:3]):
            if (component-scanMin[dimension])*(component-scanMax[dimension]) > 0:
                break # One dimension was out of range, so no need to check the rest
        else:
            # We have found an atom that is within the box
            foundAtoms.append(index)

    return foundAtoms

def buildSphere(atomCoords, boxSize=20):
    
    radius=np.divide(boxSize, 2)
    computedDistances=np.linalg.norm(atomCoords, axis=-1)
    foundAtomIndices=np.where(computedDistances <= radius)[0]
    
    return foundAtomIndices
            
