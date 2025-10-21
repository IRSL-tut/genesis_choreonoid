rb=RobotBuilder()

cntr = 1
bx=rb.makeBox(x=10, y=40, z=2.0, color=[0.7, 0.7, 0.7])
bx.translate(fv(-5 + 0.5, 0, -1.0))

for i in range(80):
    bx=rb.makeBox(x=0.5, y=40, z=2.0, color=[0.5, 0.5 + (cntr%2)*0.3, 0.5 + (cntr%2)*0.3])
    bx.translate(fv(0.25 + cntr*0.5, 0, -1.0 + 0.1*(random.random() - 0.5)))
    cntr = cntr + 1

rb.createLinkFromShape(name='Root', root=True, density=2000.0)

rb.exportURDF('env.urdf')


