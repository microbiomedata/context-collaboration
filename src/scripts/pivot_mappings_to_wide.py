import pandas as pd
import click
from typing import Tuple


def concatenate_columns(df: pd.DataFrame, columns: Tuple[str, str], new_column_name: str) -> pd.DataFrame:
    """
    Concatenate two columns of a DataFrame into a new column.

    Args:
        df (pd.DataFrame): Input DataFrame.
        columns (Tuple[str, str]): Names of the columns to concatenate.
        new_column_name (str): Name of the new column to create.

    Returns:
        pd.DataFrame: DataFrame with the new concatenated column.
    """
    # Check if all specified columns exist in the DataFrame
    for column in columns:
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in the DataFrame.")

    # Perform concatenation
    df[new_column_name] = df[columns[0]].astype(str) + '|' + df[columns[1]].astype(str)
    return df


@click.command()
@click.option('--input-file', '-i', required=True, type=click.Path(exists=True), help='Path to the input TSV file.')
@click.option('--output-file', '-o', required=True, type=click.Path(), help='Path to save the output TSV file.')
def process_data(input_file: str, output_file: str) -> None:
    """
    Process TSV file by concatenating columns and pivoting the data.

    Args:
        input_file (str): Path to the input TSV file.
        output_file (str): Path to save the output TSV file.
    """
    try:
        # Read the TSV file into a DataFrame
        df = pd.read_csv(input_file, sep='\t')

        # Concatenate agent and timestamp into a new column
        df = concatenate_columns(df, ('agent', 'timestamp'), 'agent_timestamp')
        df = concatenate_columns(df, ('confidence', 'comment'), 'confidence_comment')

        # Pivot the data
        df_pivot = df.pivot_table(
            index=['ontology_class_slug', 'ontology_class_label', 'mixs_context_label', 'mixs_environment_label'],
            columns='agent_timestamp',
            values='confidence_comment',
            aggfunc='first')

        # Reset index to make 'ontology_class_slug', 'ontology_class_label', 'mixs_context_label', 'mixs_environment_label' regular columns
        df_pivot.reset_index(inplace=True)

        # Write the pivoted DataFrame to a new TSV file
        df_pivot.to_csv(output_file, sep='\t', index=False)
        click.echo("Data processed successfully!")
    except Exception as e:
        click.echo(f"Error processing data: {str(e)}")


if __name__ == '__main__':
    process_data()
