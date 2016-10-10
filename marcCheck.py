from pymarc import *
import csv
import urllib.parse
import urllib.request
import tkinter
import random
import time, datetime

root = tkinter.Tk()
root.withdraw()

def checkOCLC(OCN):
    url = 'https://worldcat.org/bib/data/'
    OCN = OCN
    WSKey = '82ncAiwFiOeGe4tgpYjzEGCadrF04kzRnWhjFfJNuM4kHObLQBoSmlc5LVducOo8GbWrj9iYDSYiZABM'
    Secret = 'UTXUhpIZ9iG612Py81lPMA=='
    timeStamp = getTime()
    nonce = generate_nonce()
    principleID = 'urn:oclc:wms:da'


def generate_nonce(length=8):
    """Generate pseudorandom number."""
    return ''.join([str(random.randint(0, 9)) for i in range(length)])

def getTime():
    d = datetime.datetime.now()
    return d


def marcCheck(ft='0', debug=0):
    """Runs a number of error checks on a MARC record set based on article:
    http://go.galegroup.com/ps/i.do?p=ITOF&u=gale15691&id=GALE|A345172851&v=2.1&it=r&sid=summon&userGroup=gale15691&authCount=1"""

    # marcFile = 'c:\\users\\fenichele\downloads\\Kanopy_MARC_Records__film-movement-pda-package.mrc'
    from tkinter import filedialog

    input("\npress any key to choose the MARC File to review\n")
    marcPath = tkinter.filedialog.askopenfile()
    marcFile = marcPath.name
    print("thanks, running...\n")

    recordCounter = 0
    with open(marcFile, 'rb') as fh:
        reader = MARCReader(fh, to_unicode=True, force_utf8=True)

        for record in reader:
            # record.force_utf8 = True

            # record = record.as_marc()
            # record = record.decode('utf-8')
            recordCounter += 1
            if debug == 1:
                if ft == '0':
                    print('Format is eBooks')
                elif ft == '1':
                    print('Format is streaming videos')
                print('Record '+str(recordCounter)+':')
            # record.force_utf8 = True

            # record = record.as_marc()
            # record = record.decode('utf-8')
            # return marc

            # test0, get the MARC 001 to confirm a unique identifier

            recID = record['001'].value()
            if recID is None:
                print("\tERROR: "+str(recordCounter)+': No Record ID (MARC 001) Found")')
            if debug == 1:
                print('\tMARC 001: '+str(recID))

            setID = record['003'].value()
            if recID is None:
                print("\tERROR: " + str(recordCounter) + ': No Set ID (MARC 001) Found")')
            if debug == 1:
                print('\tMARC 003: '+str(setID))

            # print LDR for review purposes only
            # if debug == 1:
            #     print('\tLDR: '+str(record.leader))

            # test 1, if ft = 0, LDRType = LDR 06/07 should equal "m", if ft = 1 LDRType should equal "g"
            LDRType = str(record.leader[6:7]).replace(" ", "#")
            if debug == 1:
                print('\tLDR/ 06-07, Type = '+str(LDRType))
            if ft == '0':
                if LDRType != 'm':
                    print("\tERROR (test 1): "+str(recordCounter)+":\tLDR 06/07 should be 'm' but is: "+LDRType)
            elif ft == '1':
                if LDRType != 'g':
                    print("\tERROR (test 1): "+str(recordCounter)+":\tLDR 06/07 should be 'g' but is: "+LDRType)

            # test 1a, verify form of record and that the BLvL makes sense
            LDRBLvL = str(record.leader[7:8]).replace(" ", "#")
            recordFormat = 'x'
            if debug == 1:
                print('\tLDR/ 07-08, BLvL = ' + str(LDRBLvL))
            if LDRType == 'm':
                if LDRBLvL not in('a', 'b', 'c', 'd', 'i', 'm', 's'):
                    print("\tERROR (test 1a): ") + str(recordCounter) + ':\tLDR Type is ' + str(LDRType) + \
                    'LDR 07/08, BLvL, should be one of the following: (a, b, c, d, i, m, s) but is: ' + str(LDRBLvL)
                else:
                    recordFormat = 'COM'
            elif LDRType in ('g', 'k', 'o', 'r'):
                if LDRBLvL not in('a', 'b', 'c', 'd', 'i', 'm', 's'):
                    print("\tERROR (test 1a): ") + str(recordCounter) + ':\tLDR Type is ' + str(LDRType) + \
                    'LDR 07/08, BLvL, should be one of the following: (a, b, c, d, i, m, s) but is: ' + str(LDRBLvL)
                else:
                    recordFormat = 'VIS'
            if debug == 1:
                print('\tRecord Format is: ' + recordFormat)

            if ft == '0':
                if LDRType != 'm':
                    print(
                        "\tERROR (test 1): " + str(recordCounter) + ":\tLDR 06/07 should be 'm' but is: " + LDRType)
            elif ft == '1':
                if LDRType != 'g':
                    print(
                        "\tERROR (test 1): " + str(recordCounter) + ":\tLDR 06/07 should be 'g' but is: " + LDRType)

            # test 2, LDR17 = LDR 17
            LDR17 = str(record.leader[17]).replace(" ", "#")
            if debug == 1:
                print('\tLDR/ 17 = ' + str(LDR17))

            # test 3 if ft = 0, MARC 006/00 = m, Additional Material Characteristics, if ft = 1, MARC 006/00 = v
            marc006 = record['006'].value()[0:1].replace(" ", "#")
            if debug == 1:
                print('\t006/ 00 = '+str(marc006))
            if marc006 != 'm':
                print("\tERROR: "+str(recordCounter)+":\tMARC 006/00 should be 'm' but it is: "+str(marc006))

            # test 4 if ft = 0, MARC 006/09 = d, if ft = 1, MARC 006/09 = c, Additional Material Characteristics
            marc00609 = record['006'].value()[9:10].replace(" ", "#")
            if debug == 1:
                print('\t006/ 09 = ' + str(marc00609))
            if ft == '0':
                if str(marc00609) != 'd':
                    print("\tERROR (test 4): " + str(recordCounter) + ":\tMARC 006/09 (should be 'd') = "
                          + str(marc00609))
            elif ft == '1':
                if str(marc00609) != 'c':
                    print("\tERROR (test 4): " + str(recordCounter) + ":\tMARC 006/09 (should be 'c') = " +
                          str(marc00609))

            # Get the MARC 007 fields for further testing

            marc007s = record.get_fields('007')

            stop007 = 'n'
            # stop007 = input ('see marc007? press "y"')
            if stop007 == 'y':
                return marc007s

            for field7 in marc007s:
                if debug == 1:
                    print('\tMARC 007: ' + str(field7.value()))

                # test 5 if ft = 0, MARC 007/00 = c, if ft = 1, MARC 007/00 either c or v, physical characteristics
                marc007 = field7.value()[0:1].replace(" ", "#")
                marc007ft1List = ['c', 'v']
                if debug == 1:
                    print('\t007/ 00 = ' + str(marc007))
                if ft == '0':
                    if str(marc007) != 'c':
                        print("\tERROR (test 5): " + str(recordCounter) + ":\tMARC 007/00 (should be 'c') = "
                              + str(marc007))
                elif ft == '1':
                    if str(marc007) not in marc007ft1List:
                        print("\tERROR (test 5): " + str(recordCounter) + ":\tMARC 007/00 (should be 'c' or 'v') = " +
                              str(marc007))

                # test 6 if ft = 0, MARC 007/01 = r,
                # if ft = 1 and marc007 = v, MARC 007/01 = z, physical characteristics
                marc00701 = field7.value()[1:2].replace(" ", "#")
                if debug == 1:
                    print('\t007/ 01 = ' + str(marc00701))
                    # print("MARC 007: " + str(record['007'].value()))
                if ft == '0':
                    if str(marc00701) != 'r':
                        print("\tERROR (test 6, ft 0): " + str(recordCounter) + ":\tMARC 007/01 (should be 'r') = " +
                              str(marc00701))
                elif ft == '1':
                    if marc007 == 'v' and str(marc00701) != 'z':
                        print("\tERROR (test 6, ft 0, 007/00 v): " + str(recordCounter) +
                              ":\tMARC 006/09 (should be 'z' when 007\00 = 'v') = " + str(marc00701))
                    elif marc007 != 'v' and str(marc00701) != 'r':
                        print("\tERROR (test 6, ft 0, 007 not v): " + str(recordCounter) +
                              ":\tMARC 007/01 (should be 'r') = " +
                              str(marc00701))

                # test 6a, if ft = 1, MARC 007/05 = a
                marc00705 = field7.value()[5:6].replace(" ", "#")
                if debug == 1:
                    print('\t007/ 05 = ' + str(marc00705))
                if ft == '1' and marc00705 != 'a':
                    print("\tError (test 6a): " + str(recordCounter) + ':\tMARC 007/05 (should be "a") = ' +
                          str(marc00705))

            # test RDA - determine if the record is an RDA record, should have LDR 18 either 'i' or 'c' and
            # MARC 040 subfield e = 'rda'

            recRDA = False
            LDRDesc = str(record.leader[18]).replace(" ", "#")
            marc040e = record['040']['e']
            if LDRDesc in ('i', 'c') and marc040e == 'rda':
                recRDA = True

            if debug == 1:
                print('\tTesting for RDA status, LDR 18: ' + LDRDesc + ', marc040$e: "' + marc040e + '", RDA?: '
                      + str(recRDA))

            # ABOVE ARE THE EASY CHECKS --- BELOW ARE THE MORE COMPLICATED CHECKS

            # test 7 00806-14 Check date(s) against 264 $c
            marc008date1 = record['008'].value()[7:11].replace(" ", "#")
            marc008date2 = record['008'].value()[11:15].replace(" ", "#")
            # get the MARC 264$c for comparison but strip the punctuation and any "c"
            try:
                marc264c = record['264']['c'].replace(".", "").replace("c", "")
            except TypeError:
                marc264c = '####'

            if debug == 1:
                print('\t008/ 06-10 = ' + str(marc008date1))
                print('\t008/ 10-14 = ' + str(marc008date2))
                print('\tMARC 264 $c = ' + str(marc264c))

            marc264ctest = marc264c.replace('[', '').replace(']', '')

            # test 7a - MARC 264 is RDA Core - if the record is RDA and MARC 264 is none report a warning
            if recRDA and record['264'] is None:
                print('\tWARNING (test 7a): ' + str(recordCounter) + '\tis RDA and has no MARC 264')

            # test 7b - checks the dates only if the 264 actually exists
            elif marc008date1 != marc264ctest and marc008date2 != marc264ctest and recRDA:
                print('\tWARNING (test 7b): ' + str(recordCounter)
                      + '\tMARC 008 / 06-14 (should match MARC 264$c when record is RDA) = '
                      + str(marc008date1) + ', ' + str(marc008date2)+'/ MARC 264$c (test) = ' + str(marc264ctest))

            # test 8 MARC 008/15-17 Check place of publication against 264$a -- SPOT ONLY
            # there doesn't seem to be a preprocessing way to do this comparison since the MARC 264 $a
            # won't include the country and could refer to multiple locations
            marc008PubPlace = record['008'].value()[15:18]
            # get the MARC 264$a for comparison but strip the punctuation and any "c"
            try:
                marc264a = record['264']['a']
            except TypeError:
                marc264a = '*no location given*'

            if debug == 1:
                print('\t008/ 15-17 = ' + str(marc008PubPlace))
                print('\tMARC 264 $a  = ' + str(marc264a))

            # test 9 MARC Format should be "o" in the 008, depending on the record format
            # - either 23 for COM or 29 for VIS, also set the length for FORMAT for the benefit of printing
            marc008FormatLen = '??'
            if recordFormat == 'COM':
                marc008Format = record['008'].value()[23:24].replace(" ", "#")
                marc008FormatLen = '23'
            elif recordFormat == 'VIS':
                marc008Format = record['008'].value()[29:30].replace(" ", "#")
                marc008FormatLen = '29'

            if debug == 1:
                print('\t008 / ' + marc008FormatLen + ' (Form) = ' + str(marc008Format))

            if marc008Format != 'o':
                print('\tERROR: ' + str(recordCounter) + '\tMARC 008 / ' + marc008FormatLen +
                      '  (should be "o" = '+str(marc008Format))

            # test 10 MARC 008 28 - Is it a government document?

            marc00828 = record['008'].value()[28:29].replace(" ", '#')
            if marc00828 is not None and marc00828 != "#":
                print('\tWARNING: ' + str(recordCounter) +
                      '\t MARC 008 / 28 is not blank, indicating a gov doc. Value is ' +
                      str(marc00828))

            # test 11 MARC 024 - Check for DOIs

            try:
                marc024 = record['024'].value().replace(" ", "#")
            except (AttributeError, TypeError):
                marc024 = None

            if marc024 is not None:
                print('\tWARNING: ' + str(recordCounter) + '\t Has a DOI in MARC 024 = ' + str(marc024))

            # test 12 MARC 035 - Checks for presence of OCLC Number - if exists - confirms electronic format

            try:
                marc035a = record['035']['a']
            except (AttributeError, TypeError):
                marc035a = None

            if marc035a is not None:
                # make a call to Worldcat API and check the data
                print('\tWARNING: ' + str(recordCounter) + '\t Has an OCN - is it electronic? = ' + str(marc035a))

            # Test 12 - Check for 050/060/082/086/090 - Report error if none exist

            callNumbers = []
            if record['050'] is not None:
                marc050 = record['050'].value()
                callNumbers.append(str(marc050))
            else:
                marc050 = "None"

            if record['060'] is not None:
                marc060 = record['060'].value()
                callNumbers.append(str(marc060))
            else:
                marc060 = "None"

            if record['082'] is not None:
                marc082 = record['082'].value()
                callNumbers.append(str(marc082))
            else:
                marc082 = "None"

            if record['086'] is not None:
                marc086 = record['086'].value()
                callNumbers.append(marc086)
            else:
                marc086 = "None"

            if record['090'] is not None:
                marc090 = record['090'].value()
                callNumbers.append(str(marc090))
            else:
                marc090 = "None"

            if len(callNumbers) == 0:
                print('\tWARNING (test 12): ' + str(recordCounter) + '\t Has No MARC 050/060/082/086/090')
            else:
                if debug == 1:
                    print('\tMARC 050 = ' + marc050)
                    print('\tMARC 060 = ' + marc060)
                    print('\tMARC 082 = ' + marc082)
                    print('\tMARC 086 = ' + marc086)
                    print('\tMARC 090 = ' + marc090)

            # Test 13 - Check that MARC Fields are Not Used, fields 256, 506, 516, 530, 533, 534, 538 - only for books

            if recordFormat == 'COM':
                marc256 = record['256']
                if marc256 is not None:
                    print('\tERROR: ' + str(recordCounter) + '\tMARC 256 is present and should not be = ' + str(marc256))
                marc506 = record['506']
                if marc506 is not None:
                    print('\tERROR: ' + str(recordCounter) + '\tMARC 506 is present and should not be = ' + str(marc506))
                marc516 = record['516']
                if marc516 is not None:
                    print('\tERROR: ' + str(recordCounter) + '\tMARC 516 is present and should not be = ' + str(marc516))
                marc530 = record['530']
                if marc530 is not None:
                    print('\tERROR: ' + str(recordCounter) + '\tMARC 530 is present and should not be = ' + str(marc530))
                marc533 = record['533']
                if marc533 is not None:
                    print('\tERROR: ' + str(recordCounter) + '\tMARC 533 is present and should not be = ' + str(marc533))
                marc534 = record['534']
                if marc534 is not None:
                    print('\tERROR: ' + str(recordCounter) + '\tMARC 534 is present and should not be = ' + str(marc534))
                marc538 = record['538']
                if marc538 is not None:
                    print('\tERROR: ' + str(recordCounter) + '\tMARC 538 is present and should not be = ' + str(marc538))

            # Test 14 - MARC 300 should say "1 online resource" (Pagination optional)

            marc300a = record['300']['a']
            if marc300a is None:
                marc300a = "None"
            elif marc300a[:17].upper() != '1 ONLINE RESOURCE':
                print('\tERROR: ' + str(recordCounter) + '\tMARC 300a does not equal "1 online resource" = '
                      + str(marc300a))

            if debug == 1:
                print('\tMARC 300a = ' + marc300a)

            # Test 15 - If MARC 583 is present - should it be? When is preservation info applicable?

            try:
                marc583 = record['583'].value().replace(" ", "#")
            except (AttributeError, TypeError):
                marc583 = None

            if marc583 is not None:
                print('\tWARNING: ' + str(recordCounter) +
                      '\t Has MARC 583, is preservation information applicable? -  MARC 583 = ') + str(marc583)

            # breaker in the debug sequence
            if debug == 1:
                stopper = str(input("stop? press 0\n"))
                if stopper == '0':
                    print(0/0)

debug = '0'
debugQ = input("press 'd' to debug\n")

ft = str(input('select format: \nbooks = 0\nvideos = 1\n'))
if debugQ == 'd':
    marcCheck(str(ft), 1)
else:
    marcCheck(str(ft), 0)