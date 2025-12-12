"""Tests for package-level imports."""


def test_import_confusius():
    """Test that the confusius package can be imported."""
    import confusius

    assert confusius is not None


def test_import_io_module():
    """Test that the io module can be imported."""
    import confusius.io

    assert confusius.io is not None


def test_import_iq_module():
    """Test that the iq module can be imported."""
    import confusius.iq

    assert confusius.iq is not None


def test_import_autc():
    """Test that AUTC classes can be imported."""
    from confusius.io import AUTCDAT, AUTCDATsLoader

    assert AUTCDAT is not None
    assert AUTCDATsLoader is not None


def test_import_echoframe():
    """Test that echoframe functions can be imported."""
    from confusius.io import load_echoframe_dat

    assert load_echoframe_dat is not None


def test_import_reduce():
    """Test that reduce functions can be imported."""
    from confusius.iq import compute_axial_velocity_volume, compute_power_doppler_volume

    assert compute_axial_velocity_volume is not None
    assert compute_power_doppler_volume is not None


def test_import_clutter_filters():
    """Test that clutter filter functions can be imported."""
    from confusius.iq import (
        clutter_filter_svd_from_indices,
        clutter_filter_svd_from_energy,
        clutter_filter_svd_from_cumsum_energy,
        clutter_filter_butterworth,
    )

    assert clutter_filter_svd_from_indices is not None
    assert clutter_filter_svd_from_energy is not None
    assert clutter_filter_svd_from_cumsum_energy is not None
    assert clutter_filter_butterworth is not None
