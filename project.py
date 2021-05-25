from simpleimage import SimpleImage
import os

DEFAULT_IMAGE = 'img/blank_resized.jpg'
COUNTRY_DIRECTORY = "countries/"
VISUALIZATION_WIDTH = 1920
VISUALIZATION_HEIGHT = 1080
MIN_LONGITUDE = -180
MAX_LONGITUDE = 180
MIN_LATITUDE = -90
MAX_LATITUDE = 90

def plot_country(visualization, filename):
    with open(filename) as cities_file:
        next(cities_file) # skip the header line

        for line in cities_file:
            line = line.strip()
            parts = line.split(",")
            
            lat = float(parts[1])
            lon = float(parts[2])
            
            plot_one_city(visualization, lat, lon)

def plot_one_city(visualization, latitude, longitude):

    x = longitude_to_x(longitude)
    y = latitude_to_y(latitude)

    # if the pixel is in bounds of the window we specified through constants,
    # plot it
    if 0 < x < visualization.width and 0 < y < visualization.height:
        plot_pixel(visualization, x , y)
    
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


def plot_pixel(visualization, x, y):
    pixel = visualization.get_pixel(x, y)
    pixel.blue = 0
    pixel.green = 0

def convert_to_gray(image):
    for pixel in image:
        if pixel.red < 200 and pixel.green < 200 and pixel.blue < 200:
            pixel.red = 0
            pixel.green = 191
            pixel.blue = 255

def main():
    image = SimpleImage(DEFAULT_IMAGE)
    convert_to_gray(image)

    all_countries = [s.split(".")[0] for s in os.listdir(COUNTRY_DIRECTORY)]
    for country in all_countries:
        country_filename = COUNTRY_DIRECTORY + country + ".csv"
        plot_country(image, country_filename)

    image.show()
    
if __name__ == '__main__':
    main()