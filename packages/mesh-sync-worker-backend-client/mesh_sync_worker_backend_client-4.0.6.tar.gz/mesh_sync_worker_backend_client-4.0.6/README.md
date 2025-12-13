# Worker Backend Client (Python)

Auto-generated Python client library for the Mesh-Sync worker-backend.

## Installation

### From PyPI (public registry)

```bash
pip install mesh-sync-worker-backend-client
```

### From source (development)

```bash
# Clone the repository and navigate to the generated Python client
cd generated/python

# Install in editable mode
pip install -e .
```

### From TestPyPI (testing)

```bash
pip install --index-url https://test.pypi.org/simple/ mesh-sync-worker-backend-client
```

### From a private PyPI registry (For Private Packages)

**Note:** GitHub Packages does not support Python/PyPI packages. For private Python packages, use a private PyPI registry.

Configure your `pip.conf` or `~/.pypirc`:

**For pip.conf (Linux/Mac: `~/.config/pip/pip.conf`, Windows: `%APPDATA%\pip\pip.ini`):**

```ini
[global]
index-url = https://your-registry.example.com/simple
```

**For authentication with .pypirc (`~/.pypirc`):**

```ini
[distutils]
index-servers =
    private

[private]
repository = https://your-registry.example.com
username = your_username
password = your_password
```

Then install:

```bash
pip install mesh-sync-worker-backend-client
```

## Usage

### Basic Example

```python
from worker_client import WorkerClient

# Initialize client
client = WorkerClient(
    base_url='http://localhost:3000',
    api_key='your_api_key',  # Optional
    timeout=30  # Optional, default 30s
)

# Type-safe method call
job = client.file_download_request({
    'url': 'https://example.com/file.pdf',
    'destination': '/downloads/file.pdf'
})

print(f'Job created: {job.job_id}')

# Check job status
status = client.get_job_status(job.job_id)
print(f'Job state: {status.state}')

# Close the client session
client.close()
```

### Using Context Manager

```python
from worker_client import WorkerClient

with WorkerClient(base_url='http://localhost:3000') as client:
    job = client.file_download_request({
        'url': 'https://example.com/file.pdf',
        'destination': '/downloads/file.pdf'
    })
    print(f'Job ID: {job.job_id}')
```

### Using Message Type Constants

```python
from worker_client import WorkerClient, MessageTypes

client = WorkerClient(base_url='http://localhost:3000')

# Dynamic message type
job = client.send_to_queue(MessageTypes.FILE_DOWNLOAD_REQUEST, {
    'url': 'https://example.com/file.pdf',
    'destination': '/downloads/file.pdf'
})
```

## Available Message Types


### backend-logging-event

**Description:** Centralized logging event for capturing all warn/error/failure logs from meshsync-backend.
This event is sent to ELK for centralized monitoring, alerting, and debugging.

Automatically emitted by the custom Pino logger interceptor when:
- logger.warn() is called
- logger.error() is called
- uncaught exceptions occur
- request failures happen (4xx, 5xx responses)

Used for:
- System health monitoring
- Error tracking and alerting
- Performance degradation detection
- Security incident tracking
- Compliance and audit trails


**Method:** `client.backend_logging_event(data, opts=None)`

**Payload Type:** `BackendLoggingEventMessage`

**Fields:**

- `eventType` (string) [✓]: Type of logging event

- `timestamp` (string) [✓]: ISO 8601 timestamp when the log was generated

- `level` (string) [✓]: Log level severity

- `message` (string) [✓]: Human-readable log message

- `context` (string) [✓]: Logger context (typically the class/service name)

- `requestId` (string) [✗]: Unique request ID for correlation (X-Request-Id header)

- `userId` (string) [✗]: ID of the authenticated user (if available)

- `httpMethod` (string) [✗]: HTTP method of the request

- `httpUrl` (string) [✗]: Request URL path (without query params for privacy)

- `httpStatusCode` (integer) [✗]: HTTP response status code

- `errorType` (string) [✗]: Error class/type name

- `errorStack` (string) [✗]: Stack trace (sanitized, no sensitive data)

- `errorCode` (string) [✗]: Application-specific error code for categorization

- `metadata` (object) [✗]: Additional structured context (sanitized, no PII)

- `environment` (string) [✗]: Deployment environment

- `serviceVersion` (string) [✗]: Backend service version

- `hostname` (string) [✗]: Server hostname/pod name

- `durationMs` (number) [✗]: Operation duration in milliseconds (if applicable)



### etsy-analytics-sync-completed

**Description:** Contains synced analytics data for Etsy listings. Backend stores this in etsy_analytics_snapshots table and indexes to ELK.


**Method:** `client.etsy_analytics_sync_completed(data, opts=None)`

**Payload Type:** `EtsyAnalyticsSyncCompletedMessage`

**Fields:**

- `originalJobId` (string) [✗]: 

- `status` (string) [✗]: 

- `syncedCount` (integer) [✗]: Number of listings successfully synced

- `errorCount` (integer) [✗]: Number of listings that failed

- `results` (array) [✗]: Analytics for each synced listing

- `errors` (array) [✗]: Errors for failed listings

- `syncedAt` (string) [✗]: 

- `nextScheduledSync` (string) [✗]: When next automatic sync should occur



### etsy-analytics-sync-request

**Description:** Syncs analytics data from Etsy API for one or more listings. Fetches views, favorites, sales, revenue, and traffic source data.
Can sync: - Specific listings (provide listingIds) - All user listings (provide userId, empty listingIds) - Shop-level analytics (provide shopId)


**Method:** `client.etsy_analytics_sync_request(data, opts=None)`

**Payload Type:** `EtsyAnalyticsSyncRequestMessage`

**Fields:**

- `listingIds` (array) [✗]: Internal listing IDs to sync. Empty = sync all for user.

- `userId` (string) [✗]: User whose listings to sync (if listingIds empty)

- `shopId` (string) [✗]: Etsy shop ID for shop-level analytics

- `timeRange` (object) [✗]: Date range for historical analytics

- `syncOptions` (object) [✗]: 

- `etsyCredentials` (object) [✗]: Encrypted Etsy OAuth credentials

- `webhookUrl` (string) [✗]: 



### etsy-publish-listing-completed

**Description:** Indicates completion of Etsy listing publication. Contains external Etsy listing ID and URL, or error details if failed.


**Method:** `client.etsy_publish_listing_completed(data, opts=None)`

**Payload Type:** `EtsyPublishListingCompletedMessage`

**Fields:**

- `originalJobId` (string) [✗]: BullMQ job ID from request

- `listingId` (string) [✗]: Internal marketplace_items ID

- `metamodelId` (string) [✗]: Metamodel that was published

- `materialName` (string) [✗]: Material variant name

- `status` (string) [✗]: Publication result

- `etsyListingId` (string) [✗]: External Etsy listing ID (only if status=SUCCESS)

- `etsyListingUrl` (string) [✗]: URL to view listing on Etsy (only if status=SUCCESS)

- `etsyFileId` (string) [✗]: Etsy digital file ID (only if status=SUCCESS)

- `error` (object) [✗]: Error details (only if status=FAILED)

- `publishedAt` (string) [✗]: When the listing was created (only if status=SUCCESS)

- `processingDuration` (integer) [✗]: Processing time in milliseconds



### etsy-publish-listing-request

