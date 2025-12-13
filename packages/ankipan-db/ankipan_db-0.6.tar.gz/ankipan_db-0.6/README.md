# ankipan_db

Database for Ankipan (https://gitlab.com/ankipan/ankipan)

## Getting started

```
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib -y
sudo service postgresql start
sudo -u postgres psql
CREATE ROLE root WITH LOGIN PASSWORD 'secure_password' CREATEDB;
CREATE DATABASE ankipan_db OWNER root;

# create .env file with db connection data (see __init__.py)

python3 -c "db = DBManager();db.make_schema()"

# fill db with data (see help(SourceParser.sync_dir) and /examples/add_data_to_db.ipynb)

```