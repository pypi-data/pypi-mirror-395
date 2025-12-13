"""
DKIST FITS header specifications.

This package contains machine readable versions of the DKIST specifications 122 and 214.
The objectives of this package are to:

* Provide a single source of truth for all software interacting with DKIST FITS specifications.
* Reduce duplication in the specifications themselves, to ease reading and updating the specifications.
* Provide a coupling between the level 1 (214) specification and the level 0
  (122) specification, as much of the metadata is copied from the level 0 to
  the level 1 headers, so if the 122 specification changes the 214
  specification is automatically updated to match.

"""
from pathlib import Path

from yamale import make_schema  # type: ignore

from .version import __version__  # type: ignore

__all__ = []


validation_schema = make_schema(Path(__file__).parent / "spec_validation_schema.yml")
