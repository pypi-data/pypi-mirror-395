from scipy.constants import N_A
import numpy as np
import pandas as pd
import ucat
import scipy.optimize
import xarray as xr

import ddeq


def haversine_fct(lon1, lat1, lon2, lat2):

    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    # Radius of earth in kilometers is 6371
    km = 6371 * c

    return km


def extract_slices(
    l2_data,
    tracer_gas,
    lat_pt,
    lon_pt,
    vec_wind_pt,
    slice_width,
    window_length,
    alignment="left",
):
    """\
    Function called by lcs.estimate_line_densities

    if alignment=='left':
        lat_pt,lon_pt are the coords of the estimated source
        Used at the beggining of the estimation process. Cut a data slice of
        width "slice_width" and length "window_length" orthogonal to the wind at
        the source and whose one edge contains the source and the other one is
        located downwind at the distance of "slice_width" from the source.

    if alignment=='center':
        lat_pt,lon_pt are the coords of an enhancement detected within the
        function lcs.estimate_line_densities. Once enhancements close to a given
        source are selected, this function extracts a data slice of width
        "slice_width" and length "window_length" centered on the enhancement and
        orthogonal to the wind direction at the enhancement 

    # OUTPUTS:

    ii_slice: indexes of the pixels of the l2_data that are selected 1) for
        detecting the enhancements close to the source (alignment=left) and for
        the process of Gaussian fitting (alignment=left)
    geom_slice: Points describing the along-wind and across-wind lines defining
        the extracted slice of data
    """
    # Precision of the sampling of the different lines
    dlonlat = 0.01

    # For the conversion km to lat/lon
    dlon = haversine_fct(lon_pt, lat_pt, lon_pt + 1, lat_pt)  # deg lon => km
    dlat = haversine_fct(0.0, 0.0, 0.0, 1.0)  # deg lat => km

    vec_wind = vec_wind_pt.copy()
    orth_vec_wind = np.array([vec_wind[1], -1 * vec_wind[0]])

    # Conversion coords km to lat/lon units
    vec_wind[0] = vec_wind[0] / dlon
    vec_wind[1] = vec_wind[1] / dlat
    orth_vec_wind[0] = orth_vec_wind[0] / dlon
    orth_vec_wind[1] = orth_vec_wind[1] / dlat

    # Ranges of lats and lons of the data window
    extent_lon = window_length / 2.0 / dlon
    min_lon = lon_pt - extent_lon
    max_lon = lon_pt + extent_lon
    extent_lat = window_length / 2.0 / dlon
    min_lat = lat_pt - extent_lat
    max_lat = lat_pt + extent_lat

    # We separate latitudinal and longitudinal wind cases
    longit_wind = abs(vec_wind[0]) >= abs(vec_wind[1])

    #  Case longitudinal wind
    if longit_wind:
        #   Equation of the along wind line
        #   lat=vec_wind[1]/vec_wind[0](lon-lon_pt)+lat_pt
        alongw_lons = np.arange(min_lon, max_lon, dlonlat)
        alongw_lats = vec_wind[1] / vec_wind[0] * (alongw_lons - lon_pt) + lat_pt

    #  Case latitudinal wind
    else:
        alongw_lats = np.arange(min_lat, max_lat, dlonlat)
        alongw_lons = vec_wind[0] / vec_wind[1] * (alongw_lats - lat_pt) + lon_pt

    # Determining end points defining the along-wind segment defining the data
    # slice
    # if alignment is left:
    #     segment end points are the ref point and the downwind point at a
    #     distance of slice width
    # if aligment is center:
    #     segment end points are the up/downwind points at distances of
    #     slice_width / 2.0 of the reference point
    #
    # Selection of upwind and downwind points of along-wind line passing through
    # the ref point
    if longit_wind:
        if vec_wind[0] > 0:

            # If plume direction is towards increasing longitudes
            dw_lons = alongw_lons[alongw_lons >= lon_pt]
            dw_lats = alongw_lats[alongw_lons >= lon_pt]
            upwind_lons = alongw_lons[alongw_lons < lon_pt]
            upwind_lats = alongw_lats[alongw_lons < lon_pt]
        else:
            dw_lons = alongw_lons[alongw_lons <= lon_pt]
            dw_lats = alongw_lats[alongw_lons <= lon_pt]
            upwind_lons = alongw_lons[alongw_lons > lon_pt]
            upwind_lats = alongw_lats[alongw_lons > lon_pt]
    else:
        if vec_wind[1] > 0:
            # If plume direction is towards increasing latitudes
            dw_lons = alongw_lons[alongw_lats >= lat_pt]
            dw_lats = alongw_lats[alongw_lats >= lat_pt]
            upwind_lons = alongw_lons[alongw_lats < lat_pt]
            upwind_lats = alongw_lats[alongw_lats < lat_pt]
        else:
            dw_lons = alongw_lons[alongw_lats <= lat_pt]
            dw_lats = alongw_lats[alongw_lats <= lat_pt]
            upwind_lons = alongw_lons[alongw_lats > lat_pt]
            upwind_lats = alongw_lats[alongw_lats > lat_pt]

    ends_alongw_lons = []
    ends_alongw_lats = []

    if alignment == "left":

        end_dist_arr = [0, slice_width]

        alongw_dist_arr = []
        for ii in range(len(dw_lons)):
            tmp_dist = haversine_fct(lon_pt, lat_pt, dw_lons[ii], dw_lats[ii])
            alongw_dist_arr.append(tmp_dist)

        alongw_dist_arr = np.array(alongw_dist_arr)

        for end_dist in end_dist_arr:
            ii_end = np.argmin(np.abs(end_dist - alongw_dist_arr))

            ends_alongw_lons.append(dw_lons[ii_end])
            ends_alongw_lats.append(dw_lats[ii_end])

    if alignment == "center":

        # The first end point is at slice_width/2. upwind distance from the fit point
        alongw_dist_arr = []
        for ii in range(len(upwind_lons)):
            tmp_dist = haversine_fct(lon_pt, lat_pt, upwind_lons[ii], upwind_lats[ii])
            alongw_dist_arr.append(tmp_dist)

        alongw_dist_arr = np.array(alongw_dist_arr)

        ii_end = np.argmin(np.abs(slice_width / 2.0 - alongw_dist_arr))

        ends_alongw_lons.append(upwind_lons[ii_end])
        ends_alongw_lats.append(upwind_lats[ii_end])

        # The second end point is at slice_width/2. downwind distance from the fit point
        alongw_dist_arr = []
        for ii in range(len(dw_lons)):
            tmp_dist = haversine_fct(lon_pt, lat_pt, dw_lons[ii], dw_lats[ii])
            alongw_dist_arr.append(tmp_dist)

        alongw_dist_arr = np.array(alongw_dist_arr)

        ii_end = np.argmin(np.abs(slice_width / 2.0 - alongw_dist_arr))

        ends_alongw_lons.append(dw_lons[ii_end])
        ends_alongw_lats.append(dw_lats[ii_end])

    # Determining end points defining the across-wind segment defining the data slice
    # - if alignment is left: segment end points are the ref point and the downwind point
    # at a distance of slice width
    # - if aligment is center: segment end points are the up/downwind points at distances of
    #  slice_width/2. of the reference point
    acrossw_lons = [None, None]
    acrossw_lats = [None, None]

    #   Equation of the across wind line
    #   lat=orth_vec_wind[1]/orth_vec_wind[0](lon-lon_pt)+lat_pt
    if longit_wind:
        acrossw_lats[0] = acrossw_lats[1] = np.arange(min_lat, max_lat, dlonlat)
        acrossw_lons[0] = (
            orth_vec_wind[0]
            / orth_vec_wind[1]
            * (acrossw_lats[0] - ends_alongw_lats[0])
            + ends_alongw_lons[0]
        )
        acrossw_lons[1] = (
            orth_vec_wind[0]
            / orth_vec_wind[1]
            * (acrossw_lats[1] - ends_alongw_lats[1])
            + ends_alongw_lons[1]
        )
    else:
        acrossw_lons[0] = acrossw_lons[1] = np.arange(min_lon, max_lon, dlonlat)
        acrossw_lats[0] = (
            orth_vec_wind[1]
            / orth_vec_wind[0]
            * (acrossw_lons[0] - ends_alongw_lons[0])
            + ends_alongw_lats[0]
        )
        acrossw_lats[1] = (
            orth_vec_wind[1]
            / orth_vec_wind[0]
            * (acrossw_lons[1] - ends_alongw_lons[1])
            + ends_alongw_lats[1]
        )

    # We select points that are at a distance of window_length/2. of the pt
    # following the across-wind direction
    acrossw_dist_arr = []
    for ii in range(len(acrossw_lons[0])):
        acrossw_dist_arr.append(
            haversine_fct(
                ends_alongw_lons[0],
                ends_alongw_lats[0],
                acrossw_lons[0][ii],
                acrossw_lats[0][ii],
            )
        )
    acrossw_dist_arr = np.array(acrossw_dist_arr)
    ii_ends = np.argsort(np.abs(acrossw_dist_arr - window_length / 2.0))

    if (ii_ends[1] - ii_ends[0]) == 1:
        # print('PB WITH RESOLUTION')
        ii_slice = []
        geom_slice = []
        return ii_slice, geom_slice

    ends_acrossw_lons = [None, None]
    ends_acrossw_lats = [None, None]

    ends_acrossw_lons[0] = acrossw_lons[0][ii_ends[0]]
    ends_acrossw_lats[0] = acrossw_lats[0][ii_ends[0]]

    ends_acrossw_lons[1] = acrossw_lons[0][ii_ends[1]]
    ends_acrossw_lats[1] = acrossw_lats[0][ii_ends[1]]

    # Selection of the data between the 2 across-wind lines
    # To perform this task, we use the cross-products of
    # the vector defining the edges, i.e orth_vec_wind and
    # the vectors defined by the ref points of the edges and the data point
    v1 = orth_vec_wind
    v2 = (
        ends_alongw_lons[1] - ends_alongw_lons[0],
        ends_alongw_lats[1] - ends_alongw_lats[0],
    )
    xp = v1[0] * v2[1] - v1[1] * v2[0]  # Cross product
    ref_sign = np.sign(xp)

    # Data points which are between the 2 edges are defined by a cross product
    # with a sign as ref_sign
    v2_arr = (
        l2_data["lon"].data - ends_alongw_lons[0],
        l2_data["lat"].data - ends_alongw_lats[0],
    )
    xp_arr_1 = np.sign(v1[0] * v2_arr[1] - v1[1] * v2_arr[0])  # Cross product

    v2_arr = (
        l2_data["lon"].data - ends_alongw_lons[1],
        l2_data["lat"].data - ends_alongw_lats[1],
    )
    xp_arr_2 = np.sign(v1[0] * v2_arr[1] - v1[1] * v2_arr[0])  # Cross product

    # Selection of the data between the 2 along-wind lines
    v1 = vec_wind
    v2 = (
        ends_acrossw_lons[1] - ends_acrossw_lons[0],
        ends_acrossw_lats[1] - ends_acrossw_lats[0],
    )
    xp = v1[0] * v2[1] - v1[1] * v2[0]  # Cross product
    orth_ref_sign = np.sign(xp)

    # Data points which are between the 2 edges are defined by a cross product
    # with a sign as ref_sign
    v2_arr = (
        l2_data["lon"].data - ends_acrossw_lons[0],
        l2_data["lat"].data - ends_acrossw_lats[0],
    )
    orth_xp_arr_1 = np.sign(v1[0] * v2_arr[1] - v1[1] * v2_arr[0])  # Cross product
    v2_arr = (
        l2_data["lon"].data - ends_acrossw_lons[1],
        l2_data["lat"].data - ends_acrossw_lats[1],
    )
    orth_xp_arr_2 = np.sign(v1[0] * v2_arr[1] - v1[1] * v2_arr[0])  # Cross product

    # Selection of the data between the 2 across-wind edges
    # and the 2 along-wind lines
    ii_slice = (
        (xp_arr_1 == ref_sign)
        & (xp_arr_2 == -ref_sign)
        & (orth_xp_arr_1 == orth_ref_sign)
        & (orth_xp_arr_2 == -orth_ref_sign)
    )

    geom_slice = {}
    geom_slice["dw_lons"] = dw_lons
    geom_slice["dw_lats"] = dw_lats
    geom_slice["upwind_lons"] = upwind_lons
    geom_slice["upwind_lats"] = upwind_lats
    geom_slice["ends_alongw_lons"] = ends_alongw_lons
    geom_slice["ends_alongw_lats"] = ends_alongw_lats
    geom_slice["acrossw_lons"] = acrossw_lons
    geom_slice["acrossw_lats"] = acrossw_lats

    return ii_slice, geom_slice


