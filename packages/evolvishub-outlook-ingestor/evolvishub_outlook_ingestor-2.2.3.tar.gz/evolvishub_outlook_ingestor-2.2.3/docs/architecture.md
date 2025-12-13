# Architecture Documentation

This document describes the architecture and design principles of the Evolvishub Outlook Ingestor library.

## Overview

The Evolvishub Outlook Ingestor is designed as a modular, scalable, and maintainable library for ingesting emails from Microsoft Outlook servers and storing them in various databases. The architecture follows clean architecture principles with clear separation of concerns.

## Design Principles

### 1. Clean Architecture
- **Separation of Concerns**: Each layer has a single responsibility
- **Dependency Inversion**: High-level modules don't depend on low-level modules
- **Interface Segregation**: Clients depend only on interfaces they use
- **Single Responsibility**: Each class has one reason to change

### 2. SOLID Principles
- **S**ingle Responsibility Principle
- **O**pen/Closed Principle
- **L**iskov Substitution Principle
- **I**nterface Segregation Principle
- **D**ependency Inversion Principle

### 3. Design Patterns
- **Strategy Pattern**: Interchangeable protocol adapters
- **Factory Pattern**: Dynamic component creation
- **Repository Pattern**: Database abstraction
- **Observer Pattern**: Progress and metrics tracking
- **Circuit Breaker**: Fault tolerance

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Application Layer                        │
├─────────────────────────────────────────────────────────────────┤
│                     OutlookIngestor (Main API)                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   CLI Module    │  │   Web API       │  │   SDK Client    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                         Core Layer                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Configuration  │  │     Logging     │  │   Exceptions    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  Data Models    │  │ Base Processor  │  │    Ingestor     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                      Business Logic Layer                      │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Protocols     │  │   Processors    │  │   Connectors    │ │
│  │                 │  │                 │  │                 │ │
│  │ • Exchange EWS  │  │ • Email Proc.   │  │ • PostgreSQL    │ │
│  │ • Graph API     │  │ • Attachment    │  │ • MongoDB       │ │
│  │ • IMAP/POP3     │  │ • Batch Proc.   │  │ • MySQL         │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
┌─────────────────────────────────────────────────────────────────┐
│                       Utility Layer                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ Retry Logic     │  │  Rate Limiting  │  │   Performance   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Monitoring    │  │    Metrics      │  │   Validation    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### Core Components

#### 1. OutlookIngestor (Main API)
- **Purpose**: Primary interface for the library
- **Responsibilities**:
  - Orchestrate email ingestion workflow
  - Manage component lifecycle
  - Handle high-level error scenarios
  - Provide progress tracking

#### 2. Configuration Management
- **Purpose**: Centralized configuration handling
- **Features**:
  - Environment variable support
  - YAML file loading
  - Type validation with Pydantic
  - Nested configuration structures

#### 3. Data Models
- **Purpose**: Define data structures
- **Components**:
  - EmailMessage: Complete email representation
  - EmailAddress: Email address with validation
  - EmailAttachment: Attachment metadata and content
  - ProcessingResult: Operation results and metrics

### Protocol Adapters

#### Base Protocol Interface
```python
class BaseProtocol(ABC):
    async def fetch_emails(self, **kwargs) -> List[EmailMessage]
    async def fetch_emails_stream(self, **kwargs) -> AsyncGenerator[List[EmailMessage], None]
    async def get_folders(self) -> List[OutlookFolder]
    async def test_connection(self) -> bool
```

#### Exchange Web Services (EWS)
- **Library**: exchangelib
- **Features**:
  - Full Exchange Server support
  - Advanced folder operations
  - Attachment handling
  - Calendar and contact support

#### Microsoft Graph API
- **Library**: msal + aiohttp
- **Features**:
  - Modern OAuth2 authentication
  - High-performance REST API
  - Rich metadata support
  - Delta queries for incremental sync

#### IMAP/POP3
- **Library**: aioimaplib
- **Features**:
  - Standard email protocols
  - Broad server compatibility
  - Efficient message retrieval
  - Folder synchronization

### Database Connectors

#### Base Connector Interface
```python
class BaseConnector(ABC):
    async def store_email(self, email: EmailMessage) -> str
    async def store_emails_batch(self, emails: List[EmailMessage]) -> List[str]
    async def get_email(self, email_id: str) -> Optional[EmailMessage]
    async def search_emails(self, filters: Dict[str, Any]) -> List[EmailMessage]
```

#### PostgreSQL Connector
- **Library**: asyncpg + SQLAlchemy
- **Features**:
  - Async connection pooling
  - Transaction support
  - JSON field support for metadata
  - Full-text search capabilities

