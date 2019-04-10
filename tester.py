#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 10:08:26 2019

@author: tamird
"""

import simulator

# Test the simulator.py
coord = "/home/data/mashas/tamir/adpy/testing/lig.pdb"
param = "/home/data/mashas/tamir/adpy/testing/pf.mdp"

sim = simulator.simulator(coord, param)

sim.prepare_topology("prepare")

sim.run("run01")
