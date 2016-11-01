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
               lx = 0.0
               x = 0.0
               y = 0.0
               yk = 0.0
               z = 0.0
               s = 0
               f = 0
               l = 1
               style = -1

               while 1:
                    gcode = fp.readline()
                    if not gcode: break
                    if (gcode == '\n'): continue
                    flag = 0
                    def test():
                         result = ''
                         if (xx): result = result + 'X' + str(x)
                         return result
                    #parse g code
                    print(gcode)
                    gg = re.search("[gG]([\d]+)\D",gcode)
                    xx = re.search("[xX]([\d\.\-]+)\D",gcode)
                    yy = re.search("[yY]([\d\.\-]+)\D",gcode)
                    zz = re.search("[zZ]([\d\.\-]+)\D",gcode)
                    ss = re.search("[sS]([\d\.\-]+)\D",gcode)
                    ff = re.search("[fF]([\d\.\-]+)\D",gcode)

                    if (gg):
                         style = int(gg.group(1))
                    if (xx):
                         x = float(xx.group(1))
                         yk = round((y-(x*tan(0.00086))),2)
                         flag = 1
                         #print("Line: ",l," X: ",x)
                    if (yy):
                         y = float(yy.group(1))
                         yk = round((y-(x*tan(0.00086))),2)
                         flag = 1
                    if (zz):
                         z = float(zz.group(1))
                         flag = 1
                    if (ss):
                         s = float(ss.group(1))
                    if (ff):
                         f = float(ff.group(1))
                         #print "s: {0}".format(s)

                    #print("Line: ",l," X: ",x," Y: ",yk," Z: ",z)

                    if(style == 1 or style == 0):
                         #lines
                         if(flag):
                              print ("Line", gcode, end='')
                              test()
                              nfp.write('G'+str(style)+' X'+str(x)+' Y'+str(yk)+' Z'+str(z)+'\n')
                    elif(style == 2 or style == 3):
                         #arcs
                              rr = re.search("[rR]([\d\.\-]+)\D",gcode)
                              if(rr):
                                   r = float(rr.group(1))
                                   pass
                              print ("arc ",gcode, end='')
                              nfp.write('G'+str(style)+' X'+str(x)+' Y'+str(yk)+'\n')

                    else: 
                         nfp.write(gcode)#
                         print (gcode, end='')				
                    l += 1
                    lx = x
                    #style = -1
               fp.close()
               nfp.close()

if __name__ == "__main__":
    if (len(sys.argv) > 1):
          parser = Parse(sys.argv[1])


