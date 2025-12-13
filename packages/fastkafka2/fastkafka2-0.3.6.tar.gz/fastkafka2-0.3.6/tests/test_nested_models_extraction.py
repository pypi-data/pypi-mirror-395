"""
Тестовый бенчмарк для проверки извлечения моделей из вложенных классов.
Использует реальные примеры из machine_microservice для проверки работоспособности
перед публикацией в PyPI.
"""
import logging
import pytest
from enum import StrEnum
from typing import Optional, Union
from pydantic import BaseModel
from fastkafka2 import KafkaHandler, KafkaMessage

# Включаем debug логирование для отладки
logging.basicConfig(level=logging.DEBUG)
# Включаем DEBUG для fastkafka2.core.registry
logging.getLogger('fastkafka2.core.registry').setLevel(logging.DEBUG)


# ============================================================
# Копируем структуру схем из machine_microservice
# ============================================================

class BaseHeaders(BaseModel):
    machine_id: str
    message_type: str
    timestamp: str


class RequestSchema(BaseModel):
    """База для входящих payload'ов"""
    pass


class ResponseSchema(BaseModel):
    """База для исходящих схем"""
    pass


# ============================================================
# machines_updates (как в machine_microservice)
# ============================================================
class MachinesUpdatesTopic:
    topic = "machines_updates"

    class MessageTypeStrEnum(StrEnum):
        CELL_STATUS_UPDATE = "cell_status_update"
        ORDER_STATUS_UPDATE = "order_status_update"
        POWER_SOURCE_STATUS_UPDATE = "power_source_status_update"
        DEVICE_STATUS_UPDATE = "device_status_update"
        CARRIAGE_POSITION_UPDATE = "carriage_position_update"
        MACHINE_STATUS_UPDATE = "machine_status_update"
        QR_SCANNER_UPDATE = "qr_scanner_update"

    class Headers(BaseHeaders, RequestSchema):
        message_type: "MachinesUpdatesTopic.MessageTypeStrEnum"

    # --- cell_status_update ---
    class CellStatusMessage:
        class CellStatusStrEnum(StrEnum):
            OPEN = "open"
            CLOSE = "close"

        class Payload(RequestSchema):
            cell_id: int
            status: "MachinesUpdatesTopic.CellStatusMessage.CellStatusStrEnum"

        class Data(RequestSchema):
            payload: "MachinesUpdatesTopic.CellStatusMessage.Payload"

    # --- order_status_update ---
    class OrderStatusMessage:
        class OrderStatusStrEnum(StrEnum):
            RECEIVED = "received"
            PROCESSING_STARTED = "processing_started"
            READY = "ready"
            ERROR = "error"

        class Payload(RequestSchema):
            order_number: str
            status: "MachinesUpdatesTopic.OrderStatusMessage.OrderStatusStrEnum"

        class Data(RequestSchema):
            payload: "MachinesUpdatesTopic.OrderStatusMessage.Payload"

    # --- power_source_status_update ---
    class PowerSourceStatusMessage:
        class PowerSourceStrEnum(StrEnum):
            MAINS = "mains"
            UPS = "ups"

        class Payload(RequestSchema):
            power_source: "MachinesUpdatesTopic.PowerSourceStatusMessage.PowerSourceStrEnum"

        class Data(RequestSchema):
            payload: "MachinesUpdatesTopic.PowerSourceStatusMessage.Payload"

    # --- device_status_update ---
    class DeviceStatusMessage:
        class DeviceTypeStrEnum(StrEnum):
            PRINTER = "printer"
            ENGINE = "engine"

        class DeviceStatusStrEnum(StrEnum):
            OK = "ok"
            ERROR = "error"

        class Payload(RequestSchema):
            device_type: "MachinesUpdatesTopic.DeviceStatusMessage.DeviceTypeStrEnum"
            name: str
            status: "MachinesUpdatesTopic.DeviceStatusMessage.DeviceStatusStrEnum"
            error_code: str
            error_message: str

        class Data(RequestSchema):
            payload: "MachinesUpdatesTopic.DeviceStatusMessage.Payload"

    # --- carriage_position_update ---
    class CarriagePositionUpdateMessage:
        class PositionNameStrEnum(StrEnum):
            PRINTER_1 = "printer_1"

        class Position(RequestSchema):
            x: int
            y: int
            z: int

        class Payload(RequestSchema):
            position_name: "MachinesUpdatesTopic.CarriagePositionUpdateMessage.PositionNameStrEnum"
            position: "MachinesUpdatesTopic.CarriagePositionUpdateMessage.Position"

        class Data(RequestSchema):
            payload: "MachinesUpdatesTopic.CarriagePositionUpdateMessage.Payload"

    # --- machine_status_update ---
    class MachineStatusMessage:
        class MachineStatusStrEnum(StrEnum):
            OK = "ok"
            ERROR = "error"

        class Payload(RequestSchema):
            status: "MachinesUpdatesTopic.MachineStatusMessage.MachineStatusStrEnum"
            order_ready: bool

        class Data(RequestSchema):
            payload: "MachinesUpdatesTopic.MachineStatusMessage.Payload"

    # --- qr_scanner_update ---
    class QRScannerUpdateMessage:
        class Payload(RequestSchema):
            qr_code: str

        class Data(RequestSchema):
            payload: "MachinesUpdatesTopic.QRScannerUpdateMessage.Payload"


