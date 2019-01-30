# GDquest Art Tools: Krita Plugin for Game Developers and Graphic Designers

Free Krita plugin for designers, game artists and digital artists to work more
productively:

- Batch export assets to multiple sizes, file types, and custom paths. Supports
  `jpg` and `png`.
- Rename layers quickly with the smart rename tool

## Batch Export Layers

GDquest Art Tools exports individual layers to image files based on metadata in
the layer name. The supported options are:

- `[e=jpg,png]` - supported export image extensions
- `[s=20,50,100,150]` - size in `%`
- `[p=path/to/custom/export/directory]` - custom output path.
    Paths can be absolute or relative to the Krita document.
- `[m=20,30,100]` - extra margin in `px`. The layer is trimmed to the
  smallest bounding box by default. This option adds extra padding around the
  layer.

A typical layer name with metadata looks like: `CharacterTorso e=png m=30
s=50,100`. This exports the layer as two images, with an added padding of 30 pixels
on each side: `CharacterTorso_s100_m030.png`, and `CharacterTorso_s050_m030.png`,
a copy of the layer scaled down to half the original size.

All the metadata tags are optional. Each tag can contain one or multiple options
separated by comma `,`. Write `e=jpg` to export the layer to `jpg` only and
`e=jpg,png` to export the layer twice, as a `jpg` and as a `png` file. Note that
the other tag, `p=` has been left out. Below we describe how the plugin works.

## Getting Started

GDquest Art Tools gives two options to batch export layers: `Export All Layers`
or `Export Selected Layers`.

`Export All Layers` only takes layers with the `e=extension[s]` tag into
account. For example, if the layer name is `LeftArm e=png s=50,100`, `Export All
Layers` will take it into account. If the layer name is `LeftArm s=50,100`, it
will not be exported with this option.

`Export Selected Layers` exports all selected layers regardless of the tags.

By default, the plugin exports the images in an `export` folder next to your
Krita document. The export follows the structure of your layer stack. The group
layers become directories and other layers export as files.

> **Supported layer types:** paint, vector, group & file layers.

## Smart Layer Rename tool

Say we have this Krita document structure:

```
GodetteGroupLayer
  +-- HeadGroupLayer
    +-- Hair
    +-- Eyes
    +-- Rest
  +-- Torso
  +-- LeftArm
  +-- RightArm
Background
```

If you want to export `GodetteGroupLayer`, `HeadGroupLayer`, `Torso`, `LeftArm`,
and `RightArm`, but not the other layers, you can select these layers and write
the following in the `Update Layer Name` text box: `e=png s=40,100` and press
<kbd>Enter</kbd>. In this example, Art Tools will export two copies of the
selected layers to png at `40%` and `100%` scale. This is what `s=40,100` does.

Say that we made a mistake: we want to export to `50%` instead of `40%`. Select
the layers once more and write `s=50,100` in the text box. Press
<kbd>Enter</kbd>. This will update the size tag and leave `e=png` untouched.

The tool can do more than add and update meta tags. If you want to remove
`GroupLayer` from the name on `GodetteGroupLayer` and `HeadGroupLayer`, select them
and write `GroupLayer=` in the text box. Press <kbd>Enter</kbd> and the
`GroupLayer` text will disappear from the selected layers.

The `=` tells the tool to search and replace. `this=[that]` will replace `this`
with `[that]`. If you don't write anything after the equal sign, the tool will
erase the text you searched for.

The rename tool is smarter with meta tags. Writing `e=` will remove the
extension tag entirely. For example, `Godete e=png s=50,100` will become
`Godette s=50,100`.
