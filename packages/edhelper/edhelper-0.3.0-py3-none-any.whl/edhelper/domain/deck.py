from datetime import datetime


class Deck:
    def __init__(
        self,
        id: int | None = None,
        name: str | None = None,
        last_update: str | None = None,
    ):
        assert isinstance(id, int | None)
        assert isinstance(name, str | None)
        assert isinstance(last_update, str | None)

        self._id = id
        self._name = name
        self._last_update = (
            last_update if last_update is not None else datetime.now().isoformat()
        )

    def _update_timestamp(self):
        self._last_update = datetime.now().isoformat()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, new_id: int | None):
        assert isinstance(new_id, int | None)
        if self._id != new_id:
            self._id = new_id
            self._update_timestamp()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str | None):
        assert isinstance(new_name, str | None)
        if self._name != new_name:
            self._name = new_name
            self._update_timestamp()

    @property
    def last_update(self):
        return self._last_update

    def update(self):
        self._update_timestamp()

    def get_values_tuple(self, id=True, name=True, last_update=True):
        values = []
        if id:
            values.append(self.id)
        if name:
            values.append(self.name)
        if last_update:
            values.append(self.last_update)
        return tuple(values)

    def __hash__(self):
        return hash(self.get_values_tuple())

    def get_list_row(self):
        return [self.id, self.name, self.last_update]
