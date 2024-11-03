import argparse 
from ising_sim import Ising_2d_sim


parser = argparse.ArgumentParser()
parser.add_argument('grid_size', type=int, help='Int n (grid size nxn).')
parser.add_argument('J', type=float, help='Float value of J.')
parser.add_argument('B', type=float, help='Float value of magnetic field B.')
parser.add_argument('beta', type=float, help='Float value of beta.')
parser.add_argument('num_of_steps', type=int, help='Number of  simulation\'s macro-steps.')
parser.add_argument('--spins_dens', '-sd', type=float, default=0.0,
                    help='Float in range (-1,1) of initial spins density.')
parser.add_argument('--pict_files', '-pf', type=str,
                    help='writes picture of n-th step to n+<file_name>.')
parser.add_argument('--anim_file', '-af', type=str,
                    help='writes animation to <file_name> file.')
parser.add_argument('--magnet_file', '-mf', type=str,
                    help='writes magnetization values to <file_name> file.')
args = parser.parse_args()

simulation = Ising_2d_sim(args.grid_size, args.J, args.beta, args.B,
                          args.spins_dens)

if type(args.magnet_file) == str:
    magnet_file = open(args.magnet_file, "w")

for i in range(args.num_of_steps):
    simulation.paint().save("test_pict_"+str(i)+".png")
    if type(args.magnet_file) == str:
        magnet_file.write(str(simulation.get_magnetization()) + "\n")
    simulation.perform_step() 

if type(args.magnet_file) == str:
    magnet_file.close()    