import pygame
import random
import math
pygame.init()

class DrawInformation:
	BLACK = 0, 0, 0
	WHITE = 255, 255, 255
	GREEN = 0, 255, 0
	RED = 255, 0, 0
	BACKGROUND_COLOR = WHITE

	GRADIENTS = [
		(128, 128, 128),
		(160, 160, 160),
		(192, 192, 192)
	]

	FONT = pygame.font.SysFont('comicsans', 20)
	LARGE_FONT = pygame.font.SysFont('comicsans', 30)

	SIDE_PAD = 100
	TOP_PAD = 150

	def __init__(self, width, height, lst):
		self.width = width
		self.height = height

		self.window = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Sorting Algorithm Visualization")
		self.set_list(lst)

	def set_list(self, lst):
		self.lst = lst
		self.min_val = min(lst)
		self.max_val = max(lst)

		self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
		self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
		self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):
	draw_info.window.fill(draw_info.BACKGROUND_COLOR)

	title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
	draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

	controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
	draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))

	sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK)
	draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 75))
 
	sorting2 = draw_info.FONT.render("M - Merge Sort | Q - Quick Sort", 1, draw_info.BLACK)
	draw_info.window.blit(sorting2, (draw_info.width/2 - sorting2.get_width()/2 , 105))
	draw_list(draw_info)
	pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
	lst = draw_info.lst

	if clear_bg:
		clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
						draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

	for i, val in enumerate(lst):
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

		color = draw_info.GRADIENTS[i % 3]

		if i in color_positions:
			color = color_positions[i] 

		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

	if clear_bg:
		pygame.display.update()


def generate_starting_list(n, min_val, max_val):
	lst = []

	for _ in range(n):
		val = random.randint(min_val, max_val)
		lst.append(val)

	return lst


def bubble_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]

			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
				draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
				yield True

	return lst

def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst
    n = len(lst)
    for i in range(n):
        swap_idx = i
        for j in range(i+1, n):
            if (ascending and lst[j] < lst[swap_idx]) or (not ascending and lst[j] > lst[swap_idx]):
                swap_idx = j

            # Highlight the currently inspected block and the current minimum/maximum block
            draw_list(draw_info, {j: draw_info.RED, swap_idx: draw_info.GREEN}, True)
            yield True

        # Swap the minimum/maximum element with the first unsorted position
        lst[i], lst[swap_idx] = lst[swap_idx], lst[i]
        # Also update the visual representation
        draw_info.lst[i], draw_info.lst[swap_idx] = draw_info.lst[swap_idx], draw_info.lst[i]

        # Highlight the swapped positions and visualize the change
        draw_list(draw_info, {i: draw_info.GREEN, swap_idx: draw_info.RED}, True)
        yield True

    return lst

def insertion_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(1, len(lst)):
		current = lst[i]

		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			lst[i] = lst[i - 1]
			i = i - 1
			lst[i] = current
			draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
			yield True

	return lst

def merge_sort(draw_info, ascending=True, lst=None, l=0, r=None):
    if r is None:
        r = len(draw_info.lst) - 1
    if lst is None:
        lst = draw_info.lst.copy()

    if l < r:
        mid = (l + r) // 2
        yield from merge_sort(draw_info, ascending, lst, l, mid)
        yield from merge_sort(draw_info,ascending, lst, mid + 1, r)
        yield from merge(draw_info, lst, l, mid, mid + 1, r, ascending)
        draw_list(draw_info, {i: draw_info.RED for i in range(l, r+1)}, True)
        yield True

    return lst

