import pygame
import math
from queue import PriorityQueue
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
    VISITED = '#83fce0'
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

    def make_start(self):
        self.state = State.START
    
    def make_end(self):
        self.state = State.FINISH

    def make_barrier(self):
        self.state = State.BARRIER

    def is_normal(self):
        return self.state == State.NORMAL
    
    def is_start(self):
        return self.state == State.START
    
    def is_finish(self):
        return self.state == State.FINISH
    
    def is_weight(self):
        return self.state == State.WEIGHT
    
    def is_barrier(self):
        return self.state == State.BARRIER
    
    def is_queue(self):
        return self.state == State.QUEUE
    
    def is_visiting(self):
        return self.state == State.VISITING
    
    def is_visited(self):
        return self.state == State.VISITED
    
    def is_path(self):
        return self.state == State.PATH
    
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
        # check all directions for barriers
        self.neighbors = []
        # In the same column as self check if row below exists and if we can add it (not barrier)
        if self.row < self.rows_tot -1 and not grid[self.row + 1][self.col].is_barrier():
             self.neighbors.append(grid[self.row -1][self.col].state)
        # check row above
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        # In the same row as self check if col to the right exists and if we can add it (not barrier)
        if self.col < self.rows_tot - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        # check col left
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
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

def bfs(draw, grid, start, end):
    pass


def main(win, width):
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
					start.make_start()

				elif not end and spot != start: #init end anywhere but end node
					end = spot
					end.make_end()

				elif spot != end and spot != start: #make barrier anywhere but start/end node
					spot.make_barrier()

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
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					bfs(lambda: draw(win, grid, ROWS, width), grid, start, end)
                
                #clear grid
				if event.key == pygame.K_c:  # C-key
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

if __name__ == "__main__":
      main(WIN, WIDTH)