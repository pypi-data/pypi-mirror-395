import numpy as np
import pandas as pd

from trap.associate import associate, de_ruiter_radius


def test_de_ruiter_radius():
    # Test values taken from vast-pipeline's `calc_de_ruiter`.
    #  -> https://github.com/askap-vast/vast-pipeline/blob/328e7a5419e12eb13cb302b2cb92b96e1895dca2/vast_pipeline/pipeline/association.py#L28

    p1_ra = np.array(
        [141.90155600000003, 141.892601, 141.899543, 141.951193, 141.94798500000002]
    )
    p1_dec = np.array([-4.200975, -4.20644, -4.202349, -4.504008, -4.49331])
    p1_err_ew = np.array(
        [
            0.00027782369653707846,
            0.00027816588026052813,
            0.00030429161656277836,
            0.00027786304943388515,
            0.00029331883450749857,
        ]
    )
    p1_err_ns = np.array(
        [
            0.00027782369653707846,
            0.00027816588026052813,
            0.00030429161656277836,
            0.00027786304943388515,
            0.00029331883450749857,
        ]
    )
    p2_ra = np.array(
        [141.901523, 141.89270900000002, 141.901523, 141.95117800000003, 141.947973]
    )
    p2_dec = np.array([-4.201026, -4.206385, -4.201026, -4.504013, -4.493317])
    p2_err_ew = np.array(
        [
            0.0002778105776660355,
            0.00027811608659412566,
            0.0002778105776660355,
            0.0002778407501433764,
            0.0002896326202114759,
        ]
    )
    p2_err_ns = np.array(
        [
            0.0002778105776660355,
            0.00027811608659412566,
            0.0002778105776660355,
            0.0002778407501433764,
            0.0002896326202114759,
        ]
    )

    expected_radius = np.array(
        [0.154488080, 0.307458456, 5.76871260, 0.0401266670, 0.0336245054]
    )
    result = de_ruiter_radius(
        p1_ra=p1_ra,
        p1_dec=p1_dec,
        p1_err_ew=p1_err_ew,
        p1_err_ns=p1_err_ns,
        p2_ra=p2_ra,
        p2_dec=p2_dec,
        p2_err_ew=p2_err_ew,
        p2_err_ns=p2_err_ns,
    )
    np.testing.assert_allclose(result, expected_radius)


def test_empty_source_list():
    """Start with an empty source list and add new sources to it.
    That way all sources are new and there are no dull-detections.
    """
    sources = pd.DataFrame(
        {
            "id": [],
            "ra": [],
            "dec": [],
            "ra_fit_err": [],
            "decl_fit_err": [],
            "based_on": [],
            "peak_flux": [],
            "uncertainty_ns": [],
            "uncertainty_ew": [],
        }
    ).set_index("id")

    new_sources = pd.DataFrame(
        {
            "id": [0, 1],
            "ra": [1, 2],
            "dec": [1, 2],
            "ra_fit_err": [1, 2],
            "decl_fit_err": [1, 2],
            "peak_flux": [1, 2],
            "uncertainty_ns": [1, 2],
            "uncertainty_ew": [1, 2],
        }
    ).set_index("id")

    null_detection_ids, new_ids, persistings_mapping, duplicate_mapping = associate(
        sources, new_sources
    )

    assert len(persistings_mapping) == 0
    assert len(duplicate_mapping) == 0
    np.testing.assert_allclose(null_detection_ids, [])
    np.testing.assert_allclose(new_ids, [0, 1])


def test_one_to_one():
    """Test basic one-to-one relations where the known and new sources are at the same location.
    This way there are no null-detections and no new sources.
    """
    sources = pd.DataFrame(
        {
            "id": [0, 1],
            "ra": [1, 2],
            "dec": [1, 2],
            "ra_fit_err": [1, 2],
            "decl_fit_err": [1, 2],
            "based_on": [np.nan, np.nan],
            "peak_flux": [1, 2],
            "uncertainty_ns": [1, 2],
            "uncertainty_ew": [1, 2],
        }
    ).set_index("id")

    new_sources = pd.DataFrame(
        {
            "id": [0, 1],
            "ra": [1, 2],
            "dec": [1, 2],
            "ra_fit_err": [1, 2],
            "decl_fit_err": [1, 2],
            "peak_flux": [1, 2],
            "uncertainty_ns": [1, 2],
            "uncertainty_ew": [1, 2],
        }
    ).set_index("id")

    null_detection_ids, new_ids, persistings_mapping, duplicate_mapping = associate(
        sources, new_sources
    )

    np.testing.assert_allclose(persistings_mapping.original_id, [0, 1])
    np.testing.assert_allclose(persistings_mapping.new_id, [0, 1])

    assert len(duplicate_mapping) == 0
    np.testing.assert_allclose(null_detection_ids, [])
    np.testing.assert_allclose(new_ids, [])


