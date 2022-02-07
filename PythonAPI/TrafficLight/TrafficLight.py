# Syncronization of the pedestrian traffic light based on the state of the corresponding vehicle traffic lights.

import glob
import os
import sys
import time

#!!!Adapt Carla's path to your case
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

client = carla.Client("127.0.0.1", 2000)
client.set_timeout(10.0)
world = client.get_world()
List = world.get_actors()

# ---
# Getting the traffic lights based and his postion
# ---
for i in List:
    if round(i.get_location().x,1) == 12.00 and round(i.get_location().y,2) ==-6.4:
        traffic_light_1 = i
    if round(i.get_location().x,1) == 6.40 and round(i.get_location().y,2) ==12:
        traffic_light_2 = i
    if round(i.get_location().x,1) == -12.00 and round(i.get_location().y,2) ==6.4:
        traffic_light_3 = i
    if round(i.get_location().x,1) == -6.40 and round(i.get_location().y,2) ==-12.00:
        traffic_light_4 = i
    if round(i.get_location().x,1) == 11.50 and round(i.get_location().y,2) ==-6.10:
        P_traffic_light_1_1 = i
    if round(i.get_location().x,1) == 11.50 and round(i.get_location().y,2) ==6.10:
        P_traffic_light_1_2 = i
    if round(i.get_location().x,1) == 6.10 and round(i.get_location().y,2) ==11.5:
        P_traffic_light_2_1 = i
    if round(i.get_location().x,1) == -6.10 and round(i.get_location().y,2) ==11.5:
        P_traffic_light_2_2 = i
    if round(i.get_location().x,1) == -11.50 and round(i.get_location().y,2) ==6.10:
        P_traffic_light_3_1 = i
    if round(i.get_location().x,1) == -11.50 and round(i.get_location().y,2) ==-6.10:
        P_traffic_light_3_2 = i
    if round(i.get_location().x,1) == -6.10 and round(i.get_location().y,2) ==-11.50:
        P_traffic_light_4_1 = i
    if round(i.get_location().x,1) == 6.10 and round(i.get_location().y,2) ==-11.50:
        P_traffic_light_4_2 = i

# ---
# Loop checking and changing the state of the traffic based on the state of the vehicle traffic light
# vehicle traffic light = red -> pedestrian traffic light = green
# vehicle traffic light = green -> pedestrian traffic light = gred
# ---

while True:
    world.tick()
    #Control Traffic Section 1
    if traffic_light_1.get_state() == carla.TrafficLightState.Red:
        P_traffic_light_1_1.set_state(carla.TrafficLightState.Green)
        P_traffic_light_1_2.set_state(carla.TrafficLightState.Green)
    else:
        P_traffic_light_1_1.set_state(carla.TrafficLightState.Red)
        P_traffic_light_1_2.set_state(carla.TrafficLightState.Red)
    # Control Traffic Section 2
    if traffic_light_2.get_state() == carla.TrafficLightState.Red:
        P_traffic_light_2_1.set_state(carla.TrafficLightState.Green)
        P_traffic_light_2_2.set_state(carla.TrafficLightState.Green)
    else:
        P_traffic_light_2_1.set_state(carla.TrafficLightState.Red)
        P_traffic_light_2_2.set_state(carla.TrafficLightState.Red)
    # Control Traffic Section 3
    if traffic_light_3.get_state() == carla.TrafficLightState.Red:
        P_traffic_light_3_1.set_state(carla.TrafficLightState.Green)
        P_traffic_light_3_2.set_state(carla.TrafficLightState.Green)
    else:
        P_traffic_light_3_1.set_state(carla.TrafficLightState.Red)
        P_traffic_light_3_2.set_state(carla.TrafficLightState.Red)
    # Control Traffic Section 4
    if traffic_light_4.get_state() == carla.TrafficLightState.Red:
        P_traffic_light_4_1.set_state(carla.TrafficLightState.Green)
        P_traffic_light_4_2.set_state(carla.TrafficLightState.Green)
    else:
        P_traffic_light_4_1.set_state(carla.TrafficLightState.Red)
        P_traffic_light_4_2.set_state(carla.TrafficLightState.Red)


