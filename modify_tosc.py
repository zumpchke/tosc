import tosclib as tosc
from pprint import pprint
import json
import sys

GROUP_WIDTH = 368
GROUP_HEIGHT = 504


def getEffectSettings(parent):
    for p in parent.children:
        p = tosc.ElementTOSC(p)
        name = p.getName()
        if name == 'effect_settings':
            return p
        return None

    return getEffectSettings(p)

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

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        pars = json.loads(f.read())
        pprint(pars)

    root = tosc.load("uzay_id2.tosc");
    parent = tosc.ElementTOSC(root[0])
    settings = getEffectSettings(parent)
    print(settings)



