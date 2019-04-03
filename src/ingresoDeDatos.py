# -*- coding: utf-8 -*-

import wx
from src import CampoCtrl, LIST_LANGUAGES,lexer
from datetime import datetime
"""
Widget en el cual se ingresan los datos sobre un fragmento de código
"""

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%% Clase que encapsula una respuesta %%%%%%%%%%%%%%%%%%%%%%%%%
class Respuesta(object):
  def __init__(self,idr=0, lenguaje=LIST_LANGUAGES[0],version='Estandar', lib='Estandar',verbo='',
    sustantivoA='',sustantivoB='',descripcion='',codigo='',fecha='',puntos=0):
    '''
    Tener en cuenta que al alterar un solo indice de getitem, se debe modificar
    en ingreso datos la inicialización
    '''
    self.idr=idr
    self.lenguaje=lenguaje
    self.version=version
    self.lib=lib
    self.verbo= verbo 
    self.sustantivoA=sustantivoA
    self.sustantivoB=sustantivoB
    self.descripcion=descripcion
    self.codigo=codigo
    self.fecha=fecha
    self.puntos=puntos
    self.index=0

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def GetTuple(self):
    return (self.idr, self.lenguaje, self.version, self.lib, self.verbo,
      self.sustantivoA, self.sustantivoB, self.descripcion,self.codigo,
      self.fecha,self.puntos)

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def SetTuple(self,tupleData):
    (self.idr, self.lenguaje, self.version, self.lib, self.verbo,
      self.sustantivoA, self.sustantivoB, self.descripcion,self.codigo,
      self.fecha,self.puntos)=tupleData

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def __getitem__(self,i):
    data={
      0:self.idr,
      1:self.lenguaje,
      2: self.version,
      3: self.lib,
      4: self.verbo,
      5: self.sustantivoA,
      6: self.sustantivoB,
      7: self.descripcion,
      8: self.codigo,
      9: self.fecha,
      10: self.puntos}
    return data[i]

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def __setitem__(self, idx, value):
    if idx== 0:
      self.idr=value
    elif idx== 1:
      self.lenguaje=value
    elif idx== 2:
      self.version=value
    elif idx== 3:
      self.lib=value
    elif idx== 4:
      self.verbo=value
    elif idx== 5:
      self.sustantivoA=value
    elif idx== 6:
      self.sustantivoB=value
    elif idx== 7:
      self.descripcion=value
    elif idx== 8:
      self.codigo=value
    elif idx== 9:
      self.fecha=value
    elif idx== 10:
      self.puntos=value
    else:
      raise ValueError('No se puede asignar, el indice %i no existe'%idx)

  def GetHtmlAnswer(self):
    """ Retorna la respuesta formateada en html"""
    htmlTx='<h3>%s</h3>\n'%self.descripcion
    htmlTx+='<font color="#204a87"> %s:: %s :: %s </font>'%(self.lenguaje,self.version,self.lib)
    htmlTx+=lexer.formatoPython(self.codigo)
    return htmlTx

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def __len__(self):
    return 11

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class IngresoDeDatos(wx.Frame):
  def __init__(self, parent, id=-1, title='Nueva Respuesta',respuesta=''):

    self.respuesta=respuesta
    if respuesta == '':
      self.respuesta=Respuesta()
    self._title=title
    title= 'id: %i - %s'%(self.respuesta.idr,title)
    wx.Frame.__init__(self, parent, id, title, size=(550, 400))

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

    self.lenguajeCtrl= CampoCtrl(panel,label='Lenguaje:', choices=LIST_LANGUAGES)
    self.versionCtrl=CampoCtrl(panel,label='Versión:',sizeInput=(200,-1) )
    self.libCtrl=CampoCtrl(panel,label='Librería:',sizeInput=(200,-1) )

    hboxA= wx.BoxSizer(wx.HORIZONTAL)
    hboxA.Add((15,-1))
    hboxA.Add(self.lenguajeCtrl)
    hboxA.Add((5,-1))
    hboxA.Add(self.versionCtrl)
    hboxA.Add((5,-1))
    hboxA.Add(self.libCtrl)
    
    self.verboCtrl=CampoCtrl(panel,label='Verbo*:')
    self.sustACtrl=CampoCtrl(panel,label='SustantivoA*:',sizeInput=(200,-1) )
    self.sustBCtrl=CampoCtrl(panel,label='SustantivoB:',sizeInput=(200,-1) )
    
    hboxB= wx.BoxSizer(wx.HORIZONTAL)
    hboxB.Add((15,-1))
    hboxB.Add(self.verboCtrl)
    hboxB.Add((5,-1))
    hboxB.Add(self.sustACtrl)
    hboxB.Add((5,-1))
    hboxB.Add(self.sustBCtrl)
    
    vbox.Add((-1,10))
    vbox.Add(hboxA)
    vbox.Add((-1,10))
    vbox.Add(hboxB)

    self.descripcionCtrl=CampoCtrl(panel,label='Descripción*:',sizeInput=(-1,-1) )
    vbox.Add((-1,10))
    vbox.Add(self.descripcionCtrl, 0, wx.EXPAND | wx.LEFT|wx.RIGHT,15)
    
    font1 = wx.Font(11, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Monospace')
    self.codigoCtrl=wx.TextCtrl(panel,style = wx.TE_MULTILINE)
    self.codigoCtrl.SetFont(font1)
    if not isinstance(self.respuesta.lenguaje ,str):
      print self.respuesta.lenguaje

    #*******************Inicializa valores segun la respuesta 
    for i, ctrl in zip(range(1,9),(self.lenguajeCtrl, self.versionCtrl, self.libCtrl,
    self.verboCtrl, self.sustACtrl, self.sustBCtrl, self.descripcionCtrl,
    self.codigoCtrl)):
      ctrl.SetValue(self.respuesta[i])

    font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
    font.SetPointSize(9)
    sst= wx.StaticText(panel, label='Código*:')
    sst.SetFont(font)
    vbox.Add((-1,10))
    vbox.Add(sst, 0, wx.EXPAND | wx.LEFT,15)
    vbox.Add(self.codigoCtrl, 1, wx.EXPAND | wx.LEFT |wx.RIGHT, 15)

    self.btAgregar = wx.Button(panel, label='Agregar')
    #self.Bind(wx.EVT_BUTTON,self.GetAnswer,self.btAgregar)
    vbox.Add((-1,10))
    vbox.Add(self.btAgregar, 0, wx.ALIGN_RIGHT|wx.RIGHT, 15)
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
    
    self.Bind(wx.EVT_TOOL, self.OnNewAnswer, self.tlNewAnser)
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def OnNewAnswer(self,e):
    self.ClearData(self.respuesta.idr+1)
    self.btAgregar.Enable()
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def GetAnswer(self,e=-1):
    if self.versionCtrl.GetValue()== '':
      self.versionCtrl.SetValue('Estandar')
    if self.libCtrl.GetValue()== '':
      self.libCtrl.SetValue('Estandar')
    for i, ctrl in zip(range(1,9),(self.lenguajeCtrl, self.versionCtrl, self.libCtrl,
    self.verboCtrl, self.sustACtrl, self.sustBCtrl, self.descripcionCtrl,
    self.codigoCtrl)):
      self.respuesta[i]=ctrl.GetValue().encode('utf-8')
    
    if self.respuesta.verbo=='':
      self.InfoText('El campo de Verbo es obligatorio')
      return 0
    if self.respuesta.sustantivoA=='':
      self.InfoText('El campo de SustantivoA es obligatorio')
      return 0
    if self.respuesta.descripcion=='':
      self.InfoText('El campo de Descripción es obligatorio')
      return 0
    if self.respuesta.codigo=='':
      self.InfoText('El campo de Codigo es obligatorio')
      return 0
    
    if self.respuesta.fecha=='':
      self.respuesta.fecha= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
#    data=[self.respuesta[i] for i in range(len(self.respuesta))]
#    print data
  
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
    self.codigoCtrl.SetValue('')
    self.respuesta.fecha=''
    self.respuesta.puntos=0
    self.respuesta.idr=idr
    title= 'id: %i - %s'%(idr,self._title)
    self.SetTitle(title)

  def InfoText(self, message, caption='Information !'):
    dlg = wx.MessageDialog(self, message, caption)
    dlg.ShowModal()