**Description:** Publishes a single metamodel listing to Etsy for a specific material variant. Creates Etsy listing, uploads digital file, and returns external listing ID.
This message is enqueued for EACH material variant when publishing a metamodel.
Example: Publishing a metamodel with PLA, Resin, ABS materials creates 3 jobs.


**Method:** `client.etsy_publish_listing_request(data, opts=None)`

**Payload Type:** `EtsyPublishListingRequestMessage`

**Fields:**

- `listingId` (string) [✗]: Internal marketplace_items table ID

- `metamodelId` (string) [✗]: Metamodel being published

- `ownerId` (string) [✗]: User ID who owns the metamodel

- `materialVariant` (object) [✗]: Material-specific listing configuration

- `baseListingData` (object) [✗]: Common listing information

- `publishOptions` (object) [✗]: 

- `etsyCredentials` (object) [✗]: Encrypted Etsy OAuth credentials

- `fileMetadata` (object) [✗]: Digital file to upload

- `webhookUrl` (string) [✗]: Callback URL for completion notification



### file-download-completed

**Description:** Notifies that a file download has been processed, indicating success or failure.

**Method:** `client.file_download_completed(data, opts=None)`

**Payload Type:** `FileDownloadCompletedMessage`

**Fields:**

- `originalJobId` (string) [✗]: The ID of the initial 'file-download-request' job this event corresponds to.

- `modelId` (string) [✗]: The unique identifier for the downloaded model.

- `status` (string) [✗]: The final status of the download operation.

- `s3Location` (object) [✗]: Details of the file's location in Minio S3 (present on success).

- `errorMessage` (string) [✗]: Contains error details if the status is FAILED.

- `downloadedAt` (string) [✗]: The timestamp when the download was completed or failed.



### file-download-request

**Description:** Downloads model file from storage provider to MinIO for processing pipeline. Acts as parent job for thumbnail generation, technical metadata analysis, and metadata generation.

**Method:** `client.file_download_request(data, opts=None)`

**Payload Type:** `FileDownloadRequestMessage`

**Fields:**

- `modelId` (string) [✗]: The unique identifier for the model to be downloaded.

- `ownerId` (string) [✗]: The identifier of the user who owns the model. Optional - if not provided, will be retrieved from StorageConnection.

- `storageLocation` (object) [✗]: The storage location of the model.

- `minioDestination` (object) [✗]: Destination in MinIO where file will be uploaded after download.

- `autoEnqueueChildren` (boolean) [✗]: Automatically enqueue thumbnail generation, technical metadata analysis, and metadata generation jobs after download completes.

- `previewType` (string) [✗]: Preview type for thumbnail generation (passed to child job).

- `generate360Views` (boolean) [✗]: Generate 16 angle views for 360° preview (passed to child job).

- `webhookUrl` (string) [✗]: Optional webhook URL to call when download completes. If provided, worker will POST completion status to this endpoint.



### marketplace-analytics-sync-completed

**Description:** Contains synced analytics data for marketplace listings. Backend stores this in marketplace_analytics_snapshots table and indexes to ELK. Works with any marketplace provider.

**Method:** `client.marketplace_analytics_sync_completed(data, opts=None)`

**Payload Type:** `MarketplaceAnalyticsSyncCompletedMessage`

**Fields:**

- `originalJobId` (string) [✗]: BullMQ job ID from original request

- `marketplaceProvider` (string) [✗]: Marketplace provider type (etsy, ebay, etc.)

- `status` (string) [✗]: Sync result (SUCCESS, PARTIAL_SUCCESS, or FAILED)

- `syncedCount` (integer) [✗]: Number of listings successfully synced

- `errorCount` (integer) [✗]: Number of listings that failed

- `results` (array) [✗]: Analytics for each synced listing

- `errors` (array) [✗]: Errors for failed listings

- `syncedAt` (string) [✗]: When sync completed (ISO 8601)

- `nextScheduledSync` (string) [✗]: When next automatic sync should occur (ISO 8601)



### marketplace-analytics-sync-request

**Description:** Syncs analytics data from marketplace API for one or more listings. Fetches views, favorites, sales, revenue, and traffic source data. Can sync: specific listings, all user listings, or shop-level analytics. Works with any marketplace provider that supports analytics (etsy, ebay, etc.).

**Method:** `client.marketplace_analytics_sync_request(data, opts=None)`

**Payload Type:** `MarketplaceAnalyticsSyncRequestMessage`

**Fields:**

- `marketplaceProvider` (string) [✗]: Marketplace provider type (etsy, ebay, etc.)

- `marketplaceConnectionId` (string) [✗]: UUID of the marketplace connection configuration

- `listingIds` (array) [✗]: Internal listing UUIDs to sync. Empty array = sync all for user.

- `userId` (string) [✗]: UUID of user whose listings to sync (if listingIds empty)

- `externalShopId` (string) [✗]: External marketplace shop ID for shop-level analytics

- `timeRange` (object) [✗]: Date range for historical analytics

- `syncOptions` (object) [✗]: Optional sync configuration

- `marketplaceCredentials` (object) [✗]: Encrypted marketplace credentials (retrieved from marketplaceConnectionId)

- `webhookUrl` (string) [✗]: Callback URL for completion notification



### marketplace-connection-sync-completed

**Description:** Notification that marketplace connection sync has completed. Contains updated connection metadata, profile information, and sync statistics.


**Method:** `client.marketplace_connection_sync_completed(data, opts=None)`

**Payload Type:** `MarketplaceConnectionSyncCompletedMessage`

**Fields:**

- `requestId` (string) [✗]: Original request ID for correlation

- `connectionId` (string) [✗]: Marketplace connection that was synced

- `marketplaceId` (string) [✗]: Marketplace provider ID

- `userId` (string) [✗]: Connection owner user ID

- `status` (string) [✗]: Overall sync result status

- `syncType` (string) [✗]: Type of sync that was performed

- `connectionData` (object) [✗]: Updated connection information

- `categories` (array) [✗]: Available marketplace categories

- `statistics` (object) [✗]: Sync operation statistics

- `completedAt` (string) [✗]: When sync completed

- `error` (object) [✗]: Error details if sync failed



### marketplace-connection-sync-request

**Description:** Requests synchronization of marketplace connection data including: - Profile information and shop details - Account status and permissions - Available categories and shipping profiles - Rate limits and API quotas
This is typically triggered after initial connection or periodically to keep marketplace metadata up to date.


**Method:** `client.marketplace_connection_sync_request(data, opts=None)`

**Payload Type:** `MarketplaceConnectionSyncRequestMessage`

**Fields:**

- `connectionId` (string) [✗]: Internal marketplace connection ID

- `marketplaceId` (string) [✗]: Marketplace provider ID (etsy, ebay, etc.)

- `userId` (string) [✗]: User who owns this connection

- `syncType` (string) [✗]: Type of sync to perform

- `priority` (string) [✗]: Processing priority

- `requestId` (string) [✗]: Unique request identifier for tracking

- `webhookUrl` (string) [✗]: Webhook URL to call when sync completes

- `metadata` (object) [✗]: Additional context data



### marketplace-credential-rotation-completed

**Description:** Notification that marketplace credential rotation has completed. Contains the rotation results, new credential metadata, and any issues encountered.


**Method:** `client.marketplace_credential_rotation_completed(data, opts=None)`

**Payload Type:** `MarketplaceCredentialRotationCompletedMessage`

**Fields:**

- `requestId` (string) [✗]: Original rotation request ID

