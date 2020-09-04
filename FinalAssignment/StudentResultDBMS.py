import bcrypt
import mysql.connector


class DBMS_Connection:
    def __init__(self):
        self.db = mysql.connector.connect(host="localhost",
                                          user="root",
                                          passwd="",
                                          database="result_management")
        self.my_cursor = self.db.cursor()

    def get_faculty(self, un):

        """This method returns the faculty of a user"""

        self.my_cursor.execute('SELECT faculty FROM users WHERE username=%s', (un,))
        return self.my_cursor.fetchone()[0]

    def get_username(self, un):

        """This method returns a value greater than 1 if a username exists in database"""

        self.my_cursor.execute('SELECT COUNT(*) FROM users WHERE username=%s', (un,))
        x = self.my_cursor.fetchone()
        if x[0] > 0:
            return True
        else:
            return False

    def show_username(self):

        """This method returns all the username of students"""

        self.my_cursor.execute('select username from users where faculty="student"')
        x = self.my_cursor.fetchall()
        return x

    def get_password(self, un):

        """This method returns the password of the specified user"""

        self.my_cursor.execute('SELECT password FROM users WHERE username=%s', (un,))
        x = self.my_cursor.fetchone()[-1]
        return x

    def store_credentials(self,nm, fc, un, pw):

        """"""
        self.my_cursor.execute('INSERT INTO users (name, faculty, username, password) VALUES (%s,%s,%s,%s)',
                               (nm, fc, un, pw))
        self.db.commit()

    def store_results(self, un, sn, sc, om):
        self.my_cursor.execute('insert into result (username,name, sub_code, obt_marks) values (%s,%s,%s,%s)',
                               (un, sn, sc, om))
        self.db.commit()

    def get_result(self, un):
        self.my_cursor.execute('select * from result where username=%s', (un,))
        x = self.my_cursor.fetchall()
        return x

    def show_result(self):

        """This method returns everything"""

        self.my_cursor.execute('select username,name,sub_code,obt_marks from result ')
        x = self.my_cursor.fetchall()
        return x

    def show_name(self, un):
        self.my_cursor.execute('select name from users where username=%s', (un,))
        x = self.my_cursor.fetchone()[0]
        return x


class Register:
    def __init__(self, nm, un, pw, fc):
        self.name = nm
        self.password = pw
        self.username = un
        self.faculty = fc

    def check_username(self):
        connection = DBMS_Connection()
        x = connection.get_username(self.username)
        if not x:
            # self.hash_password() --- > for hashing
            connection.store_credentials(self.name, self.faculty, self.username, self.password)  # for plaintext pw
        return x

    def hash_password(self):
        connection = DBMS_Connection()
        salt = bcrypt.gensalt()
        encoded_pw = self.password.encode('utf-8')
        hashed = bcrypt.hashpw(encoded_pw, salt)
        connection.store_credentials(self.username, hashed)


class Login:
    def __init__(self, un, pw):
        self.username = un
        self.password = pw

    def check_username(self):
        connection = DBMS_Connection()
        return connection.get_username(self.username)

    def check_password(self):
        connection = DBMS_Connection()
        DBMS_password = connection.get_password(self.username)
        if DBMS_password == self.password:
            return connection.get_faculty(self.username)
        else:
            return False

        # enc_password = self.password.encode('utf-8')
        # hashed = DBMS_Connection().get_password(self.username)
        # hashed = bytes(hashed, encoding='utf-8')
        # print(hashed)
        # return bcrypt.checkpw(enc_password, hashed)


class Result:
    def __init__(self, un, sn, sc, om):
        self.username = un
        self.Student_name = sn
        self.subject_code = sc
        self.obtained_marks = om

    def check_username(self):
        connection = DBMS_Connection()
        return connection.get_username(self.username)

    def store_result(self):
        connection = DBMS_Connection()
        connection.store_results(self.username, self.Student_name, self.subject_code, self.obtained_marks)

    def get_result(self):
        connection = DBMS_Connection()
        result = connection.get_result(self.username)
        return result

# test = DBMS_Connection()
# test.show_name('student')
