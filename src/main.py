import pygame
import math
from queue import PriorityQueue, Queue
from collections import deque
from enum import Enum

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('A* Path Finding Algo')

class State(Enum):
	""" different states a node may be in """

	NORMAL = '#f6f4f2'
	START = '#71DE5F'
	FINISH = '#F15353'
	WEIGHT = '#eba173'
	BARRIER = '#434343'
	QUEUE = '#ebbfff'
	VISITING = '#fc03c6'
	came_from = '#83fce0'
	PATH = '#f2fc83'

class Node:
	def __init__(self, row, col, width, rows_tot):
		self.row = row
		self.col = col
		self.width = width
		self.rows_tot = rows_tot
		self.pos = self.row, self.col
		self.x = row * width
		self.y = col * width
		self._state = State.NORMAL
		self.neighbors = []

	def __repr__(self):
		return '<Node {}, State \'{}\'>'.format(self.pos, self.state.name)
	
	def __lt__(self, other):
		return False

	def is_barrier(self):
		return self.state == State.BARRIER
	
	def reset(self):
		self.state = State.NORMAL

	@property
	def state(self):
		return self._state
	
	@state.setter
	def state(self, state):
		self._state = state
	
	def draw(self, win):
		# print(self.state)
		
		pygame.draw.rect(win, self.state.value, (self.x, self.y, self.width, self.width))
	
	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.rows_tot - 1 and not grid[self.row + 1][self.col].is_barrier() and grid[self.row + 1][self.col]:
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier() and grid[self.row - 1][self.col]:
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.rows_tot - 1 and not grid[self.row][self.col + 1].is_barrier() and grid[self.row][self.col + 1]:
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier() and grid[self.row][self.col - 1]:
			self.neighbors.append(grid[self.row][self.col - 1])
	

def manhattan(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def make_grid(rows, width):
	grid = []
	gap = width // rows #width of each cube
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			n = Node(i, j ,gap, rows) 
			grid[i].append(n)
	return grid

def draw_grid(win, rows, width):
	gap = width // rows #width of each cube
	grey = (128, 128, 128)
	for i in range(rows): 
		pygame.draw.line(win, grey, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, grey, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
	win.fill('#f6f4f2')

	for row in grid:
		for node in row:
			node.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update() #take whats drawn and update display

def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		if current is None:
			break
		if current.state != State.START and current.state != State.FINISH:
			current.state = State.PATH
		draw()

def bfs(draw, start, end):
	print('BFS')
	que = Queue() #initial queue
	que.put(start)
	came_from = {} #Visited
	came_from[start] = None

	while not que.empty(): 
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return False

		cur = que.get() #remove node and set to curr
		if cur == end: #path found
			reconstruct_path(came_from, end, draw)
			end.state = State.FINISH #change color
			return True

		for n in cur.neighbors: #traverse neighbors not visted
			if n not in came_from:
				came_from[n] = cur #add to visted
				n.state = State.came_from #color update
				draw()
				que.put(n)	#add neighbor to queue
		
	return False

def dfs(draw, current, end, came_from):
    if current == end:  # Path found
        reconstruct_path(came_from, end, draw)
        return True

    for neighbor in current.neighbors:
        if neighbor not in came_from:
            came_from[neighbor] = current  # Add to visited nodes
            neighbor.state = State.came_from  # Color update
            draw()  # Update the visualization

            if dfs(draw, neighbor, end, came_from):
                return True

    return False


def dfs_search(draw, start, end):
    came_from = {}  # Visited nodes
    came_from[start] = None

    return dfs(draw, start, end, came_from)


def main(win, width):
	pygame.font.init()
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			
			#Assigning Grid Node
			if pygame.mouse.get_pressed()[0]: # LEFT-CLICK
				pos = pygame.mouse.get_pos() 
				row, col = get_clicked_pos(pos, ROWS, width) #get the node position
				spot = grid[row][col] #get node at pos
				if not start and spot != end: #init start anywhere but end node
					start = spot
					start.state = State.START

				elif not end and spot != start: #init end anywhere but end node
					end = spot
					end.state = State.FINISH

				elif spot != end and spot != start: #make barrier anywhere but start/end node
					spot.state = State.BARRIER

			# Clearing Grid Node
			elif pygame.mouse.get_pressed()[2]: # RIGHT-CLICK
				pos = pygame.mouse.get_pos() 
				row, col = get_clicked_pos(pos, ROWS, width) #get the node position
				spot = grid[row][col] #get node at pos
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			#begin Algorithm by updating neighbors for each node in grid
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_b and start and end: # b-key = bfs
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)
					bfs(lambda: draw(win, grid, ROWS, width), start, end)
				if event.key == pygame.K_d and start and end: # d-key = dfs
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)
					dfs_search(lambda: draw(win, grid, ROWS, width), start, end)
				#clear grid
				if event.key == pygame.K_c:  # C-key
					start = None
					end = None
					grid = make_grid(ROWS, width)
	pygame.quit()

if __name__ == "__main__":
	  main(WIN, WIDTH)