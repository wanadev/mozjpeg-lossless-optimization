MozJPEG Lossless Optimization
=============================

|Github| |Discord| |PYPI Version| |Build Status| |Black| |License|

This library optimizes JPEGs losslessly using MozJPEG_.

To reduce the file sizes,

* the Huffman table of the JPEGs is optimized,
* the baseline JPEGs are converted to progressive JPEGs,
* and any metadata and ICC profiles are removed.

The JPEGs optimized with this library are identical to what you get using the
``jpegtran`` tool from MozJPEG with the ``-optimize``, ``-progressive`` and
``-copy none`` options.


.. _MozJPEG: https://github.com/mozilla/mozjpeg


Usage
-----

Optimizing (losslessly) a JPEG:

.. code-block:: python

   import mozjpeg_lossless_optimization

   with open("./image.jpg", "rb") as input_jpeg_file:
       input_jpeg_bytes = input_jpeg_file.read()

   output_jpeg_bytes = mozjpeg_lossless_optimization.optimize(input_jpeg_bytes)

   with open("./out.jpg", "wb") as output_jpeg_file:
       output_jpeg_file.write(output_jpeg_bytes)

To preserve image metadata, you can set the ``copy`` parameter to
``mozjpeg_lossless_optimization.COPY_MARKERS.ALL``:

.. code-block:: python

   output_jpeg_bytes = mozjpeg_lossless_optimization.optimize(
       input_jpeg_bytes,
       copy=mozjpeg_lossless_optimization.COPY_MARKERS.ALL,
   )

Possible values for the ``copy`` parameter:

* ``COPY_MARKERS.NONE``: copy no optional markers (default),
* ``COPY_MARKERS.COMMENTS``: copy only comment (COM) markers,
* ``COPY_MARKERS.ALL``: copy all optional markers,
* ``COPY_MARKERS.ALL_EXCEPT_ICC``: copy all optional markers except APP2,
* ``COPY_MARKERS.ICC``: copy only ICC profile (APP2) markers.

Converting an image to an optimized JPEG (using `Pillow <https://pillow.readthedocs.io/>`_):

.. code-block:: python

    from io import BytesIO

    from PIL import Image  # pip install pillow
    import mozjpeg_lossless_optimization


    def convert_to_optimized_jpeg(input_path, output_path):
        jpeg_io = BytesIO()

        with Image.open(input_path, "r") as image:
            image.convert("RGB").save(jpeg_io, format="JPEG", quality=90)

        jpeg_io.seek(0)
        jpeg_bytes = jpeg_io.read()

        optimized_jpeg_bytes = mozjpeg_lossless_optimization.optimize(jpeg_bytes)

        with open(output_path, "wb") as output_file:
            output_file.write(optimized_jpeg_bytes)


    convert_to_optimized_jpeg("input.png", "optimized.jpg")


Install
-------

From PyPI
~~~~~~~~~

To install MozJPEG Lossless Optimization from PyPI, just run the following
command::

    pip install mozjpeg-lossless-optimization

.. NOTE::

   We provide precompiled packages for most common platforms. You may need to
   install additional build dependencies if there is no precompiled package
   available for your platform (see below).


From Sources
~~~~~~~~~~~~

To install MozJPEG Lossless Optimization, MozJPEG will be compiled, so you will
need a C compilator and cmake. On Debian / Ubuntu you can install everything
you need with the following command::

    sudo apt install build-essential cmake python3 python3-dev python3-pip python3-setuptools

Once everything installed, clone this repository::

    git clone https://github.com/wanadev/mozjpeg-lossless-optimization.git

Then navigate to the project's folder::

    cd mozjpeg-lossless-optimization

Retrieve submodules::

    git submodule init
    git submodule update

And finally build and install using the following command::

    python3 setup.py install


Hacking
-------

Get the source and build C lib and module:

