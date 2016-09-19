#!/usr/bin/env python3

from .globals import *

class Power:
    def __init__(self):
        self.chemical = 0
        self.thermal = 0
        self.electrical = 0
        self.solar = 0

class Energy:
    def __init__(self):
        self.chemical = 0
        self.thermal = 0
        self.electrical = 0
        self.solar = 0

class State:
    def __init__(self):
        self.provide = False
        self.consume = False

class Device:
    def __init__(self):
        self.state = State()
        self.energy_now = Energy()
        self.energy_provided = Energy()
        self.energy_consumed = Energy()
        self.energy_max = Energy()
        self.power = Power()  # For diagnosis

    def update(self, power, state=None):
        if state == 'provide':
            self.state.provide = True
            self.state.consume = False
        elif state == 'consume':
            self.state.provide = False
            self.state.consume = True
        elif state == 'both':
            self.state.provide = True
            self.state.consume = True
        elif state == 'off':
            self.state.provide = False
            self.state.consume = False

        self._log_current_power  # Store input power for diagnosis
        return power
    
    def _to_energy(self, power_type):
        return power_type*(timestep/3600)
    
    def _to_power(self, energy_type):
        return energy_type*(3600/timestep)
    
    def _log_current_power(self, power):
        """
        copy.deepcopy whould also work, but the direct implementation is faster
        """
        self.power.electrical = power.electrical
        self.power.thermal = power.thermal
        self.power.chemical = power.chemical
        self.power.solar = power.solar
