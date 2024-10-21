from dudraw.color import Color
import dudraw
from random import randint
#this if for the files at the bottom
import os


"""
    This program is a classic game of snake. The limit variable determines the speed, the lower the limit, the faster
    fewer frames inbetween screen updates. The head of the snake is controlled using WASD, and when the snake eats
    a yellow piece of food, it gets bigger. If the snake hits itself or the edge of the screen, the game ends.
    Filename: wild_project1_snake.py
    Author: Kragen Wild
    Date: 2-17-23
    Course: Programming II
    Assignment: Project 1 - Snake
    Collaborators: nada
    Internet Source: https://thispointer.com/python-three-ways-to-check-if-a-file-is-empty/
"""


class Node:
    """
    The class "Node" is initialized with with 3 instance variables, the value, previous, and the next
    parameters: self, v, p, n
    return: Str
    """
    def __init__(self, v, p, n):
        self.value = v
        self.prev = p
        self.next = n
    def __str__(self) -> str:
        """
        string function, returns it's value
        """
        return str(self.value)

# I hope I dont have to add comments explaining doubly linked lists

class DoublyLinkedList:
    """
    The class "DoublyLinkedList" is initialized with with 4 instance variables, header, trailer, and size
    It has numerous functions which can add and subtract elements from the list, find certain values, and more
    parameters: self, self.header, self.trailer, self.size
    """
    def __init__(self):
        self.header = Node(None,None,None)
        self.trailer = Node(None,self.header,None)
        self.header.next = self.trailer
        self.size = 0
        
    def add_between(self, v, n1, n2):
        if n1 is None or n2 is None:
            raise ValueError("Nodes cannot be none.")
        if n1.next is not n2:
            raise ValueError("Node 2 must follow node 1.")

        #step 1: make a new node, value v, prev is n1 next is n2
        newnode = Node(v,n1,n2)
        #step 2: n1.next points to new node
        n1.next = newnode
        #step 3: n2.prev points to new node
        n2.prev = newnode
        #step 4: size
        self.size += 1

    def add_first(self, v):
        self.add_between(v, self.header, self.header.next)

    def add_last(self,v):
        self.add_between(v, self.trailer.prev, self.trailer)

    def __str__(self) -> str:
        if self.header.next is self.trailer:
            return "[]"
        result = '['
        temp_node = self.header.next
        while not temp_node.next is self.trailer:
            result += str(temp_node) + " "
            temp_node = temp_node.next
        result += str(temp_node) + "]"
        return result

    def remove_between(self, n1, n2):
    # check if either node1 or node2 is None. Raise a ValueError if so.
        if n1 is None or n2 is None:
            raise ValueError("Nodes cannot be none.")
    # Check that node1 and node 2 has exactly 1 node between them, 
    # raise a ValueError if not
        if n1.next.next is not n2:
            raise ValueError("There is more than one node between the 2 nodes you entered.")

    # Everything is in order, so delete the node between node1 and node2, 
    # returning the value that was stored in it
        to_return = n1.next.value
        n1.next = n2
        n2.prev = n1
        self.size -= 1
        return to_return

    def remove_first(self):
        to_return = self.header.next.value
        self.remove_between(self.header, self.header.next.next)
        return to_return

    def remove_last(self):
        to_return = self.trailer.prev.value
        self.remove_between(self.trailer.prev.prev, self.trailer)
        return to_return

    def search(self, v):
        index = 0
        temp = self.header.next
        while temp.value is not v:
            temp = temp.next
            index += 1
            if temp.next is None:
                return -1
        return index
            
    def find_min(self):
        temp_node = self.head
        min = self.head.value
        while not temp_node is None:
            if min > temp_node.value:
                min = temp_node.value
            temp_node = temp_node.next
        return min

    def get_size(self):
        return self.size

    def first(self):
        return self.header.next.value

    def last(self):
        return self.trailer.prev.value

    def is_empty(self):
        if self.size == 0:
            return True
        else:
            return False

    def get(self, index):
        if self.size == 0:
            raise IndexError("The list is empty.")
        temp_node = self.header.next
        for i in range(index):
            if temp_node.next == None:
                raise IndexError("Index does not exist.")
            if i != index:
                temp_node = temp_node.next
        return temp_node.value


