import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QVBoxLayout, QPushButton)
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import Qt, QRect, QPoint, QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import time
import screeninfo

# Almacena una lista de todos los arboles necesarios para crear el arbol final desde el estado anterior
trees_list = []
# Almacena una lista de los valores de todos los arboles necesarios para crear el arbol final desde el estado inicial, es usada para generar la lista trees_list
trees_values_list = []
# Obtiene las dimenciones de la pantalla
screen = screeninfo.get_monitors()[0]
window_with = screen.width
height = screen.height

# Clase que representa un nodo en el arbol
class Node():
    def __init__(self, value,color = 1):
        self.value = value                               # Valor del nodo
        self.parent = None                               # Padre del nodo
        self.left = None                                 # Hijo izquierdo del nodo
        self.right = None                                # Hijo derecho del nodo
        self.color = color                               # Color del nodo donde 1 es rojo y 0 negro, por defecto dodos empiezan como rojos
        self.position = [0,0]                            # Posicion del nodo para su dibujado

    def __str__(self):
        return ("pos: " + str(self.position))


# Clase usada para dibujar todo el arbol
class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.tree = None

        self.Tree_1 = RBTree()          # Se crea una instancia de un arbol y se define como arbol usado para la graficacion

        self.set_tree(self.Tree_1)      # Se establece el arbol creado como arbol principal

        self.resize(window_with, 700)   

        self.tiempo = 0                 # Variable utilizada para controlar los pasos en la animacion
        self.timer = QTimer(self, interval=2000) # Timer que incrementa en 1 la varibale tiempo para la animacion, llamado cada 2 segundos
        self.timer.timeout.connect(self.update_draw) # El timer llama a la funcion que actualiza el lienzo

    def update_draw(self):
        self.update()

# Este evento es ejecutado cada vez que el lienzo se actualiza
    def paintEvent(self, event):
        # En caso de que la animacion aun no termine sigue ejecutando la animacion
        if self.tiempo < len(trees_list):
            self.draw_tree(trees_list[self.tiempo])
        else:
        # Si la animacion ya termino solamente dibuja el arbol final
            self.draw_tree(self.tree)

        
        
# Este metodo es usado para para dibujar el arbol
    def draw_tree(self,tree):
        global trees_list
        # Se establecen los parametros para realizar el dibujo por medio de un QPainter
        bounce = QPainter(self)
        bounce.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.black, 5)
        bounce.setPen(pen)
        bounce.setBrush(Qt.red)
        # Se establece el arbol pasado como arbol principal
        self. set_tree(tree)
        # Se llama a la funcion encargada de dibujar cada nodo de forma recursiva partiendo del nodo root del arbol establecido como principal
        self.draw_node(tree.root, bounce, tree)
        # Si la animacion aun no termina
        if self.tiempo < len(trees_list):
            # Incrementa el tiempo en 1 para continuar con el siguente paso
            self.tiempo+=1
        else:
            # Si la animacion ya termino reinicia el tiempo y para el timer
            self.tiempo = 0
            self.timer.stop()

# Metodo encargado de dibujar cada nodo del arbol
    def draw_node(self, node, bounce, tree):
        # Se establecen los colores donde 1 es rojo y 0 verde (que representa al verde en los arboles red-black)
        if node.color == 1:
            bounce.setBrush(Qt.red)
        else:
            bounce.setBrush(Qt.green)
        # Si el nodo existe
        if node is not None:
            # Se dibuja el nodo tomando en cuenta su pocicion y su diametro que es de 40. Ademas del valor del nodo
            bounce.drawEllipse(
                QRect(node.position[0]-20, node.position[1]-20, 40, 40))
            bounce.drawText(QRect(
                  node.position[0]-20, node.position[1]-20, 40, 40), Qt.AlignCenter, str(node.value))
            # Si el arbol tiene hijo izquierdo se dibuja la linea desde el nodo actual al siguente y se pasa este nodo de forma recursiva
            if node.left is not None and node.left != tree.NULL:
                bounce.drawLine(node.position[0]-20, node.position[1], node.left.position[0], node.left.position[1])
                self.draw_node(node.left, bounce,tree)
          

            # Si el arbol tiene hijo derecho se dibuja la linea desde el nodo actual al siguente y se pasa este nodo de forma recursiva
            if node.right is not None and node.right != tree.NULL:
                bounce.drawLine(node.position[0]+20, node.position[1], node.right.position[0], node.right.position[1])
                self.draw_node(node.right, bounce,tree)

# Este metodo establece el arbol pasado como arbol principal
    def set_tree(self, tree):
        self.tree = tree

