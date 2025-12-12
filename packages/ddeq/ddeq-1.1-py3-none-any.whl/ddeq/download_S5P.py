import calendar
import datetime
import glob
import math
import os
import sys
import time
import warnings

from tqdm import tqdm
import cdsapi
import requests
import zipfile

import ddeq

# Module to set filesystem paths appropriate for user's operating system
from pathlib import Path

# Modules to create interactive menus in Jupyter Notebook
from IPython.display import display
import ipywidgets as widgets

# Other modules
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import matplotlib.patheffects as PathEffects
import numpy as np
import pandas as pd
import xarray as xr

import scipy.constants

R = scipy.constants.R
g = scipy.constants.g
k = scipy.constants.k
N_A = scipy.constants.N_A

# TODO
# - improve Downloader (handle exceptions and error codes)
# - check hash
# - allow user to choose which file to download (e.g for AUX there are 2 files for each date because the TM5 model was re-run)


# define dictionary of important variables for each product
product_variables = {
    "L2__CH4___": {
        "keep_variables": [
            "methane_mixing_ratio",
            "methane_mixing_ratio_precision",
            "methane_mixing_ratio_bias_corrected",
        ]
    },
    "L2__CLOUD_": {
        "keep_variables": [
            "cloud_fraction",
            "cloud_fraction_precision",
            "cloud_top_pressure",
            "cloud_top_pressure_precision",
            "cloud_base_pressure",
            "cloud_base_pressure_precision",
            "cloud_top_height",
            "cloud_top_height_precision",
            "cloud_base_height",
            "cloud_base_height_precision",
            "cloud_optical_thickness",
            "cloud_optical_thickness_precision",
        ]
    },
    "L2__CO____": {
        "keep_variables": [
            "carbonmonoxide_total_column",
            "carbonmonoxide_total_column_precision",
            "carbonmonoxide_total_column_corrected",
        ]
    },
    "L2__HCHO__": {
        "keep_variables": [
            "formaldehyde_tropospheric_vertical_column",
            "formaldehyde_tropospheric_vertical_column_precision",
        ]
    },
    "L2__NO2___": {
        "keep_variables": [
            "nitrogendioxide_tropospheric_column",
            "nitrogendioxide_tropospheric_column_precision",
            "averaging_kernel",
            "air_mass_factor_total",
            "air_mass_factor_troposphere",
            "tm5_constant_a",
            "tm5_constant_b",
            "cloud_fraction_crb",
            "solar_zenith_angle",
            "surface_altitude",
        ]
    },
    "L2__O3____": {
        "keep_variables": [
            "ozone_total_vertical_column",
            "ozone_total_vertical_column_precision",
        ]
    },
    "L2__SO2___": {
        "keep_variables": [
            "sulfurdioxide_total_vertical_column",
            "sulfurdioxide_total_vertical_column_precision",
            "averaging_kernel",
            "air_mass_factor",
            "tm5_constant_a",
            "tm5_constant_b",
            "cloud_fraction_crb",
            "surface_altitude",
        ]
    },
}

# define dictionary of important variables for all products
global_vars = [
    "time_utc",
    "delta_time",
    "qa_value",
    "surface_pressure",
    "longitude_bounds",
    "latitude_bounds",
]


### Acknowledgement
# The following UI is based on the Python Script Tutorial
# (https://www.star.nesdis.noaa.gov/atmospheric-composition-training/python_tropomi_level2_download.php)
# by the NOAA/NESDIS/STAR Aerosols and Atmospheric Composition Science Team.