class Block:
    """
    The class "Block" is initialized with with 4 instance variables, x_pos, y_pos, size, and color
    parameters: self, x, y, size, color
    return: Str
    """
    def __init__(self, x, y, size, color):
        self.x_pos = x
        self.y_pos = y
        self.size = size
        self.color = color

    def draw(self):
        """
        this function draws a filled square in a specific location, size, and color
        perameters: none
        return: none
        """
        dudraw.set_pen_color(self.color)
        dudraw.filled_square(self.x_pos, self.y_pos, self.size)

class Snake(Block):
    """
    The class "Snake" is initialized with with 6 instance variables, snake_list (a DoublyLinkedList), 
    snake_head (the first item in the list), snake_tail (the last item in the list), snake_length, and snake_location
    parameters: none
    return: depends on the function
    """
    def __init__(self):
        self.snake_list = DoublyLinkedList()
        #a node is added as the first value in the doublylinkedlist, with a block as the value
        self.snake_list.add_first(Block(.025,.025,.025, Color(0,0,0)))
        self.snake_head = self.snake_list.header.next
        self.snake_tail = self.snake_list.trailer.prev
        #the size of the snake is set to 1
        self.snake_length = 1
        #this list of snake block locations is set to empty
        self.snake_location = []


    def draw_snake(self):
        """
        this function goes through each segment of the snake a draws a block at that segment's location
        perameters: self
        return: none
        """
        #this loop has a temp item go through the snake for as many times as the snake is long,
        # and the temp item draws the segemnt it is on and moves on to the next one 
        temp_block = self.snake_head
        for i in range(self.snake_length):
            temp_block.value.draw()
            temp_block = temp_block.next

    def detect_food(self, food)->bool:
        """
        this function checks if the head of the snake is in the same position as the food on screen, and returns true if it is
        false if it isnt, and the size of the snake goes up by one
        perameters: self, food: class
        return: Bool
        """
        if self.snake_head.value.x_pos == food.x_pos:
            if self.snake_head.value.y_pos == food.y_pos:
                #the length of the snake is incrimented by one
                self.snake_length += 1
                return True
        return False
        
    def snake_grow(self, x_dir, y_dir):
        """
        this function adds a block at the beginning of the list in the direction of the users keypress, so it appears as if the snake grew
        perameters: self, x_dir:int, y_dir:int
        return: none
        """
        #using the x and y dir, this line of code adds a block at the beginning of the list, with locations based of the existing head of the snake
        #but in the direction of the keypress (a generates an x and y dir of -1,0, s generates an x and y dir of 0,-1,
        #d generates an x and y dir of 1,0, and w generates an x and y dir of 0,1)
        #the new block is placed at the x and y locaton of the ecisting head, plus the values of x and y dir from the keypress
        self.snake_list.add_first(Block(round(self.snake_head.value.x_pos + x_dir*.025*2, 5), round(self.snake_head.value.y_pos + y_dir*.025*2, 5), .025, Color(0,0,0)))
        self.snake_head = self.snake_list.header.next

    def move(self, x_dir, y_dir):
        """
        this function works exactly like the snake_grow() funciton, it adds a block at the beginning of the list in the 
        direction of the users keypress, so it appears as if the snake grew, and the block at the end of the list is removed,
        so it looks like the snake grew
        perameters: self, x_dir:int, y_dir:int
        return: none
        """
        #same code used in snake_grow()
        self.snake_list.add_first(Block(round(self.snake_head.value.x_pos + x_dir*.025*2, 5), round(self.snake_head.value.y_pos + y_dir*.025*2, 5), .025, Color(0,0,0)))
        self.snake_head = self.snake_list.header.next

        #the last block of the list is removed
        self.snake_list.remove_last()

    def change_heading(self, key)->tuple:
        """
        this function takes in a kepress, and depending on what it is, a corresponding x and y direction are returned
        think of the directions the WASD keys represent. a means to go left, so the x is -1 and the y is 0, because the y doesnt change.
        the w key means to go up, so the x is 0 and the y is one, etc.
        perameters: self, key: str
        return: tuple
        """
        if key == "a":
            return (-1,0)
        if key == "s":
            return (0,-1)
        if key == "d":
            return (1,0)
        if key == "w":
            return (0,1)

    def detect_wall(self)->bool:
        """
        this function checks if the middle of the head of the snake falls above out of the range of the canvas, and returns 
        true if it does, and false if it doesnt
        perameters: self
        return: Bool
        """
        if self.snake_head.value.x_pos >= 1 or self.snake_head.value.x_pos < 0:
            return True
        if self.snake_head.value.y_pos >= 1 or self.snake_head.value.y_pos < 0:
            return True
        return False
    
    def detect_self(self)->bool:
        """
        this function checks if the head of the snake shares location with any other part of the snake, and returns
        true if it does
        perameters: self
        return: Bool
        """
        #this loop runs for as long as the snake is -1, because you dont need to check if the head overlaps the head
        #there is the rounding fuction, becuase sometimes i would get numbers ending with .0000001 or .99999.
        #the temp goes through the snake, checking if the x and y positons of segments both overlap with the head
        temp = self.snake_head
        for i in range(self.snake_length-1):
            if round(self.snake_head.value.x_pos, 5) == round(temp.next.value.x_pos, 5) and round(self.snake_head.value.y_pos, 5) == round(temp.next.value.y_pos, 5):
                return True
            temp = temp.next

    def get_location(self)->list:
        """
        this function creates a list of block locations and returns it
        perameters: self
        return: list
        """
        #the locations of the snake is set to an empty list
        self.snake_location = []
        temp_block = self.snake_head
        #the loop iterates through the snake and adds the x and y position as a tuple to the list
        for i in range(self.snake_length-1):
            self.snake_location.append((temp_block.value.x_pos, temp_block.value.y_pos))
            temp_block = temp_block.next
        #the list is returned
        return self.snake_location

