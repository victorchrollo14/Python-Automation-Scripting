# Python-Automation-Scripting

This Repo Contains a bunch of python Scripts for automating MySQL and Scraping Data.

## Battery Status
This folder contains the script which uses MySQLDb library in python to connect to MySQL server using python and gets the 
Gprs device status from the server and checks the battery status of device to see if there are any problems in battery functioning.

## Scrape Log Files
The gprs device generates a log file that contains data on the internal process of the device.
This script basically checks for completely processed data and from that data it gets only the required parameters.

## ledger script
Ledger script scrapes a list of items from the ledger(a csv file) and displays in a new csv file.

## device Testing automation
This script is used to automate the testing of multiple grps devices at the same time, which saves a lot of time.
without this script you would need a dedicated person to go through the device updates from MySQL server and check if the device is 
working fine, which is time consuming and complicated.
The script works as follows:
* Read a csv file containing different configurations, and query the configurations into MySQL using python
* Test the device in slow mode.
* Switch on a fan automatically by sending a command to a hardware device that controls the on/off in the fan.
(The devices are kept on the fan, inorder to introduce vibrations and switch the device to fast mode)
* after the device has gone to fast mode, off the fan and test in fast mode.
* print all the test case results into a log file.
