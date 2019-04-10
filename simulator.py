#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
A module to manage the running of simulations.

Created on Mon Apr  1 15:58:56 2019

@author: tamird
"""

import subprocess
import os
import glob


class simulator:
    """
    A simulator object. Can be initialised with an atomic coordinate file
    and an MDP parameter file, and used to perform a simulation.
    """

    def __init__(self, coordinates, parameters):
        """
        Initialise the simulator object with coordinates and parameters.

        Parameters
        ----------
        coordinates : str
            Absolute filepath to an atomic coordinate file in PDB format.
        parameters : str
            Absolute filepath to a parameter file.
        """
        self.coordinates = coordinates
        self.parameters = parameters
        self.workdir = os.path.dirname(self.coordinates)+'/'
        self.basename = os.path.splitext(os.path.basename(self.coordinates))[0]
        
        self.gmxrc = "/home/data/mashas/yaronbe/AnchorDock/AnchorDock/gromacs_shrek/GMXRC.bash"
        self.ff = "amber99sb-ildn"
        self.shell = "/bin/bash"

    def write_submission_script(self, commands, name):
        """
        Write the qsub submission file.
        """
        head = ["#!/bin/bash",
                "#$ -N "+name,
                "#$ -q all_old.q",
                "#$ -o "+self.workdir,
                "#$ -cwd",
                "#$ -j y",
                "#$ -pe pe_slots 1",
                "#$ -S "+self.shell,
                "source "+self.gmxrc]
        with open(self.workdir+name+".sub", 'w') as script:
            script.write("\n".join(head))
            script.write("\n")
            script.write("\n".join(commands))
            script.write("\n")
        
    def prepare_topology(self, name):
        """
        Prepare the topology files for the simulation. Constraints
        can be added using this method (TODO)
        """
        # Write GRO and TOP files
        
        self.groName = self.basename+'.gro'
        self.topName = self.basename+'.top'
        
        prepare = ['pdb2gmx',
                   '-f',
                   self.coordinates,
                   '-o',
                   self.workdir+self.groName,
                   '-p',
                   self.workdir+self.topName,
                   '-ff',
                   self.ff,
                   '-water',
                   'none',
                   '-vsite',
                   'hydrogens',
                   '-ignh']

        # Write submission file
        self.write_submission_script([" ".join(prepare)],
                                     name)
        
        #Submit run
        subprocess.call(["qsub", self.workdir+name+".sub"])

    def run(self, name):
        """
        Run the simulation. This method writes the simulation commands to a
        script file and submits it using qsub.
        """
        
        # Grompp 
        grompp = ['grompp',
                  '-f',
                  self.parameters,
                  '-po',
                  self.workdir+name+'.mdp',
                  '-c',
                  self.workdir+self.groName,
                  '-p',
                  self.workdir+self.topName,
                  '-o',
                  self.workdir+name+'.tpr']
        # Run 
        run = ['mdrun',
               '-s',
               self.workdir+name+'.tpr',
               '-deffnm',
               name]
        
        # Write the qsub script file
        self.write_submission_script([" ".join(grompp), 
                                      " ".join(run)], 
                                     name)
        
        # Submit run
        subprocess.call(["qsub", self.workdir+name+".sub"])
