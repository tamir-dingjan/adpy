#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A module to automatically cluster a trajectory.

Created on Mon Apr  8 11:43:44 2019

@author: tamird
"""

import os
import mdtraj as md



class cluster:
    """
    A clustering object, which contains the methods to initialise the cluster-
    ing calculation, and write the clustered output.
    """
    
    def __init__(self, trajectory, topology):
        """
        Initialise the cluster object.
        
        Parameters
        ----------
        trajectory : str
            Filepath to trajectory file (XTC)
        topology : str
            Filepath to topology file (PDB/GRO)
        """
        
        self.traj = trajectory
        self.top = topology
        
        self.workdir = os.path.dirname(self.traj)+'/'
        self.basename = os.path.splitext(os.path.basename(self.traj))[0]
        
        # Write a PDB if given a GRO
        if 'gro' in os.path.splitext(os.path.basename(self.top))[-1]:
            # Write PDB
            # Update self.top
        
        # Load MD
        self.t = md.load(self.traj, top=self.top)
        
    def cluster(self):
        """
        Perform the clustering.
        """
        
        
        