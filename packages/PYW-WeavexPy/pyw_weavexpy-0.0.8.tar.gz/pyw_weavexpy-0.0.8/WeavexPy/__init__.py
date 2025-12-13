# http://127.0.0.1:5000 
import webview
from threading import Thread

def get_html(html, arq=False):
    html_ = ''
    if arq == False:
        if isinstance(html, list):
            for _ in html:
                html_ += str(_) + '\n'
        else:
            html_ += html
    else:
        with open(f'{html}.html', "r", encoding="utf-8") as f:
            conteudo = f.read() 
                
        html_ += conteudo 
        
    return html_
        
def get_js(js, arq=False):
    js_ = ''
    if arq == False:
        if isinstance(js, list):
            for _ in js:
                js_ += str(_) + '\n'
        else:
            js_ += js
    else:
        with open(f'{js}.js', "r", encoding="utf-8") as f:
            conteudo = f.read() 
                
        js_ += conteudo
        
    return js_

class create_object_style:
    def __init__(self, name):
        self.name = f'.{name}'

    def norm(self):
        return self.name

    def focus(self):
        return self.name + ':focus'
    
    def active(self):
        return self.name + ':active'
    
    def hover(self):
        return self.name + ':hover'

    def ativo(self):
        return self.name + '.ativo'


def scale(s):
    return f'scale({s})'

def rgb(r=255, b=255, g=255):
    return f'rgb({r}, {b}, {g})'
def hex_shadow(hex_color):
    hex_color = hex_color.lstrip('#')

    if len(hex_color) == 6: 
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        a = 1  
    elif len(hex_color) == 8:  
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        a = int(hex_color[6:8], 16) / 255
    else:
        raise ValueError("Formato inválido. Use RRGGBB ou RRGGBBAA")

    return f"rgba({r},{g},{b},{a})"

def s(var):
    return f'{var}s'

def deg(var):
    return f'{var}deg'
def px(var):
    return f'{var}px'
def cm(var):
    return f'{var}cm'
def mm(var):
    return f'{var}mm'
def pt(var):
    return f'{var}pt'
def pc(var):
    return f'{var}pc'

def rel(var):
    '''var -> %var '''
    return f'{var}%'
def em(var):
    return f'{var}em'
def rem(var):
    return f'{var}rem'
def ex(var):
    return f'{var}ex'
def ch(var):
    return f'{var}ch'
def vh(var):
    return f'{var}vh'
def vw(var):
    return f'{var}vw'
def vmin(var):
    return f'{var}vmin'
def vmax(var):
    return f'{var}vmax'


def hr_shadow(size=px(2), color='#ccc', box_shadow = (0, 'low', px(5)), shadow_color = hex_shadow('#000000')):
    sh = box_shadow[1]
    if sh == 'low': sh = 2
    elif sh == 'top' : sh = -2
    sh = px(sh)
    return f'<hr style="border: none; border-top: {size} solid {color}; box-shadow: {box_shadow[0]} {sh} {box_shadow[2]} {shadow_color};">'
def hr_boder_style(size=px(2), color='#000', boder_top = 'solid'):
    return f'<hr style"border: none; border-top: {size} {boder_top} {color};">'
def br_style(style):
    return f'<br style={style}>'
def hr_style(style):
    return f'<hr style={style}>'

def translate(x, y):
    return f'translate({x}, {y})'
def custom(*values):
    return ' '.join(values)

