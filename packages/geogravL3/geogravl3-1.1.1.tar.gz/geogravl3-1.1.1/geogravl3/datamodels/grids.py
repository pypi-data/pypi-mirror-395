#!/usr/bin/env python

# SPDX-License-Identifier: GPL-3.0-or-later
# FileType: SOURCE
# SPDX-FileCopyrightText: 2025 GFZ Helmholtz Centre for Geosciences
# SPDX-FileCopyrightText: 2025, "Eva Boergens" at GFZ Potsdam
"""
Grid objects for working with 2D and 3D gridded data.

This module defines:
- GridBase: a base class with lat/lon coordinate handling
- Grid2DObject: 2D grids [nlat, nlon]
- Grid3DObject: 3D grids [ntime, nlat, nlon] with time axis
- Grid3DIceObject: Polar stereographic projected 3D grids [ntime, nx, ny] with time axis for Ice
"""
import copy
from abc import ABC
from logging import Logger

import numpy as np


class GridBase(ABC):
    """
    Base class for grid objects with lat/lon coordinates.

    Attributes
    ----------
    grid : np.ndarray
        A 2D array containing the grid [n x m].
    lon : np.ndarray
        A 1D array containing the longitude coordinates [m].
    lat : np.ndarray
        A 1D array containing the latitude coordinates [n].
    """

    def __init__(self, logger: Logger, grid: np.ndarray, lon: np.ndarray, lat: np.ndarray) -> None:
        """
        Initialize an GridBase instance with grids and coordinates.

        Args:
            logger (Logger): Logger instance for logging information and debugging messages.
            grid (np.ndarray): A 2D array containing the grid [n x m].
            lon (np.ndarray): A 1D array containing the longitude coordinates [m].
            lat (np.ndarray): A 1D array containing the latitude coordinates [n].

        Attributes:
            grid (np.ndarray): The grid.
            lon (np.ndarray): The longitude coordiantes of the grid
            lat (np.ndarray): the latitude coordinates of the grid

        Raises:
            ValueError: If the dimensions are not fitting together
        """
        self.grid = grid
        self.lon = lon
        self.lat = lat

        # Validate lon/lat dimensions
        if grid.shape[-1] != lon.shape[0] or grid.shape[-2] != lat.shape[0]:
            message = (
                f"Grid shape {grid.shape} does not match "
                f"lat ({lat.shape[0]}) and lon ({lon.shape[0]}) lengths"
            )
            logger.error(message)
            raise ValueError(message)

    # ----------------
    # Comparison helpers
    # ----------------
    def same_coords(self, other: "GridBase") -> bool:
        """
        Compare if this grid has the same lat/lon coordinates as another.

        Works for both 2D<->2D, 3D<->3D, and 2D<->3D.

        Returns
        -------
        Bool: True if same coordinates, False else
        """
        return (
            np.array_equal(self.lat, other.lat)
            and np.array_equal(self.lon, other.lon)
        )

    def copy(self, deep=True):
        """Return a copy of the object."""
        return copy.deepcopy(self) if deep else copy.copy(self)

    # Convenience properties
    @property
    def nlat(self) -> int:
        """
        Length of latitude array.

        Returns
        -------
        int: lengths of latitude array
        """
        return self.lat.shape[0]

    @property
    def nlon(self) -> int:
        """
        Length of longitude array.

        Returns
        -------
        int: lengths of longitude array
        """
        return self.lon.shape[0]

    @property
    def shape(self) -> tuple[int, ...]:
        """
        Shape of grid in longitude and latitude dimension.

        Returns
        -------
        tuple(int,int): (lengths of latitude array, lengths of longitude array)
        """
        return self.grid.shape

    def get_grid_area(self, radius: float = None) -> np.ndarray:
        """
        Area of the grid cells.

        radius (float): Reference radius. If omitted or set to None, the global constant earths_radius_iers is used

        Returns
        -------
        area (nd.array): Spherical area of the grid shape (lengths of latitude, lengths of longitude)
        """
        from ..utils.utils import get_constant  # import here to avoid circular import

        def _get_area(lon_ll, lat_ll, lon_ur, lat_ur, R):
            # returns area of rectangular on sphere, defined by corner points lower left ll and upper right ur
            deg_to_rad = get_constant('deg_2_rad')
            a = (np.abs((lon_ll - lon_ur) * deg_to_rad) *
                 np.abs((np.sin(lat_ll * deg_to_rad) - np.sin(lat_ur * deg_to_rad))) * R ** 2)
            return a

        if radius is None:
            radius = get_constant('earths_radius_iers')

        delta_lon = (self.lat.max() - self.lat.min()) / (self.nlat - 1) if self.nlat > 1 else 0.0
        delta_lat = (self.lon.max() - self.lon.min()) / (self.nlon - 1) if self.nlon > 1 else 0.0
        # Compute all band areas at once (vectorized)
        a_vals = np.array([
            _get_area(0, lat - delta_lat / 2, delta_lon, lat + delta_lat / 2, radius)
            for lat in self.lat
        ])
        # Handle poles explicitly
        pole_mask = np.isin(self.lat, [90, -90])
        a_vals[pole_mask] = (radius ** 2 * (delta_lon * np.pi / 180) * 2 * np.cos(np.deg2rad(90)) *
                             np.sin(np.deg2rad(delta_lat / 2)))

        w = np.repeat(a_vals[:, None], self.nlon, axis=1)
        return w

    def get_grid_info_dict(self) -> dict:
        """
        Get the grid information of self and store it in a grid info dict.

        Returns
        -------
        grid_infos (dict)
        """
        grid_info = {}
        grid_info["xsize"] = self.nlon
        grid_info["ysize"] = self.nlat
        grid_info["xfirst"] = self.lon[0]
        grid_info["xinc"] = self.lon[1] - self.lon[0]
        grid_info["yfirst"] = self.lat[0]
        grid_info["yinc"] = self.lat[1] - self.lat[0]
        return grid_info


