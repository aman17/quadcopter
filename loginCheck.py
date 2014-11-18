import psycopg2

try:
    conn = psycopg2.connect(database = "201201065", user = "201201065", password="201201065", host="10.100.71.21",port="5432")
    print "success"
except:
    print "I am unable to connect to the database"
cur = conn.cursor()
def get_ip(usrid):
    print type(usrid)
    cur.execute("SELECT * FROM cns.login")
    rows = cur.fetchall()
    print rows
    return rows
def login(usr,pwd):

    cur.execute("SELECT * FROM cns.loginData WHERE userId=%s and pwd=%s",(usr,pwd))
    rows = cur.fetchall()
    print "aman hello..."
    print rows
    
    for row in rows:
        print " ",row[0]," ",row[1]," ",row[2]
        a = row
        return a
    '''fh1 =open("list.txt","a+")
    #usr = raw_input("username: ")
    usr_data = usr
    #pwd = raw_input("password: ")
    pwd_data = pwd
    
    fh =open("list.txt","a+")
    acc = ""
    while 1:
        
        usr_name = fh.readline()
        usr_name = usr_name[:-1]
        if not usr_name:
            msg = 'username not found'        
            break
        pas = fh.readline()
        pas = pas[:-1]
        cat = fh.readline()
        cat = cat[:-1]
        if usr_name == usr_data:    
            if pas == pwd_data:
                #self.sock.send(cat)
                acc = cat
                
                break
            else :
                acc = 'incorrect password'
                msg = 'incorrect password /n please try again'
                break
    return acc'''
if __name__ == '__main__':
    print(login("chirag","mehta"))
