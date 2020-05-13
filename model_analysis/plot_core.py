import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.rcsetup import cycler
from matplotlib.colors import to_hex


# Marks a confidence interval
_ci_mark = "CI_"

confidence_interval_format = {
    "linestyle": ':',
    "marker": '',
}
# Collect the error behaviour of pandas when plotting an empty dataframe
error_pd_empty_plot = Exception()
try:
    pd.DataFrame().plot()
except Exception as e:
    error_pd_empty_plot = e

pd.plotting.register_matplotlib_converters()
# Module defaults can be configured after loading 
default_color_cycle = plt.rcParams['axes.prop_cycle']
default_color_map = plt.cm.viridis
default_plot_kwargs = {
    "report": {'linestyle':'', 'markevery':1, 'marker': 'o', 'markersize':3},
    "model": {},
    "forecast": {'linestyle':'--'},
}

intervention_labels = {
    "lockdown" : "Lockdown",
    "public_events" : "Cancel events",
    "schools_universities": "School closures",
    "self_isolating_if_ill": "Self-isolation\nwhen ill",
    "social_distancing_encouraged": "Social distancing",
}

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


def define_color_cycler_from_map(n, colormap=None):
    if colormap is None:
        colormap = default_color_map
    return cycler(color=[
        to_hex(colormap(float(i) / float(n))) for i in range(n)
    ])


def get_confidence_interval_lines(ax):
    ci_lines = []
    for line in ax.get_lines():
        if _ci_mark in line.get_label():
            is_ci_line = True
            for prop in confidence_interval_format:
                is_ci_line &= (
                    getattr(line, 'get_' + prop)()
                    == confidence_interval_format[prop]
                )
            if is_ci_line:
                ci_lines.append(line)
    return ci_lines


def get_invalid_label_lines(ax):
    ci_lines = []
    for line in ax.get_lines():
        if "_" == line.get_label()[:1]:
            ci_lines.append(line)
    return ci_lines


def remove_confidence_interval_lines(ax):
    for line in get_confidence_interval_lines(ax):
        line.remove()


def remove_confidence_interval_legend_labels(ax):
    ci_lines = get_confidence_interval_lines(ax)
    ci_lines.extend(get_invalid_label_lines(ax))
    line_legend = [l for l in ax.get_lines() if l not in ci_lines]
    ax.legend(handles=line_legend)


def get_current_legend_handles(ax):
    label_list = [t.get_text() for t in ax.get_legend().get_texts()]
    line_list = [l for l in ax.get_legend().get_lines()]
    handles, labels = ax.get_legend_handles_labels()

    # handler_map = ax.get_legend().get_legend_handler_map()

    for handle, label in zip(handles, labels):
        if label in label_list:
            line_list[label_list.index(label)] = handle

    return line_list, label_list

def add_lines_to_legend(ax, handles, labels=None):
    copy_handles, copy_labels = get_current_legend_handles(ax)
    copy_handles.extend(handles)
    if labels is None:
        labels = [h.get_label() for h in handles]
    copy_labels.extend(labels)
    ax.legend(handles=copy_handles, labels=copy_labels)

def modify_legend(ax, **kwargs):
    copy_handles, copy_labels = get_current_legend_handles(ax)
    ax.legend(handles=copy_handles, labels=copy_labels, **kwargs)

def axis_date_limits(axs, min_date=None, max_date=None, format_date=None):
    if type(axs) != type(list()):
        axs = [axs]
    # Tailor axis limits
    for ax in axs:
        try:
            x_min, x_max = pd.to_datetime(ax.get_xlim(), unit='D')
        except:
            print("Warning: Failed to run `pd.to_datetime(ax.get_xlim(), unit='D')`")
            print(f"{ax.get_xlim()} = ax.get_xlim() ; trying without unit")
            x_min, x_max = pd.to_datetime(ax.get_xlim())

        if not (max_date is None):
            ax.set_xlim(right=min(x_max, pd.to_datetime(max_date, format=format_date)))
        if not (min_date is None):
            ax.set_xlim(left=max(x_min, pd.to_datetime(min_date, format=format_date)))

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

def plot_timeseries_confidence_interval_country(
    forecast_df,
    active_columns,
    plot_quantity, # y label of the plot
    country,
    *,
    country_label=None,
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
    timeseries_type="time series",
    verbose=True,
    **kwargs
):
    if country_label is None:
        country_label = country

    if verbose:
        print(f"Plotting {timeseries_type} for {country_label}")

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
        ).dt.to_period('D')
    return in_df


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