# Este metodo genera los arboles intermedios para lograr la animacion y los almacena en la lista global trees_list
    def generate_trees(self):
        for i in trees_values_list:
            new_tree = RBTree()
            new_tree.fill_tree(i)
            trees_list.append(new_tree)



# Clase de la ventana principal
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(window_with, height)
        self.setWindowTitle("Red Black Tree")
        # Crea una instancia de la clase AppDemo
        self.GC = AppDemo()

        # Inserta una serie de nodos para empezar con un arbol por defecto
        
        #self.GC.Tree_1.insertNode(10)
        #self.GC.Tree_1.insertNode(20)
        
        #self.GC.Tree_1.insertNode(30)
        
        #self.GC.Tree_1.insertNode(5)
        

        #self.GC.Tree_1.insertNode(4)
         
        #self.GC.Tree_1.insertNode(2)
        
        #self.GC.Tree_1.insertNode(1)
        
        #self.GC.Tree_1.insertNode(-1)

        # Establece la posicion de cada nodo si es que se insertan valores por defecto
        self.GC.Tree_1.set_positions()

        layout = QVBoxLayout()
        layout.addWidget(self.GC)

        # Campos donde se ingresaran los valores para crear cada nodo
        lable_nodes_list = QLabel("Ingrese un valor entero: ")
        self.input_nodes_list = QLineEdit() 
		
		# Creamos la expresión regular para permitir solo números enteros positivos y negativos
        regex = QRegExp("-?[0-9]+")
        
		# Creamos el validador y lo asignamos al QLineEdit
        validator = QRegExpValidator(regex)
        self.input_nodes_list.setValidator(validator)

        #Creamos un boton que inserte el valor ingresado y lo insertamos a la composicion
        botton_start = QPushButton("Start")
        HBox_nodes_list = QHBoxLayout()
        HBox_nodes_list.addWidget(lable_nodes_list)
        HBox_nodes_list.addWidget(self.input_nodes_list)
        layout.addLayout(HBox_nodes_list)
        layout.addWidget(botton_start)

        # Generamos el widget central y lo configuramos para que se muestre
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        botton_start.clicked.connect(self.read_list)

# Metodo usado para leer el valor del input e inica el proceso de ingreso en el arbol
    def read_list(self):
        global trees_values_list
        global trees_list
        # Si la animacion no temrina no puede ingresar un nuevo valor
        if self.GC.tiempo == 0:
            # Limpia la lista usadas para crear la animacion
            trees_values_list = []
            trees_list = []
            # Lee el valor del input, si no puede leerlo y convertirlo a entero se retorna la funcion
            try:
                value = int(self.input_nodes_list.text())
            except:
                return
            
            # Si el valor ingresado ya existe se retorna la funcion
            for i in self.GC.Tree_1.read_values(self.GC.Tree_1.root):
                if value == i[0]:
                    return
            # Se inserta el valor al arbol
            self.GC.Tree_1.insertNode(value, True)
            # Se establecen las nuevas posicion de los nodos
            self.GC.Tree_1.set_positions()
            # Se generan los arboles necesarios para la animacion
            self.GC.generate_trees()
            # Se inicializa el timer para la animacion
            self.GC.timer.start()




# Clase de un arbol Rojo Negro
class RBTree():
    def __init__(self):
        # El nodo root del arbol siempre empieza como un nodo con valor 0 sin padre ni hijos
        self.NULL = Node(0)
        self.NULL.color = 0
        self.NULL.left = None
        self.NULL.right = None
        self.root = self.NULL

# Se establece la posicion de root y se llama de forma recursiva al metodo set_positions_node()
    def set_positions(self):
        # El nodo root se posiciona a la mitad de la pantalla, 50 pixeles por debajo del borde superior
        self.root.position[0] = int(window_with/2)
        self.root.position[1] = 50
        self.set_positions_node(self.root, 1)

# Metodo recursivo para establecer la posicion de cada nodo con base al nodo pasado y un sentido que depende de si es un hijo izquierdo o derecho
    def set_positions_node(self, node, sentido):
        if node is not None and node.parent is not None:
            if node.parent.parent is None:
                # En caso de ser un nodo del nivel 2 
                with_increment = window_with/4
            else:
                # En caso de ser un nodo de un nivel superior
                with_increment = abs(node.parent.position[0] - node.parent.parent.position[0])/2    # Este calculo considera la separacion entre el nodo padre y el nodo abuelo del nodo actual, y la divide entre dos

        # Se establecen las posiciones para el nodo actual
        if node is not None and node.parent is not None:
            node.position[0] = int(node.parent.position[0]+with_increment*sentido)
            node.position[1] = int(node.parent.position[1]+100)
        # Si tiene hijo izquierdo se pasa este de forma recursiva
        if node.left is not None:   
            self.set_positions_node(node.left, -1)
        # Si tiene hijo derecho se pasa este de forma recursiva
        if node.right is not None:
            self.set_positions_node(node.right, 1)
