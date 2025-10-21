## testing eval in choreonoid

## jupyter console --kernel=choreonoid
exec(open('/choreonoid_ws/install/share/irsl_choreonoid/sample/irsl_import.py').read())

import sys
sys.argv.append('-e')
sys.argv.append('bex24_P0320')
sys.argv.append('--ckpt=1000')
#sys.argv.append('-e')
#sys.argv.append('bex24_P0080')
#sys.argv.append('--ckpt=800')
#sys.argv.append('-e')
#sys.argv.append('bex24_P0160')
#sys.argv.append('--ckpt=2700')

__name__ = 'hoge'
exec(open('bex24_eval_cnoid.py').read())
env, policy = main()

### over-write parameter here
env.env_cfg['kp'] = 7.0 ## 28.0
env.env_cfg['kd'] = 2.0 ## 0.2
env.env_cfg['rotorInertia'] = 0.2

obs, _ = env.reset()
obs = torch.tensor([[.0]*45], device=env.device, dtype=torch.float32)
while env.sim.isRunning():
    with torch.no_grad():
        actions = policy(obs)
        obs, rews, dones, infos = env.step(actions)

## testing eval in genesys
# ipython
%autoindent

import sys
sys.argv.append('-e')
sys.argv.append('bex24_P0160')
sys.argv.append('--ckpt=2700')

__name__ = 'hoge'
exec(open('bex24_eval_gs.py').read())
env, policy = main()

obs, _ = env.reset()
with torch.no_grad():
    print("obs<:", obs)
    actions = policy(obs)
    print("act:", actions)
    obs, rews, dones, infos = env.step(actions)
    print("obs>:", obs)

for nm in dir(env):
   if '_reward' in nm:
       f=getattr(env, nm)
       print(nm, f())
