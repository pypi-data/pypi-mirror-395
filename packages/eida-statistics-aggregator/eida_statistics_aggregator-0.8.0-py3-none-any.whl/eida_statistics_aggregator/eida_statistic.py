import logging
from datetime import date, timedelta

from python_hll2.hll import HLL
from python_hll2.util import NumberUtil



class EidaStatistic:
    """
    One statistic object.
    A statistic is for one day, network, station, location, channel, country.
    It has the following attributes:
    * size : the amount of data shipped for this statistic
    * nb_requests : the number of requests
    * nb_successful_requests : the number of OK requests
    * nb_unsuccessful_requests: the number of requests that did not deliver any data
    * unique_clients : a set (hll object) of clients.
    """

    def __init__(
        self,
        date,
        network="",
        station="",
        location="--",
        channel="",
        country="",
    ):
        """
        Class initialisation
        """
        self.original_day = date
        self.network = network
        self.station = station
        self.location = location
        self.channel = channel
        self.country = country
        self.size = 0
        self.nb_requests = 1
        self.nb_successful_requests = 0
        self.nb_unsuccessful_requests = 0
        self.unique_clients = HLL(11, 5)

    def _shift_to_begin_of_month(self):
        """
        Set the date as the first day of month. The statistics are meant to be displayed
        by month.
        :param event_datetime is a DateTime or Date object. Must have a weekday() method
        """
        if not isinstance(self.original_day, date):
            raise TypeError("datetime.date expected")
        return self.original_day - timedelta(days=(self.original_day.day - 1))

    def key(self):
        """
        Generate a unique key for this object in order to identify it easily and compare
        2 objects.
        2 statistics can be merged if they have the same key.
        """
        return f"{self._shift_to_begin_of_month()}_{self.network}_{self.station}_{self.location}_{self.channel}_{self.country}"

    def aggregate(self, eidastat):
        """
        Aggregate a statistic to this object.
        This function alters the called object by aggregating another statistic object
        into it:
        - incrementing counts,
        - summing sizes
        - aggregating HLL objects
        """
        # Check if the two keys are the same
        if self.key() == eidastat.key():
            self.size += eidastat.size
            self.nb_requests += eidastat.nb_requests
            self.nb_successful_requests += eidastat.nb_successful_requests
            self.nb_unsuccessful_requests += eidastat.nb_unsuccessful_requests
            self.unique_clients.union(eidastat.unique_clients)
        else:
            logging.warning(
                "Key %s to aggregate differs from called object's key %s",
                eidastat.key(),
                self.key(),
            )

    def info(self):
        """
        Return a string describing the object.
        """
        return f"{self.original_day} {self.network} {self.station} {self.location} {self.channel} from {self.country} {self.size}b {self.nb_successful_requests} successful requests from {self.unique_clients.cardinality()} unique clients"

    def to_dict(self):
        """
        Dump the statistic as a dictionary
        """
        unique_clients_bytes = self.unique_clients.to_bytes()
        return {
            "month": str(self._shift_to_begin_of_month()),
            "network": self.network,
            "station": self.station,
            "location": self.location,
            "channel": self.channel,
            "country": self.country,
            "bytes": self.size,
            "nb_requests": self.nb_requests,
            "nb_successful_requests": self.nb_successful_requests,
            "nb_unsuccessful_requests": self.nb_unsuccessful_requests,
            "clients": "\\x"
            + NumberUtil.to_hex(unique_clients_bytes, 0, len(unique_clients_bytes)),
        }
