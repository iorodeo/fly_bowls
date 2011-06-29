#!/usr/bin/env python
"""
Example: simple line plot.
Show how to make and save a simple line plot with labels, title and grid
"""
from __future__ import division
import numpy
import pylab


diameter = 20
# diameter = 5
# depth = 0.138
depth = 1
slope = 11                              # in degrees
theta = slope*numpy.pi/180

# Curves on top and bottom
L = ((depth)*numpy.pi)/(2*numpy.tan(theta))
if diameter/2 < L/2:
    raise ValueError("The depth is too large for this diameter.")

X = numpy.linspace(0,L)
# Y = ((depth)/2)*(1+numpy.cos(X*numpy.pi/L))
Y = ((depth)/2)*(1+numpy.sin(X*numpy.pi/L - numpy.pi/2))
# pylab.plot(X,Y)

# Add points to close profile
# CenterX = L/2 + diameter/2
# X = numpy.append(X,[CenterX,CenterX,0])
# Y = numpy.append(Y,[0,(2*depth),(2*depth)])

# Offset X
# X = X - L/2 - diameter/2

# Curve on bottom only
L = (depth*numpy.pi)/(2*numpy.tan(theta))
if diameter/2 < L/2:
    raise ValueError("The depth is too large for this diameter.")

X = numpy.linspace(0,L/2)
# Y = (depth/2)*(1+numpy.cos(X*numpy.pi/L))
Y = (depth/2)*(1+numpy.sin(X*numpy.pi/L - numpy.pi/2))

x0 = 0
y0 = 0
x1 = L/2 + depth/numpy.tan(theta)
y1 = 3/2*depth
X = numpy.append(X,x1)
Y = numpy.append(Y,y1)

# Offset for diameter, x0 and y0
offset = x0 + diameter/2 - L/2 - depth/(2*numpy.tan(theta))
x1 = x1 + offset
X = X + offset
y1 = y0 + y1
Y = Y + y0

# Add points to close profile
X = numpy.append(X,[x0,x0,offset])
Y = numpy.append(Y,[y1,y0,y0])

pylab.plot(X, Y)
pylab.axis('equal')
pylab.xlabel('X (mm)')
pylab.ylabel('Y (mm)')
pylab.title('Fly Bowl Cross Section')
pylab.grid(True)
pylab.savefig('simple_plot')

pylab.show()
