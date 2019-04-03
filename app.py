#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import wx
import wx.html
import sqlite3


from src import IngresoDeDatos, JkListCtrl, Respuesta, LIST_LANGUAGES
from src import BusquedaDeDatos
print ' ** wx version: %s'%wx.__version__
print ' ** sqlite version: %s'%sqlite3.sqlite_version

# Valores de id para eventos
VL_FIND_ANSWER=1 #Buscar respuestas
VL_NEW_ANSWER=2 #Nueva respuesta

TB_CONOCIMIENTO='conocimiento'
TB_COMENTARIOS='comentarios'
TB_LIBRERIAS='librerias'

"""
Requiere tener:
  *sqlite3
  
"""

class JkApp(wx.Frame):

  def __init__(self, parent, title):
    wx.Frame.__init__(self, parent, title=title, size=(600,700))
    self.InitVars()
    self.InitUI()
    self.SetTitle('Procesa datos')
    self.Move((215,15))
    self.Show(True)
    
    #self.OnNewAnswer(-1)

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def InitVars(self, dbFile='./data/jkdb'):
    #*** Variables
    self.maxAnswerView=12 #Máximas respuestas a observar
    self.db = sqlite3.connect(dbFile)
    self.db.text_factory = str
    cursor = self.db.cursor()
    cursor.execute('SELECT Count(*) FROM conocimiento')
    self.idr_max= cursor.fetchone()[0]
     
    print( '  Número de respuestas: %i'%self.idr_max)
    #Aquí debe de tomar la última respuesta para reajustar los valores
    #por defecto de la respuesta.
    self.lastAsk= Respuesta()
    self.ViewAsk=[]#Respuestas mostradas
    #*** Indice con las diferentes opciones para busquedas
    self.indexOptionsSearch=Respuesta(0,[],[],[],[],[],[])
    

    if self.idr_max > 0:
      #Obtiene las diferentes opciones en cada campo posible de busqueda
      ids=self.indexOptionsSearch
      cursor.execute('SELECT lenguaje FROM conocimiento GROUP BY lenguaje')
      ids.lenguaje=[t[0] for t in cursor.fetchall()]
      cursor.execute('SELECT version FROM conocimiento GROUP BY version')
      ids.version=[t[0] for t in cursor.fetchall()]
      cursor.execute('SELECT libreria FROM conocimiento GROUP BY libreria')
      ids.lib=[t[0] for t in cursor.fetchall()]
      cursor.execute('SELECT verbo FROM conocimiento GROUP BY verbo')
      ids.verbo=[t[0] for t in cursor.fetchall()]
      cursor.execute('SELECT sustantivoA FROM conocimiento GROUP BY sustantivoA')
      ids.sustantivoA=[t[0] for t in cursor.fetchall()]
      cursor.execute('SELECT sustantivoB FROM conocimiento GROUP BY sustantivoB')
      tmp=cursor.fetchall()
      ids.sustantivoB=[(t[0].decode('utf-8')).encode('utf-8') for t in tmp]
      
      cursor.execute('SELECT * FROM conocimiento ORDER BY id DESC LIMIT ?',(self.maxAnswerView,))
      rtas=cursor.fetchall()#Lista de tuplas,
      rta= list(rtas[0])

      for i in range(len(rta)):
        if isinstance(rta[i], unicode): 
          rta[i]=rta[i].encode('utf-8')
      #Cambia por el índice del lenguaje
      #rta[1]=LIST_LANGUAGES.index(rta[1])
      if rta[2] == '':
        rta[2]='Estandar'
      if rta[3] == '':
        rta[3] = 'Estandar'
      self.lastAsk.SetTuple(rta)

      self.viewAsk= self.ConsultaARtas(rtas)
      print len(self.viewAsk)


  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def ConsultaARtas(self,lista):
    """ Pasa una lista de consulta, a una lista de respuestas
      El principal cambio corresponde al formato UTF-8
    """
    asks=[]
    for r in lista:
      r=list(r)
      for i in range(len(r)):
        if isinstance(r[i], unicode): 
          r[i]=r[i].encode('utf-8')
      if r[2] == '': r[2]='Estandar'
      if r[3] == '': r[3] = 'Estandar'
      ask= Respuesta()
      ask.SetTuple(r)
      asks.append(ask)
    
    return asks

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def InitUI(self):
    panel = wx.Panel(self)
    self.panel=panel
    self.CreateMenuBar()
    self.CreateToolbar()
    self.newAnswerCtrl=None
    self.findAnswerCtrl=None

    panel.SetBackgroundColour('#4f5049')
    vbox = wx.BoxSizer(wx.VERTICAL)
    panel.SetSizer(vbox)

    vbox.Add(self.toolbar,0,wx.EXPAND,border=5)
    #***********************************************
    self.list=JkListCtrl(panel,['Ultimas Respuestas Agregadas'])
    descripciones=[]
    for ask in self.viewAsk:
      descripciones.append('(%s) -- %s'%(ask.lenguaje,ask.descripcion))
    self.list.AddColumnData(0,descripciones)
    self.list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelectAnswer)
    vbox.Add(self.list, 1, wx.EXPAND | wx.ALL, 10)
    #***********************************************
    self.asksCtrl= wx.html.HtmlWindow(panel, -1)
    self.asksCtrl.SetPage(self.viewAsk[0].GetHtmlAnswer())
    #self.asksCtrl.copy=self.CopyFromCode
    self.asksCtrl.Bind(wx.EVT_KEY_DOWN, self.OnKey)
    vbox.Add(self.asksCtrl, 1, wx.EXPAND|wx.LEFT|wx.RIGHT,10)
    
    
    #self.Bind(wx.EVT_LIST_COL_CLICK, self.OnSelectAnswer, self.asksCtrl)
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def CopyFromCode(self):
    """Copia desde el control que muestra codigo
      debido a que para mostrar los espacios en blanco se usa el nbsp
      que es el caracter 255, y al copiar al portapapeles y usarlo 
      directamente genera problemas, pues el espacio normal es el caracter
      32, por ello se intercepta la copia con CTRL+C y se ajusta la cadena
      obtenida"""
    self.Msg('Se está copiando')
    if not wx.TheClipboard.IsOpened():
      do = wx.TextDataObject()
      wx.TheClipboard.Open()
      success = wx.TheClipboard.GetData(do)
      
      if success:
        cadena=do.GetText().encode('utf-8')
        cadena=cadena.replace('\xff', ' ')
        do.SetText(cadena)
        wx.TheClipboard.SetData(do)
        self.Msg( 'Codigo copiado')
      else:
        self.Msg("No se puede copiar nada")
      wx.TheClipboard.Close()
    else:
      self.Msg('No se pudo acceder al clipboard')
  def OnKey(self, event):
    # If Ctrl+C is pressed...
    if event.ControlDown() and event.GetKeyCode() == 67:
      self.CopyFromCode()
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def CreateToolbar(self):
    #************************************
    #************* BARRA DE HERRAMIENTAS
    toolbar1 = wx.ToolBar(self.panel, -1, style= wx.TB_HORIZONTAL)
    self.toolbar= toolbar1
    toolbar1.AddSeparator()
    tlFindAnswer = toolbar1.AddLabelTool(-1, '', wx.Bitmap('icons/findAsk.png'))
    tlNewAnser = toolbar1.AddLabelTool(-1, '', wx.Bitmap('icons/newAsk.png'))
    toolbar1.AddSeparator()
    toolbar1.Realize()
    self.Bind(wx.EVT_TOOL, self.OnNewQuestion, tlFindAnswer)
    self.Bind(wx.EVT_TOOL, self.OnNewAnswer, tlNewAnser)
    
    #self.toolbar.EnableTool(ID_TLSAVEXLSX,False)

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def CreateMenuBar(self):
    filemenu= wx.Menu()
    menuOpen = filemenu.Append(wx.ID_OPEN, "&Open"," Open a file to edit")
    menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
    
    # menu Tools
    toolsMenu= wx.Menu()
    menuBuscar= wx.MenuItem(toolsMenu,VL_FIND_ANSWER, '&Find\tCtrl+F')
    toolsMenu.Append(menuBuscar.GetId(),"&Find\tCtrl+F","Busqueda")
    menuNuevaRespuesta= wx.MenuItem(toolsMenu,VL_NEW_ANSWER, '&New answer\tCtrl+N')
    toolsMenu.Append(menuNuevaRespuesta.GetId(),'&New answer\tCtrl+N',"Nueva respuesta")

    # menu Ayuda
    helpmenu= wx.Menu()
    menuAbout= helpmenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
    
    # Creating the menubar.
    menuBar = wx.MenuBar()
    menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
    menuBar.Append(toolsMenu, "&Tools")
    menuBar.Append(helpmenu, "&Help")
    self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
    #Crea barra de estado
    self.sb = self.CreateStatusBar()
    # Events.
    #self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
    self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
    self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
    self.Bind(wx.EVT_MENU, self.OnNewQuestion, id=VL_FIND_ANSWER)
    self.Bind(wx.EVT_MENU, self.OnNewAnswer, id=VL_NEW_ANSWER)
    
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def OnSelectAnswer(self,e):
    currentItem = e.m_itemIndex
    if currentItem < len(self.viewAsk):
      self.asksCtrl.SetPage(self.viewAsk[currentItem].GetHtmlAnswer())
      self.Msg('Respuesta:%i'%currentItem)
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def OnNewQuestion(self,e):
    self.Msg( 'Nueva búsqueda **')
    if self.findAnswerCtrl == None:
      ids=self.indexOptionsSearch
      self.findAnswerCtrl = BusquedaDeDatos(self,-1,'Buqueda de datos',ids)
      self.findAnswerCtrl.Bind(wx.EVT_BUTTON,self.OnFindAnswer,self.findAnswerCtrl.btBuscar)
      self.Bind(wx.EVT_WINDOW_DESTROY, self.OnNewQuestionClose, id= self.findAnswerCtrl.GetId())
    else:
      self.findAnswerCtrl.ClearData()
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def OnNewQuestionClose(self,e):
    self.Msg('Ventana para busqueda de respuestas cerrada')
    self.findAnswerCtrl=None

  def OnFindAnswer(self,e):
    self.Msg('Buscando respuestas')
    question=self.findAnswerCtrl.GetQuestion()
    #Define la búsqueda según los parámetros dados
    st=""
    if question.lenguaje != '':
      if st != '':
        st+= ' AND '
      st+= "lenguaje IS '%s' "%question.lenguaje
    if question.version != '':
      if st != '':
        st+= ' AND '
      st+= "version IS '%s' "%question.version
    if question.lib != '':
      if st != '':
        st+= ' AND '
      st+= "libreria IS '%s' "%question.lib
    if question.verbo!= '':
      if st != '':
        st+= ' AND '
      st+= "verbo IS '%s' "%question.verbo
    if question.sustantivoA!= '':
      if st != '':
        st+= ' AND '
      st+= "sustantivoA IS '%s' "%question.sustantivoA
    if question.sustantivoB!= '':
      if st != '':
        st+= ' AND '
      st+= "sustantivoB IS '%s' "%question.sustantivoB
    cursor = self.db.cursor()
    if st != '':
      #print '  consulta: %s'%st
      consulta= 'SELECT * FROM conocimiento WHERE '+st
      consulta+=' ORDER BY id DESC LIMIT '+str(self.maxAnswerView)
      cursor.execute(consulta)
    else:
      cursor.execute('SELECT * FROM conocimiento ORDER BY id DESC LIMIT ?',
    (self.maxAnswerView,))
    
    rtas=cursor.fetchall()
    if len(rtas)>0:
      self.viewAsk= self.ConsultaARtas(rtas)
      descripciones=[]
      for ask in self.viewAsk:
        descripciones.append('(%s) -- %s'%(ask.lenguaje,ask.descripcion))
      self.list.AddColumnData(0,descripciones)
      self.Msg('Se hallaron %i respuestas'%len(rtas))
    else :
      self.Msg('No se hallaron respuestas')
    

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def OnNewAnswer(self,e):
    self.Msg('Nueva respuesta')
    if self.newAnswerCtrl == None:
      rta=Respuesta(self.idr_max+1, self.lastAsk.lenguaje,
        self.lastAsk.version, self.lastAsk.lib)
      self.newAnswerCtrl = IngresoDeDatos(self,-1,'Nueva respuesta',rta)
      self.newAnswerCtrl.Bind(wx.EVT_BUTTON,self.OnAddNewAnswer,self.newAnswerCtrl.btAgregar)
      self.Bind(wx.EVT_WINDOW_DESTROY, self.OnNewAnswerClose, id= self.newAnswerCtrl.GetId())
    else:
      self.newAnswerCtrl.ClearData(self.idr_max+1)
      self.newAnswerCtrl.btAgregar.Enable()#Habilita el boton
    #self.cptActiva=True
    
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def OnNewAnswerClose(self,e):
    self.Msg('Ventana para ingreso de respuesta cerrada')
    self.newAnswerCtrl=None

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def OnAddNewAnswer(self,e):
    respuesta= self.newAnswerCtrl.GetAnswer()
    if respuesta == 0:
      self.Msg('No se pudo agregar la nueva respuesta')
      return 0
    cursor = self.db.cursor()
    cursor.execute('''INSERT INTO conocimiento
                   VALUES(?,?,?,?,?,?,?,?,?,?,?)''', respuesta.GetTuple())
    self.db.commit()#Guarda los cambios
    self.idr_max+=1

    if self.idr_max != respuesta.idr:
      raise ValueError('Hay un error en el "id" asignado a la nueva respuesta')
    #respuesta.lenguaje=LIST_LANGUAGES.index(respuesta.lenguaje)//*******************************
    self.lastAsk=respuesta
    e.GetEventObject().Disable() #Deshabilita una nueva respuesta
    self.Msg('Agregando nueva respuesta')

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def Msg(self,texto):
    self.sb.SetStatusText('>>  '+ texto)
    print texto
 
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def OnAbout(self,e):
    # Create a message dialog box
    dlg = wx.MessageDialog(self, 
    """ Una herramienta para almacenar conocimiento
    version 1.0 (Alpha)
    Carlos Jacanamejoy (2018)""",
     "Acerca de respuestas", wx.OK)
    dlg.ShowModal() # Shows it
    dlg.Destroy() # finally destroy it when finished.

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def OnExit(self,e):
    self.db.close()
    self.Close(True)  # Close the frame.

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def main():
  ex = wx.App()
  JkApp(None,'Procesa datos')
  ex.MainLoop()


if __name__ == '__main__':
    main()
    
