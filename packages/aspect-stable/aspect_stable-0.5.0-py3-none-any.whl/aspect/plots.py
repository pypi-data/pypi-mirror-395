import logging

import numpy as np
from matplotlib import pyplot as plt, gridspec, colors, rc_context
from .io import Aspect_Error, cfg
from lime.plotting.plots import theme
from .tools import detection_function, stratify_sample
import matplotlib.patheffects as path_effects

_logger = logging.getLogger("aspect")


def decision_matrix_plot(matrix_arr, output_address=None, categories=None, exclude_diagonal=True, show_categories=False,
                         cfg_fig=None):

    # Try to find from database if None provided
    matrix_name = None
    if isinstance(matrix_arr, str):
        if matrix_arr in cfg['decision_matrices']:
            matrix_name = str(matrix_arr)
            matrix_arr = np.array(cfg['decision_matrices'][matrix_arr])
        else:
            raise Aspect_Error(f'Decision matrix "{matrix_arr}" not found in configuration file please')


    # Default categories from configuration file
    default_categories = cfg['metadata']['category_order']

    # Trim matrix to the categories requested
    if categories is not None:
        indices = [default_categories.index(label) for label in categories]
        matrix_arr = matrix_arr[np.ix_(indices, indices)]
    else:
        categories = default_categories

    # Number of categories
    n_categories = matrix_arr.shape[0]

    # Set the diagonal to a distinct value (e.g., -1) to differentiate it
    if exclude_diagonal:
        np.fill_diagonal(matrix_arr, -1)

    # Figure format
    decision_colors = ['#ffe6ccff', '#ffccccff']
    axes_labels = None if matrix_name is None else cfg['decision_matrices'][f'{matrix_name}_labels']

    # Start the figure
    with rc_context(cfg_fig):

        # Define colors for values
        cmap = colors.ListedColormap(['white', decision_colors[0], decision_colors[1]])
        bounds = [-1.5, -0.5, 0.5, 1.5]
        norm = colors.BoundaryNorm(bounds, cmap.N)

        # Adjusting the plot by adding gridlines to the subplots
        fig = plt.figure(figsize=(10, 8))
        gs = gridspec.GridSpec(n_categories, 2, width_ratios=[n_categories, 1], wspace=0.05)

        # Plot the decision matrix on the left (column 0 of the GridSpec)
        ax_matrix = fig.add_subplot(gs[:, 0])
        ax_matrix.matshow(matrix_arr, cmap=cmap, norm=norm)

        # Customize matrix ticks and labels
        ax_matrix.set_xticks(range(n_categories))
        ax_matrix.set_yticks(range(n_categories))

        ax_matrix.set_xticklabels(categories, rotation=45)
        ax_matrix.set_yticklabels(categories)

        # Add black gridlines to separate each square
        ax_matrix.set_xticks(np.arange(-.5, n_categories, 1), minor=True)
        ax_matrix.set_yticks(np.arange(-.5, n_categories, 1), minor=True)
        ax_matrix.grid(which="minor", color="black", linestyle='-', linewidth=2)
        ax_matrix.tick_params(which="minor", size=0)
        ax_matrix.tick_params(axis='x', bottom=False, labelbottom=False)

        if axes_labels is not None:
            ax_matrix.set_ylabel(axes_labels[0], color=decision_colors[0], path_effects=[
                                path_effects.Stroke(linewidth=0.5, foreground='black'), path_effects.Normal()])

            ax_matrix.set_title(axes_labels[1], color=decision_colors[1], path_effects=[
                                path_effects.Stroke(linewidth=0.5, foreground='black'), path_effects.Normal()])

            # ax_matrix.set_xlabel(axes_labels[1], color=decision_colors[1], path_effects=[
            #                     path_effects.Stroke(linewidth=0.5, foreground='black'), path_effects.Normal()])

        # Add individual plots on the right side (column 1 of the GridSpec) for each category
        if show_categories:
            for i, category in enumerate(categories):
                ax_plot = fig.add_subplot(gs[i, 1])

                # Example placeholder data for each category plot
                x = np.linspace(0, 10, 100)
                y = np.sin(x + i)  # Example sine wave that varies by row
                ax_plot.step(x, y, color=cfg['colors'][category])

                # Add gridlines to the subplots
                ax_plot.grid(True, which='both', linestyle='--', linewidth=0.5)

                # Hide y-axis ticks for these small plots for a cleaner look
                ax_plot.yaxis.set_ticks([])
                ax_plot.xaxis.set_ticks([])

        # Output the result
        if output_address is None:
            plt.show()
        else:
            fig.savefig(output_address, bbox_inches='tight')

    return

