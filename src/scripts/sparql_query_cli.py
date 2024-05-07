import click
import sparql_dataframe
import pandas as pd
import re

# using sparql_dataframe and pandas because they handle special characters in the output very nicely

# hopefully we won't need these anymore
max_cell_val_length = 999_999
replacement_value = f"value omitted because length exceeds {max_cell_val_length} characters"


# def replace_whitespace(text):
#     """Replaces all stretches combining newline, carriage return, or tab characters
#     with a single whitespace character.
#
#     Args:
#       text: The text to be modified.
#
#     Returns:
#       The modified text with whitespace stretches collapsed.
#     """
#     return re.sub(r"[\\n\r\t]+", " ", text)


# not crazy about iterating over rows, making a new list of dicts and then converting that to a dataframe
# maybe this won't be necessary anymore either
def convert_to_dataframe(results):
    """ Convert query results to a pandas DataFrame. """
    data = []
    # Extract variable names (headers)
    headers = results.columns
    # Extract each row of results
    for index, row in results.iterrows():
        new_row = {}
        for header in headers:
            value = row[header]
            if isinstance(value, str) and len(value) > max_cell_val_length:
                value = replacement_value
            new_row[header] = value
        data.append(new_row)
    return pd.DataFrame(data)


@click.command()
@click.option('--query-file', type=click.Path(exists=True), required=True, help='File containing the SPARQL query.')
@click.option('--endpoint', required=True, help='URL of the SPARQL endpoint.')
@click.option('--output-file', required=True, help='Output CSV file name.')
def main(query_file, endpoint, output_file):
    """ Execute a SPARQL query from a file against a specified endpoint and output results in CSV format. """
    with open(query_file, 'r') as file:
        query = file.read()
    df = sparql_dataframe.get(endpoint, query)
    df = convert_to_dataframe(df)
    df.to_csv(output_file, index=False)


if __name__ == "__main__":
    main()
