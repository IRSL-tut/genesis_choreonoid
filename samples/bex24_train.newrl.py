import argparse
import os
import pickle
import shutil

from importlib import metadata
ver_rsl_rl = metadata.version("rsl-rl-lib")
print(f"Version of rsl-rl-lib : {ver_rsl_rl}")

from rsl_rl.runners import OnPolicyRunner

import genesis as gs

from bex24_env_gs import Bex24Env as RL_Env

def get_train_cfg(exp_name, max_iterations):
    train_cfg_dict = {
        ## runner
        "class_name": "OnPolicyRunner",
        # -- general
        "num_steps_per_env": 24,
        "max_iterations": max_iterations,
        "seed": 1,
        # -- observations
        # "obs_groups": {"policy": ["policy"], "critic": ["policy", "privileged"]} # maps observation groups to types. See `vec_env.py` for more information
        "obs_groups": {"policy": ["policy"], "critic": ["policy"]}, # maps observation groups to types. See `vec_env.py` for more information
        # -- logging parameters
        "save_interval": 100,
        "experiment_name": exp_name,
        "run_name": "",
        # -- logging writer
        "logger": "tensorboard",  # tensorboard, neptune, wandb #not in v2.2.4
        "neptune_project": "legged_gym", #not in v2.2.4
        "wandb_project":   "legged_gym", #not in v2.2.4
        ##
        "empirical_normalization": None,
        ###
        "algorithm": {
            "class_name": "PPO",
            # -- training
            "learning_rate": 0.001,
            "num_learning_epochs": 5,
            "num_mini_batches": 4,
            "schedule": "adaptive",
            # -- value function
            "value_loss_coef": 1.0,
            "clip_param": 0.2,
            "use_clipped_value_loss": True,
            # -- surrogate loss
            "desired_kl": 0.01,
            "entropy_coef": 0.01,
            "gamma": 0.99,
            "lam": 0.95,
            "max_grad_norm": 1.0,
            # -- miscellaneous
            "normalize_advantage_per_mini_batch": False, #not in v2.2.4
        },
        "init_member_classes": {},
        ###
        "policy": {
            "class_name": "ActorCritic",
            "activation": "elu",
            "actor_obs_normalization": False, #not in v2.2.4
            "critic_obs_normalization": False, #not in v2.2.4
            "actor_hidden_dims": [512, 256, 128],
            "critic_hidden_dims": [512, 256, 128],
            "init_noise_std": 1.0,
            "noise_std_type": "scalar", # 'scalar' or 'log' #not in v2.2.4
        },
    }
    return train_cfg_dict


