import maya.OpenMaya as om
import maya.cmds as cmds
import random, time

def arPolyNoise(geoObject, maxDisplacement):
    """Apply noise to the supplied geometry object using the supplied max displacement."""
    # get the dag path for the shapeNode using an API selection list
    selection = om.MSelectionList()
    dagPath = om.MDagPath()
    try:
        selection.add(geoObject)
        selection.getDagPath(0, dagPath)
    except: raise
    # apply noise to the shape's points
    try:        
        # initialize a geometry iterator
        geoIter = om.MItGeometry(dagPath)
        # get the positions of all the vertices in world space
        pArray = om.MPointArray()
        geoIter.allPositions(pArray)
        # displace each of the vertices
        for i in xrange(pArray.length()):
            displacement = om.MVector.one * random.random() * maxDisplacement
            pArray[i].x += displacement.x
            pArray[i].y += displacement.y
            pArray[i].z += displacement.z
        # update the surface of the geometry with the changes
        geoIter.setAllPositions(pArray)
        meshFn = om.MFnMesh(dagPath)
        meshFn.updateSurface()
    except: raise

def create_car(name, length=2, width=1):
    # Create the car components
    body = create_body(length, width)
    tires = create_tires(length, width)
    
    # Group the car components
    final_name = assemble_car(name, body, tires)
    
    # Clear any selections in the scene
    cmds.select(clear=True)
    
    return final_name
    
def create_body(length=2, width=1):
    # Create a plane that represents the car body.
    # Return the transform node name.
    body = cmds.polyPlane(w=length, h=width, name="body")
    arPolyNoise(body[0], 0.02)
    return body[0]
    
def create_tires(body_length, body_width):
    # Create four tires for the car.
    # Size and position are relative to the body dimensions.
    tire_width = 0.25 * body_width
    tire_radius = 0.25 * body_length
    x_pos = 0.5 * body_length
    z_pos = 0.5 * body_width + 0.5 * tire_width
    
    fl_tire = create_tire("front_left_tire", tire_width, tire_radius, x_pos, 0, -z_pos)
    fr_tire = create_tire("front_right_tire", tire_width, tire_radius, x_pos, 0, z_pos)
    rl_tire = create_tire("rear_left_tire", tire_width, tire_radius, -x_pos, 0, -z_pos)
    rr_tire = create_tire("rear_right_tire", tire_width, tire_radius, -x_pos, 0, z_pos)
    
    return [fl_tire, fr_tire, rl_tire, rr_tire]
    
def create_tire(name, width, radius, tx, ty, tz):
    # Create a cylinder that represents a tire.
    # Return the transform node name.
    tire = cmds.polyCylinder(h=width, r=radius, ax=(0,0,1), sc=True, name=name)
    cmds.setAttr("{0}.translate".format(tire[0]), tx, ty, tz)
    arPolyNoise(tire[0], 0.02)
    return tire[0]
    
def assemble_car(name, body, tires):
    # Create groups for the body and tires and parent them
    # under the main car group.
    # Return the car group name.
    body_grp = cmds.group(body, name="body_grp")
    tires_grp = cmds.group(tires, name="tires_grp")
    
    car_grp = cmds.group(body_grp, tires_grp, name=name)
    return car_grp
    
if __name__ == "__main__":
    name = create_car("test_car")
    print("Car created: {0}".format(name))
    



# start the timer and add the noise
#timeStart = time.clock()
# create a sphere and add noise
#sphere = cmds.polySphere(radius=1, subdivisionsX=200, subdivisionsY=200)
#arPolyNoise(sphere[0], 0.02)
# stop the timer
#timeStop = time.clock()
#print('Execution time: %s seconds.'%(timeStop-timeStart))




