## Add your own custom Makefile targets here
RUN = poetry run
ENVO_OAKLIB = runoak -i sqlite:obo:envo
UBERGRAPH = https://ubergraph.apps.renci.org/sparql
NMDC_GRAPHDB = http://35.173.42.85/repositories
NMDC_GRAPHDB_ENVO = $(NMDC_GRAPHDB)/envo-2024-05-01

# includes
# ENVO:00000428 ! biome

assets/outputs/oaklib/biomes.txt:
	#ENVO descendants 'biome'
	$(RUN) $(ENVO_OAKLIB) descendants 'biome' > $@

assets/outputs/oaklib/environmental_materials.txt:
	#ENVO descendants 'biome'
	$(RUN) $(ENVO_OAKLIB) descendants 'environmental material' > $@

assets/outputs/sparql/envo_subset_non_host_non_food_env_local_scale_annotations.csv: assets/queries/sparql/envo_subset_non_host_non_food_env_local_scale_annotations.rq
	$(RUN) sparql-query-cli \
		--query-file $<	\
		--endpoint $(NMDC_GRAPHDB_ENVO) \
		--output-file $@


assets/outputs/sparql/biome_annotations.csv: assets/queries/sparql/biome_annotations.rq
	$(RUN) sparql-query-cli \
		--query-file $<	\
		--endpoint $(NMDC_GRAPHDB_ENVO) \
		--output-file $@


assets/outputs/sparql/environmental_material_annotations.csv: assets/queries/sparql/environmental_material_annotations.rq
	$(RUN) sparql-query-cli \
		--query-file $<	\
		--endpoint $(NMDC_GRAPHDB_ENVO) \
		--output-file $@

assets/outputs/sparql/environmental_material_relations_pivot_filtered.csv: assets/queries/sparql/environmental_material_relations_pivot.rq
	$(RUN) ubergraph-pivot \
		--endpoint "https://ubergraph.apps.renci.org/sparql" \
		--min-object-usage 2 \
		--min-pred-usage 2 \
		--object-exclusion-list assets/exclusion_lists/environmental_material_relation_object_exclusions.txt \
		--predicate-exclusion-list assets/exclusion_lists/environmental_material_relation_predicate_exclusions.txt \
		--output-basename "environmental_material_relations" \
		--output-dir "assets/outputs/sparql/" \
		--query-file $<


#envo_selected_material_entity_relations_pivot_object_usage.csv envo_selected_material_entity_relations_pivot_predicate_usage.csv envo_selected_material_entity_relations_pivot_raw.csv: envo_selected_material_entity_relations_pivot_filtered.csv
#
#assets/outputs/sparql/envo_selected_material_entity_relations_pivot_filtered.csv:
#	$(RUN) ubergraph-pivot \
#		--endpoint "https://ubergraph.apps.renci.org/sparql" \
#		--max-object-usage 100 \
#		--min-col-sparsity 2 \
#		--object-exclusion-list assets/queries/sparql/envo_relation_object_exclusions.txt \
#		--output-basename "envo_selected_material_entity_relations_pivot" \
#		--output-dir "assets/outputs/sparql/" \
#		--query-file "assets/queries/sparql/envo_relations_pivot.rq"


assets/outputs/sparql/biome_relations_object_usage.csv assets/outputs/sparql/biome_relations_predicate_usage.csv assets/outputs/sparql/biome_relations_raw.csv: assets/outputs/sparql/biome_relations_pivot_filtered.csv

assets/outputs/sparql/biome_relations_pivot_filtered.csv: assets/queries/sparql/biome_relations_pivot.rq
	$(RUN) ubergraph-pivot \
		--endpoint "https://ubergraph.apps.renci.org/sparql" \
		--min-object-usage 2 \
		--min-pred-usage 2 \
		--object-exclusion-list assets/exclusion_lists/biome_relation_object_exclusions.txt \
		--predicate-exclusion-list assets/exclusion_lists/biome_relation_predicate_exclusions.txt \
		--output-basename "biome_relations" \
		--output-dir "assets/outputs/sparql/" \
		--query-file $<

assets/outputs/sparql/biome_merged.csv: assets/outputs/sparql/biome_annotations.csv \
assets/outputs/sparql/biome_relations_pivot_filtered.csv
	$(RUN) python src/scripts/csv_left_join_on_first_cols.py \
		--left-csv $(word 1,$^) \
		--right-csv $(word 2,$^) \
		--output $@