def scatter_plot(fig, ax, x_arr, y_arr, labels_arr, feature_list, color_dict, alpha=0.5, idx_target=None,
                 detection_range=None, ratio_color=None):

    # Input user diagnostic coloring
    if ratio_color is not None:
        idcs_data = np.where(np.isin(labels_arr, feature_list))[0]
        color_arr = ratio_color[idcs_data] # ratio_color[idcs_data]
        scatter = ax.scatter(x_arr[idcs_data], y_arr[idcs_data], c=color_arr, cmap='viridis', alpha=alpha, edgecolor='none')
                             # norm=colors.LogNorm(vmin=1, vmax=np.nanmax(color_arr)))
        cbar = fig.colorbar(scatter, ax=ax)
        cbar.set_label('Max - Min')

    # Category coloring
    else:
        for i, feature in enumerate(feature_list):
            idcs_class = labels_arr == feature
            x_feature = x_arr[idcs_class]
            y_feature = y_arr[idcs_class]
            label = f'{feature} ({y_feature.size})'
            color_points = color_dict[feature]
            ax.scatter(x_feature, y_feature, label=label, c=color_points, alpha=alpha, edgecolor='none')

    # Failed entries
    if idx_target is not None:
        ax.scatter(x_arr[idx_target], y_arr[idx_target], marker='x', label='selection', color='black')

    if detection_range is not None:
        ax.plot(detection_range, detection_function(detection_range))

    return

def parse_fig_cfg(fig_cfg=None, ax_diag=None, ax_line=None, dtype=None):

    # Input configuration updates default
    theme.set_style('dark')

    fig_cfg = fig_cfg if fig_cfg is not None else {'axes.labelsize': 10, 'axes.titlesize': 10,
                                                'figure.figsize': (12, 6), 'hatch.linewidth': 0.3, 'legend.fontsize': 8,
                                                   }
    fig_cfg = theme.fig_defaults(fig_cfg)

    if dtype == 'classifier':
        ax_diag = {} if ax_diag is None else ax_diag
        ax_diag = {'xlabel': r'$\frac{\sigma_{gas}}{\Delta\lambda_{inst}} = \sigma_{pixels}$ (Gaussian sigma in pixels)',
                   'ylabel': r'$\frac{A_{gas}}{\sigma_{noise}}$ (Signal-to-noise)',
                   **ax_diag}

        ax_line = {} if ax_line is None else ax_line
        ax_line = {'xlabel': 'Feature Number', 'ylabel': 'value', **ax_line}

    if dtype == 'doublet':
        ax_diag = {} if ax_diag is None else ax_diag
        ax_diag = {'xlabel': r'$\frac{\sigma_{gas}}{\Delta\lambda_{inst}} = \sigma_{pixels}$ (Gaussian sigma in pixels)',
                   'ylabel': r'$S_{pixels}$ (pixels)',
                   **ax_diag}

        ax_line = {} if ax_line is None else ax_line
        ax_line = {'xlabel': 'Feature Number', 'ylabel': 'value', **ax_line}

    return {'fig': fig_cfg, 'ax1': ax_diag, 'ax2': ax_line}


def maximize_center_fig(maximize_check=False, center_check=False):

    if maximize_check:

        # Windows maximize
        mng = plt.get_current_fig_manager()

        try:
            mng.window.showMaximized()
        except:
            try:
                mng.resize(*mng.window.maxsize())
            except:
                _logger.debug(f'Unable to maximize the window')

    if center_check:

        try:
            mngr = plt.get_current_fig_manager()
            mngr.window.setGeometry(1100, 300, mngr.canvas.width(), mngr.canvas.height())
        except:
            _logger.debug(f'Unable to center plot window')

    return


def save_close_fig_swicth(file_path=None, bbox_inches=None, fig_obj=None, maximise=False, plot_check=True):

    # By default, plot on screen unless an output address is provided
    if plot_check:
        output_fig = None

        if file_path is None:

            # Tight layout
            if bbox_inches is not None:
                plt.tight_layout()

            # Window positioning and size
            maximize_center_fig(maximise)

            # Display
            plt.show()

        else:
            plt.savefig(file_path, bbox_inches=bbox_inches)

            # Close the figure in the case of printing
            if fig_obj is not None:
                plt.close(fig_obj)

    # Return the figure for output plotting
    else:
        output_fig = fig_obj

    return output_fig


def ax_wording(ax, ax_cfg=None, legend_cfg=None, yscale=None):

    ax.update(ax_cfg)

    if legend_cfg is not None:
        ax.legend(**legend_cfg)

    if yscale is not None:
        ax.set_yscale(yscale)

    return