- `connectionId` (string) [✗]: Marketplace connection that was rotated

- `marketplaceId` (string) [✗]: Marketplace provider ID

- `userId` (string) [✗]: Connection owner user ID

- `status` (string) [✗]: Overall rotation operation status

- `rotationType` (string) [✗]: Type of rotation that was performed

- `reason` (string) [✗]: Original reason for rotation

- `newCredentials` (object) [✗]: Metadata about new credentials

- `oldCredentials` (object) [✗]: Status of previous credentials

- `operationDetails` (object) [✗]: Details of the rotation operation

- `connectionStatus` (object) [✗]: Connection status after credential rotation

- `nextRotation` (object) [✗]: Information about next scheduled rotation

- `error` (object) [✗]: Error details if rotation failed

- `notifications` (array) [✗]: Notifications sent as part of rotation



### marketplace-credential-rotation-request

**Description:** Requests rotation/refresh of marketplace connection credentials. This is used for: - OAuth token refresh when tokens are near expiry - API key rotation for enhanced security - Re-authentication after connection errors - Scheduled credential updates


**Method:** `client.marketplace_credential_rotation_request(data, opts=None)`

**Payload Type:** `MarketplaceCredentialRotationRequestMessage`

**Fields:**

- `connectionId` (string) [✗]: Marketplace connection ID requiring credential rotation

- `marketplaceId` (string) [✗]: Marketplace provider ID (etsy, ebay, etc.)

- `userId` (string) [✗]: User who owns the connection

- `rotationType` (string) [✗]: Type of credential rotation to perform

- `reason` (string) [✗]: Reason for credential rotation

- `urgency` (string) [✗]: How urgently the rotation is needed

- `currentCredentials` (object) [✗]: Current credential metadata (no actual secrets)

- `options` (object) [✗]: Rotation configuration options

- `requestId` (string) [✗]: Unique request identifier

- `webhookUrl` (string) [✗]: Webhook URL for completion notification

- `scheduledAt` (string) [✗]: When this rotation was scheduled (if scheduled)

- `metadata` (object) [✗]: Additional request context



### marketplace-listing-sync-completed

**Description:** Notification that marketplace listing sync operation has completed. Contains detailed results of the sync including created/updated listings, errors encountered, and performance statistics.


**Method:** `client.marketplace_listing_sync_completed(data, opts=None)`

**Payload Type:** `MarketplaceListingSyncCompletedMessage`

**Fields:**

- `requestId` (string) [✗]: Original request ID for correlation

- `connectionId` (string) [✗]: Marketplace connection that was synced

- `marketplaceId` (string) [✗]: Marketplace provider ID

- `userId` (string) [✗]: Connection owner user ID

- `status` (string) [✗]: Overall sync operation status

- `syncDirection` (string) [✗]: Direction of sync that was performed

- `statistics` (object) [✗]: Detailed sync operation statistics

- `results` (object) [✗]: Detailed sync results by operation

- `successfulListings` (array) [✗]: Details of successfully processed listings

- `failedListings` (array) [✗]: Details of listings that failed to sync

- `errors` (array) [✗]: Non-listing-specific errors encountered

- `completedAt` (string) [✗]: When sync operation completed

- `nextSyncRecommendedAt` (string) [✗]: When next sync is recommended



### marketplace-listing-sync-request

**Description:** Requests synchronization of marketplace listings for a connection. Can sync specific listings or all listings for a marketplace connection.
Includes bidirectional sync: - Pull: Fetch listings from marketplace to update local database - Push: Update marketplace listings with local changes - Full: Both pull and push operations


**Method:** `client.marketplace_listing_sync_request(data, opts=None)`

**Payload Type:** `MarketplaceListingSyncRequestMessage`

**Fields:**

- `connectionId` (string) [✗]: Marketplace connection ID

- `marketplaceId` (string) [✗]: Marketplace provider ID (etsy, ebay, etc.)

- `userId` (string) [✗]: User who owns the connection

- `syncDirection` (string) [✗]: Direction of sync operation

- `syncScope` (string) [✗]: Scope of listings to sync

- `listingIds` (array) [✗]: Specific listing IDs to sync (if syncScope=specific)

- `externalListingIds` (array) [✗]: External marketplace listing IDs to sync

- `options` (object) [✗]: Sync configuration options

- `priority` (string) [✗]: Processing priority

- `requestId` (string) [✗]: Unique request identifier

- `webhookUrl` (string) [✗]: Webhook URL for completion notification

- `metadata` (object) [✗]: Additional request context



### marketplace-publish-listing-completed

**Description:** Indicates completion of marketplace listing publication. Contains external listing ID and URL, or error details if failed. Works with any marketplace provider (etsy, ebay, etc.).

**Method:** `client.marketplace_publish_listing_completed(data, opts=None)`

**Payload Type:** `MarketplacePublishListingCompletedMessage`

**Fields:**

- `originalJobId` (string) [✗]: BullMQ job ID from original request

- `listingId` (string) [✗]: Internal marketplace_items UUID

- `metamodelId` (string) [✗]: UUID of the metamodel that was published

- `marketplaceProvider` (string) [✗]: Marketplace provider type (etsy, ebay, etc.)

- `materialName` (string) [✗]: Material variant name

- `status` (string) [✗]: Publication result (SUCCESS or FAILED)

- `externalListingId` (string) [✗]: External marketplace listing ID (only if status=SUCCESS)

- `externalListingUrl` (string) [✗]: URL to view listing on marketplace (only if status=SUCCESS)

- `externalFileId` (string) [✗]: External marketplace file ID (only if status=SUCCESS)

- `error` (object) [✗]: Error details (only if status=FAILED)

- `publishedAt` (string) [✗]: When the listing was created (ISO 8601, only if status=SUCCESS)

- `processingDuration` (integer) [✗]: Processing time in milliseconds



### marketplace-publish-listing-request

**Description:** Publishes a single metamodel listing to a marketplace for a specific material variant. Creates listing, uploads digital file, and returns external listing ID. This message is enqueued for EACH material variant when publishing a metamodel. The marketplace type (etsy, ebay, etc.) is determined by the marketplaceProvider field.

**Method:** `client.marketplace_publish_listing_request(data, opts=None)`

**Payload Type:** `MarketplacePublishListingRequestMessage`

**Fields:**

- `listingId` (string) [✗]: Internal marketplace_items table UUID

- `metamodelId` (string) [✗]: UUID of the metamodel being published

- `ownerId` (string) [✗]: UUID of the user who owns the metamodel

- `marketplaceProvider` (string) [✗]: Marketplace provider type (etsy, ebay, leboncoin, etc.)

- `marketplaceConnectionId` (string) [✗]: UUID of the marketplace connection configuration

- `materialVariant` (object) [✗]: Material-specific listing configuration

- `baseListingData` (object) [✗]: Common listing information shared across variants

- `publishOptions` (object) [✗]: Publishing configuration (marketplace-specific options)

- `marketplaceCredentials` (object) [✗]: Encrypted marketplace credentials (retrieved from marketplaceConnectionId)

- `fileMetadata` (object) [✗]: Digital file to upload

- `webhookUrl` (string) [✗]: Callback URL for completion notification



### media-batch-download-completed

**Description:** Notifies that a batch media download has been completed.

**Method:** `client.media_batch_download_completed(data, opts=None)`

**Payload Type:** `MediaBatchDownloadCompletedMessage`

**Fields:**