from .server import *
from .ehtml import *
from .css import *
from .script import *
from .obj import *
def NavMenu():
    def script():
        zoom_level = 1.0

        # Remove menu anterior
        def remover_menu():
            old = document.select("#menu_custom")
            if old:
                old[0].remove()

        # Ajustar zoom
        def aplicar_zoom():
            document.body.style.zoom = str(zoom_level)

        # Cria o menu
        def mostrar_menu(evt):
            evt.preventDefault()
            remover_menu()

            menu = html.DIV(Id="menu_custom")
            menu.style = {
                "position": "absolute",
                "top": f"{evt.clientY}px",
                "left": f"{evt.clientX}px",
                "background": "#fff",
                "border": "1px solid #ccc",
                "padding": "5px",
                "border-radius": "5px",
                "z-index": "9999",
                "box-shadow": "0 2px 6px rgba(0,0,0,0.2)",
                "cursor": "pointer",
                "user-select": "none"
            }

            # Opções
            op1 = html.DIV("""<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-browser-chrome" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M16 8a8 8 0 0 1-7.022 7.94l1.902-7.098a3 3 0 0 0 .05-1.492A3 3 0 0 0 10.237 6h5.511A8 8 0 0 1 16 8M0 8a8 8 0 0 0 7.927 8l1.426-5.321a3 3 0 0 1-.723.255 3 3 0 0 1-1.743-.147 3 3 0 0 1-1.043-.7L.633 4.876A8 8 0 0 0 0 8m5.004-.167L1.108 3.936A8.003 8.003 0 0 1 15.418 5H8.066a3 3 0 0 0-1.252.243 2.99 2.99 0 0 0-1.81 2.59M8 10a2 2 0 1 0 0-4 2 2 0 0 0 0 4"/>
</svg> Abrir no navegador""")
            op2 = html.DIV("""<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-90deg-left" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M1.146 4.854a.5.5 0 0 1 0-.708l4-4a.5.5 0 1 1 .708.708L2.707 4H12.5A2.5 2.5 0 0 1 15 6.5v8a.5.5 0 0 1-1 0v-8A1.5 1.5 0 0 0 12.5 5H2.707l3.147 3.146a.5.5 0 1 1-.708.708z"/>
</svg> Voltar""")
            op3 = html.DIV("""<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-90deg-right" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M14.854 4.854a.5.5 0 0 0 0-.708l-4-4a.5.5 0 0 0-.708.708L13.293 4H3.5A2.5 2.5 0 0 0 1 6.5v8a.5.5 0 0 0 1 0v-8A1.5 1.5 0 0 1 3.5 5h9.793l-3.147 3.146a.5.5 0 0 0 .708.708z"/>
</svg> Avançar""")
            op4 = html.DIV("""<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-counterclockwise" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M8 3a5 5 0 1 1-4.546 2.914.5.5 0 0 0-.908-.417A6 6 0 1 0 8 2z"/>
  <path d="M8 4.466V.534a.25.25 0 0 0-.41-.192L5.23 2.308a.25.25 0 0 0 0 .384l2.36 1.966A.25.25 0 0 0 8 4.466"/>
</svg> Resetar página""")
            op5 = html.DIV("""<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-zoom-in" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M6.5 12a5.5 5.5 0 1 0 0-11 5.5 5.5 0 0 0 0 11M13 6.5a6.5 6.5 0 1 1-13 0 6.5 6.5 0 0 1 13 0"/>
  <path d="M10.344 11.742q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1 6.5 6.5 0 0 1-1.398 1.4z"/>
  <path fill-rule="evenodd" d="M6.5 3a.5.5 0 0 1 .5.5V6h2.5a.5.5 0 0 1 0 1H7v2.5a.5.5 0 0 1-1 0V7H3.5a.5.5 0 0 1 0-1H6V3.5a.5.5 0 0 1 .5-.5"/>
</svg> Zoom +""")
            op6 = html.DIV("""<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-zoom-out" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M6.5 12a5.5 5.5 0 1 0 0-11 5.5 5.5 0 0 0 0 11M13 6.5a6.5 6.5 0 1 1-13 0 6.5 6.5 0 0 1 13 0"/>
  <path d="M10.344 11.742q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1 6.5 6.5 0 0 1-1.398 1.4z"/>
  <path fill-rule="evenodd" d="M3 6.5a.5.5 0 0 1 .5-.5h6a.5.5 0 0 1 0 1h-6a.5.5 0 0 1-.5-.5"/>
</svg> Zoom −""")

            for op in (op1, op2, op3, op4, op5, op6):
                op.style.padding = "3px 10px"
                op.style.border_bottom = "1px solid #eee"

            menu <= op1
            menu <= op2
            menu <= op3
            menu <= op4
            menu <= op5
            menu <= op6

            document <= menu

            # Funções
            def abrir(evt):
                window.open(window.location.href, "_blank")
                remover_menu()

            def voltar(evt):
                window.history.back()
                remover_menu()

            def avancar(evt):
                window.history.forward()
                remover_menu()

            def resetar(evt):
                window.location.reload()

            def zoom_mais(evt):
                global zoom_level
                zoom_level += 0.1
                aplicar_zoom()
                remover_menu()

            def zoom_menos(evt):
                global zoom_level
                zoom_level = max(0.2, zoom_level - 0.1)
                aplicar_zoom()
                remover_menu()

            op1.bind("click", abrir)
            op2.bind("click", voltar)
            op3.bind("click", avancar)
            op4.bind("click", resetar)
            op5.bind("click", zoom_mais)
            op6.bind("click", zoom_menos)

        # Clicar fora fecha
        def fechar(evt):
            remover_menu()

        document.bind("contextmenu", mostrar_menu)
        document.bind("click", fechar)
    return FrontScript(script)
    
    
