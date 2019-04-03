# -*- coding: utf-8 -*-
import wx
import sys, traceback
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
"""
Control que permite visualizar una lista o tabla de datos
"""

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class JkListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
  def __init__(self, parent, headers):
    wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT|wx.BORDER_SUNKEN)
    ListCtrlAutoWidthMixin.__init__(self)
    ie=0
    self.headers=headers[:]
    for i in headers:
      self.InsertColumn(ie, i, width=130)
      ie+=1

  def ClearHeaders(self):
    self.headers[:]=[]
  
  def AddColumnData(self,nColumn,data):
    """Número de columna, y una lista con los datos a insertar
      Actualiza los datos de la columna con los nuevos datos suministrados
      en data.
    """
    numRows = self.GetItemCount()
    numData = len(data)
    print u'Número de datos a agregar: '+ str(numData)
    ie=0
    for string in data:
      if ie == numRows:
        val = self.InsertStringItem(sys.maxint, '')
        numRows+=1
      self.SetStringItem(ie, nColumn, string)
      ie+=1
    #Borra los espacios que quedan sin rellenar datos
    if ie < numRows:
      for row in range(numRows)[ie:]:
        self.SetStringItem(row, nColumn, '')
