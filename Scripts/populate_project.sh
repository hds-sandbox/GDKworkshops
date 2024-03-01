#!/bin/bash

# Create the main folders
mkdir -p Data Intermediate Backup Environments 

# Create the subfolders inside Backup
mkdir -p Backup/Data Backup/Scripts Backup/Analysis Backup/Results

# Create the soft links
ln -s Backup/Data Data
ln -s Backup/Scripts Scripts
ln -s Backup/Analysis Analysis
ln -s Backup/Results Results
