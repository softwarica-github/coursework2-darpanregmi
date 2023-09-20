from distutils.log import error
import pymysql

# Connect with MySQL database    -Host Name     -PORT No.   -UserName    -Password    -Create database named `votingsystem`
mydb = pymysql.connect(host="localhost", port=3306, user="root", password="", database="votingsystem")


def connect():
    try:
        print("--------------------------------------------------")
        mycursor = mydb.cursor()
        mycursor.execute("""CREATE TABLE vote (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                voter_id VARCHAR(20) NOT NULL UNIQUE, 
                                poll VARCHAR(50) NOT NULL, 
                                district VARCHAR(50) NOT NULL)""")
        mycursor = mydb.cursor()
        mycursor.execute("""CREATE TABLE voters (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                voter_id VARCHAR(20) NOT NULL UNIQUE, 
                                name VARCHAR(50) NOT NULL,
                                citizenship VARCHAR(12) NOT NULL UNIQUE,
                                phone VARCHAR(10) NOT NULL UNIQUE,
                                district VARCHAR(50) NOT NULL,
                                gender VARCHAR(20) NOT NULL,
                                password VARCHAR(100) NOT NULL UNIQUE,
                                cpassword VARCHAR(100) NOT NULL)""")
        mycursor = mydb.cursor()
        mycursor.execute("""CREATE TABLE admin (
                               id INTEGER PRIMARY KEY,
                               username TEXT NOT NULL UNIQUE,
                               password TEXT NOT NULL,
                               confirm_password TEXT NOT NULL)""")
        print("[DONE]   BUILD SUCCESSFULLY!!")
        print("--------------------------------------------------")
    except:
        print("[DONE]   CONNECTED SUCCESSFULLY!!")
        print("--------------------------------------------------")

def get_admin_details(username, password):
    """Function to fetch the admin's details from the database."""
    try:
        mycursor = mydb.cursor()
        sql = "SELECT  * FROM admin WHERE username=%s AND password=%s"
        mycursor.execute(sql, (username, password))
        result = mycursor.fetchone()
        return result
    except Exception as e:
        print("[WARN]   Failed to fetch admin details:", e)
        return None

def findByCitizenship(citizenship):
    try:
        mycursor = mydb.cursor()
        sql = "SELECT  * FROM voters WHERE citizenship='%s'"%citizenship
        mycursor.execute(sql)
        result = mycursor.fetchone()
        return result
    except:
        print("[WARN]   Failed to find user by citizenship no")

def findByCitizenships(citizenship):
    try:
        mycursor = mydb.cursor()
        sql = "SELECT citizenship, name, phone, district, gender FROM voters WHERE citizenship=%s"
        mycursor.execute(sql, (citizenship, ))
        result = mycursor.fetchone()
        return result
    except Exception as e:
        error("[WARN]   Failed to find user by citizenship no: " + str(e))

def findByVoterId(voterId):
    try:
        mycursor = mydb.cursor()
        sql = "SELECT  * FROM voters WHERE voter_id='%s'"%voterId
        mycursor.execute(sql)
        result = mycursor.fetchone()
        return result
    except:
        print("[WARN]   Failed to find user by Voter ID")

def findByVoterIdAndPassword(voterId, password1):
    try:
        mycursor = mydb.cursor()
        sql = "SELECT  * FROM voters WHERE voter_id=%s AND password=%s"
        mycursor.execute(sql, (voterId, password1))
        result = mycursor.fetchone()
        return result
    except Exception as e:
        error("[WARN]   Failed to find user by Voter ID: {}".format(str(e)))


def addVoter(voterId, name, citizenship, phone, district, gender, password, cpassword):
    try:
        mycursor = mydb.cursor()
        sql = "INSERT INTO voters(voter_id, name, citizenship, phone, district, gender, password, cpassword) VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')".format(voterId, name, citizenship, phone, district, gender, password, cpassword)
        mycursor.execute(sql)
        mydb.commit()
        return True
    except:
        print("[WARN]   User Record failed to register")
        return False


def submitVote(voterId, poll, district):
    try:
        mycursor = mydb.cursor()
        sql = "INSERT INTO vote(voter_id, poll, district) VALUES('{0}', '{1}', '{2}')".format(voterId, poll, district)
        mycursor.execute(sql)
        mydb.commit()
        return True
    except:
        print("[WARN]   Unable to submit Vote")
        return False


def findByVoterIdinVote(voterId):
    try:
        mycursor = mydb.cursor()
        sql = "SELECT  * FROM vote WHERE voter_id='%s'"%voterId
        mycursor.execute(sql)
        result = mycursor.fetchone()
        return result
    except:
        error("[WARN]   Error during finding voter from vote entity")


def getTotalCount():
    try:
        mycursor = mydb.cursor()
        sql = "SELECT count(*) FROM vote"
        mycursor.execute(sql)
        result = mycursor.fetchone()
        return result
    except:
        error("[WARN]   Error while fetching total vote count")


def getTotalUserCount():
    try:
        mycursor = mydb.cursor()
        sql = "SELECT count(*) FROM voters"
        mycursor.execute(sql)
        result = mycursor.fetchone()
        return result
    except:
        error("[WARN]   Error while fetching total user count")


def getPartyCount(party):
    try:
        mycursor = mydb.cursor()
        sql = "SELECT count(*) FROM vote WHERE poll like '%{0}%'".format(party)
        mycursor.execute(sql)
        result = mycursor.fetchall()
        return result
    except:
        print("[WARN]   Error while fetching party count")


def getallVoters():
    try:
        mycursor = mydb.cursor()
        sql ="""SELECT voters.voter_id, voters.name, voters.citizenship, voters.phone, voters.gender, voters.district, IF(vote.voter_id IS NULL, 'Not Voted', 'Voted') AS voted_status, vote.district
                FROM voters
                LEFT JOIN vote ON voters.voter_id=vote.voter_id;"""
        mycursor.execute(sql)
        result = mycursor.fetchall()
        return result
    except Exception as e:
        print("[WARN] Failed to fetch all Voters record:", e)
        return []


def getUserByCitizenship(citizenship):
    try:
        mycursor = mydb.cursor()
        sql ="""SELECT voters.name, voters.phone, voters.gender, voters.district
                FROM voters
                LEFT JOIN vote ON voters.voter_id=vote.voter_id
                WHERE citizenship = '{0}'""".format(citizenship)
        mycursor.execute(sql)
        result = mycursor.fetchone()
        return result
    except:
        print("[WARN]   Failed to fetch user by citizenship no.")


def updateUserByCitizenship(name, phone, gender, district, citizenship):
    try:
        mycursor = mydb.cursor()
        sql ="""UPDATE voters SET name='{0}', phone='{1}', gender='{2}', district='{3}' 
                WHERE citizenship='{4}'""".format(name, phone, gender, district, citizenship)
        mycursor.execute(sql)
        mydb.commit()
        return True
    except:
        print("[WARN]   Failed to update user record")
        return False


def deleteUserByCitizenship(citizenship):
    try:
        mycursor = mydb.cursor()
        sql ="""DELETE FROM voters
                WHERE citizenship = '{0}'""".format(citizenship)
        mycursor.execute(sql)
        mydb.commit()
        return True
    except:
        print("[WARN]   Failed to delete user")
        return False