def show_UI(sources=None):
    """
    Creates an UI to select the desired Sentinel 5-P product.
    Do NOT re-run block if you change menu selections (re-running block resets menus to defaults)!
    """

    # Formatting settings for drop-down menus
    style = {"description_width": "140px"}
    style_date = {"description_width": "80px"}
    layout = widgets.Layout(width="180px")
    layout_date = widgets.Layout(width="150px", height="30px")
    layout_caption = widgets.Layout(height="40px", justify_content="center")

    # Caption for map domain boundaries
    product_caption = widgets.Label(
        value="SELECT THE PRODUCT DETAILS. DO NOT RERUN THIS BLOCK IF YOU CHANGE MENU SELECTIONS",
        layout=layout_caption,
    )

    # Create drop-down menus using widgets
    product = widgets.Dropdown(
        options=[
            ("-", None),
            ("Aerosol Index", "L2__AER_AI"),
            ("Aerosol Layer Height", "L2__AER_LH"),
            ("Auxiliary", "AUX_CTMANA"),
            ("Carbon Monoxide", "L2__CO____"),
            ("Clouds", "L2__CLOUD_"),
            ("Formaldehyde", "L2__HCHO__"),
            ("Methane", "L2__CH4___"),
            ("Nitrogen Dioxide", "L2__NO2___"),
            ("Ozone", "L2__O3____"),
            ("Sulfur Dioxide", "L2__SO2___"),
        ],
        style=style,
        layout=layout,
    )
    latency = widgets.Dropdown(
        options=[
            ("-", None),
            ("Near real time", "NRTI"),
            ("Offline", "OFFL"),
            ("Reprocessing", "RPRO"),
        ],
        style=style,
        layout=layout,
        disabled=False,
    )
    level = widgets.Dropdown(
        options=[("L2", "L2"), ("L1B", "L1b"), ("-", None)], style=style, layout=layout
    )
    orbit = widgets.Text(value="-", style=style, layout=layout)
    start_year = widgets.Dropdown(
        options=[str(y) for y in range(2018, datetime.datetime.now().year + 1)],
        description="Start Year:",
        style=style_date,
        layout=layout_date,
    )
    start_month = widgets.Dropdown(
        options=[(calendar.month_abbr[i], f"{i:02d}") for i in range(1, 13)],
        description="Start Month:",
        style=style_date,
        layout=layout_date,
    )
    start_day = widgets.Dropdown(
        options=[f"{num:02}" for num in range(1, 32)],
        description="Start Day:",
        style=style_date,
        layout=layout_date,
    )
    end_year = widgets.Dropdown(
        options=[str(y) for y in range(2018, datetime.datetime.now().year + 1)],
        description="End Year:",
        style=style_date,
        layout=layout_date,
    )
    end_month = widgets.Dropdown(
        options=[(calendar.month_abbr[i], f"{i:02d}") for i in range(1, 13)],
        description="End Month:",
        style=style_date,
        layout=layout_date,
    )
    end_day = widgets.Dropdown(
        options=[f"{num:02}" for num in range(1, 32)],
        description="End Day:",
        style=style_date,
        layout=layout_date,
    )

    # Format product details to display side-by-side
    col_1 = widgets.VBox(
        [widgets.Label("Product:"), product],
        layout=widgets.Layout(display="flex", align_items="center"),
    )
    col_2 = widgets.VBox(
        [widgets.Label("Data Latency:"), latency],
        layout=widgets.Layout(display="flex", align_items="center"),
    )
    col_3 = widgets.VBox(
        [widgets.Label("Processing level:"), level],
        layout=widgets.Layout(display="flex", align_items="center"),
    )
    col_4 = widgets.VBox(
        [widgets.Label("Orbit number:"), orbit],
        layout=widgets.Layout(display="flex", align_items="center"),
    )
    first_row = widgets.HBox(
        [col_1, col_2, col_3, col_4],
        layout=widgets.Layout(
            display="flex",
            justify_content="space-around",
            height="100px",
            align_items="flex-start",
        ),
    )

    # Format observation start/end dates menus to display side-by-side
    start_date = widgets.HBox(
        [start_year, start_month, start_day],
        layout=widgets.Layout(display="flex", justify_content="space-around"),
    )
    end_date = widgets.HBox(
        [end_year, end_month, end_day],
        layout=widgets.Layout(display="flex", justify_content="space-around"),
    )

    # update end year based on selection of start year
    def update_end_year_options(change):
        end_year.options = [
            str(y)
            for y in range(int(start_year.value), datetime.datetime.now().year + 1)
        ]

    # Listen for changes in the selected value
    start_year.observe(update_end_year_options, "value")

    # update end month based on selection of start month
    def update_end_month_options(change):
        end_month.options = [(calendar.month_abbr[i], f"{i:02d}") for i in range(1, 13)]
        if end_year.value == start_year.value:
            end_month.options = [
                (calendar.month_abbr[i], f"{i:02d}")
                for i in range(int(start_month.value), 13)
            ]

    # Listen for changes in the selected value
    start_year.observe(update_end_month_options, "value")
    end_year.observe(update_end_month_options, "value")
    start_month.observe(update_end_month_options, "value")

    # update end day based on selection of start day
    def update_day_options(change):
        n_days_start = calendar.monthrange(
            int(start_year.value), int(start_month.value)
        )[1]
        n_days_end = calendar.monthrange(int(end_year.value), int(end_month.value))[1]
        start_day.options = [f"{num:02}" for num in range(1, n_days_start + 1)]
        end_day.options = [f"{num:02}" for num in range(1, n_days_end + 1)]
        if end_year.value == start_year.value and end_month.value == start_month.value:
            end_day.options = [
                f"{num:02}" for num in range(int(start_day.value), n_days_end + 1)
            ]

    # Listen for changes in the selected value
    start_year.observe(update_day_options, "value")
    end_year.observe(update_day_options, "value")
    start_month.observe(update_day_options, "value")
    end_month.observe(update_day_options, "value")
    start_day.observe(update_day_options, "value")

    # if auxiliary product is selected, the other boxes should be disabled
    def deactivate_options(change):
        latency.value = None if product.value == "AUX_CTMANA" else latency.value
        level.value = None if product.value == "AUX_CTMANA" else "L2"
        orbit.value = "-" if product.value == "AUX_CTMANA" else orbit.value
        latency.disabled = True if product.value == "AUX_CTMANA" else False
        level.disabled = True if product.value == "AUX_CTMANA" else False
        orbit.disabled = True if product.value == "AUX_CTMANA" else False
        select_aoi.disabled = True if product.value == "AUX_CTMANA" else False

    product.observe(deactivate_options, "value")

    # Choose between coordinates, source and area
    select_aoi = widgets.ToggleButtons(
        options=["Coordinates", "Point source", "Polygon"],
        tooltips=[
            "Enter lon/lat of a point",
            "Select a source from a given list",
            "Enter lon/lat extents of a polygon",
        ],
        value=None,
        disabled=False,
        layout=widgets.Layout(
            display="flex",
            justify_content="center",
            height="80px",
            align_items="center",
        ),
    )

    # Caption for coordinates
    coordinate_caption = widgets.Label(
        value="ENTER LONGITUDE/LATITUDE FOR A POINT OF INTEREST", layout=layout_caption
    )

    # Create boxes to enter the coordintates of a point
    lon_float = widgets.BoundedFloatText(
        description="Longitude:",
        value=0,
        min=-180,
        max=180,
        disabled=False,
        layout=widgets.Layout(width="250px", height="30px"),
    )
    lat_float = widgets.BoundedFloatText(
        description="Latitude:",
        value=0,
        min=-90,
        max=90,
        disabled=False,
        layout=widgets.Layout(width="250px", height="30px"),
    )
    coordinate_box = widgets.HBox([lon_float, lat_float], layout=layout_caption)

    # Caption for source selection
    point_caption = widgets.Label(value="SELECT A SOURCE", layout=layout_caption)

    # Create boxes to select a source
    source_str = widgets.Dropdown(
        options=["not available"] if sources is None else sources.source.values,
        description="Source: ",
        disabled=True if sources is None else False,
        layout=widgets.Layout(width="250px", height="30px", justify_content="center"),
    )
    point_box = widgets.HBox([source_str], layout=layout_caption)

    # Caption for map domain boundaries
    domain_caption = widgets.Label(
        value="ENTER LATITUDE/LONGITUDE BOUNDARIES FOR SEARCH AREA",
        layout=layout_caption,
    )

    # Create boxes for longitude
    west_lon_float = widgets.BoundedFloatText(
        value=0,
        min=-180,
        max=180,
        disabled=False,
        layout=widgets.Layout(width="100px", height="30px", justify_content="center"),
    )
    east_lon_float = widgets.BoundedFloatText(
        value=0,
        min=-180,
        max=180,
        disabled=False,
        layout=widgets.Layout(width="100px", height="30px", justify_content="center"),
    )
    lon_box = widgets.HBox(
        [
            widgets.Label("Western-most Longitude"),
            west_lon_float,
            east_lon_float,
            widgets.Label("Eastern-most Longitude"),
        ],
        layout=widgets.Layout(
            display="flex", align_items="center", justify_content="center"
        ),
    )

    # Create boxes for latitude
    north_lat_float = widgets.BoundedFloatText(
        value=0,
        min=-90,
        max=90,
        disabled=False,
        layout=widgets.Layout(width="100px", height="30px"),
    )
    south_lat_float = widgets.BoundedFloatText(
        value=0,
        min=-90,
        max=90,
        disabled=False,
        layout=widgets.Layout(width="100px", height="30px"),
    )
    north_lat_box = widgets.VBox(
        [widgets.Label("Northern-most Latitude"), north_lat_float],
        layout=widgets.Layout(display="flex", align_items="center"),
    )
    south_lat_box = widgets.VBox(
        [south_lat_float, widgets.Label("Southern-most Latitude")],
        layout=widgets.Layout(display="flex", align_items="center"),
    )

    # Display drop-down menus
    output = widgets.Output()
    display(product_caption, first_row)
    display(start_date, end_date)
    display(select_aoi, output)

    # display point selection based on choice
    def get_toggle_traits(change):
        output.clear_output()
        with output:
            if product.value != "AUX_CTMANA":
                if select_aoi.value == "Coordinates":
                    display(coordinate_caption, coordinate_box)

                elif select_aoi.value == "Point source":
                    display(point_caption, point_box)

                elif select_aoi.value == "Polygon":
                    display(domain_caption, north_lat_box, lon_box, south_lat_box)
            else:
                display(widgets.VBox([]))

    select_aoi.observe(get_toggle_traits, "value")
    product.observe(get_toggle_traits, "value")

    return (
        product,
        latency,
        level,
        orbit,
        start_year,
        start_month,
        start_day,
        end_year,
        end_month,
        end_day,
        select_aoi,
        lon_float,
        lat_float,
        source_str,
        west_lon_float,
        east_lon_float,
        south_lat_float,
        north_lat_float,
    )


