# Alex Pacholuk 
# Python Final Proj
# 12.4.20

# This program is designed to be an interactive weather forecast.
# Based on user input, this program will look at real weather
# forecasts from weather.org and ouput a visual representation 
# of the data in the deisred manner.

# In order to look up location for weather without only puting lat 
# and lng points, I needed to use a geocoding feature from another
# service before using the weather.gov API.  For this I went with
# Google Maps API Geocoding service.


# Import stuff
import requests # for using API
import json
from matplotlib import pyplot as plt # for using graphs
from credentials import gmaps_key # for google geocoding



# Main Function
def main():

    runAgain = 'Y'
    # Welcome greeting
    print('\nWelcome! Let\'s search for the weather...')

    # While loop controlling entire program
    while runAgain.upper() == 'Y':

        # Weather search options
        print('\nHow would you like to search for weather forecasts?')
        print('\n1: Address Search')
        print('2: Latitude, Longitude Search')
        searchBy = input('\n> ')

        # if input error...
        if searchBy != '1' and searchBy != '2':

            # Print error message
            print('\nInput error. Please enter a valid search type.')

        # Search by address...
        elif searchBy == '1':

            # Function calls
            latLngPoints = addressSearch()
            forecastUrl = latLngSearch2(latLngPoints)
            graphData = forecast(forecastUrl)
            graphStuff(graphData)
            
        # Search by Lat/Long...
        elif searchBy == '2':

            # Function calls
            forecastUrl = latLngSearch()
            graphData = forecast(forecastUrl)
            graphStuff(graphData)

        # Run again?
        runAgain = input('\nRun again? y/n\n\n> ')

    # Bye-bye message
    print('\nEnding program. See you next time!\n')



#-----------------------Functions----------------------




# Search by address lookup...
def addressSearch():

    # Prints header purely for cosmetics
    print('\n-------------------------------\n')

    # Confirmation
    print('\nExcellent! Searching by address...')

    # Gather Address Info from user
    addressInput = input('\nPlease enter street address: \n\n> ')
    cityInput = input('\nPlease enter city: \n\n> ')
    stateInput = input('\nPlease enter state abbreviation: \n\n> ')

    # Create full address
    fullAddress = (addressInput.title() + ',' + cityInput.title() + ',' + stateInput.upper())

    # get url friendly version of addressInput that replaces spaces with '+'
    address = fullAddress.replace(' ', '+')

    # create full google geocode url
    googleGeocodeUrl1 = 'https://maps.googleapis.com/maps/api/geocode/json?address=' # appended with outputFormat?parameters
    googleGeocodeUrl = (googleGeocodeUrl1 + str(address) + '&key=' + gmaps_key)

    # get request
    r = requests.get(googleGeocodeUrl)
    print('\nThe status code is {}'.format(r.status_code))

    # the magic sauce (looks for the formatted address and lat/lng points)
    response = r.json()["results"][0]
    formattedAddress = response["formatted_address"]
    latitude = response["geometry"]["location"]["lat"]
    longitude = response["geometry"]["location"]["lng"]

    # print stuff
    print('\n----------Results-----------')
    print('\nAddress: ' + formattedAddress)
    print('\nLatitude: ' + str(latitude))
    print('\nLongitude: ' + str(longitude))


    # return list for use in other module
    return[latitude, longitude]




# Search by lat/lng
def latLngSearch():

    # Prints header purely for cosmetics
    print('\n-------------------------------\n')

    # Confirmation
    print('\nExcellent! Searching by latitude and longitude...')

    # Gather lat/lng from user
    lat = input('\nEnter latitude coordinate: \n\n> ')
    lng = input('\nEnter longitude coordinate: \n\n> ')

    # create full 'weather.gov' url
    weatherUrl1 = 'https://api.weather.gov/points/' # appended with outputFormat?parameters
    weatherUrl2 = (weatherUrl1 + lat + ',' + lng)

    # get request
    r = requests.get(weatherUrl2)
    print('\nThe status code is {}'.format(r.status_code))

    # gets another url for then seeing hourly forecast data
    response = r.json()["properties"]
    forecastUrl = response["forecastHourly"]

    # return url for hourly forecast
    return forecastUrl






