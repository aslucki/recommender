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


def get_columns_info():

    columns_mapping = {
        'organization_name': 'Name',
        'headquarters_location': 'Location',
        'description': 'Description',
        'industries': 'Industries',
        'website': 'Website',
        'linkedin': 'Linkedin',
        'number_of_employees': 'No. Employees',
        'total_funding_amount_currency_(in_usd)': 'Total Funding $',
        'founded_date': 'Founded Date',
        'top_5_investors': 'Top 5 Investors',
        'number_of_funding_rounds': 'No. Funding rounds',
        'last_funding_date': 'Last Funding Date',
        'last_funding_amount_currency_(in_usd)': 'Last Funding $',
        'funding_status': 'Funding Status',
        'estimated_revenue_range': 'Estimated Revenue'
    }

    limited_output = [
        'ID', 'Name', 'Location', 'Description', 'Industries', 'Website',
        'Linkedin', 'No. Employees', 'Total Funding $'
    ]

    info = {
        'mapping': columns_mapping,
        'limited_output': limited_output
    }

    return info


def table_to_dict(table: pd.DataFrame, sorted_features=None):
    table.fillna("", inplace=True)
    columns_mapping = get_columns_info()['mapping']
    columns = [columns_mapping.get(column, column)
               for column in table.columns]
    rows = table.values

    details = None
    if sorted_features:
        details = sorted_features

    return {"columns": columns, "rows": rows, "details": details}
