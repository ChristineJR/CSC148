Contents of the data directory:

demo.json
- example format of the configuration for a SchedulingExperiment
- used in the line simple_check('data/demo.json') in the main block
at the bottom of experiment.py
- also used in the line compare_algorithms('data/demo.json') in the main block
at the bottom of explore.py

map-data.txt
- sample file containing distances between cities
- referred to in demo.json
- used in a1_starter_tests and the calls to simple_check and compare_algorithms noted above

parcel-data-small.txt and truck-data-small.txt
- sample files containing parcels and trucks
- referred to in demo.json
- used in a1_starter_tests and the calls to simple_check and compare_algorithms noted above

demo-parcel-data.txt and demo-truck-data.txt
- these are regenerated with random parcel and truck data whenever you run
the provided generator.py
- they are not used in any of the provided starter code
