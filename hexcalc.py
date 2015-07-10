#!/usr/bin/python
import sys
import argparse
import os

verbose = False
current = '0x00000000'
targetbytes = ''
sumbytes = ''
start = ''
lasttry = ''
lastresult = current
ops = []
results = {}
allowed = ''
checkbad = False


def query_yes_no(question, default="yes"):
    """
    http://code.activestate.com/recipes/577058/
    Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def clearScreen():
    os.system("clear")

def status(full=True):
    if not verbose: clearScreen()

    if full:
        print ""
        print "Bytes to encode: " + targetbytes
        print "\n\tGoal Sum: %08x" % int(sumbytes, 16)
        print "\tLast:     %08x" % int(lastresult, 16)
        print "\tCurrent:  %08x" % int(current, 16)
        print ""
        print "\tLast try: " + lasttry
        print ""
        for i in range(len(ops)):
            sys.stdout.write("\nSubtract " + str(i+1) + " : " + ops[i])


def makeHexStr(inputdata):
    data = inputdata.rstrip()
    data = data.strip('"')
    data = data.decode('string-escape')
    returnval = "0x" + data[::-1].encode('hex')
    if verbose: print "VERBOSE: returnval = " + returnval
    return returnval

def reset():
    global ops, current, lasttry, lastresult
    ops = []
    current = "0x00000000"
    lasttry = "0x00000000"
    lastresult = "0x00000000"

def add(hexstr):
    global current
    current = hex(int(current, 16) + int(hexstr, 16))

def charCheck(data):
    global allowed

    badchar = []
    if checkbad:
        if verbose: print "\nVERBOSE: Checking data: " + data
        hexstr = data[2:].decode('hex')
        if verbose: print "\nVERBOSE: Checking hexstr: " + hexstr
        for byte in hexstr:
            if byte not in allowed:
                badchar.append(byte)

        if len(badchar) > 0:
            print "\n\nWARNING - The following byte(s) are not on the allowed list:"
            for ch in badchar:
                print ch.encode('hex'),
            print ""


def calc(inputdata):
    global start, targetbytes, ops, sumbytes, lasttry, current, lastresult, results

    if verbose: print "VERBOSE: InputData: " + inputdata
    targetbytes = makeHexStr(inputdata)
    if verbose: print "VERBOSE: targetbytes: " + targetbytes
    sumbytes = hex(0xFFFFFFFF - int(targetbytes, 16) + 0x1)
    status()

    try:
        while sumbytes[2:] not in current:
            accept = False
            while not accept:
                print ""
                optry = raw_input("\nEnter a hex string:"
                                  "\nFormat 0x00112233"
                                  "\n(ctrl+c to move to next value or type 'back'):\n ")
                if optry.lower() != 'back':
                    add(optry)
                    lastresult = current
                    lasttry = optry
                    ops.append(optry)
                    print ""
                    status()
                    charCheck(optry)
                    accept = query_yes_no("\nKeep new value? :", default="no")
                    if not accept:
                        ops.pop()
                        current = hex(int(current, 16) - int(lasttry, 16))
                        status()
                    else:
                        status()
                else:
                    try:
                        ops.pop()
                        current = hex(int(current, 16) - int(lasttry, 16))
                        status()
                    except IndexError:
                        print "No values have been entered yet."

        #When done calculating (or after keyboard interrupt) save progress in results dict
        results[targetbytes] = ops

        #reset fields
        reset()

    except KeyboardInterrupt:
        print ""
        print ""
        reset()
        results[targetbytes] = ops
        ops = []
        current = "0x00000000"
        lasttry = "0x00000000"
        lastresult = "0x00000000"

def printResults():
    global results

    print "Final Results\n"
    for target, operands in results.iteritems():
        print ""
        print "Target value: " + target
        print "Subtract the following values:"
        for oper in operands:
            print "\t" + oper


def main():
    global verbose, allowed, checkbad

    parser = argparse.ArgumentParser(description="Hex Calculation")
    parser.add_argument("-v",
                        "--verbose",
                        help="print verbose log (everything in response)",
                        action="store_true")
    parser.add_argument("-f",
                        "--infile",
                        required=True,
                        help="Path to file with binary strings - 4 bytes per line ('\\x75\\xe7\\x3f\\x34')")
    parser.add_argument("-a",
                        "--charfile",
                        help="Path to file with list of allowed characters in format '\\x75' ")
    args = parser.parse_args()

    if args.verbose: verbose = args.verbose

    try:
        f = open(args.infile, 'r')
    except:
        print "Error reading input file " + args.infile + ". Exiting.."
        sys.exit(1)

    if args.charfile:
        try:
            cf = open(args.charfile, 'r')
            allowed = cf.read().decode('string-escape')
            allowed = allowed.rstrip()
            allowed = allowed.strip('"')
            checkbad = True
        except IOError:
            print "Error reading allowed character file " + args.charfile + ". Exiting.."

    for line in f.readlines():
        calc(line)

    printResults()

if __name__ == '__main__':
        main()