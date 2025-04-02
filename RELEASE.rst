Things to do while releasing a new version
==========================================

This file is a memo for the maintainer.


0. Checks
---------

* If MozJPEG has been updated, ensure that ``MANIFEST.in`` has been updated,
  generate an sdist package and check we are able to build a wheel from it::

      ./scripts/generate_manifest_in.sh > MANIFEST.in

      python setup.py sdist

      python3 -m venv checkwheel.env
      checkwheel.env/bin/pip install dist/*.tar.gz


1. Release
----------

* Update version number in ``setup.py``
* Edit / update changelog in ``README.rst``
* Commit / tag (``git commit -m vX.Y.Z && git tag vX.Y.Z && git push && git push --tags``)


2. Publish PyPI package
-----------------------

Publish source dist and wheels on PyPI.

→ Automated :)


3. Publish Github Release
-------------------------

* Make a release on Github
* Add changelog
