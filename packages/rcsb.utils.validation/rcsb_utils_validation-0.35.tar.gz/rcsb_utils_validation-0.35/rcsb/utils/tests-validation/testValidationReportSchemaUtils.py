##
# File:    ValidationReportSchemaUtilsTests.py
# Author:  J. Westbrook
# Date:    3-Feb-2019
# Version: 0.001
#
# Update:
#  1-Jun-2020 jdw Updated to V4 schema consolidate static (required  by V4) and dynamic definitions.
#
##
"""
Tests for wwPDB validation schema to dictionary translation tools.
"""

__docformat__ = "google en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"

import logging
import os
import unittest

from rcsb.utils.io.MarshalUtil import MarshalUtil
from rcsb.utils.validation.ValidationReportSchemaUtils import ValidationReportSchemaUtils

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()


class ValidationReportSchemaUtilsTests(unittest.TestCase):
    def setUp(self):
        self.__dirPath = os.path.join(os.path.dirname(TOPDIR), "rcsb", "mock-data")
        self.__xsdPath = os.path.join(HERE, "test-data", "wwpdb_validation_v004.xsd")
        self.__dictPath = os.path.join(HERE, "test-output", "vrpt_mmcif_ext_v4.dic")
        self.__dictStaticPath = os.path.join(HERE, "test-data", "em_validation_ext_v4.dic")
        #
        # This schema mapping file is used by the XML report data file reader.
        self.__dictionaryMapPath = os.path.join(HERE, "test-output", "vrpt_dictmap_v4.json")
        self.__dictionaryMapCsvPath = os.path.join(HERE, "test-output", "vrpt_dictmap_v4.csv")
        self.__mU = MarshalUtil()

    def tearDown(self):
        pass

    def testProcessXsdSchema(self):
        vrsu = ValidationReportSchemaUtils()
        sObj = vrsu.readSchema(self.__xsdPath, verbose=False)
        logger.debug("Returns type %r", type(sObj))
        logger.debug("Schema category length %d", len(sObj))
        ok = self.__mU.doExport(os.path.join(HERE, "test-output", "schema-object.json"), sObj, fmt="json", indent=3)

        # import static definitions -
        scL = self.__mU.doImport(self.__dictStaticPath, fmt="mmcif-dict")
        logger.info("Static definition count %d", len(scL))
        #
        cL = vrsu.buildDictionary(sObj)
        logger.info("Generated definition count %d", len(cL))
        #
        cL.extend(scL)
        ok = self.__mU.doExport(self.__dictPath, cL, fmt="mmcif-dict")
        self.assertTrue(ok)
        #
        dictionaryMap = vrsu.getDictionaryMap(sObj)
        ok = self.__mU.doExport(self.__dictionaryMapPath, dictionaryMap, fmt="json")
        self.assertTrue(ok)
        #
        self.assertTrue("attributes" in dictionaryMap)
        self.assertTrue(len(dictionaryMap["attributes"]) > 420)

    def testExportMapping(self):
        """Export schema correspondences as CSV."""
        vrsu = ValidationReportSchemaUtils()
        sObj = vrsu.readSchema(self.__xsdPath)
        dictionaryMap = vrsu.getDictionaryMap(sObj)
        logger.info("Attribute count %d", len(dictionaryMap["attributes"]))
        rL = []
        for ky, dD in dictionaryMap["attributes"].items():
            kyL = ky.split("|")
            catN = kyL[0]
            atN = kyL[1]
            row = {"xml_el": catN, "xml_at": atN, "mmcif_cat": dD["cat"], "mmcif_at": dD["at"]}
            rL.append(row)
        #
        #
        self.__mU.doExport(self.__dictionaryMapCsvPath, rL, fmt="csv")
        # def __serializeCsv(self, filePath, rowDictList, fieldNames=None, **kwargs):{}


def readValidationSchema():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ValidationReportSchemaUtilsTests("testProcessXsdSchema"))
    return suiteSelect


def exportMapping():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(ValidationReportSchemaUtilsTests("testExportMapping"))
    return suiteSelect


if __name__ == "__main__":

    mySuite = readValidationSchema()
    unittest.TextTestRunner(verbosity=2).run(mySuite)

    mySuite = exportMapping()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
