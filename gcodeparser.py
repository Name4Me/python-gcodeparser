from math import tan
import sys
import re

class Parse(object):

     def __init__(self, filename):
          self.filename = filename
          self.parse()

     def parse(self):

          try:
               fp = open(self.filename,'r')
          except IOError:
               print("Unable to open the file" + self.filename + "\n")
          else:
               nfp = open("k"+self.filename,'w')
               prevX = -9999.0
               prevY = -9999.0
               prevZ = -9999.0
               prevG = -1
               prevF = -9999.0
               lx = 0.0
               x = 0.0
               y = 0.0
               yk = 0.0
               z = 0.0
               s = 0.0
               f = 0.0
               l = 1
               g = -1

               while 1:
                    gcode = fp.readline()
                    if not gcode: break
                    if (gcode == '\n'): 
                         nfp.write(gcode)                         
                         continue
                    flag = 0

                    #parse g code
                    
                    gg = re.search("[gG]([\d]+)\D",gcode)
                    xx = re.search("[xX]([\d\.\-]+)\D",gcode)
                    yy = re.search("[yY]([\d\.\-]+)\D",gcode)
                    zz = re.search("[zZ]([\d\.\-]+)\D",gcode)
                    rr = re.search("[rR]([\d\.\-]+)\D",gcode)
                    ss = re.search("[sS]([\d\.\-]+)\D",gcode)
                    ff = re.search("[fF]([\d\.\-]+)\D",gcode)

                    if (gg): g = int(gg.group(1))
                    if (xx): x = float(xx.group(1))
                    if (yy): y = float(yy.group(1))
                    if (zz): z = float(zz.group(1))
                    if (rr): r = float(rr.group(1))
                    if (ss): s = float(ss.group(1))
                    if (ff): f = float(ff.group(1))

                    values = ''

                    if (xx and x != prevX): 
                         prevX = x
                         flag = 1
                         values = values + ' X' + str(x)
                         if (not yy) :
                              yk = round((prevY-(x*tan(0.00086))),2)
                              values = values + ' Y' + str(yk)

                    if (yy and y != prevY):
                         prevY = y
                         flag = 1
                         yk = round((y-(prevX*tan(0.00086))),2)
                         values = values + ' Y' + str(yk)

                    if (zz and z != prevZ): 
                         prevZ = z
                         flag = 1
                         values = values + ' Z' + str(z)

                    if (ff and f != prevF): 
                         prevF = f
                         values = values + ' F' + str(f)

                    print(gcode)
                    print('S: ',values)



                    #lines
                    if((g == 1 or g == 0) and flag): nfp.write('G'+str(g)+values+'\n')
                    elif(g == 2 or g == 3): nfp.write('G'+str(g)+values+' R'+str(r)+'\n')
                    elif(flag): nfp.write(values+'\n')
                    else: 
                         nfp.write(gcode)
                         #print (gcode, "Demo",end='')				
                    l += 1
                    g = -1
               fp.close()
               nfp.close()

if __name__ == "__main__":
    if (len(sys.argv) > 1):
          parser = Parse(sys.argv[1])

