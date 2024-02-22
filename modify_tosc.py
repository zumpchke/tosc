import tosclib as tosc
from pprint import pprint
import json
import sys

GROUP_WIDTH = 368
GROUP_HEIGHT = 504

from tosclib.elements import ControlElements, ControlType, Value

groups = {}

def oscMsg() -> tosc.OSC:
    """Create a message with a path constructed with custom Partials"""
    return tosc.OSC(
            path=[
                tosc.Partial(),  # Default is the constant '/'
                tosc.Partial(type="PROPERTY", value="parent.name"),
                tosc.Partial(),
                tosc.Partial(type="PROPERTY", value="name"),
                ]
            )


def getEffectSettings(parent, result):
    for p in parent.children:
        p = tosc.ElementTOSC(p)
        name = p.getName()
        if name == 'effect_settings':
            result[0] = p

        getEffectSettings(p, result)




def work(parent):
    for p in parent.children:
        p = tosc.ElementTOSC(p)
        name = p.getName()
        propW = tosc.Property("s", "origWidth", "%f" % p.getW())
        propH = tosc.Property("s", "origHeight", "%f" % p.getH())
        try:
            p.createProperty(propW)
            p.createProperty(propH)
        except ValueError:
            pass

        if name != 'projector_settings':
            print(name)
            if 'proj' in name:
                prop_flipx = tosc.Property("i", "flipx", "0")
                prop_flipy = tosc.Property("i", "flipy", "0")
                prop_rot = tosc.Property("f", "rot", "0")
                prop_scale = tosc.Property("f", "scale", "0.5")
                prop_xpos = tosc.Property("f", "xpos", "0.5")
                prop_ypos = tosc.Property("f", "ypos", "0.5")

                try:
                    p.createProperty(prop_flipx)
                    p.createProperty(prop_flipy)
                    p.createProperty(prop_rot)
                    p.createProperty(prop_scale)
                    p.createProperty(prop_xpos)
                    p.createProperty(prop_ypos)
                except ValueError:
                    pass

        work(p)


#work(parent)
#tosc.write(root, "uzay_id2.tosc")

def createControl(parent, i, height, info):
    frame = parent.getFrame()
    print(frame)
    control_type = None
    if info['style'] == 'Toggle':
        control_type = ControlType.BUTTON
    elif info['style'] == 'Float':
        control_type = ControlType.FADER
    else:
        assert(False)


    # Create control
    control = tosc.ElementTOSC(parent.createChild(control_type))
    t = tosc.Property("s", "buttonType", "1")
    t1 = tosc.Property("s", "orientation", "1")
    t2 = tosc.Property("s", "centered", "1")
    control.setName(info['name'].lower())
    control.createProperty(t)
    control.createProperty(t1)
    if info['default'] == 0.5:
        control.createProperty(t2)
        control.createValue(Value(key="x", default="%f" % info['default']))
    control.setColor([1, 0, 0, 1])
    control.setFrame([0, height*i, frame[2], height])
    msg = oscMsg()
    control.createOSC(message=msg)


    # Create Label
    label = tosc.ElementTOSC(parent.createChild(ControlType.LABEL))
    label.createValue(Value(key="text", default=info['name']))
    p1 = tosc.Property("s", "interactive", "0")
    p2 = tosc.Property("s", "background", "0")
    label.createProperty(p1)
    label.createProperty(p2)
    label.setName('label_' + info['name'])
    label.setFrame([0, height*i, frame[2], height])



def createGroup(parent, key, pars):
    print(dir(parent))
    print(parent.getFrame())
    frame = parent.getFrame()

    index = pars[key]['index']
    group = tosc.ElementTOSC(parent.createChild(ControlType.GROUP))
    group.setName("settings_%d" % (index))
    group.setFrame([0, 0, frame[2], frame[3]])
    group.setColor((0.25, 0.25, 0.25, 1))
    _visible = tosc.Property("s", "visible", "0")
    group.createProperty(_visible)
    num_pars = len(pars[key]['Custom'])
    height = int(parent.getH() / num_pars)
    for i, par in enumerate(pars[key]['Custom']):
        createControl(group, i, height, pars[key]['Custom'][par])




if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        pars = json.loads(f.read())
        pprint(pars)

    root = tosc.load("uzay_id2.tosc");
    parent = tosc.ElementTOSC(root[0])
    settings = [None]
    getEffectSettings(parent, settings)

    for key in pars:
        createGroup(settings[0], key, pars)

    tosc.write(root, "test.tosc")




