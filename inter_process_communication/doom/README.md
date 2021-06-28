# Play the classic Doom game through HDF5

## Description

No project is a serious project unless it runs Doom.

This example uses a [modified version of an open source Doom game engine](
https://github.com/lucasvr/chocolate-doom) that exports the game display
through a System V shared memory segment.
 
Each time the dataset is read, the user-defined function attaches to that
shared memory segment and retrieves the framebuffer and the game palette.
It then encodes that data as a regular bi-dimensional HDF5 dataset which
can be printed using regular tools.

## Data preparation

First, download and install the modified Doom game engine. Next, compile the
UDF and attach it to an existing HDF5 file (in this example, `doom.h5`)  with:

```
hdf5-udf doom.h5 doom.cpp Framebuffer:320x200:uint8 Palette:7680:uint8
```

## Data consumption

Open a new window and launch the Doom executable. Wait until the game starts
and then launch the [readh5 utility](https://github.com/lucasvr/hdf5-udf/blob/default/examples/readh5.cpp)
in a loop so that the game video frames are contiguously shown as you play it.

```
xterm -bg black -fa 'Monospace' -fs 2 -geometry 640x200 -e 'while true; do readh5 doom.h5 Framebuffer Palette; clear; done'
```

![](screenshot.jpg)
