Super basic method of viewing the knowledgebase csvs coming out of the Cosmos pipeline.

Allows filtering by document, bbox type, and term of interest (currently searching `target_img_path`)



## Usage

```
PG_CONN_STR="postgresql://postgres:@localhost:54321/cosmos_figs" ./setup.sh # imports the csvs in ./output
PG_CONN_STR="postgresql://postgres:@localhost:54321/cosmos_figs" python server.py # runs the app, available at localhost:8051
```

## Current assumptions:
- the image paths as stored in the csv/db are relative to working dir 
- the csv outputs of interest are in ./output/
- an externally running postgres setup, with database created. Connection string is passed in at runtime:


