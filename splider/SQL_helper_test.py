from SQL_helper import SQLHelper
from splider_config import SpliderConfig as sc


def main():
    sql_helper = SQLHelper(sc.SQL_USER_NAME, sc.SQL_USER_PASSWORD, sc.SQL_DATABASE_NAME)

    a = 1
    b = 2


if __name__ == '__main__':
    main()
