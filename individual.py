import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QMainWindow, QVBoxLayout, QPushButton)
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import Qt, QRect, QPoint, QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class AppDemo(QWidget):
	def __init__(self):
		super().__init__()
		self.tree = None

		self.Tree_1 = Tree()
		value = [5,3,6,4,2,1,8,7,9]
		#self.Tree_1.fill_tree(value)
		#self.Tree_1.set_positions()
		#self.Tree_1.inorder()
		self.set_tree(self.Tree_1)
		self.list_nodes_inorder = "Orden: "
		
		print(self.tree.inorder_list_current)
		print(self.tree.inorder_list)
		
		self.resize(1000, 700)

		self.tiempo = 0
		self.timer = QTimer(self, interval=1000)
		self.timer.timeout.connect(self.update_draw)

	def update_draw(self):
		self.update()

	def paintEvent(self, event):
		self.draw_tree()
		#self.draw_selectro()
	
	def draw_tree(self):
		bounce = QPainter(self)
		bounce.setPen(Qt.black)
		bounce.setBrush(Qt.red)
		bounce.drawText(50,600,self.list_nodes_inorder)
		self.draw_node(self.tree.root, bounce)
	
	def draw_node(self, node, bounce):
		if node is not None:
			bounce.drawEllipse(QRect(node.position[0]-node.radio, node.position[1]-node.radio, 40, 40))
			bounce.drawText(QRect(node.position[0]-node.radio,node.position[1]-node.radio,40,40),Qt.AlignCenter, str(node.value))
			if node.left is not None:
				bounce.drawLine(node.position[0],node.position[1], node.position[0] - 80, node.position[1] + 100)
				self.draw_node(node.left, bounce)
			if node.right is not None:
				bounce.drawLine(node.position[0],node.position[1], node.position[0] + 80, node.position[1] + 100)
				self.draw_node(node.right,bounce)
			
	
	def draw_selectro(self):
		bounce = QPainter(self)
		bounce.setPen(Qt.black)
		bounce.setBrush(Qt.green)
		if self.tiempo < (len(self.tree.inorder_list_current)):
			if self.tiempo in self.tree.inorder_list:
				bounce.setBrush(Qt.green)
				bounce.drawRect(QRect(self.tree.inorder_list_current[self.tiempo].position[0]-self.tree.root.radio, self.tree.inorder_list_current[self.tiempo].position[1]+self.tree.root.radio+20,40,10))
				self.list_nodes_inorder += str(self.tree.inorder_list_current[self.tiempo].value) + ", "
				bounce.drawText(50,600,self.list_nodes_inorder)
			else:
				bounce.setBrush(Qt.white)
				bounce.drawRect(QRect(self.tree.inorder_list_current[self.tiempo].position[0]-self.tree.root.radio, self.tree.inorder_list_current[self.tiempo].position[1]+self.tree.root.radio+20,40,10))
				bounce.drawText(50,600,self.list_nodes_inorder)
			
		else:
			self.timer.stop()
			self.tiempo = 0
			self.list_nodes_inorder = "Orden: "
			self.Tree_1.root = None
			self.Tree_1.inorder_list_current = []
			self.Tree_1.inorder_list = []
		self.tiempo+=1
		    


	def update_position(self):
		if self.rect_circle.bottom() > self.height() and self.y_direction == 1:
			self.y_direction = -1
		if self.rect_circle.top() < 0 and self.y_direction == -1:
			self.y_direction = 1
		self.tiempo+=1		
		self.rect_circle.translate(self.step * self.y_direction)
		self.update()
		
	def set_tree(self, tree):
		self.tree = tree
	
