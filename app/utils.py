import pandas as pd


def load_stored_ids(entries):
    saved_entries = []
    discarded_entries = []

    for entry in entries:
        if entry.is_discarded:
            discarded_entries.append(entry.startup_id)
        else:
            saved_entries.append(entry.startup_id)

    return set(saved_entries), set(discarded_entries)


def table_to_dict(table: pd.DataFrame, sorted_features=None):

    columns = table.columns
    rows = table.values

    details = None
    if sorted_features:
        details = sorted_features

    return {"columns": columns, "rows": rows, "details": details}
