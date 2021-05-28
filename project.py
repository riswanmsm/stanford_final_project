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
import csv
import json
from simpleimage import SimpleImage
import os
import random

DEFAULT_IMAGE = 'img/green_world.jpg'
COUNTRY_POPULATION_DIRECTORY = "countries/population/"
COUNTRY_COVID_DIRECTORY = "countries/covid/"
VISUALIZATION_WIDTH = 1019
VISUALIZATION_HEIGHT = 471
MIN_LONGITUDE = -180
MAX_LONGITUDE = 180
MIN_LATITUDE = -90
MAX_LATITUDE = 90
WRONG_ATTEMPT_MARKS = 5
MAXIMUM_SCORE = 100

def plot_country(visualization, filename, covid_file_name, world_population, country, dic_covid_effect):
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
    cities = plot_data['cities']

    covid_effect = get_covid_effect(country_covid_case, country_city_population)
    for i in range(len(lat)):
        population_density = get_population_density(population[i], world_population)  
        # if population_density > 0:
            # print(population_density, covid_effect)
        plot_one_city(visualization, lat[i], lon[i], population_density, covid_effect)
        key = country + '_' + cities[i] + '_' + str(i)
        # if key in dic_covid_effect:
        #     print(key)
        dic_covid_effect[key] = {'country_name': country, 'city_name': cities[i], 'population_density': population_density, 'covid_effect': covid_effect}
        # with open(r'innovators.csv', 'a') as file:
        #     writer = csv.writer(file) 
        #     writer.writerow([country, cities[i], population[i], population_density, covid_effect])
    
                

def get_plot_data(filename):
    lat = []
    lon = []
    population = []
    country_city_population = 0
    cities = []
    with open(filename) as cities_file:
        next(cities_file) # skip the header line
        for line in cities_file:
            line = line.strip()
            parts = line.split(",")
            lat.append(float(parts[1]))
            lon.append(float(parts[2]))
            cities.append(parts[0])
            if parts[3]:
                population.append(float(parts[3]))
                country_city_population += float(parts[3])
            else:
                population.append(0.0)
    plot_data = {'lat': lat, 'lon': lon, 'population': population, 'country_city_population': country_city_population, 'cities': cities}
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
    return 5000 * city_population / world_population

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
    pixel.green = 255 if 255 * covid_effect > 255 else int(255 * covid_effect)
    pixel.red = 255 if 255 * population_density > 255 else int(255 * population_density)
    # if population_density > 15 and covid_effect <= 0.6:
    #     pixel.red = 255
    #     pixel.green = 0
    # elif population_density > 10 and covid_effect > 0.6:
    #     pixel.red = 255
    #     pixel.green = 255
    # elif population_density <= 15 and covid_effect > 5:
    #     pixel.red = 0
    #     pixel.green = 255
    # elif population_density < 0.001 and covid_effect < 0.001:
    #     pixel.red = 0
    #     pixel.green = 0

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

def show_main_instruction():
    print('\n\n\n')
    print('\t-----------------------------------------------------------------------------------------------')
    print('\t|    You are going to view a plotted world map                                                |')
    print('\t|                                                                                             |')
    print('\t|    * \033[1mYellow\033[0m pixels on the map indicate \033[1mHIGH\033[0m population density and \033[1mHIGH\033[0m covid-19 effect     |')
    print('\t|    * \033[1mRed\033[0m pixels on the map indicate \033[1mHIGH\033[0m population density and \033[1mLOW\033[0m covid-19 effect         |')
    print('\t|    * \033[1mGreen\033[0m pixels on the map indicate \033[1mLOW\033[0m population density and \033[1mHIGH\033[0m covid-19 effect       |')
    print('\t|    * \033[1mBlack\033[0m pixels on the map indicate \033[1mLOW\033[0m population density and \033[1mLOW\033[0m covid-19 effect        |')
    print('\t|                                                                                             |')
    print('\t|    * Once you view the map you are going to participate in a quiz in the console.           |')
    print('\t|                                                                                             |')
    print('\t|    **** Questions are relevant to the map so look the map carefully ****                    |')
    print('\t-----------------------------------------------------------------------------------------------')
    input('\n\tPress Enter to view the plotted map: ')

def country_quiz_instruction():
    print('-----------------------------------------------------------------------------------------------')
    print('| You are going to given the first letter of the country which is the answer for the question |')
    print('| You need to fill the blanks by entering letters one by one until you find all the letters   |')
    print('| If you find the letter correctly you will be appreciated otherwise you will get a chance    |')
    print('-----------------------------------------------------------------------------------------------')

def show_country_quiz():
    # show country quiz instruction
    input('Press Enter to view the quiz instruction: ')
    country_quiz_instruction()
    user_interest = input('Enter 1 to continue or any other key to quit: ')
    if user_interest != '1':
        return
    
    # take user input
    # check user input and show the result
    input('Country Quiz: ')

def get_quiz_data(dic_covid_effect, random_quiz):
    lst_countries = []
    if random_quiz == 'hh':
        for key in dic_covid_effect:
            # create list with cities having high population density and high covid effect
            if dic_covid_effect[key]['population_density'] > 10 and dic_covid_effect[key]['covid_effect'] > 0.6:
                lst_countries.append(dic_covid_effect[key])
    if random_quiz == 'hl':
        for key in dic_covid_effect:
            # create list with cities having high population density and low covid effect
            if dic_covid_effect[key]['population_density'] > 15 and dic_covid_effect[key]['covid_effect'] <= 0.6:
                lst_countries.append(dic_covid_effect[key])
    if random_quiz == 'lh':
        for key in dic_covid_effect:
            # create list with cities having low population density and high covid effect
            if dic_covid_effect[key]['population_density'] <= 15 and dic_covid_effect[key]['covid_effect'] > 5:
                lst_countries.append(dic_covid_effect[key])
    if random_quiz == 'll':
        for key in dic_covid_effect:
            # create list with cities having low population density and low covid effect
            if dic_covid_effect[key]['population_density'] < 0.001 and dic_covid_effect[key]['covid_effect'] < 0.001:
                lst_countries.append(dic_covid_effect[key])
    
    return lst_countries

