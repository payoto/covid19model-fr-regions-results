import pandas as pd
from matplotlib import pyplot as plt

from . import plot_core

def axis_date_limits(ax, min_date=None, max_date=None):
    # Tailor axis limits
    x_min, x_max = pd.to_datetime(ax.get_xlim(), unit='D')
    if not (max_date is None):
        ax.set_xlim(right=min(x_max, pd.to_datetime(max_date)))
    if not (min_date is None):
        ax.set_xlim(left=max(x_min, pd.to_datetime(min_date)))

# plots the 

def plot_forecast_country(
    forecast_df,
    country,
    *,
    country_label=None,
    **kwargs
):
    """ Plots the forecasted daily deaths with the 95% confidence interval.

    Arguments:
        forecast_df (pd.Dataframe) : a data frame whic results from loading
        <run-name>-forecast-data.csv
        country (str) : a string corresponding to a country or geographical zone
        in the data.
    
    Keyword Arguments:
        country_label (str) : The label to use in the data
        **kwargs: Keyword arguments are passed to (in order of precedence):
            - `plot_core.plot_timeseries_confidence_interval_country`
            - `pd.Dataframe.plot`
            - `pyplot.plot`

    Example extra keyword args are: color, ax, 

    kwargs are passed to `pd.Dataframe.plot()`:
        color (str): A color hex string
        ax (plt.Axes) : An axis 
    """
    # Select the active columns
    active_columns = [
        col for col in forecast_df.columns if 'estimated_deaths' in col
    ]
    plot_quantity = "Forecasted daily deaths"
    date_label = min(forecast_df["time"])
    
    if country_label is None:
        country_label = f"{country} (forecast from {date_label})"
    country_field = "country"

    return plot_core.plot_timeseries_confidence_interval_country(
        forecast_df,
        active_columns,
        plot_quantity, # y label of the plot
        country,
        country_label=country_label,
        country_field=country_field,
        timeseries_type="forecast",
        **kwargs
    )


def plot_model_country(
    model_df,
    country,
    *,
    country_label=None,
    **kwargs
):
    """ Plots the forecasted daily deaths with the 95% confidence interval.

    Arguments:
        model_df (pd.Dataframe) : a data frame whic results from loading
        <run-name>-forecast-data.csv
        country (str) : a string corresponding to a country in the 

    kwargs are passed to `pd.Dataframe.plot()`:
        color (str): A color hex string
        ax (plt.Axes) : An axis 
    """
    # Select the active columns
    active_columns = [
        "estimated_deaths", "death_min", "death_max",
    ]
    plot_quantity = "Modelled daily deaths"
    date_label = max(model_df["time"])
    country_field="region"
    if country_label is None:
        country_label = f"{country} (model to {date_label})"
    
    return plot_core.plot_timeseries_confidence_interval_country(
        model_df,
        active_columns, 
        plot_quantity, # y label of the plot
        country,
        country_label=country_label,
        country_field=country_field,
        timeseries_type="model",
        **kwargs
    )


def plot_report_country(
    model_df,
    country,
    *,
    country_label=None,
    **kwargs
):
    """ Plots the forecasted daily deaths with the 95% confidence interval.

    Arguments:
        model_df (pd.Dataframe) : a data frame whic results from loading
        <run-name>-forecast-data.csv
        country (str) : a string corresponding to a country in the 

    kwargs are passed to `pd.Dataframe.plot()`:
        color (str): A color hex string
        ax (plt.Axes) : An axis 
    """
    # Select the active columns
    active_columns = [
        "deaths",
    ]
    plot_quantity = "Reported daily deaths"
    date_label = max(model_df["time"])
    country_field="region"
    if country_label is None:
        country_label = f"{country} (Reported deaths to {date_label})"
    
    return plot_core.plot_timeseries_country(
        model_df,
        active_columns, 
        plot_quantity, # y label of the plot
        country,
        country_label=country_label,
        country_field=country_field,
        timeseries_type="reports",
        **kwargs
    )


