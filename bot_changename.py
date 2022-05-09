import socket
def changename(group,qq="1475326665",name="bot"):
        ip = '127.0.0.1'
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, 5700))
        payload = "GET /set_group_card?group_id="+str(group)+"&user_id="+qq+"&card="+str(name)+" HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
        client.send(payload.encode("utf-8"))
        client.close()
        return 0
