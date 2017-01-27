# SweetIQ's Location Loader Library

Introduction
---------------------
SweetIQ's Location Loader library acts as a template you can use to integrate 
with SweetIQ's Location API.  It includes a python script that can connect 
to your database, extract the mapped data and send it to SweetIQ.  This library 
also offers you the option of setting this script to run as a service on your
system to ensure that your data is always up-to-date on the SweetIQ database.

Before running the script for the first time, there are a few things you will 
need to setup.

Configuration
-------------
Configure your credentials in `config.py` to a) access to SweetIQ's 
environment, and b) establish a connection with your database.

Setup the service by setting the push interval in `config.py`.

Test Connection to SweetIQ
--------------------------
To test the connection to SweetIQ, be sure to put your authentication data in
config.py and call:

`python3 load_location.py test`

You should see

`testing connection
connection successful`

In the event of an error, you should see the error code from the server.

Setup Data Mapping
-----------------

Map your data fields (i.e. location name, address, phone number, etc) to 
those supported by SweetIQ by overwriting `sweetiq/load_sql`.  

This file does two things: a) basic mapping by selecting your field names 
and returning them to the associated field name in the SweetIQ database, and 
b) extra transformations that are easier to script in python.

See the SweetIQ Location API Specification (`http://locs-stag.swiq3.com/docs/`) 
for the complete list of fields, their supported formats and short descriptions.

Test Your Mapping
-----------------
Once you are done with the mapping, you should test to see if it was done 
properly. Do so by running the the application using 
`python3 load_locations.py test-mapping`. 

This call does three things: a) pushes the data from your database to SweetIQ's, 
b) performs a search in the SweetIQ db for all current data, and c) compares the
two data sets and highlights the differences.  

Please note that `--verify-update` should not be run in the production environment.
Instead, these changes will be reviewed by your SweetIQ Account Manager.

Using Docker
-----------------
* build the docker image: `docker build -t load_sweetiq .`
* load_location: launch it with docker using `docker run load_sweetiq`
