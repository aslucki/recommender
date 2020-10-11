import os

import numpy as np
import pandas as pd


class Recommender:

    def __init__(self, database_dir):
        self.database_dir = database_dir
        self.data = self.load_data()
        self.features = self.load_features()
        self.companies = self.data['Company'].to_list()
        self.feature_columns = self.data.loc[:, 'Employees':].columns

    def load_data(self):
        return pd.read_csv(os.path.join(self.database_dir,
                                        'companies.csv'))

    def load_features(self):
        return pd.read_csv(os.path.join(self.database_dir,
                                        'features.csv'))

    def find_most_similar(self, company_name, restricted_ids, n=3):
        company_id = self.data.loc[self.data['Company']
                                   == company_name, 'ID'].values[0]
        query_vector =\
            self.features.loc[self.features['ID']
                              == company_id, self.feature_columns].values

        searchable_features = self.features[~self.features['ID'].isin(restricted_ids)]
        feature_vectors = searchable_features.loc[:, self.feature_columns].values
        similarities = np.inner(query_vector, feature_vectors)
        selected = np.argsort(similarities.flatten())[::-1][1:n+1]

        selected_ids = searchable_features.iloc[selected]['ID']

        sorted_features = self.sort_features_matches(query_vector, feature_vectors[selected])

        return self.data[self.data['ID'].isin(selected_ids)], sorted_features

    def sort_features_matches(self, query_vector, selected_vectors):

        differences = np.abs(selected_vectors - query_vector)
        sorted_matches = np.argsort(differences)
        sorted_features = []
        for match in sorted_matches:
            sorted_features.append([self.feature_columns[i] for i in match])

        return sorted_features

















