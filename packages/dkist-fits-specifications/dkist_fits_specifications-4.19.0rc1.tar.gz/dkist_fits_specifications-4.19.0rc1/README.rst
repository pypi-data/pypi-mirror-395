Machine readable FITS specifications for DKIST data.
----------------------------------------------------

|codecov|

This repository contains machine readable versions of DKIST specifications for FITS files.

This repository is used alongside the `dkist-header-validator <https://pypi.org/project/dkist-header-validator/>`__ to validate that SPEC122 or SPEC214 data is compliant with these DKIST specifications. To use the validator, please click `here <https://pypi.org/project/dkist-header-validator/>`__ and follow the installation instructions.

Usage
-----

This repository contains machine readable versions of DKIST specifications 122 (level 0 FITS files), 214 l0 (Data Center ingested files) and 214 (level 1 FITS files),
as well as the spec for dataset extras.
There are three submodules `spec122`, `spec214`, and `dataset_extras`; they respectively provide `load_spec122`, `load_level0_spec214`, `load_spec214`, and
`load_sparse_dataset_extra` functions which return the "simple" schema for each specification.
The `spec214` and `dataset_extras` modules also provide `load_full_spec214` and `load_full_dataset_extra` functions, which provides extra metadata
on the schema designed for generation of documentation.
Finally, all three modules provide `load_processed_*` functions, which adjusts the schemas based on an L0/L1 header given as input.
`load_processed_*` are the highest-level "gimme-the-actual-spec" functions for each spec.

Releases
--------

Version Numbers
###############

The version number of this repository follows the following form:

    vX.Y.Z

The version number of this repository does not follow semantic versioning for the Python code in the package, it versions **the specifications** using the following interpretation of the three components:

* ``X``: This number will be incremented for any change which **results in a backwards incompatible change to the FITS headers**.
  This could include things such as removal of a key or changing the interpretation of a key in any way, such as a change in units.
  Any change which could *potentially* mean that a script written to process one of our headers would *yield a different result* needs a change to this number.

* ``Y``: This number will be incremented for **any** backwards compatible change to the header.
  This means any change which leads to any character in the header changing (other than values obviously) so this could include changes to comments describing values or the addition of new keys to the header.
  Changing the ordering of the keys in the header does, or fields in ``COMMENT`` or ``HISTORY`` cards do not require changes to this number, but a change in a value comment would (as these may be parsed to extract units etc).

* ``Z``: This number will be incremented for any change to the repository which does not lead to a change in the FITS headers.
  This means any change to the Python API, infrastructure or anything else.
  The Python API should **not be considered stable** between increments of this number.

Changelog
#########

When you make **any** change to this repository it **MUST** be accompanied by a changelog file.
The changelog for this repository uses the `towncrier <https://github.com/twisted/towncrier>`__ package.
Entries in the changelog for the next release are added as individual files (one per change) to the ``changelog/`` directory.

Writing a Changelog Entry
^^^^^^^^^^^^^^^^^^^^^^^^^

A changelog entry accompanying a change should be added to the ``changelog/`` directory.
The name of a file in this directory follows a specific template::

  <PULL REQUEST NUMBER>.<TYPE>[.<COUNTER>].rst

The fields have the following meanings:

* ``<PULL REQUEST NUMBER>``: This is the number of the pull request, so people can jump from the changelog entry to the diff on BitBucket.
* ``<TYPE>``: This is the type of the change and must be one of the values described below.
* ``<COUNTER>``: This is an optional field, if you make more than one change of the same type you can append a counter to the subsequent changes, i.e. ``100.bugfix.rst`` and ``100.bugfix.1.rst`` for two bugfix changes in the same PR.

The list of possible types is defined the the towncrier section of ``pyproject.toml``, the types are:

* ``spec_breaking``: This is a change which is a backwards incompatible change to the FITS headers.
  If a release has a change of this type in it **the first number in the version number must be incremented**.
* ``spec_change``: This is a change which is a backwards compatible change to the FITS headers.
  If a release has a change of this type in it **the second number in the version number must be incremented**.
* ``code_breaking``: This is a change which breaks the Python API.
  The Python API changes only increment the last version number, so it is important to clearly document in the changelog when a release changes the API in a breaking manner.
* ``code_feature``: This change is a backwards compatible change to the Python API, such as a new feature.
* ``bugfix``: This is a change which fixes a bug in the Python API (but has no resultant change in the headers).
* ``doc``: A documentation change.
* ``deprecation``: A change which introduces a warning that a feature in the Python API will be changed in the future.
* ``trivial``: Any small change which doesn't fit anywhere else, such as a change to the package infrastructure.


Rendering the Changelog at Release Time
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When you are about to tag a release first you must run ``towncrier`` to render the changelog.
The steps for this are as follows:

* Install towncrier with `pip install towncrier`
* Run `towncrier build --version vx.y.z` using the version number you want to tag.
* Agree to have towncrier remove the fragments.
* Add and commit your changes.
* Tag the release.

Documentation
-------------

Note that this repo makes use of sphinx-automodapi rather than autoapi like a lot of the other DKIST DC repos to have a little more control over rendering the limited Python API.

License
-------

This project is Copyright (c) AURA/NSO and licensed under
the terms of the BSD 3-Clause license. This package is based upon
the `Openastronomy packaging guide <https://github.com/OpenAstronomy/packaging-guide>`_
which is licensed under the BSD 3-clause licence. See the licenses folder for
more information.

.. |codecov| image:: https://codecov.io/bb/dkistdc/dkist-fits-specifications/graph/badge.svg?token=10BY10VI5Z
 :target: https://codecov.io/bb/dkistdc/dkist-fits-specifications
