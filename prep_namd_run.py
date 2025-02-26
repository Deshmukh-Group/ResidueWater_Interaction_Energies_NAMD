import sys

def modify_beta_column(pdb_file, res1, output_pdb):
    """
    Modify the beta column in the PDB file for two residues and save to a new PDB file.
    """
    with open(pdb_file, 'r') as f_in, open(output_pdb, 'w') as f_out:
        for line in f_in:
            if line.startswith(('ATOM', 'HETATM')):
                res_num = int(line[22:26].strip())
                res_name = line[17:20].strip()
                if res_num == res1 and res_name !='SOD':
                    new_line = line[:60] + '  1.00' + line[66:]
                elif res_name == 'TIP':
                    new_line = line[:60] + '  2.00' + line[66:]
                else:
                    new_line = line
                f_out.write(new_line)
            else:
                f_out.write(line)

def generate_namd_config(res1, dcd_file):
    """
    Generate a NAMD configuration script based on the provided PDB and parameters.
    """
    namd_script = f"""
structure ./NAMD_input.psf
paraTypeCharmm on
parameters          ./par_all36m_prot.prm
parameters          ./par_all36_na.prm
parameters          ./par_all36_carb.prm
parameters          ./par_all36_lipid.prm
parameters          ./par_all36_cgenff.prm
parameters          ./toppar_water_ions.str
numsteps 1
switching off
exclude scaled1-4
outputname {res1}-temp
temperature 0
COMmotion yes
cutoff 12
dielectric 1
switchdist 10.0
pairInteraction on
pairInteractionGroup1 1
pairInteractionFile ./{res1}-temp.pdb
pairInteractionGroup2 2
coordinates ./{res1}-temp.pdb
set ts 0
coorfile open dcd ./{dcd_file}
while {{ ![coorfile read] }} {{
    firstTimeStep $ts
    run 0
    incr ts 1
}}
coorfile close
"""
    # Save the NAMD script to a file
    namd_filename = f"{res1}-temp.namd"
    with open(namd_filename, 'w') as f:
        f.write(namd_script)

    print(f"NAMD configuration saved to {namd_filename}")

if __name__ == "__main__":
    # Define the input PDB file, DCD file, residues, and output file name
    pdb_file = sys.argv[1]
    dcd_file = sys.argv[2]
    res1 = int(sys.argv[3])

    output_file = f'{res1}-temp.pdb'

    # Call the function to modify the beta column and write the new file
    modify_beta_column(pdb_file, res1, output_file)

    # Generate the NAMD configuration file
    generate_namd_config(res1, dcd_file)

    print(f"File '{output_file}' created with beta values updated for residues {res1} and TIP3.")
    
