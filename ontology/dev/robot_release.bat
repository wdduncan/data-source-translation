REM this bat file must be in the dev directory to work properly
REM remove any existing owl files in the directory
@echo off
cd build
del *.owl
cd ..

REM copy dev ontology and imports into directory
copy data-source-ontology-dev.owl ..\build

cd imports
for %%a in (*import.owl) do copy "%%a" ..\build
cd ../build
REM since the robot.jar file is in the directory, calls to robot are made using the java -jar ./robot.jar command
REM alternatively, you can call robot directly if your system is configured properly 
REM for example, if the path to robot is in your PATH environment variable 
REM you can perform merge by simple executing robot merge

REM merge owl files
"%JAVA_HOME%\bin\java.exe" -jar ..\robot.jar merge^
  --inputs "*.owl"^
  --include-annotations true^
  --collapse-import-closure true^
  --output data-source-ontology-merged.owl
   
REM REM add date to IRI version; e.g.: http://purl.obolibrary.org/obo/2018-06-05/data-source-ontology.owl
"%JAVA_HOME%\bin\java.exe" -jar ..\robot.jar annotate^
  --input data-source-ontology-merged.owl^
  --ontology-iri "http://purl.data-source-translation.org/data-source-translation.owl"^
  --version-iri "http://purl.data-source-translation.org/%date:~-4,4%%date:~-7,2%%date:~-10,2%/data-source-translation.owl"^
  --output data-source-ontology-annotated.owl

REM run reasoner on the ontology and add inferred axioms to final output
"%JAVA_HOME%\bin\java.exe" -jar ..\robot.jar reason^
	--input data-source-ontology-annotated.owl^
  --reasoner HermiT^
  --annotate-inferred-axioms true^
  --output data-source-ontology.owl

REM clean up
REM remove imports
for %%a in (*import.owl) do del "%%a"

REM remove dev, merge, annotated temp ontologies
REM comment out these lines if you wish to examine them
del data-source-ontology-dev.owl
del data-source-ontology-merged.owl
del data-source-ontology-annotated.owl

cd ..
@echo on