def estimate_line_densities(
    source, l2_data, wind_xr, lcs_params, tracer_gas="CO2", fit_background=True
):
    """\
    Estimates line densities close to a given source.
    Proceeds as follows:

    1) A data slice, which width is the distance travelled by the wind in one
    hour from the source and which length is defined by
    lcs_params['window_length'], is extracted from the "l2_data" by the function
    lcs.extract_slices. Of note that this slice is orthogonal to the wind at the
    source and contains the data downwind the source.

    2) Potential enhancements are detected close to the "source".
    Enhancements are defined as the data values minus the mean of the data
    contained within the slice. Only enhancements characterized by
    enhancement > lcs_params['Enhancement_thresh'] * std(data_slice) and by a
    distance to the along-wind line lower than 10 km are selected.

    3) Data slices of width lcs_params['fit_pt_slice_width'] centered on the
    selected enhancements are extracted by the function lcs.extract_slices.

    4) Gaussian fittings are performed on the extracted data slices

    #OUTPUTS:
    res_line_densities: Dictionnary with most of quantities characterizing the
    line densities (wind at the fitted point, parameters of the Gaussian
    fitting, ...).
    """
    verbose = lcs_params["verbose"]

    # Parameters of the algorithm
    window_length = lcs_params["window_length"]
    n_min_fit_pts = lcs_params["n_min_fit_pts"]
    fit_pt_slice_width = lcs_params["fit_pt_slice_width"]
    Enhancement_thresh = lcs_params["Enhancement_thresh"]

    res_line_densities = {}
    check_flag = 0

    lds = []  # Array where line densities are stored

    # function for fitting the line density
    fit_func = ddeq.functions.gauss

    # Wind at the source
    lon_source, lat_source, _ = ddeq.sources.get_location(source)
    lon_source = float(lon_source[0])
    lat_source = float(lat_source[0])

    # Function which extracts the wind at the given point
    src_vec_wind = ddeq.wind.get_wind_at_location(wind_xr, lon_source, lat_source)
    vec_wind = src_vec_wind.copy()
    orth_vec_wind = np.array([vec_wind[1], -1 * vec_wind[0]])

    # For the conversion km to lat/lon
    dlon = haversine_fct(
        lon_source, lat_source, lon_source + 1, lat_source
    )  # deg lon => km
    dlat = haversine_fct(0.0, 0.0, 0.0, 1.0)  # deg lat => km

    tmp_vec_wind = vec_wind.copy()
    tmp_orth_vec_wind = orth_vec_wind.copy()

    # Conversion coords km to lat/lon units
    tmp_vec_wind[0] = vec_wind[0] / dlon
    tmp_vec_wind[1] = vec_wind[1] / dlat

    tmp_orth_vec_wind[0] = orth_vec_wind[0] / dlon
    tmp_orth_vec_wind[1] = orth_vec_wind[1] / dlat

    # Slice width is fixed as the distance travelled by the wind during one hour
    norm_wind = np.sqrt(src_vec_wind[0] ** 2 + src_vec_wind[1] ** 2)
    slice_width = float(norm_wind * 3.6)  # km
    if slice_width < fit_pt_slice_width:
        slice_width = fit_pt_slice_width  # For weak winds, this guarantees to have a window with enough pixels

    # WE BUILD A SLICE ORTHOGONAL TO THE WIND DIRECTION AT THE SOURCE
    ij_window, geom_window = extract_slices(
        l2_data,
        tracer_gas,
        lat_source,
        lon_source,
        vec_wind,
        slice_width,
        window_length,
        alignment="left",
    )

    data_window = l2_data[tracer_gas].data[ij_window]
    bool_cond = ~np.isnan(data_window)
    data_window = data_window[bool_cond]

    if np.any(np.isinf(data_window)):
        return res_line_densities

    # Check if data
    # We need at least n_min_fit_pts points in order to perform the regression
    if len(data_window) < n_min_fit_pts:
        if verbose:
            print("No enough points: " + str(len(data_window)))
        return res_line_densities

    window_lons = l2_data["lon"].data[ij_window]
    window_lats = l2_data["lat"].data[ij_window]

    data_window_std = l2_data[tracer_gas + "_std"].data[ij_window]
    p_surf = l2_data["psurf"].data[ij_window]

    window_lons = window_lons[bool_cond]
    window_lats = window_lats[bool_cond]

    data_window_std = data_window_std[bool_cond]
    p_surf = p_surf[bool_cond]

    if np.any(np.isinf(p_surf)):
        if verbose:
            print("PB WITH PRESSURE FIELDS")
        return res_line_densities

    # Index of the valid points
    ij_valid_arr = ij_window.flatten()
    ij_valid_arr = np.argwhere(ij_valid_arr == True)
    ij_valid_arr = ij_valid_arr[bool_cond]

    # We compute the distances of the pixels to the along-wind line
    centered_distances = np.zeros_like(window_lons)

    # We build a center line relative of the subtrack
    #
    # Equation of the across wind line
    # alongw_lats=vec_wind[1]/vec_wind[0]*(alongw_lons-lon_pt)+lat_pt
    # alongw_lons=vec_wind[0]/vec_wind[1]*(alongw_lats-lat_pt)+lon_pt
    refProjLat = (
        geom_window["ends_alongw_lats"][0] + geom_window["ends_alongw_lats"][1]
    ) / 2.0
    refProjLon = (
        geom_window["ends_alongw_lons"][0] + geom_window["ends_alongw_lons"][1]
    ) / 2.0

    # Longitudinal source winds
    if abs(tmp_vec_wind[0]) >= abs(tmp_vec_wind[1]):
        k = tmp_orth_vec_wind[0] / tmp_orth_vec_wind[1]
        b = refProjLon - k * refProjLat

        # Distances are computed wrt the middle point of the along-wind segment
        for ipt, projLat in enumerate(window_lats):
            projLon = k * projLat + b
            centered_distances[ipt] = np.sign(projLat - refProjLat) * haversine_fct(
                refProjLon, refProjLat, projLon, projLat
            )
    else:
        k = tmp_orth_vec_wind[1] / tmp_orth_vec_wind[0]
        b = refProjLat - k * refProjLon

        # Distances are computed wrt the middle point of the along-wind segment
        for ipt, projLon in enumerate(window_lons):
            projLat = k * projLon + b
            centered_distances[ipt] = np.sign(projLon - refProjLon) * haversine_fct(
                refProjLon, refProjLat, projLon, projLat
            )

    # SELECTING VALID ENHANCEMENTS
    #
    # enhancement = float(data_window[ipt]) - d_mean
    # enhancement>Enhancement_thresh*d_std
    #
    # In order to prevent the algorithm to detect plumes from another source,
    # we restrict the area of search of the enhancements around 10 km from the
    # along-wind direction

    tmp_ij_valid_arr = []
    pts_valid_arr = []

    refProjLat = (
        geom_window["ends_alongw_lats"][0] + geom_window["ends_alongw_lats"][1]
    ) / 2.0
    refProjLon = (
        geom_window["ends_alongw_lons"][0] + geom_window["ends_alongw_lons"][1]
    ) / 2.0

    d_std = np.std(data_window)
    d_mean = np.mean(data_window)

    for ipt in range(len(window_lons)):
        tmp_dist = haversine_fct(
            refProjLon, refProjLat, window_lons[ipt], window_lats[ipt]
        )

        if np.abs(centered_distances[ipt]) > fit_pt_slice_width:
            continue

        enhancement = float(data_window[ipt]) - d_mean

        if enhancement > Enhancement_thresh * d_std:
            tmp_ij_valid_arr.append(ij_valid_arr[ipt])
            pts_valid_arr.append(ipt)

    if len(pts_valid_arr) == 0:
        if verbose:
            print("NO VALID FIT PTS")
        return res_line_densities

    ij_valid_arr = tmp_ij_valid_arr

    for iel, ipt in enumerate(pts_valid_arr):

        lat_fit_pt = float(window_lats[ipt])
        lon_fit_pt = float(window_lons[ipt])

        vec_wind = ddeq.wind.get_wind_at_location(wind_xr, lon_fit_pt, lat_fit_pt)
        vec_track = np.array([vec_wind[1], -1 * vec_wind[0]])

        # Conversion coords km to lat/lon units
        dlon = haversine_fct(
            lon_fit_pt, lat_fit_pt, lon_fit_pt + 1, lat_fit_pt
        )  # deg lon => km
        dlat = haversine_fct(0.0, 0.0, 0.0, 1.0)  # deg lat => km

        # We select data that is a slice centered on the enhancement point with
        # a width of fit_pt_slice_width and height window width
        # The slice is othogonal to the wind at the point
        ij_slice, geom_slice = extract_slices(
            l2_data,
            tracer_gas,
            lat_fit_pt,
            lon_fit_pt,
            vec_wind,
            fit_pt_slice_width,
            window_length,
            alignment="center",
        )
        if len(ij_slice) == 0:
            if verbose:
                print("NO SLICE data cut")
            continue

        data_slice = l2_data[tracer_gas].data[ij_slice]
        bool_cond = np.isfinite(data_slice)
        data_slice = data_slice[bool_cond]

        # Check if enough data
        if len(data_slice) < n_min_fit_pts:
            if verbose:
                print("NO ENOUGH DATA WITHIN THE SLICE")
            continue

        slice_lons = l2_data["lon"].data[ij_slice]
        slice_lats = l2_data["lat"].data[ij_slice]

        data_slice_std = l2_data[tracer_gas + "_std"].data[ij_slice]

        slice_lons = slice_lons[bool_cond]
        slice_lats = slice_lats[bool_cond]
        data_slice_std = data_slice_std[bool_cond]

        #  We computed centered distances along the wind at the fit point
        #  For sake of precision, we separate cases with latitudinal and
        # longitudinal winds
        slice_centered_distances = np.zeros_like(slice_lons)

        # We build a center line relative of the subtrack
        # Equation of the across wind line
        # alongw_lats=vec_wind[1]/vec_wind[0]*(alongw_lons-lon_pt)+lat_pt
        # alongw_lons=vec_wind[0]/vec_wind[1]*(alongw_lats-lat_pt)+lon_pt
        tmp_vec_track = [None, None]
        tmp_vec_track[0] = vec_track[0] / dlon
        tmp_vec_track[1] = vec_track[1] / dlat

        tmp_vec_wind = [None, None]
        tmp_vec_wind[0] = vec_wind[0] / dlon
        tmp_vec_wind[1] = vec_wind[1] / dlat

        refProjLat = lat_fit_pt
        refProjLon = lon_fit_pt

        # Longitudinal source winds
        if abs(tmp_vec_wind[0]) >= abs(tmp_vec_wind[1]):
            k = tmp_vec_track[0] / tmp_vec_track[1]
            b = refProjLon - k * refProjLat

            # Distances are computed wrt the middle point of the along-wind segment
            for ipt2, projLat in enumerate(slice_lats):
                projLon = k * projLat + b
                slice_centered_distances[ipt2] = np.sign(
                    projLat - refProjLat
                ) * haversine_fct(refProjLon, refProjLat, projLon, projLat)
        else:
            k = tmp_vec_track[1] / tmp_vec_track[0]
            b = refProjLat - k * refProjLon

            # Distances are computed wrt the middle point of the along-wind segment
            for ipt2, projLon in enumerate(slice_lons):
                projLat = k * projLon + b
                slice_centered_distances[ipt2] = np.sign(
                    projLon - refProjLon
                ) * haversine_fct(refProjLon, refProjLat, projLon, projLat)

        # Longitudinal source winds
        #
        # Normalization of the enhancement
        # to ease the fit
        d_mean = np.mean(data_slice)
        d_std = np.std(data_slice)
        norm_data_slice = (data_slice - d_mean) / d_std
        norm_enhancement = (float(data_window[ipt]) - d_mean) / d_std

        # prior estimation of parameters
        prior_Gauss_std = 1.5
        prior_Gauss_A = prior_Gauss_std * norm_enhancement * (2 * np.pi) ** 0.5

        if fit_background:
            p0 = (
                prior_Gauss_A,  # line density
                prior_Gauss_std,  # standard width
                0,  # shift in across wind direction
                0,  # slope of background
                0,  # intercept of background
            )
        else:
            p0 = (
                prior_Gauss_A,  # line density
                prior_Gauss_std,  # standard width
                0,  # shift in across wind direction
            )

        try:
            popt, pcov = scipy.optimize.curve_fit(
                fit_func, slice_centered_distances, norm_data_slice, p0=p0
            )
        except (RuntimeError, scipy.optimize.OptimizeWarning):
            if verbose:
                print("PB WITH THE FIT")
            continue

        if (np.isnan(pcov[0, 0])) | (np.isinf(pcov[0, 0])):
            continue
        if pcov[0, 0] < 0:
            continue

        std_emis = np.sqrt(pcov[0, 0])
        popt[0] = abs(popt[0])
        popt[1] = abs(popt[1])
        sig = popt[1]  # sigma of the Gaussian (km)

        # Data of the peak
        bool_cond = (np.abs(slice_centered_distances - popt[1]) <= 3 * sig) & (
            norm_data_slice > 1
        )

        ii_peak = np.argwhere(bool_cond).flatten()

        data_peak = norm_data_slice[ii_peak]
        data_peak_distances = slice_centered_distances[ii_peak]

        # check the quality of the fit
        R2 = np.corrcoef(fit_func(data_peak_distances, *popt), data_peak)[0, 1] ** 2

        if (np.isnan(R2)) | (np.isinf(R2)):
            continue

        #  To compute the emissions, we rescale the amplitude of the Gaussian to
        #  the original scale
        std_emis = std_emis * d_std
        data_peak = data_peak * d_std + d_mean

        # We renormalize the amplitude of the Gaussian and of the linear term
        popt[0] = popt[0] * d_std

        if fit_background:
            popt[3] = popt[3] * d_std
            popt[4] = popt[4] + d_mean

        # unit vector
        vec_track = vec_track / np.sqrt(vec_track.dot(vec_track))

        lds.append(
            {
                "std_emis": std_emis,
                "ij_valid": ij_valid_arr[iel],
                "R2": R2,
                "popt": popt,
                "lat_pt_fit": lat_fit_pt,
                "lon_pt_fit": lon_fit_pt,
                "dlon": dlon,
                "dlat": dlat,
                "p_surf": float(p_surf[ipt]),
                "centered_distances": slice_centered_distances,
                "ij_slice": ij_slice,
                "vec_track": vec_track,
                "vec_wind": vec_wind,
            }
        )
        check_flag += 1

    if check_flag > 3:
        res_line_densities["line_densities"] = lds
        res_line_densities["ij_window"] = ij_window
        res_line_densities["src_vec_wind"] = src_vec_wind
        res_line_densities["orthw_lat_arr"] = geom_window["acrossw_lats"]
        res_line_densities["orthw_lon_arr"] = geom_window["acrossw_lons"]
        res_line_densities["alongw_lat_arr"] = geom_window["dw_lats"]
        res_line_densities["alongw_lon_arr"] = geom_window["dw_lons"]
        res_line_densities["ref_lon_arr"] = geom_window["ends_alongw_lons"]
        res_line_densities["ref_lat_arr"] = geom_window["ends_alongw_lats"]

        if verbose:
            print(str(len(lds)) + " LD found !")
    else:
        res_line_densities = {}

    return res_line_densities


