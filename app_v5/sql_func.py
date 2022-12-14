import sqlite3   #enable control of an sqlite database
# import os      # imported to be able to test without running into errors

# os.system('rm -rf blog_database.db') # this is to delete the dataframe file as to not encounter any errors during testing

# opens a connection with sql3 
def open_connection():
    db = sqlite3.connect('blog_database.db') #open if file exists, otherwise create
    c = db.cursor() # creates cursor object to pass commands to the database
    return (db,c) # returns the cursor and databse so that can be used when manipulating the database
    
# saves the database and closes the connection
def close_connection(db):
    db.commit() #save changes
    db.close()  #close database

'''THIS FUNCTION SHOULD NEVER BE RUN, ALL TABLES SHOULD BE CREATED MANUALLY BEFORE THEY ARE USED'''

'''
STRUCTURE OF THE DATABASES (SPECS):

USERNAMES(username NOT NULL PRIMARY KEY,password)
BLOGS(blog_id PRIMARY KEY, author NOT NULL,title NOT NULL,post_date NOT NULL,content_description,content_body)
'''
# creates table if and only it doesn't exist yet (should only be used at initiation)
# def create_table(table_name,data: tuple):
#     db,c = open_connection() # open connection

#     # runs the commands to create the table (using question marks)
#     c.execute(f'''create table if not exists {table_name}({",".join(data)})''')

#     close_connection(db) # close and save


# adds an entry to a specific table that already exists
def add_entry(table_name,data: tuple):
    db,c = open_connection() # open connection

    # execute the command, and use sqls place holders
    c.execute(f'''insert into {table_name} values({("?,"*len(data))[:-1]})''',data)

    close_connection(db) # close and save




# read an entry from a specific table that already exists
def read_entry(table_name,query: tuple, *args):
    db,c = open_connection() # open connection

    # execute the command, and conconate the *args
    c.execute(f'''select {",".join(args)} from {table_name} where {query[0]} = "{query[1]}"''')
    ret_msg = c.fetchone()

    close_connection(db) # close and save
    
    return ret_msg

# edits an entry (only one) in a specific table (returns original entry)
def edit_entry(table_name,query: tuple, **kwargs):
    db,c = open_connection() # open connection

    column_list = list(kwargs.keys())
    entry_list = list(kwargs.values())

    # this is to return the orignal entries in their positions
    ret_msg = []
    for vals in column_list:
        ret_msg.append({vals:read_entry(table_name,query,vals)[0]})

    # to format the command
    inject_tmpl = ""
    for val in column_list:
        inject_tmpl += val + " = ?,"

    c.execute(f'''update {table_name} set {inject_tmpl[:-1]} where {query[0]} = "{query[1]}"''',entry_list)

    close_connection(db) # close and save
    return ret_msg

# deletes an entry and returns the original row
def delete_entry(table_name,data: tuple):
    db,c = open_connection() # open connection

    ret_msg = read_entry(table_name,data,"*")

    c.execute(f'''delete from {table_name} where {data[0]} = ?''', data[1])

    close_connection(db) # close and save
    return ret_msg


def entry_exists(table_name,data: tuple):
    db,c = open_connection() # open connection

    c.execute(f'''select exists( select {data[0]} from {table_name} where {data[0]} = "{data[1]}" )''');
    ret_msg = c.fetchone()[0]

    if ret_msg == 0:
        ret_msg = False
    else:
        ret_msg = True

    close_connection(db) # close and save
    return ret_msg



# add_entry("usernames",("kosta","pp"))
# add_entry("usernames",("aaron","pp"))
# print(entry_exists("usernames",("username","kosta")))





# if __name__ == "__main__":

#     create_table("blogs",(
#         "blog_id PRIMARY KEY NOT NULL", "author TEXT NOT NULL", "title TEXT NOT NULL", "post_date TEXT NOT NULL","content_description TEXT","content_body TEXT"
#         ))

#     create_table("usernames",("username TEXT NOT NULL PRIMARY KEY", "password TEXT NOT NULL"))

#     # add_entry("usernames",("drew","pp"))
#     add_entry("blogs",("1","drew","test","11/4/2022","this is a test","shout out my label / I'm in this ***** with TB"))


    # create_table("students",("name","id","date","gpa"))
    # add_entry("students",("andrew","9000","null","66%"))
    # add_entry("students",("kosta","9001","null","null"))
    # add_entry("students",("matt","001","null","null"))
    # add_entry("students",("bruv","8989","null","null"))
    # print(read_entry("students",("id",9000),"name","date","gpa"))

    # print(edit_entry("students",("id",9000),name="brotha",date="11/9/12",gpa="79%"))
    # print(read_entry("students",("id",9000),"name","date","gpa"))