def convert_date_sentinel_api_format(year, month, day):
    # Format the selected date to a format digestible by the API
    formatted_date = year + "-" + month + "-" + day
    return formatted_date


def list_files(
    west_lon,
    east_lon,
    south_lat,
    north_lat,
    start_date,
    end_date,
    product_abbreviation,
    latency,
    level,
    orbit,
    only_latest=False,
):
    """\
    Create list of TROPOMI data file names based on the UI input.
    Return the file list, the size of each file and the product details.
    """
    ids = []
    filenames = []

    # format some of the parameters
    orbit = None if orbit == "-" else orbit

    if product_abbreviation == "AUX_CTMANA" or (
        west_lon is None
        and east_lon is None
        and south_lat is None
        and north_lat is None
    ):
        footprint = None
    else:
        footprint = area_of_interest(west_lon, east_lon, south_lat, north_lat)

    # Query per day as the number of returns per query is limited to 20
    # (LEO: 14-15 orbits per day)
    for date in pd.date_range(start_date, end_date):
        start_date = date.strftime("%Y-%m-%dT00:00:00Z")
        end_date = date.strftime("%Y-%m-%dT23:59:59Z")

        # define components of the query
        url_init = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq 'SENTINEL-5P'"
        prod_type = (
            f"Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/OData.CSC.StringAttribute/Value eq '{product_abbreviation}')"
            if product_abbreviation
            else product_abbreviation
        )
        proc_lvl = (
            f"Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'processingLevel' and att/OData.CSC.StringAttribute/Value eq '{level}')"
            if level
            else level
        )
        proc_md = (
            f"Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'processingMode' and att/OData.CSC.StringAttribute/Value eq '{latency}')"
            if latency
            else latency
        )
        orb_nr = (
            f"Attributes/OData.CSC.IntegerAttribute/any(att:att/Name eq 'orbitNumber' and att/OData.CSC.IntegerAttribute/Value eq '{orbit}')"
            if orbit
            else orbit
        )
        bbox = (
            f"OData.CSC.Intersects(area=geography'SRID=4326;{footprint}')"
            if footprint
            else footprint
        )
        st_date = f"ContentDate/Start ge {start_date}" if start_date else start_date
        end_date = f"ContentDate/Start le {end_date}" if end_date else end_date
        query = " and ".join(
            filter(
                None,
                [
                    url_init,
                    prod_type,
                    proc_lvl,
                    proc_md,
                    orb_nr,
                    bbox,
                    st_date,
                    end_date,
                ],
            )
        )

        try:
            # Access the API and create query
            products = requests.get(query).json()
        except:
            raise ConnectionError("Error connecting to the server")

        if 'value' in products:
            ids_day = [v['Id'] for v in products['value']]
            fns_day = [v['Name'] for v in products['value']]

            if only_latest and product_abbreviation == 'AUX_CTMANA':
                index = np.argsort(fns_day)[-1]
                ids_day = [ids_day[index]]
                fns_day = [fns_day[index]]

            ids.extend(ids_day)
            filenames.extend(fns_day)
        else:
            print(f'No results for {date.strftime("%Y-%m-%d")}.')

    return ids, filenames


class Download:
    def __init__(self, path, username, password):
        self.save_path = path
        self.username = username
        self.password = password
        self.keycloak_token = None

    def get_keycloak(self) -> str:
        data = {
            "client_id": "cdse-public",
            "username": self.username,
            "password": self.password,
            "grant_type": "password",
        }
        try:
            r = requests.post(
                "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
                data=data,
            )
            r.raise_for_status()
        except Exception as e:
            raise Exception(
                f"Keycloak token creation failed. Response from the server was: {r.json()}"
            )
        return r.json()["access_token"]

    def download_files(self, ids, filenames):

        # open session (using exisiting token if available)
        if self.keycloak_token is None:
            self.keycloak_token = self.get_keycloak()

        session = requests.Session()
        session.headers.update({"Authorization": f"Bearer {self.keycloak_token}"})

        # iterrat of filenames

        for file_id, file_name in zip(ids, filenames):

            if os.path.exists(os.path.join(self.save_path, file_name)):
                print(f"File {file_name} already exists. Skipping download.")
                continue

            try:
                print(f"Querying {file_name}")
                url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products({file_id})/$value"
                response = session.get(url, allow_redirects=False, stream=True)

                while response.status_code in (301, 302, 303, 307, 401):
                    url = response.headers["Location"]
                    response = session.get(url, allow_redirects=False, stream=True)

                    if response.status_code == 401:
                        self.keycloak_token = self.get_keycloak()
                        session.headers.update(
                            {"Authorization": f"Bearer {self.keycloak_token}"}
                        )

                if response.status_code not in range(200, 299):
                    raise Exception(
                        f"Unsuccessful server response. Status code: {response.status_code}"
                    )

                folder_name = (
                    response.headers.get("Content-Disposition")
                    .split("filename=")[-1]
                    .strip('"')
                )
                folderpath = os.path.join(self.save_path, folder_name)
                filepath = folderpath.replace("zip", "nc")

                with open(folderpath, "wb") as file:
                    file_size = int(response.headers.get("Content-Length", 0))
                    progress = tqdm(
                        total=file_size,
                        unit="iB",
                        unit_scale=True,
                        desc=f"Downloading {folder_name}",
                        miniters=1,
                    )
                    for data in response.iter_content(1024):
                        file.write(data)
                        progress.update(len(data))
                    progress.close()

                with zipfile.ZipFile(folderpath, "r") as zip_ref:
                    for member in zip_ref.namelist():
                        if member.endswith(".nc"):
                            zip_ref.extract(member, self.save_path)
                            extracted_file = os.path.join(self.save_path, member)
                            new_file = os.path.join(
                                self.save_path, os.path.basename(member)
                            )
                            os.rename(extracted_file, new_file)

                os.remove(folderpath)  # remove .zip folder
                os.rmdir(folderpath[:-4])  # remove extracted folder

            except Exception as e:
                print(f"Error downloading file with id {file_name}: {str(e)}")


def tropomi_download_files(ids, filenames, save_path, username, password):

    # make dir if necessary
    os.makedirs(save_path, exist_ok=True)

    # Init downloader providing save path and credentials.
    downloader = Download(save_path, username, password)

    # Extract data file ids from dataframe to list
    if ids:
        try:
            downloader.download_files(ids, filenames)
        except KeyboardInterrupt:
            print("\nDownload was interrupted by user.")


