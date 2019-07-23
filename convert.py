inFile = open('ip.txt','r')
list_ip=[]

ll = inFile.readlines()
for line in ll:
    print (line)
    line = line.split(':')
    list_ip.append(line)
inFile.close()
proxyFile = open('proxy.txt', 'a')
for i in list_ip:
    ip, port = i
    proxyFile.write("None|%s|%s|None|None|HTTP|None|None" % (ip, port[:-1]))
    proxyFile.write("\n" )
proxyFile.close()

