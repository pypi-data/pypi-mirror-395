##
# File:    MultiProcPoolUtilTests.py
# Author:  jdw
# Date:    17-Nov-2018
#
# Updates:
#
##
"""

"""

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"

import logging
import random
import re
import sys
import unittest

from rcsb.utils.multiproc.MultiProcPoolUtil import MultiProcPoolUtil

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class StringTests(object):
    """A skeleton class that implements the interface expected by the multiprocessing
    utility module --

    """

    def __init__(self, **kwargs):
        pass

    def reverser(self, dataList, procName, optionsD, workingDir):
        """Lexically reverse the characters in the input strings.
        Flag strings with numerals as errors.

        Read input list and perform require operation and return list of
        inputs with successful outcomes.
        """
        _ = optionsD
        _ = workingDir
        successList = []
        retList1 = []
        retList2 = []
        diagList = []
        skipped = 0
        logger.debug("%s dataList %r", procName, dataList)
        for tS in dataList:
            if re.search("[8-9]", tS):
                # logger.info("skipped %r", tS)
                skipped += 1
                continue
            rS1 = tS[::-1]
            rS2 = rS1 + tS
            sumC = 0
            for s1 in tS:
                sumC += ord(s1) - ord(s1)
            diag = len(rS2)
            successList.append(tS)
            retList1.append(rS1)
            retList2.append(rS2)
            diagList.append(diag)

        logger.debug("%s skipped %d dataList length %d successList length %d", procName, skipped, len(dataList), len(successList))
        #
        return successList, retList1, retList2, diagList


class MultiProcPoolUtilTests(unittest.TestCase):
    def setUp(self):
        self.__verbose = True

    def tearDown(self):
        """"""

    @unittest.skipIf(sys.version_info[0] < 3, "not supported in this python version")
    def testMultiProcString(self):
        """"""

        try:
            sCount = 1000
            dataList = []
            for _ in range(sCount):
                sLength = random.randint(100, 30000)
                dataList.append("".join(["9"] * sLength))
                dataList.append("".join(["b"] * sLength))
            #
            # logger.info("Length starting list is %d", len(dataList))

            sTest = StringTests()

            mpu = MultiProcPoolUtil(verbose=True)
            mpu.set(workerObj=sTest, workerMethod="reverser")
            # 8 - proc 236 chunk 10  pool chunk 5
            # 8 - proc 252 chunk 100 pool chunk 5
            # 8 - proc 247 chunk 10 pool chunk 2

            ok, failList, resultList, _ = mpu.runMulti(dataList=dataList, numProc=4, numResults=2, chunkSize=10)
            #
            logger.info("Returns: %r unique failures %d first result length %d second result length %d", ok, len(failList), len(resultList[0]), len(resultList[1]))
            # self.assertEqual(len(failList), sCount)

            self.assertGreaterEqual(len(failList), 1)
            self.assertEqual(sCount, len(resultList[0]))
            self.assertEqual(sCount, len(resultList[1]))
            self.assertFalse(ok)

        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()

    @unittest.skipIf(sys.version_info[0] < 3, "not supported in this python version")
    def testMultiProcStringAsync(self):
        """"""

        try:
            sCount = 10000
            dataList = []
            for _ in range(sCount):
                sLength = random.randint(100, 30000)
                dataList.append("".join(["9"] * sLength))
                dataList.append("".join(["b"] * sLength))
            #
            # logger.info("Length starting list is %d", len(dataList))

            sTest = StringTests()

            mpu = MultiProcPoolUtil(verbose=True)
            mpu.set(workerObj=sTest, workerMethod="reverser")
            # SCount 300 000
            # 8 - proc 232s chunk 10  pool chunk 5
            # 8 - proc chunk 100 pool chunk 5
            # 8 - proc chunk 10 pool chunk 2

            ok, failList, resultList, _ = mpu.runMultiAsync(dataList=dataList, numProc=4, numResults=2, chunkSize=10)
            #
            logger.info("Returns: %r unique failures %d first result length %d second result length %d", ok, len(failList), len(resultList[0]), len(resultList[1]))
            # self.assertEqual(len(failList), sCount)

            self.assertGreaterEqual(len(failList), 1)
            self.assertEqual(sCount, len(resultList[0]))
            self.assertEqual(sCount, len(resultList[1]))
            self.assertFalse(ok)

        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()


def suiteMultiProcPoolSync():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(MultiProcPoolUtilTests("testMultiProcString"))
    suiteSelect.addTest(MultiProcPoolUtilTests("testMultiProcStringAsync"))
    return suiteSelect


if __name__ == "__main__":

    mySuite1 = suiteMultiProcPoolSync()
    unittest.TextTestRunner(verbosity=2).run(mySuite1)
