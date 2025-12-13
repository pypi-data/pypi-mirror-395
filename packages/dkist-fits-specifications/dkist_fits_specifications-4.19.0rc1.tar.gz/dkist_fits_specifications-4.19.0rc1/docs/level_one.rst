.. _level-one-data-products:

Level One Data
==============

Level one data are provided by the DKIST data center for all scientific observations carried out by the telescope.
The level one data are calibrated to remove any effects introduced by the telescope or instruments.
The result of these calibration recipes is a level one "dataset" which are the smallest units of DKIST data which are searchable from the data center.

A Level One "Dataset"
---------------------

A single dataset contains observations from a single camera, a single instrument, in a single pass band for a continuous period of observation.
Each of these datasets is spread across many FITS files in the form described by :ref:`spec-214`.
In addition to the FITS files the level one Dataset also contains the following files:

* A single ASDF file which has a record of all the metadata for the Dataset, and can be loaded using the `dkist` Python package.
* A quality report PDF, which is a high level summary of the observing conditions and paramters of the data which might affect scientific utility. The data that generated this report is also contained in the ASDF file.
* A quick view movie, which is an animation of the Dataset which can be used as a preview.

The ASDF File
-------------

The ASDF file is provided alongside the Dataset to facilitate inspection and analysis of the metadata of a Dataset, without having to transfer all the data.
This, in concert with the preview movie, is designed to help make decisions on if a given Dataset is of interest, or what parts of it are, without needing to transfer it.

The ASDF file provides the following information about the dataset:

* A table of all the FITS headers for all the FITS files contained in the dataset.
* An ordered nested list of the filenames of all the FITS files, providing the information about how to reconstruct the full dataset array from all the component FITS arrays.
* Information about the dtype, shape and HDU number of the arrays in the FITS file.
* A `gWCS <https://gwcs.readthedocs.io/>`__ object providing the coordinate information for the reconstructed dataset array.

The FITS Files
--------------

As already mentioned the data in a Dataset is distributed amongst many FITS files.
This is due to the potential size of each of these datasets, and to eliminate on demand processing at the data center a single level one dataset is distributed across many FITS files.
Each individual FITS file represents what can be considered to be a "single calibrated exposure".
This means that when all the processing steps have been taken into account there can be many actual exposures of the instrument involved, but these have all been reduced to a single array.
The exact contents of each FITS file vary depending on the type of instrument and the mode it was operating in, but some examples would be:

* A single wideband image without polrimetric information with a single timestamp (VBI).
* A single slit position, at one Stokes profile, with a single timestamp (ViSP / CryoNIRSP).
* A single narrow band image, at one Stokes profile, with a single timestamp (VTF).

Each level one FITS file should have only one HDU which contains data, it is expected that this will be the second HDU in the file and the data will be RICE compressed as described by the FITS 4 standard.
For more information about the metadata provided in each FITS file see :ref:`spec-214`.