def get_cfgs():
    env_cfg = {
        "num_actions": 12,
        "default_joint_angles": {  # [rad]
            "LF_JOINT1": 0.0,
            "RF_JOINT1": 0.0,
            "LB_JOINT1": 0.0,
            "RB_JOINT1": 0.0,
            "LF_JOINT2": 0.65,
            "RF_JOINT2": 0.65,
            "LB_JOINT2": 0.8,
            "RB_JOINT2": 0.8,
            "LF_JOINT3": -1.05,
            "RF_JOINT3": -1.05,
            "LB_JOINT3": -1.2,
            "RB_JOINT3": -1.2,
        },
        "joint_names": [
            "RF_JOINT1",
            "RF_JOINT2",
            "RF_JOINT3",
            "LF_JOINT1",
            "LF_JOINT2",
            "LF_JOINT3",
            "RB_JOINT1",
            "RB_JOINT2",
            "RB_JOINT3",
            "LB_JOINT1",
            "LB_JOINT2",
            "LB_JOINT3",
        ],
        # PD
        #"kp": 20.0,
        #"kd": 0.2,
        #"clip_actions": 8.0,
        #"kp": 80.0,
        #"kd": 0.4,
        #"clip_actions": 6.0,
        #"kp": 160.0,
        #"kd": 0.6,
        #"clip_actions": 5.0,
        #"kp": 320.0,
        #"kd": 0.8,
        #"clip_actions": 4.0,
        "kp": 1280.0,
        "kd": 1.6,
        "clip_actions": 2.0,
        #termination
        "termination_if_roll_greater_than":  45,  # degree
        "termination_if_pitch_greater_than": 45,
        # base pose
        "base_init_pos": [0.0, 0.0, 0.515],
        "base_init_quat": [1.0, 0.0, 0.0, 0.0],
        "base_z_noise": [-0.001, 0.001], #
        "base_pitch_noise": [-0.5/180*3.14, 0.5/180*3.14], #
        "base_roll_noise": [-0.5/180*3.14, 0.5/180*3.14], #
        "episode_length_s": 20.0,
        "resampling_time_s": 4.0,
        "action_scale": 1.0,
        "simulate_action_latency": True,
        "dt": 0.01,    ## add by IRSL
        "substeps": 10, ## add by IRSL
        "rotorInertia": 0.1, ## add by IRSL
    }
    obs_cfg = {
        "num_obs": 45,
        "obs_scales": {
            "lin_vel": 2.0,
            "ang_vel": 0.25,
            "dof_pos": 1.0,
            "dof_vel": 0.05,
        },
    }
    reward_cfg = {
        "tracking_sigma": 0.25,
        "base_height_target": 0.4944,
        "feet_height_target": 0.075,
        "reward_scales": {
            "tracking_lin_vel": 4.0, # 1.0
            "tracking_ang_vel": 0.2,
            # "lin_vel_z": -1.0,
            "base_height": -50.0,  # -50.0
            "action_rate": -0.001, # -0.005
            "similar_to_default": -0.4, #-0.1
            "base_rotation_P": -0.1,  # ? ## add by IRSL
            "base_rotation_R": -0.05, # ? ## add by IRSL
            # "effort": -2*1e-6, # ## add by IRSL
            # "episode_len": 1.0, # ## add by IRSL
            "correct_action": 4.0, # ## add by IRSL
            #"joint_position_error": 2.0, # ## add by IRSL
            "plus_watt": 400.0, # ## add by IRSL
        },
    }
    command_cfg = {
        "num_commands": 3,
        "lin_vel_x_range": [0.4, 2.4],
        "lin_vel_y_range": [0, 0],
        "ang_vel_range":   [0, 0],
    }

    return env_cfg, obs_cfg, reward_cfg, command_cfg


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--exp_name", type=str, default="bex24-walking")
    parser.add_argument("-B", "--num_envs", type=int, default=4096)
    parser.add_argument("--max_iterations", type=int, default=101)
    parser.add_argument("--resume", type=str, default=None)
    parser.add_argument("--view", action='store_true')

    args = parser.parse_args()

    gs.init(logging_level="warning")

    log_dir = f"logs/{args.exp_name}"
    env_cfg, obs_cfg, reward_cfg, command_cfg = get_cfgs()
    train_cfg = get_train_cfg(args.exp_name, args.max_iterations)

    ## over-write parmeter here


    ## making directory
    if os.path.exists(log_dir):
        shutil.rmtree(log_dir)
    os.makedirs(log_dir, exist_ok=True)

    if args.resume is not None:
        resume_path = args.resume
        if not os.path.isfile(resume_path):
            raise Exception('file not found {}'.format(resumepath))

    pickle.dump(
        [env_cfg, obs_cfg, reward_cfg, command_cfg, train_cfg],
        open(f"{log_dir}/cfgs.pkl", "wb"),
    )

    env = RL_Env(
        num_envs=args.num_envs,
        env_cfg=env_cfg,
        obs_cfg=obs_cfg,
        reward_cfg=reward_cfg,
        command_cfg=command_cfg,
        dt=env_cfg['dt'],
        substeps=env_cfg['substeps'],
        show_viewer=args.view,
    )

    runner = OnPolicyRunner(env, train_cfg, log_dir, device=gs.device)
    if args.resume is not None:
        runner.load(resume_path)
    runner.learn(num_learning_iterations=args.max_iterations, init_at_random_ep_len=True)

if __name__ == "__main__":
    main()

"""
# training
python examples/locomotion/bex24_train.py
"""
