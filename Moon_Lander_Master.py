'''Moon Lander Game 1
   Simple text-based version of a moon landing game. 1D with minimal physics.
'''
import sys, pygame
pygame.init()

scr_size = 1000, 800
scr_height = 800
black = 0, 0, 0
white = 255, 255, 255

screen = pygame.display.set_mode(scr_size)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 0, 0))

def print_pg(text, text_y,text_size=24):
    font = pygame.font.Font(None, text_size)
    for text_line in text.split("\n"):
        line = font.render(text_line, 1, (128, 255, 128))
        pygame.draw.rect(background, black, (0, text_y - 12, 250, text_size))
        textpos = line.get_rect(left = 20, centery = text_y)
        background.blit(line, textpos)
        text_y += text_size
        print (textpos)

def display_lander(lander, height):
    pygame.draw.rect(background, black, (251, 0, 750, 800))
    background.blit(lander, (450, 800 - height * 800 / pericynthion - 45))
    screen.blit(background, (0, 0))
    pygame.display.flip()

lander = pygame.image.load("Apollo_LunarModule.png")
lander = pygame.transform.scale(lander, (58, 45))
lander_rect = lander.get_rect()

# Physics and lander constants
gravity_0 = 1.62      # Moon's gravity at surface
LM_mass = 15.2e3      # Launch mass of LM (15.2 tonnes)
DPS_thrust =  45.04e3 # Descent propulsion system full power thrust (N)
burn_rate = 7.5       # Fuel use at 100% thrust, kg/s
fuel_supply = 900     # Fuel available for descent
throttle_min = 0.1
throttle_max = 0.6    # DPS engine can be throttled between 10% & 60% of full thrust
pericynthion = 15.0e3 # Lowest point in Lunar orbit - descend from here
max_impact_speed = 10 # Gives ~ 3g over 1.7m
time_step = 1         # Simulation time step (s)

# Initial conditions
height = pericynthion
speed = 0.0
thrust = 0.0
time = 0.0

# Loop until landed or crashed
while (height > 0):
    # Current time, height, thrust & speed
    print_pg("Time = {:.1f} s\nHeight = {:.0f} m\nThrust = {:.0f} N\nDescent speed = {:.2f} m/s\nFuel = {:.1f} kg".
             format(time, height, thrust * DPS_thrust, speed, fuel_supply), 12)
    display_lander(lander, height)

    # Thrust must be 10% - 60% or 100%
    for event in pygame.event.get():
            
            # determine if X was clicked, or Ctrl+W or Alt+F4 was used
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    break
            
                # determine if a letter key was pressed
                if event.key == pygame.K_b:
                    thrust = 1.0
                elif event.key == pygame.K_0:
                    thrust = 0.0
 
    thrust_time = 1.0
    time += time_step
    #while (thrust_time < 0):
     #  thrust_time = float(input("Thrust time (s)? "))
    
    for ii in range(int(thrust_time // time_step)):
        prev_height = height
        thrust = min(thrust, fuel_supply / (burn_rate * time_step))
        speed = speed + (gravity_0 - thrust * DPS_thrust / LM_mass) * time_step
        height = height - speed * time_step
        fuel_used = thrust * burn_rate * time_step
        fuel_supply = fuel_supply - fuel_used
        LM_mass = LM_mass - fuel_used


        if (height <= 0.0):
            break

    pygame.time.delay(int(thrust_time * 10))
        
print_pg("Time = {:.1f} s\nHeight = {:.0f} m\nThrust = {:.0f} N\nDescent speed = {:.2f} m/s\nFuel = {:.1f} kg".
         format(time, height, thrust * DPS_thrust, speed, fuel_supply), 12)

if abs(speed) < max_impact_speed:
    print_pg("Landed!", 180,120)
else:
    print_pg("Oops!!", 180,120)

display_lander(lander, height)

print (speed)
print (max_impact_speed)
print (height)
pygame.time.delay(5000)

