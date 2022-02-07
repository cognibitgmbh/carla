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

bp_library = world.get_blueprint_library()
pedestrian_bps = bp_library.filter('walker.*')
pedestrian_blueprint = pedestrian_bps[0]

spawn_transform = carla.Transform()
spawn_transform.location = carla.Vector3D(x=0, y=0, z=10)

pedestrian_actor = world.spawn_actor(pedestrian_blueprint, spawn_transform)

walker_control = carla.WalkerControl()
walker_control.speed = 1

pedestrian_actor.apply_control(walker_control)




