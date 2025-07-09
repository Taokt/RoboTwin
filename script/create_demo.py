import sys

sys.path.append("./")

import sapien.core as sapien
from sapien.render import clear_cache
from collections import OrderedDict
import pdb
from envs import *
import yaml
import importlib
import json
import traceback
import os
import time
from argparse import ArgumentParser

current_file_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(current_file_path)

# from envs.beat_block_hammer import *
from collect_data import class_decorator, get_camera_config, get_embodiment_config

def create_demo(task_name, task_config):
    
    task = class_decorator(task_name)
    config_path = f"./task_config/{task_config}.yml"

    with open(config_path, "r", encoding="utf-8") as f:
        args = yaml.load(f.read(), Loader=yaml.FullLoader)

    args['task_name'] = task_name

    embodiment_type = args.get("embodiment")
    embodiment_config_path = os.path.join(CONFIGS_PATH, "_embodiment_config.yml")

    with open(embodiment_config_path, "r", encoding="utf-8") as f:
        _embodiment_types = yaml.load(f.read(), Loader=yaml.FullLoader)

    def get_embodiment_file(embodiment_type):
        robot_file = _embodiment_types[embodiment_type]["file_path"]
        if robot_file is None:
            raise "missing embodiment files"
        return robot_file

    if len(embodiment_type) == 1:
        args["left_robot_file"] = get_embodiment_file(embodiment_type[0])
        args["right_robot_file"] = get_embodiment_file(embodiment_type[0])
        args["dual_arm_embodied"] = True
    elif len(embodiment_type) == 3:
        args["left_robot_file"] = get_embodiment_file(embodiment_type[0])
        args["right_robot_file"] = get_embodiment_file(embodiment_type[1])
        args["embodiment_dis"] = embodiment_type[2]
        args["dual_arm_embodied"] = False
    else:
        raise "number of embodiment config parameters should be 1 or 3"

    args["left_embodiment_config"] = get_embodiment_config(args["left_robot_file"])
    args["right_embodiment_config"] = get_embodiment_config(args["right_robot_file"])

    if len(embodiment_type) == 1:
        embodiment_name = str(embodiment_type[0])
    else:
        embodiment_name = str(embodiment_type[0]) + "+" + str(embodiment_type[1])

    # show config
    print("============= Config =============\n")
    print("\033[95mMessy Table:\033[0m " + str(args["domain_randomization"]["cluttered_table"]))
    print("\033[95mRandom Background:\033[0m " + str(args["domain_randomization"]["random_background"]))
    if args["domain_randomization"]["random_background"]:
        print(" - Clean Background Rate: " + str(args["domain_randomization"]["clean_background_rate"]))
    print("\033[95mRandom Light:\033[0m " + str(args["domain_randomization"]["random_light"]))
    if args["domain_randomization"]["random_light"]:
        print(" - Crazy Random Light Rate: " + str(args["domain_randomization"]["crazy_random_light_rate"]))
    print("\033[95mRandom Table Height:\033[0m " + str(args["domain_randomization"]["random_table_height"]))
    print("\033[95mRandom Head Camera Distance:\033[0m " + str(args["domain_randomization"]["random_head_camera_dis"]))

    print("\033[94mHead Camera Config:\033[0m " + str(args["camera"]["head_camera_type"]) + f", " +
          str(args["camera"]["collect_head_camera"]))
    print("\033[94mWrist Camera Config:\033[0m " + str(args["camera"]["wrist_camera_type"]) + f", " +
          str(args["camera"]["collect_wrist_camera"]))
    print("\033[94mEmbodiment Config:\033[0m " + embodiment_name)
    print("\n==================================")

    args["embodiment_name"] = embodiment_name
    args['task_config'] = task_config
    args["save_path"] = os.path.join(args["save_path"], str(args["task_name"]), args["task_config"])
    task.setup_demo(**args)
    return task

TASKS = {
    1: "adjust_bottle",
    2: "beat_block_hammer",
    3: "blocks_ranking_rgb",
    4: "blocks_ranking_size",
    5: "click_alarmclock",
    6: "clock_bell",
    7: "dump_bin_bigbin",
    8: "grab_roller",
    9: "handover_block",
    10: "handover_mic",
    11: "hanging_mug",
    12: "lift_pot",
    13: "move_can_pot",
    14: "move_pillbottle",
    15: "move_playingcard_away",
    16: "move_stapler_pad",
    17: "open_laptop",
    18: "open_microwave",
    19: "pick_diverse_bottles",
    20: "pick_dual_bottles",
    21: "place_a2b_left",
    22: "place_a2b_right",
    23: "place_bread_basket",
    24: "place_bread_skillet",
    25: "place_burger_fries",
    26: "place_can_basket",
    27: "place_cans_plasticbox",
    28: "place_container_plate",
    29: "place_dual_shoes",
    30: "place_empty_cup",
    31: "place_fan",
    32: "place_mouse_pad",
    33: "place_object_basket",
    34: "place_object_scale",
    35: "place_object_stand",
    36: "place_phone_stand",
    37: "place_shoe",
    38: "press_stapler",
    39: "put_bottles_dustbin",
    40: "put_object_cabinet",
    41: "rotate_qrcode",
    42: "scan_object",
    43: "shake_bottle",
    44: "shake_bottle_horizontally",
    45: "stack_blocks_three",
    46: "stack_blocks_two",
    47: "stack_bowls_three",
    48: "stack_bowls_two",
    49: "stamp_seal",
    50: "turn_switch",
}

# task_name = input("Enter task name or number (e.g., block_hammer_beat): ")
# task_name = TASKS[int(task_name)] if task_name.isdigit() else task_name
task_name = TASKS[2] # You can change this to any task you want to run
task_config = "demo_randomized"
demo = create_demo(task_name, task_config)
demo.play_once() # if you want to run the task


# Adding a dummy hammer for visualization
# demo.dummy, demo.dummy_data = create_glb(
#     demo.scene,
#     pose=sapien.Pose(pose1[:3],pose1[3:]),
#     modelname="020_hammer_2",
# )


## Picking the hammer
# block_pose = demo.block.get_functional_point(0, "pose").p
# arm_tag = ArmTag("left" if block_pose[0] < 0 else "right")

# Grasp the hammer with the selected arm
# demo.move(demo.grasp_actor(demo.hammer, arm_tag=arm_tag, pre_grasp_dis=0.12, grasp_dis=0.01))
# Move the hammer upwards
# demo.move(demo.move_by_displacement(arm_tag, z=0.07, move_axis="arm"))


# Move the gripper to a specific pose
# pose = demo.robot.left_ee.global_pose
# pose.p = np.array([0, 0, 1])
# pose.q = np.array([0.0, -1.0, 0.0, 1.0])
# actions = [Action(arm_tag, "move", target_pose=pose)]
# demo.move((arm_tag, actions))

while not demo.viewer.closed:
    demo.scene.step()
    demo.scene.update_render()
    demo.viewer.render()