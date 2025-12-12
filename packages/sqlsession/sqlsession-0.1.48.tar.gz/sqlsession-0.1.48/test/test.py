
conn = {
    "user":     'owl',
    "port":     '5432',
    "database": 'owl_dev',
    "type":     'pgsql',
    "password": 'owl',
    "host":     'localhost'
}

from sqlsession import SqlSession

with SqlSession(conn) as session:
    session.execute("create temp table temp_test (id int);")
    session.execute("create temp table temp_view as select * from pg_stat_activity;")
