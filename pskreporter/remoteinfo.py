from time import time

class RemoteInfo:
    def __init__(self, callsign, mode, freq = None, snr = None, grid = None, latlng = None, qso_date = None, time_on = None):
        self._callsign = callsign
        self._mode = mode
        self._freq = freq
        self._snr = snr
        self._grid = grid
        self._latlng = latlng
        self._qso_date = int(qso_date or time())
        self._time_on = int(time_on or time())


    def __str__(self):
        return f"RemoteInfo(callsign = {self._callsign}, freq = {self._freq}, mode = {self._mode}, snr = {self._snr}, grid = {self._grid}, latlng = {self._latlng}, qso_date = {self._qso_date}, time_on = {self._time_on})"


    def __repr__(self):
        return self.__str__()


    @property
    def callsign(self):
        return self._callsign

    @property
    def freq(self):
        return self._freq

    @property
    def mode(self):
        return self._mode

    @property
    def snr(self):
        return self._snr

    @property
    def grid(self):
        return self._grid

    @property
    def latlng(self):
        return self._latlng

    @property
    def qso_date(self):
        return self._qso_date

    @property
    def time_on(self):
        return self._time_on

    def to_dict(self):
        return {
            "callsign": self._callsign,
            "freq": self._freq,
            "mode": self._mode,
            "snr": self._snr,
            "grid": self._grid,
            "latlng": self._latlng,
            "qso_date": self._qso_date,
            "time_on": self._time_on
        }
