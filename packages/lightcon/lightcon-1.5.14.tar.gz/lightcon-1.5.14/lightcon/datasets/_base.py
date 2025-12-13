"""
Base data loading code for all datasets
"""

import csv
import gzip
import os
from ..utils._fixes import _open_text, _open_binary
from typing import Tuple, List
from typing_extensions import Literal
import pickle
import json

import numpy as np

DATA_MODULE = "lightcon.datasets.data"

def load_json_data(
        data_file_name,
        data_module=DATA_MODULE
):
    """Loads `data_file_name` from `data_module with `importlib.resources`.
    Parameters
    ----------
    data_file_name : str
        Name of csv file to be loaded from `data_module/data_file_name`.
        For example `'wine_data.csv'`.
    data_module : str or module, default='scilightcon.datasets.data'
        Module where data lives. The default is `'scilightcon.datasets.data'`.
    Returns
    -------
    data : json object
    """
    with _open_text(data_module, data_file_name) as json_file:
        json_data = json.load(json_file)

    return json_data


def load_csv_data(
    data_file_name,
    *,
    data_module=DATA_MODULE
):
    """Loads `data_file_name` from `data_module with `importlib.resources`.
    Parameters
    ----------
    data_file_name : str
        Name of csv file to be loaded from `data_module/data_file_name`.
        For example `'wine_data.csv'`.
    data_module : str or module, default='scilightcon.datasets.data'
        Module where data lives. The default is `'scilightcon.datasets.data'`.
    Returns
    -------
    data : ndarray of shape (n_samples, n_features)
        A 2D array with each row representing one sample and each column
        representing the features of a given sample.
    target : ndarry of shape (n_samples,)
        A 1D array holding target variables for all the samples in `data`.
        For example target[0] is the target variable for data[0].
    target_names : ndarry of shape (n_samples,)
        A 1D array containing the names of the classifications. For example
        target_names[0] is the name of the target[0] class.
    """
    with _open_text(data_module, data_file_name) as csv_file:
        data_file = csv.reader(csv_file)
        n_header = 0
        possibly_header = next(data_file)
        header = [''] * len(possibly_header)
        is_header = possibly_header[0][0] == '#'
        if is_header:            
            header = possibly_header
            header[0] = header[0][1:]
            header = [entry.strip() for entry in header]

        while is_header:
            n_header = n_header + 1
            is_header = next(data_file)[0][0] == '#'

        csv_file.seek(n_header)
        n_samples = sum(1 for row in data_file) - n_header
        csv_file.seek(n_header)
        temp = next(data_file)
        n_features = len(temp)
        csv_file.seek(n_header)
        data = np.empty((n_samples, n_features))

        for i, ir in enumerate(data_file):
            if i>=n_header:
                data[i-n_header] = np.asarray(ir, dtype=np.float64)

    return data, header

