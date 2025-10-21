import argparse
import os
import pickle

from importlib import metadata
import torch
try:
    try:
        if metadata.version("rsl-rl"):
            raise ImportError
    except metadata.PackageNotFoundError:
        if metadata.version("rsl-rl-lib") != "2.2.4":
            raise ImportError
except (metadata.PackageNotFoundError, ImportError) as e:
    raise ImportError("Please uninstall 'rsl_rl' and install 'rsl-rl-lib==2.2.4'.") from e
from rsl_rl.runners import OnPolicyRunner

from bex24_env_cnoid import Bex24Env as RLEnv

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--exp_name", type=str, default="bex24-walking")
    parser.add_argument("--ckpt", type=int, default=100)
    args = parser.parse_args()

    log_dir = f"logs/{args.exp_name}"
    env_cfg, obs_cfg, reward_cfg, command_cfg, train_cfg = pickle.load(open(f"logs/{args.exp_name}/cfgs.pkl", "rb"))
    reward_cfg["reward_scales"] = {}

    ## override
    env_cfg["episode_length_s"] = 40.0
    command_cfg["lin_vel_x_range"] = [1.0, 1.0]

    if not 'dt' in env_cfg:
        env_cfg['dt'] = 0.01
    if not 'substeps' in env_cfg:
        env_cfg['substeps'] = 4

    env = RLEnv(
        num_envs=1,
        env_cfg=env_cfg,
        obs_cfg=obs_cfg,
        reward_cfg=reward_cfg,
        command_cfg=command_cfg,
        dt=env_cfg['dt'],
        substeps=env_cfg['substeps'],
        show_viewer=True,
    )

    runner = OnPolicyRunner(env, train_cfg, log_dir, device='cuda')
    resume_path = os.path.join(log_dir, f"model_{args.ckpt}.pt")
    runner.load(resume_path)
    policy = runner.get_inference_policy(device='cuda')

    return env, policy

def eval_policy(env, policy):
    obs, _ = env.reset()
    with torch.no_grad():
        while True:
            actions = policy(obs)
            obs, rews, dones, infos = env.step(actions)

if __name__ == "__main__":
    env, policy = main()
    eval_policy(env, policy)

"""
# evaluation
python examples/locomotion/bex24_eval.py -e bex24-walking -v --ckpt 100
"""
