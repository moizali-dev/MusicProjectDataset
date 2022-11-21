{% macro set_table() %}

    dataset_{{ run_started_at.astimezone(modules.pytz.timezone("America/New_York")).strftime("%Y_%m_%d") }}

{% endmacro %}