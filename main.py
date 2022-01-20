import timeit
from PSO import *


if __name__ == "__main__":

	def func1(x):
		return (x[:, 0] - 5.0)**2 + (x[:, 1] - 2.5)**2

	def func2(x):
		return x[:, 0]**2 + x[:, 1]**2 + 100*np.sin(x[:, 0]**2) + 100 * np.cos(x[:, 1]**2)

	def func3(x):
		return np.exp(np.sin(50 * x[:, 0])) + np.sin(60 * np.exp(x[:, 1])) + np.sin(70 * np.sin(x[:, 0])) + np.sin(np.sin(80 * x[:, 1])) - np.sin(10 * (x[:, 0]+x[:, 1])) + 0.25 * (x[:, 0]**2+x[:, 1]**2)

	def func4(x):
		return x[:, 0]**2 + x[:, 1]**2 + x[:, 2]**2 + 100 * np.sin(x[:, 0]**2) + 100 * np.cos(x[:, 1]**2) + 100 * np.sin(np.cos(x[:, 2]**2));

	optimizer = PSO_Optimizer(3, n_particles = 600)
	optimizer.initialize([8, 8, 8], [0, 0, 0])

	start = timeit.default_timer()

	results = optimizer.optimize(func4, n_iterations = 100, if_display = False)

	stop = timeit.default_timer()
	execution_time = stop - start

	print(f"{results[1]: .10f}: ({results[0][0]: .10f}, {results[0][1]: .10f}, {results[0][2]: .10f})")

	print("Time spent: " + str(execution_time))  # This returns time in seconds




