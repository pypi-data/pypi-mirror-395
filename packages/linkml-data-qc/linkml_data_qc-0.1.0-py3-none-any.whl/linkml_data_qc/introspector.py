"""Schema introspection utilities for identifying recommended slots.

This module provides tools to analyze LinkML schemas and identify slots
marked as `recommended: true`, which are used for compliance analysis.

Example - Basic schema introspection:

    >>> introspector = SchemaIntrospector("tests/data/test_schema.yaml")
    >>> "description" in introspector.recommended_slots
    True
    >>> "email" in introspector.recommended_slots
    True
    >>> "name" in introspector.recommended_slots  # required, not recommended
    False

Example - Getting class slot information:

    >>> csm = introspector.get_class_slots("Person")
    >>> csm.class_name
    'Person'
    >>> "description" in csm.recommended_slots
    True
    >>> "email" in csm.recommended_slots
    True

Example - Checking if a name is a class:

    >>> introspector.is_class("Person")
    True
    >>> introspector.is_class("string")
    False

Example - Getting traversable (inlined) slots for recursion:

    >>> traversable = introspector.get_traversable_slots("Person")
    >>> slot_names = [s.name for s in traversable]
    >>> "address" in slot_names
    True
    >>> "friends" in slot_names
    True

"""

from dataclasses import dataclass, field

from linkml_runtime.utils.schemaview import SchemaView


@dataclass
class SlotInfo:
    """Information about a schema slot.

    Example:
        >>> info = SlotInfo(
        ...     name="description",
        ...     range="string",
        ...     multivalued=False,
        ...     recommended=True,
        ...     inlined=False
        ... )
        >>> info.name
        'description'
        >>> info.recommended
        True
    """

    name: str
    range: str
    multivalued: bool
    recommended: bool
    inlined: bool


@dataclass
class ClassSlotMap:
    """Mapping of a class to its slots with recommended info.

    Example:
        >>> csm = ClassSlotMap(
        ...     class_name="Person",
        ...     slots=[],
        ...     recommended_slots=["description", "email"]
        ... )
        >>> csm.class_name
        'Person'
        >>> len(csm.recommended_slots)
        2
    """

    class_name: str
    slots: list[SlotInfo] = field(default_factory=list)
    recommended_slots: list[str] = field(default_factory=list)


class SchemaIntrospector:
    """Analyze LinkML schema to identify recommended slots and traversal paths.

    Example:
        >>> introspector = SchemaIntrospector("tests/data/test_schema.yaml")
        >>> len(introspector.recommended_slots) > 0
        True
    """

    def __init__(self, schema_path: str):
        """Initialize with a schema file path.

        Args:
            schema_path: Path to LinkML schema YAML file

        Example:
            >>> introspector = SchemaIntrospector("tests/data/test_schema.yaml")
            >>> introspector.schema_path
            'tests/data/test_schema.yaml'
        """
        self.schema_path = schema_path
        self.sv = SchemaView(schema_path)
        self._recommended_cache: set[str] | None = None
        self._class_slot_cache: dict[str, ClassSlotMap] = {}

    @property
    def recommended_slots(self) -> set[str]:
        """Get all slot names marked as recommended.

        Example:
            >>> introspector = SchemaIntrospector("tests/data/test_schema.yaml")
            >>> slots = introspector.recommended_slots
            >>> isinstance(slots, set)
            True
            >>> "description" in slots
            True
        """
        if self._recommended_cache is None:
            self._recommended_cache = {
                s for s in self.sv.all_slots() if self.sv.get_slot(s).recommended
            }
        return self._recommended_cache

    def get_class_slots(self, class_name: str) -> ClassSlotMap:
        """Get slot information for a class.

        Args:
            class_name: Name of the LinkML class

        Returns:
            ClassSlotMap with all slots and recommended slots for the class

        Example:
            >>> introspector = SchemaIntrospector("tests/data/test_schema.yaml")
            >>> csm = introspector.get_class_slots("Address")
            >>> csm.class_name
            'Address'
            >>> "street" in csm.recommended_slots
            True
            >>> "city" in csm.recommended_slots
            True
        """
        if class_name in self._class_slot_cache:
            return self._class_slot_cache[class_name]

        slots = []
        for slot_name in self.sv.class_slots(class_name):
            slot = self.sv.get_slot(slot_name)
            slots.append(
                SlotInfo(
                    name=slot_name,
                    range=slot.range or "string",
                    multivalued=bool(slot.multivalued),
                    recommended=bool(slot.recommended),
                    inlined=bool(slot.inlined or slot.inlined_as_list),
                )
            )

        csm = ClassSlotMap(
            class_name=class_name,
            slots=slots,
            recommended_slots=[s.name for s in slots if s.recommended],
        )
        self._class_slot_cache[class_name] = csm
        return csm

    def is_class(self, name: str) -> bool:
        """Check if name refers to a defined class.

        Args:
            name: Name to check

        Returns:
            True if name is a defined class, False otherwise

        Example:
            >>> introspector = SchemaIntrospector("tests/data/test_schema.yaml")
            >>> introspector.is_class("Person")
            True
            >>> introspector.is_class("Address")
            True
            >>> introspector.is_class("integer")
            False
        """
        return name in self.sv.all_classes()

    def get_traversable_slots(self, class_name: str) -> list[SlotInfo]:
        """Get slots whose range is another class (for recursion).

        These are slots that can be traversed to analyze nested objects.
        Only inlined slots are traversable.

        Args:
            class_name: Name of the class to get traversable slots for

        Returns:
            List of SlotInfo for slots that reference other classes

        Example:
            >>> introspector = SchemaIntrospector("tests/data/test_schema.yaml")
            >>> traversable = introspector.get_traversable_slots("Person")
            >>> names = [s.name for s in traversable]
            >>> "address" in names
            True
            >>> "name" in names  # string slot, not traversable
            False
        """
        csm = self.get_class_slots(class_name)
        return [s for s in csm.slots if self.is_class(s.range) and s.inlined]
