from .style import style
class title :
    def __init__(self, title_type = 1, content = '', cls = None, id = None, name = None) :
        self.title_type = title_type
        self.content = content
        self.cls = f' class="{cls}"' if not cls == None else ''
        self.id = f' id="{id}"' if not id == None else ''
        self.name = f' name="{name}"' if not name == None else ''
        self.s = style('line')
        self.style = self.s.obj_sty

    def __str__(self): return f'<h{self.title_type} {self.cls}{self.id}{self.name} style={self.s.set()}>{self.content}</h{self.title_type}>'

class paragraph :
    def __init__(self, content = '', cls = None, id = None, name = None) :
        self.content = content
        self.cls = f' class="{cls}"' if not cls == None else ''
        self.id = f' id="{id}"' if not id == None else ''
        self.name = f' name="{name}"' if not name == None else ''
        self.s = style('line')
        self.style = self.s.obj_sty

    def __str__(self): return f'<p {self.cls}{self.id}{self.name} style={self.s.set()}>{self.content}</p>'
    
class legend :
    def __init__(self, content = '', cls = None, id = None, name = None) :
        self.content = content
        self.cls = f' class="{cls}"' if not cls == None else ''
        self.id = f' id="{id}"' if not id == None else ''
        self.name = f' name="{name}"' if not name == None else ''
        self.s = style('line')
        self.style = self.s.obj_sty

    def __str__(self): return f'<legend {self.cls}{self.id}{self.name} style={self.s.set()}>{self.content}</legend>'

class anchor :
    def __init__(self, href='/', target='_self', content = '', cls = None, id = None, name = None) :
        self.content = content
        self.href = f' href="{href}"'
        self.target = f' target="{target}"'
        self.cls = f' class="{cls}"' if not cls == None else ''
        self.id = f' id="{id}"' if not id == None else ''
        self.name = f' name="{name}"' if not name == None else ''
        self.s = style('line')
        self.style = self.s.obj_sty

    def __str__(self): return f'<a {self.href}{self.target}{self.cls}{self.id}{self.name} style={self.s.set()}>{self.content}</a>'
    
class label :
    def __init__(self, content = '', cls = None, id = None, name = None, For = None) :
        self.content = content
        self.cls = f' class="{cls}"' if not cls == None else ''
        self.id = f' id="{id}"' if not id == None else ''
        self.For = f' for="{For}"' if not For == None else ''
        self.name = f' name="{name}"' if not name == None else ''
        self.s = style('line')
        self.style = self.s.obj_sty

    def __str__(self): return f'<label {self.For}{self.cls}{self.id}{self.name} style={self.s.set()}>{self.content}</label>'
    
class textarea :
    def __init__(self, content = '', cols=None, rows=None, placeholder = None, cls = None, id = None, name = None, disabled:bool= False) :
        self.content = content
        self.cols = f' cols={cols}' if not cols == None else ''
        self.rows = f' rows={rows}' if not rows == None else ''
        self.placeholder = f' placeholder="{placeholder}"' if not placeholder == None else ''
        self.cls = f' class="{cls}"' if not cls == None else ''
        self.id = f' id="{id}"' if not id == None else ''
        self.name = f' name="{name}"' if not name == None else ''
        self.disabled = f' disabled' if disabled else ''
        self.s = style('line')
        self.style = self.s.obj_sty

    def __str__(self): return f'<textarea {self.cls}{self.id}{self.name}{self.cols}{self.rows}{self.placeholder} style={self.s.set()}>{self.content}</textarea>'

class select:
    def __init__(self, cls = None, id = None, name = None, disabled:bool=False):
        self.cls = f' class="{cls}"' if not cls == None else ''
        self.id = f' id="{id}"' if not id == None else ''
        self.name = f' name="{name}"' if not name == None else ''
        self.s = style('line')
        self.style = self.s.obj_sty
        self.disabled = f' disabled' if disabled else ''
        self.optios = ''
        
    def option(self, value = '', content = '') : self.optios += f'  <option value="{value}">{content}</option>\n'
    def __str__(self) : return f'<select {self.cls}{self.id}{self.name}{self.disabled}>\n{self.optios}\n</select>'

