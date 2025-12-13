from compas.geometry import Geometry
from compas.geometry import Point


class Dot(Geometry):
    """A dot is text displayed at a point location.

    The dot maintains constant screen size regardless of zoom level,
    similar to Rhino's Dot command.

    Parameters
    ----------
    point : :class:`compas.geometry.Point` | list[float]
        The location of the dot.
    text : str
        The text to display.
    name : str, optional
        The name of the dot.

    Attributes
    ----------
    point : :class:`compas.geometry.Point`
        The location of the dot.
    text : str
        The text to display.

    Examples
    --------
    >>> from compas.geometry import Point
    >>> from compas_notebook.geometry import Dot
    >>> dot = Dot([0, 0, 0], "Hello")
    >>> dot.point
    Point(x=0.000, y=0.000, z=0.000)
    >>> dot.text
    'Hello'

    """

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "point": Point.DATASCHEMA,
            "text": {"type": "string"},
        },
        "required": ["point", "text"],
    }

    @property
    def __data__(self):
        return {
            "point": self._point.__data__,
            "text": self._text,
        }

    @classmethod
    def __from_data__(cls, data):
        return cls(
            point=Point.__from_data__(data["point"]),
            text=data["text"],
        )

    def __init__(self, point, text, name=None):
        super().__init__(name=name)
        self._point = None
        self._text = None
        self.point = point
        self.text = text

    def __repr__(self):
        return f"Dot({self.point!r}, {self.text!r})"

    def __eq__(self, other):
        if not isinstance(other, Dot):
            return False
        return self.point == other.point and self.text == other.text

    @property
    def point(self):
        return self._point

    @point.setter
    def point(self, value):
        if not isinstance(value, Point):
            value = Point(*value)
        self._point = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = str(value)

    def transform(self, transformation):
        """Transform the dot.

        Parameters
        ----------
        transformation : :class:`compas.geometry.Transformation`
            The transformation to apply.

        Returns
        -------
        None

        """
        self.point.transform(transformation)
