# Changelog

This document lists new features, improvements, changes, and bug fixes in each release of the package.

## Krita Batch Exporter 1.1.1

### Bug fixes

- Fixed errors with export paths in Krita 4.3.0+.
- Fixed missing attribute error when pressing export.

## Krita Batch Exporter 1.1.0

### Features

- Added a `t=` option (trim) for layers. Write `t=false` on any layer to export it at the document's size. This is useful for animation.

### Changes

- Simplified the source code using `pathlib.Path` instead of `os.sep`.

### Bug fixes

- Fixed export with COA tools.

## Krita Batch Exporter 1.0.0

### New features

- Added support for the [Blender Cut-Out Animation tools](https://github.com/ndee85/coa_tools), a Free tool to do modular 2D character animation.
- Added a field to specify the output path for the entire export, instead of having to do it per layer.
- Added support for all color models and spaces.
- Added an auto-install shell script, `install-krita4.2.sh`

### Improvements

- File name prefixes are now only added if you use a transformation like scale or margin.
- Added tool-tips.

### Documentation

- Updated the manual to cover new features.
- Added a detailed install guide to the [README](https://github.com/GDQuest/krita-batch-exporter)
- Removed obsolete content about Pillow and Python installs.

### Changes

- Renamed the addon to Krita Batch Exporter.
- The add-on now uses QImage instead of Pillow, making it much easier to install.

## Krita Batch Exporter 1.0.0 alpha

⚠ This release is for testing purposes. Some features may not work as expected or have bugs. If you find any, please report it in the [issues tab](https://github.com/GDQuest/krita-batch-exporter/issues).

### 📘 Tutorials

Get started with the add-on and the batch export tools: https://youtu.be/jJE5iqE8Q7c

Updated the plugin's built-in documentation. See [Manual.md](https://github.com/GDquest/krita-batch-exporter/blob/master/gdquest_art_tools/Manual.md)

### 🎥🕺 New features

- **COA Tools export** basic support for exporting to coa_tools
  - Export multiple layers to [coa_tools](https://github.com/ndee85/coa_tools) format
- **Batch export all layers in the background** based on metadata in their name
  - Scale images on export
  - Add an empty margin to images
  - Export individual sprites to precise paths, relative or absolute
  - Export multiple copies of a layer
- **Smart batch rename tool** with search and replace to add metadata to many layers at once
- **Export all selected layers**
  - The structure of the export folder follows your layer stack
