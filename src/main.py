import os
import argparse
from visier.connector import Authentication
from visier.connector import VisierSession
from repl import SqlLikeShell


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visier SQL-like Shell")
    parser.add_argument("-u", "--username", help="Visier username", type=str)
    parser.add_argument("-p", "--password", help="Visier password", type=str)
    parser.add_argument("-a", "--apikey", help="Visier API key", type=str)
    parser.add_argument("-v", "--vanity", help="Visier vanity", type=str)
    parser.add_argument("-H", "--host", help="Visier host", type=str)
    parser.add_argument("-w", "--width", help="Maximum column width", type=int, default=30)
    args = parser.parse_args()

    username = args.username or os.getenv("VISIER_USERNAME")
    password = args.password or os.getenv("VISIER_PASSWORD")
    apikey = args.apikey or os.getenv("VISIER_APIKEY")
    vanity = args.vanity or os.getenv("VISIER_VANITY")
    host = args.host or os.getenv("VISIER_HOST")

    if not username or not password or not apikey or not host:
        raise Exception("ERROR: Missing required credentials. Please provide username, password, apikey, and host.")

    auth = Authentication(
        username = username,
        password = password,
        host = host,
        api_key = apikey,
        vanity = vanity)

    with VisierSession(auth) as session:
        SqlLikeShell(session, args.width).cmdloop()