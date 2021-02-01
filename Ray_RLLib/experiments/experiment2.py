from experiments.base_experiment import *
from helper.CarlaHelper import spawn_vehicle_at, post_process_image, update_config
import random
import numpy as np
from gym.spaces import Box
from itertools import cycle
import cv2
import time
import carla
import gc

SERVER_VIEW_CONFIG = {
}

SENSOR_CONFIG = {
    "CAMERA_NORMALIZED": [True], # apparently doesnt work if set to false, its just for the image!
    "CAMERA_GRAYSCALE": [True],
    "FRAMESTACK": 4,
}

BIRDVIEW_CONFIG = {
    "SIZE": 190,
    "RADIUS": 15,
    "FRAMESTACK": 4
}

OBSERVATION_CONFIG = {
    "CAMERA_OBSERVATION": [False],
    "BIRDVIEW_OBSERVATION": True,
}

EXPERIMENT_CONFIG = {
    "OBSERVATION_CONFIG": OBSERVATION_CONFIG,
    "Server_View": SERVER_VIEW_CONFIG,
    "SENSOR_CONFIG": SENSOR_CONFIG,
    "server_map": "Town02_Opt",
    "BIRDVIEW_CONFIG": BIRDVIEW_CONFIG,
    "n_vehicles": 0,
    "n_walkers": 0,
    "hero_vehicle_model": "vehicle.lincoln.mkz2017",
}

class Experiment(BaseExperiment):
    def __init__(self):
        config=update_config(BASE_EXPERIMENT_CONFIG, EXPERIMENT_CONFIG)
        super().__init__(config)

    def initialize_reward(self, core):
        """
        Generic initialization of reward function
        :param core:
        :return:
        """
        self.previous_distance = 0
        self.i = 0
        self.frame_stack = 4  # can be 1,2,3,4
        self.prev_image_0 = None
        self.prev_image_1 = None
        self.prev_image_2 = None
        self.allowed_types = [carla.LaneType.Driving, carla.LaneType.Parking]

    def set_observation_space(self):
        num_of_channels = 3
        image_space = Box(
            low=0.0,
            high=255.0,
            shape=(
                self.experiment_config["BIRDVIEW_CONFIG"]["SIZE"],
                self.experiment_config["BIRDVIEW_CONFIG"]["SIZE"],
                num_of_channels * self.experiment_config["BIRDVIEW_CONFIG"]["FRAMESTACK"],
            ),
            dtype=np.uint8,
        )
        self.observation_space = image_space

    def process_observation(self, core, observation):
        """
        Process observations according to your experiment
        :param core:
        :param observation:
        :return:
        """
        self.set_server_view(core)
        image = post_process_image(observation['birdview'],
                                   normalized = False,
                                   grayscale = False
        )

        if self.prev_image_0 is None:
            self.prev_image_0 = image
            self.prev_image_1 = self.prev_image_0
            self.prev_image_2 = self.prev_image_1

        images = image

        if self.frame_stack >= 2:
            images = np.concatenate([self.prev_image_0, images], axis=2)
        if self.frame_stack >= 3 and images is not None:
            images = np.concatenate([self.prev_image_1, images], axis=2)
        if self.frame_stack >= 4 and images is not None:
            images = np.concatenate([self.prev_image_2, images], axis=2)

        self.prev_image_2 = self.prev_image_1
        self.prev_image_1 = self.prev_image_0
        self.prev_image_0 = image

        return images

    def inside_lane(self, map):
        self.current_w = map.get_waypoint(self.hero.get_location(), lane_type=carla.LaneType.Any)
        return self.current_w.lane_type in self.allowed_types

    def dist_to_driving_lane(self, map_):
        cur_loc = self.hero.get_location()
        self.current_w = map_.get_waypoint(cur_loc)
        return math.sqrt((cur_loc.x - self.current_w.transform.location.x)**2 +
                         (cur_loc.y - self.current_w.transform.location.y)**2)

    def get_done_status(self):
        #done = self.observation["collision"] is not False or not self.check_lane_type(map)
        self.done_idle = self.max_idle < self.t_idle
        if self.get_speed() > 2.0:
            self.t_idle = 0
        self.done_max_time = self.max_ep_time < self.t_ep
        self.done_falling = self.hero.get_location().z < -0.5
        return self.done_idle or self.done_max_time or self.done_falling

    def compute_reward(self, core, observation, map):
        """
        Reward function
        :param observation:
        :param core:
        :return:
        """

        c = float(np.sqrt(np.square(self.hero.get_location().x - self.start_location.x) + \
                            np.square(self.hero.get_location().y - self.start_location.y)))

        d = self.dist_to_driving_lane(map)
        Dmin, Dmax = 5, 25
        if d < Dmin:
            m = 1
        else:
            m = max((d - Dmax) / (Dmin - Dmax), 0)

        if c > self.previous_distance + 1e-2:
            if self.inside_lane(map) and self.current_w.is_junction():
                m=m*10
            reward = m*(c - self.previous_distance)
            self.previous_distance = c
        else:
            reward = 0

        self.start_location = self.hero.get_location()
        self.previous_distance = 0
        if self.done_max_time:
            print("Done by max time")
            reward += 10
        if self.done_falling:
            print("Done falling")
            reward += -3
        if self.done_idle:
            print("Done idle")
            reward += -1

        # if self.observation["collision"] != False or not self.inside_lane(map):
        #     reward = 0
        # elif c > self.previous_distance + 1e-2:
        #     reward = c - self.previous_distance
        # else:
        #     reward = 0

        if c > 30: # to avoid losing points for getting closer to initial location
            self.start_location = self.hero.get_location()
            self.previous_distance = 0
        # if self.previous_distance < 15 and reward < 0:
        #     reward = 0
        #     print("avoid negative reward")
        return reward
