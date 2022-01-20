import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation 

class PSO_Optimizer():
	"""
			This is a generic function optimizer by using the
		particle swarm algorithm.
			Inputs: 
				'func': the function to be optimized
				'n_dimensions': the number of variables in func
				'n_particles': the number of particles used
	"""
	def __init__(self, n_dimensions, n_particles = 100):
		self.n_dimensions = n_dimensions;
		self.n_particles = n_particles;
		self.particles = np.zeros([n_particles, (3 * n_dimensions + 1)]);

	def initialize(self, init_width = [1.0], init_shift = [0.0]):
		"""
				Initialize:
					1. the particles' positions 
					2. the particles' velocities,
					3. the best positions of all particle in the 
					   history 
					4. the best (smallest) function values of all 
					   particles in the history
				Inputs: 
					'init_width': a list containing values
					'init_shift': a list containing values
					The initial positions are randomly generated.
					'init_width' specifies the width of the position
				distribution and 'init_shift' specifies the shift of 
				the distribution center. Ideally 'init_width' and
				'init_shift' should have the same length equal to
				'n_dimensions'. If their length are smaller than
				'n_dimensions', only the first 'len(init_width)' 
				dimensions will be initialized accordingly and the 
				rest will be initialized as zero. If their length are 
				greater than 'n_dimensions', only the first 'n_dimensions'
				entries will be used for the initialization.
					the best (smallest) function values of all 
				particles in the history will be initialized as a big
				value (1e10) and all the other quantities will be 
				initialized as zero.
		"""
		assert len(init_width)==len(init_shift), "'init_width' and 'init_shift' must have the same length!"

		if len(init_width) >=  self.n_dimensions:
			for i in range(self.n_dimensions):
				self.particles[:, i] = ((np.random.rand(1, self.n_particles) - 0.5) * init_width[i]) + init_shift[i]
		else:
			for i in range(len(init_width)):
				self.particles[:, i] = ((np.random.rand(1, self.n_particles) - 0.5) * init_width[i]) + init_shift[i]
			for i in range(len(init_width), self.n_dimensions, 1):
				self.particles[:, i] = ((np.random.rand(1, self.n_particles) - 0.5) + 0.0)
		for i in range(self.n_dimensions):
			self.particles[:, i + self.n_dimensions] = ((np.random.rand(1, self.n_particles) - 0.5) + 0.0)
		self.particles[:, 2 * self.n_dimensions:3 * self.n_dimensions] = 0.0
		self.particles[:, -1] = 1e10

	def optimize(self, func, inertia = 1.0, correction_factor = 2.0, n_iterations = 100, if_display = True):
		"""
				Update the quantities according to the PSO updating
			rules.
				Inputs: 
					1. 'inertia': a PSO parameter
					2. 'correction_factor': a PSO parameter
					3. 'n_iterations': the number of iterations
				Outputs:
					a list in the form of [[...], ...], where the first
				entry is a sublist of length 'n_dimensions' containing 
				the optimized values for all variables and the second 
				entry is the optimized (smallest) value of the function
				that the optimizer found. 
		"""
		results = np.zeros([self.n_particles, self.n_dimensions])
		for i_iter in range(n_iterations):
			"""Update the positions of particles"""
			results[:, :] = self.particles[:, 0:self.n_dimensions]+self.particles[:, 2 * self.n_dimensions:3 * self.n_dimensions]/1.2
			self.particles[:, 0:self.n_dimensions] = results[:, :]
			"""Evaluate the function value"""
			value = func(results)
			"""Update the best positions and values"""
			for i in range(self.n_particles):
				if value[i] < self.particles[i,-1]:
					self.particles[i,self.n_dimensions:2 * self.n_dimensions] = self.particles[i,0:self.n_dimensions]
					self.particles[i,-1] = value[i]
				else:
					pass
			"""Find the best position and its particle in the history"""
			gbest = np.argmin(self.particles[:, -1])
			"""Update the velocities"""
			self.particles[:, 2 * self.n_dimensions:3 * self.n_dimensions] = np.random.rand() * inertia * self.particles[:, 2 * self.n_dimensions:3 * self.n_dimensions]+correction_factor * np.random.rand() * (self.particles[:, self.n_dimensions:2 * self.n_dimensions]-self.particles[:, 0:self.n_dimensions])+correction_factor * np.random.rand() * (self.particles[gbest,self.n_dimensions:2 * self.n_dimensions]-self.particles[:, 0:self.n_dimensions])

			if if_display:
				plt.pause(0.01)
				plt.close('all')
				if self.n_dimensions == 2:
					self.plot_fig_2d(i_iter+1, n_iterations, False, i_iter)
				elif self.n_dimensions == 3:
					self.plot_fig_3d(i_iter+1, n_iterations, False, i_iter)
				else:
					pass

		if if_display:
			if self.n_dimensions == 2:
				self.plot_fig_2d(i_iter+1, n_iterations, True, i_iter)
			elif self.n_dimensions == 3:
				self.plot_fig_3d(i_iter+1, n_iterations, True, i_iter)
			else:
				pass
			
		return [list(self.particles[gbest,0:self.n_dimensions]), self.particles[gbest,-1]]

	def plot_fig_2d(self, i_iter, n_iterations, block):
		fig  =  plt.figure()
		plt.scatter(self.particles[:, 0], self.particles[:, 1], linewidths = 1, edgecolors = 'black')
		plt.xlim([-10,10])
		plt.ylim([-10,10])
		plt.title("%d/%d" %(i_iter, n_iterations))
		plt.show(block = block)

	def plot_fig_3d(self, i_iter, n_iterations, block, view_angle):
		fig  =  plt.figure()
		ax  =  fig.add_subplot(projection = '3d')
		ax.scatter(self.particles[:, 0], self.particles[:, 1], self.particles[:, 2], linewidths = 1, edgecolors = 'black')
		ax.set_xlim(-10,10)
		ax.set_ylim(-10,10)
		ax.set_zlim(-10,10)
		ax.set_title("%d/%d" %(i_iter, n_iterations))
		ax.view_init(elev = 2.5 * i_iter, azim = 4 * i_iter)
		plt.show(block = block)


