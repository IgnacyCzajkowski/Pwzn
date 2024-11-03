import numpy as np 
import random as rnd

class Ising_2d_sim():
    def __init__(self, grid_size, J, beta, B, init_spin_dens):
        # Creating simulation grid and initializing spins
        num_pos = int((grid_size ** 2) * 0.5 * (init_spin_dens + 1))
        init_pos = np.ones(num_pos)
        init_neg = -1 * np.ones(grid_size ** 2 - num_pos)
        init_spins = np.concatenate((init_pos, init_neg))
        np.random.shuffle(init_spins)
        self.grid = init_spins.reshape((grid_size, grid_size))

        # Initializing simulation's constants
        self.J = J 
        self.beta = beta
        self.B = B  

    def perform_micro_step(self):
        # Chosing random spin
        index_x = rnd.randint(0, self.grid.shape[0] - 1)
        index_y = rnd.randint(0, self.grid.shape[1] - 1)
        index_spin = self.grid[index_x, index_y]

        # Calculating energy's difference
        mask_array = np.array([[0, 1, 0],
                               [1, 0, 1],
                               [0, 1, 0]])
        mask_array = index_spin * mask_array
        padded_grid = np.pad(self.grid, pad_width=1, mode='constant',
                             constant_values=0)
        padded_x = index_x + 1
        padded_y = index_y + 1
        index_neighb = padded_grid[padded_x-1 : padded_x+2,
                                   padded_y-1 : padded_y+2]
        E_part1 = np.sum(index_neighb * mask_array) 
        delta_E = 2 * (self.J * E_part1 + self.B * index_spin)
        
        # Deciding on switching the spin
        if delta_E < 0:
            self.grid[index_x, index_y] *= -1
        elif rnd.random() <= np.exp(-1 * self.beta * delta_E):
            self.grid[index_x, index_y] *= -1 

    def perform_step(self):
        for _ in range(self.grid.shape[0] * self.grid.shape[1]):
            self.perform_micro_step()