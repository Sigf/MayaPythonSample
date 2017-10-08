import maya.cmds as mc
import pymel.core as pm
from ..utils.generic import undo

def freezeTransforms():
    mc.makeIdentity(apply = True, t=1, r=1, s=1, n=0, pn=1)

def centerPivot():
    mc.xform(cpc = True)

def clearHistory():
    mc.delete(ch = True)

@undo
def createQuadArrow():
    mc.curve(d=1, p=[(-1,0,-1),
    (-1,0,-3),
    (-2,0,-3),
    (0,0,-5),
    (2, 0, -3),
    (1, 0, -3),
    (1, 0, -1),
    (3, 0, -1),
    (3, 0, -2),
    (5, 0, 0),
    (3, 0, 2),
    (3, 0, 1),
    (1, 0, 1),
    (1, 0, 3),
    (2, 0, 3),
    (2, 0, 3),
    (0, 0, 5),
    (-2, 0, 3),
    (-1, 0, 3),
    (-1, 0, 1),
    (-3, 0, 1),
    (-3, 0, 2),
    (-5, 0, 0),
    (-3, 0, -2),
    (-3, 0, -1),
    (-1, 0, -1)])

@undo
def createJointsOnCurve(steps):
    selectedCurve = pm.ls(sl=True)
    for t in range(0,steps):
        newJoint = pm.joint(p=(0,0,0))
        pm.pathAnimation(newJoint, c=selectedCurve[0], su=(2/steps)*t)

@undo
def setPivotToCenter():
    selectedObjects = mc.ls(tr=True, s=False, sl=True)

    for obj in selectedObjects:
        mc.move(0, 0, 0, obj+".scalePivot", obj+".rotatePivot", absolute=True)

@undo
def mirrorDuplicate(axis):
    clone = mc.duplicate(rr = True)
    tempGroup = mc.group(clone)

    mc.select(cl = True)
    mc.select(tempGroup)

    setPivotToCenter()

    if axis is 0:
        mc.setAttr(tempGroup+".scaleX", -1)

    if axis is 1:
        mc.setAttr(tempGroup+".scaleY", -1)

    if axis is 2:
        mc.setAttr(tempGroup+".scaleZ", -1)

    mc.parent(clone, w=True)
    mc.delete(tempGroup)
    freezeTransforms()
