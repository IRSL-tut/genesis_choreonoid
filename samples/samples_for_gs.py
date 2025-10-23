# ipython
%autoindent

import sys
sys.argv.append('-e')
sys.argv.append('bex24_P1280b')
sys.argv.append('--ckpt=19999')

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

# calc reward
for nm in dir(env):
   if '_reward' in nm:
       f=getattr(env, nm)
       print(nm, f())
