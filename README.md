# demo_reel
***
Code examples for public viewing


#####*utah_air_tools.py*
Defines and determines which 10 mile by 10 mile grid in Utah that an input lat/long pair represent.  Built for use in Utah Hadoop User Group's air quality project.
#####*get_weather_data.py*
Using forecast.io API, extracts 20 elements of weather data from site for given lat/log and writes out to .csv file for 'n' periods.  Also calculates implied moon phase. 
#####*spark_tmr_demo.py*
Written for Pyspark job to demonstrate Google Cloud Platform's Dataproc product.  Reads in csv file of flight data (22 million rows, 17 fields) from Google storage and calculates and ranks carriers by average flight delay time for both east and west bound flights.  Determination of east or west bound is calculated within the program.