class Grid2DObject(GridBase):
    """
    Represents 2D grids and associated coordinates.

    Attributes
    ----------
    grid : np.ndarray
        A 2D array containing the grid [n x m].
    lon : np.ndarray
        A 1D array containing the longitude coordinates [m].
    lat : np.ndarray
        A 1D array containing the latitude coordinates [n].
    """

    def __init__(self, logger: Logger, grid: np.ndarray, lon: np.ndarray, lat: np.ndarray) -> None:
        """
        Initialize an Grid2DObject instance with grids and coordinates.

        Args:
            logger (Logger): Logger instance for logging information and debugging messages.
            grid (np.ndarray): A 2D array containing the grid [n x m].
            lon (np.ndarray): A 1D array containing the longitude coordinates [m].
            lat (np.ndarray): A 1D array containing the latitude coordinates [n].

        Attributes:
            grid (np.ndarray): The grid.
            lon (np.ndarray): The longitude coordiantes of the grid
            lat (np.ndarray): the latitude coordinates of the grid

        Raises:
            ValueError: If the dimensions are not fitting together
        """
        if grid.ndim != 2:
            message = f"Grid2DObject expects 2D grid, got {grid.ndim}D"
            logger.error(message)
            raise ValueError(message)
        super().__init__(logger=logger, grid=grid, lon=lon, lat=lat)

    def to_Grid3DObject(self, logger, date):
        """Convert a Grid2DObject to a 3D Object with the provided time."""
        return Grid3DObject(logger=logger,
                            grid=np.expand_dims(self.grid, axis=0),
                            dates=np.array([date]),
                            lon=self.lon,
                            lat=self.lat)


class Grid3DObject(GridBase):
    """
    Represents 3D grids and associated coordinates.

    Attributes
    ----------
    grid : np.ndarray
        A 3D array containing the grid [t x n x m].
    dates : np.ndarray
        A 1D array containing the dates, as datetime.date objects, corresponding to the data [t].
    lon : np.ndarray
        A 1D array containing the longitude coordinates [m].
    lat : np.ndarray
        A 1D array containing the latitude coordinates [n].
    """

    def __init__(self, logger: Logger, grid: np.ndarray, dates: np.ndarray, lon: np.ndarray, lat: np.ndarray) -> None:
        """
        Initialize an Grid3DObject instance with grid, coordinates, and dates.

        Args:
            logger (Logger): Logger instance for logging information and debugging messages.
            grid (dt.date): A 3D array containing the grid [t x n x m].
            dates (np.ndarray): A 1D array containing the dates of the grid [t].
            lon (np.ndarray): A 1D array containing the longitude coordinates [m].
            lat (np.ndarray): A 1D array containing the latitude coordinates [n].

        Attributes:
            grid (np.ndarray): The grid.
            dates (np.ndarray): the dates in datetime.date format
            lon (np.ndarray): The longitude coordinates of the grid
            lat (np.ndarray): the latitude coordinates of the grid

        Raises:
            ValueError: If the dimensions are not fitting together
        """
        if grid.ndim != 3:
            message = f"Grid3DObject expects 3D grid, got {grid.ndim}D"
            logger.error(message)
            raise ValueError(message)

        if grid.shape[0] != dates.shape[0]:
            message = f"Time dimension mismatch: grid time={grid.shape[0]}, dates={dates.shape[0]}"
            logger.error(message)
            raise ValueError(message)

        super().__init__(logger=logger, grid=grid, lon=lon, lat=lat)
        self.dates = dates

    def to_Grid2DObject(self, logger: Logger, index: int) -> Grid2DObject:
        """Reduce Grid3DObject to Grid2DObject for one given timestep (index)."""
        return Grid2DObject(logger=logger, grid=np.squeeze(self.grid[index]), lon=self.lon, lat=self.lat)

    # Extra comparison for time dimension
    def same_time(self, other: "Grid3DObject") -> bool:
        """
        Compare if two 3D grids have the same time coordinates.

        Returns
        -------
        Bool: True if same time array, False else
        """
        return np.array_equal(self.dates, other.dates)

    def same_grid(self, other: "Grid3DObject") -> bool:
        """
        Compare if two 3D grids have the same coordinates in all dimensions(lat, lon, time).

        Returns
        -------
        Bool: True if same dimension, False else
        """
        return (
            np.array_equal(self.lat, other.lat)
            and np.array_equal(self.lon, other.lon)
            and np.array_equal(self.dates, other.dates)
        )

    @property
    def ntime(self) -> int:
        """
        Length of time array.

        Returns
        -------
        int: lengths of time array
        """
        return self.dates.shape[0]