def test_one_to_many():
    """Start with one source and have multiple new sources near the original source.
    Of the new sources, only one will match the original source. The other sources are considered new sources.
    There are no null-detections.
    """
    sources = pd.DataFrame(
        {
            "id": [0],
            "ra": [1],
            "dec": [1],
            "ra_fit_err": [1],
            "decl_fit_err": [1],
            "based_on": [np.nan],
            "peak_flux": [1],
            "uncertainty_ns": [1],
            "uncertainty_ew": [1],
        }
    ).set_index("id")

    new_sources = pd.DataFrame(
        {
            "id": [0, 1, 2],
            "ra": [1.01, 1, 0.98],
            "dec": [1.01, 1, 0.98],
            "ra_fit_err": [1.01, 1, 0.98],
            "decl_fit_err": [1.01, 1, 0.98],
            "peak_flux": [1.01, 1, 0.98],
            "uncertainty_ns": [1.01, 1, 0.98],
            "uncertainty_ew": [1.01, 1, 0.98],
        }
    ).set_index("id")

    null_detection_ids, new_ids, persistings_mapping, duplicate_mapping = associate(
        sources, new_sources
    )

    np.testing.assert_allclose(persistings_mapping.original_id, [0])
    np.testing.assert_allclose(persistings_mapping.new_id, [1])

    np.testing.assert_allclose(duplicate_mapping.original_id, [0, 0])
    np.testing.assert_allclose(duplicate_mapping.new_id, [0, 2])

    np.testing.assert_allclose(null_detection_ids, [])
    np.testing.assert_allclose(new_ids, [])


def test_many_to_one():
    """Start with multiple sources and have only one source in the new image.
    This way there is one persistent source, no new sources and several null-detections.
    """
    sources = pd.DataFrame(
        {
            "id": [0, 1, 2],
            "ra": [1.01, 1, 0.98],
            "dec": [1.01, 1, 0.98],
            "ra_fit_err": [1.01, 1, 0.98],
            "decl_fit_err": [1.01, 1, 0.98],
            "based_on": [np.nan, np.nan, np.nan],
            "peak_flux": [1.01, 1, 0.98],
            "uncertainty_ns": [1.01, 1, 0.98],
            "uncertainty_ew": [1.01, 1, 0.98],
        }
    ).set_index("id")

    new_sources = pd.DataFrame(
        {
            "id": [0],
            "ra": [1],
            "dec": [1],
            "ra_fit_err": [1],
            "decl_fit_err": [1],
            "peak_flux": [1],
            "uncertainty_ns": [1],
            "uncertainty_ew": [1],
        }
    ).set_index("id")

    null_detection_ids, new_ids, persistings_mapping, duplicate_mapping = associate(
        sources, new_sources
    )

    # Check returned ids
    np.testing.assert_allclose(persistings_mapping.original_id, [1])
    np.testing.assert_allclose(persistings_mapping.new_id, [0])

    assert len(duplicate_mapping) == 0

    np.testing.assert_allclose(null_detection_ids, [0, 2])
    np.testing.assert_allclose(new_ids, [])


def test_combination():
    """Test a combination of one_to_one, one_to_many and many_to_one.
    This does not tesst a real many_to_many case because the many_to_one and one_to_many relations
    involve different points.
    This way there are both null-detections and new sources.
    """

    sources = pd.DataFrame(
        {
            "id": [0, 1, 2, 3, 4, 5],
            "ra": [0, 1, 2, 12, 3, 3.02],
            "dec": [0, 1, 2, 12, 3, 3.02],
            "ra_fit_err": 6 * [0.01],
            "decl_fit_err": 6 * [0.01],
            "based_on": 6 * [np.nan],
            "peak_flux": 6 * [1],
            "uncertainty_ns": 6 * [0.01],
            "uncertainty_ew": 6 * [0.01],
        }
    ).set_index("id")

    new_sources = pd.DataFrame(
        {
            "id": [0, 1, 2, 3, 4, 5],
            "ra": [2, 0, 1, 1.02, 3, -18],
            "dec": [2, 0, 1, 1.02, 3, -18],
            "ra_fit_err": 6 * [0.01],
            "decl_fit_err": 6 * [0.01],
            "peak_flux": 6 * [1],
            "uncertainty_ns": 6 * [0.01],
            "uncertainty_ew": 6 * [0.01],
        }
    ).set_index("id")

    null_detection_ids, new_ids, persistings_mapping, duplicate_mapping = associate(
        sources, new_sources
    )

    np.testing.assert_allclose(persistings_mapping.original_id, [2, 0, 1, 4])
    np.testing.assert_allclose(persistings_mapping.new_id, [0, 1, 2, 4])

    np.testing.assert_allclose(duplicate_mapping.original_id, [1])
    np.testing.assert_allclose(duplicate_mapping.new_id, [3])

    np.testing.assert_allclose(null_detection_ids, [3, 5])
    np.testing.assert_allclose(new_ids, [5])