def estimate_lds_with_constraint(
    gas, NO2_res_line_densities, l2_data, lcs_params, fit_background=True
):
    """\
    Estimate {gas} line densities with the Gaussian sigma that has been estimated
    when determining line densities for previous gas.
    """
    if not fit_background:
        raise NotImplementedError
    n_min_fit_pts = lcs_params["n_min_fit_pts"]
    verbose = lcs_params["verbose"]
    res_line_densities = {}
    check_flag = 0
    CO2_NO2_lds = []

    # Pixels corresponding to the window where NO2 enhancements are computed and
    # where NO2 line densities are computed
    ij_window = NO2_res_line_densities["ij_window"]
    NO2_lds = NO2_res_line_densities["line_densities"]

    data_CO2_1D = l2_data[
        gas
    ].data.flatten()  # <-For the computation of the enhancements
    data_window = l2_data[gas].data[ij_window]
    bool_cond = np.isfinite(data_window)
    data_window = data_window[bool_cond]

    #   Check if there is enough CO2 data.
    #   BEWARE: NO2 and CO2 data could have a different spatial distributions if CLOUDS.
    #
    # We need at least n_min_fit_pts points in order to perform the regression
    if len(data_window) < n_min_fit_pts:
        if verbose:
            print("No enough points: " + str(len(data_window)))
        return res_line_densities

    for i_ld, NO2_ld in enumerate(NO2_lds):

        ij_valid = NO2_ld["ij_valid"]
        if np.isnan(data_CO2_1D[ij_valid]):
            continue

        ij_slice = NO2_ld["ij_slice"]

        data_slice = l2_data["CO2"].data[ij_slice]
        bool_cond = np.isfinite(data_slice)
        data_slice = data_slice[bool_cond]

        #   Check if enough CO2 data
        #   BEWARE: NO2 and CO2 data could have a different spatial distributions if CLOUDS.
        #   -> We have to recompute the centered distances
        if len(data_slice) < n_min_fit_pts:
            if verbose:
                print("NO ENOUGH DATA WITHIN THE SLICE")
            continue

        slice_lons = l2_data["lon"].data[ij_slice]
        slice_lats = l2_data["lat"].data[ij_slice]
        data_slice_std = l2_data["CO2_std"].data[ij_slice]

        slice_lons = slice_lons[bool_cond]
        slice_lats = slice_lats[bool_cond]
        data_slice_std = data_slice_std[bool_cond]

        #  We computed new centered distances along the wind at the fit point
        slice_centered_distances = np.zeros_like(slice_lons)

        # We build a center line relative of the subtrack
        #
        # Equation of the across wind line
        # alongw_lats=vec_wind[1]/vec_wind[0]*(alongw_lons-lon_pt)+lat_pt
        # alongw_lons=vec_wind[0]/vec_wind[1]*(alongw_lats-lat_pt)+lon_pt
        tmp_vec_track = [None, None]
        vec_track = NO2_ld["vec_track"]

        # Conversion coords km to lat/lon units
        tmp_vec_track[0] = vec_track[0] / NO2_ld["dlon"]
        tmp_vec_track[1] = vec_track[1] / NO2_ld["dlat"]
        refProjLat = NO2_ld["lat_pt_fit"]
        refProjLon = NO2_ld["lon_pt_fit"]

        vec_wind = NO2_ld["vec_wind"]
        tmp_vec_wind = [None, None]
        tmp_vec_wind[0] = vec_wind[0] / NO2_ld["dlon"]
        tmp_vec_wind[1] = vec_wind[1] / NO2_ld["dlat"]

        # Longitudinal source winds
        if abs(tmp_vec_wind[0]) >= abs(tmp_vec_wind[1]):
            k = tmp_vec_track[0] / tmp_vec_track[1]
            b = refProjLon - k * refProjLat

            # Distances are computed wrt the middle point of the along-wind segment
            for ipt, projLat in enumerate(slice_lats):
                projLon = k * projLat + b
                slice_centered_distances[ipt] = np.sign(
                    projLat - refProjLat
                ) * haversine_fct(refProjLon, refProjLat, projLon, projLat)
        else:
            k = tmp_vec_track[1] / tmp_vec_track[0]
            b = refProjLat - k * refProjLon

            # Distances are computed wrt the middle point of the along-wind segment
            for ipt, projLon in enumerate(slice_lons):
                projLat = k * projLon + b
                slice_centered_distances[ipt] = np.sign(
                    projLon - refProjLon
                ) * haversine_fct(refProjLon, refProjLat, projLon, projLat)

        #  Retrieving parameters of the fit to the NO2 data
        NO2_popt = NO2_ld["popt"]

        # Defining the Gaussian fitting function for the CO2 data
        no2_sig = NO2_popt[1]
        no2_mu = NO2_popt[2]
        fit_func = ddeq.functions.FixedGaussCurve(no2_sig, no2_mu)

        # Normalization of the enhancement to ease the fit
        d_mean = np.mean(data_slice)
        d_std = np.std(data_slice)
        norm_data_slice = (data_slice - d_mean) / d_std
        norm_enhancement = (float(data_CO2_1D[ij_valid]) - d_mean) / d_std

        #  Prior values of the parameters of the Gaussian fitting function
        prior_Gauss_std = 1.5
        prior_Gauss_A = prior_Gauss_std * norm_enhancement * (2 * np.pi) ** 0.5

        p0 = (prior_Gauss_A, 0, 0)

        try:
            tmp_popt, pcov = scipy.optimize.curve_fit(
                fit_func, slice_centered_distances, norm_data_slice, p0=p0
            )

            popt = np.concatenate(([tmp_popt[0]], [no2_sig, no2_mu], tmp_popt[1:]))

            # Check if the fit is correct by assessing if uncertainties were indeed computed
            # or make sense (i.e. they are positive)
            if (np.isnan(pcov[0, 0])) | (np.isinf(pcov[0, 0])):
                continue
            if pcov[0, 0] < 0:
                continue

            std_emis = np.sqrt(pcov[0, 0])

            popt[0] = abs(popt[0])
            popt[1] = abs(popt[1])  # sigma of the Gaussian (km)
            sig = popt[1]

            # Data of the peak
            bool_cond = (np.abs(slice_centered_distances - popt[1]) <= 3 * sig) & (
                norm_data_slice > 1
            )

            ii_peak = np.argwhere(bool_cond).flatten()

            data_peak = norm_data_slice[ii_peak]
            data_peak_distances = slice_centered_distances[ii_peak]

            # check the quality of the fit
            R2 = (
                np.corrcoef(
                    ddeq.functions.gauss(data_peak_distances, *popt), data_peak
                )[0, 1]
                ** 2
            )

            if (np.isnan(R2)) | (np.isinf(R2)):
                continue

            #  To compute the emissions, we rescale the amplitude of the Gaussian to
            #  the original scale
            std_emis = std_emis * d_std
            data_peak = data_peak * d_std + d_mean

            # We renormalize the amplitude of the Gaussian
            popt[0] = popt[0] * d_std

            if fit_background:
                popt[3] = popt[3] * d_std
                popt[4] = popt[4] + d_mean

            CO2_NO2_lds.append(
                {
                    "std_emis": std_emis,
                    "R2": R2,
                    "popt": popt,
                    "lat_pt_fit": NO2_ld["lat_pt_fit"],
                    "lon_pt_fit": NO2_ld["lon_pt_fit"],
                    "dlat": NO2_ld["dlat"],
                    "dlon": NO2_ld["dlon"],
                    "p_surf": NO2_ld["p_surf"],
                    "centered_distances": slice_centered_distances,
                    "ij_slice": ij_slice,
                    "vec_track": NO2_ld["vec_track"],
                    "vec_wind": NO2_ld["vec_wind"],
                }
            )
            check_flag += 1

        except RuntimeError:
            if verbose:
                print("PB WITH THE FIT")
            continue

    if check_flag > 3:
        res_line_densities["line_densities"] = CO2_NO2_lds
        res_line_densities["ij_window"] = NO2_res_line_densities["ij_window"]
        res_line_densities["src_vec_wind"] = NO2_res_line_densities["src_vec_wind"]
        res_line_densities["orthw_lat_arr"] = NO2_res_line_densities["orthw_lat_arr"]
        res_line_densities["orthw_lon_arr"] = NO2_res_line_densities["orthw_lon_arr"]
        res_line_densities["alongw_lat_arr"] = NO2_res_line_densities["alongw_lat_arr"]
        res_line_densities["alongw_lon_arr"] = NO2_res_line_densities["alongw_lon_arr"]
        res_line_densities["ref_lon_arr"] = NO2_res_line_densities["ref_lon_arr"]
        res_line_densities["ref_lat_arr"] = NO2_res_line_densities["ref_lat_arr"]
        res_line_densities["satellite"] = NO2_res_line_densities["satellite"]
        res_line_densities["orbit"] = NO2_res_line_densities["orbit"]
        res_line_densities["lon_eq"] = NO2_res_line_densities["lon_eq"]

        if verbose:
            print(str(len(CO2_NO2_lds)) + " LD found !")
    else:
        res_line_densities = []

    return res_line_densities


