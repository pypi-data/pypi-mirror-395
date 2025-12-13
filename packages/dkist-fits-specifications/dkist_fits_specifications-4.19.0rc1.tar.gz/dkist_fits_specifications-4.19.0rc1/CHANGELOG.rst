v4.17.0 (2025-05-30)
====================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Add the keys `PV<i>_<0, 1, 2>(A)` to the spec for inclusion in Level 1 headers. (`#72 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/72>`__)


v4.16.0 (2025-05-21)
====================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Remove the `PV<i>_<0, 1, 2>(A)` keys from the Level 1 spec while downstream issues are worked on.

v4.15.0 (2025-05-21)
====================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Add the keys `PV<i>_<0, 1, 2>(A)` to the spec for inclusion in Level 1 headers. (`#70 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/70>`__)
- Relax required-ness constraints on the CHECKSUM and DATASUM keys. (`#71 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/71>`__)


v4.14.0 (2025-05-06)
====================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Add the THEAP key to the level 0 and level 1 specifications. (`#69 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/69>`__)


v4.13.0 (2025-04-14)
====================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Add the HISTORY card to the level 0 and level 1 specifications. (`#68 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/68>`__)


v4.12.0 (2025-04-14)
====================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Adding new percentile keys to the L1 headers (DATAP02 and DATAP05). (`#65 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/65>`__)


New Feature in the Python API
-----------------------------

- Add a method to return the SPEC-0214 keys marked as "level0_only". (`#66 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/66>`__)


Bug Fixes to the Python API
---------------------------

- Fix bug where a header key's comment could be clobbered when passing through `reformat_spec214_header`. (`#67 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/67>`__)


Internal Changes
----------------

- Move coverage configuration to pyproject.toml and add coverage badge to README.rst. (`#64 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/64>`__)


v4.11.0 (2025-02-10)
====================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Convert `ODSOBSID` to a required field so that `PRODUCT` will always get computed. (`#62 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/62>`__)


New Feature in the Python API
-----------------------------

- New keyword `PRODUCT` that will provide continuity when reprocessing occurs. (`#63 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/63>`__)


Internal Changes
----------------

- Update Bitbucket pipelines to use standardized lint and scan steps. (`#60 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/60>`__)
- Update Bitbucket pipelines to use execute script for standard steps. (`#61 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/61>`__)


v4.10.0 (2024-11-25)
====================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- CNAME<n> was previously CNAME<d> in the headers, but was being expanded with one too many axes for VBI causing an error in dkist-inventory. This change updates to CNAME<n>, so that the header is now expanded correctly. (`#59 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/59>`__)


v4.9.0 (2024-11-22)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Making CNAMEn keywords not required so that this is a backwards compatible change. (`#58 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/58>`__)


v4.8.0 (2024-11-22)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Adding in the CNAMEn keywords into the fits spec. Astropy uses these,
  so it would be helpful if we also used them. This information was already contained in the DWNAMEn
  and keywords, so the CNAME keywords will hold the same info. We’re just trying to play nice with Astropy. (`#57 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/57>`__)


v4.7.0 (2024-10-07)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- SPEC 0122 Revision K Updates (`#56 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/56>`__)
- Adjusted CRSP_073 to include a new grating. (`#56 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/56>`__)
- Added a new keyword CAM__044 to track the camera shutter mode that is important for data calibration. (`#56 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/56>`__)
- Adjusted TTBLTRCK keyword values to allow for new tracking modes. (`#56 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/56>`__)
- Adjusted CRSP_051, CRSP_052 to accommodate the new reality of blocking filters instead of lamps. (`#56 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/56>`__)


Documentation
-------------

- Correctly identify type of `DLCURSTP` as "boolean" in key description. (`#55 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/55>`__)


v4.6.0 (2024-08-15)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Correcting the list of allowed values for TTBLTRCK. (`#54 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/54>`__)


v4.5.0 (2024-08-12)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Adding `PV1_0A`, `PV1_1A`, and `PV1_2A` to the CRYO-NIRSP headers. (`#53 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/53>`__)


