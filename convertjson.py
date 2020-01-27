import os, sqlite3, json, time, re
from sys import argv
start_time = time.perf_counter()
script, filename = argv

def run():
    os.chdir("D:\\sqllogs\\")
    sqldb = "bro.db"
    conn = sqlite3.connect(sqldb)
    file = open("D:\\broLogs\\total\\" + filename + ".log")
    with file as f:
        try:
            c = conn.cursor()
            print("Successfully connected to: " + sqldb)
            holder = []
            keylist = []
            jsdata = []
            line = f.readline()
            jsline = json.loads(line)
            holder.append(jsline.keys())
            for d in holder[0]:
                r = re.sub(r'([a-z_]+)\.([a-z_]+)',r'\1_\2',d)
                keylist.append(r)
            
            create_table = 'CREATE TABLE ' + filename + '(id INT PRIMARY KEY, ' + ', '.join(keylist) +');'
            c.execute(create_table)
            for line in f:
                try:
                    jsdata = []
                    jsline = json.loads(line)
                    for p, i in enumerate(keylist):
                        x = jsline.get(keylist[p])
                        jsdata.append(str(x))
                    query = "INSERT INTO " + filename + "(" + ", ".join(keylist) + ") VALUES(\"" + "\", \"".join(jsdata) + "\");"
                    c.execute(query)
                except sqlite3.Error as error:
                    print("Failed to insert data into sqlite table", error)
    
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if (conn):
                conn.commit()
                conn.close()
                print("The SQLite connection is closed")
run()
print(time.perf_counter() - start_time, "seconds")
