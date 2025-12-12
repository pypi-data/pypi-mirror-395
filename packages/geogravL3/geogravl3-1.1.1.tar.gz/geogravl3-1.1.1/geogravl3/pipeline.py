#!/usr/bin/env python

# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""Main module."""
import os
from typing import Dict, Union, List

import numpy as np

from geogravl3.io.writers import write_tws_nc, write_obp_nc, write_ice_nc, save_timeseries_to_csv, \
    save_ice_timeseries_to_csv
from geogravl3.processing.grid_processing.l3_processing import (
    tws_processing, im_processing, obp_processing, prepare_land_ocean_masks
)
from geogravl3.processing.grid_processing.remove_coseismic import get_eq_filenames
from geogravl3.processing.shc_processing.degree_1_terms import estimate_degree1_sh
from geogravl3.processing.shc_processing.replace_low_degrees import replace_low_degrees
from geogravl3.processing.spherical_harmonics.sh_synthesis import sh_synthesis
from geogravl3.processing.shc_processing.gia_correction import reduce_gia_model
from geogravl3.processing.shc_processing.run_filter import run_filter
from geogravl3.processing.shc_processing.s2_aliased_signal import remove_s2_aliased_signal
from geogravl3.processing.timeseries import remove_mean_sh
from geogravl3.datamodels.grids import Grid3DObject, Grid3DIceObject
from geogravl3.datamodels.shc import SHObject
from geogravl3.io.readers import read_grid_definition, read_load_love_numbers, read_input_folder, \
    read_region_geojson, read_ice_basins_from_kernel
from geogravl3.utils.utils import create_logger
from geogravl3.utils.date_utils import datetime_to_date_float, reference_period_2_datetime
from geogravl3.config import Config
from geogravl3.processing.l4_processing.l4_timeseries import (
    precompute_region_masks, compute_regional_timeseries,
    compute_regional_timeseries_std, compute_regional_ice_timeseries, compute_regional_ice_timeseries_std)
from geogravl3.data_downloads.downloads import download_resources


class ResultObjects:
    """
    Define an object to store all intermediate results.

    Attributes
    ----------
    type (str): either shc or grid
    name (str): describing latest processing step
    value: Value of latest processing step, either List[SHObject], Grid3DObject,
    or Dict[str, Union[Grid3DObject (for TWS and OBP), Grid3DIceObject (for ice)]]
    filter_name (str): name of the applied filter for this processing line. None before filtering
    domain (str): domain name after the domain specific processing

    """

    def __init__(self, type: str = None,
                 name: str = None,
                 value: Union[List[SHObject], Grid3DObject, Dict[str, Union[Grid3DObject, Grid3DIceObject]]] = None,
                 filter_name: str = None,
                 domain: str = None
                 ):
        """
        Initialize a ResultObject instance.

        Attributes:
        type: Category in which the results fall, either 'shc' or 'grid'
        name: Specific name related to the processing step, should be self-explanatory
        filter_name: Name of the applied filter, None before filtering
        domain: Name of the domain, None before domain specific stuff
        value: Result to be stored, either list

        """
        self.type = type
        self.name = name
        self.value = value
        self.filter_name = filter_name
        self.domain = domain


