# remove any existing owl files in the directory
rm *.owl

# copy dev ontology and imports into directory
cp ../data-source-ontology-dev.owl .
cp ../imports/*import.owl .

# since the robot.jar file is in the directory, calls to robot are made using the java -jar ./robot.jar command
# alternatively, you can call robot directly if your system is configured properly 
# for example, if the path to robot is in your PATH environment variable 
# you can perform merge by simple executing robot merge

# merge owl files
# you can also call robot merge ...; but I have placed the jar file in the directory
java -jar ./robot.jar merge \
  --inputs "*.owl" \
  --include-annotations true \
  --collapse-import-closure true \
  --output data-source-ontology-merged.owl
   
# # add date to IRI version; e.g.: http://purl.obolibrary.org/obo/2018-06-05/data-source-ontology.owl
java -jar ./robot.jar annotate \
  --input data-source-ontology-merged.owl \
  --ontology-iri "http://purl.data-source-translation.org/data-source-translation.owl" \
  --version-iri "http://purl.data-source-translation.org/`date '+%Y-%m-%d'`/data-source-translation.owl" \
  --output data-source-ontology-annotated.owl

# run reasoner on the ontology and add inferred axioms to final output
java -jar ./robot.jar reason \
	--input data-source-ontology-annotated.owl \
  --reasoner HermiT \
  --annotate-inferred-axioms true \
  --output data-source-ontology.owl

# clean up
# remove imports
rm *import.owl

# remove dev, merge, annotated temp ontologies
# comment out these lines if you wish to examine them
rm data-source-ontology-dev.owl
rm data-source-ontology-merged.owl
rm data-source-ontology-annotated.owl
