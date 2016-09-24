import datetime
import random
import json
import os
import sys
import copy

sys.path.insert(0, os.path.join('..'))
import terawatt_model

from focus_groups import create_agent_n


def run_agent_n_day_n(agent_n, car_max_energy=22000):
    sun = terawatt_model.Sun()
    photovoltaic = terawatt_model.Photovoltaic()
    car1 = terawatt_model.Car(agent_n['car1_max_energy'])
    car2 = terawatt_model.Car(agent_n['car2_max_energy'])
    provider = terawatt_model.Provider()
    battery = terawatt_model.Battery()
    electrolysis = terawatt_model.Electrolysis()
    methanization = terawatt_model.Methanization()
    cogeneration = terawatt_model.Cogeneration()
    time_start = datetime.datetime(2016, 9, 24, 0, 0, 0, 0)

    # Car starts fully charged
    car1.energy_now.electrical = car_max_energy
    car2.energy_now.electrical = car_max_energy
    
    battery.battery_current_energy = agent_n['battery_energy']
    cogeneration.energy_now.chemical = agent_n['cogeneration_energy']
    
    # Subtract power required for drive of day
    agent_n['car1_distance_additional'] = random.randint(0, 20)
    agent_n['car2_distance_additional'] = random.randint(0, 20)
     # Now drive somewhere afterwards the energy is harvested for car charging
    agent_n['car1_drive_success'] = car1.drive(agent_n['car1_distance_work']+agent_n['car1_distance_additional'])
    agent_n['car2_drive_success'] = car2.drive(agent_n['car2_distance_work']+agent_n['car2_distance_additional'])
 
    for dt in range(0, 3600*24-1, terawatt_model.timestep):
        time = time_start + datetime.timedelta(0, dt) # days, seconds

        power = sun.update(time=time)
        power = photovoltaic.update(power)

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

        if agent_n['charge_car2_start'] <= time.hour <= agent_n['charge_car2_start'] + agent_n['charge_car2_time']:
            if car2.energy_now.electrical < 0.99*car2.energy_max.electrical:
                power_requested.electrical += car2.get_power_in_max().electrical

        power_requested.chemical += cogeneration.power_conversion_electrical_to_chemical(power_requested.electrical).chemical
        power = cogeneration.update(power, state='provide', power_requested=power_requested)
        power_requested.electrical -= power.electrical
        power = battery.update(power, state='provide', power_requested=power_requested)

        # Consumers consume
        if agent_n['charge_car1_start'] <= time.hour <= agent_n['charge_car1_start'] + agent_n['charge_car1_time']:
            power = car1.update(power)

        if agent_n['charge_car2_start'] <= time.hour <= agent_n['charge_car2_start'] + agent_n['charge_car2_time']:
            power = car2.update(power)

        power = provider.update(power)
        
        
   # Excess energy will come from the provider but we have to pay for it
    agent_n['car1_energy'] = car_max_energy - car1.energy_now.electrical
    agent_n['car2_energy'] = car_max_energy - car2.energy_now.electrical
    # Battery will only buffer internal and remain its state
    agent_n['battery_energy'] = battery.energy_now.electrical
    agent_n['cogeneration_energy'] = cogeneration.energy_now.chemical

    return agent_n


data = []
for n in range(5):
   
    print('Number of agents processed', n) 
    data_agent = []
    agent_n = create_agent_n(n)
    print(agent_n)
    data_agent.append(copy.deepcopy(agent_n))

    for day in range(25):
        agent_n = run_agent_n_day_n(agent_n)
        print(agent_n)
        data_agent.append(copy.deepcopy(agent_n))
    
    data.append(data_agent)
    
    # write intermediary results 
    with open('agents_undisciplined_provider.dat', 'w') as outfile:
        json.dump(data, outfile)


with open('agents_undisciplined_provider.dat', 'w') as outfile:
    json.dump(data, outfile)

