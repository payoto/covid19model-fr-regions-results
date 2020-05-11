import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from . import custom_formatter
from . import plot_core

label_single_line_length = 40

def default_label_generator(country, data_string, date_label):
    
    country_label = f"{country} ({data_string} {date_label})"
    if len(country_label) > label_single_line_length:
        data_label = f"({data_string} {date_label})"
        if (
            len(country) <= label_single_line_length 
            and len(data_label) <= label_single_line_length
        ):
            country_label = country + "\n" + data_label
        else:
            print("Warning: Label too long, need to code contigency")
            country_label = country + "\n" + data_label

    return country_label

# plots the fatalities

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
        'estimated_deaths_forecast',
        'estimated_deaths_forecast_min',
        'estimated_deaths_forecast_max',
    ]
    plot_quantity = "Forecasted daily deaths"
    date_label = min(forecast_df["time"])
    
    if country_label is None:
        country_label = default_label_generator(country, "forecast from ", date_label)
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
        country_label = default_label_generator(country, "model to ", date_label)
    
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
        country_label = default_label_generator(country, "Reported deaths to ", date_label)
    
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

# plots the fatalities (cumulated)

def plot_all_deaths_forecast_country(
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
        'estimated_deaths_forecast_c',
        'estimated_deaths_forecast_min_c',
        'estimated_deaths_forecast_max_c',
    ]
    plot_quantity = "Forecasted daily deaths"
    date_label = min(forecast_df["time"])
    
    if country_label is None:
        country_label = default_label_generator(country, "forecast from ", date_label)
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


def plot_all_deaths_model_country(
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
        "estimated_deaths_c", "death_min_c", "death_max_c",
    ]
    plot_quantity = "Modelled total deaths"
    date_label = max(model_df["time"])
    country_field="region"
    if country_label is None:
        country_label = default_label_generator(country, "model to ", date_label)
    
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


def plot_all_deaths_report_country(
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
        "deaths_c",
    ]
    plot_quantity = "Reported total deaths"
    date_label = max(model_df["time"])
    country_field="region"
    if country_label is None:
        country_label = default_label_generator(country, "Reported deaths to ", date_label)
    
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


def plot_all_deaths_country(
    data_dict,
    country,
    *,
    ax=None,
    **kwargs
):
    if ax is None:
        fig, ax = plt.subplots()
    labels = ['', '', '']
    ax, labels[0] = plot_all_deaths_report_country(
        data_dict["modelling"], country, ax=ax, **kwargs
    )
    ax, labels[1] = plot_all_deaths_model_country(
        data_dict["modelling"], country, ax=ax, **kwargs
    )
    ax, labels[2] = plot_all_deaths_forecast_country(
        data_dict["forecasting"], country, ax=ax, **kwargs
    )
    plot_core.remove_confidence_interval_legend_labels(ax)
    return ax, labels 


# plots the cases