def show_question_instruction(random_quiz):
    if random_quiz == 'hh':
        print('\t\t\tOne of the city having high population density and high covid-19 effect')
        print('\t\t\tIt was shown in yellow or orange color pixel in the plotted map')
    if random_quiz == 'hl':
        print('\t\t\tOne of the city having high population density and low covid-19 effect')
        print('\t\t\tIt was shown in red color pixel in the plotted map')
    if random_quiz == 'lh':
        print('\t\t\tOne of the city having low population density and high covid-19 effect')
        print('\t\t\tIt was shown in green color pixel in the plotted map')
    if random_quiz == 'll':
        print('\t\t\tOne of the city having low population density and low covid-19 effect')
        print('\t\t\tIt was shown in black color pixel in the plotted map')

def appreciate_user():
    lst_appreciatios = [
        'Well Done Mate !',
        'Congratulations',
        'Best Kick',
        'WoooooW',
        'You nailed it!',
        'Very Good'
    ]
    print(random.choice(lst_appreciatios))

def show_final_marks(wrong_attempt):
    score = MAXIMUM_SCORE - wrong_attempt * WRONG_ATTEMPT_MARKS
    score = score if score > 0 else 0
    print('\n\t\tCongratulations You Have Successfully Completed The Game!')
    print('\n\t\tThe Score You Gained Is:', score, '/', '100')

def show_question(country_name, city_name):
    answer_with_blank = list(city_name)
    found_characters = []
    for i in range(1, len(answer_with_blank)):
        if answer_with_blank[i] != ' ':
            answer_with_blank[i] = '_'
    # print(city_name)
    # print(answer_with_blank)
    wrong_attempt = 0
    city_name_lower = city_name.lower()
    print('\n\t\tThe first letter of the city is given below and the remainig letters are showing as _')
    while True:
        print('\n\t\tName of the city with blanks:\033[1m', ''.join(answer_with_blank), '\033[0m')
        user_answer = input('\n\t\tEnter a character to fill a balnk in the city name: ')
        user_answer_lower = user_answer.lower()
        if len(user_answer) != 1:
            print('\n\t\tPlease enter one character at a time')  
        elif user_answer_lower in found_characters:
            print('\n\t\tThe letter you entered is already found')
        elif user_answer_lower in city_name_lower[1:]:
            for i in range(1, len(city_name_lower)):
                if city_name_lower[i] == user_answer_lower:
                    answer_with_blank[i] = city_name[i]
            found_characters += user_answer_lower
            appreciate_user()
        else:
            wrong_attempt += 1
            print('\n\t\tThe letter you entered is wrong and your wrong attempts are :', wrong_attempt)
            print('\t\tYou are going to loose', WRONG_ATTEMPT_MARKS, 'marks for each wrong attempts')
            print('\t\tClue ******** \n\t\t\tThe country of the city is:\033[1m', country_name, '\033[0m')

        if ''.join(answer_with_blank) == city_name:
            break
    show_final_marks(wrong_attempt)


def create_question(quiz_data, random_quiz):
    print('\n\n\n\n\t\t\033[1m =======================================  Quiz   ======================================= \033[0m\n')
    show_question_instruction(random_quiz)
    # print('\n')
    answer = random.choice(quiz_data)
    city_name = answer['city_name']
    country_name = answer['country_name']
    # print(city_name)
    # print(country_name)
    show_question(country_name, city_name)
    print('\n\t\t',city_name, 'is a city situated in', country_name)
    print('\n\t\t',city_name, 'is a city situated in', country_name)
    show_question_instruction(random_quiz)

def create_quiz(dic_covid_effect):
    input('\n\n\tPlease press enter to participate in the quiz: ')
    tpl_choices = ('hh', 'hl', 'lh', 'll')
    random_quiz = random.choice(tpl_choices)
    quiz_data = get_quiz_data(dic_covid_effect, random_quiz)
    create_question(quiz_data, random_quiz)
    
def main():
    # show_main_instruction()
    image = SimpleImage(DEFAULT_IMAGE)

    all_countries = [s.split(".")[0] for s in os.listdir(COUNTRY_POPULATION_DIRECTORY)]
    world_population = get_world_population(all_countries)
    # with open('innovators.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(["Country", "City", "Population", "Population Density", "Covid Effect"])
    dic_covid_effect = {}
    for country in all_countries:
        country_filename = COUNTRY_POPULATION_DIRECTORY + country + ".csv"
        covid_file_name = COUNTRY_COVID_DIRECTORY + country + ".txt"
        plot_country(image, country_filename, covid_file_name, world_population, country, dic_covid_effect)
    
    # print(dic_covid_effect)
    # with open("covid_dic.json", "w") as outfile: 
    #     json.dump(dic_covid_effect, outfile)
    
    show_main_instruction()
    image.show()
    create_quiz(dic_covid_effect)
    # show the country quiz
    # show_country_quiz()
    
if __name__ == '__main__':
    main()