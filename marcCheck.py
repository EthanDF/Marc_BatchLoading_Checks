from pymarc import *
import csv
import urllib.parse
import urllib.request


def checkOCLC(OCN):
    url = 'https://worldcat.org/bib/data/'
    OCN = OCN
    WSKey = '82ncAiwFiOeGe4tgpYjzEGCadrF04kzRnWhjFfJNuM4kHObLQBoSmlc5LVducOo8GbWrj9iYDSYiZABM'
    Secret = 'UTXUhpIZ9iG612Py81lPMA=='


def marcCheck(debug=0):
    """Runs a number of error checks on a MARC record set based on article:
    http://go.galegroup.com/ps/i.do?p=ITOF&u=gale15691&id=GALE|A345172851&v=2.1&it=r&sid=summon&userGroup=gale15691&authCount=1"""

    marcFile = 'MyMarcRecords.mrc'

    recordCounter = 0
    with open(marcFile, 'rb') as fh:
        reader = MARCReader(fh, to_unicode=True, force_utf8=True)

        for record in reader:
            recordCounter += 1
            if debug == 1:
                print('Record '+str(recordCounter)+':')
            record.force_utf8 = True

            marc = record.as_marc()
            marc = marc.decode('utf-8')
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

            # test 1, LDR07isM = LDR 06/07 should equal "m"
            LDR07isM = str(record.leader[7:8]).replace(" ", "#")
            if debug == 1:
                print('\tLDR/ 06-07 = '+str(LDR07isM))
            if LDR07isM != 'm':
                print("\tERROR: "+str(recordCounter)+":\t"+LDR07isM)

            # test 2, LDR17 = LDR 17
            LDR17 = str(record.leader[17]).replace(" ", "#")
            if debug == 1:
                print('\tLDR/ 17 = ' + str(LDR17))

            # test 3 MARC 006/00 = m, Additional Material Characteristics
            marc006 = record['006'].value()[0:1].replace(" ", "#")
            if debug == 1:
                print('\t006/ 00 = '+str(marc006))
            if marc006 != 'm':
                print("\tERROR: "+str(recordCounter)+":\tMARC 006/00 = "+str(marc006))

            # test 4 MARC 006/09 = d, Additional Material Characteristics
            marc00609 = record['006'].value()[9:10].replace(" ", "#")
            if debug == 1:
                print('\t006/ 09 = ' + str(marc00609))
            if str(marc00609) != 'd':
                print("\tERROR: " + str(recordCounter) + ":\tMARC 006/09 (should be 'd') = " + str(marc00609))

            # test 5 MARC 007/00 = c, physical characteristics
            marc007 = record['007'].value()[0:1].replace(" ", "#")
            if debug == 1:
                print('\t007/ 00 = ' + str(marc007))
            if str(marc007) != 'c':
                print("\tERROR: " + str(recordCounter) + ":\tMARC 006/09 (should be 'c') = " + str(marc007))

            # test 6 MARC 007/01 = r, physical characteristics
            marc00701 = record['007'].value()[1:2].replace(" ", "#")
            if debug == 1:
                print('\t007/ 01 = ' + str(marc00701))
            if str(marc00701) != 'r':
                print("\tERROR: " + str(recordCounter) + ":\tMARC 006/09 (should be 'r') = " + str(marc00701))

            # ABOVE ARE THE EASY CHECKS --- BELOW ARE THE MORE COMPLICATED CHECKS

            # test 7 00806-14 Check date(s) against 260 $c
            marc008date1 = record['008'].value()[7:11].replace(" ", "#")
            marc008date2 = record['008'].value()[11:15].replace(" ", "#")
            # get the MARC 260$c for comparison but strip the punctuation and any "c"
            try:
                marc260c = record['260']['c'].replace(".", "").replace("c", "")
            except TypeError:
                marc260c = '####'

            if debug == 1:
                print('\t008/ 06-10 = ' + str(marc008date1))
                print('\t008/ 10-14 = ' + str(marc008date2))
                print('\tMARC 260 $c = ' + str(marc260c))

            if marc008date1 != marc260c and marc008date2 != marc260c:
                print('\tERROR: ' + str(recordCounter) + '\tMARC 008 / 06-14 (should match MARC 260$c) = '
                      + str(marc008date1) + ', ' + str(marc008date2)+'/ MARC 260$c = ' + str(marc260c))

            # test 8 MARC 008/15-17 Check place of publication against 260$a -- SPOT ONLY
            # there doesn't seem to be a preprocessing way to do this comparison since the MARC 260 $a
            # won't include the country and could refer to multiple locations
            marc008PubPlace = record['008'].value()[15:18]
            # get the MARC 260$a for comparison but strip the punctuation and any "c"
            try:
                marc260a = record['260']['a']
            except TypeError:
                marc260a = '*no location given*'

            if debug == 1:
                print('\t008/ 15-17 = ' + str(marc008PubPlace))
                print('\tMARC 260 $a  = ' + str(marc260a))

            # test 9 MARC 008/23 Format should be "o" for electronic
            marc00823 = record['008'].value()[23:24].replace(" ", "#")

            if debug == 1:
                print('\t008 / 23 = ' + str(marc00823))

            if marc00823 != 'o':
                print('\tERROR: ' + str(recordCounter) + '\tMARC 008 / 23 (should be "o" = '+str(marc00823))

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
                print('\tWARNING: ' + str(recordCounter) + '\t Has No MARC 050/060/082/086/090')
            else:
                if debug == 1:
                    print('\tMARC 050 = ' + marc050)
                    print('\tMARC 060 = ' + marc060)
                    print('\tMARC 082 = ' + marc082)
                    print('\tMARC 086 = ' + marc086)
                    print('\tMARC 090 = ' + marc090)

            # Test 13 - Check that MARC Fields are Not Used, fields 256, 506, 516, 530, 533, 534, 538

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
if debugQ == 'd':
    marcCheck(1)
else:
    marcCheck()