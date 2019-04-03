# -*- coding: utf-8 -*-

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%% Lista de lenguajes Válidos %%%%%%%%%%%%%%%%%%%%%%%%%%%%
LIST_LANGUAGES=('Python','C', 'Octave', 'C++', 'Git', 'Makefile','Java', 'Latex', 'html','SQLite')


def formatoPython(codigo):
  """Da formato html de un fragmento de codigo"""
  
  salida=codigo.replace('&', '&amp;')
  salida=salida.replace('<', '&lt;')
  salida=salida.replace('>', '&gt;')
  salida=salida.replace(' ','&nbsp;')
  salida=salida.replace('\n','<br>\n')
  salida='''<p>%s</p>'''%salida
  return salida
  

