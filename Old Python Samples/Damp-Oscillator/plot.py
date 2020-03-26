#!/opt/local/bin/python
# Position vs. time for Homework Project 2

import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8,6), dpi=80)

ax = plt.subplot(111)

paramsFilename = 'params'
filename = 'position.dat'

# set title
plt.title(r'Numerical Solution for $x(t)$',fontsize=16,color='black')

# Read in data
data = np.loadtxt(filename)
tdata = data.T[0]
xdata = data.T[1]

params = np.loadtxt(paramsFilename)
x0 = params[0]
v0 = params[1]
k = params[2]
b = params[3]
m = params[4]

alpha = k/m
beta = b/m
omega = np.sqrt(4*alpha-beta**2)/2

A = x0
B = (beta*x0+v0)/omega

def x(t):
	return A*np.cos(omega*t)*np.exp(-beta*t/2)+B*np.sin(omega*t)*np.exp(-beta*t/2)

# set up domain variables
tmin = np.min(tdata)
tmax = np.max(tdata)
trange = tmax - tmin

xmin = np.min(xdata)
xmax = np.max(xdata)
xrange = xmax - xmin

texact = np.linspace(tmin,tmax,1001,endpoint=True)
xexact = x(texact)

# Plot the data
plt.plot(tdata,xdata,color='red', linewidth=1.5,label='Numerical Solution')
plt.plot(texact,xexact,color='blue',linewidth=1.5,linestyle='dashed',label='Exact Solution')

# Set the axis labels
plt.xlabel(r'$t$',fontsize=16,labelpad=0)
plt.ylabel(r'$x(t)$',fontsize=16)

# Set the axis limits with a bit of a margin
margin = 0.1
plt.xlim(tmin, tmax)
plt.ylim(xmin - xrange * margin, xmax + xrange * margin)

# Remove unneeded axes
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

plt.legend(loc='upper right',frameon=True)

# Makes other axes intersect at the origin
#ax.spines['bottom'].set_position(('data',0))
#ax.spines['left'].set_position(('data',0))

# Save figure to file
plt.savefig("xvst.pdf",dpi=72)

# Display figure
#plt.show()