def test_many_to_many():
    """
    Test a case where there are several starting sources that are all close to several sources in the new image.
    Since there are more new sources than starting sources, there are new sources but no null-detections.
    These values are taken from a test run with real data.
    The ids are sparse. In a real run they would likely be perfectly ascending, starting at 0, but
    in order for the association function to be robust it should also be able to handle the case where they are not.

    Expected match:
       new_id | based_on
       108   ->  223
       110   ->  113
       113   ->  nan (new source)
    """
    sources = pd.DataFrame(
        {
            "id": [113, 223],
            "ra": [61.40, 61.44],
            "dec": [64.917, 64.913],
            "ra_fit_err": [0.000115, 0.0018],
            "decl_fit_err": [0.000034, 0.000462],
            "based_on": [np.nan, np.nan],
            "peak_flux": [1.86, 0.05],
            "uncertainty_ns": [0.00278, 0.00292],
            "uncertainty_ew": [0.00278, 0.00292],
        }
    ).set_index("id")

    new_sources = pd.DataFrame(
        {
            "id": [
                108,
                110,
                113,
            ],  # Note that 113 here does not match the 113 in sources
            "ra": [61.44, 61.40, 61.35],
            "dec": [64.917, 64.913, 64.92],
            "ra_fit_err": [0.000115, 0.0018, 0.0015],
            "decl_fit_err": [0.000034, 0.000462, 0.00039],
            "peak_flux": [1.86, 0.05, 0.05],
            "uncertainty_ns": [0.00278, 0.00292, 0.00287],
            "uncertainty_ew": [0.00278, 0.00292, 0.00287],
        }
    ).set_index("id")

    null_detection_ids, new_ids, persistings_mapping, duplicate_mapping = associate(
        sources, new_sources
    )

    np.testing.assert_allclose(persistings_mapping.original_id, [223, 113])
    np.testing.assert_allclose(persistings_mapping.new_id, [108, 110])

    np.testing.assert_allclose(duplicate_mapping.original_id, [113])
    np.testing.assert_allclose(duplicate_mapping.new_id, [113])

    np.testing.assert_allclose(null_detection_ids, [])
    np.testing.assert_allclose(new_ids, [])


def test_many_to_many_conflict():
    """
    Test a case where there are several starting sources that are all close to several sources in the new image.
    In this setup, The many-to-one initially select the same known source.

    We start with the following connections, this would be after a first-pass filter of rough proximity:
        new_id | known_id | de_Ruiter_r
        0     ->     0   ->    3
        1     ->     0   ->    1
        1     ->     1   ->    2
        1     ->     2   ->    3
        3     ->     2   ->    3

    In this setup, known source 1 is nearby all three new sources.
    Known source 0 is near new source 0 and known source 2 is near new source 2.
    The de Ruiter radius is written between the connections.


    These relations look likse so:
    known_id - de_ruiter - new_id
                0 - 3 - 0
                       /
                    1
                 /
                1 - 2 - 1
                 \
                    3
                       \
                2 - 3 - 2

    Spatial source distribution is something like:

                    N1
                    |
                    |
        K0 --- N0 - K1 -- N2 ---K2

    Where K0, K1 and K2 are the known sources and N0, N1 and N2 are the new sources.
    Dashes indicate the de Ruiter distance where more dashes means a higher value.

    Given the de Ruiter radii in this setup, we want it to get the connections:
    new_id | known_id
        1 -> 0
        2 -> 2
    And know source 0 is considered old for it's only connection of de Ruiter radius 3 gets assigned
    to known source 1 because it has a lower de Ruiter radius of 1.
    New source 1 is consdered a fresh source because it's only connection to known source 1 has a de
    Ruiter radius of 2, which is larger than the de Ruiter radius of 1 from known source 1 to new source 0.
    """
    sources = pd.DataFrame(
        {
            "id": [0, 1, 2],
            "ra": [61.44, 61.40, 61.35],
            "dec": [64, 64, 64],
            "ra_fit_err": [0.0015, 0.0015, 0.0015],
            "decl_fit_err": [0.0015, 0.0015, 0.0015],
            "peak_flux": [1, 1, 1],
            "uncertainty_ns": [0.00278, 0.00278, 0.00278],
            "uncertainty_ew": [0.00278, 0.00278, 0.00278],
        }
    ).set_index("id")

    # Note: the dec has more impact on the de Ruiter radius than ra at this location
    new_sources = pd.DataFrame(
        {
            "id": [0, 1, 2],
            "ra": [61.41, 61.40, 61.38],
            "dec": [64, 64.014, 64],
            "ra_fit_err": [0.0015, 0.0015, 0.0015],
            "decl_fit_err": [0.0015, 0.0015, 0.0015],
            "peak_flux": [1, 1, 1],
            "uncertainty_ns": [0.00278, 0.00278, 0.00278],
            "uncertainty_ew": [0.00278, 0.00278, 0.00278],
        }
    ).set_index("id")

    null_detection_ids, new_ids, persistings_mapping, duplicate_mapping = associate(
        sources, new_sources, surpress_duplications=True
    )

    np.testing.assert_allclose(persistings_mapping.original_id, [1, 2])
    np.testing.assert_allclose(persistings_mapping.new_id, [0, 2])

    np.testing.assert_allclose(duplicate_mapping.original_id, [1])
    np.testing.assert_allclose(duplicate_mapping.new_id, [1])

    np.testing.assert_allclose(null_detection_ids, [0])
    np.testing.assert_allclose(
        new_ids, []
    )  # The new id is covered in the duplicate mapping
