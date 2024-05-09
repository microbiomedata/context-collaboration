import pprint

import click
import pandas as pd

from oaklib import get_adapter
from oaklib.datamodels.vocabulary import IS_A

from typing import Union, List, NewType

from datetime import datetime

Slug = NewType('Slug', str)  # namesapce_localid
Curie = NewType('Curie', str)  # namesapce:localid


def slugs_to_curies(slug: Union[Slug, List[Slug]]) -> Union[Curie, List[Curie]]:
    """
    Convert a slug or a list of slugs to CURIE format(s).

    Parameters:
        slug (Union[Slug, List[Slug]]): The slug(s) to convert.

    Returns:
        Union[Curie, List[Curie]]: The CURIE format(s) converted from the slug(s).
    """
    if isinstance(slug, list):
        return [Curie(s.replace('_', ':')) for s in slug]
    else:
        return Curie(slug.replace('_', ':'))


def curies_to_slugs(curie: Union[Curie, List[Curie]]) -> Union[Slug, List[Slug]]:
    """
    Convert a CURIE or a list of CURIEs to slug(s).

    Parameters:
        curie (Union[Curie, List[Curie]]): The CURIE(s) to convert.

    Returns:
        Union[Slug, List[Slug]]: The slug(s) converted from the CURIE(s).
    """
    if isinstance(curie, list):
        return [Slug(c.replace(':', '_')) for c in curie]
    else:
        return Slug(curie.replace(':', '_'))


def get_descendant_slugs(adapter, parent_slug: Slug, reflexive: bool = False) -> List[Slug]:
    """
    Get the descendant slugs of a parent slug using the provided adapter.

    Parameters:
        adapter: The adapter used to retrieve descendants.
        parent_slug (Slug): The slug of the parent.

    Returns:
        List[Slug]: A list of descendant slugs.
    """
    descendants = []
    parent_curie = slugs_to_curies(parent_slug)
    for descendant in adapter.descendants(parent_curie, predicates=[IS_A], reflexive=reflexive):
        descendant_slug = curies_to_slugs(descendant)
        descendants.append(descendant_slug)  # Convert to Slug type explicitly
    return descendants


def get_labels_from_curies(adapter, curie: Union[Curie, List[Curie]]) -> Union[str, List[str]]:
    """
    Get the label(s) of a CURIE or a list of CURIEs using the provided adapter.

    Parameters:
        adapter: The adapter used to retrieve the label(s).
        curie (Union[Curie, List[Curie]]): The CURIE(s) to get the label(s) for.

    Returns:
        Union[str, List[str]]: The label(s) of the CURIE(s).
    """
    if isinstance(curie, list):
        return [adapter.label(c) for c in curie]
    else:
        return adapter.label(curie)


@click.command()
@click.option('--tsv-input', type=click.Path(exists=True), prompt='Please provide the path to the TSV file',
              help='Path to the TSV input file.')
@click.option('--mixs-context-label',
              type=click.Choice(['env_broad_scale', 'env_local_scale', 'env_medium'], case_sensitive=True),
              multiple=True,
              help='Filter by one or more MIXS context labels. Allowed values are env_broad_scale, env_local_scale, and env_medium.')
@click.option('--mixs-environment-label', type=click.Choice([
    'Agriculture', 'Air', 'BuiltEnvironment', 'FoodAnimalAndAnimalFeed',
    'FoodFarmEnvironment', 'FoodFoodProductionFacility', 'FoodHumanFoods',
    'HostAssociated', 'HumanAssociated', 'HumanGut', 'HumanOral',
    'HumanSkin', 'HumanVaginal', 'HydrocarbonResourcesCores',
    'HydrocarbonResourcesFluidsSwabs', 'MicrobialMatBiofilm',
    'MiscellaneousNaturalOrArtificialEnvironment', 'PlantAssociated',
    'Sediment', 'Soil', 'SymbiontAssociated', 'WastewaterSludge', 'Water'
], case_sensitive=False), multiple=True, help='Filter by one or more MIXS environment labels.')
@click.option('--agent', multiple=True, help='Filter by one or more agents.')
@click.option('--timestamp', multiple=True, help='Filter by one or more timestamps.')
@click.option('--min-confidence', type=float, help='Minimum confidence level to filter by (0 to 1).')
@click.option('--tsv-output', required=True, type=click.Path(), help='Path to the output file.')
@click.option('--timezone',
              type=click.Choice(['EDT', 'EST', 'PDT', 'PST', 'UTC'], case_sensitive=False),
              required=True,
              multiple=False,
              help='Specify your timezone for stamping the output.')
@click.option('--inputs-as-inferences', is_flag=False, help='Include the input mappings in the output.')
def process_tsv(tsv_input, mixs_context_label, mixs_environment_label, agent, timestamp, min_confidence, tsv_output,
                timezone, inputs_as_inferences):
    pd.set_option('display.max_columns', None)

    # Get the current datetime
    current_datetime = datetime.now()

    # Format the datetime object into the desired pattern
    timestamp_string = current_datetime.strftime('%Y-%m-%dT%H:%M')

    timestamp_string += f' {timezone}'

    print(timestamp_string)

    adapter = get_adapter("sqlite:obo:envo")

    # Read the TSV file into a DataFrame
    df = pd.read_csv(tsv_input, sep='\t')

    # Print the shape of the DataFrame before filtering
    click.echo(f'The shape of the input is: {df.shape}')

    # Apply filters based on provided values. Only filter rows if options are not empty.
    if mixs_context_label:
        df = df[df['mixs_context_label'].isin(mixs_context_label)]
    if mixs_environment_label:
        df = df[df['mixs_environment_label'].isin(mixs_environment_label)]
    if agent:
        df = df[df['agent'].isin(agent)]
    if timestamp:
        df = df[df['timestamp'].isin(timestamp)]
    if min_confidence is not None:  # Check if a minimum confidence level is specified
        df = df[df['confidence'] >= min_confidence]

    df = df.drop_duplicates()

    # Print the shape of the DataFrame after filtering
    click.echo(f'The shape of the filtered DataFrame is: {df.shape}')

    # Create an empty list to store dictionaries representing rows
    inferences_data = []

    # Iterate over rows and print results as dictionaries
    for index, row in df.iterrows():
        row_dict = row.to_dict()
        subclasses = get_descendant_slugs(adapter, row_dict['ontology_class_slug'],
                                          reflexive=inputs_as_inferences)  # add some caching
        subclasses_labels = get_labels_from_curies(adapter, slugs_to_curies(subclasses))  # add some caching
        for subclass, label in zip(subclasses, subclasses_labels):  # assuming they have the same length!
            row_dict = {
                "confidence": 0.5,
                'agent': "expand-subset",
                'comment': f"Inferred from {row['agent']} {row['timestamp']}: {row['ontology_class_slug']}/{row['ontology_class_label']} @ {row['confidence']}",
                'mixs_context_label': row["mixs_context_label"],
                'mixs_environment_label': row["mixs_environment_label"],
                'ontology_class_label': label,
                'ontology_class_slug': subclass,
                'timestamp': timestamp_string,
            }
            inferences_data.append(row_dict.copy())

    # Create a DataFrame from the list of dictionaries
    inferences = pd.DataFrame(inferences_data)
    inferences = inferences.drop_duplicates()

    click.echo(f'The shape of the output is: {inferences.shape}')

    # write the DataFrame to a TSV file
    inferences.to_csv(tsv_output, sep='\t', index=False)


if __name__ == '__main__':
    process_tsv()

#
