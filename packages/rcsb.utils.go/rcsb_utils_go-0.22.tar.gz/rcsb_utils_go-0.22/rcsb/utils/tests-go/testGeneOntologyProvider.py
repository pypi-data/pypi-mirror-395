##
# File:    testGeneOntologyProvider.py
# Author:  J. Westbrook
# Date:    10-Dec-2019
# Version: 0.001
#
# Updates:
#   29-Jul-2025 dwp Update tests based on changes to GO data on 2025-07-22
#
##
"""
Tests for various utilities for extracting data from Gene Ontology OBO export files

"""

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2.0"

import logging
import os
import unittest

from rcsb.utils.go.GeneOntologyProvider import GeneOntologyProvider

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]-%(module)s.%(funcName)s: %(message)s")
logger = logging.getLogger()


class GeneOntologyProviderTests(unittest.TestCase):
    def setUp(self):
        self.__workPath = os.path.join(HERE, "test-output")

    def tearDown(self):
        pass

    def testReloadGeneOntology(self):
        """Test load from source"""
        try:
            goP = GeneOntologyProvider(goDirPath=self.__workPath, useCache=False)
            ok = goP.testCache()
            self.assertTrue(ok)
            #
            goId = "GO:2001317"
            ok = goP.exists(goId)
            self.assertTrue(ok)
            nm = goP.getName(goId)
            logger.debug("name %r", nm)
            self.assertEqual(nm, "kojic acid biosynthetic process")

            #
            rL = goP.getRootNodes()
            logger.info("root nodes %d", len(rL))
            self.assertEqual(len(rL), 3)

            #
            # These numbers may change as some terms become obsolete
            # in future GO updates.
            # See http://geneontology.org/stats.html and https://github.com/geneontology/go-announcements
            goIdL = [("GO:0023052", 1), ("GO:0051179", 1), ("GO:0033036", 2), ("GO:1990747", 26)]
            for goId, numParents in goIdL:
                print(goId)
                nm = goP.getName(goId)
                self.assertIsNotNone(nm)
                nL = goP.getAdjacentParents(goId)
                self.assertIsNotNone(nL)
                nL = goP.getPredecessors(goId)
                self.assertIsNotNone(nL)
                nL = goP.getSuccessors(goId)
                self.assertIsNotNone(nL)
                linL = goP.getDescendants(goId, includeSelf=False)
                self.assertGreaterEqual(len(linL), numParents)
                logger.info("%a Lineage(%d) %r", goId, len(linL), linL)

            # Test getting tree node list with input GO ID list
            gIdL = [tup[0] for tup in goIdL]
            trL = goP.exportTreeNodeList(filterL=gIdL)
            logger.debug("trL %r", trL)
            logger.info("Length of filtered tree node list %d", len(trL))
            self.assertGreaterEqual(len(trL), 28)

            # Test getting full tree node list (without input GO ID list)
            gIdL = [tup[0] for tup in goIdL]
            trL = goP.exportTreeNodeList()
            logger.debug("trL %r", trL)
            logger.info("Length of full tree node list %d", len(trL))
            self.assertGreaterEqual(len(trL), 30000)

        except Exception as e:
            logger.exception("Failing with %s", str(e))
            self.fail()


def readGeneOntology():
    suiteSelect = unittest.TestSuite()
    suiteSelect.addTest(GeneOntologyProviderTests("testReloadGeneOntology"))
    return suiteSelect


if __name__ == "__main__":
    mySuite = readGeneOntology()
    unittest.TextTestRunner(verbosity=2).run(mySuite)
