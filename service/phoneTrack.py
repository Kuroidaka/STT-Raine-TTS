import phonenumbers, folium, sys, argparse, os
from phonenumbers import geocoder, timezone, carrier 
from colorama import init, Fore
from dotenv import load_dotenv

load_dotenv()


init()

def process_number(number):
    try:
        global location
        # Parse the phone number. See this as extracting relevant information from the Phone number.
        parsed_number = phonenumbers.parse(number)
        '''Display a message indicating the tracking attempt. We'll also format the parsed number to the 
        international format.'''
        print(f"{Fore.GREEN}[+] Attempting to track location of "
              f"{phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}..")
        # Get and display the time zone ID
        print(f"{Fore.GREEN}[+] Time Zone ID: {timezone.time_zones_for_number(parsed_number)}")
        # Get the geographic location of the Phone number and display it.
        location = geocoder.description_for_number(parsed_number, "en")
        if location:
            print(f"{Fore.GREEN}[+] Region: {location}")
        else:
            print(f"{Fore.RED}[-] Region: Unknown")
        '''Get the service provider (carrier) and display it if available. Some businesses and 
        organizations do not use public service providers. So you may not see the carrier in that case.'''
        if carrier.name_for_number(parsed_number, 'en'):
            print(f"{Fore.GREEN}[+] Service Provider:  {carrier.name_for_number(parsed_number, 'en')}")
        else:
            pass
    # Handle exceptions, such as invalid phone numbers or connectivity issues.
    except Exception:
        print(f"{Fore.RED}[-] Please specify a valid phone number (with country code)"
              " or check your internet connection.")
        sys.exit()
        
def get_approx_coordinates():
    from opencage.geocoder import OpenCageGeocode
    global coder, latitude, longitude
    try:
        coder = OpenCageGeocode(os.environ['OPEN_CAGE_KEY'])
        query = location
        results = coder.geocode(query)
        # Extract latitude and longitude from the geocoding results. These are the coordinates of the number's location.
        latitude = results[0]['geometry']['lat']
        longitude = results[0]['geometry']['lng']
        # Print the obtained latitude and longitude.
        print(f"[+] Latitude: {latitude}, Longitude: {longitude}")
        # Perform a reverse geocoding query to obtain an address based on coordinates.
        address = coder.reverse_geocode(latitude, longitude)
        # Check if an address was found.
        if address:
            address = address[0]['formatted']
            print(f"{Fore.LIGHTRED_EX}[+] Approximate Location is {address}")
        else:
            # If no address was found, print an error message.
            print(f"{Fore.RED}[-] No address found for the given coordinates.")
    except Exception:
        '''Handle exceptions by printing an error message and exiting the script. This would prevent the program from 
        crashing'''
        print(f"{Fore.RED}[-] Could not get the location of this number. Please specify a valid phone number or "
              "check your internet connection.")
        sys.exit()
        
# This function basically removes unwanted characters from the Phone number such as white spaces.
def clean_phone_number(phone_number):
    cleaned = ''.join(char for part in phone_number for char in part if char.isdigit() or char == '+')
    return cleaned or "unknown"


def draw_map():
    try:
        # Create a Folium map centered around the latitude and longitude of the number's coordinates.
        my_map = folium.Map(location=[latitude, longitude], zoom_start=9)
        # Add a marker to the map at the specified latitude and longitude with a popup displaying the 'location' variable.
        folium.Marker([latitude, longitude], popup=location).add_to(my_map)
        ''' Clean the phone number and use it to generate a file name with an '.html' extension
        we'll basically save each map with the number of the owner for easy identification.'''
        cleaned_phone_number = clean_phone_number(args.phone_number) # We'll see 'args' soon.
        file_name = f"{cleaned_phone_number}.html"
        # Save the map as an HTML file with the generated file name.
        my_map.save(file_name)
        # Print a message indicating where the saved HTML file can be found.
        print(f"[+] See Aerial Coverage at: {os.path.abspath(file_name)}")
    # Handle the 'NameError' exception, which can occur if the 'latitude' or 'longitude' variables are not defined.
    except NameError:
        print(f"{Fore.RED}[-] Could not get Aerial coverage for this number. Please check the number again.")
        
# Function to handle command-line arguments.
def cli_argument():
    parser = argparse.ArgumentParser(description="Get approximate location of a Phone number.")
    parser.add_argument("-p", "--phone", dest="phone_number", type=str,
                        help="Phone number to track. Please include the country code when specifying the number.",
                        required=True, nargs="+")
    argument = parser.parse_args()
    if not argument.phone_number:
        print(f"{Fore.RED}[-] Please specify the phone number to track (including country code)."
              " Use --help to see usage.")
        sys.exit()
    return argument

args = cli_argument()

# Call the process_number function and pass the phone number as a single string.
process_number("".join(args.phone_number))

get_approx_coordinates()
draw_map()
