.. _release_history:

Release History
===============

Version Numbers

The version number of this repository uses the following form:

    vX.Y.Z

The version number of this repository does not follow semantic versioning for the Python code in the package, it versions **the specifications** using the following interpretation of the three components:

* ``X``: This number will be incremented for any change which **results in a backwards incompatible change to the FITS headers**.
  This could include things such as removal of a key or changing the interpretation of a key in any way, such as a change in units.
  Any change which could *potentially* mean that a script written to process one of our headers would *yield a different result* will lead to a change to this number.

* ``Y``: This number will be incremented for **any** backwards compatible change to the header.
  This means any change which leads to any character in the header changing (other than values obviously) so this could include changes to comments describing values or the addition of new keys to the header.
  Changing the ordering of the keys in the header, or fields in ``COMMENT`` or ``HISTORY`` cards do not require changes to this number, but a change in a value comment would (as these may be parsed to extract units etc).

* ``Z``: This number will be incremented for any change to the repository which does not lead to a change in the FITS headers.
  This means any change to the Python API, infrastructure or anything else.
  The Python API should **not be considered stable** between increments of this number.

Changelog

.. changelog::
   :towncrier: ../
   :changelog_file: ../CHANGELOG.rst
   :towncrier-title-underline-index: 1
