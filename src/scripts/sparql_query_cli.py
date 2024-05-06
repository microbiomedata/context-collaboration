import click
from SPARQLWrapper import SPARQLWrapper, JSON


def convert_to_tsv(results):
    """ Convert query results to TSV format. """
    # Extract variable names (headers)
    headers = results["head"]["vars"]
    # Print headers
    print("\t".join(headers))
    # Print each row of results
    for result in results["results"]["bindings"]:
        row = [result[var]['value'] if var in result else "" for var in headers]
        print("\t".join(row))


@click.command()
@click.option('--query-file', type=click.File('r'), required=True, help='File containing the SPARQL query.')
@click.option('--endpoint', required=True, help='URL of the SPARQL endpoint.')
def main(query_file, endpoint):
    """ Execute a SPARQL query from a file against a specified endpoint and output results in TSV format. """
    query = query_file.read()
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    convert_to_tsv(results)


if __name__ == "__main__":
    main()