class Food:
    """
    The class "Food" is initialized with with 4 instance variables, x_pos, y_pos, size, and color
    parameters: none
    return: none
    """
    def __init__(self):
        self.x_pos = round(randint(1,9)/10 + .025, 5)
        self.y_pos = round(randint(1,9)/10 + .025, 5)
        self.size = .025
        self.color = Color(247,208,3)

    def draw(self, s):
        """
        this function draws the food at the location and color and size of the class
        perameters: self, s: object
        return: none
        """
        #every 5th piece of food is purple, every 10th piece of food is blue, and every 20th is green
        if s.snake_length %20 == 0:
            dudraw.set_pen_color_rgb(51, 242, 73)
        elif s.snake_length %10 == 0:
            dudraw.set_pen_color_rgb(31, 224, 195)
        elif s.snake_length %5 == 0:
            dudraw.set_pen_color_rgb(199, 80, 197)
        else:
            dudraw.set_pen_color(self.color)
        dudraw.filled_square(self.x_pos, self.y_pos, self.size)

    def reset_location(self, s):
        """
        this function sets the position of the class to a random position on the canvas, and if that position
        overlaps the snake, a new position is chosen
        perameters: self, s:object
        return: none
        """
        self.x_pos = round(randint(1,9)/10 + .025, 5)
        self.y_pos = round(randint(1,9)/10 + .025, 5)
        #this loop will continue until a location that doesnt overlap the snake is found
        while (self.x_pos, self.y_pos) in s.snake_location:
            self.x_pos = round(randint(1,9)/10 + .025, 5)
            self.y_pos = round(randint(1,9)/10 + .025, 5)

