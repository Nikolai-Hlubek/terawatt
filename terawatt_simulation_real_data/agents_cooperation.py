import datetime
import random
import json
import os
import sys
import copy

sys.path.insert(0, os.path.join('..'))
import terawatt_model


def create_agent_n():
    agent_n = dict(
        #car1_energy = random.randint(0, terawatt_model.Car.energy_max.electrical),
        car1_energy = 0,
        charge_car1_start = random.randint(0, 19),
        charge_car1_time = random.randint(0, 5),
        car1_distance_work = random.randint(40, 80),
        car1_distance_additional = 0,
        car1_drive_success = False,
        #car2_energy = random.randint(0, terawatt_model.Car.energy_max.electrical),
        car2_energy = 0,
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


def run_agent_n_day_n(agent_n):
    sun = terawatt_model.Sun()
    photovoltaic = terawatt_model.Photovoltaic()
    car1 = terawatt_model.Car()
    car2 = terawatt_model.Car()
    provider = terawatt_model.Provider()
    battery = terawatt_model.Battery()
    electrolysis = terawatt_model.Electrolysis()
    methanization = terawatt_model.Methanization()
    cogeneration = terawatt_model.Cogeneration()
    time_start = datetime.datetime(2016, 9, 24, 0, 0, 0, 0)

    car1.energy_now.electrical = agent_n['car1_energy']
    car2.energy_now.electrical = agent_n['car2_energy']
    battery.battery_current_energy = agent_n['battery_energy']
    cogeneration.energy_now.chemical = agent_n['cogeneration_energy']

    max_energy = dict(
        energy = 0,
        timestamp = 0,
    )


    for dt in range(0, 3600*24-1, terawatt_model.timestep):
        time = time_start + datetime.timedelta(0, dt) # days, seconds
        
        power = sun.update(time=time)
        power = photovoltaic.update(power, time=time)

        power = battery.update(power, state='consume')
        power = electrolysis.update(power, state='both', power_requested=methanization.get_power_in_max())
        power = methanization.update(power, state='both', power_requested=methanization.get_power_out_max())
        power = cogeneration.update(power, state='consume')

        # Consumers request
        power_requested = terawatt_model.Power()
        if agent_n['charge_car1_start'] <= time.hour <= agent_n['charge_car1_start'] + agent_n['charge_car1_time']:
            # cannot compare against full charge. Due to incremental energies we never reach full charge exactly.
            if car1.energy_now.electrical < 0.99*car1.energy_max.electrical:
                power_requested.electrical += car1.get_power_in_max().electrical

        if agent_n['max_energy_timestamp'] <= dt <= agent_n['max_energy_timestamp'] + agent_n['charge_car2_time']*3600:
            if car2.energy_now.electrical < 0.99*car2.energy_max.electrical:
                power_requested.electrical += car2.get_power_in_max().electrical

        power_requested.chemical += cogeneration.power_conversion_electrical_to_chemical(power_requested.electrical).chemical
        power = cogeneration.update(power, state='provide', power_requested=power_requested)
        power_requested.electrical -= power.electrical
        power = battery.update(power, state='provide', power_requested=power_requested)

        # Consumers consume
        if agent_n['charge_car1_start'] <= time.hour <= agent_n['charge_car1_start'] + agent_n['charge_car1_time']:
            power = car1.update(power)

        if agent_n['max_energy_timestamp'] <= dt <= agent_n['max_energy_timestamp'] + agent_n['charge_car2_time']*3600:
            power = car2.update(power)

        power = provider.update(power)

        # Find energy maximum for today
        current_total_energy = photovoltaic.energy_now.electrical + battery.energy_now.electrical + cogeneration.energy_now.electrical
        if current_total_energy > max_energy['energy']:
            max_energy['energy'] = current_total_energy
            max_energy['timestamp'] = dt
        
        
    # Subtract power required for drive of day
    agent_n['car1_distance_additional'] = random.randint(0, 10)
    agent_n['car2_distance_additional'] = random.randint(0, 10)
    agent_n['car1_drive_success'] = car1.drive(agent_n['car1_distance_work']+agent_n['car1_distance_additional'])
    agent_n['car2_drive_success'] = car2.drive(agent_n['car2_distance_work']+agent_n['car2_distance_additional'])
    agent_n['car1_energy'] = car1.energy_now.electrical
    agent_n['car2_energy'] = car2.energy_now.electrical
    agent_n['battery_energy'] = battery.energy_now.electrical
    agent_n['cogeneration_energy'] = cogeneration.energy_now.chemical
    agent_n['max_energy_timestamp'] = max_energy['timestamp']

    return agent_n


# Load focus groups from agents undisciplined
with open('agents_undisciplined.dat') as json_data:
    data_agent_undisciplined = json.load(json_data)

data = []
for agent in range(5):
    
    print('Number of agents simulated', agent)
    data_agent = []
    agent_n = data_agent_undisciplined[agent][0]
    print(agent_n)
    data_agent.append(copy.deepcopy(agent_n))
    agent_n['max_energy_timestamp'] = 0

    for day in range(25):
        agent_n = run_agent_n_day_n(agent_n)
        print(agent_n)
        data_agent.append(copy.deepcopy(agent_n))
    
    data.append(data_agent)


    with open('agents_cooperation.dat', 'w') as outfile:
        json.dump(data, outfile)


with open('agents_cooperation.dat', 'w') as outfile:
    json.dump(data, outfile)

