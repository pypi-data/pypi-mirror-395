from .ivolatility_backtesting import (
    BacktestResults, BacktestAnalyzer, ResultsReporter,
    ChartGenerator, ResultsExporter, run_backtest, run_backtest_with_stoploss,
    init_api, api_call, APIHelper, APIManager,
    ResourceMonitor, create_progress_bar, update_progress, format_time,
    StopLossManager, PositionManager, StopLossConfig,
    calculate_stoploss_metrics, print_stoploss_section, create_stoploss_charts,
    create_stoploss_comparison_chart,
    optimize_parameters, plot_optimization_results,
    create_optimization_folder,
    preload_options_data,
    STRATEGIES, StrategyRegistry, detect_strategy_type, format_params_string,
    preload_data_universal,  # NEW: Universal preloader V2
    safe_get_greek, collect_garbage,  # Helper functions
    apply_optimization_preset, list_optimization_presets, 
    calculate_combinations_count, print_preset_info,
    get_cache_config, UniversalCacheManager,
    _process_options_df,
    precalculate_indicators_from_config, build_indicator_lookup,
    INDICATOR_REGISTRY, auto_calculate_lookback_period
)

__all__ = [
    'BacktestResults', 'BacktestAnalyzer', 'ResultsReporter',
    'ChartGenerator', 'ResultsExporter', 'run_backtest', 'run_backtest_with_stoploss',
    'init_api', 'api_call', 'APIHelper', 'APIManager',
    'ResourceMonitor', 'create_progress_bar', 'update_progress', 'format_time',
    'StopLossManager', 'PositionManager', 'StopLossConfig',
    'calculate_stoploss_metrics', 'print_stoploss_section', 'create_stoploss_charts',
    'create_stoploss_comparison_chart',
    'optimize_parameters', 'plot_optimization_results',
    'create_optimization_folder',
    'preload_options_data',
    'STRATEGIES', 'StrategyRegistry', 'detect_strategy_type', 'format_params_string',
    'preload_data_universal',  # NEW: Universal preloader V2
    'safe_get_greek', 'collect_garbage',  # Helper functions
    'apply_optimization_preset', 'list_optimization_presets', 
    'calculate_combinations_count', 'print_preset_info',
    'get_cache_config', 'UniversalCacheManager',
    '_process_options_df',
    'precalculate_indicators_from_config', 'build_indicator_lookup',
    'INDICATOR_REGISTRY', 'auto_calculate_lookback_period'
]