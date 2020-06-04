import os
from pathlib import Path

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def split_column_to_dict(run_manifest, column="countries", sep=";"):
    """Splits a column in csv format into a dictionary"""
    for index, row in run_manifest.iterrows():
        countries = {
            x.strip('" '): True 
            for x in row[column].strip().split(";")
        }
        countries.pop('', None)
        run_manifest.loc[index, column] = [countries]  # Listed as data frame tries to unpack otherwise
    return run_manifest

def read_manifest(manifest_file):
    """ Reads and parses the run manifest files.
    """
    run_manifest = pd.read_csv(manifest_file)
    run_manifest.rename(columns=lambda x: x.strip(), inplace=True)
    run_manifest = split_column_to_dict(run_manifest, 'countries', sep=';')
    run_manifest = split_column_to_dict(run_manifest, 'modelling zones', sep=';')
    for col in ["folder", "last available data", "version"]:
        run_manifest[col] = run_manifest[col].str.strip()
    return run_manifest

def get_analysis_set(
    run_manifest, 
    selection_fun=lambda x: True, 
    data_to_load=None,
):
    ''' 
    '''
    if type(run_manifest) == type(str()) \
        or type(run_manifest) == type(Path()):
        run_manifest = read_manifest(run_manifest)
    
    analysis_set = run_manifest[run_manifest.apply(selection_fun ,axis=1)]
    analysis_set['model'] = None

    for index, row in analysis_set.iterrows():
        analysis_set.loc[index, 'model'] = Model_Folder(
            row['folder'].strip(), load_failure_is_err=False)
        analysis_set.loc[index, 'model'].load_data(data_to_load)
    return analysis_set

class Model_Folder(object):
    """
    """
    
    default_files_to_load = {
        'interventions': 'base-intervention',
        'modelling': 'base-plot',
        'forecasting': 'forecast-data',
        'ifr': 'inputs-active_regions_ifr',
        'reprodution': 'final-Rt',
        # 'mu': 'final-mu',
        'NPI impact': 'covars-alpha-reduction',
        'mobility': 'inputs-processed-mobility',
        'arguments': 'inputs-parsed-cmd-arguments',
    }

    def __init__(
        self,
        run_directory,
        *args,
        files_to_load=None,
        load_failure_is_err=True,
    ):
        if files_to_load is None:
            files_to_load = Model_Folder.default_files_to_load
        self.run_directory = Path(run_directory)
        self.files_to_load = files_to_load
        self.find_files(load_failure_is_err=load_failure_is_err)
    
    def find_files(self, load_failure_is_err=True):
        
        if not hasattr(self, 'files'):
            self.files = {}
            self.missing_files = {}

        all_found = True
        for file_key in self.files_to_load:
            self.files[file_key] = self.run_directory.joinpath(
                self.run_directory.name + '-' + self.files_to_load[file_key] + '.csv'
            )
            # Checks that files exist
            all_found &= self.files[file_key].is_file()
            if not self.files[file_key].is_file():
                print(f"WARNING: csv corresponding to {file_key} could not be found\n{self.files[file_key]}")
                self.missing_files[file_key] = self.files[file_key]
                self.files.pop(file_key)

        if not all_found:
            err_text = f"One or more of the required csvs was not found in folder:\n {self.run_directory}"
            if load_failure_is_err:
                raise FileNotFoundError("Error : " + err_text)
            else:
                print("Warning : " + err_text)
        return self.files

    def load_data(self, data_category=None):
        self.data = {}
        if data_category is None:
            for file in self.files:
                self.data[file] = pd.read_csv(self.files[file])
            data_categories = [file for file in self.files]

        elif isinstance(data_category, type(list())):
            for file in data_category:
                self.data[file] = pd.read_csv(self.files[file])
            data_categories = data_category

        elif isinstance(data_category, type(str())):
            self.data[data_category] = pd.read_csv(self.files[data_category])
            data_categories = [data_category]

        else:
            raise AttributeError(
                f"Unknown data_category format of type {type(data_category)}")

        self._process_data(data_categories)

    def _process_data(self, data_categories):
        for data_category in data_categories:

            if data_category == "arguments":
                df_args = self.data[data_category]
                self.data[data_category] = {
                    row.iloc[0]: row.iloc[1]
                    for i, (_, row) in enumerate(df_args.iterrows())
                }

