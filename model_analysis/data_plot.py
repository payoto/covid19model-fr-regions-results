import pandas as pd
from matplotlib import pyplot as plt

def plot_forecast_country(
    forecast_df,
    country,
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
    active_columns, plot_quantity, date_label =\
        forecast_plot_specifiers(forecast_df)
    
    if country_label is None:
        country_label = f"{country} ({date_label})"
    
    print(f"Plotting forecast for {country_label}")
    return plot_timeseries_confidence_interval_country(
        forecast_df,
        active_columns, 
        plot_quantity, # y label of the plot
        country,
        country_label,
        **kwargs
    )

def forecast_plot_specifiers(forecast_df):
    active_columns = [
        col for col in forecast_df.columns if 'estimated_deaths' in col
    ]
    plot_quantity = "Forecasted daily deaths"
    date_label = min(forecast_df["time"])
    return (active_columns, plot_quantity, date_label)

def plot_timeseries_confidence_interval_country(
    forecast_df,
    active_columns,
    plot_quantity, # y label of the plot
    country,
    country_label=None,
    **kwargs
):
    """ Plots the time series of a confidence interval.

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

    # Compute the date field which is used as the x-axis
    forecast_df = enable_time_series_plot(
        forecast_df,
        timeseries_field_out='date'
    )

    if 'ax' in kwargs:
        ax_plot = kwargs['ax']
    else:
        ax_plot = plt

    color_arg = {}
    if 'color' in kwargs:
        color_arg['color'] = kwargs['color']

    line_color, = ax_plot.plot(forecast_df["date"].iloc[1],
        forecast_df[active_columns[0]].iloc[1],
        **color_arg
    )
    kwargs['color'] = line_color.get_color()
    line_color.remove()

    axis_est_deaths = forecast_df.loc[
        forecast_df["country"] == country
    ].plot(x="date", y=active_columns,  **kwargs)
    axis_est_deaths.set_ylabel(plot_quantity)
    # Formatting of the confidence interval lines to be dashed
    for line in axis_est_deaths.get_lines():
        if lower_ci_mark in line.get_label()\
            or upper_ci_mark in line.get_label():
            line.set_linestyle('--')
    axis_est_deaths.legend(handles=axis_est_deaths.get_lines())
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

def plot_forecast_countries(
    forecast_df, 
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
        axout, main_label = plot_forecast_country(
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