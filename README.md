# waningve-covid-mys-2022-expansion
This repository contains files required to replicate the **vaccine effectiveness portion** in "Waning Effectiveness and Safety of Homologous Primary AZD1222, CoronaVac, and BNT162b2 Vaccines in the Adult Population in Malaysia", presented at the 16th Vaccine Congress 2022, Italy.

The repository contains the following.
1. Python scripts to estimate the AORs of SARS-CoV-2 infection, and the VE against severe COVID-19 outcomes (ICU admission, and death), by vaccine-combination-and-time-since-vaccination groups. These are in the main directory.
2. Anonymised, and cleaned, data vintages consolidated from various **nationally-comprehensive** administrative data sources in Malaysia's national COVID-19 surveillance system, and COVID-19 vaccination drive. These are in the ```Data``` folder.
3. Pre-compiled output files, including additional, more detailed, findings not presented at the congress, e.g., VE by age groups. These are in the ```Output``` folder.

## Data documentation
### Infection 
The base of this data set is the Malaysia Vaccine Administration System (MyVAS), which contains COVID-19 vaccination records, and demographics of every person who has received at least one dose of COVID-19 vaccines in Malaysia. These were matched deterministically using national IDs, and passport numbers, with the test data set, which records all supervised COVID-19 tests conducted in Malaysia, both antigen rapid tests (RTK-Ag) and Reverse Transcription Polyamerase Chain Reaction (RT-PCR) tests. Under Malaysian law, the reporting of COVID-19 outcomes are mandatory throughout the study period. These were further matched against data collected in Malaysia's QR code-based automated contact tracing system (AutoTrace), hosted on the national contact tracing application, MySejahtera, whose use is also legally mandated during the study period. After applying additional exclusion and inclusion rules, we are left with adults (aged 18+) who received their primary doses of COVID-19 vaccines (only homologous AZD1222, BNT162b2, or CoronaVac) between 21 July 2021 and 31 October 2021, and taken supervised COVID-19 tests between 1 November 2021 and 31 December 2021, but never tested positive before 1 November 2021, or received boosters (dose 3) before 1 January 2022.

The data vintage contains the following columns.
1. ```type_comb```: Type of vaccines received (aa = 2x AZD1222; pp = 2x BNT162b2; ss = 2x CoronaVac)
2. ```vaxtiming```: Timing of full vaccination, 14-days post-dose 2 (1 = first 4 weeks of 21 Jul - 31 Oct 2021; 2 = subsequent 4 weeks; 3 = ...; 4 = last group)
3. ```type_timing```: Strings concatenating ```type_comb``` and ```vaxtiming```
4. ```date1```: Date of first dose 
5. ```date2```: Date of second dose 
6. ```date3```: Date of third dose
7. ```date_test```: Date of first negative supervised COVID-19 test, or date of first positive supervised COVID-19 test (if ever tested positive)
8. ```type```: Type of COVID-19 test taken
9. ```result```: Result of COVID-19 test taken
10. ```dead```: Indicates if the individual died due to COVID-19 (evaluated by a clinical audit panel)
11. ```date_death```: Date of death due to COVID-19
12. ```private2```: Indicates if the second dose of the primary vaccination was privately purchased, instead of for free via the national vaccination programme
13. ```comorb```: Indicates presence of self-reported major comorbdities
14. ```age```: Age 
15. ```ethnicity```: Ethnicity (0 = Malay; 1 = Chinese; 2 = Indian; 3 = Sarawakian Native; 4 = Sabahan Native; 5 = other Natives; 6 = Indigeneous; 7 = Others)
16. ```male```: Sex 
17. ```frontliner```: Indicates if the individual is a healthcare worker (0 = general population; 1 = public sector; 2 = private sector)
18. ```state_id```: Indicates state of residence (1 to 14)
19. ```trace_count```: Indicates number of times the individual was identified as a contact of a COVID-19-positive individual (checked into the same place and same time as someone who tests positive by the end of the day) throughout 21 July 2021 and 31 October 2021
20: ```test_count```: Indicates number of times the individual had taken supervised COVID-19 tests throughout 21 July 2021 and 31 October 2021

### Severe outcomes
The base of this data set is the Confirmed COVID-19 Line Listing, which contains all confirmed COVID-19 cases in Malaysia, as well as demographic details. Reporting of COVID-19 outcomes, including test results, was legally mandated during the study period. These were matched deterministically using a unique case number to the COVID-19 Deaths Line Listing, which contains all deaths due to COVID-19 as evaluated by a clinical audit panel. Subsequently, the data set was matched using national IDs, and passport numbers, with the COVID-19 ICU Admissions Register. Finally, the data set was matched against the MyVAS for vaccination details, as well as the AutoTrace data set for a proxy of baseline SARS-CoV-2 exposure risk. After applying exclusion and inclusion rules, we are left with adults (aged 18+) with confirmed COVID-19-positive status between 1 November 2021 and 31 December 2021, received their primary doses of COVID-19 vaccines (only homologous AZD1222, BNT162b2, or CoronaVac) between 21 July 2021 and 31 October 2021, or never vaccinated until 31 December 2021. Moreover, the included subjects never tested positive before 1 November 2021, or received boosters (dose 3) before 1 January 2022.

The data vintage contains the following columns.
1. ```type_comb```: Type of vaccines received (aa = 2x AZD1222; pp = 2x BNT162b2; ss = 2x CoronaVac)
2. ```vaxtiming```: Timing of full vaccination, 14-days post-dose 2 (1 = first 7 weeks of 21 Jul - 31 Oct 2021; 2 = last 7 weeks)
3. ```type_timing```: Strings concatenating ```type_comb``` and ```vaxtiming```
4. ```vax_full```: Indicates in the individual was deemed fully vaccinated (14-days post-dose 2)
5. ```date1```: Date of first dose 
6. ```date2```: Date of second dose 
7. ```fullvaxweek```: Week of the year 2021 when the individual was deemed fully vaccinated (14-days post-dose 2)
8. ```date_lab```: Date of confirmatory test for COVID-19-positive status
9. ```dead```: Indicates if the individual died due to COVID-19 (evaluated by a clinical audit panel)
10. ```date_death```: Date of death due to COVID-19
11. ```icu```: Indicates if the individual was admitted into the COVID-19 ICU ward
12. ```comorb```: Indicates presence of self-reported major comorbdities
13. ```age```: Age 
14. ```malaysian```: Nationality
15. ```male```: Sex 
16. ```frontliner```: Indicates if the individual is a healthcare worker (0 = general population; 1 = public sector; 2 = private sector)
17. ```state_id```: Indicates state of residence (1 to 14)
18. ```trace_count```: Indicates number of times the individual was identified as a contact of a COVID-19-positive individual (checked into the same place and same time as someone who tests positive by the end of the day) throughout 21 July 2021 and 31 October 2021
19: ```traced```: Indicates if the individual was ever identified as a contact of a COVID-19-positive individual

## Replication guide

1. ```git clone suahjl/waningve-covid-mys-2022-expansion```
2. ```pip install requirements.txt```
3. ```aor_infection```
4. ```ve_severe```