# Get a forecast url from returned lat/lng points from google maps address search
def latLngSearch2(latLngPoints):
    lat = latLngPoints[0]
    lng = latLngPoints[1]

    # create full weather.gov url
    weatherUrl1 = 'https://api.weather.gov/points/' # appended with outputFormat?parameters
    weatherUrl2 = (weatherUrl1 + str(lat) + ',' + str(lng))

    # get request
    r = requests.get(weatherUrl2)
    print('\nThe status code is {}'.format(r.status_code))

    # gets another url for then seeing hourly forecast data
    response = r.json()["properties"]
    forecastUrl = response["forecastHourly"]

    # return url for hourly forecast
    return forecastUrl






# Retrieves Hourly Forecasts
def forecast(forecastUrl):

    # get request
    r = requests.get(forecastUrl)
    print('\nThe status code is {}'.format(r.status_code))

    # looks at hourly forecast data
    response = r.json()["properties"]["periods"]

    # Prints header purely for cosmetics
    print('\n-------------------------------\n')

    # Print?
    printStuff = input('\nWould you like to print forecasts to terminal? y/n\n\n> ')

    # Empty List
    times = []
    temps = []
    forecasts = []

    # For loop to read data
    for data in response:

        # Gather hourly weather data
        time = data["startTime"]
        date = time[:10]
        timeFrame = time[11:]
        temp = data["temperature"]
        tempUnit = data["temperatureUnit"]
        shortForecast = data["shortForecast"]
        
        # Print hourly weather data
        if printStuff.lower() == 'y' or printStuff.lower() == 'yes':
            print('\nDate: ' + str(date))
            print('Timeframe: ' + str(timeFrame))
            print('Temp: ' + str(temp) + str(tempUnit))
            print('Short Forecast: ' + str(shortForecast))

        times.append(time)
        temps.append(temp)
        forecasts.append(shortForecast)

    # Return 2 lists - time frames and temperatures
    return times, temps, forecasts




# Graph the data
def graphStuff(graphData):

    # Extract 1/2 of Graph Data
    times = graphData[0]
    temps = graphData[1]
    forecasts = graphData[2]
    halfIndex = len(times) / 2
    
    # Make Graph more concise
    smallerTimes = times[:int(halfIndex)]
    smallerTemps = temps[:int(halfIndex)]
    smallerForecasts = forecasts[:int(halfIndex)]

    # Get every other item
    smallerTimesHalved = smallerTimes[::2]
    smallerTempsHalved = smallerTemps[::2]
    smallerForecastsHalved = smallerForecasts[::2]

    datesTimes = []

    # For loop to extract data for better formatting
    for data in smallerTimesHalved:

        # Grab just the date and store it in var
        date = data[:10]

        # Reformat Date as month-day
        month = date[5:8]
        day = date[8:]
        newDate = str(month) + str(day) 

        # Get index
        index = smallerTimesHalved.index(data)

        # Prepare format for graph ticks
        timeFrame = data[11:16]
        dateTime = (timeFrame + ' | ' + newDate + ' | ' + smallerForecastsHalved[index])
        datesTimes.append(dateTime)

    # Data color input for graph
    graphColor = input('\nWhat\'s your favorite color? (stick to basic colors please)\n\n> ')

    # Plot Data
    fig = plt.figure(dpi=128, figsize=(12, 7.5))
    plt.scatter(datesTimes, smallerTempsHalved, c=graphColor, edgecolors='none', alpha=0.5)

    # Format Plot
    plt.title('Weather Forecast', fontsize=24)
    plt.xlabel('Dates/Times/Forecasts', fontsize=16)
    fig.autofmt_xdate()
    plt.ylabel('Temperatures (F)', fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=6)



    # Save, display or both?a
    temp = 0

    while temp == 0:

        graphInstructions = input('\nWould you like to display, save, or display & save your forecast? \n\n1: save\n2: display\n3: both\n\n> ')

        # Display Graph
        if graphInstructions == '2':
            plt.show()
            temp +=1

        # Save Graph
        elif graphInstructions == '1':
            figName = input('\nWhat would you like to title your save file (ie. Forecast Graph)? \n\n> ')
            print('\nSaving File as ' + str(figName) + '.png\nMake sure to check your local directory for it, otherwise look in users.')
            plt.savefig(str(figName) + '.png')
            temp +=1

        # Save & Display Graph
        elif graphInstructions == '3':
            figName = input('\nWhat would you like to title your save file (ie. Forecast Graph)? \n\n> ')
            print('\nSaving File as ' + str(figName) + '.png\nMake sure to check your local directory for it, otherwise look in users.')
            plt.savefig(str(figName) + '.png')
            plt.show()
            temp +=1

        # Input error
        else: 
            print('\nInput Error.  Please only enter save, display, or both.\n')

main()