import os

import numpy as np
import pandas as pd


class Recommender:

    def __init__(self, database_dir):
        self.database_dir = database_dir
        self.data = self.load_data()
        self.features = self.load_features()
        self.companies = self.data['Name'].to_list()
        self.feature_columns = self.features.loc[:, 'cb_rank_(company)':].columns

    def load_data(self):
        return pd.read_csv(os.path.join(self.database_dir,
                                        'companies.csv'))

    def load_features(self):
        return pd.read_csv(os.path.join(self.database_dir,
                                        'features.csv'))

    def filter_data(self, company_data, filters):
        new_restricted_ids = []
        for filter in filters:
            if filter == 'same_country':
                country = company_data['Location'].str.split().values[0][-1]
                new_restricted_ids.extend(
                    self.data[~self.data['Location'].str.contains(country)]['ID'].values)
            elif filter == 'same_industry':
                industries = company_data['Industries'].str.split(',').values[0]
                new_restricted_ids.extend(
                    self.data[
                        ~(
                            (~self.data['Industries'].isna()) &
                            (self.data['Industries'].str.contains('|'.join(industries)))
                        )]['ID'].values)
            elif filter == 'has_linkedin':
                new_restricted_ids.extend(self.data[self.data['Linkedin'].isna()]['ID'].values)

        return set(new_restricted_ids)

    def find_most_similar(self, company_name, restricted_ids, threshold, filters=None):
        company_data = self.data.loc[self.data['Name'] == company_name, :]
        company_id = company_data['ID'].values[0]

        if filters is not None:
            restricted_ids =\
                restricted_ids.union(self.filter_data(company_data,filters))

        query_vector =\
            self.features.loc[self.features['ID']
                              == company_id, self.feature_columns].values

        searchable_features = self.features[~self.features['ID'].isin(restricted_ids)]
        feature_vectors = searchable_features.loc[:, self.feature_columns].values
        similarities = np.inner(query_vector, feature_vectors)
        number_of_qualified_results = min(500, sum(similarities.flatten() >= threshold))
        selected = np.argsort(similarities.flatten())[::-1][1:number_of_qualified_results]
        selected_ids = searchable_features.iloc[selected]['ID']

        output_data = self.data.loc[self.data['ID'].isin(selected_ids), :]
        try:
            output_data = output_data.sort_values(by='ID', key=lambda x: selected)
        except ValueError:
            pass

        info = self.alternative_matches(company_data.squeeze(),
                                        output_data)

        return output_data, info

    def sort_features_matches(self, query_vector, selected_vectors):

        differences = np.abs(selected_vectors - query_vector)
        sorted_matches = np.argsort(differences)
        sorted_features = []
        for match in sorted_matches:
            sorted_features.append([self.feature_columns[i] for i in match])

        return sorted_features

    @staticmethod
    def alternative_matches(company_data, matching_startups):
        info = []
        for _, match in matching_startups.iterrows():
            info.append(InfoTemplate(company_data, match).get_info())

        return info


class InfoTemplate:
    def __init__(self, query_startup, matching_startup):
        self.query_startup = query_startup
        self.matching_startup = matching_startup
        self.query_name = self.query_startup['Name']
        self.matching_name = self.matching_startup['Name']

    def get_info(self):
        return f"Location:\n {self.location()}\n\n"\
               f"Industries:\n {self.industries()}\n\n"\
               f"Employees:\n {self.employees()}\n\n" \
               f"Total funding:\n {self.funding()}\n\n"

    def location(self):

        query_country =\
            self.query_startup['Location'].split(',')[-1].strip()
        matching_country =\
            self.matching_startup['Location'].split(',')[-1].strip()

        if query_country == matching_country:
            return f"{self.query_name} is headquartered in the {query_country}, "\
                   f"just like {self.matching_name}"
        else:
            return f"The headquarters of {self.query_name} is located in {query_country}, "\
                   f"while the headquarters of {self.matching_name} is located in {matching_country}"

    def industries(self):
        try:
            query_industries = self.query_startup['Industries'].split(',')
            matching_industries = self.matching_startup['Industries'].split(',')
        except AttributeError:
            return "No data available"

        common = list(set(query_industries) & set(matching_industries))
        different = list(set(query_industries) - set(matching_industries))

        if not different:
            return f'{self.query_name} and {self.matching_name} have '\
                   f'all the same industires categories: {", ".join(common)}'
        if common and different:
            return f'{self.query_name} and {self.matching_name} have the same '\
                   f'industries categories: {", ".join(common)}. \n'\
                   f'{self.query_name} have different industries categories: '\
                   f'{", ".join(different)}'
        else:
            return f'{self.query_name} operates in: {", ".join(query_industries)} '\
                   f'that don\'t overlap with {self.matching_name} industries'

    def employees(self):
        try:
            query_employees = self.query_startup['No. Employees']
            matching_employees = self.matching_startup['No. Employees']
            if (str(matching_employees) == 'nan'
                or str(query_employees) == 'nan'):
                raise AttributeError()
        except AttributeError:
            return "No data available"

        if query_employees == matching_employees:
            return f'{self.query_name} and {self.matching_name} '\
                   f'have the same number of empolyees'
        else:
            return f'{self.query_name} employs {query_employees} and '\
                   f'{self.matching_name} employs {matching_employees} people.'

    def funding(self):
        try:
            query_funding = self.query_startup['Total Funding $']
            matching_funding = self.matching_startup['Total Funding $']

            if (str(query_funding) == 'nan'
                    or str(matching_funding) == 'nan'):
                raise AttributeError()
        except AttributeError:
            return "No data available"

        return f'{self.query_name}\'s total funding is ${round(query_funding)}. ' \
               f'{self.matching_name} total funding is ${round(matching_funding)}.\n' \
               f'It means that {self.query_name} collected ' \
               f'{query_funding / matching_funding * 100:.2f}% of ' \
               f'the {self.matching_name}\'s funding.'























