import mysql.connector
from mysql.connector import Error
import random


def jSON(res, column):
    data = []
    for val in res:
        m = {}
        for x, col in zip(val, column):
            m[col] = x
        data.append(m)
    return data


class APPSql():
    def __init__(self, db):
        self.username = "root"
        self.hostname = "localhost"
        self.password = "12345908527"
        self.db = db
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                user=self.username,
                host=self.hostname,
                passwd=self.password,
                database=self.db
            )
            print("Connected Successfully")
        except Error as e:
            print(f"Error:{e}")

    def read_query(self, query, params):
        cursor = self.connection.cursor(dictionary=True)
        results = None
        try:
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
        except Error as e:
            print("Error: ", e)

    def insert_query(self, query, params):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
            return True
        except Error as err:
            print(f"Error:{err}")
            return False

    def call_storedproc(self, storedName, params):
        cursor = self.connection.cursor(dictionary=True)
        results = []
        try:
            cursor.callproc(storedName, params)
            for res in cursor.stored_results():
                results.extend(res.fetchall())
            return results
        except Error as err:
            print(f"Error: {err}")

    def close_connection(self):
        self.connection.close()


if __name__ == "__main__":

    # results = connection.read_query("SELECT * FROM posts")
    # random_number = random.randint(1, len(results))
    # final_results = [i for i in results if i["ID"] == random_number]
    # print(final_results)

    connection = APPSql("SocialMedia")
    results = connection.read_query("SELECT * FROM Posts", ())
    random_number = random.randint(1, len(results))
    final_results = [results[random_number]]
    print(final_results)
    connection.close_connection()