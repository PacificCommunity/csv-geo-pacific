## General description
Combines data from multiple sources into a cohesive datasets

## Goals
1. Enable users to visually enable data across multiple counties
2. Enable users to visually enable data in a single country

## What will work
Imagine we have a csv containing average household income at the Admin Level 2 for all countries

| AL2_NAME      | Country        | Avg Income |
| ------------- | -------------- | -----------|
| Sua           | American Samoa | $100       | 
| ...           | ...            | ...        |
| Hihifo        | Tonga          | $300       |


Or perhaps we just have average household income at the Admin Level 2 (COUNTY) in American Samoa

| ASM_COUNTY_NAME  | Country        | Avg Income |
| ---------------- | -------------- | -----------|
| Sua              | American Samoa | $100       | 
| ...              | ...            | ...        |
| Ituau            | American Samoa | $300       |

Valid names can be
- AL2_NAME (for non-country-specfic).
- AL2_CODE (for non-country-specfic).
- {ISO3}_AL2_NAME eg `ASM_AL2_NAME` for Administrative Level 2 Names in American Samoa.
- {ISO3}_AL2_CODE eg `ASM_AL2_CODE` for Administrative Level 2 Codes in American Samoa.
- {ISO3}_{LOCAL ADMIN NAME}_NAME eg `ASM_COUNTY_NAME` for counties (AL2) in American Samoa.
- {ISO3}_{LOCAL ADMIN NAME}_CODE eg `ASM_COUNTY_CODE` for counties (AL2) in American Samoa.


Or perhaps we want to use Admin Level 3 codes in Tonga.
When using codes we need to make sure they are prefixed by the Country ISO3 Code

| TON_AL3_CODE | Village Name | Country  | Avg Income |
| ------------ | ------------ | -------- | -----------|
| TON1709      | 'Ahau        | Tonga    | $100       | 
| ...          | ...          | ...      | ...        |
| TON1110      | 'Ataa        | Tonga    | $300       |