# Copyright (C) 2024 Matthew Richardson

'''
The goal of this parser is to maintain interoperability with Biopython's parsing of PDB files while adding information within mol2 files to Biopython structure objects. Although the name of this class is 'mol2parser', it is a combination PDB parser and mol2parser. The private methods may be used to parse mol2 files individually, but this parser is not designed to be used this way.

'''

import numpy as np
import re
from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.Polypeptide import is_aa

class mol2parser:
    
    def __init__(self,pdbfile,mol2file=None):
        
        if mol2file is None:
            mol2file=pdbfile + '.mol2'

        try:
            self._parse_pdb(pdbfile)                # First parse the PDB file to get a structure object
            self._parse_mol2(mol2file)              # Parse corresponding mol2file to extract additional data about the protein
            self._update_records()                  # Add the mol2file data to the atom objects obtained from the PDB file

        except ParseError:
            print("Files were unable to be parsed")

    def _update_records(self):

        # Update the atom objects extracted from the PDB file with information from the corresponding mol2 file

        try:
            self._add_detailed_atom_type()
            self._add_atom_type()
            self._add_bond_info()
            self._add_atom_index()
        
        except ParseError:
            print("Unable to update atomic records from mol2 file")

    def _parse_pdb(self, file):

        # Call instance of Biopython PDB parser to get structure, residues, and atom objects
        
        pdb=PDBParser()
        self.structure=pdb.get_structure(file, file)
        
        self.atoms=[]
        self.residues=[]
        residueIndex=-1

        for residue in self.structure.get_residues():

            if is_aa(residue):

                self.residues.append(residue)
                residueIndex+=1

                for atom in residue.get_atoms():
                    atom.isAA=True
                    atom.residueIndex=residueIndex
                    self.atoms.append(atom)

            else:

                for atom in residue.get_atoms():
                    atom.isAA=False
                    atom.residueIndex=False
                    self.atoms.append(atom)

    def _parse_mol2(self, file):
        
        with open(file, 'r') as mol2file:
            
            sectionCounter=-1
            self.sections=[]
            self.parsedData=[]
            delimiter=re.compile(r'\s+')
            
            for line in mol2file:

                line=line.strip()
                
                if line.startswith('@<TRIPOS>'):
                    sectionCounter+=1
                    self.parsedData.append([line.removeprefix('@<TRIPOS>')])
                    sectionName=self.parsedData[sectionCounter][0]
                    self.sections.append([sectionName,sectionCounter])
            
                elif line:
                    line=delimiter.split(line)      
                    self.parsedData[sectionCounter].append(line)

            self.sections=dict(self.sections)
                            
                    
    def _get_atoms(self):

        return self.parsedData[self.sections['ATOM']][1:]

    def _get_bonds(self):

        return self.parsedData[self.sections['BOND']][1:]

    def _add_detailed_atom_type(self):
        
        mol2atoms=self._get_atoms()

        for i in range(len(self.atoms)):
            self.atoms[i].detailedAtomType=mol2atoms[i][5]

    def _add_atom_type(self):

        for i in range(len(self.atoms)):
            self.atoms[i].atomType=self.atoms[i].detailedAtomType[0]
        
    def _add_atom_index(self):

        for i in range(len(self.atoms)):
            self.atoms[i].mol2atomIndex=i
    
    def _add_bond_info(self):
        
        mol2bonds=self._get_bonds()

        for bond in mol2bonds:
            
            originID, targetID, bondType=int(bond[1]), int(bond[2]), bond[3]
            originIndex, targetIndex=originID-1, targetID-1

            # Sanity Check
            if not originID==self.atoms[originIndex].get_serial_number():
                raise ValueError("mol2 atom index does not match PDB index")

            # Test to see if the atom object already contains the bondData attribute
            if not hasattr(self.atoms[originIndex],'bondData'):
                self.atoms[originIndex].bondData=[]

            self.atoms[originIndex].bondData.append([targetIndex, bondType])

class ParseError(Exception):
    pass
