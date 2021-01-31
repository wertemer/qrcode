#!/usr/bin/python3
# -*- coding: utf-8 -*-
import wx
import os
import ftplib
import pyqrcode
class MainQR(wx.Frame):
    procmes=''
    def __init__(self,parent,title):
        #окно
        wx.Frame.__init__(self,parent,title='QR',size=(500,400),style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX)
        #panel для размещения элементов управления, auto tab
        panel = wx.Panel(self, -1)
        #цвет окна
        self.SetBackgroundColour((220, 220, 220))
        wx.StaticText(panel, -1, "Хост", style=wx.ALIGN_LEFT,pos=(10,10))
        self.host=wx.TextCtrl(panel,id=1,pos=(35,5),size=(100,20)) 
        wx.StaticText(panel, -1, "Пользователь", style=wx.ALIGN_LEFT,pos=(140,10))
        self.user=wx.TextCtrl(panel,id=2,pos=(215,5),size=(100,20))
        wx.StaticText(panel, -1, "Пароль", style=wx.ALIGN_LEFT,pos=(320,10))
        self.pasw=wx.TextCtrl(panel,id=3,pos=(360,5),size=(130,20),style=wx.TE_PASSWORD)
        #open apk
        self.btnOpen=wx.Button(panel,label='Open',id=-1,pos=(390,60),size=(75,20))
        #help open
        self.btnHelpOpen=wx.Button(panel,label='Open',id=-1,pos=(390,90),size=(75,20),style=wx.TE_READONLY)
        #выбор apk
        wx.StaticText(panel, -1, "Файл:", style=wx.ALIGN_LEFT,pos=(10,60))
        self.path1=wx.TextCtrl(panel,pos=(85,60),size=(300,20),style=wx.TE_READONLY)
        #help pdf
        wx.StaticText(panel, -1, "Файл помощи:", style=wx.ALIGN_LEFT,pos=(10,95))
        self.path2=wx.TextCtrl(panel,pos=(85,90),size=(300,20),style=wx.TE_READONLY)
        #Описание изменений
        wx.StaticText(panel, -1, "Внесенные изменения:", style=wx.ALIGN_LEFT,pos=(10,125))
        self.change=wx.TextCtrl(panel,pos=(10,140),size=(480,200),style=wx.TE_MULTILINE)
        #кнопки
        self.btnOk=wx.Button(panel,label="Ok",id=-1,pos=(285,350),size=(100,20))
        self.btnCancel=wx.Button(panel,label='Cancel',id=-1,pos=(390,350),size=(100,20))
        #события кнопок
        self.Bind(wx.EVT_BUTTON,self.OnOpenFile,self.btnOpen)
        self.Bind(wx.EVT_BUTTON,self.OnStop,self.btnCancel)
        self.Bind(wx.EVT_BUTTON,self.OnOk,self.btnOk)
        self.Bind(wx.EVT_BUTTON,self.OnOpenHelp,self.btnHelpOpen)
        self.Show(True)
    #выбираем файл
    def OnOpenFile(self,event):
        #Диалог открытия файлов
        dialog = wx.FileDialog(self, "Choose a file", os.getcwd(),"", "*.apk")
        if dialog.ShowModal() == wx.ID_OK:
            #выводим путь файла
            self.path1.SetValue(dialog.GetPath())
        dialog.Destroy()
    #закрываем окно
    def OnStop(self,event):
        self.Close()
    #Сохраняем qr-код на disk
    def OnOk(self,event):
        self.procmes=''
        host=self.host.GetValue()
        usr=self.user.GetValue()
        pas=self.pasw.GetValue()
        fl=self.path1.GetValue()
        ch=self.change.GetValue()
        hlp=self.path2.GetValue()
        #Проверка заполнения полей
        mes=''
        if host=='':
            mes+=' Введите хост!'
            dlg = wx.MessageDialog(self,mes,"Error", wx.OK) 
            dlg.ShowModal()
            return 0
        if usr=='':
            mes+=' Введите пользователя!'
            dlg = wx.MessageDialog(self,mes,"Error", wx.OK) 
            dlg.ShowModal()
            return 0
        if pas=='':
            mes+=' Введите пароль!'
            dlg = wx.MessageDialog(self,mes,"Error", wx.OK) 
            dlg.ShowModal()
            return 0
        if fl=='':
            mes+=' Выберите APK файл!'
            dlg = wx.MessageDialog(self,mes,"Error", wx.OK) 
            dlg.ShowModal()
            return 0
        if ch=='':
            mes+=' Введите изменения в новой версии мобильного приложения!';
            dlg = wx.MessageDialog(self,mes,"Error", wx.OK) 
            dlg.ShowModal()
            return 0
        if hlp!='':
            self.UploadHelp(hlp,host,usr,pas)
        self.UpLoad(fl,host,usr,pas)
        self.QR(fl,host,usr,pas)
        self.Change(ch,fl,host,usr,pas)
        dlg = wx.MessageDialog(self,self.procmes,"Information", wx.OK)
        dlg.ShowModal()
    def OnOpenHelp(self,event):
        #Диалог открытия файлов
        dialog = wx.FileDialog(self, "Choose a file", os.getcwd(),"", "*.pdf")
        if dialog.ShowModal() == wx.ID_OK:
            #выводим путь файла
            self.path2.SetValue(dialog.GetPath())
        dialog.Destroy()
    #Загрузка файла apk на сервер
    def UpLoad(self,pfile,h,u,p):
        """
        pfile - полное имя файла
        h - ftp host
        u - ftp user
        p - ftp password
        m - message
        """
        i=pfile.rfind('\\')
        fname=pfile[i+1:len(pfile)]
        try:
            ftp=ftplib.FTP(h,u,p)
            ftp.cwd('/mobile/versions')
            # Открываем файл для передачи в бинарном режиме
            f=open(pfile,"rb")
            # Передаем файл на сервер
            send=ftp.storbinary("STOR "+fname,f)
            # Закрываем FTP соединение
            ftp.close()
            f.close()
            self.procmes+=' Загрузка завершена'+fname
        except:
            self.procmes+=' Ошибка передачи по FTP файла'+fname
            return 0
    #загрузка на сервер мануала мобильного приложения
    def UploadHelp(self,phelp,h,u,p):
        """
        phelp - полное имя файла мануала
        h - ftp host
        u - ftp user
        p - ftp password
        """
        i=phelp.rfind('\\')
        fname=phelp[i+1:len(phelp)]
        try:
            ftp=ftplib.FTP(h,u,p)
            ftp.cwd('/mobile/versions/helps')
            # Открываем файл для передачи в бинарном режиме
            f=open(phelp,"rb")
            # Передаем файл на сервер
            send=ftp.storbinary("STOR manual.pdf",f)
            # Закрываем FTP соединение
            ftp.close()
            f.close()
            self.procmes+=' Файл загружен : '+fname+'\n'
        except:
            self.procmes+=' Ошибка передачи по FTP файла'+fname+'\n'
            return 0
    #Генерация и сохранение qr-code на сервер
    def QR(self,pfile,h,u,p):
        i=pfile.rfind('\\')
        fname=pfile[i+1:len(pfile)]
        #удалаяем последние 4 символа
        fname=fname[:-4]
        pth='http://'+h+'/mobile/versions/'+fname+'.apk'
        try:
            url=pyqrcode.create(pth)
            url.svg('qr.svg',scale=4)
        except:
            dlg = wx.MessageDialog(self,'Ошибка генерации QR-кода',"Error", wx.OK) 
            dlg.ShowModal()
            return 0
        try:
            ftp=ftplib.FTP(h,u,p)
            ftp.cwd('/mobile/versions/QR')
            f=open('qr.svg','rb')
            send=ftp.storbinary('STOR '+fname+'.svg',f)
            ftp.close()
            f.close()
            self.procmes+=' QR - код сгенерирован и загружен на сервер\n'
        except:
            self.procmes+=' Ошибка генерации QR-кода '+fname+'.svg\n'
            return 0
    #Cохранение измененений в текстовый файл и сохранение этого файла на сервере
    def Change(self,txt,pfile,h,u,p):
        i=pfile.rfind('\\')
        fname=pfile[i+1:len(pfile)]
        #удалаяем последние 4 символа
        fname=fname[:-4]
        try:
            ftp=ftplib.FTP(h,u,p)
            ftp.cwd('/mobile/versions/changes')
            f=open('qr.txt','w',encoding='utf-8')
            txt.encode('UTF-8')
            f.write(txt)
            f.close()
            f1=open('qr.txt','rb')
            send=ftp.storbinary('STOR '+fname+'.txt',f1)
            ftp.close()
            f1.close()
            self.procmes+=' Файл измененеий загружен\n'
        except:
            self.procmes+=' Файл на загружен '+fname+'.txt\n'
            return 0
app=wx.App()
wnd=MainQR(None,'QR')
app.MainLoop()