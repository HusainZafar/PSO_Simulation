'''
Paper referred: Particle Swarm Optimization:  A Tutorial

PSO : Particle Swarm Optimizer
For the objective function: |(0.07*i - 10)**3 - 8*i + 500|, which has a local minima and a global minima.
Requires optimization along a single dimension.
'''

'''
v(t+1) = w*v(t) + c1*r1*[p_best(t) - x(t)] + c2*r2*[g_best(t) - x(t)]	: For each particle
x(t+1) = x(t) + v(t+1)							: For each particle

0.8 < w < 1.2  => w = 1
0 < c1, c2 < 2 => c1 = c2 = 2
0 < r1, r2 < 1

velocity clamping: vmax = k * (xmax - xmin) / 2; 0.1 < k < 1.0 => k = 0.5
'''

import matplotlib.pyplot as plt, random

def function(values):
	output = []
	for i in values:
		output.append(abs((0.07*i - 10)**3 - 8*i + 500))
	return output

def near_minima(values, offset):
	output = 0
	for i in values:
		#326.038 is the actual value at which objective function is 0(cheked using a grapher)
		if abs(i-326.038) < offset:
			output += 1
	return output

#define initial parameters for the PSO
w = 0;c1 = c2 = 2; k = 0.5; xmax = 500; xmin = 0
vmax = k * (xmax - xmin)/2 
max_iter = 500
no_particles = 100

values_x = [] #position of each point
velocity = [] #velocity of each point
p_best_x   = [] #personal_best of each point x_val
g_best_x   = random.randrange(xmin, xmax)  #global best x_value

#assign random positions and velocities to the particles
for i in range(no_particles):
    values_x.append(random.uniform(xmin, xmax + 1))
    velocity.append(random.randrange(-vmax, vmax))

p_best_x = values_x[::]

#initial plot settings
plt.axis([0, 500, 0, 1200])
plt.ion()
plt.plot(values_x, function(values_x), 'rx')
plt.title('PSO Simulation')
plt.ylabel('objective function = |(7/100x - 10)^3 - 8x +500|')
plt.text(450, 1300, "Total particles     : 100")
plt.text(450, 1250, "Near minima(5%): 100")
plt.text(2, 1300, "Number of iterations: 0")
plt.text(2, 1250, "Global minima : " + str(g_best_x))
plt.xlabel('x')
plt.show()

plt.plot(range(500), function(range(500)), 'g', linewidth = 0.5)

for j in range(max_iter):
    #clear previous plot and plot curve
    plt.gcf().clear()
    plt.axis([0, 500, 0, 1200])
    plt.title('PSO Simulation')
    plt.ylabel('objective function = |(7/100x - 10)^3 - 8x +500|')
    plt.xlabel('x')
    plt.text(450, 1300, "Total particles     : 100")
    plt.text(450, 1250, "Near minima(5%): " + str(near_minima(values_x,25)))
    plt.text(-80, 1300, "Number of iterations: " + str(j))
    plt.text(-80, 1250, "Global minima : " + str(g_best_x))

    plt.plot(range(500), function(range(500)), 'g', linewidth = 0.5)
    
    #calculate fitness of the particles
    fitness = function(values_x)
    p_best_y = function(p_best_x)

    #update personal best for each particle
    for i in range(no_particles):
        if fitness[i] < p_best_y[i]:
            p_best_x[i] = values_x[i]

    #update global best for each particle
    min_value, min_index = min( (v, i) for i, v in enumerate(p_best_y) )
    if [min_value] < function([g_best_x]):
        g_best_x = p_best_x[min_index]
    
    #for each iteration,
    for i in range(no_particles):
        r1, r2 = random.random(), random.random()
        
        #calculate new velocity and set it in the [min, max] range
        velocity[i] = w*velocity[i] + c1*r1*(p_best_x[i] - values_x[i]) + c2*r2*(g_best_x - values_x[i])
        if velocity[i] > vmax:    velocity[i] = vmax
        if velocity[i] < -vmax:    velocity[i] = -vmax
        
	#calculate new positions and set it in the [min, max] range
        values_x[i] = values_x[i] + velocity[i]
        if values_x[i] > xmax:    values_x[i] = xmax
        if values_x[i] < xmin:    values_x[i] = xmin
    
    #plot new particle positions
    for i in range(no_particles):
        plt.plot(values_x, function(values_x), 'rx')
    
    plt.pause(0.2)
    print (g_best_x)

#prevent plot from closing
while True:
    plt.pause(0.05)
