from PyQt5 import QtWidgets, QtSql

class Data:
    def __init__(self):
        super(Data, self).__init__()
        self.create_connection()

    def create_connection(self):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('my_results_db.db')

        if not db.open():
            QtWidgets.QMessageBox.critical(None, 'Cannot open database',
                                           'Click Cancel to exit', QtWidgets.QMessageBox.Cancel)
            return False

        query = QtSql.QSqlQuery()
        query.exec('CREATE TABLE IF NOT EXISTS results (ID integer primary key AUTOINCREMENT, '
                   'Level VARCHAR(20), Date VARCHAR(20), Time VARCHAR(20))')
        return True

    def execute_query_with_params(self, sql_query, query_values=None):
        query = QtSql.QSqlQuery()
        query.prepare(sql_query)

        if query_values is not None:
            for query_value in query_values:
                query.addBindValue(query_value)

        query.exec()
        return query

    def add_new_result_query(self, level, date, time):
        sql_query = 'INSERT INTO results (Level, Date, Time) VALUES (?, ?, ?)'
        self.execute_query_with_params(sql_query, [level, date, time])

    def update_result_query(self, level, date, time, id):
        sql_query = 'UPDATE results SET Level=?, Date=?, Time=? WHERE ID=?'
        self.execute_query_with_params(sql_query, [level, date, time, id])

    def get_level(self, level):
        sql_query = 'SELECT * FROM results WHERE Level=?'
        query = self.execute_query_with_params(sql_query, [level])

        if query.next():
            return query.value('ID'), query.value('Date'), query.value('Time')

        return False