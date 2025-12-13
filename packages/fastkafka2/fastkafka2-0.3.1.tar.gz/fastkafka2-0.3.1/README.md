# fastkafka2

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/fastkafka2.svg)](https://pypi.org/project/fastkafka2/)

**Next-generation FastAPI-like developer experience for Kafka.**

Fast, type-safe, and easy-to-use Kafka library for Python with async support, lazy deserialization, and built-in Pydantic validation.

Built on top of `confluent-kafka-python` for high performance and reliability.

### Why fastkafka2?

- **FastAPI-like syntax** - If you know FastAPI, you'll feel at home
- **Lazy deserialization** - Only deserialize messages that match your handlers
- **Type safety** - Full type hints with Pydantic validation
- **Production ready** - Built-in error handling, retry logic, and monitoring
- **Zero configuration** - Sensible defaults, works out of the box

## Features

- **High Performance**: Lazy message deserialization - body is only deserialized when handler accepts the message
- **Type Safety**: Full type hints and Pydantic validation support with IDE autocomplete
- **Header Filtering**: Fast filtering by headers before deserialization (saves CPU/memory)
- **Easy to Use**: FastAPI-like decorator syntax - familiar and intuitive
- **Ordering Guaranteed**: Sequential processing per partition (maintains message order)
- **Auto Topic Creation**: Automatic topic creation on startup
- **Dependency Injection**: Built-in DI support for clean architecture
- **Async/Await**: Full async support with Python asyncio
- **Error Handling**: Robust error handling with retry logic and offset management
- **Monitoring**: Built-in statistics and metrics for observability

## Installation

```bash
pip install fastkafka2
```

**System Requirements:**

fastkafka2 uses `confluent-kafka-python` which requires C extensions. Pre-built wheels are available for most platforms.

If installation fails, you may need to install system dependencies:

**Linux:**
```bash
# Ubuntu/Debian
sudo apt-get install librdkafka-dev python3-dev

# CentOS/RHEL
sudo yum install librdkafka-devel python3-devel
```

**macOS:**
```bash
brew install librdkafka
```

**Windows:**
Pre-built wheels are available, no additional setup required.

## Project Structure

Here's a recommended project structure for organizing your Kafka handlers:

```shell
├── api/
│   ├── kafka/
│   │   ├── handlers/
│   │   │   ├── orders/
│   │   │   │   ├── schemas.py      # Pydantic models
│   │   │   │   └── handler.py      # Order handlers
│   │   │   ├── payments/
│   │   │   │   ├── schemas.py
│   │   │   │   └── handler.py
│   │   │   └── base_handler.py     # Combines all handlers
│   │   └── lifespan.py              # App lifecycle
│
├── main.py                          # Entry point
└── requirements.txt
```

### Example Files

#### `api/kafka/handlers/orders/schemas.py`

```python
from pydantic import BaseModel
from enum import Enum

class OrderStatus(str, Enum):
    CREATED = "created"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class OrderData(BaseModel):
    id: int
    customer_id: int
    amount: float
    items: list[str]
    status: OrderStatus

class OrderHeaders(BaseModel):
    source: str
    priority: str
    timestamp: str
```

#### `api/kafka/handlers/orders/handler.py`

```python
import logging
from fastkafka2 import KafkaHandler, KafkaMessage, KafkaProducer
from .schemas import OrderData, OrderHeaders, OrderStatus

logger = logging.getLogger(__name__)

# Handler with prefix for orders topic group
orders_handler = KafkaHandler(prefix="orders")

# Producer instance (should be started in lifespan)
# See lifespan.py for proper initialization
producer = KafkaProducer(bootstrap_servers="127.0.0.1:9092")


# Business logic functions
async def process_order(order_id: int, customer_id: int, amount: float) -> dict:
    """
    Business logic function to process an order.
    This could interact with database, external APIs, etc.
    """
    logger.info(f"Processing order {order_id} for customer {customer_id}")
    
    # Example: Save to database, call external service, etc.
    # result = await database.save_order(order_id, customer_id, amount)
    # await payment_service.charge(customer_id, amount)
    
    return {
        "order_id": order_id,
        "status": "processed",
        "processed_at": "2025-01-01T12:00:00Z"
    }


async def send_order_notification(customer_id: int, order_id: int, amount: float):
    """
    Send notification to customer about order.
    """
    logger.info(f"Sending notification to customer {customer_id} about order {order_id}")
    # Example: Send email, push notification, etc.
    # await email_service.send(customer_id, f"Order {order_id} created: ${amount}")


async def update_order_status(order_id: int, status: OrderStatus):
    """
    Update order status in database.
    """
    logger.info(f"Updating order {order_id} status to {status}")
    # Example: Database update
    # await database.update_order_status(order_id, status)


@orders_handler("created")
async def on_order_created(msg: KafkaMessage[OrderData, OrderHeaders]):
    """
    Handle order creation.
    Models are inferred from KafkaMessage type annotation.
    """
    logger.info(f"Order {msg.data.id} created for customer {msg.data.customer_id}")
    logger.info(f"Amount: ${msg.data.amount}, Source: {msg.headers.source}")
    
    # Call business logic function
    result = await process_order(
        order_id=msg.data.id,
        customer_id=msg.data.customer_id,
        amount=msg.data.amount
    )
    
    # Send notification
    await send_order_notification(
        customer_id=msg.data.customer_id,
        order_id=msg.data.id,
        amount=msg.data.amount
    )
    
    # Send to processing topic
    # Note: producer must be started (usually in lifespan)
    await producer.send_message(
        topic="orders.processing",
        data=result,
        headers={"source": "handler"}
    )


@orders_handler(
    "updates",
    headers_filter={"priority": "high"}  # Only process high priority orders
)
async def on_order_update(msg: KafkaMessage[OrderData, OrderHeaders]):
    """
    Handle order updates with header filtering.
    Body is only deserialized if priority is "high".
    Models are inferred from KafkaMessage type annotation.
    """
    logger.info(f"High priority order update: {msg.data.id} -> {msg.data.status}")
    
    # Call function to update order status
    await update_order_status(
        order_id=msg.data.id,
        status=msg.data.status
    )
    
    # Additional business logic
    if msg.data.status == OrderStatus.COMPLETED:
        await send_order_notification(
            customer_id=msg.data.customer_id,
            order_id=msg.data.id,
            amount=msg.data.amount
        )
```

#### `api/kafka/handlers/payments/schemas.py`

```python
from pydantic import BaseModel

class PaymentData(BaseModel):
    order_id: int
    amount: float
    method: str

class PaymentHeaders(BaseModel):
    source: str
    transaction_id: str
```

#### `api/kafka/handlers/payments/handler.py`

```python
import logging
from fastkafka2 import KafkaHandler, KafkaMessage
from .schemas import PaymentData, PaymentHeaders

logger = logging.getLogger(__name__)

payments_handler = KafkaHandler(prefix="payments")


# Business logic functions
async def validate_payment(order_id: int, amount: float, method: str) -> bool:
    """
    Validate payment details.
    """
    logger.info(f"Validating payment for order {order_id}: ${amount} via {method}")
    # Example: Check payment method, validate amount, etc.
    # is_valid = await payment_gateway.validate(order_id, amount, method)
    return True


async def record_payment_transaction(
    order_id: int,
    amount: float,
    method: str,
    transaction_id: str
) -> dict:
    """
    Record payment transaction in database.
    """
    logger.info(f"Recording payment transaction {transaction_id} for order {order_id}")
    # Example: Save to database
    # transaction = await database.save_payment({
    #     "order_id": order_id,
    #     "amount": amount,
    #     "method": method,
    #     "transaction_id": transaction_id
    # })
    return {
        "transaction_id": transaction_id,
        "order_id": order_id,
        "status": "recorded"
    }


async def notify_payment_success(customer_id: int, order_id: int, amount: float):
    """
    Notify customer about successful payment.
    """
    logger.info(f"Notifying customer {customer_id} about payment for order {order_id}")
    # Example: Send notification
    # await notification_service.send(
    #     customer_id,
    #     f"Payment of ${amount} processed for order {order_id}"
    # )


@payments_handler("processed")
async def on_payment_processed(msg: KafkaMessage[PaymentData, PaymentHeaders]):
    """
    Handle payment processing.
    Demonstrates calling multiple business logic functions.
    """
    logger.info(
        f"Payment processed for order {msg.data.order_id}: "
        f"${msg.data.amount} via {msg.data.method}"
    )
    logger.info(f"Transaction ID: {msg.headers.transaction_id}")
    
    # Validate payment
    is_valid = await validate_payment(
        order_id=msg.data.order_id,
        amount=msg.data.amount,
        method=msg.data.method
    )
    
    if not is_valid:
        logger.error(f"Invalid payment for order {msg.data.order_id}")
        return
    
    # Record transaction
    transaction = await record_payment_transaction(
        order_id=msg.data.order_id,
        amount=msg.data.amount,
        method=msg.data.method,
        transaction_id=msg.headers.transaction_id
    )
    
    # Notify customer (example: get customer_id from order)
    # customer_id = await get_customer_id_from_order(msg.data.order_id)
    # await notify_payment_success(customer_id, msg.data.order_id, msg.data.amount)
    
    logger.info(f"Payment processing completed: {transaction}")
```

#### `api/kafka/handlers/base_handler.py`

```python
from fastkafka2 import KafkaHandler
from api.kafka.handlers.orders.handler import orders_handler
from api.kafka.handlers.payments.handler import payments_handler

# Base handler that combines all handler groups
base_handler = KafkaHandler()

base_handler.include_handler(orders_handler)
base_handler.include_handler(payments_handler)
```

#### `api/kafka/lifespan.py`

```python
import logging
from contextlib import asynccontextmanager
from fastkafka2 import KafkaApp, KafkaProducer
from api.kafka.handlers.base_handler import base_handler

logger = logging.getLogger(__name__)

# Create producer instance for lifespan
kafka_producer = KafkaProducer(bootstrap_servers="127.0.0.1:9092")

@asynccontextmanager
async def lifespan(app: KafkaApp):
    """
    Application lifespan context manager.
    Handles startup and shutdown logic.
    """
    logger.info("Starting Kafka application...")
    try:
        # Start producer
        await kafka_producer.start()
        logger.info("Kafka producer started")
        
        yield
        
        logger.info("Application running...")
    finally:
        # Cleanup on shutdown
        await kafka_producer.stop()
        logger.info("Kafka producer stopped")
        logger.info("Application shutdown complete")

# Create Kafka app
app = KafkaApp(
    title="Order Processing Service",
    description="Kafka-based order and payment processing microservice",
    bootstrap_servers="127.0.0.1:9092",
    group_id="order_service",
    lifespan=lifespan,
)

# Include handlers
app.include_handler(base_handler)
```

#### `main.py`

```python
import asyncio
import logging
from api.kafka.lifespan import app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    # Run the application
    # Handles SIGINT/SIGTERM for graceful shutdown
    asyncio.run(app.run())
```

## Quick Start

### Basic Handler

```python
from fastkafka2 import KafkaHandler, KafkaMessage

handler = KafkaHandler()

@handler("example")
async def example_handler(message: KafkaMessage):
    print(f"Received: {message.data}")
    print(f"Headers: {message.headers}")
```

### Typed Validation

You can get strong typing and validation like in FastAPI using function annotations. **Models are automatically extracted from `KafkaMessage[Data, Headers]` type annotation:**

```python
from pydantic import BaseModel
from fastkafka2 import KafkaHandler, KafkaMessage

class OrderData(BaseModel):
    id: int
    amount: float
    customer: str

class OrderHeaders(BaseModel):
    source: str
    priority: str

handler = KafkaHandler()

# Models are automatically inferred from KafkaMessage[OrderData, OrderHeaders] annotation
# No need to specify data_model or headers_model in decorator!
@handler("orders")
async def on_order(msg: KafkaMessage[OrderData, OrderHeaders]):
    # msg.data and msg.headers are fully typed and validated
    # IDE will autocomplete: msg.data.id, msg.data.amount, etc.
    print(f"Order {msg.data.id} for {msg.data.customer}: ${msg.data.amount}")
    print(f"Source: {msg.headers.source}, Priority: {msg.headers.priority}")
```

**Important:** The `Data` and `Headers` types in `KafkaMessage[Data, Headers]` must be Pydantic `BaseModel` classes. They are automatically extracted and used for validation.

**Nested classes are supported:** You can use nested classes like `Topic.Message.Data` and `Topic.Headers`:

```python
class MachinesUpdatesTopic:
    class Headers(BaseModel):
        machine_id: str
        message_type: str
    
    class CellStatusMessage:
        class Data(BaseModel):
            cell_id: int
            status: str

handler = KafkaHandler()

@handler("machines_updates", headers_filter={"message_type": "cell_status_update"})
async def handle_cell_status(
    msg: KafkaMessage[
        MachinesUpdatesTopic.CellStatusMessage.Data,
        MachinesUpdatesTopic.Headers,
    ],
):
    # Models are automatically extracted from nested classes!
    cell_id = msg.data.cell_id
    machine_id = msg.headers.machine_id
```

### Header Filtering (Fast!)

One of the key performance features: **message body is only deserialized when handler accepts the message**.

This means you can filter messages by headers without deserializing the body, which is much faster:

```python
from fastkafka2 import KafkaHandler, KafkaMessage

handler = KafkaHandler()

# Filter by exact header match (dict)
@handler(
    "events",
    headers_filter={"message_type": "order_created"}  # Only process this type
)
async def handle_order_created(msg: KafkaMessage[OrderData, OrderHeaders]):
    print(f"Order created: {msg.data.id}")

# Filter by custom function
@handler(
    "events",
    headers_filter=lambda h: h.get("priority") == "high"  # Custom filter
)
async def handle_high_priority(msg: KafkaMessage[OrderData, OrderHeaders]):
    print(f"High priority order: {msg.data.id}")
```

**Performance Note**: When a message arrives:
1. Headers are read immediately (fast)
2. Handlers are filtered by headers (fast)
3. **Body is deserialized ONLY if handler accepts the message** (lazy)
4. If no handler matches, body is never deserialized (saves CPU/memory)

### Handler Prefixes

Group handlers with prefixes:

```python
# All handlers will listen to "orders.*" topics
orders_handler = KafkaHandler(prefix="orders")

@orders_handler("created")  # Listens to "orders.created"
async def on_order_created(msg: KafkaMessage):
    pass

@orders_handler("cancelled")  # Listens to "orders.cancelled"
async def on_order_cancelled(msg: KafkaMessage):
    pass
```

### Combining Handlers

Combine multiple handler groups:

```python
from fastkafka2 import KafkaHandler

orders_handler = KafkaHandler(prefix="orders")
payments_handler = KafkaHandler(prefix="payments")

base_handler = KafkaHandler()
base_handler.include_handler(orders_handler)
base_handler.include_handler(payments_handler)
```

### Producer

Send messages to Kafka:

```python
from fastkafka2 import KafkaProducer
from pydantic import BaseModel

class OrderData(BaseModel):
    id: int
    amount: float

producer = KafkaProducer(bootstrap_servers="127.0.0.1:9092")

async def send_order():
    await producer.start()
    
    # Send with dict
    await producer.send_message(
        topic="orders",
        data={"id": 1, "amount": 100.0},
        headers={"source": "api"},
        key="order-1"
    )
    
    # Send with Pydantic model
    order = OrderData(id=2, amount=200.0)
    await producer.send_message(
        topic="orders",
        data=order,
        headers={"source": "api", "priority": "high"}
    )
    
    await producer.stop()
```

### Full Application Example

```python
# api/kafka/handlers/orders.py
from pydantic import BaseModel
from fastkafka2 import KafkaHandler, KafkaMessage, KafkaProducer

class OrderData(BaseModel):
    id: int
    amount: float

class OrderHeaders(BaseModel):
    source: str
    priority: str

handler = KafkaHandler(prefix="orders")
producer = KafkaProducer(bootstrap_servers="127.0.0.1:9092")

@handler("created")
async def on_order_created(msg: KafkaMessage[OrderData, OrderHeaders]):
    print(f"Order {msg.data.id} created: ${msg.data.amount}")
    
    # Send to another topic
    await producer.send_message(
        topic="orders.processed",
        data={"order_id": msg.data.id, "status": "processed"},
        headers={"source": "handler"}
    )
```

```python
# api/kafka/handlers/base.py
from fastkafka2 import KafkaHandler
from api.kafka.handlers.orders import handler as orders_handler

base_handler = KafkaHandler()
base_handler.include_handler(orders_handler)
```

```python
# api/kafka/lifespan.py
import logging
from contextlib import asynccontextmanager
from fastkafka2 import KafkaApp, KafkaProducer
from api.kafka.handlers.base import base_handler

# Producer for lifespan
kafka_producer = KafkaProducer(bootstrap_servers="127.0.0.1:9092")

@asynccontextmanager
async def lifespan(app: KafkaApp):
    logging.info("Starting lifespan")
    try:
        await kafka_producer.start()
        yield
        logging.info("Lifespan active")
    finally:
        await kafka_producer.stop()
        logging.info("Lifespan stopped")

app = KafkaApp(
    title="Kafka Gateway",
    description="Kafka-based microservice",
    bootstrap_servers="127.0.0.1:9092",
    group_id="my_service",
    lifespan=lifespan,
)

app.include_handler(base_handler)
```

```python
# main.py
import asyncio
import logging
from api.kafka.lifespan import app

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    asyncio.run(app.run())
```

## Advanced Usage

### Dependency Injection

fastkafka2 supports dependency injection for handler parameters:

```python
from fastkafka2 import KafkaHandler, KafkaMessage

class DatabaseService:
    async def get_order(self, order_id: int):
        return {"id": order_id, "status": "active"}

# Register dependency (simplified example)
# In real usage, DI container resolves dependencies automatically

handler = KafkaHandler()

@handler("orders")
async def handle_order(msg: KafkaMessage, db: DatabaseService):
    # db is automatically injected
    order = await db.get_order(msg.data.id)
    print(f"Order: {order}")
```

### Manual Consumer Configuration

You can also use consumer directly:

```python
from fastkafka2 import KafkaConsumerService

consumer = KafkaConsumerService(
    topics=["orders", "payments"],
    bootstrap_servers="127.0.0.1:9092",
    group_id="my_group",
    enable_auto_commit=False,  # Manual commit
    auto_offset_reset="earliest"
)

await consumer.start()
# Messages are processed automatically by registered handlers
await consumer.stop()
```

## Performance Optimization

### Lazy Deserialization

fastkafka2 uses lazy deserialization for optimal performance:

- **Headers are read immediately** (small, fast to parse)
- **Body remains as raw bytes** until handler accepts the message
- **Body is deserialized only when needed** (when handler matches)
- **No deserialization if no handler matches** (saves CPU/memory)

This is especially beneficial when:
- You have many handlers filtering by headers
- Most messages don't match any handler
- Message bodies are large
- You need high throughput

### Partition Ordering

Messages are processed sequentially per partition, guaranteeing order:

- Each partition has its own processing queue
- Messages in the same partition are processed in order
- Different partitions can be processed in parallel

## API Reference

### KafkaHandler

```python
handler = KafkaHandler(prefix: str = "")
```

- `prefix`: Optional prefix for all topics in this handler group

Methods:
- `handler(topic, headers_filter=None)`: Decorator for registering handlers
  - `topic`: Kafka topic name (string)
  - `headers_filter`: Optional filter for headers (dict or callable function)
  - **Models are automatically extracted** from `KafkaMessage[Data, Headers]` type annotation in function signature
  - The function must have a parameter annotated with `KafkaMessage[Data, Headers]` where `Data` and `Headers` are Pydantic `BaseModel` classes
- `include_handler(other_handler)`: Include another handler group

### KafkaApp

```python
app = KafkaApp(
    title: str,
    description: str,
    bootstrap_servers: str = "localhost:9092",
    group_id: str | None = None,
    lifespan: Callable | None = None
)
```

Methods:
- `include_handler(handler)`: Register handler group
- `start()`: Start the application
- `stop()`: Stop the application
- `run()`: Run with signal handling (SIGINT/SIGTERM)

### KafkaProducer

```python
producer = KafkaProducer(bootstrap_servers: str)
```

Methods:
- `start()`: Start the producer
- `stop()`: Stop the producer
- `send_message(topic, data, headers=None, key=None)`: Send a message

### KafkaMessage

```python
class KafkaMessage(Generic[TData, THeaders]):
    topic: str
    data: TData
    headers: THeaders
    key: str | None
```

## Requirements

- Python >= 3.10
- confluent-kafka >= 2.6, < 3
- pydantic >= 2.0
- orjson >= 3.0.0
- typing-extensions >= 4.0.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built on top of [confluent-kafka-python](https://github.com/confluentinc/confluent-kafka-python)
- Inspired by [FastAPI](https://fastapi.tiangolo.com/) for its excellent developer experience
- Uses [Pydantic](https://docs.pydantic.dev/) for data validation

## Support

For issues, questions, or contributions, please open an issue on [GitHub](https://github.com/yourusername/fastkafka2).

---

Made for the Python Kafka community
