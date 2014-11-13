import sqlite3

conn = sqlite3.connect('20140127MnemosynelogsAll.db')

function list_user_ids():
    c = conn.cursor()
    c.execute(