class div:
    def __init__(self, cls = None, id = None, name = None):
        self.cls = f' class="{cls}"' if not cls == None else ''
        self.id = f' id="{id}"' if not id == None else ''
        self.name = f' name="{name}"' if not name == None else ''
        self.s = style('line')
        self.style = self.s.obj_sty
        self.content = []
        
    def add(self, element) : self.content.append(element)
    def __str__(self) : 
        Format = ''
        for e in self.content : Format += f'{e}\n'
        return f'<div {self.cls}{self.id}{self.name} style={self.s.set()}>\n   {Format}\n</div>\n'

class fieldset:
    def __init__(self, cls = None, id = None, name = None):
        self.cls = f' class="{cls}"' if not cls == None else ''
        self.id = f' id="{id}"' if not id == None else ''
        self.name = f' name="{name}"' if not name == None else ''
        self.s = style('line')
        self.style = self.s.obj_sty
        self.content = []
        
    def add(self, element) : self.content.append(element)
    def __str__(self) : 
        Format = ''
        for e in self.content : Format += f'{e}\n'
        return f'<fieldset {self.cls}{self.id}{self.name} style={self.s.set()}>\n   {Format}\n</fieldset>\n'


class form:
    def __init__(self, method = None, action = None, cls = None, id = None, name = None):
        self.method = f' method="{method}"' if not method == None else ''
        self.action = f' action="/{action}"' if not action == None else ''
        self.cls = f' class="{cls}"' if not cls == None else ''
        self.id = f' id="{id}"' if not id == None else ''
        self.name = f' name="{name}"' if not name == None else ''
        self.s = style('line')
        self.style = self.s.obj_sty
        self.content = []
        
    def add(self, element) : self.content.append(element)
    def __str__(self) : 
        Format = ''
        for e in self.content : Format += f'{e}\n'
        return f'<form {self.method}{self.action}{self.cls}{self.id}{self.name} style={self.s.set()}>\n   {Format}\n</form>'
    
class entry:
    def __init__(self, value = '', placeholder = None, type = 'text', cls = None, id = None, name = None, disabled:bool=False):
        self.value = f'value="{value}"'
        self.placeholder = f' placeholder="{placeholder}"' if not placeholder == None else ''
        self.type = f' type="{type}"' if not type == None else ''
        self.cls = f' class="{cls}"' if not cls == None else ''
        self.id = f' id="{id}"' if not id == None else ''
        self.name = f' name="{name}"' if not name == None else ''
        self.s = style('line')
        self.style = self.s.obj_sty
        self.disabled = f' disabled' if disabled else ''
        
    def __str__(self) : return f'<input {self.value}{self.placeholder}{self.type}{self.cls}{self.id}{self.name}{self.disabled} style={self.s.set()}>'
    
class button:
    def __init__(self, content = '', type = 'submit', cls = None, id = None, name = None, onclick = None, disabled:bool=False):
        self.value = str(content)
        self.type = f' type="{type}"' if not type == None else ''
        self.cls = f' class="{cls}"' if not cls == None else ''
        self.id = f' id="{id}"' if not id == None else ''
        self.onclick = f' onclick="{onclick}"' if not onclick == None else ''
        self.name = f' name="{name}"' if not name == None else ''
        self.s = style('line')
        self.style = self.s.obj_sty
        self.disabled = f' disabled' if disabled else ''
        
    def __str__(self) : return f'<button {self.onclick}{self.type}{self.cls}{self.id}{self.name}{self.disabled} style={self.s.set()}>{self.value}</button>'
    
class img:
    def __init__(self, src = '', alt = '', cls = None, id = None, name = None):
        
        self.src = f' src="{src}"'
        self.alt = f' alt="{alt}"'
        self.cls = f' class="{cls}"' if not cls == None else ''
        self.id = f' id="{id}"' if not id == None else ''
        self.name = f' name="{name}"' if not name == None else ''
        self.s = style('line')
        self.style = self.s.obj_sty

    def __str__(self): return f'<img {self.src}{self.alt}{self.cls}{self.id}{self.name} style={self.s.set()}>'
    
    