assets/outputs/sparql/environmental_material_merged.csv: assets/outputs/sparql/environmental_material_annotations.csv \
assets/outputs/sparql/environmental_material_relations_pivot_filtered.csv
	$(RUN) python src/scripts/csv_left_join_on_first_cols.py \
		--left-csv $(word 1,$^) \
		--right-csv $(word 2,$^) \
		--output $@

# which runoak
  #/home/mark/.cache/pypoetry/virtualenvs/context-collaboration-meDaFbyk-py3.10/bin/runoak

# https://github.com/INCATools/ontology-access-kit/blob/main/src/oaklib/cli.py

# #!/home/mark/.cache/pypoetry/virtualenvs/context-collaboration-meDaFbyk-py3.10/bin/python
  ## -*- coding: utf-8 -*-
  #import re
  #import sys
  #from oaklib.cli import main
  #if __name__ == '__main__':
  #    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
  #    sys.exit(main())

#  find ~ -name envo.db
  #/home/mark/gitrepos/nmdc-ontology/downloads/envo.db
  #/home/mark/gitrepos/semantic-sql/envo.db
  #/home/mark/biosample_etc_database/envo.db
  #/home/mark/.data/oaklib/envo.db

# runoak descendants --help
  #Usage: runoak descendants [OPTIONS] [TERMS]...
  #
  #  List all descendants of a term
  #
  #  Example:
  #
  #      runoak -i sqlite:obo:obi descendants assay -p i
  #
  #  Example:
  #
  #      runoak -i sqlite:obo:uberon descendants heart -p i,p
  #
  #  This is the inverse of the 'ancestors' command; see the documentation for
  #  that command. But note that 'descendants' commands have the potential to be
  #  more "explosive" than ancestors commands, especially for high level terms,
  #  and for when predicates are not specified
  #
  #  Python API:
  #
  #     https://incatools.github.io/ontology-access-kit/interfaces/obograph
  #
  #Options:
  #  -p, --predicates TEXT           A comma-separated list of predicates. This
  #                                  may be a shorthand (i, p) or CURIE
  #  -M, --graph-traversal-method [HOP|ENTAILMENT]
  #                                  Whether formal entailment or graph walking
  #                                  should be used.
  #  -D, --display TEXT              A comma-separated list of display options.
  #                                  Use 'all' for all
  #  -O, --output-type TEXT          Desired output type
  #  -o, --output FILENAME           Output file, e.g. obo file
  #  --help                          Show this message and exit.

# runoak cache-ls
  #[pystow] ls -al /home/mark/.data/oaklib
  #total 1981452
  #drwxrwxr-x 2 mark mark       4096 May  3 20:57 .
  #drwxrwxr-x 4 mark mark       4096 Feb 16 11:08 ..
  #-rw-rw-r-- 1 mark mark    3637248 Mar 29 17:04 aio.db
  #-rw-rw-r-- 1 mark mark     775706 Mar 29 17:04 aio.db.gz
  #-rw-rw-r-- 1 mark mark  106467328 Feb 16 14:59 drugbank.db
  #-rw-rw-r-- 1 mark mark   19696744 Feb 16 14:59 drugbank.db.gz
  #-rw-rw-r-- 1 mark mark   77246464 May  3 20:57 envo.db
  #-rw-rw-r-- 1 mark mark   14895192 May  3 20:57 envo.db.gz
  #-rw-rw-r-- 1 mark mark  394846208 Feb 16 14:59 mesh.db
  #-rw-rw-r-- 1 mark mark   87556908 Feb 16 14:59 mesh.db.gz
  #-rw-rw-r-- 1 mark mark 1114869760 Feb 16 14:59 mondo.db
  #-rw-rw-r-- 1 mark mark  208981682 Feb 16 14:59 mondo.db.gz

