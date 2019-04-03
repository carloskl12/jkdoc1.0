# -*- coding: utf-8 -*-

import wx
from src import CampoCtrl, LIST_LANGUAGES, Respuesta, TextCtrlAutoComplete
from datetime import datetime
"""
Widget en el cual se ingresan los datos sobre un fragmento de código
"""

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class BusquedaDeDatos(wx.Frame):
  def __init__(self, parent, id=-1, title='Nueva Busqueda',optionsSearch=''):

    self.optionsSearch=optionsSearch
    self.respuesta=Respuesta( lenguaje='', lib='',version='')
    self._title=title
    #title= 'id: %i - %s'%(self.respuesta.idr,title)
    wx.Frame.__init__(self, parent, id, title, size=(550, 250))

    self.InitUI()
    self.Centre()
    self.Show(True)
    
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def InitUI (self):
    panel = wx.Panel(self)
    self.panel=panel
    self.CreateToolbar()

    vbox = wx.BoxSizer(wx.VERTICAL)
    panel.SetSizer(vbox)
    vbox.Add(self.toolbar,0,wx.EXPAND,border=5)
    ops=self.optionsSearch
    self.descripcionCtrl=CampoCtrl(panel,label='Descripción:',sizeInput=(-1,-1) )
    print ops.lenguaje
    self.lenguajeCtrl= CampoCtrl(panel, label='Lenguaje:', choices=ops.lenguaje)
    self.versionCtrl=CampoCtrl(panel,label='Versión:',choices=ops.version, sizeInput=(200,-1) )
    self.libCtrl=CampoCtrl(panel,label='Librería:',choices=ops.lib, sizeInput=(200,-1) )

    hboxA= wx.BoxSizer(wx.HORIZONTAL)
    hboxA.Add((15,-1))
    hboxA.Add(self.lenguajeCtrl)
    hboxA.Add((5,-1))
    hboxA.Add(self.versionCtrl)
    hboxA.Add((5,-1))
    hboxA.Add(self.libCtrl)
    
    self.verboCtrl=CampoCtrl(panel,label='Verbo:',choices=ops.verbo)
    self.sustACtrl=CampoCtrl(panel,label='SustantivoA:',choices=ops.sustantivoA,sizeInput=(200,-1) )
    self.sustBCtrl=CampoCtrl(panel,label='SustantivoB:',choices=ops.sustantivoB,sizeInput=(200,-1) )
    
    hboxB= wx.BoxSizer(wx.HORIZONTAL)
    hboxB.Add((15,-1))
    hboxB.Add(self.verboCtrl)
    hboxB.Add((5,-1))
    hboxB.Add(self.sustACtrl)
    hboxB.Add((5,-1))
    hboxB.Add(self.sustBCtrl)
    

    vbox.Add((-1,10))
    vbox.Add(self.descripcionCtrl, 0, wx.EXPAND | wx.LEFT|wx.RIGHT,15)
    
    vbox.Add((-1,10))
    vbox.Add(hboxB)
    vbox.Add((-1,10))
    vbox.Add(hboxA)

    #*******************Inicializa valores segun la respuesta 
    for i, ctrl in zip(range(1,8),(self.lenguajeCtrl, self.versionCtrl, self.libCtrl,
    self.verboCtrl, self.sustACtrl, self.sustBCtrl, self.descripcionCtrl)):
      ctrl.SetValue(self.respuesta[i])

    self.btBuscar = wx.Button(panel, label='Buscar')
    #self.Bind(wx.EVT_BUTTON,self.GetAnswer,self.btBuscar)
    vbox.Add((-1,10))
    vbox.Add(self.btBuscar, 0, wx.ALIGN_RIGHT|wx.RIGHT, 15)
    vbox.Add((-1,10))
  
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def CreateToolbar(self):
    #************************************
    #************* BARRA DE HERRAMIENTAS
    self.toolbar = wx.ToolBar(self.panel, -1, style= wx.TB_HORIZONTAL)
    self.toolbar.AddSeparator()
    self.tlFindAnswer = self.toolbar.AddLabelTool(-1, '', wx.Bitmap('icons/findAsk.png'))
    self.tlNewAnser = self.toolbar.AddLabelTool(-1, '', wx.Bitmap('icons/newAsk.png'))
    self.toolbar.AddSeparator()
    self.toolbar.Realize()

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def GetQuestion(self,e=-1):
    
    for i, ctrl in zip(range(1,8),(self.lenguajeCtrl, self.versionCtrl, self.libCtrl,
    self.verboCtrl, self.sustACtrl, self.sustBCtrl, self.descripcionCtrl)):
      self.respuesta[i]=ctrl.GetValue().encode('utf-8')
    
    self.respuesta.fecha= datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return self.respuesta

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def ClearData(self,idr=0,modo=0):
    """
      Borra los datos mostrados parcialmente si el modo es cero
    """
    self.verboCtrl.SetValue('')
    self.sustACtrl.SetValue('')
    self.sustBCtrl.SetValue('')
    self.descripcionCtrl.SetValue('')
    self.respuesta.fecha=''
    self.respuesta.puntos=0
    self.respuesta.idr=idr
    title= self._title
    self.SetTitle(title)

  def InfoText(self, message, caption='Information !'):
    dlg = wx.MessageDialog(self, message, caption)
    dlg.ShowModal()


