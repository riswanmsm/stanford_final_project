"""
    This program will open provided world map image
    Read latitude, longitude and population data from countries csv file provided in countries population folder
    Read total covid 19 infected cases from txt files in the countries covid directory
    Plot on the world map according to the data read from these files
    Get all the total population from all the city population data and divide city population by that to get population density
    If population density is higher plot the pixel of the image in the lat long cordinate 
    High density will be red and law will be black and the color vary between these two according to the density
    Covid cases for that country divided by the country population gathered from the cities and marked as covid effect
    If covid effect high green colour of the pixer will be high otherwise green will be 0 so green varies between 0 and 255
    The pixel representing cities will be shown according to the below
        if population density is high and covid effect is high - pixel.red = high and pixel.green = high so it will looks yeellow
        if population density is low and covid effect is high - pixel.red = low and pixel.green = high so it will looks green
        if population density is low and covid effect is low - pixel.red = low and pixel.green = low so it will looks black
    * The data gathered here is from the files provided for our course in Ed platform
    * The total population and the country population covid cases are taken from those files
    * Some places country population is lower than country covid case because the country population only counts from the cities provided in the file 
"""
from simpleimage import SimpleImage
import os

DEFAULT_IMAGE = 'img/green_world.jpg'
COUNTRY_POPULATION_DIRECTORY = "countries/population/"
COUNTRY_COVID_DIRECTORY = "countries/covid/"
VISUALIZATION_WIDTH = 1019
VISUALIZATION_HEIGHT = 471
MIN_LONGITUDE = -180
MAX_LONGITUDE = 180
MIN_LATITUDE = -90
MAX_LATITUDE = 90

def plot_country(visualization, filename, covid_file_name, world_population):
    """
    Collect the latitude and longitude data of each city of a country
    Collect final covid cases from the files in covid directory
    Plot each cities in the country through looping
    """
    country_covid_case = get_country_covid_case(covid_file_name)
    plot_data = get_plot_data(filename)

    lat = plot_data['lat']
    lon = plot_data['lon']
    population = plot_data['population']
    country_city_population = plot_data['country_city_population']

    covid_effect = get_covid_effect(country_covid_case, country_city_population)
    
    for i in range(len(lat)):
        population_density = get_population_density(population[i], world_population)  
        if population_density > 0:
            # print(population_density, covid_effect)
            plot_one_city(visualization, lat[i], lon[i], population_density, covid_effect)

def get_plot_data(filename):
    lat = []
    lon = []
    population = []
    country_city_population = 0
    with open(filename) as cities_file:
        next(cities_file) # skip the header line
        for line in cities_file:
            line = line.strip()
            parts = line.split(",")
            lat.append(float(parts[1]))
            lon.append(float(parts[2]))
            if parts[3]:
                population.append(float(parts[3]))
                country_city_population += float(parts[3])
            else:
                population.append(0.0)
    plot_data = {'lat': lat, 'lon': lon, 'population': population, 'country_city_population': country_city_population}
    return plot_data 

def get_country_covid_case(covid_file_name):
    country_covid_cases = 0
    if os.path.exists(covid_file_name):
        with open(covid_file_name) as covid_file:
            for line in covid_file:
                line = line.strip()
            country_covid_cases = int(line)
    return country_covid_cases

def get_population_density(city_population, world_population):
    return 50000 * city_population / world_population

def get_covid_effect(country_covid_cases, country_city_population):
    # lst_population_density.append(10 * country_covid_cases / country_city_population)
    return 8 * country_covid_cases / country_city_population

def plot_one_city(visualization, latitude, longitude, population_density, covid_effect):

    x = longitude_to_x(longitude)
    y = latitude_to_y(latitude)

    # if the pixel is in bounds of the window we specified through constants,
    # plot it
    if 0 < x < visualization.width and 0 < y < visualization.height:
        plot_pixel(visualization, x , y, population_density, covid_effect)
    
def longitude_to_x(longitude):
    """
    Scales a longitude coordinate to a coordinate in the visualization email
    """
    return VISUALIZATION_WIDTH * (longitude - MIN_LONGITUDE) / (MAX_LONGITUDE - MIN_LONGITUDE)

def latitude_to_y(latitude):
    """
    Scales a latitude coordinate to a coordinate in the visualization email
    """
    return VISUALIZATION_HEIGHT * (1.0 - (latitude - MIN_LATITUDE) / (MAX_LATITUDE - MIN_LATITUDE))

def plot_pixel(visualization, x, y, population_density, covid_effect):
    pixel = visualization.get_pixel(x, y)
    pixel.red = 255 if 255 * population_density > 255 else int(255 * population_density)
    pixel.green = 255 if 255 * covid_effect > 255 else int(255 * covid_effect)
    pixel.blue = 0

def get_world_population(all_countries):
    world_population = 0
    for country in all_countries:
        country_filename = COUNTRY_POPULATION_DIRECTORY + country + ".csv"
        with open(country_filename) as cities_file:
            next(cities_file) # skip the header line

            for line in cities_file:
                line = line.strip()
                parts = line.split(",")
                if parts[3] != '':
                    city_population = float(parts[3])
                    world_population += city_population
    return world_population
    
def main():
    image = SimpleImage(DEFAULT_IMAGE)

    all_countries = [s.split(".")[0] for s in os.listdir(COUNTRY_POPULATION_DIRECTORY)]
    world_population = get_world_population(all_countries)
    for country in all_countries:
        country_filename = COUNTRY_POPULATION_DIRECTORY + country + ".csv"
        covid_file_name = COUNTRY_COVID_DIRECTORY + country + ".txt"
        plot_country(image, country_filename, covid_file_name, world_population)

    image.show()
    
if __name__ == '__main__':
    main()