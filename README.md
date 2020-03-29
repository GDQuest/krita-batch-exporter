# Krita Batch Exporter

![Plugin banner image](./img/krita-batch-exporter-banner.svg)

Export your game assets, sprites, designs, and more with speed and flexibility!

This Free Krita 4 add-on is a tool to help designers, game artists, and digital artists to work more productively.

Batch Exporter brings smart batch layer export and renaming. With it, you can **automatically re-export** groups and layers to specific folders, **scale images on export**, and more! All that using Krita 4's new background save. If you've ever used Photoshop's Generator feature, this is similar.

![Plugin demo](https://raw.githubusercontent.com/GDquest/krita-batch-exporter/master/img/krita-art-tools-example.jpg)

Our goal is to extend and enhance powerful but underused features that already exist in Krita to empower artists.

## How to Use and video demo

You can find a [video intro and tutorial](https://youtu.be/jJE5iqE8Q7c) on our YouTube channel.

The plugin also comes with [text-based](https://github.com/GDquest/krita-batch-exporter/blob/master/krita_batch_exporter/Manual.md) documentation.

## How to install

Due to limitations in Krita, the plugin needs Python 3 and a specific version of the Pillow image library installed alongside it to use all its features.

### Using the auto-install script

_This install program needs testing. Please report any bug you find in [the issues tab](https://github.com/GDQuest/krita-batch-exporter/issues/new)._

You can run the install script `./install-krita4.2.sh` from your terminal. On Windows, you must run this program from a bash shell. If you have git installed, you can use git bash, otherwise the Windows Subsystem for Linux.

```sh
chmod +x install-krita4.2.sh # Make the program executable
./install-krita4.2.sh
```

It should install all the files you need for the add-on to work in Krita 4.2.x. It can also upgrade the add-on if you want to install a new release.

### Manual installation

To install the add-on manually, you need to:

1. Download the "Source code (zip)" file in the [latest release](https://github.com/GDQuest/krita-batch-exporter/releases)
1. Open Krita and go to the Settings menu -> Manage Resources
1. Click "Open Resources Folder" to access your Krita resources directory
1. Copy and paste the "krita_batch_exporter" folder in the `pykrita/` directory

Then, you currently need a version of the Pillow image library that depends on your operating system and the version of Python built into Krita.

#### Installing Pillow

_Note: Pillow and the add-on should come built-into future versions of Krita. We need help from a developer to add support for Windows. For more information, see our [pull request](https://invent.kde.org/kde/krita/-/merge_requests/116)._

For that, you need to use the command line and have Python 3 and its package manager pip installed. If that's not the case, see the guide below.

The add-on will try to find Pillow in a folder named `Dependencies/` inside `krita_batch_exporter/`.

You can find the Pillow installer files here: https://pypi.org/project/Pillow/#files

The file names have the supported version of Python in the form `cp35`, meaning "C Python 3.5". These at the files we need for Krita 4.2.x. You then need to pick the one that corresponds to your OS. For instance, for me, it is `Pillow-7.0.0-cp35-cp35m-manylinux1_x86_64.whl`.

From there, here are the steps to finish installing the add-on:

1. Right-click on the Pillow install file in your web browser and select "Copy the link's address" or a similar option.
2. Open your terminal inside the `krita_batch_exporter/` folder.
3. Run the command `python3 -m pip install --target Dependencies/ -- $link_to_pillow_install_file`

Replace `$link_to_pillow_install_file` with the link you copied in the first step.

### Activating the add-on

To activate the add-on:

1. Restart Krita.
2. Go to the Settings menu -> Configure Krita -> Python Plugin Manager.
3. Click the checkbox next to GDQuest Batch Exporter.

You are now ready to use it!

### Python 3, pip, and Pillow

If you don't have Python 3 installed, download the executable on https://www.python.org/downloads/ and run the installer.

If you use Linux, you most likely have Python 3 installed already. If not, in most distributions, you can install both Python 3 and its package manager pip by running a command in your shell.

If you use Ubuntu or a Debian-based distribution, write `sudo apt install python3 python3-pip` in your terminal. Here is a more detailed Python install guide for Linux users: https://docs.python-guide.org/starting/install3/linux/

## Follow us, Support our work

Krita Batch Exporter is a GDQuest project. Our mission is to bring people together to become better game developers, all that using and contributing to Free Software.

This add-on's development is funded by our [game creation courses for Godot](https://gdquest.mavenseed.com/). Consider getting one to support our work!

We make Free tutorials and tools to learn game creation. You can find us on:

- [Our YouTube channel](https://www.youtube.com/c/gdquest/)
- [Twitter](https://twitter.com/NathanGDquest)

We also have a [Discord community](https://discord.gg/CHYVgar)!
