import json


def get_abi():
    abi_file = open('ballot_mgmt/api/contract/Ballot_sol_Ballot.abi')
    abi_json = json.load(abi_file)
    abi_file.close()
    
    return abi_json

def get_bytecode():
    bytecode_file = open('ballot_mgmt/api/contract/Ballot_sol_Ballot.bin')
    bytecode_string = bytecode_file.read()
    bytecode_file.close()
    
    return bytecode_string