def get_tropomi_files(
    west_lon,
    east_lon,
    south_lat,
    north_lat,
    start_date,
    end_date,
    product_abbreviation,
    latency,
    level,
    orbit,
    save_path,
    username,
    password,
    ask=True,
):
    """
    Print the available TROPOMI data files that match user specifications in the UI.
    Ask the user if the files should be downloaded.
    """

    # Query S5P Data Hub and list file names matching user-entered info
    print(f"Query files from {start_date} to {end_date}...", end="")
    sys.stdout.flush()
    ids, filenames = list_files(
        west_lon,
        east_lon,
        south_lat,
        north_lat,
        start_date,
        end_date,
        product_abbreviation,
        latency,
        level,
        orbit,
    )
    print(f" found {len(ids)} files.")

    # Print list of available file names/sizes
    if len(filenames) > 0:
        print(f"\nList of {len(filenames)} available data files:")
        for file in filenames:
            print(file)

        # Print directory where files will be saved
        print("\nData files will be saved to:", save_path)

        # Ask user if they want to download the available data files
        # If yes, download files to specified directory
        if ask:
            download_question = f"\nWould you like to download the "
            f'{str(len(filenames))} files?\nType "y" or "n" and hit "Enter"\n'
            ask_download = input(download_question)
            while ask_download.lower() not in ["yes", "y", "no", "n"]:
                ask_download = input("Enter 'y' (save) or 'n' (don't save).")
            if ask_download.lower() in ["yes", "y"]:
                tropomi_download_files(ids, filenames, save_path, username, password)
            else:
                print("\nFiles are not being downloaded.")
        else:
            tropomi_download_files(ids, filenames, save_path, username, password)
    else:
        print("\nNo files retrieved.  Check settings and try again.")


def get_coordinates(
    select_aoi,
    lon_float,
    lat_float,
    source_str,
    west_lon_float,
    east_lon_float,
    south_lat_float,
    north_lat_float,
    sources=None,
):
    """
    Get the coordinates for the API query based on the selected localisation type.
    """
    if select_aoi.value is None:
        raise TypeError("Select a method to localise the satellite image")

    elif select_aoi.value == "Coordinates":
        lon = lon_float.value
        lat = lat_float.value
        west_lon, east_lon, south_lat, north_lat = get_bounding_box(
            lon, lat, distance=1e3
        )

    elif select_aoi.value == "Point source":
        if source_str.value != "not available":
            lon = sources.sel(source=source_str.value).longitude.values
            lat = sources.sel(source=source_str.value).latitude.values
            west_lon, east_lon, south_lat, north_lat = get_bounding_box(
                lon, lat, distance=1e3
            )
        else:
            raise TypeError("Select another method to localise the satellite image")

    elif select_aoi.value == "Polygon":
        west_lon = west_lon_float.value
        east_lon = east_lon_float.value
        south_lat = south_lat_float.value
        north_lat = north_lat_float.value

        if (
            west_lon == east_lon == south_lat == north_lat
            or west_lon == east_lon
            or south_lat == north_lat
        ):
            raise TypeError("Select a valid polygon")

    return (str(west_lon), str(east_lon), str(south_lat), str(north_lat))


# Main function
def main_UI(
    username,
    password,
    data_path,
    product,
    latency,
    level,
    orbit,
    start_year,
    start_month,
    start_day,
    end_year,
    end_month,
    end_day,
    select_aoi,
    lon_float,
    lat_float,
    source_str,
    west_lon_float,
    east_lon_float,
    south_lat_float,
    north_lat_float,
    sources=None,
):
    """
    Search for TROPOMI data as specified in the UI.
    Ask the user if the files should be downloaded to the indicated directory.
    If the file is already present, the download is skipped.
    """

    # Set directory to save downloaded files (as pathlib.Path object)
    # Use current working directory for simplicity
    save_path = data_path

    # Get TROPOMI product abbreviation used in file name
    product_abbreviation = product.value

    # Change user-entered observation year/month/day for observation period to format used by Sentinel API
    start_date = convert_date_sentinel_api_format(
        start_year.value, start_month.value, start_day.value
    )
    end_date = convert_date_sentinel_api_format(
        end_year.value, end_month.value, end_day.value
    )

    # Convert latitude/longitude values entered as floats to string format used by Sentinel API
    if product.value != "AUX_CTMANA":
        west_lon, east_lon, south_lat, north_lat = get_coordinates(
            select_aoi,
            lon_float,
            lat_float,
            source_str,
            west_lon_float,
            east_lon_float,
            south_lat_float,
            north_lat_float,
            sources,
        )
    else:
        west_lon, east_lon, south_lat, north_lat = None, None, None, None

    # Execute script
    get_tropomi_files(
        west_lon,
        east_lon,
        south_lat,
        north_lat,
        start_date,
        end_date,
        product_abbreviation,
        latency.value,
        level.value,
        orbit.value,
        save_path,
        username=username,
        password=password,
    )


def get_bounding_box(lon0, lat0, distance):
    """
    Calculates the minimum and maximum longitudes and latitudes of a box around
    a given source.

    Paramaters
    ----------
    lon0 : float
        Longitude of source.
    lat0 : float
        Latitude of source.
    distance : float
        Distance between source and box to be calculated in m.

    Returns
    -------
    (min_lat, min_lon, max_lat, max_lon) : float
        Tuple of minimum and maximum longitudes and latitudes.
    """

    R = 6378137  # Radius of earth in meters
    lat = lat0 * math.pi / 180  # convert latitude to radians
    lon = lon0 * math.pi / 180  # convert longitude to radians
    d = distance / R  # convert distance to radians

    # Calculate the corners of the bounding box
    min_lat = lat - d
    max_lat = lat + d
    min_lon = lon - d / math.cos(lat)
    max_lon = lon + d / math.cos(lat)

    # Convert back to degrees
    min_lat = min_lat * 180 / math.pi
    max_lat = max_lat * 180 / math.pi
    min_lon = min_lon * 180 / math.pi
    max_lon = max_lon * 180 / math.pi

    return (min_lon, max_lon, min_lat, max_lat)


def area_of_interest(min_lon, max_lon, min_lat, max_lat):
    """
    Format a string with the given minimum and maximum longitudes and latitudes
    to create the bounding polygon around a source.
    """
    polygon = (
        "POLYGON(("
        f"{min_lon} {min_lat},"  # Bottom-Left
        f"{min_lon} {max_lat},"  # Top-Left
        f"{max_lon} {max_lat},"  # Top-Right
        f"{max_lon} {min_lat},"  # Bottom-Right
        f"{min_lon} {min_lat}))"  # Bottom-Left
    )
    return polygon


