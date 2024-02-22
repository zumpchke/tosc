import tosclib as tosc

root = tosc.load("uzay_id2.tosc");

parent = tosc.ElementTOSC(root[0])

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

        if 'proj' in name:
            print(name)
        work(p)


work(parent)

tosc.write(root, "uzay_id2.tosc")
