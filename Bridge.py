import sys
from pywifi.wifi import PyWiFi
from threading import Timer
from pywifi import const

class Bridge():

    def __init__(self):
        self.wifi = PyWiFi()
        self.iface = self.wifi.interfaces()[0]
        self.allProfiles = []
        self.allWiFi_names = []

    def scanWifi(self):
        resultsSrc = self.iface.scan_results()
        akmOfAllWiFi = []

        for res in resultsSrc:
            if bool(self.allWiFi_names.__contains__(res.ssid)) != True:
                # Create JSON from the {string}
                self.allWiFi_names.append(res.ssid)
                self.allProfiles.append(res)

                case = {
                    0: None,
                    1: 'WPA',
                    2: 'WPA_PSK',
                    3: 'WPA2',
                    4: 'WPA2_PSK',
                    5: 'UNKNOWN'
                }

                akm = case[res.akm[0]]
                akmOfAllWiFi.append(akm)

        print(self.allWiFi_names)
        print(akmOfAllWiFi)

    def getIface(self):
        return self.iface

    def connectTo(self, selectedSSID, password):
        print(selectedSSID, password)

        br = mainScan()

        for WiFi_Profile in br.allProfiles:
            # print('checking', WiFi_Profile.ssid)
            if WiFi_Profile.ssid == selectedSSID:
                # print('WiFi found')
                
                # assert iface.status() in\ 
                # [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]
                
                WiFi_Profile.auth = const.AUTH_ALG_OPEN
                WiFi_Profile.cipher = const.CIPHER_TYPE_CCMP
                WiFi_Profile.akm = WiFi_Profile.akm
                WiFi_Profile.key = None
                
                if password != None or WiFi_Profile.akm != const.AKM_TYPE_NONE:
                    WiFi_Profile.key = password

                minimalConnect(br, WiFi_Profile)

                if br.getIface().status() != const.IFACE_CONNECTED or br.getIface().status() != const.IFACE_CONNECTING:
                    # Retrying connect again
                    # print(WiFi_Profile.ssid)
                    # print(WiFi_Profile.auth)
                    # print(WiFi_Profile.akm)
                    # print(WiFi_Profile.cipher)
                    # print(WiFi_Profile.bssid)
                    # print(WiFi_Profile.key)
                    
                    if WiFi_Profile.akm != const.AKM_TYPE_NONE:
                        for auth in range(0, 2):
                            for cipher in range(0, 5):
                                WiFi_Profile.auth = auth
                                WiFi_Profile.cipher = cipher
                                WiFi_Profile.key = ""

                                # print("cipher {cipher}", cipher)
                                Timer(1000, minimalConnect(br, WiFi_Profile))

                                if br.getIface().status() == const.IFACE_CONNECTED or br.getIface().status() == const.IFACE_CONNECTING:
                                    if br.getIface().status() == const.IFACE_CONNECTING:
                                        print("CONNECTING")
                                        break
                                    else:
                                        print("CONNECTED")
                                        break                   

                if br.getIface().status() == const.IFACE_CONNECTED:
                    print("CONNECTED")
                    break

                print("CONNECTING")

def minimalConnect(br, WiFi_Profile):
    if br.getIface().status() != const.IFACE_CONNECTED or br.getIface().status() != const.IFACE_CONNECTING:
        br.getIface().disconnect()

    # print("#############################################################")
    # print(WiFi_Profile.ssid)
    # print(WiFi_Profile.akm) 
    # print(WiFi_Profile.auth)
    # print(WiFi_Profile.cipher)
    # print(WiFi_Profile.bssid)
    # print(WiFi_Profile.key)
    # print("#############################################################")

    br.getIface().add_network_profile(WiFi_Profile)
    br.getIface().connect(WiFi_Profile)

    # print(br.getIface().status())

# Run iface.scan() and after that wait 10 seconds
def mainScan():
    br = Bridge()

    br.getIface().scan()
    Timer(10.0, br.scanWifi).run()

    return br

def mainConnect():
    # Play by command line args
    selectedSSID = sys.argv[2]
    try:
        password = sys.argv[3]
    except:
        password = None

    Bridge().connectTo(selectedSSID, password)                

def mainStatus():
    # Check if connected to any WiFi network
    iface_mode = Bridge().getIface().status()
    cases = {
        const.IFACE_DISCONNECTED: 'DISCONNECTED',
        const.IFACE_SCANNING: 'SCANNING',
        const.IFACE_INACTIVE: 'INACTIVE',
        const.IFACE_CONNECTING: 'CONNECTING',
        const.IFACE_CONNECTED: 'CONNECTED'
    }[iface_mode]

    print(cases)

# Like switch case
cases = {
    '-scan': mainScan,
    '-connect': mainConnect,
    '-status': mainStatus
}

runCase = cases[sys.argv[1]]
runCase()