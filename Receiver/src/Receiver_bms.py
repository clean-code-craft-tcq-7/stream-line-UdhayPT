import subprocess
import os
import json, re

class ReceiverBMS:
    def __init__(self) -> None:
        self.root_dir = self.root_dir = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'],
                                    stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
        self.stream_length = 50
        self.regex_match = r".+: (.+)%,.+: (.+) A"
        self.receiver_config_json = os.path.join(self.root_dir, "Receiver", "inc", "receiver_config.json")

    def get_json_data(self, path):
        data = {}
        if os.path.exists(path):
            with open(path, 'r') as jsonread:
                data = json.load(jsonread)
        return data
    
    def get_battery_parameters(self, console_data):
        battery_param = self.get_json_data(self.receiver_config_json)["Receiver_Config"]["Battery_Parameters"]
        # battery_level, charging_current = battery_param
        if re.match(self.regex_match, console_data):
            for idx, key in enumerate(battery_param):
                battery_param[key] = re.search(self.regex_match, console_data).group(idx+1)
        return battery_param

if __name__ == "__main__":
    R_obj = ReceiverBMS()
    for i in range(R_obj.stream_length):
        console_sender_data = input()
        param_dict = R_obj.get_battery_parameters(console_sender_data)
        
        
        