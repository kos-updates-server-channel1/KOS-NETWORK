from datetime import datetime
import sqlite3
import ntpath # FILE NAME Extraction
import base64 # IMAGE URI Encoding
 
RECORD_PER_PAGE = 5

class DBSystem (wx.Frame):
    def __init__(self):

        # Database 초기화
        self.conn = sqlite3.connect("minutediary.db")
        self.cursor = self.conn.cursor()
        self.CheckSchema()
        self.LoadDiary(0)
                
    def CheckSchema(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS DIARY (
        DIARY_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        CREATEDATE DATETIME, 
        NOTE CHAR(140))
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS DIARY_IMG (
        IMG_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        IMG BLOB, 
        DIARY_ID INTEGER, 
        FOREIGN KEY(DIARY_ID) REFERENCES DIARY(DIARY_ID))
        """)

    def OnTypeText(self, event):
        self.lengthStaticText.SetLabel(
            "현재 글자 수 : {0}".format(len(self.inputTextCtrl.GetValue())))
        self.leftPanel.Layout()

    def OnFindImageFile(self, event):
        openFileDialog = wx.FileDialog(
            self, "Open", 
            wildcard="Image files (*.png, *.jpg, *.gif)|*.png;*.jpg;*.jpeg;*.gif",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_OK:
            self.input_image_path = openFileDialog.GetPath()
            
            # 비율을 유지하면서 이미지 크기를 윈도우에 맞추기
            img = wx.Image(self.input_image_path, wx.BITMAP_TYPE_ANY)
            Width = img.GetWidth()
            Height = img.GetHeight()
            if Width > Height:
                NewWidth = self.MaxImageSize
                NewHeight = self.MaxImageSize * Height / Width
            else:
                NewWidth = self.MaxImageSize
                NewHeight = self.MaxImageSize * Width / Height
            img = img.Scale(NewWidth, NewHeight)
            self.imageStaticBitmap.SetBitmap(wx.Bitmap(img))
            self.leftPanel.Layout()
            self.leftPanel.Refresh()
        
        openFileDialog.Destroy()

    def OnInputButton(self, event):
        fileName = ntpath.basename(self.input_image_path)
        self.cursor.execute(
            "INSERT INTO DIARY (DIARY_ID, CREATEDATE, NOTE) VALUES(NULL, ?, ? )", 
            (str(datetime.now()), self.inputTextCtrl.GetValue()))

        diary_id = self.cursor.lastrowid

        if self.input_image_path.strip() != "":
            self.cursor.execute(
                "INSERT INTO DIARY_IMG (IMG_ID, IMG, DIARY_ID) VALUES(NULL, ?, ?)",
                (sqlite3.Binary(open(self.input_image_path,"rb").read()), 
                 diary_id))
        
        self.conn.commit()

        wx.MessageBox("저장되었습니다.", "140자 일기장", wx.OK) 

        self.inputTextCtrl.SetValue("")        
        self.input_image_path = ""
        self.imageStaticBitmap.SetBitmap(wx.Bitmap(0,0))

        self.leftPanel.Layout()
        self.leftPanel.Refresh()
        self.LoadDiary(0)

    def LoadDiary(self, page):
        self.cursor.execute(
            "SELECT D.DIARY_ID, D.CREATEDATE, D.NOTE, I.IMG FROM DIARY "
            + "AS D LEFT OUTER JOIN DIARY_IMG AS I "
            + "ON D.DIARY_ID = I.DIARY_ID ORDER BY D.CREATEDATE DESC "
            + "LIMIT {0} OFFSET {1}"
            .format(RECORD_PER_PAGE, page*RECORD_PER_PAGE))

        html = """
            <html>
            <head>
            </head><body>{0}</body></html>
            """
        diary_id = 0
        body = ""
        for row in self.cursor:
            diary_id = int(row[0]);
            imgTag = ""
            if row[3] != None:
                imgTag = """<img src='data:image/png;base64,{0}' 
                style='width:300px; height:auto;' align=center>
                """.format(
                    base64.b64encode(row[3]).decode("ascii")
                    )

            content = """<a name="neural">
                <p style="word-wrap:break-word;font-size=12px;">
                <font size=2><b><i>
                {1}
                </i></b>
                <a href="del:{0}">[삭제]</a></font><br>
                {2}
                <br>
                {3}
                """.format(diary_id, row[1], row[2], imgTag)
            body += content

        pageNavigation = "<p align='center' style='font-size=12px'>"
        
        # Prev 버튼(링크)
        if page > 0:
            pageNavigation += "<a href='nav:{0}'>Prev</a>".format(page - 1)
        
        pageNavigation += "&nbsp;"

        # Next 버튼(링크)
        self.cursor.execute(
            "SELECT count(*) FROM DIARY WHERE DIARY_ID<{0}".format(diary_id))
        row = self.cursor.fetchone() 
        
        if row != None:
            nextRowCount = row[0]
            if nextRowCount > 0:
                pageNavigation += "<a href='nav:{0}'>Next</a>".format(page + 1)

        pageNavigation += "</p>"
        body += pageNavigation

        self.outputHtmlWnd.SetPage(html.format(body), "")

if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame()
    frame.Show()

    app.MainLoop()