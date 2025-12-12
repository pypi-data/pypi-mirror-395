Installing Nx5d
===============

Windows, Mac or Linux?
----------------------

Nx5d is developed under Linux.

But there's nothing that *specifically and necessarily* binds Nx5d to
Linux except that Linux is the main operation system of the core
developers, and therefore Nx5d hasn't been sufficiently tested
under Windows or MacOS. Consequently, you're very, very likely
to run into minor problems if you decide to use something else
than Linux.

We're very happy to accept patches on how to fix issues you
may encounter. And to help you understand Nx5d internals well
enough to be able to do that.

As to continuously maintaining Windows or MacOS version: our
forces are spread very thin as it is, so this is likely to not
become a pripority, unless who uses either of those systems
on a daily basis decides to join our ranks -- a circumstance
we'd be very excited about :-)


Via Container
-------------

For our own purposes, we automatically package and build a Jupyter Server
contianer image which contains Nx5d, as well as our X-ray diffraction
processing recipes.

(We prefer using [Podman](https://podman.io) over Docker because it is a
more advanced, yet more lightweight interface to Linux's container
capabilities. But Podman and Docker are command-line compatible, so you
can simply swap `podman` for `docker` in the following if the latter is
more up your alley. Also, if you're running this in Windows or Mac, you
likely don't have a choice but to use Docker, since Podman is only available
for native Linux hosts.)

This is how you spin up a Jupyter Server based on the "semi-official" 
Nx5d image:

```
podman run -ti --rm --pull=always \
           --volume /home/data/repository:/var/repo:z \
           --env NX5D_DATA_REPO=/var/repo/{proposal}/data.hdf5#{scan} \
		   registry.gitlab.com/kmc3-xpp/ops/jhub-image
```

What we've done here is the following:
- use `-ti` and `--rm` for a more terminal-friendly experience (you
  will get to see the output, and you can shoot down the Jupyter server
  using Ctrl+C)
- use `--pull=always` to make sure that the container
  image used is always up-to-date
- assumed that the data you're working with is in your `/home/data/repo`
  folder on your host machine, that every proposal has its subfolder
  with a file named `data.h5` inside which contains your data scans
  and your spice
- set the environment variable `NX5D_DATA_REPO` so that Nx5d knows
  finds your data.

Did I mention that this is our preferred method of usage? ;-)

The details of how to organize repositories and how to set environment
variables are beyond the scope of this installation guide. You'll
find plenty of information in the [API guide](./api-guide.md) or in
the [real-life examples](./examples.md) section.

Natively From PyPI Or Git-Sources
---------------------------------

### From PyPI

You can install and use Nx5d in a Python environment of your choosing,
and follow most of the examples of this tutorial, directly from PyPI:

```
pip install nx5d
```

We try not to break the PyPI version and keep it as stable as possible,
but remember that Nx5d's is still very much work-in-progress. Expect
things to go awry at times.

### From GitLab

The official Git repository is at [GitLab](https://gitlab.com/kmc3-xpp/nx5d).
The PyPI version has a stronger focus on API stability and therefore lacks
a bit behind the bleeding-edge developments. 
If you want to use the latest code, or want to help, you can check out
the official codebase and install as editable:

```
git clone https://gitlab.com/kmc3-xpp/nx5d
pip install -e ./nx5d[test]
```

### How To Work

Frankly, this is up to you -- you can spin up your own Jupyter Server
or Jupyter Lab instance; or you can use Nx5d directly from a suitable
IPython shell; or you can write code using your favourite editor or IDE,
e.g. Spyder.

Be sure to define the necessary environment variables, e.g. assuming that
your data is under `/home/data/repo`, something like this might be in order:

```
export NX5D_DATA_REPO=/home/data/repo/{proposal}/data.h5#{scan}
```
