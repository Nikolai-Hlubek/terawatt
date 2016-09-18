# basic.py
class Power:
    def __init__(self):
        self.__chemical = 0
        self.__thermal = 0
        self.__electrical = 0
        self.__solar = 0

class Energy:
    def __init__(self):
        self.chemical = 0
        self.thermal = 0
        self.electrical = 0

class State:
    def __init__(self):
        self.produce = False
        self.consume = False

class Device:
    def __init__(self):
        self.state = State()
        self.energy_now = Energy()
        self.energy_max = Energy()
        self.power = Power()  # For diagnosis

    def update(self, power, state=None):
        if state == 'produce':
            self.state.produce = True
            self.state.consume = False
        elif state == 'consume':
            self.state.produce = False
            self.state.consume = True
        elif state == 'both':
            self.state.produce = True
            self.state.consume = True
        elif state == 'off':
            self.state.produce = False
            self.state.consume = False

        self.power = power  # Store input power for diagnosis
        return power

class Need:
    ''' This class represents the need for power at a given timepoint in the future. '''

    def __init__(self, time, power):
        # Future timepoint in seconds since 01.01.1970
        self.timepoint=time
        # Power needed in W
        self.power=power

class Consumer:
    ''' This class represents an entity which consumes energy at a certain point in 
    the future. This means that random or very short term power consumption will not
    be handled here.'''

    def __init__(self, broker):
        self.need=[]

    def update():
        __updateNeed()
        __tellBroker()

    def __updateNeed(self):
        pass

    def __tellBroker(self):
        broker.update(self.need)

class Producer:
    ''' This class represents an entity which is able to produce energy at a certain
    point in the future. '''

    def __init__(self):
        self.registeredNeeds=[]

    def providePower(self, need):
        remaining_need,available_need=__provideEnergy(need)
        __registerNeed(available_need)
        return remaining_need

    def update(self):
        pass

    def __provideEnergy(self, need):
        pass

    def _registerNeed(self, available_need):
        pass

class Broker:
    ''' The broker receives all energy needs and sends requests to producers. In general,
    this could be parallelized?'''
    def __init__(self):
        pass
