# Copyright (C) 2024 Matthew Richardson

from spheronizator import functions as box
from spheronizator.mol2parser import mol2parser
import numpy as np
import re
import warnings

class voxelBuilder:

    def __init__(self, config=None):
        
        # Load configuration file
        self._get_config(config)

        # Attribute bondTypeDict determines the indexing of the output array in addition to the types of bonds that will be present in the output. Strings must match what is present in the associated mol2 file.
        self.bondTypeDict={
                '1':0,      # Single bonds
                '2':1,      # Double bonds
                '3':2,      # Triple bonds
                'am':3,     # Amides
                'ar':4      # Aromatics
                }

        # Attribute atomTypeDict determines the indexing of the output array in addition to the types of atoms that will be present in the output. Strings must match what is present in the first character of the associated mol2 file atom type. 
        self.atomTypeDict={
                'H':0,
                'C':1,
                'N':2,
                'O':3,
                'P':4,
                'S':5
                }

    def reloadConfig(self, configPath=None):
        
        self._get_config(configPath)

    def parse(self, pdbfile, mol2file=None):

        # Wrapper method for mol2parser class. This simplifies the interface.

        parser=mol2parser(pdbfile, mol2file)    # Create instance of parser object, parse and update atom objects
        self.structure=parser.structure
        self.residues=parser.residues

        # Only get atoms that belong to amino acids
        self.atoms=[atom for atom in parser.atoms if atom.isAA]

        self._get_resnames()
    
    def buildData(self):
        
        self._get_voxels()                      # Generate our voxels we will need for each box and store as object attribute
        self._init_arrays()                     # Initialize all arrays we will need for output data

        # Sanity check
        if self.voxels.shape[0:3]!=self.output.shape[1:4]:
            raise ValueError("Voxel array shape and output array shape do not match! File a bug report.")

        
        for i in range(len(self.residues)):
    
            # Build data for atom abscence / presence
            foundAtomIndices, projectedCoords=self._build_box(self.residues[i])
            self._process_box(foundAtomIndices, projectedCoords, i)

            # Build data for bond information
            self._process_box_bonds(foundAtomIndices, i)
               
    def check_collision(self):

        return np.any(self.output > 1)

    def find_collisions(self):

        return np.transpose(np.where(self.output > 1))
    
    def _get_config(self, configPath=None):

        if configPath is None:
            configPath='config'

        try:
           with open(configPath, 'r') as configFile:
                
                config=[]
                delimiter=re.compile(r'=')

                for line in configFile:
                    
                    line=line.strip()

                    if line and not line.startswith('#'):
                        config.append(delimiter.split(line))
                
                
                self.config=dict(config)

        except:

            self.config={
                        'boxSize':20,
                        'voxelSpacing':1,
                        'useFloatVoxels':'True',
                        'dataType':'bool',
                        'useWarnings':'True',
                        'useSpheres':'False'
                    }

        # Unpack values to attributes. This allows this values to be changed after initialization.
        self.boxSize            = int(  self.config['boxSize'])
        self.voxelSpacing       = int(  self.config['voxelSpacing'])
        self.useFloatVoxels     =       self.config['useFloatVoxels'].startswith('True')
        self.dataType           =       self.config['dataType']
        self.useWarnings        =       self.config['useWarnings'].startswith('True')
        self.useSpheres         =       self.config['useSpheres'].startswith('True')
    
    def _init_arrays(self):
        
        voxelArrayLength=np.rint(np.divide(self.boxSize, self.voxelSpacing) + 1).astype(int)
        residueCount=len(self.residues)

        # Output array for atom presence / abscence
        self.output=np.zeros((
                residueCount,                   # Number of residues in protein
                voxelArrayLength,               # Size of voxel array
                voxelArrayLength,
                voxelArrayLength,
                len(self.atomTypeDict),         # Size of atomTypeDict representing the count of atom channels
                2                               # Last dimension indicates whether or not atom belongs to the parent residue of the box
                ), dtype=self.dataType)

        self.outputBonds=np.zeros((
                residueCount,
                len(self.bondTypeDict)          # Size of bondTypeDict representing the count of different types of bonds to be considered
                ), dtype=int)
    
    def _get_resnames(self):

        self.resnames=[residue.get_resname() for residue in self.residues]
    
    def _build_box(self, residue):

        # Obtain coordinate projection of all atom objects about a standard position based on the parent residue
        projectedAtoms=box.get_boxProjection(residue, self.atoms)

        # Get the indices of all atoms contained within the box
        if self.useSpheres:
            foundAtomIndices=box.buildSphere(projectedAtoms, self.boxSize)
        else:
            foundAtomIndices=box.buildBox(projectedAtoms, self.boxSize)

        return foundAtomIndices, projectedAtoms
                
    def _get_voxels(self):

        # Generate voxels and store as attribute.  Voxels are not unique to each box, so they only need to be generated once.
        if self.useFloatVoxels:
            self.voxels=box.get_floatVoxels(self.boxSize, self.voxelSpacing)

        else:
            self.voxels=box.get_voxels(self.boxSize, self.voxelSpacing)

    def _process_box(self, foundAtomIndices, projectedCoords, residueIndex):  

        for i in foundAtomIndices:
            
            atom=self.atoms[i]
             
            try:
                atomTypeIndex=self.atomTypeDict[atom.atomType]
            except:
                continue
 
            voxelIndex, voxelCoords=box.get_closestVoxel(projectedCoords[i], self.voxels)

            if self.useWarnings and self.output[residueIndex][voxelIndex][atomTypeIndex][0]:
                voxelStr=str(voxelIndex).strip(r"()")
                print(f"Warning: Atom collision at index ({residueIndex}, {voxelStr}, {atomTypeIndex}) by atom with index {i}.")
            
            self.output[residueIndex][voxelIndex][atomTypeIndex][0]+=1

            if atom.isAA and atom.residueIndex==residueIndex:
                self.output[residueIndex][voxelIndex][atomTypeIndex][1]+=1

    def _process_box_bonds(self, foundAtomIndices, residueIndex):
        
        mol2indices=[self.atoms[i].mol2atomIndex for i in foundAtomIndices]
        
        for i in foundAtomIndices:
            
            atom=self.atoms[i]

            if hasattr(atom, 'bondData'):
                for bond in atom.bondData:
                    if bond[0] in mol2indices:
                        try:
                            bondIndex=self.bondTypeDict[bond[1]]

                        except:
                            continue

                        self.outputBonds[residueIndex][bondIndex]+=1

    
    def _debug_export_boxes(self):

       # This function is used to export generated boxes into a directory as PDB files themselves for testing/debugging purposes. 
        
        from Bio.PDB.PDBIO import Select
        from Bio.PDB import PDBIO

        io=PDBIO()
        
        class boxSelect(Select):
            def accept_atom(self, atom):
                if atom in foundAtoms:
                    return True
                else:
                    return False

        for index,residue in enumerate(self.residues):

            foundAtomsIndex, projectedCoords=self._build_box(residue)
            foundAtoms=[self.atoms[i] for i in foundAtomsIndex]
            filename_out="output/box" + str(index+1) + ".pdb"
            io.set_structure(self.structure)
            io.save(filename_out,boxSelect())
            print(filename_out)

