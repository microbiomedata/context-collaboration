* claude-3-opus-20240229
* 2024-05-07T17:00 EDT
* 581f0d1c-63c0-47b1-a108-76c29a28f709

----

* src/context_collaboration/schema/context_collaboration.yaml (schema)
* examples/context_collaboration_template.yaml (examples)
* sparql queries
    * assets/queries/sparql/environmental_material_annotations.rq
    * assets/queries/sparql/environmental_material_relations_pivot.rq
* sparql results
    * assets/outputs/sparql/environmental_material_merged.csv

Processed:
* Agriculture
* BuiltEnvironment
* Air
* HydrocarbonResourcesCores
* HydrocarbonResourcesFluidsSwabs
* Soil
* Water
* HostAssociated
* MicrobialMatBiofilm
* MiscellaneousNaturalOrArtificialEnvironment
* PlantAssociated
* Sediment

Skipped (contain "food" or "human" in the label):
* FoodAnimalAndAnimalFeed
* FoodFarmEnvironment
* FoodFoodProductionFacility
* FoodHumanFoods
* HumanAssociated
* HumanGut
* HumanOral
* HumanSkin
* HumanVaginal

Remaining to be processed:
* SymbiontAssociated
* WastewaterSludge



are there any ontology classes that you want to map to env_medium and any mixs_environment_label that you haven't ahd a chance to do yet? if so, you can start emitting them now in a single JSON structure. don't repeat any mappings you have already done.
