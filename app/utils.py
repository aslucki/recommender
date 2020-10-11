import os

import pandas as pd


def load_stored_ids(database_path):
    saved_entries = set()
    discarded_entries = set()

    try:
        with open(os.path.join(database_path,
                               'saved_entries.txt'), 'r') as f:
            ids = [entry.strip() for entry in f.readlines()]
            saved_entries.update(ids)
    except FileNotFoundError:

        pass

    try:
        with open(os.path.join(database_path,
                               'discarded_entries.txt'), 'r') as f:
            ids = [entry.strip() for entry in f.readlines()]
            discarded_entries.update(ids)
    except FileNotFoundError:
        pass

    return saved_entries, discarded_entries


def table_to_dict(table: pd.DataFrame, sorted_features=None):

    columns = table.columns
    rows = table.values

    details = None
    if sorted_features:
        details = sorted_features

    return {"columns": columns, "rows": rows, "details": details}