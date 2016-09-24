import datetime
import random
import json
import os
import sys
import copy

sys.path.insert(0, os.path.join('..'))
import terawatt_model


def create_agent_n(n):
    agent_n = dict(
            car1_energy = 0,
            charge_car1_start = random.randint(0, 19),
            charge_car1_time = 6,
            car1_distance_work = random.randint(60, 120),
            car1_distance_additional = 0,
            car1_max_energy = 22000,
            car1_drive_success = False,
            car2_energy = 0,
            charge_car2_start = random.randint(0, 19),
            charge_car2_time = 6,
            car2_distance_work = random.randint(60, 120),
            car2_distance_additional = 0,
            car2_max_energy = 22000,
            car2_drive_success = False,
            battery_energy = 0,
            cogeneration_energy = 0,
    )
    if n == 0:
        agent_n['charge_car1_start'] = 18
        agent_n['charge_car2_start'] = 19
    elif n == 1:
        agent_n['charge_car1_start'] = 21
        agent_n['charge_car2_start'] = 17
    elif n == 2:
        agent_n['charge_car1_start'] = 12
        agent_n['charge_car2_start'] = 19
    elif n == 3:
        agent_n['charge_car1_start'] = 8
        agent_n['charge_car2_start'] = 16
    elif n == 4:
        agent_n['charge_car1_start'] = 20
        agent_n['charge_car2_start'] = 22
    else:
        agent_n = dict(
            #car1_energy = random.randint(0, terawatt_model.Car.energy_max.electrical),
            car1_energy = 0,
            car1_max_energy = 22000,
            charge_car1_start = random.randint(0, 19),
            charge_car1_time = random.randint(0, 5),
            car1_distance_work = random.randint(40, 80),
            car1_distance_additional = 0,
            car1_drive_success = False,
            #car2_energy = random.randint(0, terawatt_model.Car.energy_max.electrical),
            car2_energy = 0,
            car2_max_energy = 22000,
            charge_car2_start = random.randint(0, 19),
            charge_car2_time = random.randint(0, 5),
            car2_distance_work = random.randint(40, 80),
            car2_distance_additional = 0,
            car2_drive_success = False,
            #battery_energy = random.randint(0, terawatt_model.Battery.energy_max.electrical),
            battery_energy = 0,
            #cogeneration_energy = random.randint(0, 1000),
            cogeneration_energy = 0,
        )
    
    return agent_n


