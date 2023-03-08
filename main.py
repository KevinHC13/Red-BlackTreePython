import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QVBoxLayout, QPushButton)
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import Qt, QRect, QPoint, QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


# Define Node
class Node():
    def __init__(self, value):
        self.value = value                                   # valueue of Node
        self.parent = None                               # Parent of Node
        self.left = None                                 # Left Child of Node
        self.right = None                                # Right Child of Node
        # Red Node as new node is always inserted as Red Node
        self.color = 1
        self.position = [0,0]

    def __str__(self):
        return ("pos: " + str(self.position))


class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.tree = None

        self.Tree_1 = RBTree()

        # valueue = [5,3,6,4,2,1,8,7,9]
        # self.Tree_1.fill_tree(valueue)
        # self.Tree_1.set_positions()
        # self.Tree_1.inorder()
        self.set_tree(self.Tree_1)
        # self.list_nodes_inorder = "Orden: "

        # print(self.tree.inorder_list_current)
        # print(self.tree.inorder_list)

        self.resize(1000, 700)

        self.tiempo = 0
        self.timer = QTimer(self, interval=1000)
        # self.timer.timeout.connect(self.update_draw)

    def update_draw(self):
        self.update()

    def paintEvent(self, event):
        self.draw_tree()

    def draw_tree(self):
        bounce = QPainter(self)
        bounce.setPen(Qt.black)
        bounce.setBrush(Qt.red)
        self.draw_node(self.tree.root, bounce)

    def draw_node(self, node, bounce):
        if node.color == 1:
            bounce.setBrush(Qt.red)
        else:
            bounce.setBrush(Qt.green)
        if node is not None:
            bounce.drawEllipse(
                QRect(node.position[0]-20, node.position[1]-20, 40, 40))
            bounce.drawText(QRect(
                  node.position[0]-20, node.position[1]-20, 40, 40), Qt.AlignCenter, str(node.value))
            if node.left is not None and node.left != self.Tree_1.NULL:
                bounce.drawLine(
                node.position[0], node.position[1], node.position[0] - 80, node.position[1] + 100)
                self.draw_node(node.left, bounce)
            if node.right is not None and node.right!= self.Tree_1.NULL:
                bounce.drawLine(
                node.position[0], node.position[1], node.position[0] + 80, node.position[1] + 100)
                self.draw_node(node.right, bounce)

    def set_tree(self, tree):
        self.tree = tree


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(1200, 800)
        self.setWindowTitle("Recorrido inorder")
        self.GC = AppDemo()

        self.GC.Tree_1.insertNode(10)
        self.GC.Tree_1.insertNode(20)
        self.GC.Tree_1.insertNode(30)
        self.GC.Tree_1.insertNode(5)
        self.GC.Tree_1.insertNode(4)
        self.GC.Tree_1.insertNode(2)

        # print("\nAfter deleting an element")
    # self.GC.delete_node(2)
    # self.GC.print_tree()

    # self.GCinsertNode(15)
    # self.GCinsertNode(17)
        self.GC.Tree_1.set_positions()
    # self.GCprint_tree()
    # print("\nAfter add an element")
    # print(bst.root)
    # print(bst.root.left)
        layout = QVBoxLayout()
        layout.addWidget(self.GC)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

# Define R-B Tree


