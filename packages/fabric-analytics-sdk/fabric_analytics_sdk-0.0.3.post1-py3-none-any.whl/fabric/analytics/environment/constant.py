PBI_SCOPE = "https://analysis.windows.net/powerbi/api/.default"

PBI_SCOPE_PPE = "https://analysis.windows-int.net/powerbi/api/.default"
# This is theoretically equal to PBI_SCOPE when calling Fabric Public API
# Note some private API, especially mwc APIs accept PBI audience only
FABRIC_SCOPE = "https://api.fabric.microsoft.com/.default"

STORAGE_SCOPE = "https://storage.azure.com/.default"
KEYVAULE_SCOPE = "https://vault.azure.net/.default"
KUSTO_SCOPE = "https://kusto.kusto.windows.net/.default"
SQL_SCOPE = "https://database.windows.net/.default"

FABRIC_ANALYTICS_SDK_CONSOLE_LOG_LEVEL = "FABRIC_ANALYTICS_SDK_CONSOLE_LOG_LEVEL"

FABRIC_ONLINE_EXPERIENCE_RUNTIME_NAME = [
    "spark_notebook_driver",
    "spark_notebook_executor",
    "sjd_driver",
    "sjd_executor",
    "python_notebook",
]
