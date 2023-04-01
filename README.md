# Visier SQL-like Shell
The Visier SQL-like Shell a very small application that technical Visier users and builders issue queries in Visier's SQL-like syntax against the Visier platform.

## Prerequisites
The SQL-like Shell issues queries to the Visier platform using the platform's public APIs. In order to successfully connect to your Visier People data, you need:
* The URL domain name prefix. Likely matching a pattern like this: `https://{vanity-name}.api.visier.io`.
* An API key that issued by Visier to your organization.
* A username identifying a user within your organization's Visier tenant who has been granted API access capabilities.
* That user's password

## Installation
The recommended approach is to install this application in a Virtual Environment.
```sh
python3 -m venv visier-sql
source visier-sql/bin/activate
pip install -r requirements.txt
```

## Run the shell
Upon starting, the shell will immediately attempt to connect to the Visier platform using the provided credentials. These can either be passed in through environment variables:
* `VISIER_HOST`
* `VISIER_USERNAME`
* `VISIER_PASSWORD`
* `VISIER_APIKEY`
* `VISIER_VANITY`

Alternatively, credentials can be provided through command line arguments. Run the application with `--help` to get the argument specifics:

`$ python src/main.py --help`

```sh
usage: main.py [-h] [-u USERNAME] [-p PASSWORD] [-a APIKEY] [-v VANITY] [-H HOST] [-w WIDTH]

Visier SQL-like Shell

options:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Visier username
  -p PASSWORD, --password PASSWORD
                        Visier password
  -a APIKEY, --apikey APIKEY
                        Visier API key
  -v VANITY, --vanity VANITY
                        Visier vanity
  -H HOST, --host HOST  Visier host
  -w WIDTH, --width WIDTH
                        Maximum column width
```
 ## Example
 Once the application has successfully started and established a connection with the Visier platform, it is ready to execute SQL-like queries:
 ```
 Welcome to the Visier SQL-like Shell.
Type help or ? to list commands.

Don't forget to terminate each SQL-like statement with a semicolon (;)

sql> select
   | Visier_Time AS "Reporting period",
   | level(Location, "Location_1") AS Country,
   | employeeCount() AS count
   | from Employee
   | where 
   | Visier_Time IN periods(date("2021-01-01"), 6, period(2, Month)) AND
   | isFemale = TRUE;


Reporting period        |Country                    |count
----------------------------------------------------------
2020-03-01T00:00:00.000Z|APAC.Australia             |99   
2020-03-01T00:00:00.000Z|APAC.Japan                 |143  
2020-03-01T00:00:00.000Z|EMEA.Poland                |83   
2020-03-01T00:00:00.000Z|EMEA.South Africa          |12   
2020-03-01T00:00:00.000Z|EMEA.Spain                 |45   
2020-03-01T00:00:00.000Z|EMEA.United Kingdom        |152  
2020-03-01T00:00:00.000Z|North America.Canada       |138  
2020-03-01T00:00:00.000Z|North America.United States|500  
...
```

## Quitting the application
Execute command `bye` without any other commands and the application will close.
```
sql> bye
Closing the application
```