"""
Contains functions for use in UHUG Air Quality study.

Written by Thom Rogers (thomrogers@att.net) 2014
Python 3.4

Functions included:

    utahlimit(lati, longi)
    Confirms supplied latitude and longitude are within Utah state boundaries
    added 07-28-2014  Thom Rogers

    grid10(thelat, thelong)
    Returns latitude and longitude band (10 mile width) from supplied lat
    and long
    added 07-28-2014  Thom Rogers

"""

def utahlimit(lati, longi):
    """
    Confirms supplied latitude and longitude are within Utah state boundaries

    Accounts for NE 'notch' as well
    returns a 'zero'(0) for a good lat long pair, a 'one'(1) for an out of
    bounds pair

    :param lati: float representing decimal latitude
    :param longi: float representing decimal longitude
    :return: either a 0 or 1 depending on if lat/long is good(0) or bad(1)
    """

    # For case when both a LATitude and LONGitude are supplied
    if lati != 0 and longi != 0:
        if 42.00000000 >= lati >= 37.000000000 and \
                -114.0466666667 <= longi <= -109.0466666667:
            # Check for 'notch' in NE
            if longi > -111.0466666667 and lati > 41:
                return 1
            return 0
        else:
            return 1
    # Now validate if supplied LATitude is "0", meaning only longitude band
    # must qualify
    else:
        if lati == 0:
            if -114.0466666667 <= longi <= -109.0466666667:
                return 0
            else:
                return 1
        # Now validate if supplied LONGitude is "0", meaning only LATitude band
        # must qualify
        else:
            if 42.00000000 >= lati >= 37.000000000:
                return 0
            else:
                return 1

def grid10(thelat, thelong):
    """
    Returns latitude and longitude band (10 mile width) from supplied lat/long

    2 args required:
    :param thelat: Latitude must be between 37 and 42, (or 0)
    :param thelong: Longitude must be between
                    -114.0466666667 and -109.0466666667, (or 0)

     Usage: grid10(39.140563, -111.676266)   will return 2113

    NOTE:
        To obtain latitude only, supply '0' as longitude arg:
            grid10(39.652,0)
        This will return a 99 as the longitude band
        so return would be 'xx99', where xx is the latitude band

        To obtain longitude only, supply '0' as latitude arg:
            grid10(0,-112.77731)
        This will return a 99 as the latitude band
        so return would be '99yy', where yy is the longitude band

        Where both lat AND long are out of bounds, '9999' is returned

    :rtype :a 4 digit string i.e. 'xxyy' where
            'xx' is the latitude band
            'yy' is the longitude band

    Usage:  grid10(39.140563, -111.676266)
            will return '2113'
            Latitude band = 21
            Longitude band = 13

    """

    # Latitude boundaries for Utah with approximate 10 mile width
    # Utah South to North boundary latitudes of 37 thru 42 inclusive
    # Utah height = 350 miles
    # 10 mile latitude bands = 5 deg of latitude / 35
    lats = [
        41.8571428571, 41.7142857143, 41.5714285714, 41.4285714286,
        41.2857142857, 41.1428571429, 41, 40.8571428571, 40.7142857143,
        40.5714285714, 40.4285714286, 40.2857142857, 40.1428571429, 40,
        39.8571428571, 39.7142857143, 39.5714285714, 39.4285714286,
        39.2857142857, 39.1428571429, 39, 38.8571428571, 38.7142857143,
        38.5714285714, 38.4285714286, 38.2857142857, 38.1428571429, 38,
        37.8571428571, 37.7142857143, 37.5714285714, 37.4285714286,
        37.2857142857, 37.1428571429, 37]

    # Longitude segments for Utah with approximate 10 mile width
    # Utah West to East boundary
    # longitudes of -114.0466666667 thru -109.0466666667 inclusive.
    # Utah width = 270 miles
    # 10 mile Longitude bands = 5 deg of longitude /  27
    longs = [
        -114.0466666667, -113.8614814815, -113.6762962963, -
        113.4911111111, -113.3059259260, -113.1207407408,
        -112.9355555556, -112.7503703704, -112.5651851852, -
        112.3800000000, -112.1948148148, -112.0096296297,
        -111.8244444445, -111.6392592593, -111.4540740741, -
        111.2688888889, -111.0837037037, -110.8985185186,
        -110.7133333334, -110.5281481482, -110.3429629630, -
        110.1577777778, -109.9725925926, -109.7874074074,
        -109.6022222223, -109.4170370371, -109.2318518519, -109.0466666667]

    # test supplied lat/long for within Utah boudaries
    if utahlimit(thelat, thelong) == 0:

        # Derive LATitude band
        if thelat != 0:
            if thelat >= min(lats, key=lambda x: abs(x - thelat)):
                latband = (
                    lats.index(min(lats, key=lambda x: abs(x - thelat))) + 1)
            else:
                latband = (
                    lats.index(min(lats, key=lambda x: abs(x - thelat))) + 2)
        else:
            # If supplied lat is zero, then caller only wants longitude, so
            # latband = 99
            latband = "99"

        # Derive LONGitude band
        if thelong != 0:
            if thelong >= min(longs, key=lambda x: abs(x - thelong)):
                longband = (
                    longs.index(
                        min(longs, key=lambda x: abs(x - thelong))) + 1)
            else:
                longband = (
                    longs.index(min(longs, key=lambda x: abs(x - thelong))))
        else:
            # If supplied long is zero, then caller only wants latitude, so
            # longband = 99
            longband = "99"

        # Return should always be 4 digits, so pad anything < 10 with a leading
        # zero
        if latband < 10:
            latband = '0' + str(latband)

        if longband < 10:
            longband = '0' + str(longband)

        return (str(latband) + str(longband))

    else:
        return '9999'  # Indicates a non-Utah lat/long pair
                       # 99 in either 1st 2 or last 2 position means
                       # non-Utah lat or long, respectively
