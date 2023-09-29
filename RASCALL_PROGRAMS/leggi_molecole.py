import subprocess
import os


def sanitize(string):
    return string.replace("/", "|")


fname = 'smiles.txt'

with open(fname) as infile:
    for mol in infile.readlines()[15020:]:
        print(mol[:-1])
        try:
            output = subprocess.check_output(['./rascall_plot', '--mol', f"{mol[:-1]}"])
        except subprocess.CalledProcessError:
            print(f"Functional group: {mol} gave error!")
            continue
        #----------------------
        sane_mol = sanitize(mol[:-1])
        #----------------------
        if b'has no functionals' in output:
            os.rename('/home/nicola/Desktop/Rascall_code/RASCALL/pippo.png', '/home/nicola/Desktop/Rascall_code/Exploration_figures_ONLY_NIST/' + sane_mol)

        elif b'not in any other databases' in output and b'with functionals' in output:
            os.rename('/home/nicola/Desktop/Rascall_code/RASCALL/pippo.png', '/home/nicola/Desktop/Rascall_code/Exploration_figures_NO_NIST/' + sane_mol)
        else:
            os.rename('/home/nicola/Desktop/Rascall_code/RASCALL/pippo.png', '/home/nicola/Desktop/Rascall_code/Exploration_figures_NIST_and_funcs/' + sane_mol)
