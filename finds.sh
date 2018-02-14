#!/bin/bash
rm ../results_temp; grep -r $1 ./inprogress >> ../results_temp; vim ../results_temp