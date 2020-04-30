import pandas as pd
from matplotlib import pyplot as plt

# Collect the error behaviour of pandas when plotting an empty dataframe
error_pd_empty_plot = Exception()
try:
    pd.DataFrame().plot()
except Exception as e:
    error_pd_empty_plot = e
type(error_pd_empty_plot)

confidence_interval_format = {
    "linestyle": '--'
}

def get_next_color(ax_plot):
    """Utility which gets the next color in the axis `ax_plot` color cycle by
    adding and removing a dot at the centre of the plot."""
    x_min, x_max = ax_plot.get_xlim()
    y_min, y_max = ax_plot.get_ylim()
    line_color, = ax_plot.plot((x_min + x_max)/2, (y_min + y_max)/2)
    color_out = line_color.get_color() 
    line_color.remove()
    return color_out


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
        country (str) : a string corresponding to a country in the 

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
    print(f"Plotting forecast for {country_label}")
    return plot_timeseries_confidence_interval_country(
        forecast_df,
        active_columns,
        plot_quantity, # y label of the plot
        country,
        country_label=country_label,
        country_field=country_field,
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
    
    print(f"Plotting model for {country_label}")
    return plot_timeseries_confidence_interval_country(
        model_df,
        active_columns, 
        plot_quantity, # y label of the plot
        country,
        country_label=country_label,
        country_field=country_field,
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
    
    print(f"Plotting reports for {country_label}")
    return plot_timeseries_country(
        model_df,
        active_columns, 
        plot_quantity, # y label of the plot
        country,
        country_label=country_label,
        country_field=country_field,
        **kwargs
    )
    

def plot_timeseries_confidence_interval_country(
    forecast_df,
    active_columns,
    plot_quantity, # y label of the plot
    country,
    *,
    country_label=None,
    country_field="country",
    **kwargs
):
    """ Plots the time series of a confidence interval.

    Some pre and post processing of the function `plot_timeseries_country`

    Arguments:
        forecast_df (pd.Dataframe) : a data frame whic results from loading
        <run-name>-forecast-data.csv
        country (string) : a string corresponding to a country in the dataframe
        active_columns (list of string) : List of column names in the dataframe
            of size  specifying mean, and bounds of the confidence interval.
        plot_quantity (string) : A string to use as Y-label

    kwargs are passed to `pd.Dataframe.plot()`:
        color (str): A color hex string
        ax (plt.Axes) : An axis 
    """
    if country_label is None:
        country_label = country

    if len(active_columns)!=3:
        raise AttributeError(
            "A confidence interval must specify 3 columns: mean, and, lower "
            + "and upper bounds."
        )

    if 'label' not in kwargs:
        upper_ci_mark = '_upper_CI95'
        lower_ci_mark = '_lower_CI95'
        kwargs['label'] = [
            country_label,
            country_label + upper_ci_mark,
            country_label + lower_ci_mark
        ]
    elif len(kwargs['label']) == 3:
        upper_ci_mark = kwargs['label'][1]
        lower_ci_mark = kwargs['label'][2]
    else:
        AttributeError(
            "Label passed to `plot_forecast_country` should be of length 3")

    axis_est_deaths, _ = plot_timeseries_country(
        forecast_df,
        active_columns,
        plot_quantity,
        country,
        country_label=country_label,
        country_field=country_field,
        **kwargs
    )

    # Formatting of the confidence interval lines to be dashed
    for line in axis_est_deaths.get_lines():
        if lower_ci_mark in line.get_label()\
            or upper_ci_mark in line.get_label():
            for prop in confidence_interval_format:
                getattr(line,'set_' + prop)(confidence_interval_format[prop])
                # line.set_linestyle('--')
    axis_est_deaths.legend(handles=axis_est_deaths.get_lines())
    return axis_est_deaths, country_label


def plot_timeseries_country(
    forecast_df,
    active_columns,
    plot_quantity, # y label of the plot
    country,
    *,
    country_label=None,
    country_field="country",
    **kwargs
):
    if country_label is None:
        country_label = country

    if 'label' not in kwargs:
        if len(active_columns)==1:
            kwargs['label'] = [country_label]
        else:
            kwargs['label'] = [
                country_label + col for col in active_columns
            ]
    # Compute the date field which is used as the x-axis
    forecast_df = enable_time_series_plot(
        forecast_df,
        timeseries_field_out='date'
    )

    if 'ax' in kwargs:
        ax_plot = kwargs['ax']
    else:
        _, ax_plot = plt.subplots()
        kwargs['ax'] = ax_plot

    if 'color' not in kwargs:
        kwargs['color'] = get_next_color(ax_plot)
    
    try:
        # plot time series quantity
        axis_est_deaths = forecast_df.loc[
            forecast_df[country_field] == country
        ].plot(x="date", y=active_columns,  **kwargs)
    except type(error_pd_empty_plot) as errid:
        # If it is the error raised by pandas for an empty plot warn the user 
        # and early return otherwise raise the error
        if errid.args == error_pd_empty_plot.args:
            print(
                f"WARNING: Data for country {country_label} "
                + "not available in dataframe. skipping plot."
            )
            return ax_plot, country_label
        else:
            raise errid

    axis_est_deaths.set_ylabel(plot_quantity)
    return axis_est_deaths, country_label


def enable_time_series_plot(
    in_df, 
    timein_field='time', 
    timeseries_field_out='date', 
    date_format="%Y-%m-%d",
    ):
    """
    Small tool to add a field to a dataframe which can be used for time series
    plotting
    """
    if timeseries_field_out not in in_df.columns:
        in_df[timeseries_field_out] = pd.to_datetime(
            in_df[timein_field],
            format=date_format
        )
    return in_df


def plot_forecast_countries(*args, **kwargs):
    return plot_timeseries_countries(plot_forecast_country, *args, **kwargs)


def plot_model_countries(*args, **kwargs):
    return plot_timeseries_countries(plot_model_country, *args, **kwargs)


def plot_timeseries_countries(
    plot_timeseries_func,
    forecast_df, 
    *,
    country_list=None,
    color_cyle=[],
    max_date=None,
    min_date=None,
    ax=None,
    **kwargs
):

    if country_list is None:
        country_list = forecast_df['country'].unique()
    
    if ax is None:
        fig, ax = plt.subplots()
    try:
        label_list = [t.get_text() for t in ax.get_legend().texts]
    except AttributeError as identifier:
        label_list = []

    for country in country_list:
        # plot the country specific forecast
        axout, main_label = plot_timeseries_func(
            forecast_df, country,
            ax=ax, **kwargs)
        label_list.append(main_label)
    
    # Tailor axis limits
    x_min, x_max = pd.to_datetime(axout.get_xlim(), unit='D')
    if not (max_date is None):
        axout.set_xlim(right=min(x_max, pd.to_datetime(max_date)))
    if not (min_date is None):
        axout.set_xlim(left=max(x_min, pd.to_datetime(min_date)))
    # Select only mean lines to appear in legend
    line_legend = [l for l in axout.get_lines() if l.get_label() in label_list]
    axout.legend(handles=line_legend)
    
    return axout