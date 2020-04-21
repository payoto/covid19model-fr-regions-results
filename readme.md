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

#### `-forecast-data.csv` - model forecast time series


## Using this data

## Example dataset and visualisation