def estimate_emissions_from_lds(
    lds, l2_data, src_lat_lon, lcs_params, tracer_gas="CO2"
):
    """\
    Once the line densities are computed, we estimate the emissions by the
    cross-sectional algorithm for each line density. The estimates are added as
    fields of the lds dictionnary
    """
    if not lds:
        return lds

    min_estim_emis = lcs_params["min_estim_emis"]
    max_estim_emis = lcs_params["max_estim_emis"]
    max_rel_std_emis = lcs_params["max_rel_std_emis"]
    f_NOx_NO2 = lcs_params["f_NOx_NO2"]
    NOx_NO2_tau_depletion = lcs_params["NOx_NO2_tau_depletion"]
    line_densities = lds["line_densities"]
    src_vec_wind = lds["src_vec_wind"]

    # To prepare for the mass-balance approach the following code computes the
    # CO2/NO2 background field, the plume signals and converts to mass columns
    # in kg/m² using the ucat Python package.
    rg = 9.80665  # m s-2 Gravity constant

    # Arrays where are stored some variables of the line densities
    emis_arr = []
    std_emis_arr = []
    popt_arr = []
    wind_arr = []
    R2_arr = []
    dist_from_src_arr = []

    # if emissions are gt max_estim_emis, we remove the associated line density
    # The estimated emissions are set to MISSVAL
    tmp_line_densities = []

    for line_density in line_densities:

        tmp_lon = line_density["lon_pt_fit"]
        tmp_lat = line_density["lat_pt_fit"]
        tmp_popt = line_density["popt"]
        tmp_vec_track = line_density["vec_track"]
        tmp_psurf = line_density["p_surf"]
        tmp_std_emis = line_density["std_emis"]
        vec_wind = line_density["vec_wind"]

        # Unit vector orthogonal to the OCO-2 track
        vec_trackorth = np.array([tmp_vec_track[1], -1 * tmp_vec_track[0]])

        # Project wind vector on it
        wind_proj = abs(np.dot(vec_wind, vec_trackorth))
        dist_from_source = (
            haversine_fct(src_lat_lon[1], src_lat_lon[0], tmp_lon, tmp_lat) * 1000
        )  # m

        # Location of the pixel
        if tracer_gas == "CO2":
            # ppm km => kg/m
            density = abs(tmp_popt[0] * 1e-3) * 0.04401 / 0.02896 * (tmp_psurf / rg)
            emis = density * wind_proj  # kgCO2/s
            emis = emis / 1e9 * 3600.0 * 24 * 365  # MtCO2/yr

            tmp_std_emis = tmp_std_emis * 1e-3 * 0.04401 / 0.02896 * (tmp_psurf / rg)
            tmp_std_emis = tmp_std_emis * wind_proj
            tmp_std_emis = tmp_std_emis / 1e9 * 3600.0 * 24 * 365

        if tracer_gas == "NO2":
            MNO2 = 46.0055e-3  # kg/moles
            density = abs(tmp_popt[0]) * 1e7 * MNO2 / N_A  # molecules/cm2 km -> kg/m
            emis = density * wind_proj  # kgNO2/s
            emis = emis / 1e6 * 3600.0 * 24 * 365  # ktNO2/yr

            # To retrieve the NOx emissions, we have to rescale by an exponential function
            # characterizing the NO2 depletion due to chemical reactions from the source to
            # the point of estimation of the NO2 emissions. Then, we have to multiply by the factor
            # emission in order to get the NOx emissions from NO2 emissions.
            norm_wind = np.sqrt(src_vec_wind[0] ** 2 + src_vec_wind[1] ** 2)
            emis = emis * np.exp(dist_from_source / norm_wind / NOx_NO2_tau_depletion)
            emis = f_NOx_NO2 * emis

            tmp_std_emis = tmp_std_emis * 1e7 * MNO2 / N_A
            tmp_std_emis = tmp_std_emis * wind_proj
            tmp_std_emis = tmp_std_emis / 1e6 * 3600.0 * 24 * 365
            tmp_std_emis = tmp_std_emis * np.exp(
                dist_from_source / norm_wind / NOx_NO2_tau_depletion
            )
            tmp_std_emis = tmp_std_emis * f_NOx_NO2

        bool_cond = (
            (emis < max_estim_emis)
            & (emis > min_estim_emis)
            & (tmp_std_emis / emis < max_rel_std_emis)
        )

        if bool_cond:
            line_density["estimated_emis"] = emis
            line_density["std_emis"] = tmp_std_emis
            line_density["vec_wind"] = vec_wind
            line_density["dist_from_source"] = dist_from_source

            tmp_line_densities.append(line_density)

            R2_arr.append(line_density["R2"])
            emis_arr.append(line_density["estimated_emis"])
            std_emis_arr.append(line_density["std_emis"])
            popt_arr.append(tmp_popt)
            wind_arr.append(line_density["vec_wind"])
            dist_from_src_arr.append(line_density["dist_from_source"])

        else:
            if lcs_params["verbose"]:
                print("EMISSIONS TOO HIGH/LOW. RATIO STD_EMIS/EMIS too HIGH")
                print(emis, " ", tmp_std_emis / emis * 100, "%")

    lds["emis_arr"] = np.array(emis_arr, dtype=np.float32)
    lds["std_emis_arr"] = np.array(std_emis_arr, dtype=np.float32)
    lds["popt_arr"] = np.array(popt_arr, dtype=np.float32)
    lds["wind_arr"] = np.array(wind_arr, dtype=np.float32)
    lds["R2_arr"] = np.array(R2_arr, dtype=np.float32)
    lds["line_densities"] = tmp_line_densities
    lds["dist_from_src_arr"] = np.array(dist_from_src_arr, dtype=np.float32)
    lds["satellite"] = getattr(l2_data, "satellite", None)
    lds["orbit"] = getattr(l2_data, "orbit", None)
    lds["lon_eq"] = getattr(l2_data, "lon_eq", None)

    return lds


