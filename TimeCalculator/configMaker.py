from configparser import ConfigParser

config_object = ConfigParser()

config_object["RUNTIME_INFO"] = {
    "numIter": 99,
    "debugMode": False
}

with open('TimeCalc.ini', 'w') as conf:
    config_object.write(conf)

print("CONFIG CREATED\n")
