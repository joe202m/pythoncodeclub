'''Moon Lander Game 1
   Simple text-based version of a moon landing game. 1D with minimal physics.
'''
import pygame

screen = pygame.display.set_mode((300,600))

grey = pygame.Color(200,200,200)
red = pygame.Color(255,0,0)

points = [(150, 0), (145, 5), (155, 5)]

rocket_area = pygame.Surface((300,600))

pygame.draw.lines(rocket_area,red,True,points)

screen.blit(rocket_area, (0, 0))

pygame.display.update()


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
time_step = 1.0       # Simulation time step (s)

# Initial conditions
time = 0.0
height = pericynthion
speed = 0.0

# Current time, height, speed & fuel_supply
print ("Time = {:.1f}s, Height = {:.0f}m, Descent speed = {:.2f}m/s, Fuel {:.2f}kg".
	   format(time, height, speed, fuel_supply))

		   # Loop until landed or crashed
while (height > 0):
    # Thrust must be 10% - 60% or 100%
    thrust = -1.0
    while(thrust < 0.0 or
          (thrust > 0.0 and thrust < throttle_min) or
          (thrust > throttle_max and thrust < 1.0) or
          thrust > 1.0):
        thrust = float(input("Thrust (% [10-60 or 100])? ")) / 100.0 # Convert from percentage

    thrust_time = -1.0
    while (thrust_time < 0):
        thrust_time = float(input("Thrust time (s)? "))
    
    for ii in range(int(thrust_time // time_step)):
        time = time + time_step
        thrust = min(thrust, fuel_supply / (burn_rate * time_step))
        speed = speed + (gravity_0 - thrust * DPS_thrust / LM_mass) * time_step
        height = height - speed * time_step
        fuel_used = thrust * burn_rate * time_step
        fuel_supply = fuel_supply - fuel_used
        LM_mass = LM_mass - fuel_used

        # Current time, height, speed & fuel_supply
        print ("Time = {:.1f}s, Height = {:.0f}m, Descent speed = {:.2f}m/s, Fuel {:.2f}kg".
	           format(time, height, speed, fuel_supply))

        if height < 0.0:
            break

if abs(speed) < max_impact_speed:
    print("Landed!")
else:
    print("Oops!!")
