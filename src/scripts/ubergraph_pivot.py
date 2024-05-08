import click
import sparql_dataframe
import pandas as pd
import logging
import os


@click.command()
@click.option('--endpoint', required=True, help='SPARQL endpoint URL')
@click.option('--query-file', required=True, help='File path to the SPARQL query file')
@click.option('--output-dir', required=True, type=click.Path(exists=True, file_okay=False, resolve_path=True),
              help='Output directory path')
@click.option('--output-basename', required=True, type=str, callback=lambda ctx, param, value: validate_basename(value),
              help='Base name of output files')
@click.option('--min-pred-usage', default=2, type=int, help='Minimum column sparsity')
@click.option('--min-object-usage', default=2, type=int, help='Minimum column sparsity')
# @click.option('--max-object-usage', default=999999, type=int, help='Maximum object usage')
@click.option('--object-exclusion-list', required=True, type=click.Path(exists=True), help='Maximum object usage')
@click.option('--predicate-exclusion-list', required=True, type=click.Path(exists=True), help='Maximum object usage')
def run_sparql_query(endpoint, query_file, output_dir, output_basename,
                     min_pred_usage, min_object_usage,
                     object_exclusion_list, predicate_exclusion_list):
    # Configure logging to stdout
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    raw_output = os.path.join(output_dir, output_basename + "_raw.csv")
    filtered_output = os.path.join(output_dir, output_basename + "_pivot_filtered.csv")
    predicate_usage_output = os.path.join(output_dir, output_basename + "_predicate_usage.csv")
    object_usage_output = os.path.join(output_dir, output_basename + "_object_usage.csv")

    # Read object exclusion list
    try:
        with open(object_exclusion_list, 'r') as file:
            object_exclusions = [line.strip() for line in file.readlines()]
        logging.info("Object exclusion list read successfully.")
    except IOError as e:
        logging.error(f"Error reading object exclusion list: {e}")
        return  # Handle the error appropriately

    # Read predicate exclusion list
    try:
        with open(predicate_exclusion_list, 'r') as file:
            predicate_exclusions = [line.strip() for line in file.readlines()]
        logging.info("Predicate exclusion list read successfully.")
    except IOError as e:
        logging.error(f"Error reading predicate exclusion list: {e}")
        return  # Handle the error appropriately

    # Read SPARQL query from file
    with open(query_file, 'r') as file:
        sparql_query = file.read()

    # Execute SPARQL query and save results to a DataFrame
    try:
        df = sparql_dataframe.get(endpoint, sparql_query, post=True)
        df.to_csv(raw_output, sep=",", index=False)
        logging.info("SPARQL query executed and results saved successfully.")
    except Exception as e:
        logging.error(f"Failed to execute SPARQL query or save results: {e}")
        return  # Or handle the error in another appropriate way

    # Get the ols value counts
    value_counts_df = df["ols"].value_counts().to_frame().reset_index()
    value_counts_df.columns = ['ols', 'count']
    value_counts_df.to_csv(object_usage_output, sep=",", index=False)
    logging.info("Object usage counts saved to file.")

    # Merge df with value_counts_df
    merged_df = pd.merge(df, value_counts_df, on='ols')
    logging.info("Dataframe merged successfully.")

    # Filter the merged dataframe based on the "Count" column
    filtered_df = merged_df[merged_df['count'] >= min_object_usage]
    logging.info("Merged dataframe filtered based on object usage.")

    # Drop the "Count" column if it's not needed in the final result
    filtered_df = filtered_df.drop('count', axis=1)
    logging.info("Count column dropped from the dataframe.")


    # Get the predicate value counts
    value_counts_df = df["predicate"].value_counts().to_frame().reset_index()
    value_counts_df.columns = ['predicate', 'count']
    value_counts_df.to_csv(predicate_usage_output, sep=",", index=False)
    logging.info("Predicate usage counts saved to file.")

    # Merge df with value_counts_df
    merged_df = pd.merge(df, value_counts_df, on='predicate')
    logging.info("Dataframe merged successfully.")

    # Filter the merged dataframe based on the "Count" column
    filtered_df = merged_df[merged_df['count'] >= min_pred_usage]
    logging.info("Merged dataframe filtered based on predicate usage.")

    # Drop the "Count" column if it's not needed in the final result
    filtered_df = filtered_df.drop('count', axis=1)
    logging.info("Count column dropped from the dataframe.")

    # Exclude rows based on object_exclusions list
    filtered_df = filtered_df[~filtered_df['ols'].isin(object_exclusions)]
    logging.info("Dataframe filtered to exclude specified objects.")

    # Exclude rows based on predicate_exclusions list
    filtered_df = filtered_df[~filtered_df['predicate'].isin(predicate_exclusions)]
    logging.info("Dataframe filtered to exclude specified predicates.")

    # Pivot the DataFrame
    pivot_df = pd.pivot_table(filtered_df, index='class', columns='predicate', values='ols',
                              aggfunc=lambda x: '|'.join(x.dropna().unique()))

    # Replace NaN values with an empty string
    pivot_df.fillna('', inplace=True)
    logging.info("DataFrame pivoted successfully.")

    # Generate a report of non-empty values in each column
    column_counts = pivot_df.astype(bool).sum(axis=0)
    report_df = pd.DataFrame({'predicate': column_counts.index, 'usage': column_counts.values})
    report_df.to_csv(predicate_usage_output, sep=",", index=False)
    logging.info("Predicate usage report generated.")

    # Remove sparse columns
    filtered_df = remove_sparse_columns(pivot_df, min_pred_usage)
    filtered_df.to_csv(filtered_output, sep=",", index=True)
    logging.info("Filtered DataFrame saved to file.")


# Function to validate output basename
def validate_basename(value):
    if '/' in value or '\\' in value:
        raise click.BadParameter('Output basename should not contain directory separators (/ or \\).')
    return value


# Function to remove columns with less than min_pred_usage non-blank values
def remove_sparse_columns(df, n):
    column_counts = df.astype(bool).sum(axis=0)
    columns_to_keep = column_counts[column_counts >= n].index
    return df[columns_to_keep]


if __name__ == '__main__':
    run_sparql_query()
