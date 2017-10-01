from datetime import datetime
import sqlite3
import ntpath # FILE NAME Extraction
import base64 # IMAGE URI Encoding
 
RECORD_PER_PAGE = 5

class DBSystem (wx.Frame):
    def __init__(self):

        # Database 초기화
        self.conn = sqlite3.connect("CrawlData.db")
        self.cursor = self.conn.cursor()
        self.CheckSchema()
        self.LoadDiary(0)

if __name__ == "__main__":
    app.MainLoop()