# ============================================================
# machines_heartbeats (как в machine_microservice)
# ============================================================
class MachinesHeartbeatsTopic:
    topic = "machines_heartbeats"

    class MessageTypeStrEnum(StrEnum):
        HEARTBEAT = "heartbeat"

    class Headers(BaseHeaders, RequestSchema):
        message_type: "MachinesHeartbeatsTopic.MessageTypeStrEnum"

    class PowerSourceStrEnum(StrEnum):
        MAINS = "mains"
        UPS = "ups"

    class HeartbeatMessage:
        class Payload(RequestSchema):
            power_source: Optional["MachinesHeartbeatsTopic.PowerSourceStrEnum"] = None

        class Data(RequestSchema):
            payload: "MachinesHeartbeatsTopic.HeartbeatMessage.Payload"


# ============================================================
# machines_commands (как в machine_microservice)
# ============================================================
class MachinesCommandsTopic:
    topic = "machines_commands"

    class MessageTypeStrEnum(StrEnum):
        OPEN_CELL = "open_cell"

    class Headers(BaseHeaders, ResponseSchema):
        message_type: "MachinesCommandsTopic.MessageTypeStrEnum"

    class OpenCellMessage:
        class Payload(ResponseSchema):
            cell_id: int

        class Data(ResponseSchema):
            payload: "MachinesCommandsTopic.OpenCellMessage.Payload"


# ============================================================
# machines_orders (как в machine_microservice)
# ============================================================
class MachinesOrdersTopic:
    topic = "machines_orders"

    class MessageTypeStrEnum(StrEnum):
        CREATE_ORDER = "create_order"

    class Headers(BaseHeaders, ResponseSchema):
        message_type: "MachinesOrdersTopic.MessageTypeStrEnum"

    class CreateOrderMessage:
        class FileItem(ResponseSchema):
            printer_name: str
            file_url: str
            pages: list[list[int]]
            copies: int
            parameters: dict

        class Payload(ResponseSchema):
            order_number: str
            cell_id: int
            erase_before: bool
            files: list["MachinesOrdersTopic.CreateOrderMessage.FileItem"]

        class Data(ResponseSchema):
            payload: "MachinesOrdersTopic.CreateOrderMessage.Payload"


# ============================================================
# Тесты handlers с глубокой вложенностью
# Handlers определены на уровне модуля (как в реальном коде)
# ============================================================

handler = KafkaHandler()


# Handlers определены на уровне модуля (не внутри функций!)
@handler(
    "machines_updates",
    headers_filter={"message_type": MachinesUpdatesTopic.MessageTypeStrEnum.CELL_STATUS_UPDATE.value},
)
async def handle_cell_status_update(
    message: KafkaMessage[
        MachinesUpdatesTopic.CellStatusMessage.Data,
        MachinesUpdatesTopic.Headers,
    ],
):
    """Handler для cell_status_update (3 уровня вложенности)"""
    assert message.data.payload.cell_id == 1
    assert message.data.payload.status.value == "open"
    assert message.headers.machine_id == "123"


@handler(
    "machines_updates",
    headers_filter={"message_type": MachinesUpdatesTopic.MessageTypeStrEnum.ORDER_STATUS_UPDATE.value},
)
async def handle_order_status_update(
    message: KafkaMessage[
        MachinesUpdatesTopic.OrderStatusMessage.Data,
        MachinesUpdatesTopic.Headers,
    ],
):
    """Handler для order_status_update (3 уровня вложенности)"""
    assert message.data.payload.order_number == "ORDER-123"
    assert message.data.payload.status.value == "received"


