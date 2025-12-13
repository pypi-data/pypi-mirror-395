#!/usr/bin/env python3

#
# NOSA HEADER START
#
# The contents of this file are subject to the terms of the NASA Open
# Source Agreement (NOSA), Version 1.3 only (the "Agreement").  You may
# not use this file except in compliance with the Agreement.
#
# You can obtain a copy of the agreement at
#   docs/NASA_Open_Source_Agreement_1.3.txt
# or
#   https://sscweb.gsfc.nasa.gov/WebServices/NASA_Open_Source_Agreement_1.3.txt.
#
# See the Agreement for the specific language governing permissions
# and limitations under the Agreement.
#
# When distributing Covered Code, include this NOSA HEADER in each
# file and include the Agreement file at
# docs/NASA_Open_Source_Agreement_1.3.txt.  If applicable, add the
# following below this NOSA HEADER, with the fields enclosed by
# brackets "[]" replaced with your own identifying information:
# Portions Copyright [yyyy] [name of copyright owner]
#
# NOSA HEADER END
#
# Copyright (c) 2020-2025 United States Government as represented by
# the National Aeronautics and Space Administration. No copyright is
# claimed in the United States under Title 17, U.S.Code. All Other
# Rights Reserved.
#

"""
Package for accessing the NASA's Satellite Situation Center (SSC) web
services https://sscweb.gsfc.nasa.gov/WebServices/REST/.

Copyright &copy; 2020-2025 United States Government as represented by the
National Aeronautics and Space Administration. No copyright is claimed in
the United States under Title 17, U.S.Code. All Other Rights Reserved.

Notes
-----
<ul>
  <li>Due to rate limiting implemented by the SSC web services, an
      attempt to make simultaneous requests from many threads is likely
      to actually reduce performance. At this time, it is best to make
      calls from five or fewer threads.</li>
  <li>This library does not currently implement the /graphs
      resources.  If there is interest in this, support could be added
      in the future.</li>
  <li>The core functionality is implemented in the `sscws.sscws`
      sub-module.  New users should start by viewing the `sscws.sscws`
      sub-module.</li>
</ul>
"""


__version__ = "2.4.6"


#
# Limit on the number of times an HTTP request which returns a
# 429 or 503 status with a Retry-After header will be retried.
#
RETRY_LIMIT = 100


#
# XML schema namespace
#
NS = 'http://sscweb.gsfc.nasa.gov/schema'
#
# Namespace for use in xml.etree.ElementTree.find*
#
ET_NS = '{' + NS + '}'
#
# XHTML schema namespace
#
XHTML_NS = 'http://www.w3.org/1999/xhtml'
#
# Namespace for use in xml.etree.ElementTree.find*
#
ET_XHTML_NS = '{' + XHTML_NS + '}'
#
# All namespaces found in responses.
#
NAMESPACES = {
    'ssc': NS,
    'xhtml': XHTML_NS
}
