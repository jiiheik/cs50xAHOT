# Rainy day

## Video Demo: https:/youtu.be/NBAX4Q-p3zg

## Description:
This is a readme summary of the Rainy Day web app. The app uses Python, HTML, Flask and Jinja.
Name: Jussi Heikkonen
Location: Tampere, Finland

## Basics

The Rainy Day app aims to answer the following simple question: Will it rain today in my city and therefore will I need to take an umbrella (or other rain gear) with me for the day?

The key differentiator in the app is its simplicity.

Many weather apps provide a lot of weather forecast information. However the information overload in these apps (and in general brought by all apps we use in our daily hectic life) might lead to missing the key point, which could have an impact on your behavior or actions for the day. Here, most importantly, one needs to know if any preparations are needed for a rainy day. The app will give a simple answer to this simple question.

The app uses the OpenWeatherMap API to get the weather forecast used in the potential outcome of rain. The service provided a thorough API documentation and provided free limited use of their API, which is why this service was used.

## Usage

In index.html, the city search box is used to give a city to search for the forecast. The search box needs to have a value, otherwise the search will not be executed. Furthermore, if for some reason a blank value is searched, a redirect is made to the search page. The app needs a valid city to execute.

If a city can’t be found, the user will be informed about this on a separate page and the user can navigate back to the search page.

If a city is found, a page will display the end result, with visuals applied accordingly. End results can be rain or no rain, based on the result from the API call.

Since the city is displayed in the URL after the search, one can save the web page to the smartphone home screen in order to simply tap to know will it rain during the current day or not.

## Structure

The app consists of three different parts.

First, there are the three HTML website templates.

index.html is the city search page, which gives the user the chance to search for a city.

The weather.html result page when a successful query is made. This page uses the Jinja framework so that the page title and body text content depends on the city searched.

not_found.html page informing the user if a city was not found

Second, there are files in the static folder. Images have been used to describe the end result of the query and to give a more visual user experience. A favicon has also been added to improve visuals on the browser tab. The CSS file that defines the basic style of all the HTML pages in the templates folder.

Third and finally, there is the app.py file that defines the behavior of the app.

### Imports

The requests library was imported in order to send requests. From flask, the relevant libraries were added for Flask, URL redirects, using HTML templates and processing data requests. datetime was used in order to get the value for the current date when searching for a city rain forecast.

### Flask framework

Since the resources relevant to the app are utilized through the Flask framework, name is used in the app = flask code.

### API key

Next, the API key from the OpenWeatherMap service is set.

### Form submission logic
Then, the root-level form submission logic in index.html is described. The search function needs to use the POST request method and the search needs to include a value (city) to redirect further to the weather endpoint, otherwise the index.html is returned. City is the value provided in the search box found from index.html

### Defining the city rain forecast logic

Next, the variable part according to the city is described. The url is in the form of /weather/[city].  Weather function is defined to use the city as a parameter. rain_data refers to the get_rain_forecast(city) function, where the city defines what is requested via the API call. If a valid city is found and the request is successful, the user will be directed to the weather.html page where it will be displayed if rain is expected or not. If a valid city is not found, then the not-found.html page will be returned. If the will_rain condition is met, the weather.html page will display this, otherwise the page will show that there is no rain expected.

### Requesting data from OpenWeather API

Moving on, the weather data is pulled from the OpenWeatherMap API using the requests library.  The base URL and parameter information have been got from the API documentation. Based on the documentation and app requirements, parameters are set for the city, units (metric used) and the API key. If the GET request is successful (status code 200), it will return the JSON response. If the request is not successful, None is returned.

### Checking for rain or drizzle from the result

Finally, the app will loop through the weather forecasts in the “list” attribute of rain_data according to the JSON response. If the result in the forecast attribute “main” includes “rain” or “drizzle” for the current day, then  the weather.html page will show that it will rain that day . Both “rain” and “drizzle” are converted to lower case, since this is used in the result got from the API call. The current day is set beforehand datetime.now function and the value is returned as a string using strftime to ensure data format compatibility with the API call result. The date is checked from the dt_text attribute.

If either “Rain” or “Drizzle” appears in the current day results, the weather.html page will display that it will rain on the current day (True). Otherwise, the weather page will display that it will not rain on the current day (False).

## Further development

There are some points for further development, including:

- Having the option to choose the city from the search box (in case of duplicate city names causing inconvenience)
- Improving visuals, which are very basic for now
- To some extent, displaying more information (but not too much). This could include the temperature of the city.

## Aknowledgements

In addition to material provided for CS50, Here is a list of some relevant documentation used in the creation of the app.

https://openweathermap.org/forecast5
https://www.w3schools.com/css/css3_gradients.asp
https://www.w3schools.com/python/default.asp#gsc.tab=0
https://jinja.palletsprojects.com/en/3.1.x/templates/
https://www.pexels.com
https://favicon.io