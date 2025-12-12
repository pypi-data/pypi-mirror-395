import numpy as np
import pandas as pd

import trap


def verify_database(db_handle):
    """Perform basic sanity checks on the data in the database. This is by no means exhaustive but may help
    identify inconsistencies that violate basic constraints of the data.
    This function raises a ValueError if it finds an inconsistency, at which point the database
    could be considered corrupted."""
    with db_handle.connect() as conn:
        images = pd.read_sql_table("images", db_handle)
        extracted_sources = pd.read_sql_table("extracted_sources", db_handle)

        # Validate that the number of unique `src_id`s matches the expected number of new sources
        # based on the new sources (where parent is -1) plus the number of duplicates.
        nr_new_sources = (extracted_sources["parent"] == -1).sum() + extracted_sources[
            "is_duplicate"
        ].sum()
        nr_unique_src_ids = len(np.unique(extracted_sources["src_id"]))
        if nr_new_sources != nr_unique_src_ids:
            raise ValueError(
                """The number of source ids does not match the expected amount
                based on the number of duplicates and parentless sources.
                """
            )

        # Validate the number of images matches the im_id column
        nr_rejected_images = images["rejected"].sum()
        nr_images_referenced_by_sources = len(np.unique(extracted_sources["im_id"]))
        if (len(images) - nr_rejected_images) != nr_images_referenced_by_sources:
            raise ValueError(
                """The number of `im_id`s does not match the number of images
                in the images table, even if corrected for rejected images.
                """
            )

        # Validate that the sources are positioned inside the expected sky area.
        # Note: currently hardcoded to match test data, though this reduced flexibility
        #       of the database verification utility. I was considering using astropy
        #       to read the bounding box of the image each source is located in, but
        #       to save storage not all 60 images of the test db are stored in the data
        #       folder, so this info is currently not available.
        if (
            extracted_sources["ra"].min() < 56
            or extracted_sources["dec"].min() < 63
            or extracted_sources["ra"].max() > 67
            or extracted_sources["dec"].max() > 68
        ):
            raise ValueError(
                """Some sources are outside of the expected coordinates of the test data.
                """
            )
