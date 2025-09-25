import requests
# the logic used in here is the same i used in my own script licensing system i made in lua it just sends a reqeust and fetches the ip and timezone for some form of geolocation check
def get_ip_address():
  
    try:
        
        ip_address = requests.get('https://api.ipify.org').text
        return ip_address
    except requests.RequestException as e:
        print(f"Error fetching IP address: {e}")
        return None

def get_timezone_from_ip(ip_address):
   
    try:
        if not ip_address:
            print("Invalid IP address.")
            return None
        
        
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        if response.status_code == 200:
            data = response.json()
            timezone = data.get("timezone")  
            if timezone:
                return timezone
            else:
                print("Timezone not found in the response.")
                return None
        else:
            print(f"Failed to fetch timezone information. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error fetching timezone: {e}")
        return None
