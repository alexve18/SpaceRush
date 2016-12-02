import mysql.connector
from mysql.connector import errorcode

class connection:
    def CheckConnection(self):
        cnx = mysql.connector.connect(user='2410982069', password='pass.123', host="tsuts.tskoli.is", database='2410982069_pygame')
        try:
            cnx
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            cnx.close()

    def newScorer(self, name, score):
        cnx = mysql.connector.connect(user='2410982069', password='pass.123', host="tsuts.tskoli.is", database='2410982069_pygame')

        cursor = cnx.cursor()
        query = ('Call AddPlayer("{}", {});'.format(name, str(score)))
        cursor.execute(query)
        cnx.commit()
        cursor.close()
        cnx.close()

    def Display(self):
        result = []
        cnx = mysql.connector.connect(user='2410982069', password='pass.123', host="tsuts.tskoli.is",database='2410982069_pygame')

        cursor = cnx.cursor()
        query = ('select * from TopPlayers order by playerPoints desc;')
        cursor.execute(query)
        for id, name, score in cursor:
            result.append(str(name) + ': ' + str(score))
        cursor.close()
        cnx.close

        return result

conn = connection()
conn.CheckConnection()