def plot_case_forecast_country(
    forecast_df,
    country,
    *,
    country_label=None,
    **kwargs
):
    """ Plots the forecasted daily cases with the 95% confidence interval.

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
        'estimated_cases_forecast',
        'estimated_cases_forecast_min',
        'estimated_cases_forecast_max',
    ]
    plot_quantity = "Forecasted daily deaths"
    date_label = min(forecast_df["time"])
    
    if country_label is None:
        country_label = default_label_generator(country, "forecast from ", date_label)
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


def plot_case_model_country(
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
        "predicted_cases", "predicted_min", "predicted_max",
    ]
    plot_quantity = "Modelled daily cases"
    date_label = max(model_df["time"])
    country_field="region"
    if country_label is None:
        country_label = default_label_generator(country, "model to ", date_label)
    
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


def plot_case_report_country(
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
        "reported_cases",
    ]
    plot_quantity = "Reported daily cases"
    date_label = max(model_df["time"])
    country_field="region"
    if country_label is None:
        country_label = default_label_generator(country, "Reported cases to ", date_label)
    
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


def plot_daily_cases_country(
    data_dict,
    country,
    *,
    ax=None,
    **kwargs
):
    if ax is None:
        fig, ax = plt.subplots()
    labels = ['', '', '']
    ax, labels[0] = plot_case_report_country(
        data_dict["modelling"], country, ax=ax, **kwargs
    )
    ax, labels[1] = plot_case_model_country(
        data_dict["modelling"], country, ax=ax, **kwargs
    )
    ax, labels[2] = plot_case_forecast_country(
        data_dict["forecasting"], country, ax=ax, **kwargs
    )
    plot_core.remove_confidence_interval_legend_labels(ax)
    return ax, labels 

# plot r_t

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
        country_label = default_label_generator(country, "model to ", date_label)
    
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
        country_label = default_label_generator(country, "forecast to ", date_label)
    
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

# Multiple countries
## Deaths
def plot_forecast_countries(*args, **kwargs):
    return plot_core.plot_timeseries_countries(plot_forecast_country, *args, **kwargs)


def plot_report_countries(*args, **kwargs):
    return plot_core.plot_timeseries_countries(plot_report_country, *args, **kwargs)


def plot_model_countries(*args, **kwargs):
    return plot_core.plot_timeseries_countries(plot_model_country, *args, **kwargs)

 
def plot_daily_deaths_countries(*args, **kwargs):
    return plot_core.plot_timeseries_countries(plot_daily_deaths_country, *args, **kwargs)

## Deaths
def plot_all_deaths_forecast_countries(*args, **kwargs):
    return plot_core.plot_timeseries_countries(plot_all_deaths_forecast_country, *args, **kwargs)


def plot_all_deaths_report_countries(*args, **kwargs):
    return plot_core.plot_timeseries_countries(plot_all_deaths_report_country, *args, **kwargs)


def plot_all_deaths_model_countries(*args, **kwargs):
    return plot_core.plot_timeseries_countries(plot_all_deaths_model_country, *args, **kwargs)

 
def plot_all_deaths_countries(*args, **kwargs):
    return plot_core.plot_timeseries_countries(plot_all_deaths_country, *args, **kwargs)

## R_t
def plot_Rt_countries(*args, **kwargs):
    return plot_core.plot_timeseries_countries(plot_Rt_country, *args, **kwargs)
 
def plot_Rt_forecast_countries(*args, **kwargs):
    return plot_core.plot_timeseries_countries(plot_Rt_forecast_country, *args, **kwargs)

## Cases
def plot_case_forecast_countries(*args, **kwargs):
    return plot_core.plot_timeseries_countries(plot_case_forecast_country, *args, **kwargs)


def plot_case_report_countries(*args, **kwargs):
    return plot_core.plot_timeseries_countries(plot_case_report_country, *args, **kwargs)


def plot_case_model_countries(*args, **kwargs):
    return plot_core.plot_timeseries_countries(plot_case_model_country, *args, **kwargs)

 
def plot_daily_cases_countries(*args, **kwargs):
    return plot_core.plot_timeseries_countries(plot_daily_cases_country, *args, **kwargs)



# Function comparisons and agregation
def compare_fatality_predictions(
    data_dict,
    **kwargs
):
    def compare_func(
        data_dict, plot_kwargs, country_list=None, ax=None, 
        plot_forecast=True
    ):
        # Plot the data (the reported data without any line, and with a marker every time)
        plot_report_countries(data_dict["modelling"], country_list=country_list,
            ax=ax, **plot_kwargs["report"])
        plot_model_countries(data_dict["modelling"], country_list=country_list,
            ax=ax, **plot_kwargs["model"])
        if plot_forecast:
            plot_forecast_countries(
                data_dict["forecasting"], 
                country_list=country_list,
                ax=ax, **plot_kwargs["forecast"]
            )

    return plot_core.compare_report_model_predictions(
        compare_func, data_dict, **kwargs)

def compare_all_fatality_predictions(
    data_dict,
    **kwargs
):
    def compare_func(
        data_dict, plot_kwargs, country_list=None, ax=None, 
        plot_forecast=True
    ):
        # Plot the data (the reported data without any line, and with a marker every time)
        plot_all_deaths_report_countries(data_dict["modelling"], country_list=country_list,
            ax=ax, **plot_kwargs["report"])
        plot_all_deaths_model_countries(data_dict["modelling"], country_list=country_list,
            ax=ax, **plot_kwargs["model"])
        if plot_forecast:
            plot_all_deaths_forecast_countries(
                data_dict["forecasting"], 
                country_list=country_list,
                ax=ax, **plot_kwargs["forecast"]
            )

    return plot_core.compare_report_model_predictions(
        compare_func, data_dict, **kwargs)

def compare_case_predictions(
    data_dict,
    **kwargs
):
    def compare_func(
        data_dict, plot_kwargs, country_list=None, ax=None, 
        plot_forecast=True
    ):
        # Plot the data (the reported data without any line, and with a marker every time)
        plot_case_report_countries(data_dict["modelling"], country_list=country_list,
            ax=ax, **plot_kwargs["report"])
        plot_case_model_countries(data_dict["modelling"], country_list=country_list,
            ax=ax, **plot_kwargs["model"])
        if plot_forecast:
            plot_case_forecast_countries(
                data_dict["forecasting"], 
                country_list=country_list,
                ax=ax, **plot_kwargs["forecast"])

    return plot_core.compare_report_model_predictions(
        compare_func, data_dict, **kwargs)

def compare_rt_and_interventions(
    data_dict,
    country_list=None,
    ax=None,
    prop_cycle=None,
    max_num_country_ci_display=3,
    plot_specific_kwargs={},
    plot_forecast=True,
    **kwargs
):
    marker_list=[',',',']
    if not plot_forecast:
        marker_list.pop(-1)
    if prop_cycle is None:
        # define a new property cycle to ensure the colour repeats correctly
        prop_cycle = plot_core.define_new_cycle(
            marker=marker_list, # which varies the marker
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
    if plot_forecast:
        plot_Rt_forecast_countries(
            data_dict["forecasting"], country_list=country_list,
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

def plot_zones_summary(zones, model_data):
    """Plots the summary for a zone or zones
    
    This summary plot has 5 plots, with daily and cumulated deaths
    as well as daily cases and reproduction number.
    """
    def put_legends_down(ax, ydown=-0.17):
        legends = [
            child for child in ax.get_children()
                if type(child) == type(ax.get_legend())
        ]
        for i, legend in enumerate(legends):
            legend.set_bbox_to_anchor((float(i) / float(len(legends)), ydown))
        
        return legends

    def correct_xticklabels(ax, disable_major):
        ax.xaxis.set_minor_locator(mdates.WeekdayLocator(interval=1))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
        if disable_major:
            ax.xaxis.set_major_formatter(mticker.NullFormatter())
        else:
            ax.xaxis.set_major_formatter(
                custom_formatter.PandasToMpl_ConciseDateFormatter(
                    mdates.MonthLocator(interval=1)
                )
            )
        ax.xaxis.set_minor_formatter(mticker.NullFormatter())
        # ax.xaxis.get_major_formatter()
        # ax.set_minor_locator(mdates.WeekdayLocator(interval=1))  
        # ugly_xtick_labels = ax.xaxis.get_major_formatter().format_ticks(ax.get_xticks())
        # ax.set_xticklabels([i.strip("\n") for i in ugly_xtick_labels])
    
    def correct_yticklabels(ax):
        y_tick_labels = []
        for i in ax.get_yticks():
            if i == float(0):
                lab = '0'
            elif abs(i)>4000:
                lab = f"{i/1000:.0f}"
            else:
                lab = f"{i/1000:.1f}"
            y_tick_labels.append(lab)
        ax.set_yticklabels(y_tick_labels)

    if type(zones) == type(str()):
        zones = [zones]

    axs = []
    fig = plt.figure(figsize=(15, 5))
    axs.append(fig.add_subplot(2,3,1))
    axs.append(fig.add_subplot(2,3,4))
    axs.append(fig.add_subplot(2,3,3))
    axs.append(fig.add_subplot(2,3,6))
    axs.append(fig.add_subplot(1,3,2))

    # Plot Fatalities
    ax = axs[0]
    compare_fatality_predictions(model_data, country_list=zones, ax=ax, verbose=False)
    ax.set_ylabel("Daily deaths")
    ax.get_legend().remove()
    ax.set_xlabel("")
    _, ymax = ax.get_ylim()
    # Plot Fatalities
    ax = axs[1]
    compare_fatality_predictions(model_data, country_list=zones, ax=ax, verbose=False)
    put_legends_down(ax, ydown=-0.34)
    ax.set_yscale('log')
    ymin, _ = ax.get_ylim()
    ax.set_ylim((0.5, ymax))
    ax.set_ylabel("Daily deaths (log scale)")

    plot_forecasts = True
    # Plot Rt and interventions
    ax = axs[2]
    compare_rt_and_interventions(
        model_data, country_list=zones, ax=ax, 
        verbose=False, plot_forecast=plot_forecasts)

    ax.minorticks_off()
    ax.set_xticklabels([])
    ax.tick_params(which='minor', label1On=False)
    ax.set_xlabel("")
    legends = put_legends_down(ax)
    for legend in legends:
        if ax.get_legend() != legend:
            legend.remove()
    plot_core.modify_legend(ax, loc='best')
    ax.set_ylabel("$R_t$")
    # Plot cases
    ax = axs[3]
    compare_case_predictions(
        model_data, country_list=zones, ax=ax, 
        verbose=False, plot_forecast=plot_forecasts)

    put_legends_down(ax, ydown=-0.34)
    ax.set_ylabel("Daily new cases (1000s)")
    correct_yticklabels(ax)
    
    # Cumulated deaths
    ax = axs[4]
    compare_all_fatality_predictions(
        model_data, country_list=zones, 
        ax=ax, verbose=False, plot_forecast=plot_forecasts)
    ax.set_ylabel("Total deaths (1000s)")
    put_legends_down(ax, ydown=-0.17)
    correct_yticklabels(ax)
    for ax, disable_major in zip(axs, [True, False, True, False, False]):
        correct_xticklabels(ax, disable_major=disable_major)

    return axs