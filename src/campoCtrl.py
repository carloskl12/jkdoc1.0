# -*- coding: utf-8 -*-

import wx
from src import TextAutocompleteCtrl
"""
  Genera un control de ingreso de algun tipo de dato,
  si el parámetro de choices se ignora, es una entrada de 
  texto, en caso contrario se ingresa una lista o tupla de 
  strings que indicará las posibles opciones a seleccionar.
"""
class CampoCtrl2(wx.Panel):
  def __init__(self, parent, id=-1,  label='dato', choices='',sizeInput=(100,-1),expand=False):
    wx.Panel.__init__(self, parent, id)
    
    vbox = wx.BoxSizer(wx.VERTICAL)
    self.SetSizer(vbox)
    
    font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
    font.SetPointSize(9)
    
    st1 = wx.StaticText(self, label=label)
    st1.SetFont(font)
    self.tc=None
    self.choices=choices
    ctrl=None
    if choices=='':
      self.tc = wx.TextCtrl(self,size=sizeInput)
      ctrl=self.tc
    else:
      self.comboBox=wx.ComboBox(self, choices=choices, style=wx.CB_READONLY, size=sizeInput)
      ctrl=self.comboBox

    vbox.Add(st1)
    vbox.Add(ctrl,1, wx.EXPAND)

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def GetValue(self):
    if self.tc !=None:
      return self.tc.GetValue()
    else:
      return self.choices[self.comboBox.GetSelection()]

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def SetValue(self, value):
    if self.tc != None:
      self.tc.SetValue(value)
    else:
      self.comboBox.SetSelection(value)#****

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class CampoCtrl(wx.Panel):
  def __init__(self, parent, id=-1,  label='dato', choices='',sizeInput=(100,-1),expand=False):
    wx.Panel.__init__(self, parent, id)
    
    vbox = wx.BoxSizer(wx.VERTICAL)
    self.SetSizer(vbox)
    
    font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
    font.SetPointSize(9)
    
    st1 = wx.StaticText(self, label=label)
    st1.SetFont(font)
    self.tc=None
    self.choices=choices
    ctrl=None
    if choices=='':
      self.tc = wx.TextCtrl(self,size=sizeInput)
      ctrl=self.tc
    else:
      self.comboBox= TextAutocompleteCtrl(self,choices=choices, entryCallback=self.SetDynamicChoices)
      #self.comboBox=wx.ComboBox(self, choices=choices, style=wx.CB_READONLY, size=sizeInput)
      ctrl=self.comboBox

    vbox.Add(st1)
    vbox.Add(ctrl,1, wx.EXPAND)

  def match(self, text, choice):
    ''' retorna falso o verdader '''
    t = text.lower()
    c = choice.lower()
    result=False
    try:
      result=c.startswith(t)
    except ValueError:
      print 'No se pudo comparar'
    return result
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def SetDynamicChoices(self):
    """Función que hay una selección dinámica"""
    ctrl = self.comboBox
    text = ctrl.GetValue().lower()
    current_choices = ctrl.GetChoices()
    choices = [choice for choice in self.choices if self.match(text, choice)]
    if choices != current_choices:
      ctrl.SetChoices(choices)
  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def GetValue(self):
    if self.tc !=None:
      return self.tc.GetValue().strip()
    else:
      return self.comboBox.GetValue().strip()
      #return self.choices[self.comboBox.GetSelection()]

  #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
  def SetValue(self, value):
    if self.tc != None:
      self.tc.SetValue(value)
    else:
      if isinstance(value,int):
        print 'valor raro %i'%value
      self.comboBox.SetValue(value)
      #self.comboBox.SetSelection(value)#****
