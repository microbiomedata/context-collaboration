## Add your own custom Makefile targets here
RUN = poetry run
ENVO_OAKLIB = runoak -i sqlite:obo:envo
UBERGRAPH = https://ubergraph.apps.renci.org/sparql
NMDC_GRAPHDB = http://35.173.42.85/repositories
NMDC_GRAPHDB_ENVO = $(NMDC_GRAPHDB)/envo-2024-05-01

assets/outputs/oaklib/biomes.txt:
	$(RUN) $(ENVO_OAKLIB) descendants 'biome' > $@

assets/outputs/oaklib/environmental_materials.txt:
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


downloads/mixs.yaml:
	curl --request GET -sL \
	     --url 'https://raw.githubusercontent.com/GenomicsStandardsConsortium/mixs/main/src/mixs/schema/mixs.yaml'\
	     --output $@

local/mixs_environmental_extensions.yaml: downloads/mixs.yaml
	yq eval '.classes | with_entries(select(.value.is_a == "Extension"))' $< | cat > $@

local/mixs_environmental_extensions_keys.txt: local/mixs_environmental_extensions.yaml
	yq eval '. | keys | .[]' -r $< | cat > $@

downloads/obo_context.jsonld:
	curl --request GET -sL \
	     --url 'https://raw.githubusercontent.com/OBOFoundry/OBOFoundry.github.io/master/registry/obo_context.jsonld'\
	     --output $@

local/obo_context.yaml: downloads/obo_context.jsonld
	yq -P -o=yaml $<  | cat > $@

local/obo_context_keys.txt: local/obo_context.yaml
	yq eval '.["@context"] | keys | .[]' -r $< | cat > $@

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


#.PHONY: validation
#validation: src/context_collaboration/schema/context_collaboration.yaml cumulative_attributed_subset_mapping_including_invalids.tsv
#	$(RUN) linkml-validate \
#	--target-class LongTable \
#	--schema  $^

cumulative_attributed_subset_mapping_including_invalids.json: src/context_collaboration/schema/context_collaboration.yaml \
cumulative_attributed_subset_mapping_including_invalids.tsv
	$(RUN) linkml-convert \
		--validate \
		--output $@ \
		--schema $^

#inferences_from_cumulative.tsv:
#	$(RUN) expand-subset \
#		--min-confidence 0.9 \
#		--mixs-context-label env_broad_scale \
#		--mixs-context-label env_medium \
#		--mixs-environment-label Soil \
#		--mixs-environment-label Water \
#		--timezone EDT \
#		--tsv-input cumulative_attributed_subset_mapping_including_invalids.tsv \
#		--tsv-output $@

inferences_from_cumulative.tsv:
	$(RUN) expand-subset \
		--min-confidence 0.5 \
		--timezone EDT \
		--tsv-input cumulative_attributed_subset_mapping_including_invalids.tsv \
		--tsv-output $@

asserted_and_inferred_mappings.tsv: cumulative_attributed_subset_mapping_including_invalids.tsv inferences_from_cumulative.tsv
	$(RUN) concatenate-tsvs $^ \
		--output-file $@

asserted_and_inferred_mappings.json: src/context_collaboration/schema/context_collaboration.yaml asserted_and_inferred_mappings.tsv
	$(RUN) linkml-convert \
		--infer \
		--output $@ \
		--schema $^ \
		--validate

asserted_and_inferred_mappings_wide.tsv: asserted_and_inferred_mappings.tsv
	$(RUN) pivot-mappings-to-wide \
		--input-file $< \
		--output-file $@

.PHONY: inference-all inference-cleanup
inference-all: inference-cleanup long_from_wide.json
inference-cleanup:
	rm -f \
		asserted_and_inferred_mappings.json  \
		asserted_and_inferred_mappings.tsv \
		asserted_and_inferred_mappings_wide.tsv \
		inferences_from_cumulative.tsv \
		long_from_wide.json \
		long_from_wide.tsv \


long_from_wide.tsv: asserted_and_inferred_mappings_wide.tsv
	$(RUN) pivot-mappings-to-long \
		--input-file $< \
		--output-file $@


long_from_wide.json: src/context_collaboration/schema/context_collaboration.yaml long_from_wide.tsv
	$(RUN) linkml-convert \
		--infer \
		--output $@ \
		--schema $^ \
		--validate

non-food-non-org-selected-mat-ents-info.tsv:
	date && time $(RUN) runoak -i sqlite:obo:envo info \
		--output-type csv --output $@ --display all \
		[ .desc//p=i ENVO:01000813 .or .desc//p=i ENVO:01001813  .or .desc//p=i BFO:0000024  .or .desc//p=i ENVO:01000281  .or .desc//p=i ENVO:00003074   .or .desc//p=i RO:0002577 ] \
		.not [ .desc//p=i FOODON:00002403  ] # 11 minutes # may also want to exclude NCBITaxon:1 snd or some chemical entities from similar searches


examples/varied-training-minimal-comments.yaml: src/context_collaboration/schema/context_collaboration.yaml examples/varied-training-minimal-comments.tsv
	$(RUN) linkml-convert \
		--infer \
		--output $@ \
		--schema $^ \
		--validate


biome-labels.tsv:
	date && time $(RUN) runoak -i sqlite:obo:envo info --output-type csv --output $@ .desc//p=i 'biome'