def plot_comps_detect(x_sect, y_norm, idx, counts, model, out_type, seg_pred, old_pred):

    print(f'Idx "{idx}"; counts: {counts}; Output: {model.number_feature_dict[out_type]} ({out_type})')

    colors_old = [cfg['colors'][model.number_feature_dict[val]] for val in old_pred]
    colors_new = [cfg['colors'][model.number_feature_dict[val]] for val in seg_pred]
    color_detection = cfg['colors'][model.number_feature_dict[out_type]]

    fig, ax = plt.subplots()
    ax.step(x_sect, y_norm, where='mid', color=color_detection, label='Out detection')
    ax.scatter(x_sect, np.zeros(x_sect.size), color=colors_old, label='Old prediction')
    ax.scatter(x_sect, np.ones(x_sect.size), color=colors_new, label='New prediction')
    ax.set_xlabel(r'Wavelength $(\AA)$')

    ax_secondary = ax.twinx()  # Creates a twin y-axis on the right
    ax_secondary.set_ylim(ax.get_ylim())  # Match the primary y-axis limits
    ax_secondary.set_yticks([0, 0.5, 1])  # Custom tick positions
    ax_secondary.set_yticklabels(['Previous\nClassification', 'Present\nClassification', 'Output\nClassification'])

    plt.tight_layout()
    plt.show()

    return

def plot_steps_backUP(spec, y_norm, idx, counts, model_mgr, out_type, seg_pred, old_pred):

    print(idx)
    x_arr = spec.wave_rest.data[spec.wave_rest.mask]
    x_sect = x_arr[idx:idx+y_norm.shape[0]]
    print(f'Idx "{idx}"; counts: {counts}; Output: {model_mgr.medium.number_feature_dict[out_type]} ({out_type})')

    colors_old = [cfg['colors'][model_mgr.medium.number_feature_dict[val]] for val in old_pred]
    colors_new = [cfg['colors'][model_mgr.medium.number_feature_dict[val]] for val in seg_pred]
    color_detection = cfg['colors'][model_mgr.medium.number_feature_dict[out_type]]

    fig, ax = plt.subplots()
    color_detection = cfg['colors'][model_mgr.medium.number_feature_dict[out_type]]
    ax.step(x_sect, y_norm[:,0], where='mid', color=color_detection, label='Out detection')
    ax.scatter(x_sect, np.zeros(x_sect.size), color=colors_old, label='Old prediction')
    ax.scatter(x_sect, np.ones(x_sect.size), color=colors_new, label='New prediction')
    ax.set_xlabel(r'Wavelength $(\AA)$')

    ax_secondary = ax.twinx()  # Creates a twin y-axis on the right
    ax_secondary.set_ylim(ax.get_ylim())  # Match the primary y-axis limits
    ax_secondary.set_yticks([0, 0.5, 1])  # Custom tick positions
    ax_secondary.set_yticklabels(['Previous\nClassification', 'Present\nClassification', 'Output\nClassification'])

    plt.tight_layout()
    plt.show()

    return

def plot_comps_detect_new(spec, theme, idx, y_norm, counts, model_mgr, out_type, old_pred, seg_pred, **kwargs):

    # Clear previous figure
    spec.plot.reset_figure()

    # Prepare the data
    x_arr = spec.wave_rest.data[spec.wave_rest.mask]
    x_sect = x_arr[idx:idx+y_norm.shape[0]]
    print(f'Idx "{idx}"; counts: {counts}; Output: {model_mgr.medium.number_feature_dict[out_type]} ({out_type})')
    colors_old = [cfg['colors'][model_mgr.medium.number_feature_dict[val]] for val in old_pred]
    colors_new = [cfg['colors'][model_mgr.medium.number_feature_dict[val]] for val in seg_pred]
    color_detection = cfg['colors'][model_mgr.medium.number_feature_dict[out_type]]

    # Display check for input figures
    display_check = False if kwargs.get('in_fig') is not None else True

    # Adjust the default theme
    plt_cfg = theme.fig_defaults(kwargs.get('in_fig'))
    ax_labels_cfg = theme.ax_defaults(kwargs.get('ax_cfg'), spec)

    # Create and fill the figure
    with (rc_context(plt_cfg)):

        # Establish figure
        spec.fig = plt.figure() if kwargs.get('in_fig') is None else kwargs.get('in_fig')

        # Establish the axes
        spec.ax_list = spec.fig.add_subplot()

        spec.ax_list.step(x_sect, y_norm[:, 0], where='mid', color=color_detection, label='Out detection')
        spec.ax_list.scatter(x_sect, np.zeros(x_sect.size), color=colors_old, label='Old prediction')
        spec.ax_list.scatter(x_sect, np.ones(x_sect.size), color=colors_new, label='New prediction')

        # Plot the spectrum
        label = kwargs.get('label')
        spec.ax_list.step(spec.wave, spec.flux, label=label, where='mid', color=theme.colors['fg'],
                          linewidth=theme.plt['spectrum_width'])

        ax_secondary = spec.ax_list.twinx()  # Creates a twin y-axis on the right
        ax_secondary.set_ylim(spec.ax_list.get_ylim())  # Match the primary y-axis limits
        ax_secondary.set_yticks([0, 0.5, 1])  # Custom tick positions
        ax_secondary.set_yticklabels(['Previous\nClassification', 'Present\nClassification', 'Output\nClassification'])

        # Switch y_axis to logarithmic scale if requested
        if kwargs.get('log_scale'):
            spec.ax_list.set_yscale('log')

        # Show the wording:
        spec.ax_list.legend()
        spec.ax_list.set(**ax_labels_cfg)

        # By default, plot on screen unless an output address is provided
        maximize = False if kwargs.get('output_address') is None else kwargs.get('output_address')
        save_close_fig_swicth(kwargs.get('output_address'), 'tight', spec.fig, maximize, display_check)

    return