def logObject():
  return '''
<script>
(function () {
    function formatarArgs(args) {
        return args.map(a => {
            try {
                if (typeof a === "object") {
                    return JSON.stringify(a);
                }
                return String(a);
            } catch {
                return "[objeto não serializável]";
            }
        }).join(" ");
    }

    function enviarParaFlask(tipo, dadosBrutos) {
        const mensagem = Array.isArray(dadosBrutos)
            ? formatarArgs(dadosBrutos)
            : dadosBrutos;

        fetch("/WeavexPy/events/__JSLOG__", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                tipo: tipo,
                mensagem: mensagem,
                url: window.location.href,
                userAgent: navigator.userAgent,
                timestamp: Date.now()
            })
        });
    }

    function interceptarConsole(nome) {
        const original = console[nome];
        console[nome] = function (...args) {
            enviarParaFlask(nome, args);
            original.apply(console, args);
        };
    }

    interceptarConsole("log");
    interceptarConsole("error");
    interceptarConsole("warn");
    interceptarConsole("info");

    window.onerror = function (msg, url, linha, coluna, erro) {
        enviarParaFlask("window.onerror", {
            msg, url, linha, coluna, erro: (erro || "").toString()
        });
    };

    window.addEventListener("unhandledrejection", event => {
        enviarParaFlask("unhandledrejection", {
            motivo: event.reason ? String(event.reason) : "desconhecido"
        });
    });

})();
</script>
'''

class Scope:
    def __init__(self, parent):
        '''## Scope

The **Scope** module is responsible for structuring the body of an HTML page. It acts as a layout manager, allowing you to build and organize the page hierarchy prior to rendering.

---
title -> <title>{self.title}</title>
lang -> <html lang="{self.lang}">
charset -> <meta charset="{self.charset}">
---

## Functions

### `add(element)`
Adds a new element to the page body.

- **Purpose:** Insert HTML components sequentially or hierarchically.  
- **Parameter:**  
  - `element`: object, string, or structure representing HTML.  
- **How it works:** Stores the element internally, keeping insertion order.  
- **Common uses:**  
  - Dynamic page construction  
  - Adding divs, text blocks, menus, scripts  
  - Incrementally expanding the layout  

---

### `__str__()`
Defines or replaces the entire page content.

- **Purpose:** Establish the final layout of the page.  
- **How it works:** Clears the existing structure and sets a new body.  
- **Common uses:**  
  - Template configuration  
  - Layout reset  
  - Base page setup'''
        self.scope = ''
        self.title = 'Document'
        self.charset = 'UTF-8'
        self.lang = 'en'
        self.set = self.__str__
        self.parent = parent
        self.style = ''
        
    def add_style(self, css):
      self.style += str(css) + '\n'
    def add(self, element) : 
        '''### `add(element)`
Adds a new element to the page body.

- **Purpose:** Insert HTML components sequentially or hierarchically.  
- **Parameter:**  
  - `element`: object, string, or structure representing HTML.  
- **How it works:** Stores the element internally, keeping insertion order.  
- **Common uses:**  
  - Dynamic page construction  
  - Adding divs, text blocks, menus, scripts  
  - Incrementally expanding the layout  '''
        self.scope += str(element) + '\n'
    def __str__(self) :
        '''### `__str__()`
Defines or replaces the entire page content.

- **Purpose:** Establish the final layout of the page.  
- **How it works:** Clears the existing structure and sets a new body.  
- **Common uses:**  
  - Template configuration  
  - Layout reset  
  - Base page setup'''
        return f'''<!DOCTYPE html>
<html lang="{self.lang}">
<head>
    <meta charset="{self.charset}">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/brython@3.11.0/brython.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/brython@3.11.0/brython_stdlib.js"></script>
    <title>{self.title}</title>
{self.parent.all_style}
<style>
{self.style}
</style>
</head>
<script type="module" src="https://pyscript.net/releases/2025.11.1/core.js"></script>
<body onload="brython()">
{self.scope}
{logObject()}
</body>
</html>'''

