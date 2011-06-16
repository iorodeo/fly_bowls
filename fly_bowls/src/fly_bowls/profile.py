#!/usr/bin/env python
"""
Example: simple line plot.
Show how to make and save a simple line plot with labels, title and grid
"""
from __future__ import division
import numpy
import pylab


diameter = 5
depth = 0.138
slope = 11                              # in degrees
theta = slope*numpy.pi/180

# Curves on top and bottom edges
# L = ((2*depth)*numpy.pi)/(2*numpy.tan(theta))
# if diameter/2 < L/2:
#     raise ValueError("The depth is too large for this diameter.")

# X = numpy.linspace(0,L)
# Y = ((2*depth)/2)*(1+numpy.cos(X*numpy.pi/L))

# Add points to close profile
# CenterX = L/2 + diameter/2
# X = numpy.append(X,[CenterX,CenterX,0])
# Y = numpy.append(Y,[0,(2*depth),(2*depth)])

# Offset X
# X = X - L/2 - diameter/2

# Curve on bottom edge only
L = (depth*numpy.pi)/(2*numpy.tan(theta))
if diameter/2 < L/2:
    raise ValueError("The depth is too large for this diameter.")

X = numpy.linspace(L/2,L)
Y = (depth/2)*(1+numpy.cos(X*numpy.pi/L))

y2 = numpy.tan(theta)*(L/2) + depth/2
X = numpy.insert(X,0,0)
Y = numpy.insert(Y,0,y2)
x1 = L/2 - depth/(2*numpy.tan(theta))

# Testing...
# H = 10
# X = numpy.linspace(0,100)
# Y = numpy.cos(X*numpy.pi/100)


pylab.plot(X, Y)
pylab.axis('equal')
pylab.xlabel('X (mm)')
pylab.ylabel('Y (mm)')
pylab.title('Fly Bowl Cross Section')
pylab.grid(True)
pylab.savefig('simple_plot')

pylab.show()
