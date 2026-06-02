import re

def parse_list_type(decoded_data):
    # get all the digits at the begging of string, till non-numeric character appears
    re_pattern = re.compile('^(\d+)')
    found = re_pattern.findall(decoded_data)[0]
    len_arr = int(found)



def parse_redis_type_protocol(decoded_data:str):
    if decoded_data[0] == '*':
        parse_list_type(decoded_data[1:])
    elif decoded_data[0] == '+':
        command
        return command, None, message


