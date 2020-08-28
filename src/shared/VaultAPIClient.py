import requests


class VaultAPIClient:
    def __init__(self, ip):
        self.ip = ip
        self.URL = "http://{}:8080".format(self.ip)

    def perform_health_check(self):
        endpoint = "{}/healthcheck".format(self.URL)
        response = requests.get(endpoint)
        return response.json(), response.status_code

    def get_download_speed(self):
        endpoint = "{}/get/downloadspeed".format(self.URL)
        response = requests.get(endpoint)
        return response.json(), response.status_code

    def perform_network_map(self):
        endpoint = "{}/networkmap/getconnectedclients".format(self.URL)
        response = requests.get(endpoint)
        return response

    def perform_localhost_port_scan(self):
        endpoint = "{}/portscan/local".format(self.URL)
        response = requests.get(endpoint)
        return response.json(), response.status_code

    def perform_port_scan(self, ip_address):
        endpoint = "{}/portscan/{}".format(self.URL, ip_address)
        response = requests.post(endpoint)
        return response.json()

    def get_list_of_connected_devices_ips(self):
        ips = []
        response = self.perform_network_map()
        if response.status_code == 200:
            clients = response.json()
            for x in range(len(clients['Clients'])):
                ips.append(clients['Clients'][x]['IP'])
            return ips
        else:
            return "Error: %s" % response.status_code

    def port_scan_all_connected_devices(self):
        results = {}
        devices = self.get_list_of_connected_devices_ips()
        for i in range(len(devices)):
            results[devices[i]] = self.perform_port_scan(devices[i])[0]
        return results

    def timeout_connected_device(self, mac_address, ban_time):
        endpoint = "{}/client/banclient/{}/{}".format(self.URL, mac_address, ban_time)
        response = requests.get(endpoint)
        return response.json(), response.status_code


# Local Testing
# router_a = VaultAPIClient("192.168.8.1")
# print(router_a.perform_health_check())
# a = router_a.perform_network_map().json()
# x = {"name": a['Clients'][0]['Hostname'],
#           "mac_address": a['Clients'][0]['MAC'],
#           "ip_address": a['Clients'][0]['IP'],
#           "status": True}
# print(x)
# print(a['Clients'][0])
# print(router_a.get_list_of_connected_devices_ips())
# print(perform_localhost_port_scan())
# print(port_scan_all_connected_devices())
# perform_port_scan("192.168.8.1")
# print(timeout_connected_device("48:01:C5:04:83:71", "1000"))