def run_pipeline(*, config_dict: dict):
    """
    Execute the pipeline with a provided configuration dictionary and set up logging.

    This function initializes and configures the pipeline by accepting a configuration
    dictionary, validating, and transforming it into the required format. It also sets up
    logging for both file output and console output using the provided settings in the
    configuration.

    Parameters:
        config_dict (dict): Dictionary containing pipeline configurations. This must
        adhere to the structure and types expected by the `Config` class.

    Raises:
        Exception: If there is an issue with validating, setting up the configuration,
        or initializing the logging pipeline, an exception is raised that includes
        details of the underlying issue.
    """
    # get a logger
    logger = create_logger(config_dict["mandatory_settings"]["output_folder"],
                           config_dict["optional_settings"]["logging_level"])

    # download resource files if not already downloaded or running within a local repository
    download_resources(logger=logger)

    try:
        config_dict = Config(**config_dict).model_dump(by_alias=True)
        logger.info(f"Starting geogravL3 with the following configuration: {config_dict}")
    except Exception as e:
        message = f"Failed to start geogravL3 pipeline => {e}"
        logger.error(message)
        raise Exception(message) from e

    # read input files into a list of SH coefficient Objects
    logger.info("Reading input data")
    input_shc, dict_date_to_filename = read_input_folder(file_list=config_dict["mandatory_settings"]["input_folder"],
                                                         max_degree=config_dict["optional_settings"]["max_degree"],
                                                         logger=logger)
    # set up a dictionary to store the results
    results = [ResultObjects('shc', 'input_data', input_shc)]

    # Reduce mean field
    times = datetime_to_date_float(np.array([s.date for s in results[0].value]))
    ref_period = reference_period_2_datetime(config_dict["optional_settings"]["time_mean"])
    if len(results[0].value) == 1:
        logger.info("Only one time step in input data, remove mean skipped.")
        results = [ResultObjects('shc', 'reduced_mean', results[0].value)]
    else:
        logger.info(f"Removal of mean field of reference period {ref_period}: ")
        if len(ref_period) == 2:
            mean_field_dict = remove_mean_sh(logger=logger, times=times, sh_list=results[0].value,
                                             start_idx=ref_period[0], end_idx=ref_period[1])
        elif len(ref_period) == 1:
            mean_field_dict = remove_mean_sh(logger=logger, times=times, sh_list=results[0].value,
                                             start_idx=ref_period[0], end_idx=ref_period[0])
        else:
            mean_field_dict = remove_mean_sh(logger=logger, times=times, sh_list=results[0].value)

        results = [ResultObjects('shc', 'reduced_mean', mean_field_dict['sh_demeaned'])]

    # filtering with all filters provided in the config file

    flag_nofilt = any(
        domain in ice
        for domain in config_dict["optional_settings"]["domain"]
        for ice in ["ice", "greenland", "antarctica"]
    )

    filters = config_dict["optional_settings"]["filter"]
    if filters is not None:
        logger.info(f"Filtering with all filters provided in the config file: "
                    f"{config_dict['optional_settings']['filter']}")
        l3_results = []
        l3_results.extend([ResultObjects('shc', 'filtered',
                                         run_filter(filter_name=f,
                                                    input_shc=results[0].value,
                                                    lmax=None,
                                                    dict_date_to_filename=dict_date_to_filename,
                                                    logger=logger),
                                         filter_name=f)
                           for f in filters])

        if flag_nofilt:
            l3_results.append(ResultObjects('shc', 'filtered',
                                            results[0].value,
                                            filter_name='nofilt'))
        results = l3_results
    elif flag_nofilt:
        logger.info("Filtering skipped")
        results = [ResultObjects('shc', 'filtered',
                                 results[0].value,
                                 filter_name='nofilt')]
    else:
        logger.info("Filtering skipped")

    # replacement of c20
    if config_dict["optional_settings"]['lowdegree_coefficients'] is not None:
        logger.info("Replace low degree harmonics")

        l3_results = []
        for r in results:
            output_shc = replace_low_degrees(logger=logger,
                                             shc=r.value,
                                             filename_replacements=config_dict["optional_settings"][
                                                 "lowdegree_coefficients"])
            l3_results.append(ResultObjects('shc', 'lowdegree_replaced',
                                            output_shc, filter_name=r.filter_name))
        results = l3_results

    # subtract GIA model
    if config_dict["optional_settings"]["gia_model"] is not None:
        logger.info("Subtracting GIA model")

        l3_results = []
        for r in results:
            output_shc = reduce_gia_model(logger=logger,
                                          filename_gia_model=config_dict["optional_settings"]["gia_model"],
                                          shc=r.value)
            l3_results.append(ResultObjects('shc', 'gia_reduced',
                                            output_shc, filter_name=r.filter_name))
        results = l3_results

    # insert coefficients of geocentre motion
    if config_dict["optional_settings"]["insert_geocenter_motion"]:
        logger.info("Insert geocentre motion to degree 1 coefficients.")
        load_love_numbers = read_load_love_numbers(logger=logger,
                                                   file_name=config_dict["optional_settings"]["love_numbers"])
        lo_mask = prepare_land_ocean_masks(logger=logger,
                                           file_land_ocean_mask=config_dict['optional_settings']['land_ocean_mask'])

        l3_results = []
        for r in results:
            output_shc, cs1 = estimate_degree1_sh(logger=logger,
                                                  sh_objects=r.value,
                                                  lomask=lo_mask,
                                                  lmax=45,
                                                  love_numbers=load_love_numbers)
            l3_results.append(ResultObjects('shc', 'deg_1_replaces',
                                            output_shc, filter_name=r.filter_name))
        results = l3_results

    # subtract aliasing signal 161d period
    if config_dict["optional_settings"]["remove_s2_aliased_signal"]:
        logger.info("Remove s2 aliased signal (161-day period)")

        l3_results = []
        for r in results:

            if len(ref_period) == 2:
                output_shc = remove_s2_aliased_signal(logger=logger,
                                                      shc=r.value,
                                                      start_idx=ref_period[0],
                                                      end_idx=ref_period[0])
            elif len(ref_period) == 1:
                logger.warning("WARNING: s2 aliased signal cannot be estimated from a single reference month! "
                               "Estimated from the whole time series")
                output_shc = remove_s2_aliased_signal(logger=logger, shc=r.value)
            else:
                output_shc = remove_s2_aliased_signal(logger=logger, shc=r.value)
            l3_results.append(ResultObjects('shc', 's2_removed',
                                            output_shc, filter_name=r.filter_name))
        results = l3_results

    # SH synthesis
    if any(domain in land_ocean
           for domain in config_dict["optional_settings"]["domain"]
           for land_ocean in ["all", "land", "ocean"]):
        logger.info("SH synthesis")
        grid_info = read_grid_definition(file_name=config_dict["optional_settings"]["grid"])
        load_love_numbers = read_load_love_numbers(logger=logger,
                                                   file_name=config_dict["optional_settings"]["love_numbers"])

        l3_results = []
        for r in results:
            if r.filter_name == 'nofilt':
                l3_results.append(r)
            else:
                output_grid = sh_synthesis(logger=logger,
                                           shc=r.value,
                                           gridinfo=grid_info,
                                           love_numbers=load_love_numbers,
                                           n_max=config_dict["optional_settings"]["max_degree"],
                                           ref_surface=config_dict["optional_settings"]["reference_surface"])
                l3_results.append(ResultObjects('grid', 'shs',
                                                output_grid, filter_name=r.filter_name))
        results = l3_results

    # Prepare Land domain, terrestrial water storage (TWS)
    l3_results = []
    if any(domain in land
           for domain in config_dict["optional_settings"]["domain"]
           for land in ["all", "land"]):
        list_earthquakes_filenames = get_eq_filenames(config_dict["optional_settings"]["earthquake"])
        if 'land' in config_dict["optional_settings"]["domain"]:
            logger.info("TWS calculation")
            for r in results:
                if r.filter_name == 'nofilt':
                    continue
                tws, tws_std = tws_processing(logger=logger,
                                              input_ewh_grid=r.value,
                                              file_land_ocean_mask=config_dict["optional_settings"]["land_ocean_mask"],
                                              domain='land',
                                              file_ice_mask=config_dict["optional_settings"]["land_ice_mask"],
                                              list_earthquakes=list_earthquakes_filenames)
                l3_results.append(ResultObjects(type='grid',
                                                name='tws',
                                                value={'tws': tws, 'tws_std': tws_std},
                                                filter_name=r.filter_name,
                                                domain='land'))
                logger.info('Save tws.nc')
                write_tws_nc(logger=logger,
                             filename=os.path.join(config_dict['mandatory_settings']['output_folder'], 'tws.nc'),
                             tws=tws,
                             std_tws=tws_std)
        # Use land processing globally (no masking of ice and ocean)
        if 'all' in config_dict["optional_settings"]["domain"]:
            logger.info("TWS global calculation")
            for r in results:
                if r.filter_name == 'nofilt':
                    continue
                tws, tws_std = tws_processing(logger=logger,
                                              input_ewh_grid=r.value,
                                              file_land_ocean_mask=config_dict["optional_settings"]["land_ocean_mask"],
                                              domain='all',
                                              list_earthquakes=list_earthquakes_filenames)
                l3_results.append(ResultObjects(type='grid',
                                                name='tws_global',
                                                value={'tws': tws, 'tws_std': tws_std},
                                                filter_name=r.filter_name,
                                                domain='land'))
                logger.info('Save tws_global.nc')
                write_tws_nc(logger=logger,
                             filename=os.path.join(config_dict['mandatory_settings']['output_folder'], 'tws_global.nc'),
                             tws=tws,
                             std_tws=tws_std)

    # Prepare ocean domain, ocean bottom pressure (OBP)
    if 'ocean' in config_dict["optional_settings"]["domain"]:
        logger.info("OBP calculation")
        list_earthquakes_filenames = get_eq_filenames(config_dict["optional_settings"]["earthquake"])

        for r in results:
            if r.filter_name == 'nofilt':
                continue
            sle, sle_std, residual_obp, residual_obp_std = (
                obp_processing(logger=logger,
                               input_ewh_grid=r.value,
                               file_land_ocean_mask=config_dict["optional_settings"]["land_ocean_mask"],
                               love_numbers=load_love_numbers,
                               list_earthquakes=list_earthquakes_filenames))
            l3_results.append(ResultObjects(type='grid',
                                            name='obp',
                                            value={'sle': sle, 'sle_std': sle_std,
                                                   'residual_obp': residual_obp, 'residual_obp_std': residual_obp_std},
                                            filter_name=r.filter_name,
                                            domain='ocean'))
            logger.info('Save obp.nc')
            write_obp_nc(logger=logger,
                         filename=os.path.join(config_dict['mandatory_settings']['output_folder'], 'obp.nc'),
                         resobp=residual_obp,
                         std_resobp=residual_obp_std,
                         barslv=sle,
                         std_barslv=sle_std)

    # Prepare ice domain, ice mass (IM)
    if any(domain == ice
           for domain in config_dict["optional_settings"]["domain"]
           for ice in ["ice", "greenland", "antarctica"]):
        logger.info("IM calculation")
        result_nofilt = [r for r in results if r.filter_name == "nofilt"][0]
        load_love = read_load_love_numbers(logger=logger, file_name=config_dict["optional_settings"]["love_numbers"])
        if any(domain in ice
               for domain in config_dict["optional_settings"]["domain"]
               for ice in ["ice", "greenland"]):
            im, im_std = im_processing(
                shc=result_nofilt.value,
                file_name_sensitivity_kernel=config_dict["optional_settings"]["sensitivity_kernel_greenland"],
                love_numbers=load_love,
                logger=logger)
            l3_results.append(ResultObjects(type='grid',
                                            name='im_greenland',
                                            value={'im': im, 'im_std': im_std},
                                            filter_name='nofilt',
                                            domain='greenland'))
            logger.info('Save im_greenland.nc')
            write_ice_nc(os.path.join(config_dict['mandatory_settings']['output_folder'], 'im_greenland.nc'),
                         dm=im,
                         std_dm=im_std)
        if any(domain in ice
               for domain in config_dict["optional_settings"]["domain"]
               for ice in ["ice", "antarctica"]):
            im, im_std = im_processing(
                shc=result_nofilt.value,
                file_name_sensitivity_kernel=config_dict["optional_settings"]["sensitivity_kernel_antarctica"],
                love_numbers=load_love,
                logger=logger)
            l3_results.append(ResultObjects(type='grid',
                                            name='im_antarctica',
                                            value={'im': im, 'im_std': im_std},
                                            filter_name='nofilt',
                                            domain='antarctica'))
            logger.info('Save im_antarctica.nc')
            write_ice_nc(os.path.join(config_dict['mandatory_settings']['output_folder'], 'im_antarctica.nc'),
                         dm=im,
                         std_dm=im_std)

    # --- Regional time series computation ---
    region_file = config_dict["optional_settings"]["region_land_geojson"]
    if (region_file is not None and any(domain in land
                                        for domain in config_dict["optional_settings"]["domain"]
                                        for land in ["all", "land"])):
        logger.info("Compute mean time series for tws.")
        # Takes the first of "tws" and "tws_global", does not matter for the time series which
        tws_results = [obj for obj in l3_results if "tws" in obj.name][0]
        tws = tws_results.value['tws']
        tws_std = tws_results.value['tws_std']

        # Precompute masks once (to avoid recomputation)
        regions = read_region_geojson(logger=logger, file_path=region_file)
        region_masks_tws = precompute_region_masks(grid=tws, regions=regions)

        # Compute regional mean and std time series using precomputed masks
        mean_ts = compute_regional_timeseries(
            grid=tws,
            regions=regions,
            precomputed_masks=region_masks_tws,
        )
        std_ts = compute_regional_timeseries_std(
            grid=tws_std,
            regions=regions,
            precomputed_masks=region_masks_tws,
        )
        save_timeseries_to_csv(file_path=os.path.join(config_dict['mandatory_settings']['output_folder'],
                                                      'tws_timeseries.csv'),
                               means_dict=mean_ts,
                               stds_dict=std_ts,
                               dates=tws.dates)

    # OBP
    region_file = config_dict["optional_settings"]["region_ocean_geojson"]
    if region_file is not None and 'ocean' in config_dict["optional_settings"]["domain"]:
        logger.info("Compute mean time series for ocean.")

        obp_results = [obj for obj in l3_results if "obp" in obj.name][0]
        sle = obp_results.value['sle']
        sle_std = obp_results.value['sle_std']
        residual_obp = obp_results.value['residual_obp']
        residual_obp_std = obp_results.value['residual_obp_std']

        # Precompute masks once (to avoid recomputation)
        regions = read_region_geojson(logger=logger,  file_path=region_file)
        region_masks_tws = precompute_region_masks(grid=sle, regions=regions)

        # Compute regional mean and std time series using precomputed masks
        mean_ts_sle = compute_regional_timeseries(
            grid=sle,
            regions=regions,
            precomputed_masks=region_masks_tws,
        )
        std_ts_sle = compute_regional_timeseries_std(
            grid=sle_std,
            regions=regions,
            precomputed_masks=region_masks_tws,
        )
        save_timeseries_to_csv(
            file_path=os.path.join(config_dict['mandatory_settings']['output_folder'], 'barslv_timeseries.csv'),
            means_dict=mean_ts_sle,
            stds_dict=std_ts_sle,
            dates=sle.dates)

        mean_ts_resobp = compute_regional_timeseries(
            grid=residual_obp,
            regions=regions,
            precomputed_masks=region_masks_tws,
        )
        std_ts_resobp = compute_regional_timeseries_std(
            grid=residual_obp_std,
            regions=regions,
            precomputed_masks=region_masks_tws,
        )
        save_timeseries_to_csv(
            file_path=os.path.join(config_dict['mandatory_settings']['output_folder'], 'resobp_timeseries.csv'),
            means_dict=mean_ts_resobp,
            stds_dict=std_ts_resobp,
            dates=results[0].value.dates)

    # IM
    if any(domain == ice
           for domain in config_dict["optional_settings"]["domain"]
           for ice in ["ice", "greenland"]):
        basin_dict = (
            read_ice_basins_from_kernel(logger=logger,
                                        file_path=config_dict["optional_settings"]["sensitivity_kernel_greenland"]))

        gis_results = [obj for obj in l3_results if "greenland" in obj.name][0]
        im = gis_results.value['im']
        im_std = gis_results.value['im_std']

        mean_ts = compute_regional_ice_timeseries(grid=im, basin_dict=basin_dict)
        mean_ts_std = compute_regional_ice_timeseries_std(logger=logger, grid=im_std, basin_dict=basin_dict)

        save_ice_timeseries_to_csv(
            file_path=os.path.join(config_dict['mandatory_settings']['output_folder'], 'greenland_timeseries.csv'),
            mean_dict=mean_ts,
            std_dict=mean_ts_std,
            dates=im.dates)

    if any(domain in ice
           for domain in config_dict["optional_settings"]["domain"]
           for ice in ["ice", "antarctica"]):
        basin_dict = (
            read_ice_basins_from_kernel(logger=logger,
                                        file_path=config_dict["optional_settings"]["sensitivity_kernel_antarctica"]))

        gis_results = [obj for obj in l3_results if "antarctica" in obj.name][0]
        im = gis_results.value['im']
        im_std = gis_results.value['im_std']

        mean_ts = compute_regional_ice_timeseries(grid=im, basin_dict=basin_dict)
        mean_ts_std = compute_regional_ice_timeseries_std(logger=logger, grid=im_std, basin_dict=basin_dict)

        save_ice_timeseries_to_csv(
            file_path=os.path.join(config_dict['mandatory_settings']['output_folder'], 'antarctica_timeseries.csv'),
            mean_dict=mean_ts,
            std_dict=mean_ts_std,
            dates=im.dates)
