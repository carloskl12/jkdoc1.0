# -*- coding: utf-8 -*-
import wx

class CheckListWin(wx.Frame):
  def __init__(self, parent, id, title, listData):
    wx.Frame.__init__(self, parent, id, title, size=(450, 400))
    panel = wx.Panel(self, -1)

    vbox = wx.BoxSizer(wx.VERTICAL)
    hbox = wx.BoxSizer(wx.HORIZONTAL)

    leftPanel = wx.Panel(panel, -1)
    rightPanel = wx.Panel(panel, -1)
    
    self.numItems= len(listData)-1
    self.log = wx.TextCtrl(rightPanel, -1, style=wx.TE_MULTILINE)
    self.list = CheckListCtrl(rightPanel)
    
    titulos = listData.pop(0)
    dim = len(titulos)
    print 'tipo de titulos: '+ str( type(titulos) != type (u'a'))
    variosDatos=True
    if type(titulos) != str and type(titulos) != type (u'a') :
      for t in titulos:
        self.list.InsertColumn(0, t, width=140)
    else:
      dim=1
      self.list.InsertColumn(0, titulos, width=140)
      variosDatos=False

    for i in listData:
      if variosDatos:
        index = self.list.InsertStringItem(sys.maxint, i[0])
        for element in range(len(i))[1:]:
          self.list.SetStringItem(index, element, i[element])
      else:
        index = self.list.InsertStringItem(sys.maxint, i)
        
    vbox2 = wx.BoxSizer(wx.VERTICAL)

    sel = wx.Button(leftPanel, -1, 'Seleccionar Todo', size=(150, -1))
    des = wx.Button(leftPanel, -1, 'Descartar Todo', size=(150, -1))
    self.apply = wx.Button(leftPanel, -1, 'Aplicar', size=(150, -1))
    self.Bind(wx.EVT_BUTTON, self.OnSelectAll, id=sel.GetId())
    self.Bind(wx.EVT_BUTTON, self.OnDeselectAll, id=des.GetId())
    self.listData=self.list.datosSel #Carga la lista de datos seleccionados
        
    vbox2.Add(sel, 0, wx.TOP, 5)
    vbox2.Add(des)
    vbox2.Add(self.apply)

    leftPanel.SetSizer(vbox2)

    vbox.Add(self.list, 1, wx.EXPAND | wx.TOP, 3)
    vbox.Add((-1, 10))
    vbox.Add(self.log, 0.5, wx.EXPAND)
    vbox.Add((-1, 10))

    rightPanel.SetSizer(vbox)

    hbox.Add(leftPanel, 0, wx.EXPAND | wx.RIGHT, 5)
    hbox.Add(rightPanel, 1, wx.EXPAND)
    hbox.Add((3, -1))

    panel.SetSizer(hbox)

    self.Centre()
    self.Show(True)

  def OnSelectAll(self, event):
    num = self.list.GetItemCount()
    for i in range(num):
      self.list.CheckItem(i)

  def OnDeselectAll(self, event):
    num = self.list.GetItemCount()
    for i in range(num):
      self.list.CheckItem(i, False)
