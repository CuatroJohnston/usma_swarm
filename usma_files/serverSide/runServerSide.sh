#!/bin/bash
> raw_data.csv
> parsed_data.js
python waypoint_server.py ; python geogen2.py ; xdg-open index.html