class Grid3DIceObject():
    """
    Represents 3D grids and associated coordinates.

    Attributes
    ----------
    grid : np.ndarray
        A 3D array containing the grid [t x n x m].
    dates : np.ndarray
        A 1D array containing the dates, as datetime.date objects, corresponding to the data [t].
    x: : np.ndarray
        A 1D array containing the x coordinates  of the polar stereographic projection [m].
    y: : np.ndarray
        A 1D array containing the y coordinates  of the polar stereographic projection [n].
    lon : np.ndarray
        A 2D array containing the longitude coordinates of the grid [n x m].
    lat : np.ndarray
        A 2D array containing the latitude coordinates of the grid [n x m].
    projection: dict
        A dictionary containing the polar stereographic projection parameter in .
    """

    def __init__(self,
                 logger: Logger,
                 grid: np.ndarray,
                 dates: np.ndarray,
                 x: np.ndarray,
                 y: np.ndarray,
                 lon: np.ndarray,
                 lat: np.ndarray,
                 projection: dict,
                 area: np.ndarray = None
                 ) -> None:
        """
        Initialize an Grid3DIceObject instance with grid, coordinates (x, y, lon, lat), dates, and projection info.

        Args:
            logger (Logger): Logger instance for logging information and debugging messages.
            grid (dt.date): A 3D array containing the grid [t x n x m].
            dates (np.ndarray): A 1D array containing the dates of the grid in datetime.date format[t].
            x (np.ndarray): A 1D array containing the x coordinates [m].
            y (np.ndarray): A 1D array containing the y coordinates [n].
            lon (np.ndarray): A 2D array containing the longitude coordinates of the grid [n x m].
            lat (np.ndarray): A 2D array containing the latitude coordinates of the grid [n x m]
            area (np.ndarray): A 2D array containing the area per grid cell[n x m], Optional
            projection (dict): Dictionary storing projection parameters

        Raises:
            ValueError: If the dimensions are not fitting together
        """
        self.grid = grid
        self.dates = dates
        self.x = x
        self.y = y
        self.lon = lon
        self.lat = lat
        self.area = area
        self.projection = projection

        # Validate x,y dimensions
        if grid.shape[-1] != x.shape[0] or grid.shape[-2] != y.shape[0]:
            message = (f"Grid shape {grid.shape} does not match "
                       f"y ({y.shape[0]}) and x ({x.shape[0]}) lengths")
            logger.error(message)
            raise ValueError(message)
        if area is not None and area.shape != grid.shape[1::]:
            message = f"Area shape {area.shape} and Grid shape {grid.shape} does not match "
            logger.error(message)
            raise ValueError(message)
        if grid.shape[0] != dates.shape[0]:
            message = f"Time dimension mismatch: grid time={grid.shape[0]}, dates={dates.shape[0]}"
            logger.error(message)
            raise ValueError(message)
        if grid.shape[1::] != lon.shape or grid.shape[1::] != lat.shape:
            message = (
                f"Grid shape {grid.shape} does not match "
                f"lon ({lon.shape}) and lat ({lat.shape[0]}) shapes"
            )
            logger.error(message)
            raise ValueError(message)

    # Extra comparison for time dimension
    def same_time(self, other: "Grid3DIceObject") -> bool:
        """
        Compare if two 3D grids have the same time coordinates.

        Returns
        -------
        Bool: True if same time array, False else
        """
        return np.array_equal(self.dates, other.dates)

    def same_grid(self, other: "Grid3DIceObject") -> bool:
        """
        Compare if two 3D grids have the same coordinates in all dimensions(lat, lon, time).

        Returns
        -------
        Bool: True if same dimension, False else
        """
        return (
            np.array_equal(self.x, other.x)
            and np.array_equal(self.y, other.y)
            and np.array_equal(self.dates, other.dates)
        )

    def copy(self, deep=True):
        """Return a copy of the object."""
        return copy.deepcopy(self) if deep else copy.copy(self)

    @property
    def ntime(self) -> int:
        """
        Length of time array.

        Returns
        -------
        int: lengths of time array
        """
        return self.dates.shape[0]

    @property
    def ny(self) -> int:
        """
        Length of latitude array.

        Returns
        -------
        int: lengths of latitude array
        """
        return self.y.shape[0]

    @property
    def nx(self) -> int:
        """
        Length of longitude array.

        Returns
        -------
        int: lengths of x array
        """
        return self.x.shape[0]

    @property
    def shape(self) -> tuple[int, ...]:
        """
        Shape of grid in x and y dimension.

        Returns
        -------
        tuple(int,int): (lengths of y array, lengths of x array)
        """
        return self.grid.shape
