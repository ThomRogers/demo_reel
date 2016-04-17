#!/usr/bin/python
import pyspark
sc = pyspark.SparkContext()


# Load file data from Google Cloud Storage to Dataproc cluster, creating an RDD
allFlt = sc.textFile("gs://thomtect/flightinfo").cache()

# Remove header from file so we can work w data ony   
header = allFlt.take(1)[0]
dataOnly = allFlt.filter(lambda line: line != header) 

# Remove blank lines 
data_noblank = dataOnly.filter( lambda x: len(x) > 0 ).cache()
data_noblank.count()     # Should be 11425752

allFlt.unpersist()

# Create and cache 2 new RDDs.  1 for west bound flights, 1 for east bound
# West = arrival_lon <  departure_lon  (longitudes are expressed as negative)
# East = arrival_lon >  departure_lon
west = data_noblank.filter(lambda line: float(line.split(',')[10]) < float(line.split(',')[6]))
east = data_noblank.filter(lambda line: float(line.split(',')[10]) > float(line.split(',')[6]))
west.count()     # Should be 5025723
east.count()     # Should be 6400029

# Compute and cache average arrival delay by carrier for east bound flights
e_pared = east.map(lambda x : (x.split(","))).map(lambda x : (x[1],x[-1])) \
              .groupByKey() \
              .map(lambda x : (x[0], map(int, list(x[1])))) \
              .map(lambda x : (x[0],round(float(sum(x[1]))/len(x[1]),1)))
 
#Compute and cache average arrival delay by carrier for west bound flights
w_pared = west.map(lambda x : (x.split(","))).map(lambda x : (x[1],x[-1])) \
 		      .groupByKey() \
 		      .map(lambda x : (x[0], map(int, list(x[1])))) \
 		      .map(lambda x : (x[0],round(float(sum(x[1]))/len(x[1]),1)))
 		      
# Print results for east bound flights ranked from most delay to least.  
e_ranks = sorted(e_pared.take(24),key=lambda x: x[1],reverse=True)
print("Average east-bound delay mins per carrier 2002 thru 2012")
for crr in e_ranks:
    print(crr[0] + '\t' +str(crr[1]))
    
# Print results for west bound flights ranked from most delay to least
w_ranks = sorted(w_pared.take(24),key=lambda x: x[1],reverse=True)
print("Average west-bound delay mins per carrier 2002 thru 2012")
for crr in w_ranks:
    print(crr[0] + '\t' + str(crr[1]))
