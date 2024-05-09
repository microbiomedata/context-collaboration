import click
import pandas as pd


@click.command()
@click.argument('input-files', nargs=-1, type=click.Path(exists=True))
@click.option('--output-file', '-o', default='output.tsv', help='Output file name')
def concatenate_tsv(input_files, output_file):
    """
    Concatenates multiple TSV files vertically and saves the output to a new TSV file.
    """
    if not input_files:
        click.echo("No input files provided.")
        return

    # Read each TSV file into a DataFrame
    dfs = []
    for file in input_files:
        df = pd.read_csv(file, sep='\t')
        dfs.append(df)

    # Concatenate vertically
    concatenated_df = pd.concat(dfs, axis=0, ignore_index=True)

    # Save to a new TSV file
    concatenated_df.to_csv(output_file, sep='\t', index=False)
    click.echo(f"Concatenated TSV files saved to {output_file}")


if __name__ == '__main__':
    concatenate_tsv()
