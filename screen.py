from tkinter import Tk, Canvas
from tsp import TSP
from solvers import Solver

CANVAS_SIZE = 800
CANVAS_COLOR = '#DDDDDD'

CIRCLE_SIZE = 10
CIRCLE_COLOR = '#444444'

LINE_SIZE = 4
LINE_COLOR = '#444444'

START_TIME = 1000
STEP_TIME = 10

def draw(solver: Solver):
    root = Tk()
    
    canvas = Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE, bg=CANVAS_COLOR)
    
    circles: list[int] = []
    
    min_x = min(coord.x for coord in solver.tsp.xy)
    max_x = max(coord.x for coord in solver.tsp.xy)
    min_y = min(coord.y for coord in solver.tsp.xy)
    max_y = max(coord.y for coord in solver.tsp.xy)
    
    for coord in solver.tsp.xy:
        x = (coord.x - min_x) / (max_x - min_x) * CANVAS_SIZE
        y = (coord.y - min_y) / (max_y - min_y) * CANVAS_SIZE
        
        top = y - CIRCLE_SIZE / 2
        left = x - CIRCLE_SIZE / 2
        bottom = y + CIRCLE_SIZE / 2
        right = x + CIRCLE_SIZE / 2
        
        circles.append(
            canvas.create_oval(top, left, bottom, right, fill=CIRCLE_COLOR, width=0)
        )
    
    lines: list[int] = []
    
    def update(i=0):
        print(f'* SCREEN UPDATE: {i + 1}/{len(solver.steps)}')
        
        state = solver.steps[i]
        
        canvas.delete(*lines)
        
        for prev, next in zip(state.value, state.value[1:] + state.value[:1]):
            prev_coords = canvas.coords(circles[prev - 1])
            next_coords = canvas.coords(circles[next - 1])
            
            prev_x = (prev_coords[0] + prev_coords[2]) / 2
            prev_y = (prev_coords[1] + prev_coords[3]) / 2
            
            next_x = (next_coords[0] + next_coords[2]) / 2
            next_y = (next_coords[1] + next_coords[3]) / 2
            
            lines.append(
                canvas.create_line(prev_x, prev_y, next_x, next_y, width=LINE_SIZE, fill=LINE_COLOR)
            )
        
        for circle in circles:
            canvas.tag_raise(circle)
        
        if i + 1 == len(solver.steps):
            return
        
        canvas.after(STEP_TIME, update, i + 1)
    
    canvas.after(START_TIME, update)
        
    canvas.pack()
    
    root.mainloop()