def plot_daily_deaths_country(
    data_dict,
    country,
    *,
    ax=None,
    **kwargs
):
    if ax is None:
        fig, ax = plt.subplots()
    labels = ['', '', '']
    ax, labels[0] = plot_report_country(
        data_dict["modelling"], country, ax=ax, **kwargs
    )
    ax, labels[1] = plot_model_country(
        data_dict["modelling"], country, ax=ax, **kwargs
    )
    ax, labels[2] = plot_forecast_country(
        data_dict["forecasting"], country, ax=ax, **kwargs
    )
    plot_core.remove_confidence_interval_legend_labels(ax)
    return ax, labels 


def plot_Rt_country(
    model_df,
    country,
    *,
    country_label=None,
    **kwargs
):
    """ Plots Rt (the epidemic reproduction number) with the 95% confidence
    interval.

    Arguments:
        model_df (pd.Dataframe) : a data frame which results from loading
        <run-name>-forecast-data.csv
        country (str) : a string corresponding to a country in the 

    kwargs are passed to `pd.Dataframe.plot()`:
        color (str): A color hex string
        ax (plt.Axes) : An axis 
    """
    # Select the active columns
    active_columns = [
        "rt", "rt_min", "rt_max",
    ]
    plot_quantity = "Inferred $R_t$"
    date_label = max(model_df["time"])
    country_field="region"
    if country_label is None:
        country_label = f"{country} (model to {date_label})"
    
    return plot_core.plot_timeseries_confidence_interval_country(
        model_df,
        active_columns, 
        plot_quantity, # y label of the plot
        country,
        country_label=country_label,
        country_field=country_field,
        timeseries_type="Inferred R(t)",
        **kwargs
    )

def plot_Rt_forecast_country(
    model_df,
    country,
    *,
    country_label=None,
    **kwargs
):
    """ Plots Rt (the epidemic reproduction number) with the 95% confidence
    interval.

    Arguments:
        model_df (pd.Dataframe) : a data frame which results from loading
        <run-name>-forecast-data.csv
        country (str) : a string corresponding to a country in the 

    kwargs are passed to `pd.Dataframe.plot()`:
        color (str): A color hex string
        ax (plt.Axes) : An axis 
    """
    # Select the active columns
    active_columns = [
        "rt", "rt_min", "rt_max",
    ]
    plot_quantity = "Forecast $R_t$"
    date_label = min(model_df["time"])
    country_field="country"
    if country_label is None:
        country_label = f"{country} (forecast to {date_label})"
    
    return plot_core.plot_timeseries_confidence_interval_country(
        model_df,
        active_columns, 
        plot_quantity, # y label of the plot
        country,
        country_label=country_label,
        country_field=country_field,
        timeseries_type="Forecast R(t)",
        **kwargs
    )


def plot_forecast_countries(*args, **kwargs):
    return plot_core.plot_timeseries_countries(plot_forecast_country, *args, **kwargs)


def plot_report_countries(*args, **kwargs):
    return plot_core.plot_timeseries_countries(plot_report_country, *args, **kwargs)


def plot_model_countries(*args, **kwargs):
    return plot_core.plot_timeseries_countries(plot_model_country, *args, **kwargs)

 
def plot_daily_deaths_countries(*args, **kwargs):
    return plot_core.plot_timeseries_countries(plot_daily_deaths_country, *args, **kwargs)


def plot_Rt_countries(*args, **kwargs):
    return plot_core.plot_timeseries_countries(plot_Rt_country, *args, **kwargs)
 
def plot_Rt_forecast_countries(*args, **kwargs):
    return plot_core.plot_timeseries_countries(plot_Rt_forecast_country, *args, **kwargs)


