import os
import json

from functools import partial
from .Infrastructure import WNode
from .Utils import kickstart, flip
from .Utils.Tree import iterPre

from krita import Krita
from PIL import Image, ImageOps

class COAToolsFormat:
    def __init__(self, cfg, statusBar):
        self.cfg = cfg
        self.statusBar = statusBar
        self.reset()

    def reset(self):
        self.nodes = []

    def showError(self, msg):
        msg, timeout = self.cfg['error']['msg'].format(msg), cfg['error']['timeout']
        self.statusBar.showMessage(msg, timeout)

    def collect(self, node):
        print("COAToolsFormat collecting %s" % ( node.name ) )
        self.nodes.append(node)

    def remap(self, oldValue, oldMin, oldMax, newMin, newMax):
        if oldMin == newMin and oldMax == newMax:
            return oldValue;
        return (((oldValue - oldMin) * (newMax - newMin)) / (oldMax - oldMin)) + newMin;

    def save(self, output_dir=''):
        # For each top-level node (Group Layer)
        cfg = self.cfg
        for wn in self.nodes:
            meta = wn.meta
            children = wn.children

            os.makedirs(output_dir, exist_ok=True)
            print("COAToolsFormat exporting %d items from %s" % ( len(children), wn.name ) )

            # TODO handle c=sheet cases from `meta['c']` and generate multi-sprite bitmaps for 'switch layers' as the GIMP exporter does
            # if meta['c'] == "sheet":
            #   self.generateSpritesheet(wn)

            try:
                if len(children) <= 0:
                    raise ValueError(wn.name,'has no children to export')

                coa_data = { 'name': wn.name, 'nodes': [] }
                print("COAToolsFormat exporting %s meta: (%s) to %s" % ( wn.name, meta['c'], output_dir ) )
                for idx, child in enumerate(children):
                    fn = child.save(output_dir)

                    node = child.node
                    coords = node.bounds().getCoords()
                    relative_coords = coords

                    parent_node = node.parentNode()
                    parent_coords = parent_node.bounds().getCoords()
                    relative_coords = [coords[0]-parent_coords[0],coords[1]-parent_coords[1]]

                    p_width = parent_coords[2]-parent_coords[0]
                    p_height = parent_coords[3]-parent_coords[1]
                    coa_entry = {
                        "children": [],
                        "frame_index": 0,
                        "name": child.name,
                        "node_path": child.name,
                        "offset": [ -p_width/2, p_height/2 ],
                        "opacity": self.remap(node.opacity(),0,255,0,1),
                        "pivot_offset": [ 0.0, 0.0 ],
                        "position": relative_coords,
                        "resource_path": fn.replace(output_dir+os.path.sep+cfg['outDir']+os.path.sep,''),
                        "rotation": 0.0,
                        "scale": [ 1.0, 1.0 ],
                        "tiles_x": 1,
                        "tiles_y": 1,
                        "type": "SPRITE",
                        "z": idx-len(children)+1
                        }
                    coa_data['nodes'].append(coa_entry)

                json_data = json.dumps(coa_data, sort_keys=True, indent=4, separators=(',', ': '))
                with open(output_dir+os.path.sep+cfg['outDir']+os.path.sep+wn.name+".json", "w") as fh:
                    fh.write(json_data)
            except ValueError as e:
                showError(e)
