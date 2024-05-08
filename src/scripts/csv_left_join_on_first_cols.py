import click
import pandas as pd


@click.command()
@click.option('--left-csv', type=click.Path(exists=True), help='Path to the first CSV file')
@click.option('--right-csv', type=click.Path(exists=True), help='Path to the second CSV file')
@click.option('--output', required=True, type=click.Path(), help='Path to output the merged CSV file')
def merge_csv(left_csv, right_csv, output):
    # Load the CSV files
    df1 = pd.read_csv(left_csv)
    df2 = pd.read_csv(right_csv)

    # Merge the dataframes using a left join on the first column of each
    merged_df = pd.merge(df1, df2, left_on=df1.columns[0], right_on=df2.columns[0], how='left')

    # Save the merged dataframe to a new CSV file
    merged_df.to_csv(output, index=False)

    print(f"Merged CSV saved as {output}")


if __name__ == "__main__":
    merge_csv()