- `batchId` (string) [✓]: The unique identifier for the batch download operation.

- `status` (string) [✓]: The final status of the batch download operation.

- `processedFiles` (array) [✗]: List of successfully processed files.

- `failedFiles` (array) [✗]: List of files that failed to process.

- `processedAt` (string) [✓]: Timestamp when the batch processing completed.

- `statistics` (object) [✗]: Statistics about the batch processing.



### media-batch-download-request

**Description:** Request to download and process a batch of media files from a storage provider. Images are compressed and resized to specified dimensions, converted to WebP format. Text files and documents are processed and stored with metadata. All processed files are uploaded to MinIO S3 storage under the media/{batchId}/ prefix.


**Method:** `client.media_batch_download_request(data, opts=None)`

**Payload Type:** `MediaBatchDownloadRequestMessage`

**Fields:**

- `batchId` (string) [✗]: Unique identifier for this batch of media files. Used for organizing processed files in S3 storage (media/{batchId}/) and correlating with completion responses.


- `storageConnectionId` (string) [✗]: UUID of the StorageConnection entity from which to download the media files. Used to authenticate and access the source storage provider.


- `mediaFiles` (array) [✗]: Array of media files to download and process. Must contain at least one file. Each file includes metadata for identification and processing.


- `compressionSettings` (object) [✗]: Optional compression settings that override deployment environment defaults. If not provided, uses values from MAX_IMAGE_WIDTH, MAX_IMAGE_HEIGHT, IMAGE_QUALITY, and OUTPUT_FORMAT environment variables.




### metamodel-metadata-generation-completed

**Description:** Handles metamodel metadata generation completion. Contains AI-generated metadata and aggregated technical analysis.

**Method:** `client.metamodel_metadata_generation_completed(data, opts=None)`

**Payload Type:** `MetamodelMetadataGenerationCompletedMessage`

**Fields:**

- `metamodelId` (string) [✓]: The unique identifier for the metamodel

- `metadata` (object) [✓]: AI-generated metadata for the metamodel

- `technicalMetadata` (object) [✓]: Aggregated technical analysis from constituent models



### metamodel-metadata-generation-request

**Description:** Handles metamodel metadata generation requests via Ollama. Aggregates data from constituent models and generates AI-enhanced metadata.

**Method:** `client.metamodel_metadata_generation_request(data, opts=None)`

**Payload Type:** `MetamodelMetadataGenerationRequestMessage`

**Fields:**

- `metamodelId` (string) [✗]: The unique identifier for the metamodel

- `constituentModelIds` (array) [✗]: Array of model IDs that compose this metamodel

- `name` (string) [✗]: The name of the metamodel

- `ownerId` (string) [✗]: The owner's user ID

- `libraryId` (string) [✗]: The library containing this metamodel

- `constituentModels` (array) [✗]: Enriched metadata for constituent models (includes storage items)

- `webhookUrl` (string) [✗]: Optional webhook URL for async completion notification



### model-analytics-collection-request

**Description:** Request to collect marketplace analytics for a specific metamodel.
Triggered by backend scheduler every 6 hours for popular/tagged metamodels.

Worker performs targeted market searches based on metamodel metadata
and stores aggregated statistics in Elasticsearch for trend analysis.


**Method:** `client.model_analytics_collection_request(data, opts=None)`

**Payload Type:** `ModelAnalyticsCollectionRequestMessage`

**Fields:**

- `metamodelId` (string) [✓]: The metamodel ID to collect analytics for

- `ownerId` (string) [✓]: Owner user ID for audit trail

- `primaryCategory` (string) [✗]: Primary classification category (e.g., "miniature", "terrain")

- `subCategory` (string) [✗]: Sub-category for more specific targeting

- `tags` (array) [✗]: Relevant tags from metamodel metadata (max 10)

- `franchise` (string) [✗]: Franchise name if detected (e.g., "Dungeons & Dragons")

- `confidence` (number) [✗]: Classification confidence score

- `priority` (string) [✗]: Collection priority level

- `triggeredBy` (string) [✗]: Source of trigger (e.g., "backend-scheduler", "manual")

- `triggeredAt` (string) [✗]: Timestamp when collection was triggered



### model-discovery-folder-processed-event

**Description:** Handles model discovery folder processed events.

**Method:** `client.model_discovery_folder_processed_event(data, opts=None)`

**Payload Type:** `ModelDiscoveryFolderProcessedEventMessage`

**Fields:**

- `connectionId` (string) [✗]: The unique identifier for the connection.

- `folderPath` (string) [✗]: The path to the processed folder.

- `discoveredFiles` (array) [✗]: A list of files discovered in the folder.

- `folderSignature` (object) [✗]: A signature representing the state of the folder.

- `processedAt` (string) [✗]: The timestamp when the folder was processed.

- `statistics` (object) [✗]: Statistics about the processed folder.



### model-discovery-scan-found-event

**Description:** Handles model discovery scan found events.

**Method:** `client.model_discovery_scan_found_event(data, opts=None)`

**Payload Type:** `ModelDiscoveryScanFoundEventMessage`

**Fields:**

- `modelId` (string) [✗]: The unique identifier for the model.

- `name` (string) [✗]: The name of the model.

- `fileName` (string) [✗]: The name of the model file.

- `description` (string) [✗]: A description of the model.

- `fileTypes` (array) [✗]: An array of file types associated with the model.

- `size` (number) [✗]: The size of the model file in bytes.

- `storageLocation` (object) [✗]: The storage location of the model.

- `providerType` (string) [✗]: The type of the storage provider.

- `metadata` (object) [✗]: A flexible object for additional metadata.



### model-discovery-scan-progress-event

**Description:** Handles model discovery scan progress events.

**Method:** `client.model_discovery_scan_progress_event(data, opts=None)`

**Payload Type:** `ModelDiscoveryScanProgressEventMessage`

**Fields:**

- `payload` (object) [✗]: Contains the discovery scan progress details.



### model-discovery-scan-request

**Description:** Handles model discovery scan requests events.

**Method:** `client.model_discovery_scan_request(data, opts=None)`

**Payload Type:** `ModelDiscoveryScanRequestMessage`

**Fields:**

- `libraryId` (string) [✗]: The ID of the library to scan.

- `storageConnectionId` (string) [✗]: The ID of the storage connection to scan.

- `providerType` (string) [✗]: The type of the storage provider.

- `path` (string) [✗]: The specific path within the storage connection to scan for this library.



### model-metadata-generation-completed

**Description:** Notifies backend that enriched marketplace metadata generation completed. Backend updates Model entity with generated description, tags, classification, etc.

**Method:** `client.model_metadata_generation_completed(data, opts=None)`

**Payload Type:** `ModelMetadataGenerationCompletedMessage`

**Fields:**

- `modelId` (string) [✓]: UUID of the model that was processed.

- `metadata` (object) [✓]: Enriched marketplace metadata generated by LLM.



### model-metadata-generation-request

**Description:** Generates enriched marketplace metadata (SEO descriptions, tags, categories) for 3D models using LLM vision analysis of thumbnails by default. Worker queries database by modelId to retrieve: Model (fileName, fileSize, ownerId, storageItem), TechnicalMetadata (geometry, quality, printability), and ThumbnailMedia (required for default vision analysis). Prerequisites: file download completed, technical metadata analysis completed (strongly recommended), thumbnail generation completed (REQUIRED for vision-enhanced analysis, default behavior). Vision analysis can be disabled via ENABLE_VISION_METADATA_GENERATION environment variable (default: true).

