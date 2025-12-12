import logging
import numpy as np
from .io import Aspect_Error
from lime.fitting.lines import gaussian_model

# Log variable
_logger = logging.getLogger('aspect')
np.random.seed(42)


def monte_carlo_expansion(flux_array, err_array, n_mc, n_pixels):

    # Get the noise parameter from the observations uncertainty on a constant scalar
    noise_scale = err_array if np.isscalar(err_array) else err_array[:, -n_pixels:][..., None]

    # Generate error matrix only for the flux features
    noise_array = np.empty((flux_array.shape[0], flux_array.shape[1], n_mc))
    noise_array[:, -n_pixels:] = np.random.normal(0, noise_scale, size=(flux_array.shape[0], n_pixels, n_mc))

    # Add noise to observation for (intervals, max_box_size + scale_features, monte_carlo_steps array)
    mc_flux = flux_array[:, :, np.newaxis] + noise_array

    return mc_flux


def scale_min_max_orig(data, axis=None):

    data_min_array = data.min(axis=axis, keepdims=True)
    data_max_array = data.max(axis=axis, keepdims=True)
    data_norm = (data - data_min_array) / (data_max_array - data_min_array)

    return data_norm


def scale_min_max(data, box_size, axis=None, scale_parameter='min-max'):

    # Norm the scale features
    data_min_array = data[:, -box_size:].min(axis=axis, keepdims=True)
    data_max_array = data[:, -box_size:].max(axis=axis, keepdims=True)
    data[:, -box_size:] = (data[:, -box_size:] - data_min_array) / (data_max_array - data_min_array)

    # Save the scaling parameters
    if scale_parameter == 'min-max':
        data[:, -box_size - 1] = ((data_max_array - data_min_array)/10000)[:,0]

    if scale_parameter == 'min-max-log':
        data[:, -box_size - 1] = (np.log10(data_max_array - data_min_array)/4)[:,0]

    # # Norm the scale features
    # data_min_array = data[:, -box_size:].min(axis=axis, keepdims=True)
    # data_max_array = data[:, -box_size:].max(axis=axis, keepdims=True)
    # data[:, -box_size:] = (data[:, -box_size:] - data_min_array) / (data_max_array - data_min_array)
    #
    # # Save the scaling parameters
    # data[:, -box_size - 1] = ((data_max_array - data_min_array)/10000)[:,0]
    # data[:, -box_size - 1] = ((data_max_array - data_min_array)/10000)[:,0]

    return

def scale_log(data, log_base, axis=None):

    data_min_array = data.min(axis=axis, keepdims=True)

    y_cont = data - data_min_array + 1
    data_norm = np.emath.logn(log_base, y_cont)

    return data_norm


def scale_log_min_max(data, log_base, axis=None):

    data_min_array = data.min(axis=axis, keepdims=True)
    data_cont = data - data_min_array + 1
    log_data = np.emath.logn(log_base, data_cont)
    log_min_array, log_max_array = log_data.min(axis=axis, keepdims=True), log_data.max(axis=axis, keepdims=True)
    data_norm = (log_data - log_min_array) / (log_max_array - log_min_array)

    return data_norm


def feature_scaling(data, transformation, log_base=None, axis=1):

    match transformation:
        case 'min-max':
            return scale_min_max(data, axis=axis)
        case 'log':
            return scale_log(data, log_base=log_base, axis=axis)
        case 'log-min-max':
            return scale_log_min_max(data, log_base=log_base, axis=axis)
        case _:
            raise Aspect_Error(f'Input scaling: "{transformation}" is not recognized')


def white_noise_scale(flux_arr):

    min, max = flux_arr.min(), flux_arr.max()

    diff = max - min if max != 0 else np.abs(max-min)

                # 1 White noise, 2 continuum
    output_type = 1 if diff > 10 else 2

    return output_type


def detection_function(x_ratio):
    return 0.5 * np.power(x_ratio, 2) - 0.5 * x_ratio + 5


def broad_component_function(intensity_ratio):
    return np.sqrt(1 + np.log(intensity_ratio)/np.log(2))


def doublet_model(wave_arr, noise_arr, cont_arr, amp, mu_line, sigma, doublet_em_sep_min, doublet_em_sep_max,
                  doublet_int_min, doublet_int_max, lower_limit, upper_limit):

    # Compute the doublet
    sep = np.random.uniform(doublet_em_sep_min, doublet_em_sep_max)
    int_diff = np.random.uniform(doublet_int_min, doublet_int_max)
    amp1, amp2 = amp, amp * int_diff
    mu1, mu2 = mu_line - sep, mu_line + sep
    sigma1, sigma2 = sigma, sigma * 1

    # Emission doublet
    if amp > 0:
        amp2 = np.clip(lower_limit, np.abs(amp2), upper_limit)

    # Absorption doublet
    else:
        amp2 = np.clip(-upper_limit, amp2, -lower_limit)

    # Generate the profiles
    gauss1 = gaussian_model(wave_arr, amp1, mu1, sigma1)
    gauss2 = gaussian_model(wave_arr, amp2, mu2, sigma2)
    flux_arr = gauss1 + gauss2 + noise_arr + cont_arr

    return flux_arr

def cosmic_ray_function(x_ratio, res_ratio_check=True):

    # Resolution ration
    if res_ratio_check:
        output = np.exp(0.5 * np.power(x_ratio, -2))

    # Intensity ratio
    else:
        output = 1/np.sqrt(2 * np.log(x_ratio))

    return output


def stratify_sample(x_arr, y_arr, n_samples=None, categories=None, randomize=True, color_array=None):

    # Inspect input sample
    unique_categories, counts = np.unique(y_arr, return_counts=True)
    min_count = min(counts)

    # Use all categories and the minimum number of counts if not provided
    n_samples = n_samples if n_samples is not None else min_count
    categories = categories if categories is not None else unique_categories

    # Check input sample size is below category
    if n_samples > min_count:
        _logger.warning(f'The input sample minimun size category ({unique_categories[counts==min_count]} = {min_count})'
                        f' is less than the requested input size ({n_samples}). The minimum count will be used instead.')
        n_samples = min_count

    # Empty mask for the target categories
    selection_mask = np.zeros(y_arr.size, dtype=bool)

    # Mark indices for each category
    print(f'\nInput sample has {y_arr.shape[0]} entries:')
    for j, category in enumerate(categories):
        print(f'- {category}: {counts[j]}')
        category_indices = np.where(y_arr == category)[0]
        sampled_indices = np.random.choice(category_indices, n_samples, replace=False)
        selection_mask[sampled_indices] = True
    print(f'Cropping to {n_samples} entries per category')

    selection_mask = np.nonzero(selection_mask)[0]

    if randomize:
        np.random.shuffle(selection_mask)

    ratio_indexed = None if color_array is None else color_array[selection_mask]

    return x_arr[selection_mask, :], y_arr[selection_mask], ratio_indexed