def create_results_xr(res_dict, l2_data, all_diags):
    """
    From the results dict generated by the method, creates a xarray dataset with
    the results.

    all_diags: if True gather information of the line densities

    # OUTPUTS:

    res_xr: xarray containing the emission estimates, their precision, the
    distance to the source of the points where emissions are estimated:
        res_xr[tracer_gas+'_emissions'] = xr.DataArray(data=emis_arr,attrs=attrs,dims=dims,coords=coords)
        res_xr[tracer_gas+'_emissions_precision'] = xr.DataArray(data=std_emis_arr,attrs=attrs,dims=dims,coords=coords)
        res_xr[tracer_gas+'_dist_from_src']
    """
    source_names = list(res_dict.keys())
    n_sources = len(source_names)

    # Parameters defining the dimensions of the matrices
    n_fit_pxl_max = (
        100  # Hard-coded must be changed if number of fitting points exceeds this limit
    )
    n_line_pts_max = 200  # Hard-coded should be changed if resolution of the lines describing the fitting window changes
    n_el_window_max = (
        300  # Hard-coded should be changed if resolution of the data changes
    )
    n_popt_max = 5  # Estimated parameters of the Gaussian fitting of the line densities. If CO2, n_popt=5.if NO2, popt=3

    # Determining the tracer gases
    tracer_gases = []

    for source_name in source_names:
        tracer_gases.extend(list(res_dict[source_name].keys()))

    tracer_gases = np.unique(tracer_gases)

    # shape of remote sensing image
    n_obs_sat, n_rows_sat = l2_data[tracer_gases[0]].shape

    # Creating a xarray dataset with the results
    attrs = {"method": "LCS"}
    res_xr = xr.Dataset(attrs=attrs)

    coords = {}
    coords["source"] = source_names

    for tracer_gas in tracer_gases:

        emis_arr = np.ones((n_sources, n_fit_pxl_max)) * np.nan
        std_emis_arr = np.ones((n_sources, n_fit_pxl_max)) * np.nan
        dist_from_src_arr = np.ones((n_sources, n_fit_pxl_max)) * np.nan

        if all_diags:
            along_wind_line_pts = np.ones((n_sources, n_line_pts_max, 2)) * np.nan
            across_wind_line_pts = np.ones((2, n_sources, n_line_pts_max, 2)) * np.nan
            window_fit_pts_index = np.zeros(
                (n_sources, n_obs_sat, n_rows_sat), dtype=bool
            )
            slice_fit_pts_index = np.zeros(
                (n_sources, n_fit_pxl_max, n_obs_sat, n_rows_sat), dtype=bool
            )
            lat_lon_fit_pts = np.ones((n_sources, n_fit_pxl_max, 2)) * np.nan
            vec_wind_fit_pts = np.ones((n_sources, n_fit_pxl_max, 2)) * np.nan
            ld_centered_distances = (
                np.ones((n_sources, n_fit_pxl_max, n_el_window_max)) * np.nan
            )
            ld_popts = np.ones((n_sources, n_fit_pxl_max, n_popt_max)) * np.nan

        for i_source, source_name in enumerate(source_names):

            if len(res_dict[source_name]) == 0:
                continue

            if not tracer_gas in res_dict[source_name]:
                continue

            if len(res_dict[source_name][tracer_gas]) > 0:
                tmp_arr = res_dict[source_name][tracer_gas]["emis_arr"]
                emis_arr[i_source, : len(tmp_arr)] = tmp_arr
                tmp_arr = res_dict[source_name][tracer_gas]["std_emis_arr"]
                std_emis_arr[i_source, : len(tmp_arr)] = tmp_arr
                tmp_arr = res_dict[source_name][tracer_gas]["dist_from_src_arr"]
                dist_from_src_arr[i_source, : len(tmp_arr)] = tmp_arr / 1000.0  # m->km

                if all_diags:
                    tmp_arr = res_dict[source_name][tracer_gas]["alongw_lat_arr"]
                    along_wind_line_pts[i_source, : len(tmp_arr), 0] = tmp_arr
                    tmp_arr = res_dict[source_name][tracer_gas]["alongw_lon_arr"]
                    along_wind_line_pts[i_source, : len(tmp_arr), 1] = tmp_arr
                    tmp_arr = res_dict[source_name][tracer_gas]["orthw_lat_arr"][0]
                    across_wind_line_pts[0, i_source, : len(tmp_arr), 0] = tmp_arr
                    tmp_arr = res_dict[source_name][tracer_gas]["orthw_lon_arr"][0]
                    across_wind_line_pts[0, i_source, : len(tmp_arr), 1] = tmp_arr
                    tmp_arr = res_dict[source_name][tracer_gas]["orthw_lat_arr"][1]
                    across_wind_line_pts[1, i_source, : len(tmp_arr), 0] = tmp_arr
                    tmp_arr = res_dict[source_name][tracer_gas]["orthw_lon_arr"][1]
                    across_wind_line_pts[1, i_source, : len(tmp_arr), 1] = tmp_arr

                    window_fit_pts_index[i_source, :, :] = res_dict[source_name][
                        tracer_gas
                    ]["ij_window"]

                    for i_ld, ld in enumerate(
                        res_dict[source_name][tracer_gas]["line_densities"]
                    ):
                        slice_fit_pts_index[i_source, i_ld, :, :] = ld["ij_slice"]
                        lat_lon_fit_pts[i_source, i_ld, 0] = ld["lat_pt_fit"]
                        lat_lon_fit_pts[i_source, i_ld, 1] = ld["lon_pt_fit"]
                        vec_wind_fit_pts[i_source, i_ld, :] = ld["vec_wind"]
                        ld_centered_distances[
                            i_source, i_ld, : len(ld["centered_distances"])
                        ] = ld["centered_distances"]
                        ld_popts[i_source, i_ld, : len(ld["popt"])] = ld["popt"]

        if tracer_gas.find("CO2") > -1:
            unit = "Mt/yr"  # <- Valid for CO2 and CO2_with_NO2

        if tracer_gas == "NO2":
            unit = "kt/yr"

        attrs = {"unit": unit}
        dims = ["source", "fit_pxls"]
        res_xr[tracer_gas + "_emissions"] = xr.DataArray(
            data=emis_arr, attrs=attrs, dims=dims, coords=coords
        )
        res_xr[tracer_gas + "_emissions_precision"] = xr.DataArray(
            data=std_emis_arr, attrs=attrs, dims=dims, coords=coords
        )

        attrs = {"unit": "km"}
        res_xr[tracer_gas + "_dist_from_src"] = xr.DataArray(
            data=dist_from_src_arr, attrs=attrs, dims=dims, coords=coords
        )

        if all_diags:
            dims = ["source", "line_pt", "lat_lon"]
            attrs = {
                "description": "Lats and lons of the points describing the along-wind line downwind from the source"
            }
            res_xr[tracer_gas + "_alongw_line_pts"] = xr.DataArray(
                data=along_wind_line_pts, attrs=attrs, dims=dims
            )

            dims = ["n_across_wind_lines", "source", "line_pt", "lat_lon"]
            attrs = {
                "description": "Lats and lons of the points describing the across-wind lines at the source and downwind from the source"
            }
            res_xr[tracer_gas + "_acrossw_line_pts"] = xr.DataArray(
                data=across_wind_line_pts, attrs=attrs, dims=dims
            )

            dims = ["source", "n_obs_sat", "n_rows_sat"]
            attrs = {
                "description": "indexes of the pxls of the main data window extracted from the l2 data"
            }
            res_xr[tracer_gas + "_window_fit_pts_index"] = xr.DataArray(
                data=window_fit_pts_index, attrs=attrs, dims=dims
            )

            dims = ["source", "fit_pxls", "n_obs_sat", "n_rows_sat"]
            attrs = {
                "description": "indexes of the pxls of the data slices extracted from the l2 data where fitting is performed"
            }
            res_xr[tracer_gas + "_slice_fit_pts_index"] = xr.DataArray(
                data=slice_fit_pts_index, attrs=attrs, dims=dims
            )

            dims = ["source", "fit_pxls", "lat_lon"]
            attrs = {
                "description": "Lats and lons of the enhancements pixels where fitting procedure is initialized"
            }
            res_xr[tracer_gas + "_lat_lon_fit_pts"] = xr.DataArray(
                data=lat_lon_fit_pts, attrs=attrs, dims=dims
            )

            dims = ["source", "fit_pxls", "lat_lon"]
            attrs = {
                "description": "Winds at the enhancements pixels where fitting procedure is initialized. Used for emission estimation"
            }
            attrs["unit"] = "m/s"
            res_xr[tracer_gas + "_vec_wind_fit_pts"] = xr.DataArray(
                data=vec_wind_fit_pts, attrs=attrs, dims=dims
            )

            dims = ["source", "fit_pxls", "n_el_window_max"]
            attrs = {
                "description": "centered distances wrt the fitting points used to fit the line densities"
            }
            attrs["unit"] = "km"
            res_xr[tracer_gas + "_centered_distances"] = xr.DataArray(
                data=ld_centered_distances, attrs=attrs, dims=dims
            )

            dims = ["source", "fit_pxls", "n_popt_max"]
            attrs = {"description": "Estimated parameters of the Gaussian fitting"}
            res_xr[tracer_gas + "_popts"] = xr.DataArray(
                data=ld_popts, attrs=attrs, dims=dims
            )

    res_xr["time"] = l2_data["time"]

    return res_xr


