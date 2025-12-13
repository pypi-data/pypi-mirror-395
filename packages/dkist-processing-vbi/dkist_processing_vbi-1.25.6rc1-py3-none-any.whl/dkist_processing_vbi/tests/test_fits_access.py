import pytest
from astropy.io import fits
from dkist_header_validator import spec122_validator

from dkist_processing_vbi.models.fits_access import VbiMetadataKey
from dkist_processing_vbi.parsers.vbi_l0_fits_access import VbiL0FitsAccess
from dkist_processing_vbi.parsers.vbi_l1_fits_access import VbiL1FitsAccess
from dkist_processing_vbi.tests.conftest import Vbi122ObserveFrames


@pytest.fixture(scope="function")
def header():
    ds = Vbi122ObserveFrames(array_shape=(1, 2, 2), num_steps=1)
    header_list = [
        spec122_validator.validate_and_translate_to_214_l0(d.header(), return_type=fits.HDUList)[
            0
        ].header
        for d in ds
    ]
    return header_list[0]


def test_metadata_keys_in_access_bases(header):
    """
    Given: the set of metadata key names in VbiMetadataKey
    When: the VBI FITS access classes define a set of new attributes
    Then: the sets are the same the attributes have the correct values
    """
    vbi_metadata_key_names = {vmk.name for vmk in VbiMetadataKey}
    all_vbi_fits_access_attrs = set()
    for access_class in [VbiL0FitsAccess, VbiL1FitsAccess]:
        fits_obj = access_class.from_header(header)
        vbi_instance_attrs = set(vars(fits_obj).keys())
        parent_class = access_class.mro()[1]
        parent_fits_obj = parent_class.from_header(header)
        parent_instance_attrs = set(vars(parent_fits_obj).keys())
        vbi_fits_access_attrs = vbi_instance_attrs - parent_instance_attrs
        for attr in vbi_fits_access_attrs:
            assert getattr(fits_obj, attr) == fits_obj.header[VbiMetadataKey[attr]]
        all_vbi_fits_access_attrs |= vbi_fits_access_attrs
    assert vbi_metadata_key_names == all_vbi_fits_access_attrs