def merge(draw_info, lst, x1, y1, x2, y2, ascending=True):
    i = x1
    j = x2
    temp = []

    pygame.event.pump()

    while i <= y1 and j <= y2:
        if (ascending and lst[i] <= lst[j]) or (not ascending and lst[i] >= lst[j]):
            temp.append(lst[i])
            i += 1
        else:
            temp.append(lst[j])
            j += 1
        draw_list(draw_info, {k: draw_info.RED for k in range(x1, y2+1)}, True)
        yield True

    while i <= y1:
        temp.append(lst[i])
        i += 1
        draw_list(draw_info, {k: draw_info.RED for k in range(x1, y2+1)}, True)
        yield True

    while j <= y2:
        temp.append(lst[j])
        j += 1
        draw_list(draw_info, {k: draw_info.RED for k in range(x1, y2+1)}, True)
        yield True

    for i, val in enumerate(temp, x1):
        lst[i] = val
        draw_info.lst[i] = val
        draw_list(draw_info, {i: draw_info.GREEN}, True)
        yield True

def quick_sort(draw_info, ascending=True, lst=None, low=0, high=None):
    if high is None:
        high = len(draw_info.lst) - 1
    if lst is None:
        lst = draw_info.lst.copy()

    if low < high:
        pi = yield from partition(draw_info, lst, low, high, ascending)
        yield from quick_sort(draw_info, ascending, lst, low, pi - 1)
        yield from quick_sort(draw_info, ascending, lst, pi + 1, high)

    return lst

def partition(draw_info, lst, low, high, ascending=True):
    i = low - 1
    pivot = lst[high]
    for j in range(low, high):
        if (ascending and lst[j] <= pivot) or (not ascending and lst[j] >= pivot):
            i = i + 1
            lst[i], lst[j] = lst[j], lst[i]
            draw_info.lst[i], draw_info.lst[j] = draw_info.lst[j], draw_info.lst[i]
            draw_list(draw_info, {i: draw_info.RED, j: draw_info.GREEN}, True)
            yield True

    lst[i + 1], lst[high] = lst[high], lst[i + 1]
    draw_info.lst[i + 1], draw_info.lst[high] = draw_info.lst[high], draw_info.lst[i + 1]
    draw_list(draw_info, {i + 1: draw_info.GREEN, high: draw_info.RED}, True)
    yield True
    return i + 1

# Flag to check if knob is being dragged
dragging = False

# Delays (feel free to adjust these values)
slow_speed = 200
normal_speed = 100
fast_speed = 50
delay_time = normal_speed  # Start with normal speed by default

def main():
	run = True
	clock = pygame.time.Clock()

	n = 50
	min_val = 0
	max_val = 100

	lst = generate_starting_list(n, min_val, max_val)
	draw_info = DrawInformation(800, 600, lst)
	sorting = False
	ascending = True

	sorting_algorithm = bubble_sort
	sorting_algo_name = "Bubble Sort"
	sorting_algorithm_generator = None

	while run:
		clock.tick(60)
		## pygame.time.wait(50) 
        
		if sorting:
			try:
				next(sorting_algorithm_generator)
			except StopIteration:
				sorting = False
		else:
			draw(draw_info, sorting_algo_name, ascending)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type != pygame.KEYDOWN:
				continue
			if event.key == pygame.K_r:
				lst = generate_starting_list(n, min_val, max_val)
				draw_info.set_list(lst)
				sorting = False
			elif event.key == pygame.K_SPACE and sorting == False:
				sorting = True
				sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
			elif event.key == pygame.K_a and not sorting:
				ascending = True
			elif event.key == pygame.K_d and not sorting:
				ascending = False
			elif event.key == pygame.K_i and not sorting:
				sorting_algorithm = insertion_sort
				sorting_algo_name = "Insertion Sort"
			elif event.key == pygame.K_b and not sorting:
				sorting_algorithm = bubble_sort
				sorting_algo_name = "Bubble Sort"
			elif event.key == pygame.K_m and not sorting:
				sorting_algorithm = merge_sort
				sorting_algo_name = "Merge Sort"
			elif event.key == pygame.K_q and not sorting:
				sorting_algorithm = quick_sort
				sorting_algo_name = "Quick Sort"       
			elif event.key == pygame.K_s and not sorting:
				sorting_algorithm = selection_sort
				sorting_algo_name = "Selection Sort" 
    
	pygame.quit()

if __name__ == "__main__":
	main()