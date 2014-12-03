#!/bin/bash

sqlite3 -separator ',' data/filtered_logs.db "select * from discrete_log where user_id=\"${1}\";"
