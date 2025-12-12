import importlib
import numpy as np
import joblib
import toml
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score
from time import time
from pathlib import Path
from .io import cfg as aspect_cfg


def get_training_test_sets(x_arr, y_arr, test_fraction, n_pixel_features, n_scale_features, random_state=None):

    # Split into training and testing:
    print(f'\nSplitting sample with categories:')
    print(np.unique(y_arr))
    sss = StratifiedShuffleSplit(n_splits=1, train_size=int(y_arr.size * (1 - test_fraction)),
                                 test_size=int(y_arr.size * test_fraction), random_state=random_state)

    for train_index, test_index in sss.split(x_arr, y_arr):
        X_train, X_test = x_arr[train_index, -n_pixel_features-n_scale_features:], x_arr[test_index, -n_pixel_features-n_scale_features:]
        y_train, y_test = y_arr[train_index], y_arr[test_index]

    # Convert strings to integers
    y_train = np.vectorize(aspect_cfg['shape_number'].get)(y_train)
    y_test = np.vectorize(aspect_cfg['shape_number'].get)(y_test)

    return X_train, y_train, X_test, y_test


def components_trainer(model_label, x_arr, y_arr, fit_cfg, list_labels, output_folder=None, test_fraction=0.1,
                       random_state=None):

    # Preparing the estimator:
    print(f'\nLoading estimator: {fit_cfg["estimator"]["class"]}')
    estimator = getattr(importlib.import_module(fit_cfg['estimator']["module"]), fit_cfg['estimator']["class"])
    estimator_params = fit_cfg.get('estimator_params', {})

    # Split into training and testing:
    print(f'\nSplitting sample with categories:')
    X_train, y_train, X_test, y_test = get_training_test_sets(x_arr, y_arr, test_fraction,
                                                              n_pixel_features=fit_cfg['box_size'], n_scale_features=1,
                                                              random_state=random_state)

    # Run the training
    print(f'\nTraining: {y_train.size/len(fit_cfg["categories"]):.0f} * {len(fit_cfg["categories"])} = {y_train.size}  points ({model_label})')
    print(f'- Settings: {fit_cfg["estimator_params"]}\n')
    start_time = time()
    ml_function = estimator(**estimator_params)
    ml_function.fit(X_train, y_train)
    end_time = np.round((time()-start_time)/60, 2)
    print(f'- completed ({end_time} minutes)')

    # Save the trained model and configuration
    output_folder = Path(output_folder)/'results'
    output_folder.mkdir(parents=True, exist_ok=True)

    model_address = output_folder/f'{model_label}.joblib'
    joblib.dump(ml_function, model_address)

    # Run initial diagnostics
    print(f'\nReloading model from: {model_address}')
    start_time = time()
    ml_function = joblib.load(model_address)
    fit_time = np.round((time()-start_time), 3)
    print(f'- completed ({fit_time} seconds)')

    print(f'\nRuning prediction on test set ({y_test.size} points)')
    start_time = time()
    y_pred = ml_function.predict(X_test)
    print(f'- completed ({(time()-start_time):0.1f} seconds)')

    # Testing confussion matrix
    print(f'\nConfusion matrix in test set ({y_test.size} points)')
    start_time = time()
    conf_matrix_test = confusion_matrix(y_test, y_pred, normalize="all")
    print(f'- completed ({(time()-start_time):0.1f} seconds)')

    # Precision, recall and f1:
    print(f'\nF1, Precision and recall diagnostics ({y_test.size} points)')
    start_time = time()
    pres = precision_score(y_test, y_pred, average='macro')
    recall = recall_score(y_test, y_pred, average='macro')
    f1 = f1_score(y_test, y_pred, average='macro')
    print(f'- completed ({(time()-start_time):0.1f} seconds)')

    print(f'\nModel outputs')
    print(f'- F1: \n {f1}')
    print(f'- Precision: \n {pres}')
    print(f'- Recall: \n {recall}')
    print(f'- Testing confusion matrix: \n {conf_matrix_test}')
    print(f'- Fitting time (seconds): \n {float(fit_time)}')

    # Save results into a TOML file
    toml_path = output_folder/f'{model_label}.toml'
    output_dict = {'resuts': {'f1':f1, 'precision':pres, 'Recall':recall, 'confusion_matrix':conf_matrix_test,
                              'fit_time': fit_time}, 'properties': fit_cfg,}
    with open(toml_path, 'w') as f:
        toml.dump(output_dict, f)

    return
