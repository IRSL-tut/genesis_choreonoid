import random
exec(open('/choreonoid_ws/install/share/irsl_choreonoid/sample/irsl_import.py').read())

def makeSimpleHeightRange(filename, iteration=80, size=0.5, width=40.0, depth=2.0, initialX=4, heightRange=(-0.1, 0.1),
                          **kwargs):
    rb=RobotBuilder()

    ## initial plane
    bx=rb.makeBox(x=initialX, y=width, z=depth, color=[0.7, 0.7, 0.7])
    bx.translate(fv(-0.5*initialX + size, 0, -0.5*depth))
    h0 = heightRange[0]
    hr = heightRange[1] - heightRange[0]
    cntr = 1
    for i in range(80):
        bx=rb.makeBox(x=size, y=width, z=depth, color=[0.5, 0.5 + (cntr%2)*0.3, 0.5 + (cntr%2)*0.3])
        bx.translate(fv(0.5*size + cntr*size, 0, -0.5*depth + hr*random.random() + h0))
        cntr = cntr + 1

    rb.createLinkFromShape(name='Root', root=True, density=2000.0)
    rb.exportURDF(filename, **kwargs)
    return rb

def makeRandomBox(filename, initialX=4, size=(0.5, 0.5), xIteration=40, yIteration=40, depth=2.0,
                  rotateRangeR=(-0.25, 0.25), rotateRangeP=(-0.25, 0.25), heightRange=(-0.04, 0.04), **kwargs):
    rb=RobotBuilder()
    #
    xres = size[0]
    yres = size[1]
    #
    rangeP0 = rotateRangeP[0]
    rangePr = rotateRangeP[1] - rotateRangeP[0]
    rangeR0 = rotateRangeR[0]
    rangeRr = rotateRangeR[1] - rotateRangeR[0]
    h0 = heightRange[0]
    hr = heightRange[1] - heightRange[0]
    #
    width = yIteration*yres
    #
    bx=rb.makeBox(x=initialX, y=width, z=depth, color=[0.7, 0.7, 0.7])
    bx.translate(fv(-0.5*initialX + xres, 0, -0.5*depth))
    # v_offset = fv(-width/2 , xres * 1.5, 0)
    for x in range(xIteration):
        for y in range(yIteration):
            bx=rb.makeBox(x=xres, y=yres, z=depth)
            cds=coordinates(fv(x*xres, y*yres, 0))
            cds.rotate(rangeR0 + rangeRr*random.random(), coordinates.X)
            cds.rotate(rangeP0 + rangePr*random.random(), coordinates.Y)
            cds.transform(coordinates(fv(0, 0, -0.5*depth)))
            cds.translate(fv(xres*1.5, yres*0.5 - width/2, hr*random.random() + h0), wrt=coordinates.wrt.world)
            bx.newcoords(cds)
    #
    rb.createLinkFromShape(name='Root', root=True, density=2000.0)
    rb.exportURDF(filename, **kwargs)
    return rb
