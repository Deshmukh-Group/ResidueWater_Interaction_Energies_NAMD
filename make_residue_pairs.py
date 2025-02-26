import MDAnalysis as mda

# Define input and output file names
pdb_file = "NAMD_input.pdb"
output_file = "residue_pairs.dat"

# Load PDB file using MDAnalysis
u = mda.Universe(pdb_file)

# Select only protein residues (excluding water, ions, etc.)
protein_residues = sorted(set(residue.resid for residue in u.select_atoms("protein").residues))

# Write to residue_pairs.dat
with open(output_file, "w") as file:
    for resid in protein_residues:
        file.write(f"{resid},TIP3\n")

print(f"Generated {output_file} with {len(protein_residues)} residue pairs.")
