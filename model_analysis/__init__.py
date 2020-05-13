
from .data_load import (
    read_manifest, Model_Folder, get_analysis_set
)

from .data_plot import (
    plot_forecast_countries, plot_forecast_country, 
    plot_model_countries, plot_model_country, 
    plot_report_country, plot_report_countries,
    plot_daily_deaths_countries, plot_daily_deaths_country,
    compare_fatality_predictions,
    compare_all_fatality_predictions,
    compare_case_predictions,
    compare_rt_and_interventions,
    plot_Rt_country, plot_Rt_countries,
    plot_Rt_forecast_country, plot_Rt_forecast_countries,
    plot_zones_summary,
    plot_all_deaths_forecast_country,
    plot_all_deaths_model_country,
    plot_all_deaths_report_country,
    plot_all_deaths_country,
    plot_case_forecast_country,
    plot_case_model_country,
    plot_case_report_country,
    plot_daily_cases_country,
    plot_all_deaths_forecast_countries,
    plot_all_deaths_report_countries,
    plot_all_deaths_model_countries,
    plot_all_deaths_countries,
    plot_case_forecast_countries,
    plot_case_report_countries,
    plot_case_model_countries,
    plot_daily_cases_countries,
)

from .plot_core import (
    get_next_color,
    remove_confidence_interval_lines,
    remove_confidence_interval_legend_labels,
    modify_legend,
    axis_date_limits,
    define_new_cycle,
    define_color_cycler_from_map,
    default_color_cycle,
    plot_interventions_countries,
)

from .translate import (
    translate_axes_to_french,
)

from . import data_plot as icl_plot
from . import plot_core as icl_plot_core
from . import data_load as icl_load
from . import translate as icl_translate
                    