**Method:** `client.model_metadata_generation_request(data, opts=None)`

**Payload Type:** `ModelMetadataGenerationRequestMessage`

**Fields:**

- `modelId` (string) [✗]: UUID of the model to generate metadata for. Worker queries database to retrieve: 1) Model entity (name, fileName, fileSize, ownerId, storageItem relationship), 2) Model.technicalMetadata relationship (vertices, faces, quality scores, printability metrics), 3) AssociatedMedia.thumbnails (via associatedMediaId) for vision-enhanced analysis. All data fetched from PostgreSQL - no additional parameters required.

- `parentJobId` (string) [✗]: ID of parent thumbnail-generation job for BullMQ dependency tracking. SHOULD be set to thumbnail-generation job ID to ensure thumbnails are ready before metadata generation (required for default vision analysis). If omitted, worker will check for thumbnail existence and wait/retry if ENABLE_VISION_METADATA_GENERATION=true.



### model-metamodel-detection-found

**Description:** Handles model metamodel detection found with hierarchical relationships.

**Method:** `client.model_metamodel_detection_found(data, opts=None)`

**Payload Type:** `ModelMetamodelDetectionFoundMessage`

**Fields:**

- `metamodels` (array) [✓]: List of metamodel nodes in hierarchical structure (roots and children).



### model-metamodel-detection-request

**Description:** Handles model metamodel detection requests.

**Method:** `client.model_metamodel_detection_request(data, opts=None)`

**Payload Type:** `ModelMetamodelDetectionRequestMessage`

**Fields:**

- `connectionId` (string) [✓]: The unique identifier for the storage connection.

- `folderPath` (string) [✓]: The path to the folder that was processed.

- `discoveredFiles` (array) [✓]: A list of files discovered in the folder.

- `folderSignature` (object) [✓]: A signature representing the state of the folder.

- `processedAt` (string) [✓]: The timestamp when the folder was processed.

- `statistics` (object) [✓]: Statistics about the processed folder.



### model-sellability-analysis-completed

**Description:** Contains sellability analysis results including Etsy-specific recommendations, material pricing, and marketplace compatibility scores

**Method:** `client.model_sellability_analysis_completed(data, opts=None)`

**Payload Type:** `ModelSellabilityAnalysisCompletedMessage`

**Fields:**

- `metamodelId` (string) [✗]: Metamodel UUID

- `ownerId` (string) [✗]: Owner user ID

- `sellabilityScore` (number) [✗]: Overall sellability score (0-100)

- `pricingRecommendations` (object) [✗]: Pricing analysis and recommendations with material-specific pricing (v2.0.0)

- `marketplaceRecommendations` (array) [✗]: Recommended marketplaces with Etsy-specific scoring (v2.0.0)

- `demandAnalysis` (object) [✗]: Market demand insights

- `qualityFactors` (object) [✗]: Quality-related factors affecting sellability

- `recommendations` (array) [✗]: Actionable recommendations to improve sellability

- `analyzedAt` (string) [✗]: Analysis completion timestamp (ISO 8601)

- `analysisVersion` (string) [✗]: Analysis algorithm version

- `error` (object) [✗]: Error information if analysis failed



### model-sellability-analysis-request

**Description:** Analyzes a metamodel to determine sellability score, pricing recommendations, and optimal marketplace selection. Enhanced with Etsy-specific analysis including competitor pricing, category demand trends, and material suitability.

**Method:** `client.model_sellability_analysis_request(data, opts=None)`

**Payload Type:** `ModelSellabilityAnalysisRequestMessage`

**Fields:**

- `metamodelId` (string) [✗]: UUID of the metamodel to analyze. Worker will fetch all model metadata, technical metadata, enriched metadata, and child models from PostgreSQL.

- `ownerId` (string) [✗]: UUID of the user who owns the metamodel

- `analysisOptions` (object) [✗]: Optional analysis configuration



### model-semantic-analysis-completed

**Description:** Handles completion of 3D model semantic analysis with generated tags and similarity results.

**Method:** `client.model_semantic_analysis_completed(data, opts=None)`

**Payload Type:** `ModelSemanticAnalysisCompletedMessage`

**Fields:**

- `modelId` (string) [✗]: The unique identifier for the model.

- `userId` (string) [✗]: The user ID who owns the model.

- `processingStatus` (string) [✗]: Final processing status.

- `semanticMetadata` (object) [✗]: Generated semantic metadata and analysis results.

- `processingTime` (object) [✗]: Processing performance metrics.

- `qualityMetrics` (object) [✗]: Processing quality and confidence metrics.

- `error` (object) [✗]: Error information if processing failed.

- `debugInfo` (object) [✗]: Additional debug information for troubleshooting.



### model-semantic-analysis-request

**Description:** Handles 3D model semantic analysis requests using ULIP-2 neural networks and FAISS vector similarity search.

**Method:** `client.model_semantic_analysis_request(data, opts=None)`

**Payload Type:** `ModelSemanticAnalysisRequestMessage`

**Fields:**

- `modelId` (string) [✗]: The unique identifier for the model.

- `userId` (string) [✗]: The user ID who owns the model.

- `storageConnectionId` (string) [✗]: The ID of the storage connection.

- `filePath` (string) [✗]: The path to the 3D model file in storage.

- `fileName` (string) [✗]: The name of the model file.

- `fileSize` (number) [✗]: The size of the model file in bytes.

- `storageProviderType` (string) [✗]: The type of the storage provider (S3, GoogleDrive, SFTP, etc).

- `processingOptions` (object) [✗]: Configuration options for semantic analysis.

- `priority` (number) [✗]: Processing priority (1=highest, 10=lowest).

- `webhookUrl` (string) [✗]: Optional webhook URL for completion notification.

- `retryCount` (number) [✗]: Current retry attempt number.



### model-technical-metadata-completed

**Description:** Reports comprehensive results of technical metadata analysis including geometry, quality metrics, and print-readiness assessment

**Method:** `client.model_technical_metadata_completed(data, opts=None)`

**Payload Type:** `ModelTechnicalMetadataCompletedMessage`

**Fields:**

- `originalJobId` (string) [✗]: ID of the original analysis request job

- `modelId` (string) [✗]: ID of the analyzed model

- `status` (string) [✗]: Analysis completion status

- `vertices` (integer) [✗]: Number of vertices in the mesh

- `faces` (integer) [✗]: Number of faces/polygons in the mesh

- `edges` (integer) [✗]: Number of edges in the mesh

- `detailLevel` (string) [✗]: Visual detail level based on polygon density

- `boundingBox` (object) [✗]: 3D bounding box dimensions in millimeters

- `volumeCubicMm` (number) [✗]: Model volume in cubic millimeters (for material calculation)

- `surfaceAreaSqMm` (number) [✗]: Total surface area in square millimeters

- `minWallThickness` (number) [✗]: Minimum wall thickness detected in millimeters (critical for printability)

- `maxWallThickness` (number) [✗]: Maximum wall thickness detected in millimeters

- `manifold` (boolean) [✗]: Is the mesh watertight/manifold? Critical for 3D printing (true = printable)

- `nonManifoldEdges` (integer) [✗]: Number of non-manifold edges (repair needed if > 0)

- `holes` (integer) [✗]: Number of holes/boundary loops in the mesh (0 = closed mesh)