v4.4.2 (2024-07-18)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Move `PV1_0`, `PV1_1`, and `PV1_2` from generic telescope keywords to CRYO-NIRSP specific keywords.


v4.4.1 (2024-07-17)
===================

Documentation
-------------

- Add information about the meaning of our version numbers to the docs. (`#52 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/52>`__)


v4.4.0 (2024-07-17)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Adding `PV1_0`, `PV1_1`, and `PV1_2` to the headers to allow instruments to define a non-linear spectral dispersion. (`#51 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/51>`__)
- Add the CRYO-NIRSP key `SLITORI` to record the slit orientation relative to solar north. (`#51 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/51>`__)


v4.3.0 (2024-06-12)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Remove instrument requiredness from DLN__043, DLN__044, and DLN__045. These keys may not be present in DL-NIRSP files. (`#50 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/50>`__)


v4.2.0 (2024-05-16)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Updated 214 DL-NIRSP Spec to match the information provided in the 122 DL-NIRSP Spec. (`#49 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/49>`__)
- Revision J:
  Added DKIST013 to capture status of Lyot stop. Added CAM__043 to indicate
  whether the frame data was simulated or not. Modified accepted range of values for
  DLN__026 to allow for the MISI upgrade. (`#49 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/49>`__)


v4.1.1 (2024-02-26)
===================

Bug Fixes to the Python API
---------------------------

- Correctly handle a header which has DEAXES=0. (`#48 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/48>`__)


v4.1.0 (2024-01-31)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Add new keyword `SOLARRAD` which contains the value of the solar radius at the time of observation, in arcseconds. (`#44 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/44>`__)
- Relax instrument key requiredness in L1 data as not all keys are guaranteed to appear in the L0 data. (`#45 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/45>`__)
- Add the `MANPROCD` key to track manual processing runs in the headers. (`#46 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/46>`__)


Breaking change to the Python API
---------------------------------

- `spec122.load_spec122` no longer returns an exanded schema. Use `spec122.load_processed_spec122` instead. (`#45 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/45>`__)


New Feature in the Python API
-----------------------------

