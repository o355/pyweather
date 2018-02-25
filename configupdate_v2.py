# PyWeather Configuration Updater
# New script is a different file name to reference the old configupdater.

import sys
import configparser
import traceback
import pip

try:
    versioninfo = open("updater//versioninfo.txt")
    versioninfo2 = versioninfo.read()
    versioninfo.close()
except:
    # Manual versioninfo check if the file couldn't be found
    print("Your versioncheck file couldn't be found. Below, please enter a number",
          "which corresponds to the version of PyWeather you're updating from.",
          "[0] 0.5.2.1 beta and earlier",
          "[1] 0.6 beta or 0.6.0.1 beta",
          "[2] 0.6.1 beta or 0.6.1 beta-https",
          "[3] 0.6.2 beta",
          "[4] 0.6.3 beta",
          "[4.01] 0.6.4 beta RC0", sep="\n")
    versionselect = input("Input here: ").lower()
    if versionselect == "0":
        print("You'll need to completely reinstall PyWeather due to the way the new config system works.",
              "Instructions are available on PyWeather's GitHub wiki.", sep="\n")
        input()
        sys.exit()
    elif versionselect == "1":
        print("Updating PyWeather using version identifier: 0.6 beta")
        versioninfo2 = "0.6 beta"
    elif versionselect == "2":
        print("Updating PyWeather using version identifier: 0.6.1 beta")
        versioninfo2 = "0.6.1 beta"
    elif versioninfo2 == "3":
        print("Updating PyWeather using version identifier: 0.6.2 beta")
        versioninfo2 = "0.6.2 beta"
    elif versioninfo2 == "4":
        print("Updating PyWeather using version identifier: 0.6.3 beta")
    elif versioninfo2 == "5":
        print("Updating PyWeather using version identifier: 0.6.4 beta-RC0")

# Define config loader
config = configparser.ConfigParser()
config.read("storage//config.ini")

# Geopy function
def geopycheck():
    print("In version 0.6.2 beta and above, your geocoder scheme needs to get set, based on your OS.",
          "PyWeather can automatically do this now, or you can manually define your scheme.",
          "Type in 'automaticsetup' for the automatic setup, and 'manualsetup' for manual setup",
          "in the prompt below.", sep="\n")
    setupmethod = input("Input here: ").lower()
    if setupmethod == "manualsetup":
        print("Geopy's Google geocoder can work in HTTPS-enabled mode on 95% of platforms,",
              "but has a tendancy to fail on OS X, or other platforms. In the prompt below,",
              "enter 'https' for geopy to work in https mode, or 'http' for http mode.",
              "Please note: Your settings will not be validated!", sep="\n")
        geopymode = input("Input here: ").lower()
        if geopymode == "https":
            config['GEOCODER']['scheme'] = 'https'
            print("Changes saved.")
        else:
            config['GEOCODER']['scheme'] = 'https'
            if geopymode == "http":
                print("Changes saved.")
            else:
                print("Couldn't understand your input. Defaulting to 'http'.")
    else:
        if setupmethod == "automaticsetup":
            print("Starting automatic setup.")
        else:
            print("Couldn't understand your input. Defaulting to automatic setup.")

        import geopy
        from geopy import GoogleV3
        geocoder = GoogleV3(scheme='https')
        # Warm-up geocode
        try:
            geocoder.geocode("123 5th Avenue, New York, NY")
        except:
            isthisisheresopythondoesntyellatme = True
        try:
            geocoder.geocode("123 5th Avenue, New York, NY")
            print("The geocoder can operate with HTTPS enabled on your OS. Saving these changes...")
            config['GEOCODER']['scheme'] = 'https'
            print("Changes saved.")
        except geopy.exc.GeocoderServiceError:
            print("Geopy probably can't run without HTTPS (or your internet went down). Trying HTTP as the scheme...")
            geocoder = GoogleV3(scheme='http')
            try:
                geocoder.geocode("123 5th Avenue, New York, NY")
                print("The geocoder can operate, but without HTTPS enabled on your OS. Saving these changes...")
                config['GEOCODER']['scheme'] = 'http'
                print("Changes saved.")
            except geopy.exc.GeocoderServiceError:
                print("You probably don't have an internet connection, as HTTPS and HTTP validation both failed.",
                      "Defaulting to HTTP as the geopy scheme...", sep="\n")
                config['GEOCODER']['scheme'] = 'http'
                print("Changes saved.")