- `flippedNormals` (integer) [✗]: Number of faces with inverted normals (causes rendering/slicing issues)

- `selfIntersections` (integer) [✗]: Number of self-intersecting faces (0 = clean geometry)

- `qualityScore` (number) [✗]: Overall quality score 0-100 (100 = perfect for printing, <60 needs repair)

- `printabilityScore` (number) [✗]: Printability score 0-100 (considers supports, orientation, size constraints)

- `requiresSupports` (boolean) [✗]: Does this model require support structures for 3D printing?

- `overhangs` (array) [✗]: Detected overhang areas requiring support structures

- `estimatedPrintTimeMinutes` (integer) [✗]: Estimated print time in minutes using normal quality settings (0.2mm layers, 20% infill)

- `printTimeEstimates` (object) [✗]: Print time estimates for different quality presets

- `estimatedMaterialGrams` (number) [✗]: Estimated material usage in grams using 20% infill (assumes PLA density 1.24g/cm³)

- `materialEstimates` (object) [✗]: Material usage estimates for different infill percentages

- `recommendedOrientation` (object) [✗]: Recommended print orientation for minimal support material and best results

- `originalUnit` (string) [✗]: Original file format unit detected from metadata or inferred from scale

- `formatVersion` (string) [✗]: File format version (e.g., 'STL Binary', 'OBJ v4', 'PLY 1.0')

- `hasColorData` (boolean) [✗]: Does the file contain per-vertex color information?

- `hasTextureCoordinates` (boolean) [✗]: Does the file contain UV texture mapping coordinates?

- `hasVertexNormals` (boolean) [✗]: Does the file contain per-vertex normal vectors?

- `analyzedBy` (string) [✗]: Tool/service that performed the analysis

- `analysisVersion` (string) [✗]: Version of the analysis algorithm (for tracking improvements)

- `analysisConfidence` (number) [✗]: Confidence level of analysis results (0.0 = uncertain, 1.0 = highly confident)

- `analysisWarnings` (array) [✗]: Warnings or issues detected during analysis (structured for programmatic handling)

- `analyzedAt` (string) [✗]: ISO 8601 timestamp when analysis was performed (e.g., '2025-11-19T14:35:22Z')

- `errorMessage` (string) [✗]: Detailed error message if status is FAILED

- `errorCode` (string) [✗]: Machine-readable error code for programmatic error handling



### model-technical-metadata-request

**Description:** Triggers comprehensive technical analysis of a 3D model file to extract geometry, quality metrics, and print-readiness information

**Method:** `client.model_technical_metadata_request(data, opts=None)`

**Payload Type:** `ModelTechnicalMetadataRequestMessage`

**Fields:**

- `modelId` (string) [✗]: Unique identifier for the model to analyze

- `ownerId` (string) [✗]: User ID who owns the model

- `storageLocation` (object) [✗]: Location of the 3D model file (legacy - used for direct download if minioPath not provided)

- `minioPath` (string) [✗]: Path to model in MinIO (e.g., 'raw_models/{modelId}/original.glb'). If provided, file will be read from MinIO instead of downloading from storage provider.

- `parentJobId` (string) [✗]: ID of parent file-download job (for BullMQ dependency tracking).

- `analysisOptions` (object) [✗]: Optional analysis configuration parameters



### thumbnail-generation-completed

**Description:** Handles thumbnail generation completed.

**Method:** `client.thumbnail_generation_completed(data, opts=None)`

**Payload Type:** `ThumbnailGenerationCompletedMessage`

**Fields:**

- `originalJobId` (string) [✗]: The ID of the original job that requested the thumbnail generation.

- `modelId` (string) [✗]: The ID of the model that the thumbnail was generated for.

- `status` (string) [✗]: The status of the thumbnail generation.

- `thumbnailPath` (string) [✗]: The path to the generated thumbnail.

- `errorMessage` (string) [✗]: An error message if the thumbnail generation failed.

- `storageLocation` (object) [✗]: The storage location of the model.



### thumbnail-generation-request

**Description:** Handles thumbnail generation requests with customization options. Supports both storage provider downloads and MinIO-cached files.

**Method:** `client.thumbnail_generation_request(data, opts=None)`

**Payload Type:** `ThumbnailGenerationRequestMessage`

**Fields:**

- `modelId` (string) [✗]: The unique identifier for the model requiring a thumbnail.

- `ownerId` (string) [✗]: The identifier of the user who owns the entity.

- `storageLocation` (object) [✗]: The storage location of the model (legacy - used for direct download if minioPath not provided).

- `minioPath` (string) [✗]: Path to model in MinIO (e.g., 'raw_models/{modelId}/original.glb'). If provided, file will be read from MinIO instead of downloading from storage provider.

- `previewType` (string) [✗]: The type of preview to generate, e.g., 'default', 'static', 'glb'.

- `generate360Views` (boolean) [✗]: Generate 16 angle views for 360° preview (4 horizontal x 4 vertical angles).

- `parentJobId` (string) [✗]: ID of parent file-download job (for BullMQ dependency tracking).

- `customization` (object) [✗]: User-defined customizations for the thumbnail.



### user-engagement-event

**Description:** User engagement and onboarding tracking events for analytics and behavioral insights.

Captures key user actions throughout their journey:
- Account creation and onboarding steps
- Feature usage and adoption
- Model management activities
- Marketplace interactions
- Subscription changes

Used for:
- User onboarding funnel analysis
- Feature adoption tracking
- User retention metrics
- A/B testing and experimentation
- Personalization and recommendations
- Product analytics dashboards


**Method:** `client.user_engagement_event(data, opts=None)`

**Payload Type:** `UserEngagementEventMessage`

**Fields:**

- `eventType` (string) [✓]: Category of user engagement event

- `action` (string) [✓]: Specific user action performed

- `timestamp` (string) [✓]: ISO 8601 timestamp when the action occurred

- `userId` (string) [✓]: Unique identifier of the user

- `userEmail` (string) [✗]: User's email (hashed for privacy in analytics)

- `userCreatedAt` (string) [✗]: When the user account was created (for cohort analysis)

- `userPlanTier` (string) [✗]: Current subscription plan tier

- `sessionId` (string) [✗]: User session identifier for grouping actions

- `requestId` (string) [✗]: Request ID for correlation with logs

- `actionDetails` (object) [✗]: Additional context about the action

- `source` (string) [✗]: Where the action originated

- `httpMethod` (string) [✗]: HTTP method used

- `httpUrl` (string) [✗]: API endpoint path

- `httpStatusCode` (integer) [✗]: HTTP response status code

- `durationMs` (number) [✗]: Action duration in milliseconds

- `experimentId` (string) [✗]: A/B test or experiment ID

- `experimentVariant` (string) [✗]: Experiment variant/group

- `environment` (string) [✗]: Deployment environment

- `clientInfo` (object) [✗]: Client/browser information (anonymized)



### worker-analytics-event

**Description:** Analytics event emitted by workers for tracking processing metrics, user behavior,
and model statistics. Consumed by worker-analytic-collector and forwarded to ELK.

All workers MUST emit this event upon job completion (success or failure).
Each worker includes its specific metrics in the `metrics` object.


**Method:** `client.worker_analytics_event(data, opts=None)`

**Payload Type:** `WorkerAnalyticsEventMessage`

**Fields:**

- `eventType` (string) [✓]: Type of analytics event

- `workerId` (string) [✓]: Identifier of the worker that processed the job

