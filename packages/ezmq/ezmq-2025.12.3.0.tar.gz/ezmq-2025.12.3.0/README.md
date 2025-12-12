# Easy Message Queue (ezmq)

A lightweight, thread-based message queue implementation in Python for managing concurrent job execution with resource management and request-response patterns.

## Quick Start

```python
from ezmq import MessageQueue, Jobs, Job, Resource

# Define a resource
class DatabaseResource(Resource):
    def _enter(self):
        return connect_to_database(self.identifier)
    
    def _exit(self):
        self._resource.close()
    
    def _peek(self):
        return read_only_connection(self.identifier)

# Define a job
class ProcessDataJob(Job):
    required_resources = ['database']
    
    def execute(self, resources, **kwargs):
        data_id = kwargs.get('data_id')
        with resources['database'] as db:
            data = db.fetch(data_id)
            return {'status': 'processed', 'data': data}

# Register jobs
class MyJobs(Jobs):
    resources = {
        'database': DatabaseResource('main.db')
    }
    process_data: ProcessDataJob

# Create and use the queue
class MyQueue(MessageQueue):
    pass

mq = MyQueue(MyJobs)

# Send a job and get response
msg_id = mq.send('process_data', data_id=123)
response = mq.receive(msg_id, timeout=10.0)

if response.success:
    print(f"Result: {response.result}")
else:
    print(f"Error: {response.error}")
```

## Core Components

### Resource

Abstract base class for managing shared resources with automatic locking.

```python
from ezmq import Resource

class MyResource(Resource):
    def _enter(self):
        # Initialize and return the resource
        return open_connection()
    
    def _exit(self):
        # Clean up the resource
        self._resource.close()
    
    def _peek(self):
        # Return read-only view without locking
        return get_read_only_view()
```

### Job

Abstract base class for creating a function to be executed.

```python
from ezmq import Job
from datetime import datetime

class EmailJob(Job):
    required_resources = ['smtp_server', 'template_engine']
    
    def execute(self, resources, **kwargs):
        to = kwargs['to']
        subject = kwargs['subject']
        
        with resources['smtp_server'] as smtp:
            smtp.send(to, subject)
        
        return {'sent': True, 'timestamp': datetime.now()}
```

### Jobs

Container class for registering and managing job types.

```python
from ezmq import Jobs

class MyJobs(Jobs):
    # Define shared resources
    resources = {
        'db': DatabaseResource('postgres://localhost/mydb'),
        'cache': CacheResource('redis://localhost'),
        'storage': FileStorageResource('/data')
    }
    
    # Register job types via type annotations
    send_email: SendEmailJob
    process_payment: ProcessPaymentJob
    generate_report: GenerateReportJob
```

### MessageQueue

Main interface for sending jobs and receiving responses.

```python
# Initialize with job types
mq = MessageQueue(MyJobs)

# Send job (returns UUID)
msg_id = mq.send('send_email', 
                 to='user@example.com',
                 subject='Welcome!')

# Receive response (blocking)
response = mq.receive(msg_id, timeout=30.0)

# Convenience method for simple cases
response = mq.send_and_receive('calculate', x=10, y=20)
```

### Response Model
```python
@dataclass
class Response:
    id: UUID           # Message ID this responds to
    success: bool      # Whether job succeeded
    error: str         # Error message if failed
    result: Any        # Return value from job.execute()
```