# Metodo usado para leer todos los valores del arbol, este metodo funciona de forma recursiva y la lista que va a retornar de todos los valores
    def read_values(self, node, values = []):
        if node is not None and node != self.NULL:
            # Se inserta el valor y el color del nodo actual
            values.append([node.value,node.color])
            if node.left is not None and node.left != self.NULL:
                self.read_values(node.left, values)
            if node.right is not None and node.right != self.NULL:
                self.read_values(node.right,values)
        return values

    def fill_tree(self,values):
        for i in values:
            self.insert(i)
        self.set_positions()

    def insert(self,value):
        if self.root == self.NULL or self.root is None:
            self.root = Node(value[0],value[1])
        else:
            self.insertNode_Normal(self.root,value)
    def insertNode_Normal(self,node,value):
        if value[0] < node.value:
            if node.left is None or node.left == self.NULL:
                new_node = Node(value[0],value[1])
                node.left = new_node
                new_node.parent =  node
            else:
                self.insertNode_Normal(node.left,value)
        else:
            if node.right is None or node.right ==self.NULL:
                new_node = Node(value[0],value[1])
                node.right = new_node
                new_node.parent = node
            else:
                self.insertNode_Normal(node.right,value)







# Metodo usado para insertar un nuevo valor pero siguendo las reglas de Red Black Tree
    def insertNode(self, key, option = False):
        node = Node(key)
        node.parent = None
        node.value = key
        node.left = self.NULL
        node.right = self.NULL
        node.color = 1                                  # Establece el color a rojo

        y = None
        x = self.root

        while x != self.NULL:                           # Encuentra una posicion para el nodo nuevo
            y = x
            if node.value < x.value:
                x = x.left
            else:
                x = x.right

        node.parent = y                                  # Establece al padre como y
        if y == None:                                   # Si el nodo es None entonces se establece como root
            self.root = node
        elif node.value < y.value:                          # Verifica si insertar en el lado izquierdo o derecho
            y.left = node
        else:
            y.right = node

        if node.parent == None:                         # El nodo root siempre se debe establecer como negro
            node.color = 0
            return

        if node.parent.parent == None:          
            return
        if option:
            trees_values_list.append(self.read_values(self.root,[]))    # Crea una copia de los valores del arbol actual
        self.fixInsert(node, option)                          # Corrige los valores insertados

    def minimum(self, node):
        while node.left != self.NULL:
            node = node.left
        return node

    # Genera una rotacion izquierda
    def LR(self, x):
        y = x.right                                      # Se asigna a y el hijo derecho del nodo pasado
        # Se intercamian los valores de los nodos hijos
        x.right = y.left
        if y.left != self.NULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:                            
            self.root = y                           
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # Genera una rotacion derecha
    def RR(self, x):
        y = x.left                                      
        x.left = y.right
        if y.right != self.NULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:                            
            self.root = y                               
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

# Metodo usado para correguir una insercion
    def fixInsert(self, k, option):
        while k.parent.color == 1:                        
            if k.parent == k.parent.parent.right:         
                u = k.parent.parent.left                  
                if u.color == 1:                          
                    u.color = 0                         
                    k.parent.color = 0
                    k.parent.parent.color = 1             
                    k = k.parent.parent
                    if option:
                        trees_values_list.append(self.read_values(self.root,[]))
                else:
                    if k == k.parent.left:                
                        k = k.parent
                        self.RR(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.LR(k.parent.parent)
                    if option:
                        trees_values_list.append(self.read_values(self.root,[]))
            else:                                         
                u = k.parent.parent.right                 
                if u.color == 1:                          
                    u.color = 0                           
                    k.parent.color = 0
                    k.parent.parent.color = 1             
                    k = k.parent.parent                   
                    if option:
                        trees_values_list.append(self.read_values(self.root,[]))
                else:
                    if k == k.parent.right:               
                        k = k.parent
                        
                        self.LR(k)
                        if option:
                            trees_values_list.append(self.read_values(self.root,[]))
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.RR(k.parent.parent)
                    if option:
                        trees_values_list.append(self.read_values(self.root,[]))
            if k == self.root:                            
                break
        self.root.color = 0                               
        if option:
            trees_values_list.append(self.read_values(self.root,[]))

# Metodo usado para mover los nodos de una posicion u a una v
    def __rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # demo = AppDemo()
    demo = MainWindow()
    demo.show()

    sys.exit(app.exec_())
