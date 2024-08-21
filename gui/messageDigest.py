import json
import motherGUI
def messageDigst(msg):
    print(msg)
    try:
        msg = json.loads(msg)
    except:
        print("Not Json ", msg)
        try:
            msg = eval(msg)
            print("Its a dict")
        except:
            print("Not a dict")
    if msg["msg_name"] == "register":
        motherGUI.createWorker(msg)
    elif msg["msg_name"] == "register_list":
        motherGUI.createWorkers(msg)
    print(type(msg))
