import socket
import time

def connect(HOST='127.0.0.1', PORT=5000):
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(180)
    try:
        sock.connect((HOST, PORT))
        print('Connection established')
        return True
    except socket.timeout:
        print('Waiting time for connection has expired')
        return False
    except Exception as e:
        print(str(e))
        return False 

def send(string):
    global sock
    string = '$' + string + '\r\n'
    c = string.encode('utf-8')
    sock.sendall(c)
    data = sock.recv(1024)
    print('Answer from controller:', data.decode())
    time.sleep(1)
    return True

def command(string):
    global sock
    c = ('$Execute,"' + string + '"\r\n').encode('utf-8')
    sock.sendall(c)
    data = sock.recv(1024)
    print('Executing command ' + string + ":", data.decode())
    return True
   
def go(x,y,z,u=0,v=-90,w=-90):
    command("Go XY("+str(x)+","+str(y)+","+str(z)+","+str(u)+","+str(v)+","+str(w)+")")
    return True
    
def move(x,y,z,u=0,v=-90,w=-90):
    command("Move XY("+str(x)+","+str(y)+","+str(z)+","+str(u)+","+str(v)+","+str(w)+")")
    return True

def go_here(x,y,z=0):
    command("Go Here +X(" + str(x) +") +Y(" + str(y) + ")" + " +Z(" + str(z) + ")")
    return True

def move_here(x,y,z=0):
    command("Move Here +X(" + str(x) +") +Y(" + str(y) + ")"+ " +Z(" + str(z) + ")")
    return True
    
def begin(speed=50,speeds=1000,accel=60,accels=200,weight=0,inertia=0,speedfactor=50,power='Low',homeset=[0,0,0,0,0,0]):
    send('Login')
    send('SetMotorsOn,0')
    command("If Error On Then Reset")
    command('Speed '+ str(speed))
    command('SpeedS ' + str(speeds))
    command('Accel ' + str(accel)+ ',' + str(accel))
    command('AccelS '+ str(accels))
    command('Weight '+ str(weight))
    command('Inertia '+ str(weight))
    command('SpeedFactor ' + str(speedfactor))
    command('Power ' + str(power))
    command('HomeSet ' + ','.join(map(str, homeset)))
    print("Initialization complete")
    return True