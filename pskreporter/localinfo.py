class LocalInfo:
    def __init__(self, callsign, grid, program_id, program_version, latlng = None, antenna = None):
        self._callsign = callsign
        self._grid = grid
        self._latlng = latlng

        # If latlng exists, override grid
        grid_lonlat = self._get_grid_from_latlng()
        if grid_lonlat:
            self._grid = grid_lonlat

        self._program_id = program_id
        self._program_version = program_version
        self._antenna = antenna


    def __str__(self):
        return f"LocalInfo(callsign = {self._callsign}, grid = {self._grid}, latlng = {self._latlng}, antenna = {self._antenna}, program_id = {self._program_id}, program_version = {self._program_version})"


    def __repr__(self):
        return self.__str__()


    def _get_grid_from_latlng(self):
        if not self._latlng:
            return None

        # TODO: Implement this, for now return None
        return None

    @property
    def callsign(self):
        return self._callsign

    @property
    def grid(self):
        return self._grid

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
            "program_id": self._program_id,
            "program_version": self._program_version,
            "antenna": self._antenna
        }
    