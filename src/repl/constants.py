# SQL-like shell constants
SQL_PROMPT = "\x1b[1;34;40msql> \x1b[0m"
SQL_CONTINUE_PROMPT = "\x1b[1;34;40m   | \x1b[0m"
SQL_BYE = "\x1b[1;32;40mClosing the application\x1b[0m"
SQL_TABLE_START = "\n\x1b[1;37;40m"
SQL_TABLE_END = "\x1b[0m\n"
SQL_OPTIONS = {
        "memberDisplayMode": "COMPACT",
        "zeroVisibility": "ELIMINATE",
        "nullVisibility": "ELIMINATE"
    }