- Allow conditional requiredness to be applied to the SPEC 214 level 0 schema. The processed schema is supplied by the
  `spec214.level0.load_level0_spec214` function. This function is cached so watch out passing in weird header cards
  (i.e., don't pass in unhashable `_HeaderCommentaryCards`) (`#45 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/45>`__)
- Allow conditional requiredness to be applied to the SPEC 122 schema. The processed schema is supplied by the
  `spec122.load_processed_spec122` function. (`#45 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/45>`__)


Internal Changes
----------------

- Add check that any 214 keys that are copies/renames of a 122 don't try to re-define schema fields that were already
  defined in the 122 key. If the 214 key really needs different values for any of its schema fields then it should be a
  new key (i.e., not a copy/rename). (`#47 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/47>`__)


v4.0.0 (2024-01-12)
===================

Breaking Changes to the Specification
-------------------------------------

- Add conditional requiredness field, `instrument_required: str(required=False)`, that makes a key `required` if it comes from a header
  from an instrument that matches the value passed to the spec field. E.g., if a key has `instrument_required: vbi` then any header
  from the VBI instrument will make that key `required`. (`#42 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/42>`__)
- "STOKES" key is now `required`. For non-polarimetric data the value will always be "I". This matches how data are
  treated in inventory. (`#43 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/43>`__)
- Add conditional requiredness field, `polarimetric_required: bool(required=False)`, that makes a key `required` if it comes from a header
  from a polarimetric dataset (i.e., a dataset that produces Stokes I, Q, U, V data). The combinations of which specific header keys/values
  conspire to indicate a dataset is polarimetric are defined on a per-instrument level. (`#43 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/43>`__)


Breaking change to the Python API
---------------------------------

- Implement framework for conditional requiredness on keys. Replaces `load_expanded_spec214` with `load_proessed_spec214`. (`#42 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/42>`__)
- Refactor spec_processors so each processor is a module under a new `spec_processor` package. (`#43 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/43>`__)


v3.9.0 (2023-11-22)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Removing CNMODCST, CNMODANG, CNOFFANG, CNCNDR, and CNCRAMP from L1 CRYO-NIRSP headers due to them not being relevant to the L1 data. (`#41 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/41>`__)


v3.8.1 (2023-09-20)
===================

Bug Fixes to the Python API
---------------------------

- Correct character case of some CRYO-NIRSP keywords. (`#40 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/40>`__)


v3.8.0 (2023-09-19)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Update FITS L0 schema to SPEC-0122 revision I. (`#39 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/39>`__)


v3.7.1 (2023-07-26)
===================

Bug Fixes to the Python API
---------------------------

- Update the python version used in the Read The Docs build process.



v3.7.0 (2023-07-26)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Adding the FITS standard key `ZBLANK` (`#36 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/36>`__)


v3.6.0 (2023-04-24)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Add `VBINMOSC` and `VBICMOSC` keys that encode the total number of and current mosaic repeat in VBI data. (`#35 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/35>`__)


v3.5.0 (2023-04-10)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Added `NSPECLNS` and `SPECLN<sl>` keys to support inclusion of spectral line information. (`#34 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/34>`__)


v3.4.0 (2023-03-15)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Add CRYO-NIRSP keys for tracking number of map scans. (`#32 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/32>`__)
- Change units for some VISP specific keywords. (`#33 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/33>`__)


v3.3.0 (2023-02-15)
===================

Bug Fixes to the Python API
---------------------------

- Proposal and experiment ID groups do not get copied from the raw headers. (`#30 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/30>`__)


Documentation
-------------

- Update FITS L0 schema to SPEC-0122 revision H. (`#31 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/31>`__)


v3.2.1 (2023-02-02)
===================

Bug Fixes to the Python API
---------------------------

- Made expansions conditional on keywords that determine their range existing. (`#29 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/29>`__)


v3.2.0 (2023-02-01)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Revert DL-NIRSP keywords to not required. (`#28 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/28>`__)


v3.1.0 (2023-02-01)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Add contributing proposal and experiment id keywords. (`#24 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/24>`__)
- Conform with SPEC-0122 revision G. (`#26 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/26>`__)
- Set required DL-NIRSP keywords. (`#27 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/27>`__)


New Feature in the Python API
-----------------------------

- Refactor how FITS keywords are integer-expanded. (`#25 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/25>`__)


v3.0.0 (2022-10-26)
===================

Bug Fixes to the Python API
---------------------------

- VELOSYS keyword type changed from bool to float. (`#23 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/23>`__)

Misc
----

- Prevent compression header keywords from being moved around during header refactoring. (`#23 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/23>`__)

v2.1.2 (2022-09-14)
===================

Bugfix
---------------------------

- Fix the type of some reprocessing keywords.


v2.1.1 (2022-09-12)
===================

Bugfix
------

- Relaxing requiredness of headers added in v2.1.0


v2.1.0 (2022-09-12)
===================

Features
--------

- Adding new keywords to support the addition of reprocessing metadata to the FITS headers.


v2.0.0 (2022-04-26)
===================

Backwards Compatible Changes to the Specification
-------------------------------------------------

- Updated Spec122 and Spec214 schemas to be consistent with SPEC-122 Rev F. (`#21 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/21>`__)


New Feature in the Python API
-----------------------------

- Change the return values of all specification loading functions to be
  ``frozendict``.
  This means that the specifications once constructed are (largely) immutable and
  therefore can be cached. Caching the specfications massively speeds up
  subsequent calls to the specification construction functions. (`#22 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/22>`__)


v1.5.0 (2022-02-10)
===================

Documentation
-------------

- Add a documenation build for the yaml files containing the specifications and other information about the data products. (`#18 <https://bitbucket.org/dkistdc/dkist-fits-specifications/pull-requests/18>`__)
