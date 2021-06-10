# Importing Libraries
import os 
from offline_utilities import preprocessLines, plagarismCheck, checkPlagarismOffline, showPlagarismOffline
from online_utilities import searchGoogle, getSearchLines, showPlagarismOnline

# Offline Plagarism 

# Path to data folder
path_to_data = os.path.join(os.getcwd(),'data/')
path_to_originals = os.path.join(path_to_data,'reference texts/') # Path to refernce texts

reference_path = path_to_data + 'huntrprint.txt' # Path to refernce file i.e raw file 

reference = preprocessLines(reference_path) # Pre processing lines from .txt file 

plagarised_object = plagarismCheck(reference, path_to_originals) # Create a plagarism object, which contains plagarised lines and corresponding ratios 

display_object_offline = checkPlagarismOffline(reference, plagarised_object, isjson = False) # display object with color coded lines 

showPlagarismOffline(display_object_offline) # Display offline plagarism file 

# Online Plagarism 

search_lines = getSearchLines(reference) # Pre processlines for online search

display_object_online = searchGoogle(search_lines) # Search Lines on google 

showPlagarismOnline(search_lines,display_object_online) # Display online plagarism file