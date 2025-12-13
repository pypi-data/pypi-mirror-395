==================
Access Logs Driver
==================

Load the content of gzipped Apache HTTP log files
Exclude bots, scrapers, etc., select URLs matching the provided regex(es), and generate a CSV of the relevant log entries.

Take postprocessed logs and strip out multiple hits in sessions, and
resolve URLs to the chosen `URI_SCHEME` (e.g. info:doi).

We strip out entries where the same (IP address * user agent) pair has accessed
a URL within the last `SESSION_TIMEOUT` (e.g. half-hour)

Additionally, we convert the URLs to ISBNs and collate request data by date,
outputting a CSV for ingest via the stats system.

Release Notes:
==============

[0.1.0] - 2025-12-08
--------------------

Changed:
    * LogStream replaced with LogProcessor, which requires open file-like
      objects as input.

Added:
    * Able to process different log formats.

[0.0.7] - 2024-01-05
--------------------

Changed:
    * Deletion of the spiders filter in ``process_download_logs.py``


[0.0.6] - 2023-08-13
--------------------

Changed:
    * Refactored driver logic
    * **breaking** | Changed parameters for the ``Request.__init__()`` method
        - Removed ``re_match_dict`` parameter
        - Added ``timestamp`` and ``user_agent`` parameters
    * Changed Request.timestamp from type ``time`` to ``datetime``
    * Changed LogStream to use the new ``Request.__init__()``
    * Expanded range for ``LogStream.logfile_names`` logic to include files
      within 1 day of the search_date
    * ``LogStream.lines()`` yields ``Request`` objects, not ``str`` values
    * ``LogStream.filter_in_line_request()`` only yields one line per measure


[0.0.5] - 2023-07-03
--------------------

Changed:
    * Added start_date and end_date for searching in the log files
    * Added the measure_uri to the result


[0.0.4] - 2023-07-31
--------------------

Changed:
    * Update file structure and name of the driver


[0.0.3] - 2023-07-25
--------------------

Changed:
    * Update requirements
    * Update using a pyproject.toml file as well as the new deployment structure


[0.0.2] - 2023-07-11
--------------------

Added:
    * Unittests

Changed:
    * Moved the files out of the package and get the file's data as parameters and return the filtered data.
    * renamed the plugin to access-logs-local
