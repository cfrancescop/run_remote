import paramiko
import time
import sys
paramiko.util.log_to_file("paramiko.log")
client = paramiko.SSHClient()
# auto add to know_hosts
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

#attende la riga pronta all'input
def wait_for_ttl(chan):
    time.sleep(1)
    buff = ''
    #]$ wait for
    while buff.find(']$') < 0 :
        resp = chan.recv(9999)
        buff += resp
        print(resp)

#end functions
def send_commands(host='localhost',username='root',commands = [],key_filename='~/.ssh/id_rsa',port=22):

    print(host)
    client.connect(host, port=port, username=username,key_filename=key_filename)

    print('Recover ssh session')

    stdin, stdout, stderr = client.exec_command('whoami')
    for line in stdout:
        print('i am ' + line.strip('\n'))
    chan = client.invoke_shell()
    for command in commands:
        print("send command %s" % command)
        chan.send(command + '\n')
        wait_for_ttl(chan)
    # close session
    client.close()

if __name__ == "__main__":
    username="root"
    key_file='~/.ssh/id_rsa'
    host="localhost"
    port=22
    commands=[]
    i=1
    while i < len(sys.argv):
        flag = sys.argv[i]
        value = sys.argv[i+1]
        print(" %s %s" % (flag,value))
        # set the username
        if flag == '-u':
            username = value
        # set the host
        elif flag == '-h':
            host = value
        # set the port
        elif flag == '-p':
            port = value
        # set the key file
        elif flag == '-i':
            key_file=value
        # read a file
        elif flag == '-f':
            file = open(value, "r") 
            for line in file: 
                commands.append(line) 
        # parse a string
        elif flag == '-s':
            commands=value.replace('"','').replace("'","").split(';')
        i+=2

    
    print('%s@%s' %(username,host) )
    send_commands(host,username=username,commands=commands,key_filename=key_file)
    #map(deploy_ibridge,hosts)
    #end main
