import numpy as np 
import random as rnd
from PIL import Image, ImageDraw  

class Ising_2d_sim():
    def __init__(self, grid_size, J, beta, B, init_spin_dens):
        # Creating simulation grid and initializing spins
        num_pos = int((grid_size ** 2) * 0.5 * (init_spin_dens + 1))
        init_pos = np.ones(num_pos, dtype=int)
        init_neg = -1 * np.ones(grid_size ** 2 - num_pos, dtype=int)
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

    def paint(self, img_size = (800, 800)):
        white_rgb = (255, 255, 255)
        black_rgb = (0, 0, 0)
        spin_col_dict = {
            -1: (255, 0, 0),
            1: (0, 0, 255)
        }
        image = Image.new("RGB", img_size, white_rgb)
        draw = ImageDraw.Draw(image)

        # Get canvas size that makes sense
        n = self.grid.shape[0]
        field_n = img_size[0] // n 
        pad_n = (img_size[0] - field_n * n) // 2 
        field_color_offset = field_n // 10

        # Draw image
        draw.rectangle([(pad_n, pad_n), (img_size[0] - pad_n, 
                        img_size[1] - pad_n)], fill=black_rgb) 
        for (row, col), field_spin in np.ndenumerate(self.grid):
            x1_pos = pad_n + col * field_n + field_color_offset 
            x2_pos = x1_pos + field_n - 2 * field_color_offset
            
            y1_pos = pad_n + row * field_n + field_color_offset
            y2_pos = y1_pos + field_n - 2 * field_color_offset

            field_col = spin_col_dict[field_spin]
            draw.rectangle([(x1_pos, y1_pos), (x2_pos, y2_pos)],
                           fill=field_col)
        return image  

    def get_magnetization(self):
        return self.grid.mean()    