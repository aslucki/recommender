import os

import numpy as np
import pandas as pd


class Recommender:

    def __init__(self, database_dir):
        self.database_dir = database_dir
        self.data = self.load_data()
        self.features = self.load_features()
        self.companies = self.data['Company'].to_list()

    def load_data(self):
        return pd.read_csv(os.path.join(self.database_dir,
                                        'companies.csv'))

    def load_features(self):
        return pd.read_csv(os.path.join(self.database_dir,
                                        'features.csv'))

    def find_most_similar(self, company_name, n=3):
        company_id = self.data.loc[self.data['Company']
                                   == company_name, 'ID'].values[0]
        query_vector = self.features.loc[self.features['ID']
                                         == company_id, :'Age'].values
        feature_vectors = self.features.loc[:, :'Age'].values
        similarities = np.inner(query_vector, feature_vectors)
        selected = np.argsort(similarities.flatten())[::-1][1:n+1]

        return self.data.iloc[selected]