def plot_interventions_countries(
    df_interventions,
    country_list,
    *,
    ax=None,
    prop_cycle=None,
    color_cycle=None,
    color=None,
    label_func=lambda row: f"{row['country']}: {row['key']}",
    verbose=False,
    **kwargs
):
    """ Plots interventions as vertical lines.
    """
    # Input handling
    if ax is None:
        fig, ax = plt.subplots()
        ax.xaxis_date()  # correctly setup x axis to be a date.
        ax.xaxis.freq = "D"

    
    if prop_cycle is None:  # Define the default property cycle
        prop_cycle = cycler(
            linestyle=['-','--', '-.', ':', ':'],
            marker=['o', 's', 'v', '+', 'x']
        )

    if (color is not None) and (color_cycle is not None):
        raise ValueError("`color` and `color_cycle` cannot be both specified.")
    
    if color is not None:
        color_cycle = cycler(color=[color])

    # Trim the list of interventions to only the relevant ones
    trimmed_interventions = find_unique_interventions(
        df_interventions, country_list
    )
    
    # Define the correct color_cycle that will match the order of the trimmed
    # intervention list
    if color_cycle is None: 
        color_list = _define_colors_of_interventions(trimmed_interventions, country_list)
        color_cycle = cycler(
            color=color_list
        )

    # Set the property cycle
    try:
        ax.set_prop_cycle(prop_cycle * color_cycle)
    except Exception as e:
        print(prop_cycle)
        print(color_cycle)
        raise e
    # Prepare the interventions for plotting
    trimmed_interventions = enable_time_series_plot(trimmed_interventions, "value")
    trimmed_interventions.sort_values(by=["key", "country", "date"], inplace=True)
    ylims = ax.get_ylim()
    vlines = []
    d_dict = {}
    # Plot the lines
    for i, row in trimmed_interventions.iterrows():
        d = row["date"]
        try: # offset markers when multiple interventions happen on the same day
            d_dict[d] += 1
        except:
            d_dict[d] = 0

        vlines.extend(
            ax.plot([d, d], [ylims[0], ylims[1] * (1 - 0.04 * d_dict[d])], 
                label=label_func(row), **kwargs
            )
        )

    # Create custom legend lines
    legend_lines = []
    for inter, props in zip(trimmed_interventions["key"].unique(), prop_cycle):
        if inter not in intervention_labels:
            intervention_labels[inter] = inter
            print(f"WARNING: intervention {inter} does not have a label, "
            + "consider setting `plot_core.intervention_labels['"
            + f"{inter}']` for better legends of plots.")
        legend_lines.append(
            plt.Line2D([0], [0], color="k", lw=2, 
                marker=props["marker"], label=intervention_labels[inter],
                ls=props["linestyle"]),

        )
    
    try:
        lg = ax.get_legend()
        lg.set_bbox_to_anchor((1.04, 0.5))
        ax.add_artist(lg)
    except:
        pass
    # Add a legend
    ax.legend(
        handles=legend_lines, title="Intervention types",
        bbox_to_anchor=(1.04, 1.0),
        loc='upper left'
    )
    return ax, (vlines, legend_lines)

def compare_report_model_predictions(
    compare_func,
    data_dict,
    country_list=None,
    ax=None,
    prop_cycle=None,
    max_num_country_ci_display=3,
    plot_specific_kwargs={},
    plot_forecast=True,
    **kwargs
):
    marker_list=['o',',',',']
    if not plot_forecast:
        marker_list.pop(-1)

    if prop_cycle is None:
        # define a new property cycle to ensure the colour repeats correctly
        prop_cycle = define_new_cycle(
            marker=marker_list, # which varies the marker
            color_frequency=len(country_list), # the same colour repeats every len(country_list) lines
            markevery=[5],  # Markers are plotted every 5 days
        )
    if ax is None:
        _, ax = plt.subplots()
    if len(country_list) > 1:
        ax.set_prop_cycle(prop_cycle)
    
    # Get the correct precedence of keyword args
    plot_kwargs = dict(default_plot_kwargs)
    for plot in plot_kwargs:
        for kwarg in kwargs:
            plot_kwargs[plot][kwarg] = kwargs[kwarg]
    for plot in plot_specific_kwargs:
        for kwarg in plot_specific_kwargs[plot]:
            plot_kwargs[plot][kwarg] = plot_specific_kwargs[plot][kwarg]

    # Plot the data (the reported data without any line, and with a marker every time)
    compare_func(
        data_dict, plot_kwargs, 
        country_list=country_list, ax=ax, plot_forecast=plot_forecast
    )

    # For clarity we remove the confidence intervals and the move the legend out
    if max_num_country_ci_display >= len(country_list):
        remove_confidence_interval_legend_labels(ax)
    else:
        remove_confidence_interval_lines(ax)

    modify_legend(ax, bbox_to_anchor=(1.04, 1.0), loc='upper left')
    return ax

def _define_colors_of_interventions(trimmed_interventions, zone_list):
    """ Defines the correct colors to use based on the zone list and 
    the unique interventions, to ensure:
    1. That the country's color is used if it is present in zone_list
    2. A single intervention is used for others
    """
    trimmed_list = {c: True for c in trimmed_interventions["country"].unique()}
    zone_country_map = {
        zone: row["country"] 
            for _, row in trimmed_interventions.iterrows()
                for zone in row["region"]
    }
    color_list = []
    for i, zone in enumerate(zone_list):
        if (
            (zone in trimmed_list) or # the zone is a country
            (
                zone_country_map[zone] not in zone_country_map 
                and trimmed_list[zone_country_map[zone]]
            ) # or the country is not in the list of zones
        ):
            # Ensure a country's interventions are only plotted once
            trimmed_list[zone_country_map[zone]] = False  
            color_list.append(
                default_color_cycle.by_key()['color'][i]
            )
    return color_list

def find_unique_interventions(df_interventions, region_list):
    """ Given a list of regions returns a datafram similar to df_interventions
    with no repeated intervention.

    This is used to trim repeated interventions that arise from modelling regions
    and countries together.
    """
    act_interventions = df_interventions.apply(
        lambda x: x["region"] in region_list, axis=1
    )
    grouped_interventions = df_interventions.loc[act_interventions,].groupby(
        ["key", "value","country"])
    trimmed_interventions = []

    for group_val, group in grouped_interventions:
        new_group = group.iloc[0, ].copy()
        new_group.loc["region"] = group["region"].unique()
        trimmed_interventions.append(new_group)

    return pd.DataFrame(trimmed_interventions)