def open_netCDF(filename, path="./"):
    """
    Read in the data files from the given path.
    Combine data from the groups PRODUCT and SUPPORT_DATA
    Return netCDF file.
    """
    if path is None:
        full_filename = filename
    else:
        full_filename = os.path.join(path, filename)
    groups = [
        "PRODUCT",
        "PRODUCT/SUPPORT_DATA/GEOLOCATIONS",
        "PRODUCT/SUPPORT_DATA/INPUT_DATA",
        "PRODUCT/SUPPORT_DATA/DETAILED_RESULTS",  # only SO2?
    ]
    try:
        data_S5p_all = xr.merge(
            [xr.open_dataset(full_filename, group=group) for group in groups]
        )

        # rename some variables
        data_S5p_all = data_S5p_all.rename({"longitude": "lon", "latitude": "lat"})

        # add attributes
        data_S5p_all.attrs = {
            "original file name": os.path.basename(filename),
            "data source": "https://s5phub.copernicus.eu/dhus/",
        }
        return data_S5p_all

    except FileNotFoundError:
        raise FileNotFoundError(
            "There is no file called '{}' in '{}'".format(filename, path)
        )


def reduce_dims_and_vars(data_S5p):
    """
    Remove the dimensions and variables from a netCDF file, which are not
    needed. Documentation of all variables: https://sentinel.esa.int/documents
    /247904/2474726/Sentinel-5P-Level-2-Product-User-Manual-Nitrogen-Dioxide.pdf

    Paramaters
    ----------
    data_S5p : netCDF
        File to be cleaned.

    Returns
    -------
    data_S5p : netCDF
        Cleaned file.
    """
    # get product name from dictionary.
    product = data_S5p.attrs["original file name"][9:19]

    # For some other products, lat and lon are variables instead of coordinates
    # => add to coordinates
    if product in ["L2__O3____", "L2__SO2___", "L2__HCHO__", "L2__CLOUD_"]:
        data_S5p = data_S5p.set_coords(("lat", "lon"))

    # get important dimensions and variables for each product
    keep_dimensions = [
        "scanline",
        "ground_pixel",
        "time",
        "lat",
        "lon",
        "corner",
        "orbit",
        "layer",
        "vertices",
    ]
    keep_variables = product_variables[product]["keep_variables"] + global_vars

    # drop unneccessary dimensions and variables
    for dim in data_S5p.indexes:
        if dim not in keep_dimensions:
            data_S5p = data_S5p.drop_dims(dim)

    for var in data_S5p.data_vars:
        if var not in keep_variables:
            data_S5p = data_S5p.drop_vars(var)

    if "time" in data_S5p.dims:
        data_S5p = data_S5p.squeeze("time")

    # format dataset
    if isinstance(data_S5p.time_utc.dtype, str):
        data_S5p["time_utc"] = data_S5p.time_utc.str.strip("Z").astype("datetime64[ns]")
    else:
        pass  # data_S5p['time_utc'] = data_S5p.time_utc.astype('datetime64[ns]')

    data_S5p = data_S5p.assign_coords(
        orbit=int(data_S5p.attrs["original file name"][52:57])
    )

    return data_S5p


def crop_data(data_S5p, source, distance, sources):
    """
    Crop the data to the latitudes and longitudes which were used to select and
    download the data. Add attributes for the source to which the data has been
    cropped and the distance around the source in the resulting netCDF file.

    Paramaters
    ----------
    data : netCDF
        File to be cropped.
    source : str
        Source to which the data should be cropped.
    distance : float
        Distance between source and box to be calculated in meters.
    sources : netCDF
        netCDF file of all available sources and their coordinates.

    Returns
    -------
    data_S5p_cropped : netCDF
        Cropped file.
    save : bool
        Indicate if the dataset is not empty and should be saved.
    """

    # longitude and latitude bounds only work if there are no nans.
    # That they are not dropped when cropping, we have to convert them to dimensions
    data_S5p = data_S5p.set_coords(("latitude_bounds", "longitude_bounds"))

    lon0, lat0, _ = ddeq.sources.get_location(sources)
    lon0, lat0 = lon0.values, lat0.values

    # get min and max lon and lat around the source
    min_lon, max_lon, min_lat, max_lat = get_bounding_box(lon0, lat0, distance)

    # crop data to area needed
    mask_lon = (data_S5p.lon >= min_lon) & (data_S5p.lon <= max_lon)
    mask_lat = (data_S5p.lat >= min_lat) & (data_S5p.lat <= max_lat)

    # check if there is data in the area of interest. Use variable which is in
    # all products
    if (
        np.count_nonzero(
            ~np.isnan(np.where(mask_lon & mask_lat, data_S5p.qa_value, np.nan))
        )
        > 0
    ):
        data_S5p_cropped = data_S5p.where(mask_lon & mask_lat, drop=True)
        save = True
    else:
        data_S5p_cropped = data_S5p.where(mask_lon & mask_lat)
        save = False

    # add attributes
    data_S5p_cropped.attrs = data_S5p.attrs
    data_S5p_cropped.attrs.update(
        {
            "description": "Sentinel-5P data - cropped to a source",
            "source": source,
            "distance around source [m]": distance,
        }
    )

    return data_S5p_cropped, save


def calc_pressure(data_S5p, pname):
    """
    Calculate the pressure of the TROPOMI layers with the following formula:
    p(t, k, j, i, l) = ap(k, l) + b(k, l)*ps(t, j, i)
    Neglects the humidity.

    Paramaters
    ----------
    data_S5p : netCDF
        TROPOMI data file with content of PRODUCT and SUPPORT_DATA groups
        Must contain the variables tm5_constant_a, tm5_constant_b and variable
        for surface pressure
    pname : str
        Name of pressure variable. psurf in ddeq, surface_pressure in S5P

    Returns
    -------
    data_S5p : netCDF
        File with added pressures
    """
    # vertices = 0 is the lower bound of the height layer, 1 the upper bound
    if all(var in data_S5p for var in ["tm5_constant_a", "tm5_constant_b", pname]):
        data_S5p["pressure"] = (
            data_S5p.tm5_constant_a + data_S5p.tm5_constant_b * data_S5p[pname]
        )
        data_S5p["pressure"].attrs["units"] = data_S5p["tm5_constant_a"].attrs["units"]
        data_S5p["pressure"].attrs[
            "formula"
        ] = "p(t, k, j, i, l) = ap(k, l) + b(k, l)*ps(t, j, i); k from surface to top of atmosphere; l=0 for base of layer, l=1 for top of layer."
    else:
        raise KeyError(
            "One of the variables tm5_constant_a, tm5_constant_b or variable for surface pressure is missing in the dataset."
        )

    return data_S5p


