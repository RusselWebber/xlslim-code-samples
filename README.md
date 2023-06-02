# xlslim-code-samples

This repo contains working examples showing how the xlSlim Excel add-in enables you to use Python in Excel.

See https://russelwebber.github.io/xlslim-docs/html/index.html and https://www.xlslim.com

Specific examples are:

## Basics
* Interactive mode where Excel mimics a Jupyter notebook
* Calling a Python function from Excel
* Using type hints
* Passing a dictionary
* Using optional arguments
* Reading a csv into Excel using Python
* Fetching JSON data from the web and showing this in Excel
* Manipulating data using SQLite and showing the results in Excel
* Calling VBA and other macro functions from Python

## Imports
* Controlling which Python functions are imported into Excel
* Adding additional paths to the Python module search path
* Dynamic imports, creating modules and functions from text in Excel

## Remote Imports
* Importing modules from GitHub and BitBucket
* Importing a module from a Gist
* Importing code from a remote ZIP archive

## NLP
* Performaing nlp with Python and Excel

## numpy
* Passing numpy arrays from Excel to Python functions
* Cacheing numpy arrays returned from Python

## pandas
* Passing pandas series and dataframes from Excel to Python functions
* Cacheing pandas series and dataframes returned from Python
* Calling a Python Monte Carlo option pricer from Excel
* Reading prices from Yahoo Finance into Excel
* Using Python sklearn to perform Principal Components Analysis of Index Prices

## Streaming
* Streaming data from Bloomberg into Excel using Python
* Streaming data from IEX into Excel using Python
* Streaming data from Kafka into Excel using Python
* Streaming numpy arrays from Kafa into Excel using Python

## VBA
* Using Python as an Excel replacement. 
* Loading csv data into Excel using PowerQuery.
* Using Python and pywin32 COM to create a pivot table.
* Adding items to the context and ribbon menus

## Finance
* Using xlSlim to run scenario analysis for equity index options. This example shows how data classes and dictionaries can be used to structure code neatly.