def estimate_emissions(
    data,
    winds,
    sources,
    gases,
    fit_backgrounds=True,
    priors=None,
    lcs_params={},
    all_diags=False,
):
    """\
    Estimate emissions using the light cross sectional flux (LCSF) method.

    Parameters
    ----------
    data : xr.Dataset
        Remote sensing data.

    winds : xr.Dataset
        2D wind field.

    sources : xr.Dataset
        Source dataset for which emissions will be estimated.

    gases : str or list of strings
        Gases for which emissions will be estimated.

    fig_backgrounds : boolean or list of booleans, optional
        If a linear background is fitted with the Gaussian curve for estimating
        line densities.

    priors : dict, optional
        A dictionary with prior informatio for each source with source strength
        and decay time. For example:

        >>> priors = {'Matimba': {
        >>>    'NO2': {
        >>>        'Q': 3.0,       # in kg/s
        >>>        'tau': 4*60**2  # in seconds
        >>>   }
        >>> }}

    lcsf_params : dict, optional
        A dictionary with additional parameters. See code for details.


    Returns
    -------
    xr.Dataset
        Results dataset with estimated emissions for each source and other
        parameters.
    """
    if isinstance(gases, str):
        gases = [gases]

    if isinstance(fit_backgrounds, bool):
        fit_backgrounds = [fit_backgrounds, fit_backgrounds]

    # SET DEFAULT VALUES
    # Minimum and maximum value of emissions that is allowed
    lcs_params.setdefault("use_prior", False)

    if lcs_params["use_prior"]:
        lcs_params["min_estim_emis"] = None
        lcs_params["max_estim_emis"] = None
    else:
        lcs_params.setdefault("min_estim_emis", 0.0)
        lcs_params.setdefault("max_estim_emis", np.inf)

    # Enhancements are selected if Enhancement > Enhancement_thresh * std(data)
    lcs_params.setdefault("Enhancement_thresh", 1.0)

    # Only estimates for which the associated sigma derived from the fit of the line densities
    # is below max_sigma_Gauss are kept. Only effective for point sources not for cities
    lcs_params.setdefault("max_sigma_Gauss", 5.0)

    # Only estimates whose relative precision is below max_rel_std_emis are kept
    # max_rel_std_emis=1. means that estimates whose relative precision or uncertainty
    # is greater than 100 % are discarded.
    lcs_params.setdefault("max_rel_std_emis", 1.0)

    # For the computation of NOx emissions from NO2 data, ratio NOx to NO2 emissions
    # The value for this ratio has been determined from results of inversions with microHH simulations
    lcs_params.setdefault("f_NOx_NO2", 3.5)

    # For the computation of NOx emissions from NO2 data, exponential decay factor for the chemical depletion of NO2 downwind
    # The value for this factor has been determined from results of inversions with microHH simulations
    lcs_params.setdefault("NOx_NO2_tau_depletion", 4 * 3600)  # <-4 hours in seconds

    #  Length of the data slices extracted from the data images
    lcs_params.setdefault("window_length", 100)  # km

    # Width of the data slice used for the estimation of the emissions
    lcs_params.setdefault("fit_pt_slice_width", 10)

    # Minimal number of data points to perform the Gaussian fit of the line densities
    lcs_params.setdefault("n_min_fit_pts", 50)

    # For debug purposes, printing of information if set to true
    lcs_params.setdefault("verbose", False)

    # START
    verbose = lcs_params["verbose"]

    # Result dict where all important variables are stored
    res_dict = {}

    # Performing the cross-sectional flux estimation for each source
    for name, source in sources.groupby("source", squeeze=False):

        res_dict[name] = {}

        if verbose:
            print("LCSF parameters")
            print(lcs_params)
            print()
            print("**************")
            print()
            print(f"Estimating line densities and emissions for source {name}")
            print()

        # Lat and Lon of the selected source
        lon_source, lat_source, _ = ddeq.sources.get_location(source)
        lon_source = float(lon_source[0])
        lat_source = float(lat_source[0])

        # For the conversion km to lat/lon
        dlon = haversine_fct(
            lon_source, lat_source, lon_source + 1, lat_source
        )  # deg lon => km
        dlat = haversine_fct(0.0, 0.0, 0.0, 1.0)  # deg lat => km

        wind_src = ddeq.wind.get_wind_at_location(winds, lon_source, lat_source)
        norm_wind = np.sqrt(wind_src[0] ** 2 + wind_src[1] ** 2)

        # Checking if data available around the source
        max_dist = norm_wind * 3.6
        max_dlat = max_dist / dlat
        max_dlon = max_dist / dlon

        bool_cond = (
            (data["lat"].data < (lat_source + max_dlat))
            & (data["lat"].data > (lat_source - max_dlat))
            & (data["lon"].data < (lon_source + max_dlon))
            & (data["lon"].data > (lon_source - max_dlon))
        )

        # If no data available around the source, we don't estimate emissions
        if not bool_cond.any():
            continue

        # PROCESS FIRST GAS

        # Set bounds for allowed estimates based on provided prior
        prior = float(priors[name][gases[0]]["Q"])

        if lcs_params['use_prior']:
            if gases[0] in ['NOx', 'NO2']:
                prior = ucat.convert_mass_per_time_unit(prior, "kg/s", "kt/a")
            else:
                prior = ucat.convert_mass_per_time_unit(prior, "kg/s", "Mt/a")

            # assuming 30% uncertainty and using 3-sigma bounds for given prior
            lcs_params["min_estim_emis"] = 0.1 * prior
            lcs_params["max_estim_emis"] = 1.9 * prior

            # update tau for source from prior
            lcs_params["NOx_NO2_tau_depletion"] = priors[name][gases[0]]["tau"]

        # Extracting data slices and estimating line densities
        lds = estimate_line_densities(
            source,
            data,
            winds,
            lcs_params,
            tracer_gas=gases[0],
            fit_background=fit_backgrounds[0],
        )

        # Estimating emissions if line densities have been extracted
        lds = estimate_emissions_from_lds(
            lds, data, [lat_source, lon_source], lcs_params, tracer_gas=gases[0]
        )
        # Add lds to result dict
        res_dict[name][gases[0]] = lds

        if verbose:
            if len(lds) > 0:
                print(
                    f"{gases[0]} median emission estimate ", np.median(lds["emis_arr"])
                )

        if len(gases) == 1:
            continue

        # PROCESS SECOND GAS (if given)

        # Set bounds for allowed estimates based on provided prior
        prior = float(priors[name][gases[1]]["Q"])

        if lcs_params['use_prior']:
            if gases[1] in ['NOx', 'NO2']:
                prior = ucat.convert_mass_per_time_unit(prior, "kg/s", "kt/a")
            else:
                prior = ucat.convert_mass_per_time_unit(prior, "kg/s", "Mt/a")

            # assuming 30% uncertainty and using 3-sigma bounds for given prior
            lcs_params["min_estim_emis"] = 0.1 * prior
            lcs_params["max_estim_emis"] = 1.9 * prior

            # update tau for source from prior
            lcs_params["NOx_NO2_tau_depletion"] = priors[name][gases[1]]["tau"]

        # use results from first gas if available
        if len(lds) != 0:
            if verbose:
                print("Use first Gaussian curves to constrain second fit.")
            lds_second = estimate_lds_with_constraint(
                gases[1],
                lds,
                data,
                lcs_params,
                fit_background=fit_backgrounds[1],
            )
        else:
            # estimate only second gas if first gas fails
            lds_second = estimate_line_densities(
                source,
                data,
                winds,
                lcs_params,
                tracer_gas=gases[1],
                fit_background=fit_backgrounds[1],
            )

        # Estimating emissions of second gas
        lds_second = estimate_emissions_from_lds(
            lds_second, data, [lat_source, lon_source], lcs_params, tracer_gas=gases[1]
        )
        # Add lds to result dict
        res_dict[name][gases[1]] = lds_second

    # Results are gathered within a xarray
    res_xr = create_results_xr(res_dict, data, all_diags)

    return res_xr


