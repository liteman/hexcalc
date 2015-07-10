======= PURPOSE =========== 

Disclaimer: This script is buggy and not very well commented. 

Which numbers do I have to subtract from 0x00000000 in order to hit my target value of 0xe7ffe775 ?

This script will help with the trial and error process. See sample output below.

An input file will specify which 4-byte sequences need to be encoded. This script will calculate a goal sum by subtracting the target value from 0xFFFFFFFF and adding 1

Goal = 0xFFFFFFFF - target + 1

You will then try to pick hex values that will add up to the goal. Once you've identified the values to hit your goal, the next target value to be encoded will be loaded.

The final output will be a summary of your calculations.


====== USAGE ===============

usage: hexcalc.py [-h] [-v] -f INFILE [-a CHARFILE]

Hex Calculation

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         print verbose log (everything in response)
  -f INFILE, --infile INFILE
                        Path to file with binary strings - 4 bytes per line
                        ('\x75\xe7\x3f\x34')
  -a CHARFILE, --charfile CHARFILE
                        Path to file with list of allowed characters in format
                        '\x75'


======== EXAMPLE ===========

./hexcalc.py -f egghunterbytes.txt -a allowed-chars.txt


====== SAMPLE OUTPUT ========

Bytes to encode: 0xfa8b5730

	Goal Sum: 0574a8d0
	Last:     00000000
	Current:  00000000

	Last try: 



Enter a hex string:
Format 0x00112233
(ctrl+c to move to next value or type 'back'):
0x02325270

Bytes to encode: 0xfa8b5730

	Goal Sum: 0574a8d0
	Last:     02325270
	Current:  02325270

	Last try: 0x02325270


Subtract 1 : 0x02325270

Enter a hex string:
Format 0x00112233
(ctrl+c to move to next value or type 'back'):
0x02314450

Bytes to encode: 0xfa8b5730

	Goal Sum: 0574a8d0
	Last:     046396c0
	Current:  046396c0

	Last try: 0x02314450


Subtract 1 : 0x02325270
Subtract 2 : 0x02314450

Enter a hex string:
Format 0x00112233
(ctrl+c to move to next value or type 'back'):
0x01111210

Bytes to encode: 0xfa8b5730

	Goal Sum: 0574a8d0   
	Last:     0574a8d0 
	Current:  0574a8d0 <-- Matches Goal

	Last try: 0x01111210


Subtract 1 : 0x02325270
Subtract 2 : 0x02314450
Subtract 3 : 0x01111210
Keep new value? : [y/N] 
 y


Final output: 
Target value: 0xfa8b5730
Subtract the following values:
	0x02325270
	0x02314450
	0x01111210