def add_NO2_profile(data_S5p, path="./", delete=False):
    """
    Download the AUX file for the given TROPOMI data product.
    Add the TM5-MP NO2 profile to the data product.
    Calcualte and add the geometric heigth of the layers for the
        data product with the hypsometric formula

    Paramaters
    ----------
    data_S5p : netCDF
        TROPOMI data file to which the NO2 profile has to be added to
    path : str
        Path where to check for / store the AUX file
    delete : bool
        Indicates if the AUX file should be deleted afterwards


    Returns
    -------
    data_S5p : netCDF
        File with added NO2 profile
    """
    # open auxiliary dataset
    aux_time = pd.to_datetime(data_S5p.time.values).round("s")
    aux_S5p_file = sorted(
        glob.glob(
            os.path.join(
                path,
                f'*S5P_OPER_AUX_CTMANA_*{aux_time.strftime("%Y%m%d")}*{(aux_time + pd.DateOffset(days=1)).strftime("%Y%m%d")}*.nc',
            )
        )
    )

    if len(aux_S5p_file) >= 1:
        aux_S5p = xr.open_dataset(aux_S5p_file[-1])
    else:
        raise FileNotFoundError(
            f"No auxilary file for {aux_time.strftime('%Y-%m-%d')} found."
        )

    # layer in S5p data starts with 0, lev in auxiliary data starts with 1
    aux_S5p["lev"] = aux_S5p.lev.values - 1

    # calculate pressure
    aux_S5p["pressure"] = aux_S5p.hyam + aux_S5p.hybm * aux_S5p.ps
    aux_S5p["pressure"].attrs["units"] = aux_S5p["hyam"].attrs["units"]
    aux_S5p["pressure"].attrs["description"] = "Pressure at layer midpoints"

    # calculate geometric height with hypsometric equation
    aux_S5p["height_profile"] = np.log(aux_S5p.ps / aux_S5p.pressure) * (
        R * aux_S5p.t / (0.02896 * g)
    )

    # interpolate auxiliary data to TROPOMI pixels
    aux_S5p = aux_S5p.sel(
        time=np.datetime64(str(data_S5p.time.values)[:-1]), method="nearest"
    )[["height_profile", "no2"]]
    aux_S5p_interp = aux_S5p.interp(lon=data_S5p.lon, lat=data_S5p.lat, method="linear")
    aux_S5p_interp = aux_S5p_interp.rename({"lev": "layer"})
    aux_S5p_interp = aux_S5p_interp.transpose(*data_S5p.averaging_kernel.dims)

    # add NO2 profile to NO2 product
    data_S5p["NO2_profile"] = (
        (data_S5p.averaging_kernel.dims),
        aux_S5p_interp.no2.values,
    )
    data_S5p["NO2_profile"].attrs = aux_S5p_interp.no2.attrs
    data_S5p["height_profile"] = (
        (data_S5p.averaging_kernel.dims),
        aux_S5p_interp.height_profile.values,
    )
    data_S5p["height_profile"].attrs["units"] = "m"
    data_S5p["height_profile"].attrs[
        "comment"
    ] = "Height above surface calculated from hypsometric equation using p, ps and t from auxiliary file."

    if delete:
        os.remove(aux_S5p_file[0])

    return data_S5p


def add_pbl_height(data_S5p, path="./"):
    # Download and add the pbl height to the TROPOMI data
    # Interpolate to the TROPOMI pixels

    time = pd.to_datetime(data_S5p.time.values)
    area = [90, -180, -90, 180]  # north, east, south, west
    era5_filename_pbl = ddeq.era5.download_single_layer(
        time, "boundary_layer_height", area, path, code="pbl", timesteps=24
    )
    era5_pbl = xr.open_dataset(era5_filename_pbl).sel(time=time, method="nearest")
    era5_pbl = era5_pbl.interp(latitude=data_S5p.lat, longitude=data_S5p.lon)
    data_S5p["pbl_height"] = ((data_S5p.lat.dims), era5_pbl.blh.values)
    data_S5p["pbl_height"].attrs = era5_pbl.blh.attrs

    return data_S5p


def update_NO2_profile(
    data_S5p, where, pbl_path="./", NO2_path="./", PBL_conc=1e-8, delete=False
):
    """
    Update TM5-MP NO2 profile from the AUX file below the PBL heigth
    The concentration is set to a constant value

    data_S5p : netCDF
        TROPOMI data file for which the NO2 profile should be updated
    where : str
        "all" or "plume": replace profile everywhere or only where a plume is detected.
    pbl_path : str
        Path where the ERA5 pbl file is stored. PBL height is given in m
    NO2_path : str
        Path where the AUX file is stored
    PBL_conc : float
        NO2 concentration in mol/mol to which the profile in the PBL should be set
        Determined from MicroHH model simulations
    delete : bool
        Indicates if the AUX file should be deleted afterwards

    Returns
    -------
    data_S5p : netCDF
        TROPOMI data file with updated NO2 profile
    """

    if "pbl_height" not in data_S5p.data_vars:
        data_S5p = add_pbl_height(data_S5p, path=pbl_path)

    if "NO2_profile" not in data_S5p.data_vars:
        data_S5p = add_NO2_profile(data_S5p, path=NO2_path, delete=delete)

    NO2_profile_attrs = data_S5p["NO2_profile"].attrs

    # update profile
    if where == "plume" and "detected_plume" in data_S5p.data_vars:
        data_S5p["NO2_profile"] = xr.where(
            (data_S5p["height_profile"] < data_S5p["pbl_height"])
            & (data_S5p["detected_plume"].any(dim="source") == True),
            PBL_conc,
            data_S5p["NO2_profile"],
            keep_attrs=True,
        )

    elif where == "all":
        data_S5p["NO2_profile"] = xr.where(
            data_S5p["height_profile"] < data_S5p["pbl_height"],
            PBL_conc,
            data_S5p["NO2_profile"],
            keep_attrs=True,
        )
    else:
        raise KeyError("No variable 'detected_plume' in dataset")

    data_S5p["NO2_profile"].attrs = NO2_profile_attrs
    data_S5p["pbl_height"].attrs["NO2 conc. in PBL"] = PBL_conc

    return data_S5p


def update_AMF(data_S5p):
    """
    Update

    Paramaters
    ----------
    data_S5p : netCDF
        TROPOMI data file for which the AMFs should be recalculated based on the new NO2 profile
        Requires variables air_mass_factor_troposphere, averaging_kernel and NO2_profile


    Returns
    -------
    data_S5p : netCDF
        File with updated AMFs
    """

    if all(
        var in data_S5p
        for var in ["air_mass_factor_troposphere", "averaging_kernel", "NO2_profile"]
    ):
        data_S5p["air_mass_factor_troposphere_new"] = (
            data_S5p.air_mass_factor_troposphere
            * (
                (
                    (data_S5p.averaging_kernel * data_S5p.NO2_profile).sum(dim="layer")
                    / data_S5p.NO2_profile.sum(dim="layer")
                )
            )
        )
        data_S5p["air_mass_factor_troposphere_new"].attrs["units"] = (
            data_S5p.air_mass_factor_troposphere.attrs["units"]
        )

    else:
        raise KeyError("No NO2 profile in dataset")

    return data_S5p


def recalculate_VCD(data_S5p, variable="NO2"):
    """
    Update VCDs based on the AMF

    Paramaters
    ----------
    data_S5p : netCDF
        TROPOMI data file for which the VCDs should be recalculated based on the new AMFs
        Requires variables air_mass_factor_troposphere and air_mass_factor_troposphere_new


    Returns
    -------
    data_S5p : netCDF
        File with updated VCDs
    """
    NO2_attrs = data_S5p[variable].attrs

    if all(
        var in data_S5p
        for var in [
            variable,
            "air_mass_factor_troposphere",
            "air_mass_factor_troposphere_new",
        ]
    ):
        data_S5p[variable] = (
            data_S5p[variable] * data_S5p.air_mass_factor_troposphere
        ) / data_S5p.air_mass_factor_troposphere_new
        data_S5p[variable].attrs = NO2_attrs
        data_S5p[variable].attrs[
            "Comment"
        ] = "VCDs reprocessed based on updated NO2 vertical profile"

    else:
        raise KeyError(
            "One of the variables air_mass_factor_troposphere, "
            "averaging_kernel or NO2_profile is missing "
            "in the dataset."
        )

    return data_S5p


