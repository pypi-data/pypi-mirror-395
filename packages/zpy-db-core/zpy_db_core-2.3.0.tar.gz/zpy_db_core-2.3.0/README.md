from zdb.mysql import ZMySQL<p align="center">
<a  href="https://github.com/NoeCruzMW/zpy-flask-msc-docs"><img width="150" src="https://lh3.googleusercontent.com/a-/AOh14GjLO5qYYR5nQl5hgavUKz4Dv3LVzWDvGtV4xNam=s600-k-no-rp-mo" alt="Zurck'z"></a>
</p>
<p align="center">
    <em>ZDB Core, Layer for connect to mysql, postgresql or oracle from python</em>
</p>
<p align="center"></p>

---

# ZPy Database Core

> Zurck'z Py

This package contains some helpers features for call function or stored procedures from python.

ZPy use the following packages:

- mysql-connector-python
- cx-Oracle
- psycopg2

## Requirements

- Python 3.6+

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install py flask micro service core .

```bash
pip install zpy
pip install package_directory directory_to_install
```

## Features

Contains some helper features with specific integrations.

- Database
    - Functions executor
    - Stored Procedures executor
    - Autocommit is false by default
- Utils
    - Context Manager Helper

## Roadmap

- ActiveRecord implementation
- Cluster
- Parallel parsed

## Basic Usage

Basic Configuration

````python

config = {
    "user": "",
    "password": "",
    "database": "",
    "host": "",
    "port": 3306
}
````

With single MySQL datasource

```python
from zdb.mysql import ZMySQL
from zdb import ZDBTransact

# Create database instance for MySQL 
mysql_db = ZMySQL.from_of(user="", password="", host="", db_name="")

# If you only execute one operation you can call directly
# Connection automatically opened and commit and close
[user] = mysql_db.call("FN_GET_USER_BY_ID", list_params=[1])

# Open connection using Context Manager

with ZDBTransact(mysql_db) as tr:
    payments = mysql_db.call("FN_GET_USER_PAYMENTS", list_params=[1], connection=tr.session)

    for payment in payments:
        mysql_db.call("FN_UPDATE_PAYMENT", list_params=[payment['id']], connection=tr.session)

```

Multiple Datasources

```python
# Define db mediator 
# Setup base configuration in ZMediator()
# The base configuration will be overwritten by add common values 
db_mngr = ZMediator(config, False)
.add_common("DB_NAME_1", "DB_USER", "DB_PASSWORD", True)  # Mark default ds
.add_common("DB_NAME_2", "DB_USER", "DB_PASSWORD")
.add_common("DB_NAME_3", "DB_USER", "DB_PASSWORD")

db_conn1 = db_mngr.default().new_connect()
db_conn2 = db_mngr.get("DB_NAME_1").new_connect()
db_conn3 = db_mngr.get("DB_NAME_3").new_connect()

try:
    # Execute function
    res = db_mngr.default().exec("FN_GET_USER_BY_ID(%d)", list_params=[1], ret_type=DBTypes.cursor)
    print(res)
    # Execute function
    res = db_mngr.get("DB_NAME_2").exec("FN_GET_USER_BY_ID(%d)", list_params=[1], ret_type=DBTypes.cursor)
    print(res)
    # Call sp
    res = db_mngr.get("DB_NAME_3").call("SP_GET_DATA", ret_type=DBTypes.cursor)
    print(res)
except Exception as e:
    logging.exception(e)
finally:
    # ⚠ Remember close opened connections
    db_conn1.close()
    db_conn2.close()
    db_conn3.close()
```

````python
session = self.db.new_connect()
try:
    count = self.db.call('SP_GENERIC_GET_ROWS', list_params=['TAROLES'], ret_type=DBTypes.integer,
                         connection=session)
    return Pager.create(data.pagination, count)
finally:
    session.close()
````

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Authors

[Noé Cruz](https://www.linkedin.com/in/zurckz/)
