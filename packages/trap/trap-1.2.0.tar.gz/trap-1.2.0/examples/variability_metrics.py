"""
Variability metrics
===================

This is an example on filtering the sources in a TraP export database to find the most variable sources.
This exmple starts with a TraP export database based on approximately 60 LOFAR 1.0 images at a 2 minute interval.
The first three of these images are available next to the export database file in the repository under tests/data/lofar1.

Let's start by opening the test database.

"""

# sphinx_gallery_thumbnail_number = 2
import trap

db_path = "../tests/data/lofar1/GRB201006A_60_images.db"
db_handle = trap.io.open_db("sqlite", db_path)

# %%
#
# There are two parameters we will use for describing the variability of a source:
#
#  - The **reduced weighted** :math:`\chi ^2 (\eta)`: This is a fit to the light curve.
#    The larger the value the less well it fits to a horizontal line and thus the more variable the source is.
#  - The **coefficient of variation** (:math:`V`): This is the magnitude of the fuxe density variation in the lightcurve.
#    The larger this value, the larger the variation in the flux densidty measurements and thus the more variable the source is.
#
# The sources we are after in this example are those that score high on both of these metrics.
#
# We can calculate these variability metrics by first constructing the lightcurves and then determining the variability within these
# lightcurves. Conevniently, we can use the post-processing function :func:`trap.post_processing.construct_varmetric` to
# do this for us

from trap.post_processing import construct_varmetric

varmetric_table = construct_varmetric(db_handle)

# %%
#
# Let's see what this gives us
#
print(varmetric_table.head())

# %%
#
# From this table, we will select only those sources (rows) where v_int i larger than zero.
# Now that we have the variability metrics, we can create a plot showing the distribution of
# the variablility values.
#

varmetric_table = varmetric_table[varmetric_table.v_int > 0]

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import NullFormatter


def plot_variability():
    left = bottom = 0.1
    width = height = 0.65
    bottom_h = left_h = left + width + 0.02
    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width, 0.2]
    rect_histy = [left_h, bottom, 0.2, height]
    fig = plt.figure(1, figsize=(12, 11))
    ax_scatter = fig.add_subplot(223, position=rect_scatter)
    plt.xlabel(r"Recuced weighted $\chi^2$", fontsize=20)
    plt.ylabel("Coefficient of variation", fontsize=20)
    ax_histx = fig.add_subplot(221, position=rect_histx)
    ax_histy = fig.add_subplot(224, position=rect_histy)
    ax_histx.xaxis.set_major_formatter(NullFormatter())
    ax_histy.yaxis.set_major_formatter(NullFormatter())
    ax_histx.axes.yaxis.set_ticklabels([])
    ax_histy.axes.xaxis.set_ticklabels([])
    xdata_var = np.log10(varmetric_table["eta_int"])
    ydata_var = np.log10(varmetric_table["v_int"])
    ax_scatter.scatter(xdata_var, ydata_var, s=10)
    ax_histx.hist(xdata_var, bins=30, histtype="stepfilled", color="b")
    ax_histy.hist(
        ydata_var, bins=30, histtype="stepfilled", color="b", orientation="horizontal"
    )
    xmin = int(min(xdata_var) - 1.1)
    xmax = int(max(xdata_var) + 1.1)
    ymin = int(min(ydata_var) - 1.1)
    ymax = int(max(ydata_var) + 1.1)
    xvals = range(xmin, xmax)
    yvals = range(ymin, ymax)
    xtxts = [r"$10^{" + str(a) + "}$" for a in xvals]
    ytxts = [r"$10^{" + str(a) + "}$" for a in yvals]
    ax_scatter.set_xlim([xmin, xmax])
    ax_scatter.set_ylim([ymin, ymax])
    ax_scatter.set_xticks(xvals)
    ax_scatter.set_xticklabels(xtxts, fontsize=20)
    ax_scatter.set_yticks(yvals)
    ax_scatter.set_yticklabels(ytxts, fontsize=20)
    ax_histx.set_xlim(ax_scatter.get_xlim())
    ax_histy.set_ylim(ax_scatter.get_ylim())
    return ax_scatter, ax_histx, ax_histy


ax_scatter, ax_histx, ax_histy = plot_variability()
plt.show()
# %%
#
# Since we want to select only the sources that score high on both variability metrics,
# we can define a cutoff threshold and select only those sources that are above both thresholds.
#
sigmaThresh = 1.3
from scipy.stats import norm


def SigmaFit(data):
    median = np.median(data)
    std_median = np.sqrt(np.mean([(i - median) ** 2.0 for i in data]))
    tmp_data = [
        a
        for a in data
        if a < 3.0 * std_median + median and a > median - 3.0 * std_median
    ]
    param1 = norm.fit(tmp_data)
    param2 = norm.fit(data)
    return param1, param2


paramx, paramx2 = SigmaFit(np.log10(varmetric_table["eta_int"]))
paramy, paramy2 = SigmaFit(np.log10(varmetric_table["v_int"]))
print(
    "Gaussian Fit eta: "
    + str(round(10.0 ** paramx[0], 2))
    + "(+"
    + str(round((10.0 ** (paramx[0] + paramx[1]) - 10.0 ** paramx[0]), 2))
    + " "
    + str(round((10.0 ** (paramx[0] - paramx[1]) - 10.0 ** paramx[0]), 2))
    + ")"
)
print(
    "Gaussian Fit V: "
    + str(round(10.0 ** paramy[0], 2))
    + "(+"
    + str(round((10.0 ** (paramy[0] + paramy[1]) - 10.0 ** paramy[0]), 2))
    + " "
    + str(round((10.0 ** (paramy[0] - paramy[1]) - 10.0 ** paramy[0]), 2))
    + ")"
)
sigcutx = paramx[1] * sigmaThresh + paramx[0]
sigcuty = paramy[1] * sigmaThresh + paramy[0]
print("eta threshold = " + str(round(10.0**sigcutx, 2)))
print("V threshold = " + str(round(10.0**sigcuty, 2)))