class ObjectPage:
    def __init__(self, page_base:list) : 
        '''## ObjectPage

The **ObjectPage** module provides a simple and structured way to add elements to a page created with `@Window().add_page()`.  
It uses a base structure defined by **`page_base`**, which serves as the initial template or layout for the page.

This class behaves like a *page builder*: it collects elements and finally produces a consolidated output — typically HTML.

---

## Methods

### `add(element)`
Adds a new element to the page.

- **Purpose:** insert components into the page layout using the `page_base` model.  
- **Parameter:**  
  - `element`: HTML content, structured object, text block, or custom component.  
- **How it works:** the element is appended internally while preserving order and structure.  
- **Common uses:**  
  - Incremental page construction  
  - Adding HTML blocks, widgets, text, or scripts  
  - Modular composition of layouts

---

### `__str__()`
Finalizes and returns the page representation.

- **Purpose:** generate the final page output based on all added elements.  
- **Returns:** usually a string containing the assembled HTML.  
- **How it works:**  
  - Merges `page_base` with the collected elements  
  - Produces the final layout for rendering  
- **Common uses:**  
  - HTML generation in frameworks  
  - Rendering pages in the browser  
  - Exporting the finished layout'''
        self.page_base = page_base
    
    def add(self, element) : 
        '''### `add(element)`
Adds a new element to the page.

- **Purpose:** insert components into the page layout using the `page_base` model.  
- **Parameter:**  
  - `element`: HTML content, structured object, text block, or custom component.  
- **How it works:** the element is appended internally while preserving order and structure.  
- **Common uses:**  
  - Incremental page construction  
  - Adding HTML blocks, widgets, text, or scripts  
  - Modular composition of layouts'''
        self.page_base.append(element)
    def __str__(self):
        '''### `__str__()`
Finalizes and returns the page representation.

- **Purpose:** generate the final page output based on all added elements.  
- **Returns:** usually a string containing the assembled HTML.  
- **How it works:**  
  - Merges `page_base` with the collected elements  
  - Produces the final layout for rendering  
- **Common uses:**  
  - HTML generation in frameworks  
  - Rendering pages in the browser  
  - Exporting the finished layout'''
        html = ''
        for e in self.page_base:
            html += f'{e}\n'
            
        return html

