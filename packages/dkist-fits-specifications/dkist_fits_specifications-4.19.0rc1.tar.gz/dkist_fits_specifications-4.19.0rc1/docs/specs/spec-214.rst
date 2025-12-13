.. _spec-214:

Level One FITS Specification
============================

This webpage is automatically generated from the latest release of the specifications repository.
As well as providing these documentation pages, this repository contains machine readable versions of both level 0 (spec 122) and level 1 (spec 214) specifications.
These machine readable versions are used in various places in the DKIST Data Center to validate and manipulate headers.

Standards applying to calibrated data
-------------------------------------

Data formats
############

All DKIST data shall be delivered – combined with its metadata in a format compliant with the `FITS 4.0`_ standard as well as the `SOLARNET Metadata recommendations for Solar Observations`_.


Compression
###########
Calibrated DKIST FITS files will be stored and delivered with a RICE compression algorithm applied as described in `FITS 4.0`_ Section 10.


Use of the World Coordinate System
##################################

All DKIST data and metadata shall be delivered using a coordinate system that complies with the World Coordinate System standard as defined in the `FITS 4.0`_ standard and `Thompson (2006)`_.
All DKIST data and metadata shall be delivered with exactly two celestial coordinate systems:

* One relevant for solar data: Helioprojective Coordinates
* One relevant for astronomical objects other than the Sun: Equatorial Coordinates

Some DKIST data will be of spectroscopic, or spectro-polarimetric nature. Where these world axes vary along the array axes in a single FITS file it will be handled within the FITS standard for spectroscopic data.


Use of the Système Internationale d’Unités
##########################################

All DKIST metadata delivered across a non DKIST-internal interface shall be in SI (base or derived) units.


Level One Header Specification
------------------------------

.. spec-214-table:: fits
.. spec-214-table:: telescope
.. spec-214-table:: datacenter
.. spec-214-table:: dataset
.. spec-214-table:: stats
.. spec-214-table:: dkist-id
.. spec-214-table:: dkist-op
.. spec-214-table:: camera
.. spec-214-table:: pac
.. spec-214-table:: ao
.. spec-214-table:: wfc
.. spec-214-table:: ws
.. spec-214-table:: vbi
.. spec-214-table:: visp
.. spec-214-table:: cryonirsp
.. spec-214-table:: dlnirsp
.. spec-214-table:: vtf
.. spec-214-table:: compression


.. _SOLARNET Metadata Recommendations for Solar Observations: https://arxiv.org/abs/2011.12139
.. _FITS 4.0: https://fits.gsfc.nasa.gov/standard40/fits_standard40aa-le.pdf
.. _Thompson (2006): https://www.aanda.org/component/article?access=bibcode&bibcode=2006A%2526A...449..791TFUL
