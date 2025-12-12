"""Threshold configuration."""

from abc import abstractmethod
from enum import Enum
from typing import TYPE_CHECKING, Any

from validio_sdk.resource._diffable import Diffable
from validio_sdk.resource._serde import NODE_TYPE_FIELD_NAME

if TYPE_CHECKING:
    from validio_sdk.code._import import ImportContext


class AdaptionRate(str, Enum):
    """Adaption rate."""

    FAST = "FAST"
    SLOW = "SLOW"


class ComparisonOperator(str, Enum):
    """Operator for comparing two numeric values."""

    EQUAL = "EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"
    NOT_EQUAL = "NOT_EQUAL"


class DecisionBoundsType(str, Enum):
    """Decision bounds type."""

    LOWER = "LOWER"
    UPPER = "UPPER"
    UPPER_AND_LOWER = "UPPER_AND_LOWER"


class DifferenceOperator(str, Enum):
    """Operator for difference threshold."""

    DECREASING = "DECREASING"
    INCREASING = "INCREASING"
    STRICTLY_DECREASING = "STRICTLY_DECREASING"
    STRICTLY_INCREASING = "STRICTLY_INCREASING"


class DifferenceType(str, Enum):
    """Type of difference."""

    ABSOLUTE = "ABSOLUTE"
    PERCENTAGE = "PERCENTAGE"


class DynamicThresholdAlgorithm(str, Enum):
    """Dynamic threshold algorithm."""

    V1 = "V1"
    V2 = "V2"


