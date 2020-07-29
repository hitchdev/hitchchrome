import requests

OMAHAPROX = "omahaprox"

def get_for_os(which_version, ossmall, oslarge):
    print(f"Downloading version data for {ossmall}...")
    historyjson = requests.get(f"https://{OMAHAPROX}y.appspot.com/history.json?channel=stable&os={ossmall}").json()
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
    ).format(oslarge, base_position[:-1])).json()['prefixes']
    
    assert len(download_urls_available) > 0
    
    prefix = download_urls_available[-1].split("/")[1]
    
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

def get_versions():
    print("Downloading version data...")
    version, chrome_url, driver_url = get_for_os(0, "linux", "Linux_x64")
    version, mac_chrome_url, mac_driver_url = get_for_os(0, "mac", "Mac")

    return {
        version : {
            "linux_chrome": chrome_url,
            "linux_chromedriver": driver_url,
            "mac_chrome": mac_chrome_url,
            "mac_chromedriver": mac_driver_url,
        },
    }
