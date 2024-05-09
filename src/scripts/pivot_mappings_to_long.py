from typing import Tuple

import pandas as pd
import click


def split_column(df: pd.DataFrame, column_to_split: str, new_columns: Tuple[str, str], sep: str = '|') -> pd.DataFrame:
    """
    Split a specified column into two new columns based on a separator.

    Args:
        df (pd.DataFrame): Input DataFrame.
        column_to_split (str): Name of the column to split.
        new_columns (Tuple[str, str]): Tuple containing names of the new columns.
        sep (str): Separator used to split the column.

    Returns:
        pd.DataFrame: DataFrame with the new columns added and the original column removed.
    """
    # Split the column into two new columns
    splits = df[column_to_split].str.split(sep, expand=True)
    df[new_columns[0]], df[new_columns[1]] = splits[0], splits[1]
    # Optionally, remove the original column after splitting
    df.drop(columns=[column_to_split], inplace=True)
    return df


@click.command()
@click.option('--input-file', '-i', required=True, type=click.Path(exists=True), help='Path to the input TSV file.')
@click.option('--output-file', '-o', required=True, type=click.Path(), help='Path to save the output TSV file.')
def process_data(input_file: str, output_file: str) -> None:
    """
    Process TSV file by transforming data from wide format to long format, splitting concatenated columns,
    removing rows without complete data, and ensuring clean output.

    Args:
        input_file (str): Path to the input TSV file.
        output_file (str): Path to the output TSV file.
    """
    try:
        # Read the TSV file into a DataFrame
        df = pd.read_csv(input_file, sep='\t')

        # Melt the DataFrame from wide to long format
        df_long = df.melt(
            id_vars=['ontology_class_slug', 'ontology_class_label', 'mixs_context_label', 'mixs_environment_label'],
            var_name='agent_timestamp', value_name='confidence_comment')

        # Split the 'agent_timestamp' column into 'agent' and 'timestamp'
        df_long = split_column(df_long, 'agent_timestamp', ('agent', 'timestamp'))

        # Split the 'confidence_comment' column into 'confidence' and 'comment'
        df_long = split_column(df_long, 'confidence_comment', ('confidence', 'comment'))

        # Remove rows where necessary data is missing
        df_long.dropna(subset=['confidence', 'comment'], inplace=True)

        # Write the long DataFrame to a new TSV file
        df_long.to_csv(output_file, sep='\t', index=False)
        click.echo("Data processed successfully!")
    except Exception as e:
        click.echo(f"Error processing data: {str(e)}")


if __name__ == '__main__':
    process_data()