def is_file_empty(file_name:str)->bool:
    """
        this function checks if the imputed file name is empty or not
        perameters: file_name: str
        return: bool
        """
    #open file to read
    with open(file_name, 'r') as read_obj:
        #read first character
        one_char = read_obj.read(1)
        #if not fetched then file is empty
        if not one_char:
           return True
    return False

    
        


        
        
                
dudraw.set_canvas_size(700,700)
#the snake and food objects are created
s = Snake()
f = Food()
#this controls how often the game updates the screen, lower means faster
limit = 10
#this variable counts up each frame, and once it reaches the limit, a frame is animated, and it goes back to 0
timer = 0
#the key is set to w, index zero is the previous key, index one is the current one
key = ["","w"]
#the dir variable is set the current key value, so the snake begins going upwards
dir = s.change_heading(key[1])
#the crash variable is set to false, becuase the snake has not crashed yet
crash = False
#the typed variable is set to false, because a key has not been typed yet
typed = False
#while crash is not true...
while not crash:
    #if the snake hits the wall or itself, the loop will break
    if s.detect_wall() or s.detect_self():
            crash = True
    #if a key is typed...
    if dudraw.has_next_key_typed():
        #if the typed variable is not true (if no key has been typed before the key just typed)...
        if not typed:
            #the typed variable is set to true, because a key has been typed
            typed = True 
            #the previous index of the key variable is set to the old current key
            key[0] = key[1]
            #the current variable is set to the key that has been typed
            key[1] = dudraw.next_key_typed()
            
                
            #this all checks to make sure that the snake cant do a u turn
            #for example, if the previous key is a, that means the snake is going left, meaning d can't be an input
            #because the snake would immidialtly go right, and so on
            if not (key[0] == "a" and key [1] == "d"):
                if not (key[0] == "d" and key [1] == "a"):
                    if not (key[0] == "w" and key [1] == "s"):
                        if not (key[0] == "s" and key [1] == "w"):
                            #the dir variable is set to the output of the change_heading() function with the input of the user
                            dir = s.change_heading(key[1])
    #if the timer == the limit or 0, meaning 20 processing frames have passed
    if timer == limit or timer == 0:
        #typed is reset to false (doing this, only one keypress can be administered bwetween each animation frame)
        typed = False
        #the timer is reset to 0
        timer = 0
        #the canvas is cleared
        dudraw.clear()
        #the food is drawn
        f.draw(s)
        #the snake is drawn
        s.draw_snake()
        #if the snake detects food...
        if s.detect_food(f):
            #the location of the food is reset
            f.reset_location(s)
            #a new piece of food is drawn
            f.draw(s)
            #the snake grows in the direction of the users keypress
            s.snake_grow(dir[0], dir[1])
        #else...
        else:
            #the snake just moves in the direction of the users keypress
            s.move(dir[0], dir[1])
    #the frame is shown for 10 miliseconds before updating
    dudraw.show(10)
    #the timer is incrimented by one
    timer += 1

#this will create a highscore file if there is none
with open(f"HIGHSCORE.txt", "a") as a_file:
    pass
#if the file is not empty...
if not is_file_empty("HIGHSCORE.txt"):

    #opens to read and write highscore file
    with open(f"HIGHSCORE.txt", "r+") as a_file:
        #defines the high score as what ever is in the file
        highscore = a_file.read()
       
else:
    #the high score is set to 0
    highscore = "0"


#opens the highscore file to write to it
with open(f"HIGHSCORE.txt", "w") as a_file:
    #if the highscore is less than the snake length of the game just played, the highscore becomes the snake length
    if int(highscore) < s.snake_length:
        highscore = s.snake_length
    #the highscore is written to the file
    a_file.write(f"{highscore}")


#this code runs once the animation while loop breaks, so if the snake crashes
#the pen color is set to red
dudraw.set_pen_color(dudraw.RED)
dudraw.set_font_size(30)
#crash is shown on screen, and the score of the player (the length of the snake) along with the highscore
dudraw.text(.5,.5,f"CRASH!\nScore: {s.snake_length}\nHighscore: {highscore}")
#this killscreen is shown for 10 seconds
dudraw.show(10000)