# %%
#
# Let's make the same plot again, but show the cutoff line we just calculated.
#

ax_scatter, ax_histx, ax_histy = plot_variability()
ax_histx.axvline(x=sigcutx, linewidth=2, color="k", linestyle="--")
ax_histy.axhline(y=sigcuty, linewidth=2, color="k", linestyle="--")
ax_scatter.axhline(y=sigcuty, linewidth=2, color="k", linestyle="--")
ax_scatter.axvline(x=sigcutx, linewidth=2, color="k", linestyle="--")
plt.show()

# %%
#
# To see what the sources look like, let's select the sources from the varmetric_table that
# are above both thresholds and plot the lightcurves next to the image. In the image we can
# plot the location of the source. Since the source is fitted in every image the location
# can vary a bit per image. We could plot the mean position, but it is also informative to
# plot all locations the source was found to view the spread.
#

import os
from pathlib import Path

import astropy
from astropy.io import fits
from astropy.wcs import WCS
from matplotlib.patches import Ellipse
from pandas import read_sql_query, read_sql_table

from trap.post_processing import construct_lightcurves

image_size = 150  # How many pixels to plot of the image. A larger size here means more zoomed out

# Select the sources above both cutoffs
variables = varmetric_table.loc[
    (varmetric_table["eta_int"] >= 10.0**sigcutx)
    & (varmetric_table["v_int"] >= 10.0**sigcuty)
]

lightcurves = construct_lightcurves(db_handle, attribute="int_flux")
lightcurves = lightcurves.loc[variables.index]
lightcurves_err = construct_lightcurves(db_handle, attribute="int_flux_err")
lightcurves_err = lightcurves_err.loc[variables.index]
is_force_fit = construct_lightcurves(db_handle, attribute="is_force_fit")
is_force_fit = is_force_fit.loc[variables.index]
images = read_sql_table("images", db_handle)
acquisition_times = images.taustart_ts

image_handle = fits.open(
    "../tests/data/lofar1/GRB201006A_final_2min_srcs-t0000-image-pb.fits"
)[0]
image_data = image_handle.data[0][0]
wmap = WCS(image_handle.header, naxis=2)

for id in lightcurves.index:
    fig = plt.figure(figsize=(16, 8))
    ax1 = fig.add_subplot(121)
    ax1.plot(acquisition_times, lightcurves.loc[id], color="k")
    for im_id, im_name in enumerate(lightcurves.columns):
        ax1.errorbar(
            acquisition_times[im_id],
            lightcurves.loc[id].to_numpy()[im_id],
            yerr=lightcurves_err.loc[id].to_numpy()[im_id],
            fmt="o",
            markersize=3,
            linestyle="-",
            color="r" if is_force_fit.loc[id].to_numpy()[im_id] else "b",
        )
    ax1.axhline(y=0.0, color="k", linestyle=":")
    ax1.tick_params(axis="x", labelrotation=90)
    ax1.set_ylabel("Flux density (Jy)")
    ax1.set_xlabel("Time")
    ax1.set_title("Source lightcurve")
    max_flux_i = np.argmax(lightcurves.loc[id])
    ax2 = fig.add_subplot(122, projection=wmap)
    ax2.imshow(
        image_data,
        # origin="lower",
        cmap="gray_r",
        # interpolation="nearest",
        vmin=np.percentile(image_data, 2),
        vmax=np.percentile(image_data, 99),
    )

    # Select the extraction locations for these sources at every image they were found at
    with db_handle.connect() as db_conn:
        source_query = (
            f"SELECT ra,dec,src_id FROM extracted_sources WHERE src_id == {id};"
        )
        sources = read_sql_query(source_query, db_conn)

        total_nr_sources = sources["src_id"].max()
        for i in range(0, int(total_nr_sources)):
            im = ax2.scatter(
                sources.ra,
                sources.dec,
                marker="o",
                facecolors="none",
                edgecolors="red",
                linewidth=2,
                transform=ax2.get_transform("fk5"),
            )
            median_ra = np.median(sources.ra)
            median_dec = np.median(sources.dec)
            px, py = wmap.wcs_world2pix(median_ra, median_dec, 1)
            ax2.set_xlim(px - image_size // 2, px + image_size // 2)
            ax2.set_ylim(py - image_size // 2, py + image_size // 2)

    ax2.coords[0].set_format_unit(astropy.units.deg)
    ax2.coords[1].set_format_unit(astropy.units.deg)
    ax2.set_xlabel("Right Ascension (deg)")
    ax2.set_ylabel("Declination (deg)")
    ax2.set_title("Source location")
    plt.show()

# %%
#
# When observing these plots, several of them look like there is no source at the red markings.
# This is not a fluke. In these cases there was a source but since we just show the first image,
# the source was not present at that locaton in the first image. In most of these cases,
# the source moved (maybe satellite?) and can sometimes still be seen in the image but at a different
# location. This becomes more obvious when inspecting the zoomed in plot for multiple images,
# but we cannot show that in this example because we only have access to a few of the input images here
# to save space. I encourage you to run this example script on data you ran on your own machine and
# see if you can identify the image the source was brightest at (using the im_id) and plot that image
# instead of simply the first image in the batch like we do here.
#
