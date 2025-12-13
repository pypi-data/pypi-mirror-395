.. _dataset_extra:

Dataset Extras Fits Specification
=================================

In addition to Level 1 science data, each dataset also comes with a set of "dataset extras" that help illuminate the
inner workings of the Level 1 science pipeline. These extras are delivered as FITS files with headers described here.
The tables below also exist in a machine readable format in the `dkist_fits_specifications` repository.

Dataset Extras Header Specification
-----------------------------------

**NOTE:** The tables of keys listed below do not apply to *all* dataset extras; each extra will contain only the subset
of these tables that are relevant to itself. See the individual instrument pipeline documentation for more information
on which tables apply to which extras.

.. dataset-extra-table:: fits
.. dataset-extra-table:: common
.. dataset-extra-table:: aggregate
.. dataset-extra-table:: ip_task
.. dataset-extra-table:: gos
.. dataset-extra-table:: wavecal
.. dataset-extra-table:: atlas
.. dataset-extra-table:: visp
.. dataset-extra-table:: cryonirsp
.. dataset-extra-table:: dlnirsp
.. dataset-extra-table:: compression
