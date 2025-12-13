from typing import List, Union


class SQL:

    def __init__(self, table_name: str, columns: List[str]):
        """
        A helper class for building SQL queries.

        Args:
            table_name (str): The name of the table to query.
            columns (list): A list of columns to select.

        Examples:
            >>> sql = SQL('my_table', ['column_1', 'column_2'])
            >>> print(sql)
            SELECT column_1, column_2 FROM my_table
        """
        self.table_name = table_name
        self.columns = columns
        self.with_statements = []
        self.join_statements = []
        self.where_statement = None
        self.order_by = None
        self.limit = None
        self._sql = None

    def add_join(self, join_statement: str):
        """
        Adds a JOIN statement to the query.

        Args:
            join_statement (str): The JOIN statement to add.

        Examples:
            >>> sql = SQL('my_table', ['column_1', 'column_2'])
            >>> sql.add_join('JOIN other_table ON my_table.id = other_table.id')
            >>> print(sql)
            SELECT column_1, column_2 FROM my_table JOIN other_table ON my_table.id = other_table.id
        """
        self.join_statements.append(join_statement)
        self._sql = None

    def add_with(self, name: str, statement: str):
        """
        Adds a WITH statement to the query.

        Args:
            name (str): The name of the WITH statement.
            statement (str): The statement to add.

        Examples:
            >>> sql = SQL('my_table', ['column_1', 'column_2'])
            >>> sql.add_with('with_1', 'SELECT * FROM other_table')
            >>> sql.add_with('with_2', 'SELECT * FROM other_table')
            >>> print(sql)
            WITH with_1 AS (SELECT * FROM other_table)
            WITH with_2 AS (SELECT * FROM other_table)
            SELECT column_1, column_2 FROM my_table
        """
        for x in self.with_statements:
            if x[0] == name:
                raise ValueError(f'Name {name} already exists.')
        self.with_statements.append((name, statement))
        self._sql = None

    def remove_with(self, name: str):
        """
        Removes a WITH statement from the query.

        Args:
            name (str): The name of the WITH statement to remove.
        """
        self.with_statements = [x for x in self.with_statements if x[0] != name]
        self._sql = None

    def set_where(self, where_statement: str):
        """
        Sets the WHERE statement for the query.

        Args:
            where_statement (str): The WHERE statement to set.

        Examples:
            >>> sql = SQL('my_table', ['column_1', 'column_2'])
            >>> sql.set_where('column_1 > 5')
            >>> print(sql)
            SELECT column_1, column_2 FROM my_table WHERE column_1 > 5
        """
        self.where_statement = where_statement
        self._sql = None

    def set_limit(self, limit: Union[int, None]):
        """
        Sets the LIMIT statement for the query.

        Args:
            limit (int | None): The LIMIT statement to set.

        Examples:
            >>> sql = SQL('my_table', ['column_1', 'column_2'])
            >>> sql.set_limit(10)
            >>> print(sql)
            SELECT column_1, column_2 FROM my_table LIMIT 10
        """
        self.limit = limit
        self._sql = None

    def set_order_by(self, order_by: str):
        """
        Sets the ORDER BY statement for the query.

        Args:
            order_by (str): The ORDER BY statement to set.

        Examples:
            >>> sql = SQL('my_table', ['column_1', 'column_2'])
            >>> sql.set_order_by('column_1 DESC')
            >>> print(sql)
            SELECT column_1, column_2 FROM my_table ORDER BY column_1 DESC
        """
        self.order_by = order_by
        self._sql = None

    def _generate_sql(self):
        if self._sql is None:
            self._sql = ''
            for name, statement in self.with_statements:
                self._sql += f'WITH {name} AS ({statement})\n'
            self._sql += f'SELECT {", ".join(self.columns)} FROM {self.table_name}'
            if self.join_statements:
                for join_statement in self.join_statements:
                    self._sql += f' {join_statement}'
            if self.where_statement is not None:
                self._sql += f' WHERE {self.where_statement}'
            if self.order_by is not None:
                self._sql += f' ORDER BY {self.order_by}'
            if self.limit is not None:
                self._sql += f' LIMIT {self.limit}'
        return self._sql

    def __str__(self):
        """
        Returns the SQL query.
        """
        return self._generate_sql()
