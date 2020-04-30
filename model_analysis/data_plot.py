import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.rcsetup import cycler


# Marks a confidence interval
_ci_mark = "CI_"

# Collect the error behaviour of pandas when plotting an empty dataframe
error_pd_empty_plot = Exception()
try:
    pd.DataFrame().plot()
except Exception as e:
    error_pd_empty_plot = e
type(error_pd_empty_plot)

confidence_interval_format = {
    "linestyle": '--',
    "marker": '',
}
default_color_cycle = plt.rcParams['axes.prop_cycle']
# Defines extensions to matplotlib for convenience

def get_next_color(
    ax_plot,
    properties=['color', 'linestyle', 'marker', 'markersize','linewidth',
                'markevery']
    ):
    """Utility which gets the next color in the axis `ax_plot` color cycle by
    adding and removing a dot at the centre of the plot."""
    x_min, x_max = ax_plot.get_xlim()
    y_min, y_max = ax_plot.get_ylim()
    line_color, = ax_plot.plot((x_min + x_max)/2, (y_min + y_max)/2)
    dict_out = {
            prop: getattr(line_color, 'get_'+prop)() for prop in properties
        }
    line_color.remove()
    return dict_out

def get_confidence_interval_lines(ax):
    ci_lines = []
    for line in ax.get_lines():
        if _ci_mark in line.get_label():
            is_ci_line = True
            for prop in confidence_interval_format:
                is_ci_line &= (
                    getattr(line,'get_' + prop)() 
                    == confidence_interval_format[prop]
                )
            if is_ci_line:
                ci_lines.append(line)
    return ci_lines

def remove_confidence_interval_lines(ax):
    for line in get_confidence_interval_lines(ax):
        line.remove()

def remove_confidence_interval_legend_labels(ax):
    ci_lines = get_confidence_interval_lines(ax)
    line_legend = [l for l in ax.get_lines() if l not in ci_lines]
    ax.legend(handles=line_legend)

def modify_legend(ax, **kwargs):
    label_list = [t.get_text() for t in ax.get_legend().get_texts()]
    handles, labels = ax.get_legend_handles_labels()
    copy_handles = []
    copy_labels = []
    for handle, label in zip(handles, labels):
        if label in label_list:
            copy_handles.append(handle)
            copy_labels.append(label)
    ax.legend(handles=copy_handles, labels=copy_labels, **kwargs)

def axis_date_limits(ax, min_date=None, max_date=None):
    # Tailor axis limits
    x_min, x_max = pd.to_datetime(ax.get_xlim(), unit='D')
    if not (max_date is None):
        ax.set_xlim(right=min(x_max, pd.to_datetime(max_date)))
    if not (min_date is None):
        ax.set_xlim(left=max(x_min, pd.to_datetime(min_date)))

def define_new_cycle(
    color_period=None,
    color_frequency=None,
    color_cycle=default_color_cycle,
    marker=[',', 'o', 'v', '+', 'x'],
    **kwargs
    ):

    if (color_frequency is not None) and (color_period is not None):
        raise AttributeError("Only a color period or frequency may be set")

    style_cycles = {
        'marker': marker,
        **kwargs
    }
    prop_cycle = 1 # plt.rcParams['axes.prop_cycle']
    for prop in style_cycles:
        tmp = {}
        tmp[prop] = style_cycles[prop]
        prop_cycle = prop_cycle * cycler(**tmp)

    if  color_period is not None:
        dict_props = {prop: [] for prop in style_cycles}
        for i, props in zip(range(color_period), prop_cycle):
            for prop in props:
                dict_props[prop].append(props[prop])
    
    
    if color_frequency is not None:
        color_cycle = cycler(color=color_cycle.by_key()['color'][:color_frequency])

    if (color_frequency is None) and (color_period is None):
        prop_cycle_sized = color_cycle * prop_cycle
    elif (color_period is not None) and (color_period > 1):
        prop_cycle_sized = color_cycle * cycler(**dict_props)
    elif (color_frequency is not None) and (color_frequency > 1):
        prop_cycle_sized = prop_cycle * color_cycle
    elif  color_period == 1 or color_frequency==1:
        prop_cycle_sized = color_cycle 
    else:
        raise AttributeError(
            f"`color_period` cannot be {color_period}, must be >=1 or None"
        )

    return prop_cycle_sized

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
    remove_confidence_interval_legend_labels(ax)
    return ax, labels 

def plot_timeseries_confidence_interval_country(
    forecast_df,
    active_columns,
    plot_quantity, # y label of the plot
    country,
    *,
    country_label=None,
    country_field="country",
    confidence_bound=95,
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
        upper_ci_mark = f'_upper_{_ci_mark}{confidence_bound}'
        lower_ci_mark = f'_lower_{_ci_mark}{confidence_bound}'
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
    custom_format_cycle=[],
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
        forecast_df, timeseries_field_out='date'
    )

    if 'ax' in kwargs:
        ax_plot = kwargs['ax']
    else:
        _, ax_plot = plt.subplots()
        kwargs['ax'] = ax_plot

    kwargs_cycle = get_next_color(ax_plot)
    for prop in kwargs_cycle:
        if prop not in kwargs:
            kwargs[prop] = kwargs_cycle[prop]
    
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

def plot_report_countries(*args, **kwargs):
    return plot_timeseries_countries(plot_report_country, *args, **kwargs)

def plot_model_countries(*args, **kwargs):
    return plot_timeseries_countries(plot_model_country, *args, **kwargs)
    
def plot_daily_deaths_countries(*args, **kwargs):
    return plot_timeseries_countries(plot_daily_deaths_country, *args, **kwargs)


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
        label_list = [t.get_text() for t in ax.get_legend().get_texts()]
    except AttributeError as identifier:
        label_list = []

    for country in country_list:
        # plot the country specific forecast
        axout, main_label = plot_timeseries_func(
            forecast_df, country,
            ax=ax, **kwargs)
        if type(main_label) == type(list()):
            label_list.extend(main_label)
        else:
            label_list.append(main_label)
    
    # Tailor axis limits
    axis_date_limits(ax, min_date=min_date, max_date=max_date)
    # Select only mean lines to appear in legend
    remove_confidence_interval_legend_labels(axout)
    
    return axout

def compare_fatality_predictions(
    data_dict,
    country_list=None,
    ax=None,
    prop_cycle=None,
    max_num_country_ci_display=3,
    **kwargs
    ):
    if prop_cycle is None:
        # define a new property cycle for the axes we are using
        prop_cycle = define_new_cycle(
            marker=['o',',','v','+'], # which varies the marker
            color_frequency=len(country_list), # the same colour repats every 3 lines
            markevery=[5],  # Markers are plotted every 5 days
        )
    if ax is None:
        _, ax = plt.subplots()
        ax.set_prop_cycle(prop_cycle)

    # Plot the data (the reported data without any line, and with a marker every time)
    plot_report_countries(data_dict["modelling"], country_list=country_list,
        ax=ax, linestyle='', markevery=1, **kwargs)
    plot_model_countries(data_dict["modelling"], country_list=country_list,
        ax=ax, **kwargs)
    plot_forecast_countries(data_dict["forecasting"], country_list=country_list,
        ax=ax, **kwargs)

    # For clarity we remove the confidence intervals and the move the legend out
    if max_num_country_ci_display >= len(country_list):
        remove_confidence_interval_legend_labels(ax)
    else:
        remove_confidence_interval_lines(ax)

    modify_legend(ax, bbox_to_anchor=(1.04, 1.0), loc='upper left')
    return ax