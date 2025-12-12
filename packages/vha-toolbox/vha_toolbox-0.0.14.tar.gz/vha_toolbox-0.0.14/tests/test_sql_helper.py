import unittest

from vha_toolbox import sql_helper


class SQLHelperTestCase(unittest.TestCase):
    def test_get_sql_1(self):
        table_name = 'my_table'
        columns = ['column_1', 'column_2']
        sql = sql_helper.SQL(table_name, columns)
        result = str(sql)
        expected_sql = 'SELECT column_1, column_2 FROM my_table'
        self.assertEqual(result, expected_sql)

    def test_get_sql_2(self):
        table_name = 'my_table'
        columns = ['column_1', 'column_2']
        sql = sql_helper.SQL(table_name, columns)
        sql.add_with('with_1', 'SELECT * FROM other_table')
        sql.add_with('with_2', 'SELECT * FROM other_table')
        result = str(sql)
        expected_sql = 'WITH with_1 AS (SELECT * FROM other_table)\nWITH with_2 AS (SELECT * FROM other_table)\nSELECT column_1, column_2 FROM my_table'
        self.assertEqual(result, expected_sql)

    def test_get_sql_3(self):
        table_name = 'my_table'
        columns = ['column_1', 'column_2']
        sql = sql_helper.SQL(table_name, columns)
        sql.add_with('with_1', 'SELECT * FROM other_table')
        sql.add_with('with_2', 'SELECT * FROM other_table')
        sql.set_where('column_1 > 5')
        result = str(sql)
        expected_sql = 'WITH with_1 AS (SELECT * FROM other_table)\nWITH with_2 AS (SELECT * FROM other_table)\nSELECT column_1, column_2 FROM my_table WHERE column_1 > 5'
        self.assertEqual(result, expected_sql)

    def test_get_sql_4(self):
        table_name = 'my_table'
        columns = ['column_1', 'column_2']
        sql = sql_helper.SQL(table_name, columns)
        sql.add_with('with_1', 'SELECT * FROM other_table')
        sql.add_with('with_2', 'SELECT * FROM other_table')
        sql.set_where('column_1 > 5')
        sql.set_limit(10)
        result = str(sql)
        expected_sql = 'WITH with_1 AS (SELECT * FROM other_table)\nWITH with_2 AS (SELECT * FROM other_table)\nSELECT column_1, column_2 FROM my_table WHERE column_1 > 5 LIMIT 10'
        self.assertEqual(result, expected_sql)

    def test_get_sql_5(self):
        table_name = 'my_table'
        columns = ['column_1', 'column_2']
        sql = sql_helper.SQL(table_name, columns)
        sql.add_with('with_1', 'SELECT * FROM other_table')
        sql.add_with('with_2', 'SELECT * FROM other_table')
        sql.set_where('column_1 > 5')
        sql.set_limit(10)
        sql.add_join('JOIN other_table ON my_table.id = other_table.id')
        result = str(sql)
        expected_sql = 'WITH with_1 AS (SELECT * FROM other_table)\nWITH with_2 AS (SELECT * FROM other_table)\nSELECT column_1, column_2 FROM my_table JOIN other_table ON my_table.id = other_table.id WHERE column_1 > 5 LIMIT 10'
        self.assertEqual(result, expected_sql)

    def test_get_sql_6(self):
        table_name = 'my_table'
        columns = ['column_1', 'column_2']
        sql = sql_helper.SQL(table_name, columns)
        sql.add_with('with_1', 'SELECT * FROM other_table')
        sql.add_with('with_2', 'SELECT * FROM other_table')
        sql.set_where('column_1 > 5')
        sql.set_limit(10)
        sql.add_join('JOIN other_table ON my_table.id = other_table.id')
        sql.add_join('JOIN other_table ON my_table.id = other_table.id')
        sql.remove_with('with_1')
        result = str(sql)
        expected_sql = 'WITH with_2 AS (SELECT * FROM other_table)\nSELECT column_1, column_2 FROM my_table JOIN other_table ON my_table.id = other_table.id JOIN other_table ON my_table.id = other_table.id WHERE column_1 > 5 LIMIT 10'
        self.assertEqual(result, expected_sql)

    def test_create_sql_used_in_with(self):
        table_name_1 = 'my_with_table'
        columns_1 = ['column_with_1', 'column_with_2']
        sql_1 = sql_helper.SQL(table_name_1, columns_1)
        sql_1_result = str(sql_1)
        expected_sql_1 = 'SELECT column_with_1, column_with_2 FROM my_with_table'
        self.assertEqual(sql_1_result, expected_sql_1)
        table_name = 'my_table'
        columns = ['column_1', 'column_2']
        sql = sql_helper.SQL(table_name, columns)
        sql.add_with('with_1', sql_1)
        sql.add_with('with_2', 'SELECT * FROM other_table')
        sql.set_where('column_1 > 5')
        sql.set_limit(10)
        sql.add_join('JOIN other_table ON my_table.id = other_table.id')
        result = str(sql)
        expected_sql = 'WITH with_1 AS (SELECT column_with_1, column_with_2 FROM my_with_table)\nWITH with_2 AS (SELECT * FROM other_table)\nSELECT column_1, column_2 FROM my_table JOIN other_table ON my_table.id = other_table.id WHERE column_1 > 5 LIMIT 10'
        self.assertEqual(result, expected_sql)


if __name__ == '__main__':
    unittest.main()
