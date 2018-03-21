import maya.cmds as cmds
    
def shipMove():
    
    ship = "ship"
    lever = "lever_handle"

    maya.cmds.connectAttr(lever+'.rx', ship+'.tz');
    maya.cmds.select(lever);
    
shipMove()

def clawsMove():
    
    push = "push"
    arms = "arms"
    
    maya.cmds.connectAttr(push+'.ty', arms'.tz');
    maya.cmds.select(push);
    
armsMove()

#def Vprint():
   # print("Vanessa")
    
#Vprint()
