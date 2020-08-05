import requests
import time

OMAHAPROX = "omahaprox"


def history(ossmall):
    return requests.get(
        f"https://{OMAHAPROX}y.appspot.com/history.json?channel=stable&os={ossmall}"
    ).json()

def get_for_os(which_version, ossmall, oslarge):
    print(f"Downloading {which_version} version data for {ossmall}...")
    time.sleep(2)
    historyjson = history(ossmall)
    version = historyjson[which_version]['version']
    major_version = version.split(".")[0]
    
    existed_positions = requests.get((
        "https://www.googleapis.com/storage/v1/b/chromium-browser-snapshots/o?delimiter=/&prefix={oslarge}/"
        "&fields=items(kind,mediaLink,metadata,name,size,updated),kind,prefixes,nextPageToken"
    )).json()
    
    base_position = requests.get(
        "https://{}y.appspot.com/deps.json?version={}".format(OMAHAPROX, version)
    ).json()['chromium_base_position']                                       

    download_urls_available = requests.get((
        "https://www.googleapis.com/storage/v1/b/chromium-browser-snapshots/o?"
        "delimiter=/&prefix={}/{}&"
        "fields=items(kind,mediaLink,metadata,name,size,updated),kind,prefixes,nextPageToken"
    ).format(oslarge, base_position[:-2])).json()['prefixes']
    
    assert len(download_urls_available) > 0
    
    prefixes = [x.split("/")[1] for x in download_urls_available]

    take_closest = lambda num,collection:min(collection, key = lambda x: abs(x-num))
    prefix = str(take_closest(int(base_position), [int(x) for x in prefixes]))
    
    #prefix = download_urls_available[-1].split("/")[1]
    
    download_urls = requests.get((
        "https://www.googleapis.com/storage/v1/b/chromium-browser-snapshots/o?"
        "delimiter=/&prefix={}/{}/&"
        "fields=items(kind,mediaLink,metadata,name,size,updated),kind,prefixes,nextPageToken"
    ).format(oslarge, prefix)).json()['items']
    
    chrome_download_url = None
    chromedriver_url = None
    
    for download_url_metadata in download_urls:
        if f"chrome-{ossmall}.zip" in download_url_metadata['mediaLink']:
            chrome_download_url = download_url_metadata['mediaLink']
            
        if "chromedriver" in download_url_metadata['mediaLink']:
            chromedriver_url = download_url_metadata['mediaLink']
    
    return major_version, chrome_download_url, chromedriver_url

def indexes_of_wanted_version_numbers(ossmall):
    indexes = []
    wanted_major_version_numbers = []
    all_version_numbers = [hjson['version'] for hjson in history(ossmall)]
    for index, version_number in enumerate(all_version_numbers):
        major_version = version_number.split(".")[0]
        if major_version not in wanted_major_version_numbers:
            if int(major_version) >= 80:
                wanted_major_version_numbers.append(major_version)
                indexes.append(index)
    return indexes

def get_versions():
    print("Downloading version data...")
    
    versions = {}
    
    for index in indexes_of_wanted_version_numbers("linux"):
        version, chrome_url, driver_url = get_for_os(index, "linux", "Linux_x64")
        
        if version not in versions:
            versions[version] = {}
        versions[version]['linux_chrome'] = chrome_url
        versions[version]['linux_chromedriver'] = driver_url
    
    for index in indexes_of_wanted_version_numbers("mac"):
        version, mac_chrome_url, mac_driver_url = get_for_os(index, "mac", "Mac")
        if version not in versions:
            versions[version] = {}
        versions[version]['mac_chrome'] = mac_chrome_url
        versions[version]['mac_chromedriver'] = mac_driver_url

    return versions
