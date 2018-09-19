from sqlalchemy import text

def get_next_free_id(engine, table_name, column_name='id'):
    '''Returns the next id to be used. Also checks gap in the sequence.
    `engine` is SQLAlchemy object returned by create_engine().'''

    sql_cmd = text('''SELECT MIN(a.{colname} + 1) AS next
    FROM {tablename} AS a
    LEFT OUTER JOIN {tablename} AS b
    ON a.{colname} + 1 = b.{colname}
    WHERE b.{colname} IS NULL;'''.format(tablename=table_name, colname=column_name))

    qry_res = engine.execute(sql_cmd)
    next_id = qry_res.fetchone()[0]

    # If the table is empty, next_id will be None. In that case, id starts from 1.
    next_id = next_id if next_id else 1

    return next_id