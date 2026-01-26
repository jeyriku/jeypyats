#!/Users/jeremierouzet/Documents/Dev/pyats/pyats-jeyws01/bin/python
# -*- coding:utf-8 -*-
########################################################################################################################
#
# File: xrd_interface_parser.py
# This file is a part of Netalps.fr
#
# Created: 2025/06/25 13:41:04
# Author: Jeremie Rouzet
#
# Last Modified: 26.01.2026 13:53:56
# Modified By: Jeremie Rouzet
#
# Copyright (c) 2025 Netalps.fr
########################################################################################################################

__author__ = ["Jeremie Rouzet"]
__contact__ = 'jeremie.rouzet@netalps.fr'
__copyright__ = 'Netalps, 2026'
__license__ = "Netalps, Copyright 2026. All rights reserved."

'''
Parser for retrieving interface status via Netconf using OpenConfig YANG models.
'''

import xmltodict
from genie.utils import Dq
from lxml import etree
from utils import sanitize_xml
from rpc_msgs import BASE_RPC
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

parser = etree.XMLParser()
parser.set_element_class_lookup(
    etree.ElementDefaultClassLookup(element=etree.ElementBase)
)


def get_interface_status(self):
    """
    Récupère le statut des interfaces via NETCONF.

    Utilise un filtre subtree correct avec la méthode dispatch.
    """
    xml_rpc = """
      <interfaces xmlns="http://openconfig.net/yang/interfaces">
        <interface>
          <state>
            <name/>
            <oper-status/>
          </state>
        </interface>
      </interfaces>
    """

    parser = etree.XMLParser(remove_blank_text=True)

    # Construction du filtre subtree avec le XML demandé
    filter_xml = f"""
      <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" type="subtree">
        {xml_rpc}
      </filter>
    """

    filter_element = etree.fromstring(filter_xml, parser)

    # Création de l'élément <get> et ajout du filtre
    get_element = etree.Element("{urn:ietf:params:xml:ns:netconf:base:1.0}get")
    get_element.append(filter_element)

    logger.info(f"Envoi de la requête NETCONF:\n{etree.tostring(get_element, pretty_print=True).decode()}")

    # Envoi de la requête via dispatch (recommandé pour éléments XML personnalisés)
    reply = self.dispatch(get_element)

    logger.info(f"Réponse reçue: {reply.xml}")

    # Parsing de la réponse
    reply_dict = xmltodict.parse(reply.xml)

    if not reply.ok or not reply_dict.get("rpc-reply", {}).get("data"):
        return []

    interfaces = Dq(reply_dict).get_values("interface")
    results = []
    for intf in interfaces:
        state = intf.get("state", {})
        results.append({
            "name": state.get("name"),
            "oper-status": state.get("oper-status")
        })
    return results
