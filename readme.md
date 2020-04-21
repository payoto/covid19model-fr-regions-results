# covid19model-fr-regions-results

This dataset is a derivative work from the Imperial College Study 
[Estimating the number of infections and the impact of nonpharmaceutical interventions (NPI) on COVID-19 in 11 European countries](https://www.imperial.ac.uk/mrc-global-infectious-disease-analysis/covid-19/report-13-europe-npi-impact/).
This repository presents results for the forecasting of the COVID-19 epidemic at French regional level.

The goal of this dataset is to open the access to the result of our simulations, we encourage:

- Suggesting runs, to validate specific behaviours.
- Making visualisation of the data that illustrate reliability.
- Analysis of the performance and forecasting.

This dataset is part of the [data against covid-19](https://opencovid19.fr/)
citizens' initiative for open data and open source code around the COVID-19
pandemic.

Looking to contribute? Check the contributing section below on ways you can help
and then go to our [projects page](https://github.com/payoto/covid19model/projects)!

Codes to run the simulations in our [sister repository](https://github.com/payoto/covid19model).

This repository is also available on [Kaggle](https://www.kaggle.com/mrpayoto/covid19-icl-method-france-regions-results)

## Licenses

- Data (all `.csv` and `.png` files) in this repository are licensed under the [CC-BY-4.0 license](LICENSE-data).
- Code in this repository (all files except `.csv` and `.png`) in this repository are licensed under the [MIT License](LICENSE-code).

## Structure of data

- Data is stored in the `runs/` folder
- Each sub-directory is a "full" run (ran with flag `--full`: 4 chains with 4000 iterations and 2000 repetitions).
- `.csv` files describing the inputs are:
  - `<run name>-inputs-active_regions_ifr.csv` : List of regions considered and the country they are part of, and the IFR used. 
  - `<run name>-base-intervention.csv` : List of NPIs per region considered. 
  - `<run name>-inputs-distribution-parameters.csv` : Configuration of distributions governing transition from infection to hospital and death. 
- Data files describing the finale fitted parameters:
  - `<run name>-covars-alpha-reduction.csv` : Reduction of the `Rt` as a result of each considered NPI (see `.png` file for visualisation). 
  - `<run name>-final-rt.csv` : Final values of `Rt` for each simulation in each region (see `.png` file for visualisation). 
  - `<run name>-final-mu.csv` : Final deviation of `Rt` for each simulation in each region (see `.png` file for visualisation).
- `.csv` files describing the modelled time series and input data:
  - `<run name>-base-plot.csv` : Time series of the fitted data from start time-to simulation time, no forecast.
  - `<run name>-forecast-data.csv` : 7 days time series forecast for each region.

### Detailed descriptions

To come.

#### `-base-plot.csv` - model fit time series

- "" : index
- `"time"` : Date in format `yyyy-mm-dd`.
- `"country"` : Country.
- `"region"` : Geographical region in country.
- `"reported_cases"` : Official reported cases of COVID-19.
- `"reported_cases_c"` : Cumulated official reported cases of COVID-19.
- `"predicted_cases_c"` : Mean **predicted** cumulated cases of COVID-19.
- `"predicted_min_c"` :  Lower bound of the 95% confidence interval of **predicted**
cumulated cases of COVID-19 (0.025% band).
- `"predicted_max_c"` :  Upper bound of the 95% confidence interval of **predicted**
cumulated cases of COVID-19 (0.975% band).
- `"predicted_cases"` : Mean **predicted** daily cases of COVID-19.
- `"predicted_min"` : Lower bound of the 95% confidence interval of **predicted**
daily cases of COVID-19 (0.025% band).
- `"predicted_max"` : Upper bound of the 95% confidence interval of **predicted**
daily cases of COVID-19 (0.975% band).
- `"predicted_min2"` : Lower bound of the 50% confidence interval of **predicted**
daily cases of COVID-19 (0.25% band).
- `"predicted_max2"` : Upper bound of the 50% confidence interval of **predicted**
daily cases of COVID-19 (0.75% band).
- `"deaths"` : Official reported daily deaths of COVID-19.
- `"deaths_c"` : Official reported cumulated deaths of COVID-19.
- `"estimated_deaths_c"` : Mean **predicted** cumulated deaths from COVID-19.
- `"death_min_c"` : Lower bound of the 95% confidence interval of **predicted**
cumulated deaths of COVID-19 (0.025% band).
- `"death_max_c"` : Upper bound of the 95% confidence interval of **predicted**
cumulated deaths of COVID-19 (0.975% band).
- `"estimated_deaths"` :  Mean **predicted** daily deaths of COVID-19.
- `"death_min"` :  Lower bound of the 95% confidence interval of **predicted**
daily deaths of COVID-19 (0.025% band).
- `"death_max"` : Upper bound of the 95% confidence interval of **predicted**
daily deaths of COVID-19 (0.975% band).
- `"death_min2"` :  Lower bound of the 50% confidence interval of **predicted**
daily deaths of COVID-19 (0.25% band).
- `"death_max2"` : Upper bound of the 50% confidence interval of **predicted**
daily deaths of COVID-19 (0.75% band).
- `"rt"` : Mean estimated R_t, the total reproduction number of the disease.
- `"rt_min"` : Lower bound of the 95% confidence interval of R_t (0.025% band).
- `"rt_max"` : Upper bound of the 95% confidence interval of R_t (0.975% band).
- `"rt_min2"` : Lower bound of the 50% confidence interval of R_t (0.25% band).
- `"rt_max2"` : Upper bound of the 50% confidence interval of R_t (0.75% band).

Columns for deaths and cases are repeated here

| Column name            | source   | temporality   | Confidence Band | Description                     |
|------------------------|----------|---------------|-----------------|---------------------------------|
| `"reported_cases"`     | Official | daily         | real sample     | cases of COVID-19.              |
| `"reported_cases_c"`   | Official | cumulated     | real sample     | cases of COVID-19.              |
| `"predicted_cases_c"`  | modeled  | cumulated     | 50%             | cases of COVID-19.              |
| `"predicted_min_c"`    | modeled  | cumulated     | 0.025%          | cases of COVID-19.              |
| `"predicted_max_c"`    | modeled  | cumulated     | 0.975%          | cases of COVID-19.              |
| `"predicted_cases"`    | modeled  | daily         | 50%             | cases of COVID-19.              |
| `"predicted_min"`      | modeled  | daily         | 0.025%          | cases of COVID-19.              |
| `"predicted_max"`      | modeled  | daily         | 0.975%          | cases of COVID-19.              |
| `"predicted_min2"`     | modeled  | daily         | 0.25%           | cases of COVID-19.              |
| `"predicted_max2"`     | modeled  | daily         | 0.75%           | cases of COVID-19.              |
| `"deaths"`             | Official | daily         | real sample     | deaths of COVID-19.             |
| `"deaths_c"`           | Official | cumulated     | real sample     | deaths of COVID-19.             |
| `"estimated_deaths_c"` | modeled  | cumulated     | 50%             | deaths of COVID-19.             |
| `"death_min_c"`        | modeled  | cumulated     | 0.025%          | deaths of COVID-19.             |
| `"death_max_c"`        | modeled  | cumulated     | 0.975%          | deaths of COVID-19.             |
| `"estimated_deaths"`   | modeled  | daily         | 50%             | deaths of COVID-19.             |
| `"death_min"`          | modeled  | daily         | 0.025%          | deaths of COVID-19.             |
| `"death_max"`          | modeled  | daily         | 0.975%          | deaths of COVID-19.             |
| `"death_min2"`         | modeled  | daily         | 0.25%           | deaths of COVID-19.             |
| `"death_max2"`         | modeled  | daily         | 0.75%           | deaths of COVID-19.             |
| `"rt"`                 | modeled  | instantaneous | 50%             |  R_t  total reproduction number |
| `"rt_min"`             | modeled  | instantaneous | 0.025%          |  R_t  total reproduction number |
| `"rt_max"`             | modeled  | instantaneous | 0.975%          |  R_t  total reproduction number |
| `"rt_min2"`            | modeled  | instantaneous | 0.25%           |  R_t  total reproduction number |
| `"rt_max2"`            | modeled  | instantaneous | 0.75%           |  R_t  total reproduction number |


#### `-forecast-data.csv` - model forecast time series


## Using this data

## Example dataset and visualisation