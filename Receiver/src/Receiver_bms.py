import subprocess
import os
import json, re

class ReceiverBMS:
    def __init__(self) -> None:
        self.root_dir = self.root_dir = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'],
                                    stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
        self.stream_length = 50
        # Regex needs to be modified depending upon the battery parameters and sender connsole output
        self.regex_match = r".+: (.+)%,.+: (.+) A"
        self.receiver_config_json = os.path.join(self.root_dir, "Receiver", "inc", "receiver_config.json")
        self.receiver_test_case_json = os.path.join(self.root_dir, "Receiver", "inc", "receiver_test_case.json")

    def get_json_data(self, path):
        data = {}
        if os.path.exists(path):
            with open(path, 'r') as jsonread:
                data = json.load(jsonread)
        return data
    
    def get_battery_parameters(self, console_data):
        battery_param = self.get_json_data(self.receiver_config_json)["Receiver_Config"]["Battery_Parameters"]
        if re.match(self.regex_match, console_data):
            for idx, key in enumerate(battery_param):
                battery_param[key] = re.search(self.regex_match, console_data).group(idx+1)
        return battery_param
    
    def print_sma(self, value):
        global avg_list, sma
        avg_list.append(float(value))
        if len(avg_list) > sma:
            avg_list.pop(0)
        return str(format(sum(avg_list)/sma, ".2f"))

    def min_max_value(self, val_list):
        return "Min : {} Max : {}".format(min(val_list), max(val_list))

    def print_min_max_avg_string(self, param_dict):
        global Asorted_Battery_Parameter, avg_list
        for param, value in param_dict.items():
            Asorted_Battery_Parameter[param].append(value)
            param_dict[param] = self.min_max_value(Asorted_Battery_Parameter[param]) + " Avg: {}".format(self.print_sma(value))
        return param_dict
        
if __name__ == "__main__":

    R_obj = ReceiverBMS()

    receiver_config = R_obj.get_json_data(R_obj.receiver_config_json)

    # This is to list all the min max average as per dynamic count of parameter
    global Asorted_Battery_Parameter, avg_list, sma
    avg_list = []
    Asorted_Battery_Parameter = receiver_config["Receiver_Config"]["Battery_Parameters"]
    sma = receiver_config["Receiver_Config"]["Simple_Moving_Average"]
    
    for i in range(R_obj.stream_length):
        console_sender_data = input()
        param_dict = R_obj.get_battery_parameters(console_sender_data)
        min_max_avg_data = json.dumps(R_obj.print_min_max_avg_string(param_dict)).replace("{","").replace("}","")
        print(console_sender_data, " | ", min_max_avg_data)