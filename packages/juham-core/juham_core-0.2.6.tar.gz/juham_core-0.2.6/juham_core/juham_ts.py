import traceback
from typing import Any, Dict, Optional, cast, Union
from typing_extensions import override
from masterpiece.timeseries import TimeSeries, Measurement
from .juham import Juham


class JuhamTs(Juham):
    """Base class for automation objects with timeseries database
    support.

    To configure the class to use a specific timeseries database implementation set
    the `database_class_id` class attribute. When instantiated the object will instantiate
    the given MQTT object with it.
    """

    database_class_id: str = ""
    write_attempts: int = 3

    def __init__(self, name: str = "") -> None:
        super().__init__(name)
        self.database_client: Optional[Union[TimeSeries, None]] = None

    @override
    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().to_dict()
        if self.database_client is not None:
            data["_database"] = {"db_client": self.database_client.to_dict()}
        return data

    @override
    def from_dict(self, data: Dict[str, Any]) -> None:
        super().from_dict(data)
        if "_database" in data:
            value = data["_database"]["db_client"]
            self.database_client = cast(
                Optional[TimeSeries], Juham.instantiate(value["_class"], self.name)
            )
            if self.database_client is not None and "_object" in value:
                self.database_client.from_dict(value)

    def initialize(self) -> None:
        self.init_database(self.name)
        super().initialize()

    def measurement(self, name: str) -> Measurement:
        timeseries: TimeSeries = cast(TimeSeries, self.database_client)
        return timeseries.measurement(name)

    def init_database(self, name: str) -> None:
        if (
            JuhamTs.database_class_id != None
            and Juham.find_class(JuhamTs.database_class_id) != None
        ):
            self.database_client = cast(
                Optional[TimeSeries], Juham.instantiate(JuhamTs.database_class_id)
            )
            self.database_client.errorq = self.error_queue()
        else:
            self.warning("Suspicious configuration: no database_class_id set")

    def write(self, point: Measurement) -> None:
        if not self.database_client:
            raise ValueError("Database client is not initialized.")

        first_exception: Optional[BaseException] = None
        for i in range(self.write_attempts):
            try:
                self.database_client.write(point)
                return
            except Exception as e:
                if first_exception is None:
                    first_exception = e
                self.warning(f"Writing ts failed, attempt {i+1}: {repr(e)}")

        self.log_message(
            "Error",
            f"Writing failed after {self.write_attempts} attempts, giving up",
            "".join(
                traceback.format_exception_only(type(first_exception), first_exception)
                if first_exception
                else "No exception"
            ),
        )

    def write_point(
        self, name: str, tags: dict[str, Any], fields: dict[str, Any], ts: str
    ) -> None:
        if not self.database_client:
            raise ValueError("Database client is not initialized.")

        first_exception: Optional[BaseException] = None
        for i in range(self.write_attempts):
            try:
                self.database_client.write_dict(name, tags, fields, ts)
                return
            except Exception as e:
                if first_exception is None:
                    first_exception is None
                self.warning(f"Writing ts failed, attempt {i+1}: {repr(e)}")

        self.log_message(
            "Error",
            f"Writing failed after {self.write_attempts} attempts, giving up",
            "".join(
                traceback.format_exception_only(type(first_exception), first_exception)
            ),
        )

    def read_last_value(
        self,
        measurement: str,
        tags: Optional[dict[str, Any]] = None,
        fields: Optional[list[str]] = None,
    ) -> dict[str, Any]:
        if not self.database_client:
            raise ValueError("Database client is not initialized.")

        first_exception: Optional[BaseException] = None
        for i in range(self.write_attempts):
            try:
                return self.database_client.read_last_value(measurement, tags, fields)
            except Exception as e:
                if first_exception is None:
                    first_exception = e
                self.warning(f"Reading ts failed, attempt {i+1}: {repr(e)}")

        self.log_message(
            "Error",
            f"Reading failed after {self.write_attempts} attempts, giving up",
            "".join(
                traceback.format_exception_only(type(first_exception), first_exception)
            ),
        )
        return {}

    def read(self, point: Measurement) -> None:
        pass
