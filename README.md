![linting](https://github.com/visier/sql-shell/actions/workflows/pylint.yml/badge.svg)
# Visier SQL-like Shell
The Visier SQL-like Shell is an application that allows technical users and builders to issue queries in Visier's SQL-like syntax against the Visier platform.

## Prerequisites
The SQL-like Shell issues queries to the Visier platform using the platform's public APIs. To successfully connect to your Visier data, you need:
* The URL domain name prefix. For example: `https://{vanity-name}.api.visier.io`.
* An API key issued by Visier.
* A username identifying a user within your organization's Visier tenant who has been granted API access capabilities.
* That user's password.

## Installation
We recommend that you install this application in a virtual environment.
```sh
python3 -m venv visier-sql
source visier-sql/bin/activate
pip install -U build
python -m build
```
After the build completes successfully, install the Python Wheel file found in the `dist` directory. For example:
```sh
pip install dist/visier_sqllike_shell-0.9.8-py3-none-any.whl
```
This installs a command line utility named `vsql-shell` in the active virtual environment.

## Run the Shell
After starting, the shell immediately attempts to connect to the Visier platform using the provided credentials. You can pass in credentials through environment variables:
* `VISIER_HOST`
* `VISIER_USERNAME`
* `VISIER_PASSWORD`
* `VISIER_APIKEY`
* `VISIER_VANITY`
* `VISIER_TARGET_TENANT_ID`

In Linux-like **non-production** environments, it may be beneficial to persist these values in a file that you 'source' into your virtual environment. 	
Create a file named `.env` and populate it like the following example:
```sh
echo -n "Enter the password for the Visier API User: "
read -s vpwd
export VISIER_VANITY=example
export VISIER_HOST=https://$VISIER_VANITY.api.visier.io
export VISIER_USERNAME=apiuser@example.com
export VISIER_PASSWORD=$vpwd
export VISIER_TARGET_TENANT_ID=partner-sub-tenant-code
export VISIER_APIKEY=the-api-key-issued-by-visier
```

Source the environment and provide the password:
```
$ source .env
```

### OAuth2 Authentication
The SQL-shell uses the [visier-connector](/visier/connector-python) to connect to Visier. Please reference this connector for details how to set up OAuth 2.0 with Visier.

You can start the REPL by running:
```sh
$ vsql-shell
```

Alternatively, you can provide credentials through command line arguments. Run the application with `--help` to get the argument specifics:

```sh
$ vsql-shell --help`
```

```sh
usage: vsql-shell [-h] [-a APIKEY] [-c CLIENT_ID] [-S CLIENT_SECRET] [-H HOST] [-p PASSWORD] [-r REDIRECT_URI] [-t TARGET_TENANT_ID] [-u USERNAME]
               [-v VANITY] [-s {analytic,staging}] [-w WIDTH]

Visier SQL-like Shell

options:
  -h, --help            show this help message and exit
  -a APIKEY, --apikey APIKEY
                        Visier API key
  -c CLIENT_ID, --client-id CLIENT_ID
                        Visier OAuth client ID
  -S CLIENT_SECRET, --client-secret CLIENT_SECRET
                        Visier OAuth client secret
  -H HOST, --host HOST  Visier host
  -p PASSWORD, --password PASSWORD
                        Visier password
  -r REDIRECT_URI, --redirect-uri REDIRECT_URI
                        Visier OAuth redirect URI
  -t TARGET_TENANT_ID, --target-tenant-id TARGET_TENANT_ID
                        Visier partner tenant name
  -u USERNAME, --username USERNAME
                        Visier username
  -v VANITY, --vanity VANITY
                        Visier vanity
  -s {analytic,staging}, --schema {analytic,staging}
                        The initial schema to use
  -w WIDTH, --width WIDTH
                        Maximum column width
```
## Example
After the application starts and establishes a connection with the Visier platform, it's ready to execute SQL-like queries:
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

## Quit the Application
Execute one of the commands `bye`, `exit` or `quit` without any other commands to close the application.
```
sql> bye
Closing the application
```
