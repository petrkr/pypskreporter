class LocalInfo:
    def __init__(self, callsign, grid, latlng, program_id, program_version, antenna = None):
        self._callsign = callsign
        self._grid = grid
        self._latlng = latlng
        self._program_id = program_id
        self._program_version = program_version
        self._antenna = antenna


    def __str__(self):
        return f"LocalInfo(callsign = {self._callsign}, grid = {self._grid}, latlng = {self._latlng}, antenna = {self._antenna}, program_id = {self._program_id}, program_version = {self._program_version})"


    def __repr__(self):
        return self.__str__()


    @property
    def callsign(self):
        return self._callsign

    @property
    def grid(self):
        return self._grid

    @property
    def latlng(self):
        return self._latlng

    @property
    def program_id(self):
        return self._program_id

    @property
    def program_version(self):
        return self._program_version

    @property
    def antenna(self):
        return self._antenna


    def to_dict(self):
        return {
            "callsign": self._callsign,
            "grid": self._grid,
            "latlng": self._latlng,
            "program_id": self._program_id,
            "program_version": self._program_version,
            "antenna": self._antenna
        }
    