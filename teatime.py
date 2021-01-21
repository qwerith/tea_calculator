from math import pi


def calculate_tea_cooldown_time(cup_radius: float, water_weight: float, preferred_temp: float) -> float:
    """
    Function to calculate time, when water in a cup reaches desired temperature

    Keyword arguments:

    cup_radius -- cup surface radius (in meters) e.g 0.05 m 

    water_weight -- weight of water in a cup (in kg) e.g. 0.5 kg for 500 ml 
    """
    c_water = 4218  # J / (kg * K) - thermal conductivity of water
    tea_temp = 100  # temperature of tea in a cup
    target_temp = preferred_temp  # target tea temperature (you can change to your desired)
    # energy difference, that is produced from cooling from tea_temp to target_temp (100 degrees to 50 degress here)
    Q1 = c_water * water_weight * (tea_temp - target_temp)
    water_surface_area = pi * cup_radius * cup_radius  # surface area
    air_temperature = 20  # temperature of air around the cup
    heat_conductivity = 510  # water + air surface conductivity
    # calculate how much heat is transferred from water to air
    Q2 = heat_conductivity * water_surface_area * (tea_temp - air_temperature)
    return Q1 / Q2  # calculate cooling time (in seconds)
