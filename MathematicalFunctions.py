#!/usr/bin/python
'''
Created on Feb 1, 2014

@author: teamA
'''

class Maths(object):
    '''
    classdocs
    '''
    @staticmethod
    def VelocityToAccel(oldV, newV, timestep):
        '''
        
        @param oldV    previous velocity
        @type          array of numbers larger then 3
        @param newV    current velocity
        @type          array of numbers larger then 3
        '''
        x = (newV[0] - oldV[0]) / timestep
        y = (newV[1] - oldV[1]) / timestep
        z = (newV[2] - oldV[2]) / timestep
        return (x, y, z)

    def __init__(self, params):
        '''
        These functions are static, the constructor should be necessary.
        '''
        