- `jobId` (string) [✓]: Unique job identifier from BullMQ

- `timestamp` (string) [✓]: ISO 8601 timestamp of event emission

- `userId` (string) [✗]: User who owns the model/triggered the job

- `modelId` (string) [✗]: Model identifier (if applicable)

- `metamodelId` (string) [✗]: Metamodel identifier (if applicable)

- `storageItemId` (string) [✗]: Storage item identifier (for download events)

- `status` (string) [✗]: Job completion status

- `errorCode` (string) [✗]: Error code if status is failure

- `errorMessage` (string) [✗]: Error message if status is failure

- `timing` (object) [✗]: Processing time metrics in milliseconds

- `metrics` (object) [✗]: Worker-specific metrics. Structure varies by eventType.



### worker-metrics-enriched-event

**Description:** Enriched metrics event for detailed worker monitoring, cost tracking,
and performance analysis. Published to backend.logging.events for
centralized monitoring and cost attribution.

This event is emitted by all workers on job completion and includes:
- LLM token usage and cost breakdown
- System resource consumption (CPU, RAM, disk I/O)
- Detailed timing breakdown by stage
- User and context attribution
- Model-specific metadata


**Method:** `client.worker_metrics_enriched_event(data, opts=None)`

**Payload Type:** `WorkerMetricsEnrichedEventMessage`

**Fields:**

- `eventType` (string) [✓]: Fixed type for enriched worker metrics

- `workerId` (string) [✓]: Identifier of the worker

- `jobId` (string) [✓]: Unique BullMQ job identifier

- `timestamp` (string) [✓]: ISO 8601 timestamp when job completed

- `status` (string) [✓]: Job completion status

- `userId` (string) [✗]: User who owns the resource/triggered the job

- `tenantId` (string) [✗]: Organization/tenant ID (for multi-tenant deployments)

- `sessionId` (string) [✗]: Session ID for correlating user actions

- `requestId` (string) [✗]: Request ID from originating API call (X-Request-Id)

- `modelId` (string) [✗]: Model ID being processed

- `metamodelId` (string) [✗]: Metamodel ID being processed

- `storageItemId` (string) [✗]: Storage item ID (for file operations)

- `timing` (object) [✗]: Comprehensive timing breakdown

- `llmUsage` (object) [✗]: LLM token usage and cost breakdown

- `resources` (object) [✗]: System resource consumption during job

- `workerMetrics` (object) [✗]: Worker-specific metrics (varies by worker type)

- `error` (object) [✗]: Error details if status is failure

- `environment` (string) [✗]: Deployment environment

- `region` (string) [✗]: Cloud region/datacenter

- `workerVersion` (string) [✗]: Worker service version

- `hostname` (string) [✗]: Pod/container hostname



## Configuration

### Environment Variables

You can use environment variables for configuration:

```python
import os
from worker_client import WorkerClient

client = WorkerClient(
    base_url=os.getenv('WORKER_BACKEND_URL', 'http://localhost:3000'),
    api_key=os.getenv('WORKER_BACKEND_API_KEY'),
    timeout=int(os.getenv('WORKER_BACKEND_TIMEOUT', '30'))
)
```

Supported environment variables:
- `WORKER_BACKEND_URL`: Base URL of the worker backend
- `WORKER_BACKEND_API_KEY`: Optional API key for authentication
- `WORKER_BACKEND_TIMEOUT`: Request timeout in seconds

### Client Options

```python
class WorkerClient:
    def __init__(
        self,
        base_url: str,        # Required: Worker backend URL
        api_key: Optional[str] = None,  # Optional: API key
        timeout: int = 30     # Optional: Request timeout in seconds
    )
```

## API Reference

### `WorkerClient`

#### Methods

