.. _database_reference:

Database reference
------------------

The export database has the following tables:

 - config: contains the input parameters of the TraP run
 - images: contains information on the input images
 - extracted_sources: contains information on each extracted source

Config
======
.. _database_reference_config:

This table stores the arguments that were used in the TraP run.
The input parameters are defined here: :ref:`Input arguments <input_arguments>`.
Note that some arguments like the database password are not stored in the config tabel.
Arguments that are not exported have a note about that in the description.

Images
======
.. _database_reference_images:

This table contains metadata and some calculated properties for each input image.

 - **id** (*int*): The index of the image
 - **rejected** (*bool*): If True, the image was ignored and not processed because of it did not meet the required quality.
 - **rms** (*float*): The Root Mean Squared value of the center region of the image, used for quality control.
 - **rms_min** (*float*): The minimum Root Mean Squared value in the source extraction region.
 - **rms_max** (*float*): The maximum Root Mean Squared value in the source extraction region.
 - **freq_eff** (*float*): Effective frequency of the image in Hz. That is, the mean frequency of all the visibility data which comprises this image. Note that FITS files the header keywords representing the effective frequency are not uniquely defined and may differ per FITS file.
 - **freq_bw** (*float*): The frequency bandwidth of this image in Hz.
 - **taustart_ts** (*float*): The timestamp of the start of the observation.
 - **url** (*str*): The location of the image at the time of processing.
 - **rb_smaj** (*float*): The semi-major axis of the restoring beam, in degrees.
 - **rb_smin** (*float*): The semi-minor axis of the restoring beam, in degrees.
 - **rb_pa** (*float*): The position angle of the restoring beam (from north to east to the major axis), in degrees.
 - **centre_ra** (*float*): The right-ascension component of the central coordinate (J2000) (or pointing centre) of the region, in degrees.
 - **centre_dec** (*float*): The declination component of the central coordinate (J2000) (or pointing centre) of the region, in degrees.
 - **xtr_radius** (*float*): The radius of the circular mask used for source extraction, in degrees. #FIXME: turn pixels in degrees

Extracted_sources
=================
.. _database_reference_extracted_sources:

In each image we search for sources. Every source that is found by the source finder is fitted with a gaussian and a bunch of properties are calculated.
This table contains these parameters for all the source fits that were performed.

When we talk about an `extracted source`, we refer to a source that was extracted from a particular image.
A non-transient source will occur in more than one image but it is extracted from every image and hence fitted
in each image where it has it's own parameters. A source in a light curve will have a different flux value
in each image for example, and this extracted sources table table stores the information of every source found in every image.
A trivial example: if there are 10 sources in the observed patch of sky and there are 5 input images, we can expect 50 entries
into this extracted sources table. Each of the 10 sources in the sky will have a unique ``src_id`` and each image will have a
corresponding ``im_id``.

 - **id** (*int*): The index of the extracted source, unique for each source in a specific image.
 - **ra** (*float*): The right-ascension component of the estimated center of the source (in J2000) as estimated by the source finder.
 - **dec** (*float*): The declination component of the estimated center of the source (in J2000) as estimated by the source finder.
 - **ra_fit_err** (*float*): The 1-sigma error on ``ra`` (in degrees) from the source gaussian fitting, calculated by the source finder. It is important to note that a source’s fitted ``ra`` error increases towards the poles, and is thus declination dependent (see also ``error_radius``).
 - **dec_fit_err** (*float*): The 1-sigma error from the source fitting for ``dec`` (in degrees), calculated by the source finder (see also ``error_radius``).
 - **peak_flux** (*float*): The peak flux (Jy), as calculated by the source finder
 - **peak_flux_err** (*float*): The 1-sigma error in the ``peak_flux`` (Jy), as calculated by the source finder
 - **int_flux** (*float*): The integrated flux (Jy), as calculated by the source finder
 - **int_flux_err** (*float*): The 1-sigma error in the ``int_flux`` (Jy), as calculated by the source finder
 - **significance_detection_level** (*float*): The significance level of the detection: :math:`20 * f_{peak}/det_{sigma}` provides the detection RMS. See: `Spreeuw (2010) <https://dare.uva.nl/search?arno.record.id=340633>`_.
 - **semimajor_axis** (*float*): Semi-major axis that was used for gauss fitting (arcsec), calculated by the source finder.
 - **semiminor_axis** (*float*): Semi-minor axis that was used for gauss fitting (arcsec), calculated by the source finder.
 - **parallactic_angle** (*float*): Position angle that was used for gauss fitting (from north through local east, in degrees), calculated by the source finder.
 - **ew_sys_err** (*float*): The systematic error on ``ra`` (arcsec). This is an on-sky angular uncertainty, independent of declination. It differs per telescope. A larger systematic error can also be used to account for ionospheric effects on source position between images, allowing for more positional flexibility when determining the associated source. Larger systematic errors do increase the likelyhood that a sidelobe is matched with the main source or vice versa.
 - **ns_sys_err** (*float*): Same as ``ew_sys_err`` but on ``dec``.
 - **error_radius** (*float*): Estimate of the absolute angular error on a source’s central position (arcsec). It is a pessimistic estimate, because it takes the sum of the error along the X and Y axes.
 - **gaussian_fit** (*bool*): Whether a gaussian was fit to the source.
 - **chisq** (*float*): Goodness of fit metrics for fitted Gaussian profiles. See `PySE's 'goodness_of_fit' function <https://github.com/transientskp/pyse/blob/a43b64d684775605051adf9f754bb0ce6eda3493/sourcefinder/measuring.py#L942>`_.
 - **reduced_chisq** (*float*): Same as ``chisq`` but divided by the number of pixels in the fitted gaussian
 - **uncertainty_ew** (*float*): The positional on-sky uncertainty in the east-west direction of the weighted mean ``ra`` (degrees). This value is calculated through :math:`\sqrt{(ew\_sys\_err^2 + error\_radius^2)}/3600`
 - **uncertainty_ns** (*float*): The positional on-sky uncertainty in the north-south direction of the weighted mean ``dec`` (degrees). This value is calculated through :math:`\sqrt{(ns\_sys\_err^2 + error\_radius^2)}/3600`
 - **im_id** (*int*): The index of the image in which this source was found. Matches the ``id`` of the :ref:`images table <database_reference_images>`
 - **src_id** (*int*): The index of the continuous source this extracted source is a part of in the context of a lightcurve. In some sense the extracted_source id is an intersection of the ``im_id`` (time axis) and the ``src_id`` (different sources in space).
 - **is_force_fit** (*bool*): If False, this source was extracted by the sourcefinder because it matched the given detection thresholds. If True, this source was fitted at a pre-deternimed location, either because the user specified this location or because a source was recently found in this location.
 - **is_duplicate** (*bool*): When multiple extracted sources are matched to the same known source, the one with the smalles De Ruiter radius is considered to be the continuation of that known source and the others are considered to be duplicates. If this extracted source is such a duplicate, ``is_duplicate`` is set to True.
 - **parent** (*int*): The index of the extracted source with the same ``src_id`` that was found in the previous image. The index matches the ``id`` column of this table. If this extracted source is the first occurance for a given ``src_id``, there is no preceding extracte source hence ``parent`` is set to -1.