#### MongoDB Connector
- **Library**: motor
- **Features**:
  - Document-based storage
  - Flexible schema
  - Aggregation pipelines
  - GridFS for large attachments

#### MySQL Connector
- **Library**: aiomysql + SQLAlchemy
- **Features**:
  - Async operations
  - Connection pooling
  - Transaction support
  - Optimized for high throughput

### Processing Pipeline

#### Email Processor
- **Purpose**: Process and normalize email data
- **Features**:
  - Content extraction and cleaning
  - Metadata enrichment
  - Attachment processing
  - Duplicate detection

#### Batch Processor
- **Purpose**: Handle high-volume processing
- **Features**:
  - Configurable batch sizes
  - Parallel processing
  - Memory management
  - Progress tracking

#### Attachment Processor
- **Purpose**: Handle email attachments
- **Features**:
  - Type detection
  - Size validation
  - Content extraction
  - Storage optimization

## Data Flow

### 1. Initialization Flow
```
Configuration Loading → Component Registration → Resource Initialization → Health Checks
```

### 2. Email Ingestion Flow
```
Protocol Connection → Folder Discovery → Email Fetching → Processing → Storage → Cleanup
```

### 3. Batch Processing Flow
```
Email Batching → Parallel Processing → Result Aggregation → Error Handling → Metrics Collection
```

## Error Handling Strategy

### Exception Hierarchy
```
OutlookIngestorError (Base)
├── ConfigurationError
├── AuthenticationError
├── ProtocolError
│   ├── ExchangeError
│   ├── GraphAPIError
│   └── IMAPError
├── DatabaseError
│   ├── ConnectionError
│   ├── QueryError
│   └── TransactionError
└── ProcessingError
    ├── ValidationError
    ├── TimeoutError
    └── MemoryError
```

### Error Handling Patterns

#### 1. Retry with Exponential Backoff
```python
@retry_with_config(AGGRESSIVE_RETRY_CONFIG)
async def fetch_emails_with_retry(self):
    # Implementation with automatic retry
```

#### 2. Circuit Breaker Pattern
```python
@CircuitBreaker(failure_threshold=5, recovery_timeout=60)
async def connect_to_server(self):
    # Implementation with circuit breaker
```

#### 3. Graceful Degradation
- Continue processing other emails if one fails
- Partial results on timeout
- Fallback to alternative protocols

## Performance Considerations

### 1. Async/Await Architecture
- Non-blocking I/O operations
- Concurrent email processing
- Efficient resource utilization

### 2. Connection Pooling
- Database connection reuse
- Protocol connection management
- Resource optimization

### 3. Memory Management
- Streaming for large datasets
- Configurable memory limits
- Garbage collection optimization

### 4. Caching Strategy
- Folder structure caching
- Authentication token caching
- Metadata caching

## Scalability Design

### 1. Horizontal Scaling
- Stateless design
- Shared database backend
- Load balancing support

### 2. Vertical Scaling
- Multi-threading support
- Configurable worker pools
- Memory optimization

### 3. Partitioning Strategy
- Date-based partitioning
- Folder-based processing
- User-based distribution

## Security Architecture

### 1. Authentication
- OAuth2 for Graph API
- Secure credential storage
- Token refresh handling

### 2. Data Protection
- TLS/SSL for all connections
- Encrypted credential storage
- Audit logging

### 3. Access Control
- Least privilege principle
- Role-based permissions
- API rate limiting

## Monitoring and Observability

### 1. Metrics Collection
- Prometheus metrics
- Performance counters
- Error rates and latencies

### 2. Logging Strategy
- Structured JSON logging
- Correlation ID tracking
- Performance metrics

### 3. Health Checks
- Component health monitoring
- Dependency checks
- Automated alerting

## Testing Strategy

### 1. Unit Testing
- Individual component testing
- Mock external dependencies
- 80%+ code coverage

### 2. Integration Testing
- Component interaction testing
- Database integration
- Protocol adapter testing

### 3. Performance Testing
- Load testing with k6
- Memory usage validation
- Throughput benchmarking

### 4. End-to-End Testing
- Complete workflow validation
- Real server integration
- Error scenario testing

## Future Extensibility

### 1. Plugin Architecture
- Custom protocol adapters
- Additional database connectors
- Processing pipeline extensions

### 2. API Evolution
- Backward compatibility
- Versioned interfaces
- Migration support

### 3. Cloud Integration
- Cloud storage support
- Serverless deployment
- Container orchestration

This architecture provides a solid foundation for a scalable, maintainable, and extensible email ingestion system that can handle enterprise-scale workloads while maintaining high performance and reliability.