- `send_to_queue(message_type: str, payload: Dict[str, Any], opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Send a job to the queue with the specified message type
  
- `get_job_status(job_id: str) -> JobStatus`
  - Get the current status of a job


- `backend_logging_event(data: BackendLoggingEventMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Centralized logging event for capturing all warn/error/failure logs from meshsync-backend.
This event is sent to ELK for centralized monitoring, alerting, and debugging.

Automatically emitted by the custom Pino logger interceptor when:
- logger.warn() is called
- logger.error() is called
- uncaught exceptions occur
- request failures happen (4xx, 5xx responses)

Used for:
- System health monitoring
- Error tracking and alerting
- Performance degradation detection
- Security incident tracking
- Compliance and audit trails


- `etsy_analytics_sync_completed(data: EtsyAnalyticsSyncCompletedMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Contains synced analytics data for Etsy listings. Backend stores this in etsy_analytics_snapshots table and indexes to ELK.


- `etsy_analytics_sync_request(data: EtsyAnalyticsSyncRequestMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Syncs analytics data from Etsy API for one or more listings. Fetches views, favorites, sales, revenue, and traffic source data.
Can sync: - Specific listings (provide listingIds) - All user listings (provide userId, empty listingIds) - Shop-level analytics (provide shopId)


- `etsy_publish_listing_completed(data: EtsyPublishListingCompletedMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Indicates completion of Etsy listing publication. Contains external Etsy listing ID and URL, or error details if failed.


- `etsy_publish_listing_request(data: EtsyPublishListingRequestMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Publishes a single metamodel listing to Etsy for a specific material variant. Creates Etsy listing, uploads digital file, and returns external listing ID.
This message is enqueued for EACH material variant when publishing a metamodel.
Example: Publishing a metamodel with PLA, Resin, ABS materials creates 3 jobs.


- `file_download_completed(data: FileDownloadCompletedMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Notifies that a file download has been processed, indicating success or failure.

- `file_download_request(data: FileDownloadRequestMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Downloads model file from storage provider to MinIO for processing pipeline. Acts as parent job for thumbnail generation, technical metadata analysis, and metadata generation.

- `marketplace_analytics_sync_completed(data: MarketplaceAnalyticsSyncCompletedMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Contains synced analytics data for marketplace listings. Backend stores this in marketplace_analytics_snapshots table and indexes to ELK. Works with any marketplace provider.

- `marketplace_analytics_sync_request(data: MarketplaceAnalyticsSyncRequestMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Syncs analytics data from marketplace API for one or more listings. Fetches views, favorites, sales, revenue, and traffic source data. Can sync: specific listings, all user listings, or shop-level analytics. Works with any marketplace provider that supports analytics (etsy, ebay, etc.).

- `marketplace_connection_sync_completed(data: MarketplaceConnectionSyncCompletedMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Notification that marketplace connection sync has completed. Contains updated connection metadata, profile information, and sync statistics.


- `marketplace_connection_sync_request(data: MarketplaceConnectionSyncRequestMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Requests synchronization of marketplace connection data including: - Profile information and shop details - Account status and permissions - Available categories and shipping profiles - Rate limits and API quotas
This is typically triggered after initial connection or periodically to keep marketplace metadata up to date.


- `marketplace_credential_rotation_completed(data: MarketplaceCredentialRotationCompletedMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Notification that marketplace credential rotation has completed. Contains the rotation results, new credential metadata, and any issues encountered.


- `marketplace_credential_rotation_request(data: MarketplaceCredentialRotationRequestMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Requests rotation/refresh of marketplace connection credentials. This is used for: - OAuth token refresh when tokens are near expiry - API key rotation for enhanced security - Re-authentication after connection errors - Scheduled credential updates


- `marketplace_listing_sync_completed(data: MarketplaceListingSyncCompletedMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Notification that marketplace listing sync operation has completed. Contains detailed results of the sync including created/updated listings, errors encountered, and performance statistics.


- `marketplace_listing_sync_request(data: MarketplaceListingSyncRequestMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Requests synchronization of marketplace listings for a connection. Can sync specific listings or all listings for a marketplace connection.
Includes bidirectional sync: - Pull: Fetch listings from marketplace to update local database - Push: Update marketplace listings with local changes - Full: Both pull and push operations


- `marketplace_publish_listing_completed(data: MarketplacePublishListingCompletedMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Indicates completion of marketplace listing publication. Contains external listing ID and URL, or error details if failed. Works with any marketplace provider (etsy, ebay, etc.).

- `marketplace_publish_listing_request(data: MarketplacePublishListingRequestMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Publishes a single metamodel listing to a marketplace for a specific material variant. Creates listing, uploads digital file, and returns external listing ID. This message is enqueued for EACH material variant when publishing a metamodel. The marketplace type (etsy, ebay, etc.) is determined by the marketplaceProvider field.

- `media_batch_download_completed(data: MediaBatchDownloadCompletedMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Notifies that a batch media download has been completed.

- `media_batch_download_request(data: MediaBatchDownloadRequestMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Request to download and process a batch of media files from a storage provider. Images are compressed and resized to specified dimensions, converted to WebP format. Text files and documents are processed and stored with metadata. All processed files are uploaded to MinIO S3 storage under the media/{batchId}/ prefix.


- `metamodel_metadata_generation_completed(data: MetamodelMetadataGenerationCompletedMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Handles metamodel metadata generation completion. Contains AI-generated metadata and aggregated technical analysis.

- `metamodel_metadata_generation_request(data: MetamodelMetadataGenerationRequestMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Handles metamodel metadata generation requests via Ollama. Aggregates data from constituent models and generates AI-enhanced metadata.

- `model_analytics_collection_request(data: ModelAnalyticsCollectionRequestMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Request to collect marketplace analytics for a specific metamodel.
Triggered by backend scheduler every 6 hours for popular/tagged metamodels.

Worker performs targeted market searches based on metamodel metadata
and stores aggregated statistics in Elasticsearch for trend analysis.


- `model_discovery_folder_processed_event(data: ModelDiscoveryFolderProcessedEventMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Handles model discovery folder processed events.

- `model_discovery_scan_found_event(data: ModelDiscoveryScanFoundEventMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Handles model discovery scan found events.

- `model_discovery_scan_progress_event(data: ModelDiscoveryScanProgressEventMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Handles model discovery scan progress events.

- `model_discovery_scan_request(data: ModelDiscoveryScanRequestMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Handles model discovery scan requests events.

- `model_metadata_generation_completed(data: ModelMetadataGenerationCompletedMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Notifies backend that enriched marketplace metadata generation completed. Backend updates Model entity with generated description, tags, classification, etc.

- `model_metadata_generation_request(data: ModelMetadataGenerationRequestMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Generates enriched marketplace metadata (SEO descriptions, tags, categories) for 3D models using LLM vision analysis of thumbnails by default. Worker queries database by modelId to retrieve: Model (fileName, fileSize, ownerId, storageItem), TechnicalMetadata (geometry, quality, printability), and ThumbnailMedia (required for default vision analysis). Prerequisites: file download completed, technical metadata analysis completed (strongly recommended), thumbnail generation completed (REQUIRED for vision-enhanced analysis, default behavior). Vision analysis can be disabled via ENABLE_VISION_METADATA_GENERATION environment variable (default: true).

- `model_metamodel_detection_found(data: ModelMetamodelDetectionFoundMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Handles model metamodel detection found with hierarchical relationships.

- `model_metamodel_detection_request(data: ModelMetamodelDetectionRequestMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Handles model metamodel detection requests.

- `model_sellability_analysis_completed(data: ModelSellabilityAnalysisCompletedMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Contains sellability analysis results including Etsy-specific recommendations, material pricing, and marketplace compatibility scores

- `model_sellability_analysis_request(data: ModelSellabilityAnalysisRequestMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Analyzes a metamodel to determine sellability score, pricing recommendations, and optimal marketplace selection. Enhanced with Etsy-specific analysis including competitor pricing, category demand trends, and material suitability.

- `model_semantic_analysis_completed(data: ModelSemanticAnalysisCompletedMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Handles completion of 3D model semantic analysis with generated tags and similarity results.

- `model_semantic_analysis_request(data: ModelSemanticAnalysisRequestMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Handles 3D model semantic analysis requests using ULIP-2 neural networks and FAISS vector similarity search.

- `model_technical_metadata_completed(data: ModelTechnicalMetadataCompletedMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Reports comprehensive results of technical metadata analysis including geometry, quality metrics, and print-readiness assessment

- `model_technical_metadata_request(data: ModelTechnicalMetadataRequestMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Triggers comprehensive technical analysis of a 3D model file to extract geometry, quality metrics, and print-readiness information

- `thumbnail_generation_completed(data: ThumbnailGenerationCompletedMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Handles thumbnail generation completed.

- `thumbnail_generation_request(data: ThumbnailGenerationRequestMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Handles thumbnail generation requests with customization options. Supports both storage provider downloads and MinIO-cached files.

- `user_engagement_event(data: UserEngagementEventMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - User engagement and onboarding tracking events for analytics and behavioral insights.

Captures key user actions throughout their journey:
- Account creation and onboarding steps
- Feature usage and adoption
- Model management activities
- Marketplace interactions
- Subscription changes

Used for:
- User onboarding funnel analysis
- Feature adoption tracking
- User retention metrics
- A/B testing and experimentation
- Personalization and recommendations
- Product analytics dashboards


- `worker_analytics_event(data: WorkerAnalyticsEventMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Analytics event emitted by workers for tracking processing metrics, user behavior,
and model statistics. Consumed by worker-analytic-collector and forwarded to ELK.

All workers MUST emit this event upon job completion (success or failure).
Each worker includes its specific metrics in the `metrics` object.


- `worker_metrics_enriched_event(data: WorkerMetricsEnrichedEventMessage, opts: Optional[Dict[str, Any]] = None) -> JobResponse`
  - Enriched metrics event for detailed worker monitoring, cost tracking,
and performance analysis. Published to backend.logging.events for
centralized monitoring and cost attribution.

This event is emitted by all workers on job completion and includes:
- LLM token usage and cost breakdown
- System resource consumption (CPU, RAM, disk I/O)
- Detailed timing breakdown by stage
- User and context attribution
- Model-specific metadata



- `close() -> None`
  - Close the HTTP session

#### Context Manager Support

The client supports the context manager protocol for automatic resource cleanup:

```python
with WorkerClient(base_url='...') as client:
    # Use client
    pass
# Session is automatically closed
```

### Response Types

#### `JobResponse`

```python
class JobResponse:
    success: bool
    job_id: str
    message_name: str
    queue: str
```

#### `JobStatus`

```python
class JobStatus:
    job_id: str
    name: str
    queue: str
    state: str  # 'waiting' | 'active' | 'completed' | 'failed' | 'delayed'
    data: Any
    returnvalue: Optional[Any]
    progress: Optional[int]
    timestamp: int
```

## Docker Usage

A Dockerfile is included for containerized usage:

```bash
cd generated/python
docker build -t worker-client-python .
docker run -it --rm worker-client-python python
```

## License

ISC
