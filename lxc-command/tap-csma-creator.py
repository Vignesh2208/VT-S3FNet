import sys
import os


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: python tap-csma-creator #LXCs SimTDF"
        sys.exit()
    PATH_TO_NS3_TAP_SRC = "/home/jereme/repos/ns-3-allinone/ns-3-dev/src/tap-bridge/examples" 
    numLXCs = sys.argv[1]
    tdf = int(float(sys.argv[2])*1000)
    template = open("template-csma.cc", 'r')
    output = open(PATH_TO_NS3_TAP_SRC + "/tap-csma-virtual-machine.cc", 'w')
    nodesVar = "x"
    netDeviceVar = "x"
    tapBridgeVar = "x"
    for line in template:
        line = line.strip()
        if "NodeContainer" in line:
            lineSplit = line.split(' ')
            nodesVar = (lineSplit[1].strip())[:-1]
#            nodesVar = nodesVar.replace(' ', '')
        if "NetDeviceContainer" in line:
            lineSplit = line.split(' ')
            netDeviceVar = lineSplit[1].strip()
        if "TapBridgeHelper" in line:
            lineSplit = line.split(' ')
            tapBridgeVar = (lineSplit[1].strip())[:-1]
        if "@@@" in line:
            line = line.replace('@@@', numLXCs)
        if "###" in line:
            line = line.replace('###', str(tdf))
        if "$$$" in line:
            for i in range(0,int(numLXCs)):
                output.write(tapBridgeVar + ".SetAttribute (\"DeviceName\", StringValue (\"tap-" + str(i+1) + "\"));\n")
                output.write(tapBridgeVar + ".Install (" + nodesVar + ".Get (" + str(i) + "), " + netDeviceVar + ".Get (" + str(i) + "));\n")
            continue
        output.write(line + "\n")
    template.close()
    output.close()    
    #print nodesVar, "|", netDeviceVar,"|", tapBridgeVar,"|"