@handler(
    "machines_updates",
    headers_filter={"message_type": MachinesUpdatesTopic.MessageTypeStrEnum.POWER_SOURCE_STATUS_UPDATE.value},
)
async def handle_power_source_status_update(
    message: KafkaMessage[
        MachinesUpdatesTopic.PowerSourceStatusMessage.Data,
        MachinesUpdatesTopic.Headers,
    ],
):
    """Handler для power_source_status_update (3 уровня вложенности)"""
    assert message.data.payload.power_source.value in ["mains", "ups"]


@handler(
    "machines_updates",
    headers_filter={"message_type": MachinesUpdatesTopic.MessageTypeStrEnum.DEVICE_STATUS_UPDATE.value},
)
async def handle_device_status_update(
    message: KafkaMessage[
        MachinesUpdatesTopic.DeviceStatusMessage.Data,
        MachinesUpdatesTopic.Headers,
    ],
):
    """Handler для device_status_update (3 уровня вложенности)"""
    assert message.data.payload.device_type.value in ["printer", "engine"]
    assert message.data.payload.status.value in ["ok", "error"]


@handler(
    "machines_updates",
    headers_filter={"message_type": MachinesUpdatesTopic.MessageTypeStrEnum.CARRIAGE_POSITION_UPDATE.value},
)
async def handle_carriage_position_update(
    message: KafkaMessage[
        MachinesUpdatesTopic.CarriagePositionUpdateMessage.Data,
        MachinesUpdatesTopic.Headers,
    ],
):
    """Handler для carriage_position_update (4 уровня вложенности!)"""
    assert message.data.payload.position_name.value == "printer_1"
    assert message.data.payload.position.x == 10
    assert message.data.payload.position.y == 20
    assert message.data.payload.position.z == 30


@handler(
    "machines_updates",
    headers_filter={"message_type": MachinesUpdatesTopic.MessageTypeStrEnum.MACHINE_STATUS_UPDATE.value},
)
async def handle_machine_status_update(
    message: KafkaMessage[
        MachinesUpdatesTopic.MachineStatusMessage.Data,
        MachinesUpdatesTopic.Headers,
    ],
):
    """Handler для machine_status_update (3 уровня вложенности)"""
    assert message.data.payload.status.value in ["ok", "error"]
    assert isinstance(message.data.payload.order_ready, bool)


@handler(
    "machines_updates",
    headers_filter={"message_type": MachinesUpdatesTopic.MessageTypeStrEnum.QR_SCANNER_UPDATE.value},
)
async def handle_qr_scanner_update(
    message: KafkaMessage[
        MachinesUpdatesTopic.QRScannerUpdateMessage.Data,
        MachinesUpdatesTopic.Headers,
    ],
):
    """Handler для qr_scanner_update (3 уровня вложенности)"""
    assert isinstance(message.data.payload.qr_code, str)


heartbeat_handler = KafkaHandler()

@heartbeat_handler(
    "machines_heartbeats",
    headers_filter={"message_type": MachinesHeartbeatsTopic.MessageTypeStrEnum.HEARTBEAT.value},
)
async def machines_heartbeat_handler(
    message: KafkaMessage[
        MachinesHeartbeatsTopic.HeartbeatMessage.Data,
        MachinesHeartbeatsTopic.Headers,
    ],
):
    """Handler для heartbeat (3 уровня вложенности)"""
    if message.data.payload.power_source:
        assert message.data.payload.power_source.value in ["mains", "ups"]


# ============================================================
# Тесты проверки регистрации handlers
# ============================================================

def test_cell_status_update_handler():
    """Проверка handler для cell_status_update"""
    from fastkafka2.core.registry import handlers_registry
    handlers = handlers_registry.get("machines_updates", [])
    assert len(handlers) >= 1
    
    cell_handler = None
    for h in handlers:
        if h.func.__name__ == "handle_cell_status_update":
            cell_handler = h
            break
    
    assert cell_handler is not None, "Handler not found"
    assert cell_handler.data_model == MachinesUpdatesTopic.CellStatusMessage.Data
    assert cell_handler.headers_model == MachinesUpdatesTopic.Headers


def test_order_status_update_handler():
    """Проверка handler для order_status_update"""
    from fastkafka2.core.registry import handlers_registry
    handlers = handlers_registry.get("machines_updates", [])
    
    order_handler = None
    for h in handlers:
        if h.func.__name__ == "handle_order_status_update":
            order_handler = h
            break
    
    assert order_handler is not None
    assert order_handler.data_model == MachinesUpdatesTopic.OrderStatusMessage.Data
    assert order_handler.headers_model == MachinesUpdatesTopic.Headers