# New function to install a library
def newlibinstaller(library):
    # Check for the library we're installing
    if library == "halo":
        librarytoinstall = "halo"
    elif library == "click":
        librarytoinstall = "click"

    else:
        # Return if the library we're installing isn't defined here.
        return

    # Check if a library is installed dependent on a plain 'ol except

    if librarytoinstall == "halo":
        try:
            import halo
            haloinstalled = True
        except:
            haloinstalled = False
    elif librarytoinstall == "click":
        try:
            import click
            clickinstalled = True
        except:
            clickinstalled = False

    # Now that we've checked for installed libraries, we now print dialogue and return
    # if no new libraries are needed
    if haloinstalled is True:
        print("For PyWeather 0.6.3 beta and above, a new library called 'halo' is required for PyWeather to operate.",
              "This library controls the new loaders that are present in PyWeather. The good news is that you already have",
              "halo installed. Skipping automatic install of halo.", sep="\n")
        return
    elif clickinstalled is True:
        print("For PyWeather 0.6.4 beta and above, a new library called 'click' is required for PyWeather to operate.",
              "This library presently controls the progress bar for the new updater. The good news is that you already have",
              "click installed. Skipping automatic install of click.", sep="\n")
        return

    # If libraries are not installed, show dialogues for specific libraries and ask for permission
    if haloinstalled is False:
        print("For PyWeather 0.6.3 beta and above, a new library called 'halo' is required for PyWeather to operate.",
              "This library controls the new loaders that are present in PyWeather. Unfortunately, halo is not installed.",
              "Would you like to perform an automatic install of halo? Yes or No.", sep='\n')
        installhalo_input = input("Input here: ").lower()
        if installhalo_input == "yes":
            installlibrary = "halo"
        elif installhalo_input == "no":
            print("To use the latest version of PyWeather, you'll need to install halo in a command line.",
                  "The command to do this is `pip3 install halo`, and it should work on most platforms.", "", sep="\n")
            return
        else:
            print("Your input could not be understood. As a precaution the automatic install will not be carried out.",
                  "To use the latest version of PyWeather, you'll need to install halo in a command line.",
                  "The command to do this is `pip3 install halo`, and it should work on most platforms.", "", sep="\n")
            return
    elif clickinstalled is False:
        print("For PyWeather 0.6.4 beta and above, a new library called 'click' is required for PyWeather to operate.",
              "This library presently controls the progress bar for the new updater. Unfortunately, click is not installed.",
              "Would you like to perform an automatic install of halo? Yes or No.", sep="\n")
        installclick_input = input("Input here: ").lower()
        if installclick_input == "yes":
            installlibrary = "click"
        elif installclick_input == "no":
            print("To use the latest version of PyWeather, you'll need to install click in a command line.",
                  "The command to do this is `pip3 install click`, and it should work on most platforms.", "", sep="\n")
            return
        else:
            print("Your input could not be understood. As a precaution the automatic install will not be carried out.",
                  "To use the latest version of PyWeather, you'll need to install click in a command line.",
                  "The command to do this is `pip3 install click`, and it should work on most platforms.", "", sep="\n")
            return

    # Now begin installing libraries
    print("Now installing %s using pip's built-in installer." % installlibrary)
    pip.main(['install', '%s' % installlibrary])
    print("Now checking if %s was properly installed..." % installlibrary)

    # Separate checks for separate libraries
    if installlibrary == "halo":
        try:
            import halo
            print("Halo has been successfully installed!")
            return
        except ImportError:
            print("When attempting an automatic install, Halo failed to install properly.",
                  "To use the latest version of PyWeather, you'll need to manually use a command line",
                  "and manually install halo. The command to do this is `pip3 install halo` on most",
                  "platforms. If an error occurred use a search engine to try and fix the error.", sep="\n")
            # Instead of using "use Google" or "use Bing", make things vague so the user isn't potentially offended
            # by their search engine selection
            return
    elif installlibrary == "click":
        try:
            import click
            print("Click has been successfully installed!")
            return
        except ImportError:
            print("When attempting an automatic install, Click failed to install properly.",
                  "To use the latest version of PyWeather, you'll need to manually use a command line",
                  "and manually install click. The command to do this is `pip3 install click` on most",
                  "platforms. If an error occurred use a search engine to try and fix the error.", sep="\n")
            return

