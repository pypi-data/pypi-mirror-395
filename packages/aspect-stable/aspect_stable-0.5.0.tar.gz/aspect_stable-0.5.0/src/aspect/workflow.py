import numpy as np
from aspect.io import read_trained_model, DEFAULT_MODEL_ADDRESS, cfg, Aspect_Error
from aspect.tools import monte_carlo_expansion, white_noise_scale, scale_min_max
from aspect.plots import plot_comps_detect
# from matplotlib import pyplot as plt
from pathlib import Path

CHOICE_DM = np.array(cfg['decision_matrices']['choice'])
TIME_DM = np.array(cfg['decision_matrices']['time'])

def flux_to_image(flux_array, approximation, model_2D):

    if model_2D is not None:

        img_flux_array = np.tile(flux_array[:, None, :, :], (1, approximation.size, 1, 1))
        img_flux_array = img_flux_array > approximation[::-1, None, None]
        img_flux_array = img_flux_array.astype(int)
        img_flux_array = img_flux_array.reshape((flux_array.shape[0], 1, -1, flux_array.shape[-1]))
        img_flux_array = img_flux_array.squeeze()

        # Original
        # flux_array_0 = flux_array[:, :, 0]
        # Old_img = np.tile(flux_array_0[:, None, :], (1, approximation.size, 1))
        # Old_img = Old_img > approximation[::-1, None]
        # Old_img = Old_img.astype(int)
        # Old_img = Old_img.reshape((flux_array_0.shape[0], 1, -1))
        # Old_img = Old_img.squeeze()

    else:
      img_flux_array = None

    return img_flux_array


def unpack_spec_flux(spectrum, rest_wl_lim):

    # Extract the mask if masked array
    pixel_mask = ~spectrum.flux.mask

    # Limit to region if requested # TODO warning negative entries
    if rest_wl_lim is not None:
        wave_rest = spectrum.wave_rest.data
        pixel_mask = pixel_mask | ~((wave_rest > rest_wl_lim[0]) & (wave_rest < rest_wl_lim[1]))

    # Extract flux and error arrays and invert the mask for location of the valid data indeces
    wave_arr = spectrum.wave.data[pixel_mask]
    flux_arr = spectrum.flux.data[pixel_mask]
    err_arr = spectrum.err_flux.data[pixel_mask]

    return wave_arr, flux_arr, err_arr, pixel_mask


def enbox_spectrum(input_flux, box_size, range_box, n_scale_features):

    # Number of scale and pixel features
    n_columns = box_size + n_scale_features

    # Number of rows in equal ter
    n_rows = input_flux.size - box_size

    # Container for the data
    box_containter = np.empty((n_rows, n_columns))

    # Assign values
    box_containter[:, -box_size:] = input_flux[np.arange(n_rows)[:, None] + range_box]

    return box_containter


def detection_spectrum_prechecks(y_arr, box_size, idcs_data):

    # Box bigger than spectrum or all entries are masked
    if (y_arr.size < box_size) or (idcs_data.sum() < box_size):
        return False

    else:
        return True


def detection_evaluation(counts_categories, idcs_categories):

    n_detections = idcs_categories.sum()

    match n_detections:

        # Undefined
        case 0:
            return 0, 0

        # One detection
        case 1:
            return np.argmax(idcs_categories), counts_categories[idcs_categories][0]

        # Two detections
        case 2:
            category_candidates = np.flatnonzero(idcs_categories)
            idx_output = CHOICE_DM[category_candidates[0], category_candidates[1]]
            output_type, output_count = category_candidates[idx_output], counts_categories[idcs_categories][idx_output]
            return output_type, output_count

        # Three detections
        case _:
            raise Aspect_Error(f'Number of detections: "{n_detections}" is not recognized')


def detection_revision(seg_pred, box_size, new_type, new_confidence):

    new_pred, new_conf = np.full(box_size, new_type), np.full(box_size, new_confidence)
    idcs_pred = TIME_DM[seg_pred, new_pred]

    return idcs_pred, new_pred, new_conf




