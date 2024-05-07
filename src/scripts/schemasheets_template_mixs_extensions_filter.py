import csv
import sys
import pandas as pd


def filter_and_clean_tsv(df):
    # df = pd.DataFrame(reader)

    # Filter rows where 'is_a' == 'Extension'
    df_filtered = df[df['is_a'] == 'Extension']

    # Columns to remove (after filtering)
    columns_to_remove = ['aliases', 'class_uri', 'from_schema', 'is_a', 'see_also']

    # Remove columns with all null values or all empty strings
    def is_empty_col(col):
        return col.isnull().all() or (col.astype(str).str.strip() == '').all()

    df_cleaned = df_filtered.loc[:, ~df_filtered.apply(is_empty_col, axis=0)]

    # Drop specified columns
    df_cleaned = df_cleaned.drop(columns_to_remove, axis=1, errors='ignore')

    return df_cleaned


def main():
    # Read TSV data from standard input
    df = pd.read_csv(sys.stdin, delimiter='\t')

    # Filter and clean data
    filtered_rows = filter_and_clean_tsv(df)

    filtered_rows.to_csv(sys.stdout, sep=',', index=False)

    # # Create a writer to send filtered data to standard output
    # csv_writer = csv.writer(sys.stdout, delimiter='\t')
    #
    # # Check if there are any rows to write
    # if filtered_rows:
    #     # Write the header row
    #     csv_writer.writerow(filtered_rows[0].keys())
    #
    #     # Write the filtered data
    #     csv_writer.writerows(row.values() for row in filtered_rows)
    # else:
    #     print("No data to write.")


if __name__ == "__main__":
    main()
