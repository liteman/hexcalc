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
        sys.stdout.flush()
        sys.stdout.write( "Bytes to encode: " + targetbytes )
        sys.stdout.write( "\n\n\tGoal Sum: %08x" % int(sumbytes, 16))
        sys.stdout.write("\n\tCurrent:  %08x" % int(current, 16))
        sys.stdout.write("\n\tLast:     %08x" % int(lastresult, 16))
        sys.stdout.write("\n")
        sys.stdout.write("\n" + "Last try: " + lasttry)
        sys.stdout.write("\n")
        for i in range(len(ops)):
            sys.stdout.write("\nSubtract " + str(i+1) + " : " + ops[i])


def makeHexStr(inputdata):
    data = inputdata.rstrip()
    data = data.strip('"')
    data = data.decode('string-escape')
    returnval = "0x" + data[::-1].encode('hex')
    if verbose: print "returnval = " + returnval
    return returnval

def add(hexstr):
    global current
    current = hex(int(current, 16) + int(hexstr, 16))

def calc(inputdata):
    global start, targetbytes, ops, sumbytes, lasttry, current, lastresult, results

    if verbose: print inputdata
    targetbytes = makeHexStr(inputdata)
    if verbose: print targetbytes
    sumbytes = hex(0xFFFFFFFF - int(targetbytes, 16) + 0x1)
    status()

    try:
        while sumbytes not in current:
            accept = False
            while not accept:
                optry = raw_input("\nEnter a hex string (ctrl+c to exit):\n ")
                add(optry)
                lastresult = current
                lasttry = optry
                ops.append(optry)
                print ""
                status()
                if sumbytes not in current:
                    accept = query_yes_no("\nKeep new value? :", default="no")
                if not accept:
                    ops.pop()
                    current = hex(int(current, 16) - int(lasttry, 16))
                    status()

        #When done calculating (or after keyboard interrupt) save progress in results dict
        results[targetbytes] = ops

        #clear ops
        ops = []

    except KeyboardInterrupt:
        print ""
        print ""
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
    global verbose

    parser = argparse.ArgumentParser(description="Hex Calculation")
    parser.add_argument("-v",
                        "--verbose",
                        help="print verbose log (everything in response)",
                        action="store_true")
    parser.add_argument("-f",
                        "--infile",
                        required=True,
                        help="Path to file with binary strings - 4 bytes per line ('\x75\xe7\x3f\x34')")
    parser.add_argument("-a",
                        "--charfile",
                        help="Path to file with list of allowed characters in format '\x75' ")
    args = parser.parse_args()

    if args.verbose: verbose = args.verbose

    try:
        f = open(args.infile, 'r')
    except:
        print "Error reading input file " + args.infile + ". Exiting.."
        sys.exit(1)

    for line in f.readlines():
        calc(line)

    printResults()

if __name__ == '__main__':
        main()