class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.resize(1200, 800)
		self.setWindowTitle("Recorrido inorder")
		self.GC = AppDemo()
		
		layout = QVBoxLayout()
		layout.addWidget(self.GC)
		lable_nodes_list = QLabel("Lista de enteros(separados por comas): ")
		self.input_nodes_list = QLineEdit() 
		
		# Creamos la expresión regular para permitir solo números y comas
		regex = QRegExp("[0-9,]+")
        
		# Creamos el validador y lo asignamos al QLineEdit
		validator = QRegExpValidator(regex)
		
		self.input_nodes_list.setValidator(validator)
		botton_start = QPushButton("Start")
		HBox_nodes_list = QHBoxLayout()
		HBox_nodes_list.addWidget(lable_nodes_list)
		HBox_nodes_list.addWidget(self.input_nodes_list)
		layout.addLayout(HBox_nodes_list)
		layout.addWidget(botton_start)
		widget = QWidget()
		widget.setLayout(layout)
		self.setCentralWidget(widget)
		botton_start.clicked.connect(self.read_list)



	def read_list(self):
		if not(self.GC.tiempo <= len(self.GC.Tree_1.inorder_list_current)):
			self.GC.Tree_1.root = None
			self.GC.Tree_1.inorder_list_current = []
			self.GC.Tree_1.inorder_list = []
			list_values = self.input_nodes_list.text()
			list_nodes = list_values.split(",")
			try:
				list_nodes = list(map(int, list_nodes))
			except:
				print("Error al convertir string a lista de enteros")
				list_nodes = [0]
			self.GC.Tree_1.fill_tree(list_nodes)
			self.GC.Tree_1.set_positions()
			self.GC.Tree_1.inorder()
			print(self.GC.Tree_1.inorder_list_current)
			print(self.GC.Tree_1.inorder_list)
			#self.GC.timer.start()
			self.GC.update_draw()
		else:
			print("Espera")
			print(self.GC.tiempo)
			print(len(self.GC.Tree_1.inorder_list_current))
		
		




class Node:
	def __init__(self,value):
		self.value = value
		self.radio = 20
		self.left = None
		self.right = None
		self.parent = None
		self.position = [0,0]
		self.added = False
	def __str__(self):
		return ("value: " + str(self.value))

class Tree:
	def __init__(self):
		self.root = None
		self.inorder_list = []
		self.inorder_list_current = []
	def insert(self,value):
		if self.root is None:
			self.root = Node(value)
		else:
			self.insertNode(self.root,value)
	def insertNode(self,node,value):
		if node.value == value:
			print(str(value) + " already exists")
			return
		if value < node.value:
			if node.left is None:
				new_node = Node(value)
				node.left = new_node
				new_node.parent =  node
			else:
				self.insertNode(node.left,value)
		else:
			if node.right is None:
				new_node = Node(value)
				node.right = new_node
				new_node.parent = node
			else:
				self.insertNode(node.right,value)
	
	def inorder(self):
		self.inorderNode(self.root)
	
	def inorderNode(self,node):
		if node is not None:
			self.inorder_list_current.append(node)
			self.clean_list()
			self.inorderNode(node.left)
			node.added = True
			if node.parent is not None:
				print(str(node.value) + " Positions: " + str(node.position)+ " Parent Position:" + str(node.parent.position))
				self.inorder_list.append(len(self.inorder_list_current)-1)
			else:
				print(str(node.value) + " Positions: " + str(node.position))
				self.inorder_list.append(len(self.inorder_list_current))
			self.inorder_list_current.append(node)
			self.clean_list()
			self.inorderNode(node.right)
			self.inorder_list_current.append(node)
			self.clean_list()
		self.clean_list()
	
	def clean_list(self):
		for i in range(0,(len(self.inorder_list_current)-2)):
			if self.inorder_list_current[i] == self.inorder_list_current[i+1]:
				del self.inorder_list_current[i]


			
	def __str__(self):
		if self.root is not None:
			return ("Raiz: "+ str(self.root.value))
		else:
			return ("Raiz " + str(self.root))

	def fill_tree(self,values):
         for i in values:
             self.insert(i)

	def set_positions(self):
		self.root.position[0] = 500
		self.root.position[1] = 50
		self.set_positions_node(self.root,1)

	def set_positions_node(self,node, sentido):
		if node is not None:
			if node.parent is not None:
				node.position[0] = node.parent.position[0]+((80*sentido)+ node.radio*sentido)
				node.position[1] = node.parent.position[1]+100
			if node.left is not None:
				print("Tiene hijo left")
				self.set_positions_node(node.left,-1)
			if node.right is not None:
				print("Tiene hijo right")
				self.set_positions_node(node.right,1)






if __name__ == '__main__':
	app = QApplication(sys.argv)

	#demo = AppDemo()
	demo = MainWindow	()
	demo.show()

	sys.exit(app.exec_())
