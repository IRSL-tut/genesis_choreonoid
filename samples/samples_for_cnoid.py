## jupyter console --kernel=choreonoid
exec(open('/choreonoid_ws/install/share/irsl_choreonoid/sample/irsl_import.py').read())

import sys
sys.argv.append('-e')
sys.argv.append('bex24_P1280b')
sys.argv.append('--ckpt=15000')


__name__ = 'hoge'
exec(open('bex24_eval_cnoid.py').read())
env, policy = main()

## overwrite configuration here
env.command_cfg['lin_vel_x_range'] = [1.4, 1.4]
env.env_cfg['rotorInertia'] = 0.1
#env.env_cfg['dt'] = 0.14
#env.env_cfg['substeps'] = 14

obs, _ = env.reset()
obs = torch.tensor([[.0]*45], device=env.device, dtype=torch.float32) ## zero reset ## TODO: should be checked

## do simulation by 1step
with torch.no_grad():
    actions = policy(obs)
    obs, rews, dones, infos = env.step(actions)

## do simulation. you can stop simulation by pressing stop button in choreonoid
while env.sim.isRunning():
    with torch.no_grad():
        actions = policy(obs)
        obs, rews, dones, infos = env.step(actions)
