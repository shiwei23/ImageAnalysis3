import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import numpy as np
import os

from . import _dpi,_single_col_width,_double_col_width,_single_row_height,_ref_bar_length, _ticklabel_size,_ticklabel_width,_font_size

# draw distance map
def plot_distance_map(distmap, ax=None, cmap='seismic_r', 
                      color_limits=[0,1500], color_norm=None, imshow_kwargs={},
                      ticks=None, tick_labels=None, 
                      tick_label_length=_ticklabel_size, tick_label_width=_ticklabel_width, 
                      font_size=_font_size, ax_label=None,
                      add_colorbar=True, colorbar_labels=None,
                      figure_width=_single_col_width, figure_dpi=_dpi, 
                      save=False, save_folder='.', save_basename='distmap.png', verbose=True):
    """Function to plot distance maps"""
    
    ## check inputs
    if np.shape(distmap)[0] != np.shape(distmap)[1]:
        raise IndexError(f"Wrong input dimension for distmap, should be nxn matrix but {distmap.shape} is given")

    
    ## create image
    if ax is None:
        fig, ax = plt.subplots(figsize=(figure_width, figure_width),
                               dpi=figure_dpi)
    
    _distmap = distmap.copy()
    _distmap[_distmap<min(color_limits)] = min(color_limits)
    # generate imshow object
    _im = ax.imshow(_distmap, cmap=cmap, interpolation='nearest', norm=color_norm,
                    vmin=min(color_limits), vmax=max(color_limits), **imshow_kwargs)
    # border
    [i[1].set_linewidth(tick_label_width) for i in ax.spines.items()]
    # ticks
    ax.tick_params('both', labelsize=font_size, 
                   width=tick_label_width, length=tick_label_length,
                   pad=1)
    if ticks is None:
        _used_ticks = np.arange(0, len(_distmap), 10**np.floor(np.log10(len(distmap))))
    else:
        _used_ticks = ticks
    ax.set_xticks(_used_ticks, minor=False)
    ax.set_yticks(_used_ticks, minor=False)
    # tick labels
    if tick_labels is not None:
        # apply tick labels 
        if len(tick_labels) == len(_distmap):
            _used_labels = [_l for _i, _l in enumerate(tick_labels) if _i in _used_ticks]
            ax.set_xticklabels(_used_labels)
            ax.set_yticklabels(_used_labels)
        elif len(tick_labels) == len(_used_ticks):
            ax.set_xticklabels(tick_labels)
            ax.set_yticklabels(tick_labels)
        else:
            print(f"tick_labels length:{len(tick_labels)} doesn't match distmap:{len(_distmap)}, skip!")
    # axis labels
    if ax_label is not None:
        ax.set_xlabel(ax_label, labelpad=2, fontsize=font_size+1)
    # colorbar    
    if add_colorbar:
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='6%', pad="2%")
        cb = fig.colorbar(_im, cax=cax, orientation='vertical')
        cax.tick_params(labelsize=font_size, width=tick_label_width, length=tick_label_length-1,pad=1)
        # border
        cb.outline.set_linewidth(tick_label_width)
    # save
    if save:
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        save_filename = os.path.join(save_folder, save_basename)
        if '.png' not in save_filename:
            save_filename += '.png'
        plt.savefig(save_filename, transparent=True)

    # return
    return ax
