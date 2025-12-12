"""
Multi-gauge comparison visualization for CAMELS attributes
Based on CHOSEN to CAMELS mapping approach
"""

import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import BoundaryNorm
from matplotlib.cm import ScalarMappable


def plot_attributes_comparison(
    attributes_df,
    attributes_to_plot,
    n_classes=6,
    colormap='RdYlBu',
    reverse_colormap=False,
    include_histogram=True,
    figure_title=None,
    figsize=None,
    save_path=None
):
    """
    Plot multiple CAMELS attributes on US maps for comparison across gauges.
    
    This function creates side-by-side maps showing the spatial distribution
    of selected attributes across multiple catchments, with optional histograms.
    
    Parameters
    ----------
    attributes_df : pd.DataFrame
        DataFrame containing gauge attributes. Must include:
        - 'gauge_id': Gauge identifier
        - 'gauge_lat': Latitude
        - 'gauge_lon': Longitude
        - Additional attribute columns to plot
    attributes_to_plot : list
        List of attribute column names to visualize
    n_classes : int, optional
        Number of color classes for quantile-based classification (default: 6)
    colormap : str, optional
        Matplotlib colormap name (default: 'RdYlBu')
    reverse_colormap : bool, optional
        Whether to reverse the colormap (default: False)
    include_histogram : bool, optional
        Whether to include histogram subplots (default: True)
    figure_title : str, optional
        Overall figure title
    figsize : tuple, optional
        Figure size (width, height). If None, auto-calculated
    save_path : str, optional
        Path to save the figure
    
    Returns
    -------
    matplotlib.figure.Figure
        The created figure
    
    Examples
    --------
    >>> from camels_attributes import extract_multiple_gauges, plot_attributes_comparison
    >>> 
    >>> # Extract attributes for multiple gauges
    >>> gauge_ids = ['01031500', '02177000', '06803530', '08324000']
    >>> df = extract_multiple_gauges(gauge_ids)
    >>> 
    >>> # Create comparison map
    >>> fig = plot_attributes_comparison(
    >>>     df,
    >>>     attributes_to_plot=['aridity', 'slope_mean', 'frac_forest'],
    >>>     colormap='RdYlBu',
    >>>     reverse_colormap=True,
    >>>     figure_title='Catchment Characteristics Comparison',
    >>>     save_path='comparison_map.png'
    >>> )
    """
    
    # Validation
    required_cols = ['gauge_id', 'gauge_lat', 'gauge_lon']
    missing_cols = [col for col in required_cols if col not in attributes_df.columns]
    if missing_cols:
        raise ValueError(f"DataFrame missing required columns: {missing_cols}")
    
    for attr in attributes_to_plot:
        if attr not in attributes_df.columns:
            raise ValueError(f"Attribute '{attr}' not found in DataFrame columns")
    
    # Setup figure
    num_plots = len(attributes_to_plot)
    if figsize is None:
        figsize = (6 * num_plots, 6 if not include_histogram else 7)
    
    if include_histogram:
        fig = plt.figure(figsize=figsize)
        gs = gridspec.GridSpec(2, num_plots, height_ratios=[5, 1], hspace=0.3)
    else:
        fig, axes = plt.subplots(1, num_plots, figsize=figsize,
                                subplot_kw={'projection': ccrs.PlateCarree()})
        if num_plots == 1:
            axes = [axes]
    
    # Get colormap
    cmap = plt.get_cmap(colormap)
    if reverse_colormap:
        cmap = cmap.reversed()
    
    # Plot each attribute
    for i, attr in enumerate(attributes_to_plot):
        # Setup map axis
        if include_histogram:
            ax_map = plt.subplot(gs[0, i], projection=ccrs.PlateCarree())
            ax_hist = plt.subplot(gs[1, i])
        else:
            ax_map = axes[i]
        
        # Get data for this attribute
        df_plot = attributes_df[['gauge_id', 'gauge_lat', 'gauge_lon', attr]].dropna()
        
        if len(df_plot) == 0:
            ax_map.text(0.5, 0.5, f'No data for {attr}',
                       ha='center', va='center', transform=ax_map.transAxes)
            continue
        
        values = df_plot[attr]
        lons = df_plot['gauge_lon']
        lats = df_plot['gauge_lat']
        
        # Create quantile-based classification
        bounds = np.round(np.quantile(values, np.linspace(0, 1, n_classes + 1)), 2)
        # Ensure unique bounds
        bounds = np.unique(bounds)
        if len(bounds) < 2:
            bounds = np.array([values.min(), values.max()])
        
        norm = BoundaryNorm(boundaries=bounds, ncolors=cmap.N)
        
        # Setup map extent (CONUS)
        ax_map.set_extent([-125, -67, 25, 50], crs=ccrs.PlateCarree())
        
        # Add map features
        ax_map.add_feature(cfeature.STATES.with_scale('50m'), 
                          edgecolor='gray', linewidth=0.5)
        ax_map.add_feature(cfeature.BORDERS.with_scale('50m'), 
                          linewidth=0.5, edgecolor='black')
        ax_map.coastlines(resolution='50m', linewidth=0.5)
        
        # Add title with letter label
        ax_map.set_title(f"({chr(97+i)}) {attr}", fontsize=14, fontweight='bold')
        
        # Plot catchments as colored points
        sc = ax_map.scatter(
            lons, lats,
            c=values,
            cmap=cmap,
            norm=norm,
            s=50,
            edgecolor='black',
            linewidth=0.3,
            alpha=0.8,
            zorder=5,
            transform=ccrs.PlateCarree()
        )
        
        # Add colorbar
        cbar = plt.colorbar(
            ScalarMappable(norm=norm, cmap=cmap),
            ax=ax_map,
            orientation='horizontal',
            pad=0.05,
            aspect=30,
            shrink=0.8
        )
        cbar.set_label(attr, fontsize=10)
        cbar.ax.tick_params(labelsize=8)
        
        # Add histogram if requested
        if include_histogram:
            ax_hist.hist(values, bins=15, color='steelblue', 
                        edgecolor='black', alpha=0.7)
            ax_hist.set_xlabel(attr, fontsize=10)
            ax_hist.set_ylabel('Count', fontsize=10)
            ax_hist.tick_params(labelsize=8)
            ax_hist.grid(True, alpha=0.3)
            
            # Add statistics text
            stats_text = f"n={len(values)}\nμ={values.mean():.2f}\nσ={values.std():.2f}"
            ax_hist.text(0.98, 0.98, stats_text,
                        transform=ax_hist.transAxes,
                        va='top', ha='right',
                        fontsize=8,
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
    
    # Add overall title
    if figure_title:
        fig.suptitle(figure_title, fontsize=16, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    
    # Save if requested
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✓ Comparison map saved: {save_path}")
    
    return fig


def create_multi_gauge_comparison(
    gauge_ids,
    attributes_to_plot,
    **kwargs
):
    """
    Convenience function to extract attributes and create comparison map in one step.
    
    Parameters
    ----------
    gauge_ids : list
        List of USGS gauge IDs
    attributes_to_plot : list
        List of attribute names to visualize
    **kwargs
        Additional arguments passed to plot_attributes_comparison()
    
    Returns
    -------
    tuple
        (attributes_df, figure) - The extracted attributes and created figure
    
    Examples
    --------
    >>> from camels_attributes.multi_gauge_viz import create_multi_gauge_comparison
    >>> 
    >>> gauge_ids = ['01031500', '02177000', '06803530']
    >>> df, fig = create_multi_gauge_comparison(
    >>>     gauge_ids,
    >>>     attributes_to_plot=['aridity', 'frac_forest', 'q_mean'],
    >>>     figure_title='Regional Comparison',
    >>>     save_path='regional_map.png'
    >>> )
    """
    from .extractor import extract_multiple_gauges
    
    print(f"Extracting attributes for {len(gauge_ids)} gauges...")
    df = extract_multiple_gauges(gauge_ids)
    
    print(f"Creating comparison map for {len(attributes_to_plot)} attributes...")
    fig = plot_attributes_comparison(df, attributes_to_plot, **kwargs)
    
    return df, fig