class strong:
    def __init__(self, content = '', cls = None, id = None, name = None):
        self.content = content
        self.cls = f' class="{cls}"' if not cls == None else ''
        self.id = f' id="{id}"' if not id == None else ''
        self.name = f' name="{name}"' if not name == None else ''
        self.s = style('line')
        self.style = self.s.obj_sty
        
    def __str__(self): return f'<strong {self.cls}{self.id}{self.name} style={self.s.set()}>{self.content}</strong>'
    
class italic:
    def __init__(self, content = '', cls = None, id = None, name = None):
        self.content = content
        self.cls = f' class="{cls}"' if not cls == None else ''
        self.id = f' id="{id}"' if not id == None else ''
        self.name = f' name="{name}"' if not name == None else ''
        self.s = style('line')
        self.style = self.s.obj_sty
        
    def __str__(self): return f'<em {self.cls}{self.id}{self.name} style={self.s.set()}>{self.content}</em>'
    
class abbr:
    def __init__(self, content = '', cls = None, id = None, name = None):
        self.content = content
        self.cls = f' class="{cls}"' if not cls == None else ''
        self.id = f' id="{id}"' if not id == None else ''
        self.name = f' name="{name}"' if not name == None else ''
        self.s = style('line')
        self.style = self.s.obj_sty
        
    def __str__(self): return f'<abbr {self.cls}{self.id}{self.name} style={self.s.set()}>{self.content}</abbr>'
     
class delt:
    def __init__(self, content = '', cls = None, id = None, name = None):
        self.content = content
        self.cls = f' class="{cls}"' if not cls == None else ''
        self.id = f' id="{id}"' if not id == None else ''
        self.name = f' name="{name}"' if not name == None else ''
        self.s = style('line')
        self.style = self.s.obj_sty
        
    def __str__(self): return f'<del {self.cls}{self.id}{self.name} style={self.s.set()}>{self.content}</del>'
    
     
class ins:
    def __init__(self, content = '', cls = None, id = None, name = None):
        self.content = content
        self.cls = f' class="{cls}"' if not cls == None else ''
        self.id = f' id="{id}"' if not id == None else ''
        self.name = f' name="{name}"' if not name == None else ''
        self.s = style('line')
        self.style = self.s.obj_sty
        
    def __str__(self): return f'<ins {self.cls}{self.id}{self.name} style={self.s.set()}>{self.content}</ins>'
     
          
class small:
    def __init__(self, content = '', cls = None, id = None, name = None):
        self.content = content
        self.cls = f' class="{cls}"' if not cls == None else ''
        self.id = f' id="{id}"' if not id == None else ''
        self.name = f' name="{name}"' if not name == None else ''
        self.s = style('line')
        self.style = self.s.obj_sty
        
    def __str__(self): return f'<small {self.cls}{self.id}{self.name} style={self.s.set()}>{self.content}</small>'
     
          
class sub:
    def __init__(self, content = '', cls = None, id = None, name = None):
        self.content = content
        self.cls = f' class="{cls}"' if not cls == None else ''
        self.id = f' id="{id}"' if not id == None else ''
        self.name = f' name="{name}"' if not name == None else ''
        self.s = style('line')
        self.style = self.s.obj_sty
        
    def __str__(self): return f'<sub {self.cls}{self.id}{self.name} style={self.s.set()}>{self.content}</sub>'
     
     
class sup:
    def __init__(self, content = '', cls = None, id = None, name = None):
        self.content = content
        self.cls = f' class="{cls}"' if not cls == None else ''
        self.id = f' id="{id}"' if not id == None else ''
        self.name = f' name="{name}"' if not name == None else ''
        self.s = style('line')
        self.style = self.s.obj_sty
        
    def __str__(self): return f'<sup {self.cls}{self.id}{self.name} style={self.s.set()}>{self.content}</sup>'
     
     
class blockquote:
    def __init__(self, content = '', cls = None, id = None, name = None):
        self.content = content
        self.cls = f' class="{cls}"' if not cls == None else ''
        self.id = f' id="{id}"' if not id == None else ''
        self.name = f' name="{name}"' if not name == None else ''
        self.s = style('line')
        self.style = self.s.obj_sty
        
    def __str__(self): return f'<blockquote {self.cls}{self.id}{self.name} style={self.s.set()}>{self.content}</blockquote>'
     