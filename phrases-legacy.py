if readable_result.find("stopp") >= 0:
            sys.exit()
        elif readable_result.find("selbstzerstörung aktivieren") >= 0:
            print('Selbstzerstörung aktiviert')
            time.sleep(1)
            print('3')
            time.sleep(1)
            print('2')
            time.sleep(1)
            print('1')
            print('Booooooooommmmm!!!!')
            sys.exit()
        elif readable_result.find("licht an") >= 0:
            client.publish("main/hm/manuel/licht/panel", "1")
        elif readable_result.find("licht aus") >= 0:
            client.publish("main/hm/manuel/licht/panel", "0")
        elif readable_result.find("licht süd an") >= 0:
            client.publish("main/hm/manuel/licht/süd", "1")
        elif readable_result.find("licht süd aus") >= 0:
            client.publish("main/hm/manuel/licht/süd", "0")
        elif readable_result.find("licht nord an") >= 0:
            client.publish("main/hm/manuel/licht/nord", "1")
        elif readable_result.find("licht nord aus") >= 0:
            client.publish("main/hm/manuel/licht/nord", "0")
        elif readable_result.find("licht bett an") >= 0:
            client.publish("main/hm/manuel/licht/bett", "1")
        elif readable_result.find("licht bett aus") >= 0:
            client.publish("main/hm/manuel/licht/bett", "0")
        elif readable_result.find("rollladen hoch") >= 0:
            client.publish("main/hm/manuel/rolladen", "100")
        elif readable_result.find("rollladen runter") >= 0:
            client.publish("main/hm/manuel/rolladen", "0")
        elif readable_result.find("rollladen auf") >= 0:
            client.publish("main/hm/manuel/rolladen", "0")