def make_results_table_for_smartcarb(results, sources, gases, data, do_print=False):
    """\
    Print results for each source.
    BEWARE: Works only for SMARTCARB dataset for which true emissions are known
    """
    if isinstance(gases, str):
        gases = [gases]

    source_names = sources.source.data
    n_sources = len(source_names)

    col_names = []
    for gas in sorted(gases):
        units = {"CO2": "Mt/yr", "NO2": "kt/yr"}[gas]
        col_names.append(f"{gas} ({units})")
        col_names.append(f"{gas} true ({units})")

    # We retrieve true emissions
    emi_time = pd.Timestamp(data.time.values)

    n_col = len(col_names)
    data_arr = np.ones((n_sources, n_col)) * np.nan

    for i_source, source_name in enumerate(source_names):

        tmp_xr = results.sel(source=source_name)

        for j, gas in enumerate(gases):
            estimate = np.nanmedian(tmp_xr[f"{gas}_emissions"].data)
            data_arr[i_source, 2 * j] = np.round(estimate, 1)

            true_value = ddeq.smartcarb.read_true_emissions(
                gas, source_name, time=emi_time
            )
            true_value = ucat.convert_mass_per_time_unit(
                true_value,
                'kg/s',
                'Mt/a' if gas == 'CO2' else 'kt/a',
            )

            data_arr[i_source, 2 * j + 1] = np.round(true_value, 1)

    df = pd.DataFrame(data_arr, index=source_names, columns=col_names)
    df = df.fillna("")

    if do_print:
        print(df)

    return df
