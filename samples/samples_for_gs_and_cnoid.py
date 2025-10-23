import sys
sys.executable='/usr/bin/python3'

##
RobotModel.loadModelItem('fake_bex24.urdf') ## should be body fixing joint order

##
gs.init()
scene = gs.Scene(
   sim_options=gs.options.SimOptions(dt=0.01, substeps=2),
   viewer_options=gs.options.ViewerOptions(
       max_FPS=int(0.5 / 0.01),
       camera_pos=(2.0, 0.0, 2.5),
       camera_lookat=(0.0, 0.0, 0.5),
       camera_fov=40,
   ),
   vis_options=gs.options.VisOptions(rendered_envs_idx=list(range(1))),
   rigid_options=gs.options.RigidOptions(
       dt=0.01,
       constraint_solver=gs.constraint_solver.Newton,
       enable_collision=True,
       enable_joint_limit=True,
   ),
   show_viewer=True)

#scene.add_entity(gs.morphs.URDF(file="env.urdf", fixed=True))
scene.add_entity(gs.morphs.URDF(file="urdf/plane/plane.urdf", fixed=True))
grobot = scene.add_entity(gs.morphs.URDF(file="fake_bex24.urdf", pos=np.array([2.0, -1.0, 0.45])))
scene.build()

motors_dof_idx = [ grobot.get_joint(name).dof_start for name in crobot.jointNames ]
