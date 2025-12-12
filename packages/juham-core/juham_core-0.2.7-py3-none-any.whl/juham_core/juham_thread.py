"""
The `juham_thread` module provides foundational classes for creating multi-threaded automation objects.

Classes:
    AutomationObject: A generic base class for automation objects running MQTT communication.
    IWorkerThread: A base class for worker threads, e.g. data acquisition.

These classes are highly flexible and designed to handle various tasks asynchronously, 
making them suitable for a wide range of applications.

Justification for subclassing from `Thread`: sharing the common memory space.

.. todo:: Decouple the functionality from the thread so that it 
can be run by any means, e.g., by process or asyncio.
"""

import json

import time
from typing import Any, Optional, cast
from typing_extensions import override
from masterpiece import MasterPieceThread
from masterpiece.mqtt import MqttMsg
from masterpiece.supervisor import SupervisorThread
from .juham_ts import JuhamTs
from queue import Queue

class JuhamThread(JuhamTs):
    """Base class of automation classes that need to run automation tasks using asynchronously running thread.
    Spawns the thread upon creation.
    Subscribes to 'event' topic to listen log events from the thread, and dispatches
    them to corresponding logging methods e.g. `self.info()`.

    """

    _systemstatus_topic : str = "status" # TODO: design bug: should not be here
    _error_queue : Queue = Queue()
    _supervisor: Optional["SupervisorThread"] = None

    def __init__(self, name: str) -> None:
        """Construct automation object. By default no thread is created nor started.

        Args:
            name (str): name of the automation object.
        """
        super().__init__(name)
        self.worker: Optional[MasterPieceThread]
        self.event_topic = self.make_topic_name("event")

    def disconnect(self) -> None:
        """Request the asynchronous acquisition thread to stop after it has finished its current job.
        This method does not wait for the thread to stop. See `shutdown()`.
        """
        if self.worker != None:
            worker: MasterPieceThread = cast(MasterPieceThread, self.worker)
            worker.stay = False

    @override
    def shutdown(self) -> None:
        if self.worker is not None:
            self.worker.stop()  # request to thread to exit its processing loop
            self.worker.join()  # wait for the thread to complete
        super().shutdown()

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        start_time = time.time()
        if msg.topic == self.event_topic:
            em = json.loads(msg.payload.decode())
            self.on_event(em)
        else:
            super().on_message(client, userdata, msg)
        end_time: float = time.time()
        elapsed_time = end_time - start_time
        self.update_metrics(elapsed_time)

    @override
    def update_metrics(self, elapsed: float) -> None:
        super().update_metrics(elapsed)
        if self._elapsed > 2.0:
            sysinfo: dict[str, dict] = {
                "threads": {self.name: self.acquire_time_spent()}
            }
            self.publish(
                self._systemstatus_topic, json.dumps(sysinfo), qos=0, retain=False
            )

    def on_event(self, em: dict[str, Any]) -> None:
        """Notification event callback e.g info or warning.

        Args:
            em (dictionary): dictionary describing the event
        """
        if em["type"] == "Info":
            self.info(em["msg"], em["details"])
        elif em["type"] == "Debug":
            self.debug(em["msg"], em["details"])
        elif em["type"] == "Warning":
            self.warning(em["msg"], em["details"])
        elif em["type"] == "Error":
            self.error(em["msg"], em["details"])
        else:
            self.error("PANIC: unknown event type " + em["type"], str(em))

    @override
    def run(self) -> None:
        """Initialize and start the asynchronous acquisition thread."""
        super().run()
        if self.worker is not None:
            self.worker.mqtt_client = self.mqtt_client
            self.worker.name = "thread_" + self.name
            self.worker.event_topic = self.event_topic
            self.worker.error_queue = self._error_queue
            self.worker.start()
            self.info(f"Starting up {self.name} - {self.worker.__class__} ")
        else:
            self.warning(f"No thread, cannot run {self.name}")

    @classmethod
    def start_hypervisor(cls) -> None:
        """Start the hypervisor thread to monitor and restart crashed threads."""
        if cls._supervisor is None:
            cls._supervisor = HypervisorThread(cls._error_queue)
            cls._supervisor.start()

    