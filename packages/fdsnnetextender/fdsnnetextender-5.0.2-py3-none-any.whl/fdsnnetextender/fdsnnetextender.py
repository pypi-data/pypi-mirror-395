import json
import logging
import re
from datetime import date, datetime
from functools import lru_cache
from urllib.error import URLError
from urllib.request import urlopen

HTTP_200_OK = 200
HTTP_204_NO_CONTENT = 204


class FdsnNetExtender:
    """
    Toolbox to manage the correspondance between a short network code
    and an extended network code.
    Correspondance is made using the metadata
    """

    def __init__(self, base_url="http://www.fdsn.org/ws/networks/1"):
        """
        param: base_url is the base url for getting metadata. Default is ws.
        """
        # we can guess that a network is temporary from this regex:
        logging.basicConfig()
        self.logger = logging.getLogger("fdsnnetextender")
        self.tempo_network_re = "^[0-9XYZ][0-9A-Z]$"
        self.base_url = base_url
        self.date_format = "%Y-%m-%d"

    def extend(self, net, date_string):
        """
        Param date_string can be a year or a date string like 2022-01-01
        """
        found = False
        extnet = net
        # Only extend temporary networks
        if re.match(self.tempo_network_re, net):
            # Normalize the start year from date_string
            try:
                # Can I cast it to an integer ? ie. is date_string just the year ?
                dateparam = date(year=int(date_string), month=1, day=1)
            except ValueError:
                self.logger.debug(
                    "Parameter %s is not a year. "
                    "Trying to guess the date in iso format",
                    date_string,
                )
                try:
                    dateparam = datetime.strptime(date_string, self.date_format).date()
                except ValueError as err:
                    msg = (
                        "date argument is not in format YYYY-MM-DD."
                        "Expected like 2022-01-01."
                    )
                    raise ValueError(msg) from err
            # Now that we have a start date :
            self.logger.debug("Trying to extend %s for %s", net, dateparam)
            # In order to make effective use of cache,
            # we always consider the first day of the year.
            # This should work except if a network code has been reused
            # in the same year. Is this possible ?
            try:
                networks = self._get_fdsn_network(net)
            except (URLError, ValueError):
                self.logger.exception("Unable to get network metadata from FDSN")
                raise
            for n in networks:
                self.logger.debug(net)
                if (
                    dateparam
                    >= datetime.strptime(n["start_date"], self.date_format).date()
                    and dateparam
                    <= datetime.strptime(n["end_date"], self.date_format).date()
                ):
                    extnet = n["fdsn_code"] + n["start_date"][0:4]
                    found = True
                    break
            if not found:
                msg = "Extended network code does not exist"
                raise ValueError(msg)
        return extnet

    @lru_cache(maxsize=1000)
    def _get_fdsn_network(self, net):
        """
        This function gets all networks metadata from FDSN, givent a short network code.
        Returns a list of dictionaries representing
        all the networks matching the short code.
        params:
        net : the short network code

        """
        request = f"{self.base_url}/query?fdsn_code={net}"
        with urlopen(request) as metadata:
            networks = {"networks": []}
            if metadata.status == HTTP_200_OK:
                networks = json.loads(metadata.read().decode("utf-8"))
            elif metadata.status == HTTP_204_NO_CONTENT:
                msg = f"No metadata for request {request}"
                raise ValueError(msg)
        return networks["networks"]
