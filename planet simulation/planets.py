import pygame
import math
pygame.init()

WIDTH, HEIGHT =  1000, 1000
SCALE_MULTIPLIER = 1
TARGET_SCALE_MULTIPLIER = 1
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
	AU = 149.6e6 * 1000
	G = 6.67428e-11
	SCALE = 250  / AU  # 1AU = 100 pixels
	TIMESTEP = 3600*24 # 1 day

	def __init__(self, x, y, radius, color, mass, image_path = "null"):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.mass = mass
		self.image_path = image_path

		self.orbit = []
		self.sun = False
		self.distance_to_sun = 0

		self.x_vel = 0
		self.y_vel = 0

	def setxy(self, x, y):
		self.x = x
		self.y = y
		print("self ")
		print(y)
  
	def draw(self, win):
		x = self.x * self.SCALE * SCALE_MULTIPLIER + WIDTH / 2
		y = self.y * self.SCALE * SCALE_MULTIPLIER + HEIGHT / 2
  
		if len(self.orbit) > 2:
			updated_points = []
			for point in self.orbit:
				x, y = point
				x = x * self.SCALE * SCALE_MULTIPLIER + WIDTH / 2
				y = y * self.SCALE * SCALE_MULTIPLIER + HEIGHT / 2
				updated_points.append((x, y))

			pygame.draw.lines(win, self.color, False, updated_points, 2)
		if self.image_path == "null":
			pygame.draw.circle(win, self.color, (x, y), self.radius)
		else:
			image = pygame.image.load(self.image_path)
			image_x = clamp(48 * SCALE_MULTIPLIER, 16, 56)
			image_y = clamp(48 * SCALE_MULTIPLIER, 16, 55)
			resized_image = pygame.transform.scale(image, (image_x, image_y))
			win.blit(resized_image, (x - image_x/2, y - image_y/2))
			
		if not self.sun:
			distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
			win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

	def attraction(self, other):
		other_x, other_y = other.x, other.y
		distance_x = other_x - self.x
		distance_y = other_y - self.y
		distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

		if other.sun:
			self.distance_to_sun = distance

		force = self.G * self.mass * other.mass / distance**2
		theta = math.atan2(distance_y, distance_x)
		force_x = math.cos(theta) * force
		force_y = math.sin(theta) * force
		return force_x, force_y

	def update_position(self, planets):
		total_fx = total_fy = 0
		for planet in planets:
			if self == planet:
				continue

			fx, fy = self.attraction(planet)
			total_fx += fx
			total_fy += fy

		self.x_vel += total_fx / self.mass * self.TIMESTEP
		self.y_vel += total_fy / self.mass * self.TIMESTEP

		self.x += self.x_vel * self.TIMESTEP
		self.y += self.y_vel * self.TIMESTEP
		self.orbit.append((self.x, self.y))

def clamp(n, min, max):
	if n < min:
		return min
	elif n > max:
		return max
	else:
		return n

def main():
	run = True
	clock = pygame.time.Clock()

	sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30, "sun.png")
	sun.sun = True

	earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24, "earth.png")
	earth.y_vel = 29.783 * 1000 

	mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23, "mars.png")
	mars.y_vel = 24.077 * 1000

	mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23, "mercury.png")
	mercury.y_vel = -47.4 * 1000

	venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24, "venus.png")
	venus.y_vel = -35.02 * 1000

	jupiter = Planet(5.203 * Planet.AU, 0, 20, WHITE, 1.898 * 10**27, "jupiter.png")
	jupiter.y_vel = 13.07 * 1000
 
	saturn = Planet(9.555 * Planet.AU, 0, 16, WHITE, 5.683 * 10**26, "saturn.png")
	saturn.y_vel = 9.68 * 1000
 
	uranus = Planet(19.218 * Planet.AU, 0, 16, WHITE, 8.681 * 10**25, "uranus.png")
	uranus.y_vel = 9.68 * 1000
 
	neptune = Planet(30.110 * Planet.AU, 0, 16, WHITE, 1.024 * 10**26, "neptune.png")
	neptune.y_vel = 6.79 * 1000
 
	planets = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune]
	global SCALE_MULTIPLIER
	global TARGET_SCALE_MULTIPLIER
 
	instruction_font = pygame.font.SysFont("comicsans", 20)
	instruction_text = instruction_font.render("Press UP to zoom in, DOWN to zoom out", 1, WHITE)
	move_instruction_text = instruction_font.render("Use WASD keys to move the planets", 1, WHITE)

	while run:
		clock.tick(60)
		WIN.fill((0, 0, 0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type != pygame.KEYDOWN:
				continue
			if event.key == pygame.K_UP:
				TARGET_SCALE_MULTIPLIER += 0.01
			if event.key == pygame.K_DOWN:
				TARGET_SCALE_MULTIPLIER -= 0.01
			elif event.key == pygame.K_w:  # Move up
				print("UP")
				for planet in planets:
					planet.setxy(planet.x, planet.y)
					print(planet.y)
			elif event.key == pygame.K_s:  # Move down
				for planet in planets:
					planet.y += 10 / SCALE_MULTIPLIER  # Adjust the value as needed
			elif event.key == pygame.K_a:  # Move left
				for planet in planets:
					planet.x -= 10 / SCALE_MULTIPLIER  # Adjust the value as needed
			elif event.key == pygame.K_d:  # Move right
				for planet in planets:
					planet.x += 10 / SCALE_MULTIPLIER
		if round(TARGET_SCALE_MULTIPLIER, 3) > round(SCALE_MULTIPLIER, 4):
			SCALE_MULTIPLIER = round(SCALE_MULTIPLIER + 0.001, 4)
		elif round(TARGET_SCALE_MULTIPLIER, 3) < round(SCALE_MULTIPLIER, 4):
			SCALE_MULTIPLIER = round(SCALE_MULTIPLIER - 0.010, 4)
		for planet in planets:
			planet.update_position(planets)
			planet.draw(WIN)

		WIN.blit(instruction_text, (10, 10))  # Position the instruction text on the screen
		WIN.blit(move_instruction_text, (10, 40))  # Position the move instruction text on the screen
		pygame.display.update()

	pygame.quit()

# TODO: Holding buttons, moving from side to side, speed scaler, maybe dont render when to far away
main()