def convert_to_ddeq_format(
    data_S5p, variable="nitrogendioxide_tropospheric_column", std=7.6e-07
):
    """
    Convert TROPOMI netCDF data into a format which can be digested by `ddeq`.
    Currently only works for NO2.
    std: 7.6e-07 kg/m2 is equivalent to 1e15 molec cm-2
    Returns the formatted netCDF file.
    """

    product = data_S5p.attrs["original file name"][11:19].replace("_", "")

    data = xr.Dataset(
        data_vars={
            f"{product}": (
                ["nrows", "nobs"],
                data_S5p[variable].values,
                {
                    "units": data_S5p[variable].attrs.get("units", ""),
                    "long_name": data_S5p[variable].attrs.get("long_name", ""),
                    "cloud_threshold": 0.30,
                    "noise_level": std,
                },
            ),
            f"{product}_std": (
                ["nrows", "nobs"],
                np.full(data_S5p[f"{variable}_precision"].shape, std),
                {
                    "units": data_S5p[f"{variable}_precision"].attrs.get("units", ""),
                    "long_name": data_S5p[f"{variable}_precision"].attrs.get(
                        "long_name", ""
                    ),
                    "cloud_threshold": 0.30,
                },
            ),
            "latc": (["nrows", "nobs", "corner"], data_S5p["latitude_bounds"].values),
            "lonc": (["nrows", "nobs", "corner"], data_S5p["longitude_bounds"].values),
            "averaging_kernel": (
                ["nrows", "nobs", "layer"],
                data_S5p["averaging_kernel"].values,
                {
                    "units": data_S5p["averaging_kernel"].attrs.get("units", ""),
                    "long_name": data_S5p["averaging_kernel"].attrs.get(
                        "long_name", ""
                    ),
                },
            ),
            "air_mass_factor_troposphere": (
                ["nrows", "nobs"],
                data_S5p["air_mass_factor_troposphere"].values,
                {
                    "units": data_S5p["air_mass_factor_troposphere"].attrs.get(
                        "units", ""
                    ),
                    "long_name": data_S5p["air_mass_factor_troposphere"].attrs.get(
                        "long_name", ""
                    ),
                },
            ),
            "tm5_constant_a": (
                ["layer", "vertices", "nrows", "nobs"],
                data_S5p["tm5_constant_a"].values,
                {
                    "units": data_S5p["tm5_constant_a"].attrs.get("units", ""),
                    "long_name": data_S5p["tm5_constant_a"].attrs.get("long_name", ""),
                },
            ),
            "tm5_constant_b": (
                ["layer", "vertices", "nrows", "nobs"],
                data_S5p["tm5_constant_b"].values,
                {
                    "units": data_S5p["tm5_constant_b"].attrs.get("units", ""),
                    "long_name": data_S5p["tm5_constant_b"].attrs.get("long_name", ""),
                },
            ),
            "psurf": (
                ["nrows", "nobs"],
                data_S5p["surface_pressure"].values,
                {
                    "units": data_S5p["surface_pressure"].attrs.get("units", ""),
                    "long_name": data_S5p["surface_pressure"].attrs.get(
                        "long_name", ""
                    ),
                },
            ),
            "clouds": (
                ["nrows", "nobs"],
                data_S5p["cloud_fraction_crb"].values,
                {
                    "units": data_S5p["cloud_fraction_crb"].attrs.get("units", ""),
                    "long_name": data_S5p["cloud_fraction_crb"].attrs.get(
                        "long_name", ""
                    ),
                },
            ),
        },
        coords={
            "lat": (["nrows", "nobs"], data_S5p["lat"].values),
            "lon": (["nrows", "nobs"], data_S5p["lon"].values),
            "time": ([], data_S5p.time_utc.mean().values),
            "orbit": ([], data_S5p["orbit"].values),
        },
        attrs=data_S5p.attrs,
    )

    data[product].values[data_S5p["qa_value"] < 0.75] = np.nan
    data[f"{product}_std"].values[data_S5p["qa_value"] < 0.75] = np.nan

    data.attrs.update({"QA value filter": "> 0.75"})

    return data


def save_file(data_S5p, path_open="./", path_save="./", delete=False, overwrite=None):
    """
    Save a file to the indicated directory.
    If the directory does not exist, it is created.
    If the file already exists, the user is asked to discard changes or
    overwrite the file.

    Paramaters
    ----------
    data_S5p : netCDF
        File to be saved to netCDF.
    path_open : str
        Path where the original file is stored.
    path_save : str
        Path to where the cropped file should be stored.
    delete : bool
        Indicate if the input file should be deleted.
    overwrite : None
        Answer to overwrite existing files. Default None, i.e. ask.
    """
    filename_output = (
        f'{data_S5p.attrs["source"]}_{data_S5p.attrs["original file name"]}'
    )
    file_exists = os.path.exists(os.path.join(path_save, filename_output))
    os.makedirs(path_save, exist_ok=True)

    if file_exists:
        if overwrite is None:
            overwrite = input(
                f"[WARNING] {filename_output} already exists in {path_save} "
                f"- overwrite? [y/n]"
            )
            while overwrite.lower() not in ['yes', 'y', 'no', 'n']:
                overwrite = input("Enter 'y' (overwrite) or 'n' (cancel).")

        if overwrite.lower() in ["no", "n"]:
            print("File not saved")

        elif overwrite.lower() in ["yes", "y"]:
            os.remove(os.path.join(path_save, filename_output))
            # sleep for 5-10 seconds because overwriting does not work otherwise
            time.sleep(10)
            data_S5p.to_netcdf(path=os.path.join(path_save, filename_output))
            print(f"\r{filename_output} replaced in directory {path_save}", end="")
    else:
        data_S5p.to_netcdf(path=os.path.join(path_save, filename_output))
        print(f"\r{filename_output} saved in directory {path_save}", end="")

    if delete:
        os.remove(os.path.join(path_open, data_S5p.attrs["original file name"]))


def crop_and_save(
    all_filenames,
    sources,
    distance,
    delete,
    overwrite=None,
    variable="nitrogendioxide_tropospheric_column",
    path_open="./",
    path_save="./",
):
    """
    Crop and save data.

    Paramaters
    ----------
    all_filenames : netCDF
        File to be saved to netCDF.
    sources : list
        Sources for which the data has to be cropped and saved.
    distance : float
        Distance between source and box to be calculated in meters.
    overwrite : None
        Answer to overwrite existing files. Default None, i.e. ask.
    path_open : str
        Path where the original file is stored.
    path_save : str
        Path to where the cropped file should be stored.
    """

    for file in all_filenames:
        data_S5p = open_netCDF(file, path=path_open)
        data_S5p = reduce_dims_and_vars(data_S5p)

        for source in sources.source.values:
            data_S5p_cropped, save = crop_data(data_S5p, source, distance, sources)
            if save:
                save_file(
                    data_S5p_cropped,
                    path_open=path_open,
                    path_save=path_save,
                    delete=delete,
                    overwrite=overwrite,
                )
            sys.stdout.flush()
    print()


