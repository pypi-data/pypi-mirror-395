##
# -*- coding: utf-8 -*-
#
# File:    GeneOntologyProvider.py
# Author:  J. Westbrook
# Date:    10-Dec-2019
# Version: 0.001
#
# Updates:
#   01-Jul-2024 dwp Adjust exportTreeNodeList method to return full node list by default unless input GO ID filter list is provided
#   29-Jul-2025 dwp Update test cache based on changes to GO data on 2025-07-22
#
##
"""
Various utilities for extracting data from the Gene Ontology OBO files
and returning lineage details.
"""

import logging
import os

import networkx
import obonet

from rcsb.utils.io.FileUtil import FileUtil

logger = logging.getLogger(__name__)


class GeneOntologyProvider(object):
    """Various utilities for extracting data from the Gene Ontology OBO files
        and returning lineage details.
    """

    def __init__(self, **kwargs):
        # Alternate: http://purl.obolibrary.org/obo/go.obo
        urlTarget = kwargs.get("urlTarget", "http://purl.obolibrary.org/obo/go/go-basic.obo")
        # go-basic.obo is guaranteed to be acyclic
        # urlTarget = kwargs.get("urlTarget", "http://purl.obolibrary.org/obo/go.obo")
        goDirPath = kwargs.get("goDirPath", ".")
        useCache = kwargs.get("useCache", True)
        self.__goGraph = self.__reload(urlTarget, goDirPath, useCache=useCache)

    def testCache(self):
        if self.__goGraph:
            logger.info("Reading %d nodes and %d edges", len(self.__goGraph), self.__goGraph.number_of_edges())
            # Numbers may change as some terms become obsolete in future GO updates.
            # See http://geneontology.org/stats.html
            # and http://current.geneontology.org/release_stats/go-stats-summary.json
            if networkx.is_directed_acyclic_graph(self.__goGraph) and len(self.__goGraph) > 39000:
                return True
        return False

    def exists(self, goId):
        try:
            return goId in self.__goGraph
        except Exception:
            return False

    def getNode(self, goId):
        try:
            return self.__goGraph[goId]
        except Exception:
            pass
        return None

    def getRootNodes(self):
        try:
            rootL = [n for n, d in self.__goGraph.out_degree() if d == 0]
            return rootL
        except Exception:
            pass
        return None

    def getName(self, goId):
        try:
            return self.__goGraph.nodes[goId]["name"]
        except Exception as e:
            logger.debug("Failing %r with %r", goId, str(e))
        return None

    def getAdjacentParents(self, goId):
        rL = []
        try:
            for child, parent, key in self.__goGraph.out_edges(goId, keys=True):
                logger.debug("%r %r - %r -> %r %r", child, self.getName(child), key, parent, self.getName(parent))
                rL.append((child, parent, key))
        except Exception:
            pass
        return rL

    def getPredecessors(self, goId):
        rL = []
        try:
            rL = [nd for nd in self.__goGraph.predecessors(goId)]
        except Exception:
            pass
        return rL

    def getSuccessors(self, goId):
        rL = []
        try:
            rL = [nd for nd in self.__goGraph.successors(goId)]
        except Exception:
            pass
        return rL

    def getDescendants(self, goId, includeSelf=True):
        """
        Args:
            goId (str): GO ID for which to get descendants.
            includeSelf (bool, optional): include input and parent nodes. Defaults to True.
        """

        linL = []
        try:
            if includeSelf:
                linL.append((goId, self.getName(goId)))
            for nd in networkx.descendants(self.__goGraph, goId):
                logger.debug("%r %r --> %r %r", goId, self.getName(goId), nd, self.getName(nd))
                linL.append((nd, self.getName(nd)))
        except Exception as e:
            logger.debug("Failing %s with %s", goId, str(e))
        return linL

    def getUniqueDescendants(self, goIdL, includeSelf=True):
        linL = []
        try:
            ndS = set()
            for goId in goIdL:
                if includeSelf:
                    ndS.add(goId)
                for nd in networkx.descendants(self.__goGraph, goId):
                    ndS.add(nd)
            #
            for nd in sorted(ndS):
                linL.append((nd, self.getName(nd)))
        except Exception as e:
            logger.debug("Failing %s with %s", goId, str(e))
        return linL

    def getFullNodeList(self):
        try:
            return list(self.__goGraph.nodes)
        except Exception as e:
            logger.debug("Failing with %r", str(e))
        return None

    def exportTreeNodeList(self, filterL=None):
        """ For the input node list export full tree node list including parent nodes

        Args:
            filterL (list): list of covered GO id lists

        Returns:
            list: [{'id': <> 'name': <name> 'parents': [<id>,<id>,...]}]
        """
        trL = []
        try:
            goIdL = self.getFullNodeList()
            logger.info("Full GO ID list length %d", len(goIdL))
            if filterL:
                goIdL = [gId for gId in goIdL if gId in filterL]
            logger.info("Filtered GO ID list length %d", len(goIdL))

            # Generate the full list of nodes and parents -
            ndS = set()
            for goId in goIdL:
                if not self.exists(goId):
                    logger.warning("%s not in current ontology", goId)
                    continue
                ndS.add(goId)
                for nd in networkx.descendants(self.__goGraph, goId):
                    ndS.add(nd)
            #
            for nd in ndS:
                # tupL = [(child, parent, key)]
                pIdL = [tup[1] for tup in self.getAdjacentParents(nd)]
                if not pIdL:
                    logger.info("Node %s (%s) has no parents", nd, self.getName(nd))
                    trL.append({"id": nd, "name": self.getName(nd)})
                else:
                    trL.append({"id": nd, "name": self.getName(nd), "parents": pIdL})

        except Exception as e:
            logger.exception("Failing with %s", str(e))
        return trL

    def __reload(self, urlTarget, dirPath, useCache=True):
        """ Reload input GO OBO ontology file and return a nx graph object.
'
        Returns:
            dictionary[goId] = {'name_list': ... , 'id_list': ... 'depth_list': ... }
        """
        goGraph = None
        #
        # mU = MarshalUtil()
        fU = FileUtil()
        fn = fU.getFileName(urlTarget)
        oboFilePath = os.path.join(dirPath, fn)
        fU.mkdir(dirPath)
        #
        if not useCache:
            for fp in [oboFilePath]:
                try:
                    os.remove(fp)
                except Exception:
                    pass
        #
        if useCache and fU.exists(oboFilePath):
            goGraph = obonet.read_obo(oboFilePath)
        else:
            logger.info("Fetching url %s to resource file %s", urlTarget, oboFilePath)
            ok = fU.get(urlTarget, oboFilePath)
            if ok:
                goGraph = obonet.read_obo(oboFilePath)
        if goGraph:
            logger.info("Reading %d nodes and %d edges", len(goGraph), goGraph.number_of_edges())
        else:
            logger.info("Go graph construction failing")
        #
        return goGraph