class RBTree():
    def __init__(self):
        self.NULL = Node(0)
        self.NULL.color = 0
        self.NULL.left = None
        self.NULL.right = None
        self.root = self.NULL

    def set_positions(self):
        self.root.position[0] = 500
        self.root.position[1] = 50
        self.set_positions_node(self.root, 1)

    def set_positions_node(self, node, sentido):
        if node is not None:
            if node.parent is not None:
                node.position[0] = node.parent.position[0]+((80*sentido) + 20*sentido)
                node.position[1] = node.parent.position[1]+100
            if node.left is not None:
                print("Tiene hijo left")
                self.set_positions_node(node.left, -1)
            if node.right is not None:
                print("Tiene hijo right")
                self.set_positions_node(node.right, 1)

    # Insert New Node

    def insertNode(self, key):
        node = Node(key)
        node.parent = None
        node.value = key
        node.left = self.NULL
        node.right = self.NULL
        node.color = 1                                   # Set root colour as Red

        y = None
        x = self.root

        while x != self.NULL:                           # Find position for new node
            y = x
            if node.value < x.value:
                x = x.left
            else:
                x = x.right

        node.parent = y                                  # Set parent of Node as y
        if y == None:                                   # If parent i.e, is none then it is root node
            self.root = node
        elif node.value < y.value:                          # Check if it is right Node or Left Node by checking the valueue
            y.left = node
        else:
            y.right = node

        if node.parent == None:                         # Root node is always Black
            node.color = 0
            return

        if node.parent.parent == None:                  # If parent of node is Root Node
            return

        self.fixInsert(node)                          # Else call for Fix Up

    def minimum(self, node):
        while node.left != self.NULL:
            node = node.left
        return node

    # Code for left rotate
    def LR(self, x):
        y = x.right                                      # Y = Right child of x
        # Change right child of x to left child of y
        x.right = y.left
        if y.left != self.NULL:
            y.left.parent = x

        # Change parent of y as parent of x
        y.parent = x.parent
        if x.parent == None:                            # If parent of x == None ie. root node
            self.root = y                                # Set y as root
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # Code for right rotate
    def RR(self, x):
        y = x.left                                       # Y = Left child of x
        # Change left child of x to right child of y
        x.left = y.right
        if y.right != self.NULL:
            y.right.parent = x

        # Change parent of y as parent of x
        y.parent = x.parent
        if x.parent == None:                            # If x is root node
            self.root = y                                # Set y as root
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # Fix Up Insertion

    def fixInsert(self, k):
        while k.parent.color == 1:                        # While parent is red
            if k.parent == k.parent.parent.right:         # if parent is right child of its parent
                u = k.parent.parent.left                  # Left child of grandparent
                if u.color == 1:                          # if color of left child of grandparent i.e, uncle node is red
                    u.color = 0                           # Set both children of grandparent node as black
                    k.parent.color = 0
                    k.parent.parent.color = 1             # Set grandparent node as Red
                    # Repeat the algo with Parent node to check conflicts
                    k = k.parent.parent
                else:
                    if k == k.parent.left:                # If k is left child of it's parent
                        k = k.parent
                        # Call for right rotation
                        self.RR(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.LR(k.parent.parent)
            else:                                         # if parent is left child of its parent
                u = k.parent.parent.right                 # Right child of grandparent
                if u.color == 1:                          # if color of right child of grandparent i.e, uncle node is red
                    u.color = 0                           # Set color of childs as black
                    k.parent.color = 0
                    k.parent.parent.color = 1             # set color of grandparent as Red
                    k = k.parent.parent                   # Repeat algo on grandparent to remove conflicts
                else:
                    if k == k.parent.right:               # if k is right child of its parent
                        k = k.parent
                        # Call left rotate on parent of k
                        self.LR(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    # Call right rotate on grandparent
                    self.RR(k.parent.parent)
            if k == self.root:                            # If k reaches root then break
                break
        self.root.color = 0                               # Set color of root as black

    # Function to fix issues after deletion
    def fixDelete(self, x):
        while x != self.root and x.color == 0:           # Repeat until x reaches nodes and color of x is black
            if x == x.parent.left:                       # If x is left child of its parent
                s = x.parent.right                        # Sibling of x
                if s.color == 1:                         # if sibling is red
                    s.color = 0                           # Set its color to black
                    x.parent.color = 1                    # Make its parent red
                    # Call for left rotate on parent of x
                    self.LR(x.parent)
                    s = x.parent.right
                # If both the child are black
                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1                           # Set color of s as red
                    x = x.parent
                else:
                    if s.right.color == 0:               # If right child of s is black
                        s.left.color = 0                  # set left child of s as black
                        s.color = 1                       # set color of s as red
                        # call right rotation on x
                        self.RR(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = 0                    # Set parent of x as black
                    s.right.color = 0
                    # call left rotation on parent of x
                    self.LR(x.parent)
                    x = self.root
            else:                                        # If x is right child of its parent
                s = x.parent.left                         # Sibling of x
                if s.color == 1:                         # if sibling is red
                    s.color = 0                           # Set its color to black
                    x.parent.color = 1                    # Make its parent red
                    # Call for right rotate on parent of x
                    self.RR(x.parent)
                    s = x.parent.left

                if s.right.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:                # If left child of s is black
                        s.right.color = 0                 # set right child of s as black
                        s.color = 1
                        # call left rotation on x
                        self.LR(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.RR(x.parent)
                    x = self.root
        x.color = 0

    # Function to transplant nodes
    def __rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # Function to handle deletion
    def delete_node_helper(self, node, key):
        z = self.NULL
        while node != self.NULL:                          # Search for the node having that valueue/ key and store it in 'z'
            if node.value == key:
                z = node

            if node.value <= key:
                node = node.right
            else:
                node = node.left

        if z == self.NULL:                                # If Kwy is not present then deletion not possible so return
            print("valueue not present in Tree !!")
            return

        y = z
        # Store the color of z- node
        y_original_color = y.color
        if z.left == self.NULL:                            # If left child of z is NULL
            x = z.right                                     # Assign right child of z to x
            # Transplant Node to be deleted with x
            self.__rb_transplant(z, z.right)
        elif (z.right == self.NULL):                       # If right child of z is NULL
            x = z.left                                      # Assign left child of z to x
            # Transplant Node to be deleted with x
            self.__rb_transplant(z, z.left)
        else:                                              # If z has both the child nodes
            # Find minimum of the right sub tree
            y = self.minimum(z.right)
            y_original_color = y.color                      # Store color of y
            x = y.right
            if y.parent == z:                              # If y is child of z
                x.parent = y                                # Set parent of x as y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 0:                          # If color is black then fixing is needed
            self.fixDelete(x)

    # Deletion of node
    def delete_node(self, value):
        self.delete_node_helper(self.root, value)         # Call for deletion

    # Function to print
    def __printCall (self, node, indent, last):
        if node != self.NULL:
            print(indent, end=' ')
            if last:
                print("R----", end=' ')
                indent += "     "
            else:
                print("L----", end=' ')
                indent += "|    "

            s_color = "RED" if node.color == 1 else "BLACK"
            print(str(node.value) + "(" + s_color + ")")
            self.__printCall(node.left, indent, False)
            self.__printCall(node.right, indent, True)

    # Function to call print
    def print_tree(self):
        self.__printCall(self.root, "", True)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # demo = AppDemo()
    demo = MainWindow()
    demo.show()

    sys.exit(app.exec_())