# runoak --help
  #Usage: runoak [OPTIONS] COMMAND [ARGS]...
  #
  #  Run the oaklib Command Line.
  #
  #  A subcommand must be passed - for example: ancestors, terms, ...
  #
  #  Most commands require an input ontology to be specified:
  #
  #      runoak -i <INPUT SPECIFICATION> SUBCOMMAND <SUBCOMMAND OPTIONS AND
  #      ARGUMENTS>
  #
  #  Get help on any command, e.g:
  #
  #      runoak viz -h
  #
  #Options:
  #  -v, --verbose
  #  -q, --quiet / --no-quiet
  #  --stacktrace / --no-stacktrace  If set then show full stacktrace on error
  #                                  [default: no-stacktrace]
  #  --save-as TEXT                  For commands that mutate the ontology, this
  #                                  specifies where changes are saved to
  #  --autosave / --no-autosave      For commands that mutate the ontology, this
  #                                  determines if these are automatically saved
  #                                  in place  [default: no-autosave]
  #  --named-prefix-map TEXT         the name of a prefix map, e.g. obo, prefixcc
  #  --prefix TEXT                   prefix=expansion pair
  #  --metamodel-mappings TEXT       overrides for metamodel properties such as
  #                                  rdfs:label
  #  --import-depth INTEGER          Maximum depth in the import tree to
  #                                  traverse. Currently this is only used by the
  #                                  pronto adapter
  #  -g, --associations TEXT         Location of ontology associations
  #  -G, --associations-type TEXT    Syntax of associations input
  #  -l, --preferred-language TEXT   Preferred language for labels and lexical
  #                                  elements
  #  --other-languages TEXT          Additional languages for labels and lexical
  #                                  elements
  #  --requests-cache-db TEXT        If specified, all http requests will be
  #                                  cached to this sqlite file
  #  -W, --wrap-adapter TEXT         Wrap the input adapter using another adapter
  #                                  (e.g. llm or semsimian).
  #  -i, --input TEXT                input implementation specification. This is
  #                                  either a path to a file, or an ontology
  #                                  selector
  #  -I, --input-type TEXT           Input format. Permissible values vary
  #                                  depending on the context
  #  -a, --add TEXT                  additional implementation specification.
  #  --merge / --no-merge            Merge all inputs specified using --add
  #                                  [default: no-merge]
  #  --profile / --no-profile        If set, will profile the command  [default:
  #                                  no-profile]
  #  --help                          Show this message and exit.
  #
  #Commands:
  #  aliases                        List aliases for a term or set of terms.
  #  ancestors                      List all ancestors of a given term or...
  #  annotate                       Annotate a piece of text using a Named...
  #  apply                          Applies a patch to an ontology.
  #  apply-obsolete                 Sets an ontology element to be obsolete
  #  apply-taxon-constraints        Test candidate taxon constraints
  #  associations                   Lookup associations from or to entities.
  #  associations-counts            Count associations, grouped by subject...
  #  associations-matrix            Co-annotation matrix query.
  #  axioms                         Filters axioms
  #  cache-clear                    Clear the contents of the pystow oaklib...
  #  cache-ls                       List the contents of the pystow oaklib...
  #  definitions                    Show textual definitions for term or set...
  #  descendants                    List all descendants of a term
  #  diff                           Compute difference between two ontologies.
  #  diff-associations              Diffs two association sources.
  #  diff-terms                     Compares a pair of terms in two ontologies
  #  diff-via-mappings              Calculates cross-ontology diff using...
  #  disjoints                      Show all disjoints for a set of terms,...
  #  dump                           Exports (dumps) the entire contents of...
  #  enrichment                     Run class enrichment analysis.
  #  expand-subsets                 For each subset provide a mapping of...
  #  extract                        Extracts a sub-ontology.
  #  fill-table                     Fills missing values in a table of...
  #  generate-definitions           Generate definitions for a term or terms.
  #  generate-disjoints             Generate candidate disjointness axioms.
  #  generate-lexical-replacements  Generate lexical replacements based on a...
  #  generate-logical-definitions   Generate logical definitions based on...
  #  generate-synonyms              Generate synonyms based on a set of...
  #  info                           Show information on term or set of terms
  #  information-content            Show information content for term or...
  #  labels                         Show labels for term or list of terms
  #  languages                      Show available languages
  #  leafs                          List all leaf nodes in the ontology
  #  lexmatch                       Performs lexical matching between pairs...
  #  lint                           Lints an ontology, applying changes in...
  #  logical-definitions            Show all logical definitions for a term...
  #  mappings                       List all mappings encoded in the ontology
  #  migrate-curies                 Rewires an ontology replacing all...
  #  normalize                      Normalize all input identifiers.
  #  obsoletes                      Shows all obsolete entities.
  #  ontologies                     Shows all ontologies
  #  ontology-metadata              Shows ontology metadata
  #  ontology-versions              Shows ontology versions
  #  paths                          List all paths between one or more start...
  #  prefixes                       Shows prefix declarations.
  #  query                          Execute an arbitrary query.
  #  relationships                  Show all relationships for a term or terms
  #  rollup                         Produce an association rollup report.
  #  roots                          List all root nodes in the ontology
  #  search                         Searches ontology for entities that have...
  #  set-apikey                     Sets an API key
  #  siblings                       List all siblings of a specified term or...
  #  similarity                     All by all similarity.
  #  similarity-pair                Determine pairwise similarity between...
  #  singletons                     List all singleton nodes in the ontology
  #  statistics                     Shows all descriptive/summary statistics
  #  subsets                        Shows information on subsets
  #  synonymize                     Deprecated: use generate-synonyms
  #  taxon-constraints              Compute all taxon constraints for a term...
  #  term-categories                List categories for a term or set of terms.
  #  term-metadata                  Shows term metadata.
  #  term-subsets                   List subsets for a term or set of terms.
  #  terms                          List all terms in the ontology
  #  termset-similarity             Termset similarity.
  #  transform                      Transforms an ontology
  #  tree                           Display an ancestor graph as an...
  #  validate                       Validate an ontology against ontology...
  #  validate-definitions           Checks presence and structure of text...
  #  validate-mappings              Validates mappings in ontology using...
  #  validate-multiple              Validate multiple ontologies against...
  #  validate-synonyms              Validates synonyms in ontology using...
  #  viz