class DetectionModel:

    def __init__(self, model_address=None, n_jobs=None, verbose=0):

        # Read the model files
        self.predictor, self.cfg = read_trained_model(model_address)

        # Specify cores (default 4) and verbpose level (default none)
        self.predictor.n_jobs = 4 if n_jobs is None else n_jobs  # Use 4 cores
        self.predictor.verbose = verbose

        # Array with the boxes size
        self.scale = self.cfg['properties']['scale']
        self.b_pixels = self.cfg['properties']['box_size']
        self.pixels_range = np.arange(self.b_pixels)

        # Components names and number variables
        self.feature_number_dict = cfg['shape_number']
        self.number_feature_dict = {v: k for k, v in self.feature_number_dict.items()}
        self.n_categories = len(self.feature_number_dict)

        return


class ModelManager:

    def __init__(self, model_address=None,):

        # Global parameters
        self.n_mc = 100
        self.detection_min = 40
        self.white_noise_maximum = 50
        self.n_scale_features = 1

        # Default values
        model_address = DEFAULT_MODEL_ADDRESS if model_address is None else model_address

        # Load the model
        self.medium = DetectionModel(model_address)
        self.large = None

        # Largest reference model parameters
        self.b_pixels_max = self.medium.b_pixels
        self.b_pixels_max_range = self.medium.pixels_range

        return

    def reload_model(self, model_address=None, n_jobs=None):

        # Call the constructor again
        self.__init__(model_address, n_jobs)

        return

    def run_models(self, data_arr):

        # Run the prediction
        scale_min_max(data_arr, self.medium.b_pixels, axis=1)

        y_pred = data_arr.transpose(0, 2, 1).reshape(-1, self.medium.b_pixels + 1)
        y_pred = self.medium.predictor.predict(y_pred).reshape(-1, 100)

        return y_pred

    def review_prediction(self, x_arr, y_arr, pred_matrix, model, exclude_continuum, plot_steps=True):

        count_categories = np.apply_along_axis(np.bincount, axis=1, arr=pred_matrix, minlength=self.medium.n_categories)

        # Exclude white-noise regions from review:
        if exclude_continuum:
            idcs_detection = np.flatnonzero(count_categories[:, 1] < self.white_noise_maximum)
        else:
            idcs_detection = np.arange(pred_matrix.shape[0])

        # Containers for total
        pred_arr = np.zeros(pred_matrix.shape[0] + model.b_pixels)
        conf_arr = np.zeros(pred_matrix.shape[0] + model.b_pixels)

        self.seg_pred = np.zeros(self.medium.b_pixels, dtype=np.int64)
        self.seg_conf = np.zeros(self.medium.b_pixels, dtype=np.int64)

        for idx in idcs_detection:

            # Get segment arrays
            self.seg_pred[:] = pred_arr[idx:idx + self.medium.b_pixels]
            self.seg_conf[:] = conf_arr[idx:idx + self.medium.b_pixels]

            # Count
            counts = count_categories[idx, :]
            idcs_categories = counts > self.detection_min

            # Choice selection
            out_type, out_confidence = detection_evaluation(counts, idcs_categories)

            # Time detection
            idcs_pred, new_pred, new_conf = detection_revision(self.seg_pred, self.medium.b_pixels, out_type,
                                                               out_confidence)

            # Only pass if more than half
            # half_check = idcs_pred[6:].sum() > 5
            half_check = idcs_pred[5:].sum() > 6
            if half_check:
                idcs_pred = np.flatnonzero(idcs_pred)
                self.seg_pred[idcs_pred] = new_pred[idcs_pred]
                self.seg_conf[idcs_pred] = new_conf[idcs_pred]
            else:
                self.seg_pred[:] = pred_arr[idx:idx + self.medium.b_pixels]
                self.seg_conf[:] = conf_arr[idx:idx + self.medium.b_pixels]

            if plot_steps:
                plot_comps_detect(x_arr[idx:idx + self.medium.b_pixels],
                                  y_arr[idx, -self.medium.b_pixels:, 0],
                                  idx, counts, self.medium,
                                  new_pred[0],
                                  pred_arr[idx:idx + self.medium.b_pixels],
                                  self.seg_pred[:])

            # Assign new categories and confidence
            pred_arr[idx:idx + self.medium.b_pixels] = self.seg_pred[:]
            conf_arr[idx:idx + self.medium.b_pixels] = self.seg_conf[:]

        return pred_arr, conf_arr