def plot_extent(
    data_S5p,
    var,
    sources,
    vmin=None,
    vmax=None,
    zoom=True,
    qa=True,
    ha="left",
    va="center",
):
    """
    Create a map of the variable indicated.

    Paramaters
    ----------
    data_S5p : netCDF
        File from which the data should be plotted.
    var : str
        Variable which should be plotted
    sources: netCDF
        File of sources with their coordinates
    vmin : float
        Minimum value on the colourbar.
    vmax : float
        Maximum value on the colourbar.
    zoom : bool
        Indicate if the map should be zoomed to the minimum and maximum
        latitudes and longitudes which were used to select and download the
        data.
    qa : bool
        Only show data with a qa_value > 0.75.
    ha : str
        Horizontal alignment of the text ["left", "center", "right"]
    va : str
        Vertical alignment of the text ["bottom", "center", "top"]

    Returns
    -------
    Plot the data.
    """

    # TODO selct based on np.nan
    lon0, lat0, _ = ddeq.sources.get_location(sources, data_S5p.source)
    lon0, lat0 = lon0.values, lat0.values

    try:
        distance = data_S5p.attrs["distance around source [m]"]
    except KeyError:
        distance = data_S5p.attrs["distance around source [km]"] * 1e3

    min_lon, max_lon, min_lat, max_lat = get_bounding_box(lon0, lat0, distance)
    lon = data_S5p.lon
    lat = data_S5p.lat

    value = data_S5p[var]
    label = data_S5p[var].long_name
    units = data_S5p[var].units

    # filter values with qa_value > 0.75
    if qa:
        if "qa_value" in data_S5p.data_vars:
            value = np.where(data_S5p["qa_value"] > 0.75, value, np.nan)
        elif "clouds" in data_S5p.data_vars:
            value = np.where(data_S5p["clouds"] < 0.25, value, np.nan)

    if vmin == None and vmax == None:
        vmin = np.nanquantile(value, 0.01)
        vmax = np.nanquantile(value, 0.99)

    # calculate offset for text so that it does not overlap with the point
    # marker
    if ha == "left":
        x_offset = 0.15
    elif ha == "right":
        x_offset = -0.15

    # plot map and gridlines
    fig, ax = plt.subplots(subplot_kw={"projection": ccrs.PlateCarree()})
    ax.coastlines(resolution="10m", color="k", linewidth=1.0)
    ax.axis("equal")
    lines = cfeature.NaturalEarthFeature(
        category="cultural", name="admin_0_boundary_lines_land", scale="10m"
    )
    ax.add_feature(lines, edgecolor="k", facecolor="none", linewidth=1.0)
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False

    # plot data and source
    m = ax.pcolormesh(
        lon,
        lat,
        value,
        vmin=vmin,
        vmax=vmax,
        cmap="viridis",
        transform=ccrs.PlateCarree(),
        shading="auto",
    )
    ax.scatter(
        lon0,
        lat0,
        marker="o",
        s=20,
        c="black",
        edgecolor="white",
        transform=ccrs.PlateCarree(),
    )
    ax.text(
        lon0 + x_offset,
        lat0,
        data_S5p.source,
        clip_on=True,
        horizontalalignment=ha,
        verticalalignment=va,
        path_effects=[PathEffects.withStroke(linewidth=2.5, foreground="w")],
    )
    # \n to prevent the label from being cut off
    fig.colorbar(m, ax=ax).set_label(label=f"{label} [{units}] \n", wrap=True)
    ax.set_title(
        f'date: {pd.to_datetime(data_S5p.time.values.item()).strftime("%Y-%m-%d")}, '
        f"orbit: {data_S5p.orbit.values}"
    )

    if zoom:
        ax.set_xlim(min_lon, max_lon)
        ax.set_ylim(min_lat, max_lat)

    return fig


def plot_orbit(filename, variable="nitrogendioxide_tropospheric_column", path="./"):
    """
    Plot the whole orbit from the downloaded netCDF file.
    """
    # read in data and remove dimensions/variables
    data_S5p = open_netCDF(filename, path)
    data_S5p = reduce_dims_and_vars(data_S5p)

    vmin = np.nanquantile(data_S5p[variable], 0.01)
    vmax = np.nanquantile(data_S5p[variable], 0.99)

    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()
    ax.coastlines()
    data_S5p[variable].plot.pcolormesh(
        ax=ax, x="lon", y="lat", add_colorbar=True, cmap="viridis", vmin=vmin, vmax=vmax
    )

    plt.title(
        f'date: {pd.to_datetime(data_S5p.time.values.item()).strftime("%Y-%m-%d")}, '
        f"orbit: {data_S5p.orbit.values}"
    )


def select_images(files, radius, fraction, sources):
    """
    Plot all TROPOMI images from a given list of files and select them if they
    are suitable for plume detection.

    Parameters:
    -----------
    files: list
        List of files in a directory which should be selected
    radius: int
        Radius of pixels around the source which should have a qa_value > 0.75
    fraction: float
        Fraction of pixels in radius around the source which should have a qa_value > 0.75
    sources: netCDF
        File of sources with their coordinates

    Returns:
    --------
    useful_orbits: List
        List of all selected orbits
    """

    useful_orbits = np.array([])

    for file in files:

        data_S5p = xr.open_dataset(file)

        product = data_S5p.attrs["original file name"][11:19].replace("_", "")

        # find source and get qa value around the source:
        lon0, lat0, _ = ddeq.sources.get_location(sources, data_S5p.source)
        lon0, lat0 = lon0.values, lat0.values

        lon_closest, lat_closest, dist = ddeq.misc.find_closest(
            data_S5p, ("lon", "lat"), (lon0, lat0)
        )

        around_source = data_S5p[product][
            lon_closest - radius : lon_closest + radius + 1,
            lat_closest - radius : lat_closest + radius + 1,
        ]

        count = np.count_nonzero(around_source < 0.25)

        if count >= fraction * (2 * radius + 1) ** 2:
            figure = ddeq.download_S5P.plot_extent(
                data_S5p, product, sources, zoom=True, qa=True
            )
            plt.show()
            useful = input(
                f"Can this image be used for plume detection of {data_S5p.source} (y/n)?"
            )

            while useful.lower() not in ["yes", "y", "no", "n"]:
                useful = input("Enter 'y' (useful) or 'n' (not useful).")

            if useful.lower() in ["yes", "y"]:
                useful_orbits = np.append(useful_orbits, data_S5p.orbit.values)
        else:
            print(
                f"Orbit {data_S5p.orbit.values} does not contain "
                f"information fullfilling the given criteria."
            )

    return useful_orbits