# Define build numbers for different versions of PyWeather. Later in time I'll switch to a dictionary and for loop
# to cover this part of the code

if versioninfo2 == "0.6 beta" or versioninfo2 == "0.6.0.1 beta":
    buildnumber = 60
elif versioninfo2 == "0.6.1 beta":
    buildnumber = 61
elif versioninfo2 == "0.6.2 beta":
    buildnumber = 62
elif versioninfo2 == "0.6.3 beta":
    buildnumber = 63
elif versioninfo2 == "0.6.4 beta":
    buildnumber = 63.01

# If we're up-to-date, stop the script
if buildnumber == 63.01:
    print("Your copy of PyWeather is up-to-date. Therefore, there is no need to run this script.",
          "Press enter to exit.", sep="\n")
    input()
    sys.exit()

# The first of the main loops. Make new sections in this loop.

if buildnumber <= 62:
    try:
        config.add_section("GEOCODER API")
    except configparser.DuplicateSectionError:
        print("Failed to add the geocoder API section.")

    try:
        config.add_section("FAVORITE LOCATIONS")
    except configparser.DuplicateSectionError:
        print("Failed to add the favorite locations section. Does it exist?")

    try:
        config.add_section("FIRSTINPUT")
    except configparser.DuplicateSectionError:
        print("Failed to add the firstinput section. Does it exist?")

    try:
        config.add_section("HURRICANE")
    except configparser.DuplicateSectionError:
        print("Failed to add the hurricane section. Does it exist?")

if buildnumber <= 61:
    try:
        config.add_section("PREFETCH")
    except configparser.DuplicateSectionError:
        print("Failed to add the prefetch section. Does it exist?")

if buildnumber <= 60:
    try:
        config.add_section("CACHE")
    except configparser.DuplicateSectionError:
        print("Failed to add the cache section. Does it exist?")

    try:
        config.add_section("RADAR GUI")
    except configparser.DuplicateSectionError:
        print("Failed to add the radar GUI section. Does it exist?")

    try:
        config.add_section("GEOCODER")
    except configparser.DuplicateSectionError:
        print("Failed to add the geocoder section. Does it exist?")

# Second loop. Add new configuration options.


if buildnumber <= 63:
    config['FAVORITE LOCATIONS']['favloc1_data'] = "None"
    config['FAVORITE LOCATIONS']['favloc2_data'] = "None"
    config['FAVORITE LOCATIONS']['favloc3_data'] = "None"
    config['FAVORITE LOCATIONS']['favloc4_data'] = "None"
    config['FAVORITE LOCATIONS']['favloc5_data'] = "None"
    config['FIRSTINPUT']['allow_airportqueries'] = "None"