# Create object with default model
model_mgr = ModelManager()




class ComponentsDetector:

    def __init__(self, spectrum, model_address=None):

        self._spec = spectrum

        # Data containers
        self.seg_pred = None
        self.seg_conf = None

        self.pred_arr = None
        self.conf_arr = None

        # Read the detection model
        if model_address is None:
            self.model_mgr = model_mgr

        return

    def components(self, exclude_continuum=True, plot_steps=False, rest_wl_lim=None, theme=None):

        # Remove masks from flux and uncertainty
        x_arr, y_arr, err_arr, idcs_data = unpack_spec_flux(self._spec, rest_wl_lim)

        # Check the validity of the spectrum
        if detection_spectrum_prechecks(y_arr, self.model_mgr.b_pixels_max, idcs_data):

            # Reshape the data to the box size and add Monte-carlo uncertainty axis
            y_medium = self.cube_data(y_arr, err_arr, self.model_mgr.medium, self.model_mgr.n_scale_features)

            # Scale and run the prediction models
            pred_medium = self.run(y_medium, self.model_mgr.medium)

            # Review the predictions and assign confidence values
            self.pred_arr = np.zeros(self._spec.flux.size, dtype=np.int64)
            self.conf_arr = np.zeros(self._spec.flux.size, dtype=np.int64)
            self.pred_arr[idcs_data], self.conf_arr[idcs_data] = self.model_mgr.review_prediction(x_arr,
                                                                                                  y_medium,
                                                                                                  pred_medium,
                                                                                                  self.model_mgr.medium,
                                                                                                  exclude_continuum,
                                                                                                  plot_steps)

        return

    def cube_data(self, data_arr, err_arr, model, n_scale_features):

        # Reshape spectrum to the max box size
        data_enbox = enbox_spectrum(data_arr, model.b_pixels, model.pixels_range, n_scale_features)
        err_enbox = enbox_spectrum(err_arr, model.b_pixels, model.pixels_range, n_scale_features)

        # MC expansion
        data_mc = monte_carlo_expansion(data_enbox, err_enbox, self.model_mgr.n_mc, model.b_pixels)

        return data_mc

    def run(self, data_arr, model):

        # Scale the data
        scale_min_max(data_arr, model.b_pixels, axis=1, scale_parameter=model.scale)

        # Run the prediction
        y_pred = data_arr.transpose(0, 2, 1).reshape(-1, model.b_pixels + 1)

        return model.predictor.predict(y_pred).reshape(-1, 100)

    def transform_category(self, input_category, segment_flux):

        match input_category:

            # White noise scale
            case 1:
                return white_noise_scale(segment_flux)

            case _:
                return input_category

    def plot_steps(self, y_norm, idx, counts, idcs_categories, out_type, out_confidence, old_pred, old_conf,
                   idcs_pred, new_pred, new_conf):

        x_arr = self._spec.wave_rest.data[~self._spec.wave_rest.mask]
        x_sect = x_arr[idx:idx+y_norm.shape[0]]
        print(f'Idx "{idx}"; counts: {counts}; Output: {model_mgr.number_feature_dict[out_type]} ({out_type})')

        colors_old = [cfg['colors'][model_mgr.number_feature_dict[val]] for val in old_pred]
        colors_new = [cfg['colors'][model_mgr.number_feature_dict[val]] for val in self.seg_pred]

        fig, ax = plt.subplots()
        color_detection = cfg['colors'][model_mgr.number_feature_dict[out_type]]
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