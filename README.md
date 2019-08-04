# General Information

## Principles
- Allow showing data across multiple countries
- Allow showing data at different levels of detail
- Allow data to be shown for a single country
  - Data should be showable using the local boundary type (eg 'Village')


## Quick summary
Data in a csv should look like one of these:

*Mapping data across multiple countries at the first Sub-Country level*

| SC1_CODE      | Country        | Avg Income |
| ------------- | -------------- | -----------|
| ASM-1         | American Samoa | $100       | 
| ...           | ...            | ...        |
| FJI-1         | Fiji           | $300       |


*Mapping data in American Samoa at the first Sub-Country (SC1) level*

| ASM_SC1_CODE     | Country        | Avg Income |
| ---------------- | -------------- | -----------|
| ASM-1            | American Samoa | $100       | 
| ...              | ...            | ...        |
| ASM-2            | American Samoa | $300       |


*Mapping data in American Samoa at the District level*

| ASM_DISTRICT_CODE | Country        | Avg Income |
| ----------------- | -------------- | -----------|
| ASM-1             | American Samoa | $100       | 
| ...               | ...            | ...        |
| ASM-2             | American Samoa | $300       |



# Available Layers
- Within PacificMap there are a number of layers which can be used for showing data against different regions
  - Country (EEZ)
  - Sub-Country 1 [more details](/subCountry1)
  - Sub-Country 2 [more details](/subCountry2)
  - Sub-Country 3 [more details](/subCountry3)
- The Sub-Country layers are an amalgamation of boundaries that approximately equivalent across countries


Valid names can be
- `SC1_CODE` (for non-country-specfic)
- {ISO3}_SC1_CODE eg `ASM_SC1_CODE` for Sub-Country 1 Codes in American Samoa.
- {ISO3}_{LOCAL ADMIN NAME}_CODE eg `ASM_DISTRICT_CODE` for districts (AL2) in American Samoa.
