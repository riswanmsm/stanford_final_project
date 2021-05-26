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

lst_population_density = []

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
            print(population_density, covid_effect)
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
    lst_population_density.append(10 * country_covid_cases / country_city_population)
    return 10 * country_covid_cases / country_city_population

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
    pixel.green = 0
    pixel.blue = 255 if 255 * covid_effect > 255 else int(255 * covid_effect)
    # print(pixel.red, pixel.green)
    
def convert_to_gray(image):
    for pixel in image:
        if pixel.green < 220:
            pixel.red = 255
            pixel.green = 255
            pixel.blue = 255
        else:
            pixel.red = 0
            pixel.green = 0
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
    # convert_to_gray(image)

    # image = SimpleImage.blank(VISUALIZATION_WIDTH, VISUALIZATION_HEIGHT)
    all_countries = [s.split(".")[0] for s in os.listdir(COUNTRY_POPULATION_DIRECTORY)]
    all_covid_data = [s.split(".")[0] for s in os.listdir(COUNTRY_COVID_DIRECTORY)]
    world_population = get_world_population(all_countries)
    for country in all_countries:
        country_filename = COUNTRY_POPULATION_DIRECTORY + country + ".csv"
        covid_file_name = COUNTRY_COVID_DIRECTORY + country + ".txt"
        plot_country(image, country_filename, covid_file_name, world_population)

    lst_population_density.sort()
    # print(lst_population_density)
    # print(max(lst_population_density))
    # print(min(lst_population_density))

    image.show()
    
if __name__ == '__main__':
    main()