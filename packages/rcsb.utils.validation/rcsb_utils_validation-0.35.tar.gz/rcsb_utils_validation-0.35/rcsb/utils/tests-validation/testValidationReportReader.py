##
# File:    ValidationReportReaderTests.py
# Author:  J. Westbrook
# Date:    3-Feb-2019
# Version: 0.001
#
# Update:
#   1-Jun-2020 jdw updated to V4 with EM extensions
#
##
"""
Tests for various utilities for extracting data from wwPDB validation
report data files.

"""

__docformat__ = "google en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"

import logging
import os
import unittest

from rcsb.utils.io.MarshalUtil import MarshalUtil
from rcsb.utils.validation.ValidationReportReader import ValidationReportReader

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()


class ValidationReportReaderTests(unittest.TestCase):
    def setUp(self):
        self.__mU = MarshalUtil()
        self.__dirPath = os.path.join(HERE, "test-data")
        self.__workPath = os.path.join(HERE, "test-output")
        self.__exampleFileXray = os.path.join(self.__dirPath, "3rer_validation.xml")
        self.__cifFileXray = os.path.join(self.__workPath, "3rer_validation.cif")
        #
        self.__exampleFileNmr = os.path.join(self.__dirPath, "6drg_validation.xml")
        self.__cifFileNmr = os.path.join(self.__workPath, "6drg_validation.cif")
        #
        self.__exampleFileEm = os.path.join(self.__dirPath, "5a32_validation.xml")
        self.__cifFileEm = os.path.join(self.__workPath, "5a32_validation.cif")
        #
        self.__dictionaryMapPath = os.path.join(HERE, "test-data", "vrpt_dictmap_v4.json")
        self.__dictionaryMap = self.__mU.doImport(self.__dictionaryMapPath, fmt="json")

    def tearDown(self):
        pass

    def testReadXrayValidationReport(self):
        vrr = ValidationReportReader(self.__dictionaryMap)
        xrt = self.__mU.doImport(self.__exampleFileXray, fmt="xml")
        cL = vrr.toCif(xrt)
        ok = self.__mU.doExport(self.__cifFileXray, cL, fmt="mmcif")
        self.assertTrue(ok)

    def testReadNmrValidationReport(self):
        vrr = ValidationReportReader(self.__dictionaryMap)
        xrt = self.__mU.doImport(self.__exampleFileNmr, fmt="xml")
        cL = vrr.toCif(xrt)
        ok = self.__mU.doExport(self.__cifFileNmr, cL, fmt="mmcif")
        self.assertTrue(ok)

    def testReadEmValidationReport(self):
        vrr = ValidationReportReader(self.__dictionaryMap)
        xrt = self.__mU.doImport(self.__exampleFileEm, fmt="xml")
        cL = vrr.toCif(xrt)
        ok = self.__mU.doExport(self.__cifFileEm, cL, fmt="mmcif")
        self.assertTrue(ok)


def readValidationReport():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ValidationReportReaderTests("testReadXrayValidationReport"))
    suiteSelect.addTest(ValidationReportReaderTests("testReadNmrValidationReport"))
    suiteSelect.addTest(ValidationReportReaderTests("testReadEmValidationReport"))
    return suiteSelect


if __name__ == "__main__":
    mySuite = readValidationReport()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
