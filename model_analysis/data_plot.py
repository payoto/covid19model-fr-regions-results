import pandas as pd
from matplotlib import pyplot as plt

def plot_forecast_country(forecast_df, country, country_label=None, **kwargs):
    """ Plots the forecasted daily deaths with the 95% confidence interval.

    Arguments:
        forecast_df (pd.Dataframe) : a data frame whic results from loading
        <run-name>-forecast-data.csv
        country (str) : a string corresponding to a country in the 

    kwargs are passed to `pd.Dataframe.plot()`:
        color (str): A color hex string
        ax (plt.Axes) : An axis 
    """
    if country_label is None:
        country_label = country

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

    # Select the active columns then plot the active rows.
    col_active = [
        col for col in forecast_df.columns if 'estimated_deaths' in col
    ]
    forecast_df = enable_time_series_plot(forecast_df)
    
    axis_est_deaths = forecast_df.loc[
        forecast_df["country"] == country
    ].plot(x="date", y=col_active,  **kwargs)

    axis_est_deaths.set_ylabel("Forecasted daily deaths")
    # Formatting of the confidence interval lines to be dashed
    for line in axis_est_deaths.get_lines():
        if lower_ci_mark in line.get_label()\
            or upper_ci_mark in line.get_label():
            line.set_linestyle('--')
    axis_est_deaths.legend(handles=axis_est_deaths.get_lines())
    return axis_est_deaths

def enable_time_series_plot(
    in_df, timein_field='time', time_out='date', date_format="%Y-%m-%d"):
    if time_out not in in_df.columns:
        in_df[time_out] = pd.to_datetime(
            in_df[timein_field],
            format=date_format
        )
    return in_df

def plot_forecast_countries(
    forecast_df, 
    country_list=None,
    color_cyle=None,
    max_date=None,
    min_date=None,
    **kwargs
):

    if country_list is None:
        country_list = forecast_df['country'].unique()
    if color_cyle is None:
        color_cyle = plt.rcParams['axes.prop_cycle']
    # Which properties of the cycler are not already specified in kwargs?
    active_cycle = {}
    for prop in color_cyle.by_key():
        active_cycle[prop] = not (prop in kwargs)

    if 'ax' not in kwargs:
        fig, kwargs['ax'] = plt.subplots()

    for country, properties in zip(country_list, color_cyle):
        # Cycle a plot property by passing it to kwargs if it was not overriden
        for prop in active_cycle:
            if active_cycle[prop]:
                kwargs[prop] = properties[prop]
        # plot the country specific forecast
        axout = plot_forecast_country(forecast_df, country, **kwargs)
    
    # Tailor axis limits
    x_min, x_max = pd.to_datetime(axout.get_xlim(), unit='D')
    if not (max_date is None):
        axout.set_xlim(right=min(x_max, pd.to_datetime(max_date)))
    if not (min_date is None):
        axout.set_xlim(left=max(x_min, pd.to_datetime(min_date)))
    # Select only mean lines to appear in legend
    line_legend = [l for l in axout.get_lines() if l.get_label() in country_list]
    axout.legend(handles=line_legend)
    
    return axout