class Window:
    def __init__(self):
        '''
The **Window** class is responsible for creating and managing the main application window using **PyWebView**.  
It centralizes the configuration of visual appearance, layout, window behavior, window state, and backend–frontend integration through JavaScript APIs.

The following attributes define the initial state and capabilities of the window.

---

## Main Attributes

### 🖼️ **Visual Settings**
| Attribute | Description |
|----------|-------------|
| `title` | Window title displayed in the title bar. |
| `background_color` | Background color (hex). |
| `transparent` | Enables window transparency. |
| `vibrancy` | Enables vibrancy effect (macOS). |
| `frameless` | Removes the default window frame. |
| `text_select` | Enables or disables text selection inside the HTML. |

---

### 🧩 **Content & Integration**
| Attribute | Description |
|----------|-------------|
| `html` | Initial HTML content. |
| `js_api` | Object exposed to JavaScript for backend ↔ frontend communication. |

---

### 📏 **Dimensions**
| Attribute | Description |
|----------|-------------|
| `width` | Initial width of the window. |
| `height` | Initial height of the window. |
| `min_size` | Minimum window size (width, height). |
| `resizable` | Allows window resizing. |

---

### 📍 **Position**
| Attribute | Description |
|----------|-------------|
| `x` | Window X position (optional). |
| `y` | Window Y position (optional). |

---

### ⚙️ **Behavior & State**
| Attribute | Description |
|----------|-------------|
| `fullscreen` | Starts in fullscreen mode. |
| `hidden` | Starts with the window hidden. |
| `minimized` | Starts minimized. |
| `on_top` | Keeps the window always on top. |
| `confirm_close` | Prompts confirmation when closing. |

---

### 🖱️ **Drag & Interaction**
| Attribute | Description |
|----------|-------------|
| `easy_drag` | Allows dragging by clicking any part of the window. |
| `draggable` | Enables only specific draggable areas. |
'''
        self.all_style = ''
        self.pages = {'home.page' : ''}
        self.app = Server(__name__, self.pages)
        
        self.title = 'WeavexPy Window'
        self.html = None
        self.js_api = None
        self.width = 800
        self.height = 600
        self.x = None
        self.y = None
        self.resizable = True
        self.fullscreen = False
        self.min_size = (200, 100)
        self.hidden = False
        self.frameless = False
        self.easy_drag = True
        self.minimized = False
        self.on_top = False
        self.confirm_close = False
        self.background_color = '#FFFFFF'
        self.text_select = False
        self.draggable = True
        self.vibrancy = None
        self.transparent = False
        

        
        


    def img_format(self, src, mimetype='image/png'):
        return self.app.__img__(src, mimetype)
    def add_style(self, css_style) : 
        '''
## add_style(css_style)

The **add_style** method adds a global CSS style to the entire application.  
It injects CSS rules into the PyWebView window, enabling consistent theming, layout standardization, and the ability to override default styles across all rendered pages.

---

## Parameters

### `css_style`
A string containing valid CSS rules.

- **Type:** `str`
- **Example:**
  ```css
  body { background-color: #222; color: white; }
'''
        self.all_style += f'<style>\n{css_style}\n</style>'
    
    def page(self, route):
        '''## page(route)

The **page** method allows the creation of complex pages using internal application functions.  
Unlike `form_page`, which is intended for simple and static layouts, this method is suited for dynamic pages that rely on Python processing or internal logic.

A route is registered and linked to a Python callback function responsible for generating or assembling the page content.

---

## Parameters

### `route`
Name or path of the page route.

- **Type:** `str`
- **Purpose:** identifies the internal page handled by a function.

---

## How it works
- The route is associated with an internal callback function.
- When the page is accessed, the function is executed.
- The callback can:
  - build HTML dynamically  
  - query databases  
  - process application data  
  - generate components programmatically  
- Ideal for non-static, logic-driven pages.

---

## Common uses
- Dynamic pages with frequently updated data.
- Dashboards, admin panels, and logic-heavy screens.
- Programmatically generated HTML or components.
- Interfaces that react to internal application states.'''
        def dec(func):
            nonlocal route
            route = str(route) if not route in ['/', 'home'] else 'pg.bp'
            if route in ['/', 'home'] : print('[ERRO] back page not in "/" or "home"')
            self.pages[str(route)] = func  
            
        return dec
    
    def form_page(self, route):
        '''## form_page

The **form_page** method allows the creation of simple pages within the application.  
It is particularly recommended for forms, static content, or lightweight layouts that do not require complex components.

It registers a new page that can be rendered or navigated to within the main window.

---

## Parameters

### `route`
Identifier for the page.

- **Type:** `str`
- **Purpose:** route the page.

---

## How it works
- The page is stored inside the window instance.
- It can be rendered at any moment.
- Ideal for:
  - small forms
  - registration screens
  - simple static interfaces

---

## Common uses
- Creating lightweight static pages.
- Building login or registration forms.
- Organizing multiple screens inside a single window.'''
        def dec(func):
            nonlocal route
            route = str(route) if route in ['/', 'home'] else 'home'
            html = ''
            page = func(page = ObjectPage([]))
            if isinstance(page, list) :
                for pg in page :
                    html += f'{pg}\n'
            else : html = str(page)
            
            html_format = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/brython@3.11.0/brython.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/brython@3.11.0/brython_stdlib.js"></script>
    <title>Document</title>
{self.all_style}
</head>
<script type="module" src="https://pyscript.net/releases/2025.11.1/core.js"></script>
<body onload="brython()">
{html}
{logObject()}
</body>
</html>'''
            
            self.pages[str(route)] = html_format
            
        return dec
            
        
                
    def run(self):
        '''Executa a aplicação, inicializando todas as páginas, estilos e rotas configuradas.'''
        def server():
            self.app.veri().run('0.0.0.0', '5000', debug=False)
            
        Thread(target=server, daemon=True).start()
            
        def qt():
            window = webview.create_window(
                url = 'http://127.0.0.1:5000',
                title=self.title,
                html=self.html,
                js_api=self.js_api,
                width=self.width,
                height=self.height,
                x=self.x,
                y=self.y,
                resizable=self.resizable,
                fullscreen=self.fullscreen,
                min_size=self.min_size,
                hidden=self.hidden,
                frameless=self.frameless,
                easy_drag=self.easy_drag,
                minimized=self.minimized,
                on_top=self.on_top,
                confirm_close=self.confirm_close,
                background_color=self.background_color,
                text_select=self.text_select,
                draggable=self.draggable,
                vibrancy=self.vibrancy,
                transparent=self.transparent
            )

            webview.start(gui="ctk")


        qt()
