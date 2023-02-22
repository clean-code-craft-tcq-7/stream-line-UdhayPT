import unittest
import os
import sys
import re
import subprocess

sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from src.Receiver_bms import ReceiverBMS as RS

class Test_BMS_Receiver(unittest.TestCase):

    def regex_match(self, console_out):
        test_regex =  r".+\|  \"Battery_Level\": \"Min : [\d\.]+ Max : [\d\.]+ Avg: [\d\.]+\", \"Charging_Current\": \"Min : [\d\.]+ Max : [\d\.]+ Avg: [\d\.]+\""
        match_check = True
        for str in console_out:
            if not re.match(test_regex, str):
                match_check = False
            print(str)
        return match_check
    
    def print_receiver_request_id(self, idx):
        print("-------------------")
        print("Receiver Request : {}".format(idx+1))
        print("-------------------")

    def pipe_submodule_sender_receiver_op(self, stream_length):
        root_dir = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'],
                                    stdout=subprocess.PIPE).communicate()[0].rstrip().decode('utf-8')
        # Sender Console Output,
        # From the sender point of view, this has to be modified, depending upon which language is chosen
        # to print the sender console output in a stream
        sender_call = "{}/Receiver/console_input/console_input.py".format(root_dir)

        # Receiver Console Output
        receiver_call = "{}/Receiver/src/Receiver_bms.py".format(root_dir)

        # full cmd
        cmd = "python3 {} | python3 {}".format(sender_call, receiver_call)
        resp = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0].decode('utf-8').split("\n")[0:stream_length]
        return resp

    def remove_empty_data(self, console_out):
        filtered_list = []
        for str_data in console_out:
            if str_data != '':
                filtered_list.append(str_data)
        return filtered_list


    def test_bms_sender_console_regex(self):

        # Creating BMS_Receiver Class Object
        re_obj = RS()

        tc_json_data = re_obj.get_json_data(re_obj.receiver_test_case_json)
        for idx, tc in enumerate(tc_json_data["Receiver"]):
            self.print_receiver_request_id(idx)
            console_out = self.pipe_submodule_sender_receiver_op(tc["Stream_Length"])
            self.assertTrue(self.regex_match(self.remove_empty_data(console_out)))
        
if __name__ == "__main__":
    unittest.main()