class CheckSample:

    def __init__(self, in_data_arr, in_pred_arr, idx_features, fig_cfg=None, ax_diag=None, ax_line=None, base=10000,
                 sample_size=None, categories=None, y_axis_scale='log', color_array=None):

        # Stratify the selection aiming for same number of points
        data_arr, pred_arr, color_array = stratify_sample(in_data_arr, in_pred_arr, sample_size, categories, randomize=True, color_array=color_array)

        self.y_base = base
        self.x_coords = data_arr[:, 1]
        self.y_coords = data_arr[:, 0]

        self.id_arr = pred_arr
        self.classes = np.sort(np.unique(self.id_arr))

        self.data_df = data_arr[:, idx_features:]
        self.wave_range = np.arange(self.data_df.shape[1])

        self.color_array = color_array
        self.y_scale = 'log' if y_axis_scale == 'log' else 'linear'
        self.y_coords_log = np.log10(self.y_coords) / np.log10(self.y_base)

        self.idx_current = None
        self.color_dict = cfg['colors']

        self.fig_format = parse_fig_cfg(fig_cfg, ax_diag, ax_line, dtype='classifier')
        self._fig, self._ax1, self._ax2 = None, None, None

        self.detection_range = np.linspace(data_arr[:,1].min(), data_arr[:,1].max(), 50) if self.y_scale == 'log' else None

        return

    def show(self):

        # Generate the figure
        with rc_context(self.fig_format['fig']):

            # Create the figure
            self._fig, (self._ax1, self._ax2) = plt.subplots(1, 2)

            # Diagnostic plot
            scatter_plot(self._fig, self._ax1, self.x_coords, self.y_coords, self.id_arr, self.classes, self.color_dict,
                         idx_target=self.idx_current, detection_range=self.detection_range, ratio_color=self.color_array)

            ax_wording(self._ax1, self.fig_format['ax1'], legend_cfg={'loc': 'lower center', 'ncol':2, 'framealpha':0.95},
                       yscale=self.y_scale)

            # Line plot
            self.index_target()
            self.line_plot()
            ax_wording(self._ax2, self.fig_format['ax2'])

            # Interactive widget
            self._fig.canvas.mpl_connect('button_press_event', self._on_click)

            # Display the plot
            plt.tight_layout()
            plt.show()

        return

    def _on_click(self, event):

        if event.inaxes == self._ax1 and event.button == 1:

            if self.y_scale == 'log':
                user_point = (event.xdata, np.log10(event.ydata) / np.log10(self.y_base))
            else:
                user_point = (event.xdata, event.ydata)


            # Get index point
            self.index_target(user_point)

            # Replot the figures
            self._ax1.clear()
            scatter_plot(self._fig, self._ax1, self.x_coords, self.y_coords, self.id_arr, self.classes, self.color_dict,
                         idx_target=self.idx_current, detection_range=self.detection_range, ratio_color=self.color_array)
            ax_wording(self._ax1, self.fig_format['ax1'], legend_cfg={'loc': 'lower center', 'ncol':2, 'framealpha':0.95},
                       yscale=self.y_scale)

            self._ax2.clear()
            # self._fig.clear()

            self.line_plot()
            plt.tight_layout()
            self._fig.canvas.draw()

        return

    def index_target(self, mouse_coords=None):

        # If no selection use first point
        if mouse_coords is None:
            self.idx_current = 0
            print(f'Reseting location')

        else:
            distances = np.sqrt((self.x_coords - mouse_coords[0]) ** 2 + (self.y_coords_log - mouse_coords[1]) ** 2)
            self.idx_current = np.argmin(distances)
            print('Click on:', mouse_coords)#, self.ratio_color[self.idx_current])

        return

    def line_plot(self):

        feature = self.id_arr[self.idx_current]
        self._ax2.step(self.wave_range, self.data_df[self.idx_current, :], label=feature,
                      color=self.color_dict[feature], where='mid')

        return