def compare_fatality_predictions(
    data_dict,
    country_list=None,
    ax=None,
    prop_cycle=None,
    max_num_country_ci_display=3,
    plot_specific_kwargs={},
    **kwargs
):
    if prop_cycle is None:
        # define a new property cycle to ensure the colour repeats correctly
        prop_cycle = plot_core.define_new_cycle(
            marker=['o',',',','], # which varies the marker
            color_frequency=len(country_list), # the same colour repeats every len(country_list) lines
            markevery=[5],  # Markers are plotted every 5 days
        )
    if ax is None:
        _, ax = plt.subplots()
        ax.set_prop_cycle(prop_cycle)
    
    # Get the correct precedence of keyword args
    plot_kwargs = {
        "report": {'linestyle':'', 'markevery':1, 'marker': 'o'},
        "model": {},
        "forecast": {'linestyle':'--'},
    }
    for plot in plot_kwargs:
        for kwarg in kwargs:
            plot_kwargs[plot][kwarg] = kwargs[kwarg]
    for plot in plot_specific_kwargs:
        for kwarg in plot_specific_kwargs[plot]:
            plot_kwargs[plot][kwarg] = plot_specific_kwargs[plot][kwarg]

    # Plot the data (the reported data without any line, and with a marker every time)
    plot_report_countries(data_dict["modelling"], country_list=country_list,
        ax=ax, **plot_kwargs["report"])
    plot_model_countries(data_dict["modelling"], country_list=country_list,
        ax=ax, **plot_kwargs["model"])
    plot_forecast_countries(data_dict["forecasting"], country_list=country_list,
        ax=ax, **plot_kwargs["forecast"])

    # For clarity we remove the confidence intervals and the move the legend out
    if max_num_country_ci_display >= len(country_list):
        plot_core.remove_confidence_interval_legend_labels(ax)
    else:
        plot_core.remove_confidence_interval_lines(ax)

    plot_core.modify_legend(ax, bbox_to_anchor=(1.04, 1.0), loc='upper left')
    return ax

def compare_rt_and_interventions(
    data_dict,
    country_list=None,
    ax=None,
    prop_cycle=None,
    max_num_country_ci_display=3,
    plot_specific_kwargs={},
    **kwargs
):
    if prop_cycle is None:
        # define a new property cycle to ensure the colour repeats correctly
        prop_cycle = plot_core.define_new_cycle(
            marker=[',',','], # which varies the marker
            color_frequency=len(country_list), # the same colour repeats every len(country_list) lines
            markevery=[5],  # Markers are plotted every 5 days
        )
    if ax is None:
        _, ax = plt.subplots()
        ax.set_prop_cycle(prop_cycle)
    
    # Get the correct precedence of keyword args
    plot_kwargs = {
        "interventions": {},
        "model": {},
        "forecast": {'linestyle':'--'},
    }
    for plot in plot_kwargs:
        for kwarg in kwargs:
            plot_kwargs[plot][kwarg] = kwargs[kwarg]
    for plot in plot_specific_kwargs:
        for kwarg in plot_specific_kwargs[plot]:
            plot_kwargs[plot][kwarg] = plot_specific_kwargs[plot][kwarg]

    # Plot the data (the reported data without any line, and with a marker every time)
    plot_Rt_countries(data_dict["modelling"], country_list=country_list,
        ax=ax, **plot_kwargs["model"])
    plot_Rt_forecast_countries(data_dict["forecasting"], country_list=country_list,
        ax=ax, **plot_kwargs["forecast"])
    

    # For clarity we remove the confidence intervals and the move the legend out
    if max_num_country_ci_display >= len(country_list):
        plot_core.remove_confidence_interval_legend_labels(ax)
    else:
        plot_core.remove_confidence_interval_lines(ax)

    plot_core.modify_legend(ax, bbox_to_anchor=(1.04, 1.0), loc='upper left')
    plot_core.plot_interventions_countries(
        data_dict["interventions"], country_list, ax=ax, **plot_kwargs["interventions"])

    return ax