class Threshold(Diffable):
    """
    Base class for a threshold configuration.

    https://docs.validio.io/docs/thresholds
    """

    def __init__(self) -> None:
        """Constructor."""
        self._node_type = self.__class__.__name__

    @abstractmethod
    def _immutable_fields(self) -> set[str]:
        pass

    @abstractmethod
    def _mutable_fields(self) -> set[str]:
        pass

    def _nested_objects(self) -> dict[str, Diffable | list[Diffable] | None]:
        return {}

    def _encode(self) -> dict[str, object]:
        return self.__dict__

    @staticmethod
    def _decode(obj: dict[str, Any]) -> "Threshold":
        cls = eval(obj[NODE_TYPE_FIELD_NAME])
        return cls(**{k: v for k, v in obj.items() if k != NODE_TYPE_FIELD_NAME})

    @abstractmethod
    def _api_create_input(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def _api_update_input(self, validator_id: str) -> dict[str, Any]:
        pass


class DifferenceThreshold(Threshold):
    """A dynamic threshold configuration.

    https://docs.validio.io/docs/thresholds#difference-threshold
    """

    def __init__(
        self,
        *,
        difference_type: DifferenceType,
        operator: DifferenceOperator,
        number_of_windows: int,
        value: int,
    ):
        """
        Constructor.

        :param difference_type: The type of difference, i.e. absolute or
            percentage
        :param operator: The operator type, e.g. increasing or decreasing
        :param number_of_windows: The number of windows to monitor over
        :param value: The value which steers the bounds
        """
        super().__init__()

        self.difference_type = (
            difference_type
            if isinstance(difference_type, DifferenceType)
            else DifferenceType(difference_type)
        )
        self.operator = (
            operator
            if isinstance(operator, DifferenceOperator)
            else DifferenceOperator(operator)
        )
        self.number_of_windows = number_of_windows
        self.value = value

    def _immutable_fields(self) -> set[str]:
        return set({})

    def _mutable_fields(self) -> set[str]:
        return {"difference_type", "operator", "number_of_windows", "value"}

    def _api_create_input(self) -> dict[str, Any]:
        return {
            "differenceType": self.difference_type.value,
            "operator": self.operator.value,
            "numberOfWindows": self.number_of_windows,
            "value": self.value,
        }

    def _api_update_input(self, validator_id: str) -> dict[str, Any]:
        return {
            "validatorId": validator_id,
            "differenceType": self.difference_type.value,
            "operator": self.operator,
            "numberOfWindows": self.number_of_windows,
            "value": self.value,
        }


class DynamicThreshold(Threshold):
    """A dynamic threshold configuration.

    https://docs.validio.io/docs/thresholds#dynamic-threshold
    """

    def __init__(
        self,
        *,
        sensitivity: float = 3.0,
        decision_bounds_type: DecisionBoundsType = DecisionBoundsType.UPPER_AND_LOWER,
        adaption_rate: AdaptionRate = AdaptionRate.FAST,
        algorithm: DynamicThresholdAlgorithm | None = None,
    ):
        """
        Constructor.

        :param sensitivity: Steers how narrow/wide the threshold's bounds
            (accepted range of values) evolves over time. Typically starts
            at 2 or 3, lower values produce wider bounds while larger values
            produce wider bounds
        :param decision_bounds_type: Configures whether to treat a value deviation
            above (UPPER) or below (LOWER) the boundary as an anomaly.
        :param adaption_rate: Adaption rate determines how fast or slow Dynamic
            Threshold adapts to changes in data.
        :param algorithm: This value is ignored and will
            be removed in a future version.
        """
        super().__init__()

        self.sensitivity = float(sensitivity)
        self.decision_bounds_type = (
            decision_bounds_type
            if isinstance(decision_bounds_type, DecisionBoundsType)
            else DecisionBoundsType(decision_bounds_type)
        )
        self.adaption_rate = (
            adaption_rate
            if isinstance(adaption_rate, AdaptionRate)
            else AdaptionRate(adaption_rate)
        )
        self.algorithm = None
        if algorithm:
            self.algorithm = (
                algorithm
                if isinstance(algorithm, DynamicThresholdAlgorithm)
                else DynamicThresholdAlgorithm(algorithm)
            )

    def _immutable_fields(self) -> set[str]:
        return set({})

    def _mutable_fields(self) -> set[str]:
        return {"adaption_rate", "sensitivity", "decision_bounds_type"}

    def _api_create_input(self) -> dict[str, Any]:
        return {
            "adaptionRate": self.adaption_rate,
            "sensitivity": self.sensitivity,
            "decisionBoundsType": self.decision_bounds_type.value,
        }

    def _api_update_input(self, validator_id: str) -> dict[str, Any]:
        return {
            "adaptionRate": self.adaption_rate,
            "sensitivity": self.sensitivity,
            "decisionBoundsType": self.decision_bounds_type.value,
            "validatorId": validator_id,
        }

    def _import_str(
        self,
        indent_level: int,
        import_ctx: "ImportContext",
        inits: list[tuple[str, Any, str | None]] | None = None,
        skip_fields: set[str] | None = None,
    ) -> str:
        inits = list(inits or [])
        # NOTE: Once algorithm is removed from the API, this entire
        # method can be removed.
        skip_fields = (skip_fields or set()) | {"algorithm"}
        return super()._import_str(
            indent_level=indent_level,
            import_ctx=import_ctx,
            inits=inits,
            skip_fields=skip_fields,
        )

    @staticmethod
    def _default_value() -> "DynamicThreshold":
        return DynamicThreshold(sensitivity=3)


class FixedThreshold(Threshold):
    """A fixed threshold configuration.

    https://docs.validio.io/docs/thresholds#fixed-threshold
    """

    def __init__(
        self,
        *,
        value: float,
        operator: ComparisonOperator,
    ):
        """
        Constructor.

        :param value: Threshold value
        :param operator: Operator applied on the threshold value.
        """
        super().__init__()

        self.value = float(value)
        self.operator = (
            operator
            if isinstance(operator, ComparisonOperator)
            else ComparisonOperator(operator)
        )

    def _immutable_fields(self) -> set[str]:
        return set({})

    def _mutable_fields(self) -> set[str]:
        return {"value", "operator"}

    def _api_create_input(self) -> dict[str, Any]:
        return {
            "value": self.value,
            "operator": self.operator.value,
        }

    def _api_update_input(self, validator_id: str) -> dict[str, Any]:
        return {
            "validatorId": validator_id,
            "value": self.value,
            "operator": self.operator.value,
        }