.. code-block:: sh

    # Install system dependencies
    sudo apt install build-essential cmake python3 python3-dev python3-pip python3-setuptools

    # Get the sources
    git clone https://github.com/wanadev/mozjpeg-lossless-optimization.git
    cd mozjpeg-lossless-optimization
    git submodule init
    git submodule update

    # Create and activate a Python virtualenv
    python3 -m venv __env__
    source __env__/bin/activate

    # Install Python dependencies in the virtualenv
    pip install cffi

    # Build MozJPEG
    # This will generate files in ./mozjpeg/build/ folder
    python setup.py build

    # Build the CFFI module "in-place"
    # This will create the ./mozjpeg_lossless_optimization/_mozjpeg_opti.*.so file on Linux
    python ./mozjpeg_lossless_optimization/mozjpeg_opti_build.py

Lint::

    pip install nox
    nox -s lint

Run tests::

    pip install nox
    pip -s test


Licenses
--------

**MozJPEG Lossless Optimization** is licensed under the BSD 3 Clause license.
See the `LICENSE
<https://github.com/wanadev/mozjpeg-lossless-optimization/blob/master/LICENSE>`_
file for more information.

**MozJPEG** is covered by three compatible BSD-style open source licenses. See
`its license file <https://github.com/mozilla/mozjpeg/blob/master/LICENSE.md>`_
for more information.


Changelog
---------

* **[NEXT]** (changes on master but not released yet):

  * Nothing yet ;)

* **v1.3.0:**

  * feat: Added an option to allow copying metadata from the original image
    (@pierotofy, #4, #33)
  * misc(build): Fixed build with cmake 3.13+ (@flozz)

* **v1.2.0:**

  * misc(mozjpeg): Updated mozjpeg to latest master commit: 9b8d11f (v4.1.5+)
    (@flozz)

* **v1.1.5:**

  * misc(deps): Pin setuptools only for PyPy on Windows platform (@flozz, #26)

* **v1.1.4:**

  * misc(wheel): Fixed Windows builds by sticking on setuptools<74 (@flozz)
  * misc(wheel): Build ARM64 wheels for Linux platform (@flozz, #23)
  * misc: Added Python 3.13 support (@flozz)
  * misc!: Removed Python 3.8 support (@flozz)

* **v1.1.3:**

  * Added Python 3.12 support (@flozz, #6)
  * Removed Python 3.7 support (@flozz)

* **v1.1.2:**

  * Added Python 3.11 support

* **v1.1.1:**

  * Fix sdist package: missing MozJPEG source files added

* **v1.1.0:**

  * Updated mozjpeg to latest master commit: fd56921 (v4.1.1+)

* **v1.0.2:**

  * ``arm64`` and ``universal2`` wheels for macOS on Apple Silicon
  * ``x86`` and ``x68_64`` wheels for musl-based Linux distro (Alpine,...)

* **v1.0.1:** Python 3.10 support and wheels
* **v1.0.0:** Handle JPEG decompression errors
* **v0.9.0:** First public release


.. |Github| image:: https://img.shields.io/github/stars/wanadev/mozjpeg-lossless-optimization?label=Github&logo=github
   :target: https://github.com/wanadev/mozjpeg-lossless-optimization
.. |Discord| image:: https://img.shields.io/badge/chat-Discord-8c9eff?logo=discord&logoColor=ffffff
   :target: https://discord.gg/BmUkEdMuFp
.. |PYPI Version| image:: https://img.shields.io/pypi/v/mozjpeg-lossless-optimization.svg
   :target: https://pypi.python.org/pypi/mozjpeg-lossless-optimization
.. |Build Status| image:: https://github.com/wanadev/mozjpeg-lossless-optimization/actions/workflows/python-ci.yml/badge.svg
   :target: https://github.com/wanadev/mozjpeg-lossless-optimization/actions
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://black.readthedocs.io/en/stable/
.. |License| image:: https://img.shields.io/pypi/l/mozjpeg-lossless-optimization.svg
   :target: https://github.com/wanadev/mozjpeg-lossless-optimization/blob/master/LICENSE
