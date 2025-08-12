# Market Stream Status Utils

This Python script interacts with the JMX Market-Stream service to fetch and analyze cache status for hosts.

## Features

- Fetches the status response for each host in a provided list or for a specific target host.
- Analyzes JMX Market-Stream responses to determine the cache health of each host.
- *(Work in Progress)* Plans to add functionality to restart hosts reporting `cacheIsRunning=false`.

## Usage

Run the main script to retrieve and review the cache status of your target hosts. The script uses multiple modules to organize functionality.

## Current Status

- Status fetching and reporting are implemented and functional.
- Restart automation is under active development.

---

Feel free to contribute or raise issues for improvements!
