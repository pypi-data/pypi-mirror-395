"""
Topographic attributes extraction from DEM data
"""

import py3dep
import xrspatial
import geopandas as gpd


def extract_topographic_attributes(watershed_geom, resolution=30):
    """
    Extract topographic attributes from DEM data.
    
    Parameters
    ----------
    watershed_geom : shapely.geometry
        Watershed boundary geometry
    resolution : int, optional
        DEM resolution in meters (default: 30)
    
    Returns
    -------
    dict
        Topographic attributes with keys:
        - elev_mean: mean elevation (m)
        - elev_min: minimum elevation (m)
        - elev_max: maximum elevation (m)
        - elev_std: elevation standard deviation (m)
        - slope_mean: mean slope (%)
        - slope_std: slope standard deviation (%)
        - area_geospa_fabric: drainage area (km²)
    
    Raises
    ------
    Exception
        If DEM extraction fails
    """
    try:
        # Get DEM data
        dem = py3dep.get_dem(watershed_geom, resolution=resolution)
        dem_proj = dem.rio.reproject("EPSG:5070")  # Equal-area projection
        
        # Compute slope
        slope_deg = xrspatial.slope(dem_proj)
        slope_mpm = py3dep.deg2mpm(slope_deg)
        slope_pct = slope_mpm * 100
        
        # Calculate elevation statistics
        elevation_stats = {
            "elev_mean": float(dem_proj.mean().values),
            "elev_min": float(dem_proj.min().values),
            "elev_max": float(dem_proj.max().values),
            "elev_std": float(dem_proj.std().values),
        }
        
        # Calculate slope statistics
        slope_stats = {
            "slope_mean": float(slope_pct.mean().values),
            "slope_std": float(slope_pct.std().values),
        }
        
        # Calculate drainage area
        watershed_proj = gpd.GeoDataFrame(
            [1], geometry=[watershed_geom], crs="EPSG:4326"
        ).to_crs("EPSG:5070")
        area_km2 = watershed_proj.geometry.area.iloc[0] / 1e6
        
        topo_attrs = {
            **elevation_stats,
            **slope_stats,
            "area_geospa_fabric": area_km2,
        }
        
        return topo_attrs
        
    except Exception as e:
        raise Exception(f"Failed to extract topographic attributes: {str(e)}")