def test_power_source_status_update_handler():
    """Проверка handler для power_source_status_update"""
    from fastkafka2.core.registry import handlers_registry
    handlers = handlers_registry.get("machines_updates", [])
    
    power_handler = None
    for h in handlers:
        if h.func.__name__ == "handle_power_source_status_update":
            power_handler = h
            break
    
    assert power_handler is not None
    assert power_handler.data_model == MachinesUpdatesTopic.PowerSourceStatusMessage.Data
    assert power_handler.headers_model == MachinesUpdatesTopic.Headers


def test_device_status_update_handler():
    """Проверка handler для device_status_update"""
    from fastkafka2.core.registry import handlers_registry
    handlers = handlers_registry.get("machines_updates", [])
    
    device_handler = None
    for h in handlers:
        if h.func.__name__ == "handle_device_status_update":
            device_handler = h
            break
    
    assert device_handler is not None
    assert device_handler.data_model == MachinesUpdatesTopic.DeviceStatusMessage.Data
    assert device_handler.headers_model == MachinesUpdatesTopic.Headers


def test_carriage_position_update_handler():
    """Проверка handler для carriage_position_update (4 уровня вложенности!)"""
    from fastkafka2.core.registry import handlers_registry
    handlers = handlers_registry.get("machines_updates", [])
    
    carriage_handler = None
    for h in handlers:
        if h.func.__name__ == "handle_carriage_position_update":
            carriage_handler = h
            break
    
    assert carriage_handler is not None
    assert carriage_handler.data_model == MachinesUpdatesTopic.CarriagePositionUpdateMessage.Data
    assert carriage_handler.headers_model == MachinesUpdatesTopic.Headers


def test_machine_status_update_handler():
    """Проверка handler для machine_status_update"""
    from fastkafka2.core.registry import handlers_registry
    handlers = handlers_registry.get("machines_updates", [])
    
    machine_handler = None
    for h in handlers:
        if h.func.__name__ == "handle_machine_status_update":
            machine_handler = h
            break
    
    assert machine_handler is not None
    assert machine_handler.data_model == MachinesUpdatesTopic.MachineStatusMessage.Data
    assert machine_handler.headers_model == MachinesUpdatesTopic.Headers


def test_qr_scanner_update_handler():
    """Проверка handler для qr_scanner_update"""
    from fastkafka2.core.registry import handlers_registry
    handlers = handlers_registry.get("machines_updates", [])
    
    qr_handler = None
    for h in handlers:
        if h.func.__name__ == "handle_qr_scanner_update":
            qr_handler = h
            break
    
    assert qr_handler is not None
    assert qr_handler.data_model == MachinesUpdatesTopic.QRScannerUpdateMessage.Data
    assert qr_handler.headers_model == MachinesUpdatesTopic.Headers


def test_heartbeat_handler():
    """Проверка handler для heartbeat"""
    from fastkafka2.core.registry import handlers_registry
    handlers = handlers_registry.get("machines_heartbeats", [])
    
    assert len(handlers) >= 1
    heartbeat_h = None
    for h in handlers:
        if h.func.__name__ == "machines_heartbeat_handler":
            heartbeat_h = h
            break
    
    assert heartbeat_h is not None
    assert heartbeat_h.data_model == MachinesHeartbeatsTopic.HeartbeatMessage.Data
    assert heartbeat_h.headers_model == MachinesHeartbeatsTopic.Headers


def test_all_handlers_registered():
    """Проверяем что все handlers успешно зарегистрированы с правильными моделями"""
    from fastkafka2.core.registry import handlers_registry
    
    # Проверяем machines_updates handlers
    machines_updates_handlers = handlers_registry.get("machines_updates", [])
    assert len(machines_updates_handlers) >= 7, f"Expected at least 7 handlers, got {len(machines_updates_handlers)}"
    
    # Проверяем что у всех handlers есть модели
    for handler in machines_updates_handlers:
        assert handler.data_model is not None, f"Handler {handler.func.__name__} has no data_model"
        assert handler.headers_model is not None, f"Handler {handler.func.__name__} has no headers_model"
        assert issubclass(handler.data_model, BaseModel), f"data_model {handler.data_model} is not BaseModel"
        assert issubclass(handler.headers_model, BaseModel), f"headers_model {handler.headers_model} is not BaseModel"
    
    # Проверяем machines_heartbeats handlers
    heartbeat_handlers = handlers_registry.get("machines_heartbeats", [])
    assert len(heartbeat_handlers) >= 1, "No heartbeat handlers found"
    
    for handler in heartbeat_handlers:
        assert handler.data_model is not None
        assert handler.headers_model is not None


if __name__ == "__main__":
    # Запуск тестов напрямую
    pytest.main([__file__, "-v"])

