CURRENT_VERSION = "1.0"

def check_version():
    import requests
    try:
        latest = requests.get("https://pypi.org/pypi/soar_locker/json").json()
        latest_ver = latest["info"]["version"]
        if latest_ver != CURRENT_VERSION:
            print(f"[SOAR-Locker] A new version ({latest_ver}) is available. Please upgrade.")
    except:
        pass
