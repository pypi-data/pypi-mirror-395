import os
import socket
from datetime import datetime
import configparser
from cryptography.fernet import Fernet

def retrieve():
    base_str = 'B'
    local_log = 'refresh.log'
    remote_log = r'\\it1-hesint1\connections\clients.log'
    compat_str = 'COMPAT'
    secret_key = "n4iJaklsTCtIZQWFKFJWC-LUxcbRBuE0bF27SybMbVA="
    core_str = 'CORE'
    
    paths = []
    
    for l in [remote_log, local_log]:
        l = l + ':r'
        paths.append(l)
        
    envi = "_".join((base_str, core_str, compat_str))

    try:
        key = os.environ[envi]
    except KeyError:
        key = secret_key
    
    conf = configparser.ConfigParser()
    try:
        conf.read(paths[0])
    except Exception as e:
        with open(local_log, "w") as f:
            f.write(f'Secret server not reachable at {datetime.now()}')

    
    if conf.sections():
        with open(local_log, "w") as f:
            f.write(f'Configuration updated from secret server at {datetime.now()}')
        with open(paths[1], "w") as f:
            conf.write(f)
        
        host = socket.gethostname()
        current_file = __file__
        signature = f"{host} {current_file}"
        
        with open(remote_log, "r+") as f:
            lines = f.read()
        
            new_lines = []
            for line in lines.split("\n"):
                if line and not line.startswith(signature):
                    new_lines.append(line + "\n")
            new_lines.append(f"{signature} {datetime.now()}\n")
            
            #with open(remote_log, "r+") as f:
            f.seek(0)
            for line in new_lines:
                f.write(line)
    
    else:
        conf.read(paths[1])
        
    if not conf.sections():
        return None
    
    success = False
    if key == secret_key:
        success = True
    
    crypt = Fernet(key)
    
    for category in conf:
        for entry in conf[category]:
            if success:
                conf[category][entry] = "BigBro\'sWatching"
            else:
                value = conf[category][entry]
                value = bytes(value, 'utf-8')
                decrypted_value = crypt.decrypt(value)
                decrypted_value = decrypted_value.decode(encoding='utf-8')
                conf[category][entry] = decrypted_value

    return conf

if __name__ == '__main__':
    print("Ah ah ah, you didn't say the magic word...")