downloads/mixs.yaml:
	curl --request GET -sL \
	     --url 'https://raw.githubusercontent.com/GenomicsStandardsConsortium/mixs/main/src/mixs/schema/mixs.yaml'\
	     --output $@

assets/large_outputs/mixs-schemasheets-template.tsv: downloads/mixs.yaml # first four lines are headers
	$(RUN) linkml2schemasheets-template \
		--source-path $< \
		--output-path $@ \
		 --debug-report-path assets/large_outputs/mixs-schemasheets-template-debug.txt \
		 --log-file assets/large_outputs/mixs-schemasheets-template-log.txt \
		 --report-style concise
	head -n 4 $@ > $@.headers.tsv

assets/large_outputs/mixs-extensions-schemasheets-template.csv: assets/large_outputs/mixs-schemasheets-template.tsv
	cat $< | $(RUN) schemasheets-template-mixs-extensions-filter  > $@

#src/context_collaboration/schema/context_collaboration.yaml: examples/context_collaboration_template.tsv
#	$(RUN) schemauto generalize-tsv \
#		--class-name "LongTable" \
#		--enum-columns "agent" $< \
#		--enum-columns "mixs_context_label" \
#		--enum-columns "mixs_environment_label" \
#		--enum-threshold 0.5 \
#		--schema-name "context_collaboration_schema" \
#		--output $@ \

#examples/context_collaboration_template.yaml: src/context_collaboration/schema/context_collaboration.yaml examples/context_collaboration_template.tsv
#	$(RUN) linkml-convert \
#		--output $@ \
#		--schema $^


#assets/outputs/llm/claude-3-opus-20240229_2024-05-07T11_45_EDT/claude-3-opus-20240229_2024-05-07T11_45_EDT_combined.tsv: \
#src/context_collaboration/schema/context_collaboration.yaml \
#assets/outputs/llm/claude-3-opus-20240229_2024-05-07T11_45_EDT
#	$(RUN) linkml-convert \
#		--output $@ \
#		--schema $^
#
#assets/outputs/llm/claude-3-opus-20240229_2024-05-07T11_45_EDT/claude-3-opus-20240229_2024-05-07T11_45_EDT_attributed.json: \
#src/context_collaboration/schema/context_collaboration.yaml \
#assets/outputs/llm/claude-3-opus-20240229_2024-05-07T11_45_EDT
#	$(RUN) linkml-convert \
#		--output $@ \
#		--schema $^



assets/outputs/llm/claude-3-opus-20240229_2024-05-08T09_30_EDT/claude-3-opus-20240229_2024-05-08T09_30_EDT_invalids_attributed.json: \
src/context_collaboration/schema/context_collaboration.yaml \
assets/outputs/llm/claude-3-opus-20240229_2024-05-08T09_30_EDT/claude-3-opus-20240229_2024-05-08T09_30_EDT_invalids_attributed.tsv
	$(RUN) linkml-convert \
		--output $@ \
		--schema $^
