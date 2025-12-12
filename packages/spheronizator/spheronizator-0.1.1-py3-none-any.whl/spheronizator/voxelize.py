#! /bin/env python

import argparse
import os
import numpy as np
from collections import defaultdict
import warnings
from spheronizator import voxelBuilder
import subprocess

warnings.filterwarnings('ignore', message='.*unrecognized record \'END\'.*')
warnings.filterwarnings('ignore', message='.*Used element.*')

def pdb_to_mol2(pdb_file):
    mol2_file = pdb_file + ".mol2"
    # Use obabel command line to convert PDB to MOL2
    # -O specifies output file, -p disables protonation if not needed
    try:
        subprocess.run(
            ["obabel", pdb_file, "-O", mol2_file, "-p"], 
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"Converted {pdb_file} to {mol2_file} using Open Babel.")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e.stderr.decode()}")
        raise RuntimeError("Open Babel failed to convert PDB to MOL2.")
    return mol2_file


allowed_res = [
    "ALA", "ARG", "ASN", "ASP", "CYS", "GLU", "GLN", "GLY", "HIS",
    "ILE", "LEU", "LYS", "MET", "PHE", "PRO", "SER", "THR", "TRP",
    "TYR", "VAL"
]

# Default voxelizer parameters
DEFAULT_VS = 0.5
DEFAULT_FV = True
DEFAULT_BS = 20
DEFAULT_US = True
DEFAULT_DT = 'float16'

overwrite = False

# Default output directories                                                                                         

DEFAULT_ATOM_OUT_PATH = "./output_vox_atoms"
DEFAULT_BOND_OUT_PATH = "./output_vox_bonds"
DEFAULT_META_OUT_PATH = "./metadata"

# Initialize with defaults (will be overridden by CLI if provided)
atom_out_path = DEFAULT_ATOM_OUT_PATH
bond_out_path = DEFAULT_BOND_OUT_PATH
meta_out_path = DEFAULT_META_OUT_PATH

os.makedirs(atom_out_path, exist_ok=True)
os.makedirs(bond_out_path, exist_ok=True)
os.makedirs(meta_out_path, exist_ok=True)
    
def extract_boxes(
    pdb_file_path,
    voxel_spacing=DEFAULT_VS,
    use_float_voxels=DEFAULT_FV,
    box_size=DEFAULT_BS,
    use_spheres=DEFAULT_US,
    data_type=DEFAULT_DT,
    overwrite_existing=overwrite,
    atom_dir=atom_out_path,
    bond_dir=bond_out_path,
    meta_dir=meta_out_path,
):
    file_name = os.path.basename(pdb_file_path)
    out_name = file_name.replace('.pdb', '.npy')
    out_name_meta = file_name.replace('.pdb', '.txt')

    # ensure directories exist
    os.makedirs(atom_dir, exist_ok=True)
    os.makedirs(bond_dir, exist_ok=True)
    os.makedirs(meta_dir, exist_ok=True)

    x = voxelBuilder("config")
    x.voxelSpacing = voxel_spacing
    x.useFloatVoxels = use_float_voxels
    x.boxSize = box_size
    x.useSpheres = use_spheres
    x.dataType = data_type

    mol2_file = pdb_to_mol2(pdb_file_path)

    x.parse(pdb_file_path, mol2_file)
    n_res = len([res for res in x.residues if res.get_resname() in allowed_res])
    print(f"Number of residues: {n_res}")
    print(f"Extracting voxel boxes/spheres for {pdb_file_path}", flush=True)

    sampled_indices = [i for i, res in enumerate(x.residues) if res.get_resname() in allowed_res]

    x.buildData()

    output_atoms = x.output[sampled_indices]
    output_bonds = x.outputBonds[sampled_indices]

    central_res = output_atoms[:, :, :, :, :, 1]
    output_atoms_masked = output_atoms

    np.save(os.path.join(atom_dir, out_name), output_atoms_masked)
    np.save(os.path.join(bond_dir, out_name), output_bonds)

    print(f"{len(x.output)} voxel boxes/spheres processed, {n_res} residues total.")

    with open(os.path.join(meta_dir, out_name_meta), 'w') as output:
        output.write('FILE_NAME\tBOX_INDEX\tRES_INDEX\tRES_LABEL\n')
        for i, res_idx in enumerate(sampled_indices):
            output.write(f"{file_name}\t{i + 1}\t{res_idx + 1}\t{x.residues[res_idx].get_resname()}\n")
def main():
    parser = argparse.ArgumentParser(description="Extract voxel boxes/spheres from a protein PDB file")
    parser.add_argument("pdb_file", type=str, help="Protein PDB file to process")
    parser.add_argument("--voxel_spacing", type=float, default=DEFAULT_VS, help="Voxel spacing (default: 0.5)")
    parser.add_argument("--use_float_voxels", type=bool, default=DEFAULT_FV, help="Use float voxels (default: True)")
    parser.add_argument("--box_size", type=int, default=DEFAULT_BS, help="Box size (default: 20)")
    parser.add_argument("--use_spheres", type=bool, default=DEFAULT_US, help="Use spheres (default: True)")
    parser.add_argument("--data_type", type=str, default=DEFAULT_DT, help="Data type (default: float16)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing outputs if present")

    # new: output directory arguments
    parser.add_argument("--atom_out_dir", type=str, default=DEFAULT_ATOM_OUT_PATH,
                        help="Directory for atom voxel outputs (default: ./output_vox_atoms)")
    parser.add_argument("--bond_out_dir", type=str, default=DEFAULT_BOND_OUT_PATH,
                        help="Directory for bond voxel outputs (default: ./output_vox_bonds)")
    parser.add_argument("--meta_out_dir", type=str, default=DEFAULT_META_OUT_PATH,
                        help="Directory for metadata outputs (default: ./metadata)")

    args = parser.parse_args()

    
    extract_boxes(
        args.pdb_file,
        voxel_spacing=args.voxel_spacing,
        use_float_voxels=args.use_float_voxels,
        box_size=args.box_size,
        use_spheres=args.use_spheres,
        data_type=args.data_type,
        overwrite_existing=args.overwrite,
        atom_dir=args.atom_out_dir,
        bond_dir=args.bond_out_dir,
        meta_dir=args.meta_out_dir,
    )


if __name__ == "__main__":
    main()
