# Find The City
This repository having code for the final project on covid 19 code in place course.
I have collected data from the files given in the ed for our exercises

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