if buildnumber <= 62:
    config['FIRSTINPUT']['geoipservice_enabled'] = 'False'
    config['FIRSTINPUT']['allow_pwsqueries'] = 'True'
    config['HURRICANE']['enablenearestcity'] = 'False'
    config['HURRICANE']['enablenearestcity_forecast'] = 'False'
    config['HURRICANE']['api_username'] = 'pyweather_proj'
    config['HURRICANE']['nearestcitysize'] = 'medium'
    config['FAVORITE LOCATIONS']['enabled'] = 'True'
    config['FAVORITE LOCATIONS']['favloc1'] = 'None'
    config['FAVORITE LOCATIONS']['favloc2'] = 'None'
    config['FAVORITE LOCATIONS']['favloc3'] = 'None'
    config['FAVORITE LOCATIONS']['favloc4'] = 'None'
    config['FAVORITE LOCATIONS']['favloc5'] = 'None'
    config['GEOCODER API']['customkey_enabled'] = 'False'
    config['GEOCODER API']['customkey'] = 'None'
    config['SUMMARY']['showyesterdayonsummary'] = 'False'
    config['PREFETCH']['yesterdaydata_atboot'] = 'False'
    config['CACHE']['yesterday_cachedtime'] = '720'
    config['UI']['extratools_enabled'] = 'False'

if buildnumber <= 61:
    config['CACHE']['tide_cachedtime'] = '480'
    config['SUMMARY']['showtideonsummary'] = 'False'
    config['CACHE']['threedayhourly_cachedtime'] = '60'
    config['CACHE']['tendayhourly_cachedtime'] = '60'
    config['PREFETCH']['10dayfetch_atboot'] = 'False'
    config['PREFETCH']['hurricanedata_atboot'] = 'False'
    config['CACHE']['hurricane_cachedtime'] = '180'

if buildnumber <= 60:
    config['CACHE']['alerts_cachedtime'] = '5'
    config['CACHE']['current_cachedtime'] = '10'
    config['CACHE']['threedayhourly_cachedtime'] = '60'
    config['CACHE']['tendayhourly_cachedtime'] = '60'
    config['CACHE']['forecast_cachedtime'] = '60'
    config['CACHE']['almanac_cachedtime'] = '240'
    config['CACHE']['sundata_cachedtime'] = '480'
    config['RADAR GUI']['radar_imagesize'] = 'normal'
    config['RADAR GUI']['bypassconfirmation'] = 'False'
    config['CACHE']['enabled'] = 'True'


# Print out new config changes, removals will come after this

print("New configuration options have been added in the version of PyWeather you're upgrading to.")

if buildnumber <= 63:
    print("FAVORITE LOCATIONS/favloc1_data - Defaults to None",
          "Sets extra data for favorite location 1.", sep="\n")
    print("FAVORITE LOCATIONS/favloc2_data - Defaults to None",
          "Sets extra data for favorite location 2.", sep="\n")
    print("FAVORITE LOCATIONS/favloc3_data - Defaults to None",
          "Sets extra data for favorite location 3.", sep="\n")
    print("FAVORITE LOCATIONS/favloc4_data - Defaults to None",
          "Sets extra data for favorite location 4.", sep="\n")
    print("FAVORITE LOCATIONS/favloc5_data - Defaults to None",
          "Sets extra data for favorite location 5.", sep="\n")
    print("FIRSTINPUT/allow_airportqueries - Defaults to True",
          "Sets if PyWeather will allow airport queries.", sep="\n")
if buildnumber <= 62:
    print("FIRSTINPUT/geoipservice_enabled - Defaults to False",
          "Sets if the service for current location queries is enabled.", sep="\n")
    print("FIRSTINPUT/allow_pwsqueries - Defaults to True",
          "Sets if PyWeather will allow PWS queries.", sep="\n")
    print("HURRICANE/enablenearestcity - Defaults to False",
          "Sets if the nearest city feature for hurricanes is enabled.", sep="\n")
    print("HURRICANE/enablenearestcity_forecast - Defaults to False",
          "Sets if the nearest city feature for hurricane forecasts is enabled.", sep="\n")
    print("HURRICANE/api_username - Defaults to 'pyweather_proj'")