"""Auto-generated worker client"""

import requests
from typing import Dict, Optional
from . import types


class JobResponse:
    """Response from enqueueing a job"""
    def __init__(self, data: Dict[str, object]):
        self.success = data.get("success", False)
        self.job_id = data.get("jobId")
        self.message_name = data.get("messageName")
        self.queue = data.get("queue")

    def __repr__(self):
        return f"JobResponse(job_id={self.job_id}, message={self.message_name})"


class JobStatus:
    """Job status information"""
    def __init__(self, data: Dict[str, object]):
        self.job_id = data.get("jobId")
        self.name = data.get("name")
        self.queue = data.get("queue")
        self.state = data.get("state")
        self.data = data.get("data")
        self.returnvalue = data.get("returnvalue")
        self.progress = data.get("progress")
        self.timestamp = data.get("timestamp")

    def __repr__(self):
        return f"JobStatus(job_id={self.job_id}, state={self.state})"


class WorkerClient:
    """HTTP-based client for worker-backend"""

    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: int = 30):
        """Initialize the worker client

        Args:
            base_url: Base URL of the worker backend (e.g., "http://localhost:3000")
            api_key: Optional API key for authentication
            timeout: Request timeout in seconds (default: 30)
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers"""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def send_to_queue(self, message_type: str, payload: Dict[str, object], opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Send a job to the queue

        Args:
            message_type: Type of message (use types.MessageTypes constants)
            payload: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID and metadata

        Raises:
            requests.HTTPError: If the request fails
        """
        url = f"{self.base_url}/api/jobs/{message_type}"
        response = self.session.post(
            url,
            json={'payload': payload, 'opts': opts},
            headers=self._get_headers(),
            timeout=self.timeout
        )
        response.raise_for_status()
        return JobResponse(response.json())

    def get_job_status(self, job_id: str) -> JobStatus:
        """Get job status by job ID

        Args:
            job_id: Job ID returned from send_to_queue

        Returns:
            JobStatus with job details

        Raises:
            requests.HTTPError: If the request fails
        """
        url = f"{self.base_url}/api/jobs/{job_id}"
        response = self.session.get(
            url,
            headers=self._get_headers(),
            timeout=self.timeout
        )
        response.raise_for_status()
        return JobStatus(response.json())


    def backend_logging_event(self, data: types.BackendLoggingEventMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Centralized logging event for capturing all warn/error/failure logs from meshsync-backend.
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


        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.BACKEND_LOGGING_EVENT, data, opts)


    def etsy_analytics_sync_completed(self, data: types.EtsyAnalyticsSyncCompletedMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Contains synced analytics data for Etsy listings. Backend stores this in etsy_analytics_snapshots table and indexes to ELK.


        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.ETSY_ANALYTICS_SYNC_COMPLETED, data, opts)


    def etsy_analytics_sync_request(self, data: types.EtsyAnalyticsSyncRequestMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Syncs analytics data from Etsy API for one or more listings. Fetches views, favorites, sales, revenue, and traffic source data.
Can sync: - Specific listings (provide listingIds) - All user listings (provide userId, empty listingIds) - Shop-level analytics (provide shopId)


        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.ETSY_ANALYTICS_SYNC_REQUEST, data, opts)


    def etsy_publish_listing_completed(self, data: types.EtsyPublishListingCompletedMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Indicates completion of Etsy listing publication. Contains external Etsy listing ID and URL, or error details if failed.


        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.ETSY_PUBLISH_LISTING_COMPLETED, data, opts)


    def etsy_publish_listing_request(self, data: types.EtsyPublishListingRequestMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Publishes a single metamodel listing to Etsy for a specific material variant. Creates Etsy listing, uploads digital file, and returns external listing ID.
This message is enqueued for EACH material variant when publishing a metamodel.
Example: Publishing a metamodel with PLA, Resin, ABS materials creates 3 jobs.


        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.ETSY_PUBLISH_LISTING_REQUEST, data, opts)


    def file_download_completed(self, data: types.FileDownloadCompletedMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Notifies that a file download has been processed, indicating success or failure.

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.FILE_DOWNLOAD_COMPLETED, data, opts)


    def file_download_request(self, data: types.FileDownloadRequestMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Downloads model file from storage provider to MinIO for processing pipeline. Acts as parent job for thumbnail generation, technical metadata analysis, and metadata generation.

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.FILE_DOWNLOAD_REQUEST, data, opts)


    def marketplace_analytics_sync_completed(self, data: types.MarketplaceAnalyticsSyncCompletedMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Contains synced analytics data for marketplace listings. Backend stores this in marketplace_analytics_snapshots table and indexes to ELK. Works with any marketplace provider.

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MARKETPLACE_ANALYTICS_SYNC_COMPLETED, data, opts)


    def marketplace_analytics_sync_request(self, data: types.MarketplaceAnalyticsSyncRequestMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Syncs analytics data from marketplace API for one or more listings. Fetches views, favorites, sales, revenue, and traffic source data. Can sync: specific listings, all user listings, or shop-level analytics. Works with any marketplace provider that supports analytics (etsy, ebay, etc.).

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MARKETPLACE_ANALYTICS_SYNC_REQUEST, data, opts)


    def marketplace_connection_sync_completed(self, data: types.MarketplaceConnectionSyncCompletedMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Notification that marketplace connection sync has completed. Contains updated connection metadata, profile information, and sync statistics.


        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MARKETPLACE_CONNECTION_SYNC_COMPLETED, data, opts)


    def marketplace_connection_sync_request(self, data: types.MarketplaceConnectionSyncRequestMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Requests synchronization of marketplace connection data including: - Profile information and shop details - Account status and permissions - Available categories and shipping profiles - Rate limits and API quotas
This is typically triggered after initial connection or periodically to keep marketplace metadata up to date.


        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MARKETPLACE_CONNECTION_SYNC_REQUEST, data, opts)


    def marketplace_credential_rotation_completed(self, data: types.MarketplaceCredentialRotationCompletedMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Notification that marketplace credential rotation has completed. Contains the rotation results, new credential metadata, and any issues encountered.


        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MARKETPLACE_CREDENTIAL_ROTATION_COMPLETED, data, opts)


    def marketplace_credential_rotation_request(self, data: types.MarketplaceCredentialRotationRequestMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Requests rotation/refresh of marketplace connection credentials. This is used for: - OAuth token refresh when tokens are near expiry - API key rotation for enhanced security - Re-authentication after connection errors - Scheduled credential updates


        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MARKETPLACE_CREDENTIAL_ROTATION_REQUEST, data, opts)


    def marketplace_listing_sync_completed(self, data: types.MarketplaceListingSyncCompletedMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Notification that marketplace listing sync operation has completed. Contains detailed results of the sync including created/updated listings, errors encountered, and performance statistics.


        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MARKETPLACE_LISTING_SYNC_COMPLETED, data, opts)


    def marketplace_listing_sync_request(self, data: types.MarketplaceListingSyncRequestMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Requests synchronization of marketplace listings for a connection. Can sync specific listings or all listings for a marketplace connection.
Includes bidirectional sync: - Pull: Fetch listings from marketplace to update local database - Push: Update marketplace listings with local changes - Full: Both pull and push operations


        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MARKETPLACE_LISTING_SYNC_REQUEST, data, opts)


    def marketplace_publish_listing_completed(self, data: types.MarketplacePublishListingCompletedMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Indicates completion of marketplace listing publication. Contains external listing ID and URL, or error details if failed. Works with any marketplace provider (etsy, ebay, etc.).

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MARKETPLACE_PUBLISH_LISTING_COMPLETED, data, opts)


    def marketplace_publish_listing_request(self, data: types.MarketplacePublishListingRequestMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Publishes a single metamodel listing to a marketplace for a specific material variant. Creates listing, uploads digital file, and returns external listing ID. This message is enqueued for EACH material variant when publishing a metamodel. The marketplace type (etsy, ebay, etc.) is determined by the marketplaceProvider field.

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MARKETPLACE_PUBLISH_LISTING_REQUEST, data, opts)


    def media_batch_download_completed(self, data: types.MediaBatchDownloadCompletedMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Notifies that a batch media download has been completed.

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MEDIA_BATCH_DOWNLOAD_COMPLETED, data, opts)


    def media_batch_download_request(self, data: types.MediaBatchDownloadRequestMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Request to download and process a batch of media files from a storage provider. Images are compressed and resized to specified dimensions, converted to WebP format. Text files and documents are processed and stored with metadata. All processed files are uploaded to MinIO S3 storage under the media/{batchId}/ prefix.


        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MEDIA_BATCH_DOWNLOAD_REQUEST, data, opts)


    def metamodel_metadata_generation_completed(self, data: types.MetamodelMetadataGenerationCompletedMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Handles metamodel metadata generation completion. Contains AI-generated metadata and aggregated technical analysis.

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.METAMODEL_METADATA_GENERATION_COMPLETED, data, opts)


    def metamodel_metadata_generation_request(self, data: types.MetamodelMetadataGenerationRequestMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Handles metamodel metadata generation requests via Ollama. Aggregates data from constituent models and generates AI-enhanced metadata.

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.METAMODEL_METADATA_GENERATION_REQUEST, data, opts)


    def model_analytics_collection_request(self, data: types.ModelAnalyticsCollectionRequestMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Request to collect marketplace analytics for a specific metamodel.
Triggered by backend scheduler every 6 hours for popular/tagged metamodels.

Worker performs targeted market searches based on metamodel metadata
and stores aggregated statistics in Elasticsearch for trend analysis.


        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MODEL_ANALYTICS_COLLECTION_REQUEST, data, opts)


    def model_discovery_folder_processed_event(self, data: types.ModelDiscoveryFolderProcessedEventMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Handles model discovery folder processed events.

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MODEL_DISCOVERY_FOLDER_PROCESSED_EVENT, data, opts)


    def model_discovery_scan_found_event(self, data: types.ModelDiscoveryScanFoundEventMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Handles model discovery scan found events.

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MODEL_DISCOVERY_SCAN_FOUND_EVENT, data, opts)


    def model_discovery_scan_progress_event(self, data: types.ModelDiscoveryScanProgressEventMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Handles model discovery scan progress events.

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MODEL_DISCOVERY_SCAN_PROGRESS_EVENT, data, opts)


    def model_discovery_scan_request(self, data: types.ModelDiscoveryScanRequestMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Handles model discovery scan requests events.

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MODEL_DISCOVERY_SCAN_REQUEST, data, opts)


    def model_metadata_generation_completed(self, data: types.ModelMetadataGenerationCompletedMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Notifies backend that enriched marketplace metadata generation completed. Backend updates Model entity with generated description, tags, classification, etc.

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MODEL_METADATA_GENERATION_COMPLETED, data, opts)


    def model_metadata_generation_request(self, data: types.ModelMetadataGenerationRequestMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Generates enriched marketplace metadata (SEO descriptions, tags, categories) for 3D models using LLM vision analysis of thumbnails by default. Worker queries database by modelId to retrieve: Model (fileName, fileSize, ownerId, storageItem), TechnicalMetadata (geometry, quality, printability), and ThumbnailMedia (required for default vision analysis). Prerequisites: file download completed, technical metadata analysis completed (strongly recommended), thumbnail generation completed (REQUIRED for vision-enhanced analysis, default behavior). Vision analysis can be disabled via ENABLE_VISION_METADATA_GENERATION environment variable (default: true).

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MODEL_METADATA_GENERATION_REQUEST, data, opts)


    def model_metamodel_detection_found(self, data: types.ModelMetamodelDetectionFoundMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Handles model metamodel detection found with hierarchical relationships.

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MODEL_METAMODEL_DETECTION_FOUND, data, opts)


    def model_metamodel_detection_request(self, data: types.ModelMetamodelDetectionRequestMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Handles model metamodel detection requests.

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MODEL_METAMODEL_DETECTION_REQUEST, data, opts)


    def model_sellability_analysis_completed(self, data: types.ModelSellabilityAnalysisCompletedMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Contains sellability analysis results including Etsy-specific recommendations, material pricing, and marketplace compatibility scores

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MODEL_SELLABILITY_ANALYSIS_COMPLETED, data, opts)


    def model_sellability_analysis_request(self, data: types.ModelSellabilityAnalysisRequestMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Analyzes a metamodel to determine sellability score, pricing recommendations, and optimal marketplace selection. Enhanced with Etsy-specific analysis including competitor pricing, category demand trends, and material suitability.

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MODEL_SELLABILITY_ANALYSIS_REQUEST, data, opts)


    def model_semantic_analysis_completed(self, data: types.ModelSemanticAnalysisCompletedMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Handles completion of 3D model semantic analysis with generated tags and similarity results.

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MODEL_SEMANTIC_ANALYSIS_COMPLETED, data, opts)


    def model_semantic_analysis_request(self, data: types.ModelSemanticAnalysisRequestMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Handles 3D model semantic analysis requests using ULIP-2 neural networks and FAISS vector similarity search.

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MODEL_SEMANTIC_ANALYSIS_REQUEST, data, opts)


    def model_technical_metadata_completed(self, data: types.ModelTechnicalMetadataCompletedMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Reports comprehensive results of technical metadata analysis including geometry, quality metrics, and print-readiness assessment

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MODEL_TECHNICAL_METADATA_COMPLETED, data, opts)


    def model_technical_metadata_request(self, data: types.ModelTechnicalMetadataRequestMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Triggers comprehensive technical analysis of a 3D model file to extract geometry, quality metrics, and print-readiness information

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.MODEL_TECHNICAL_METADATA_REQUEST, data, opts)


    def thumbnail_generation_completed(self, data: types.ThumbnailGenerationCompletedMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Handles thumbnail generation completed.

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.THUMBNAIL_GENERATION_COMPLETED, data, opts)


    def thumbnail_generation_request(self, data: types.ThumbnailGenerationRequestMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Handles thumbnail generation requests with customization options. Supports both storage provider downloads and MinIO-cached files.

        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.THUMBNAIL_GENERATION_REQUEST, data, opts)


    def user_engagement_event(self, data: types.UserEngagementEventMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """User engagement and onboarding tracking events for analytics and behavioral insights.

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


        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.USER_ENGAGEMENT_EVENT, data, opts)


    def worker_analytics_event(self, data: types.WorkerAnalyticsEventMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Analytics event emitted by workers for tracking processing metrics, user behavior,
and model statistics. Consumed by worker-analytic-collector and forwarded to ELK.

All workers MUST emit this event upon job completion (success or failure).
Each worker includes its specific metrics in the `metrics` object.


        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.WORKER_ANALYTICS_EVENT, data, opts)


    def worker_metrics_enriched_event(self, data: types.WorkerMetricsEnrichedEventMessage, opts: Optional[Dict[str, object]] = None) -> JobResponse:
        """Enriched metrics event for detailed worker monitoring, cost tracking,
and performance analysis. Published to backend.logging.events for
centralized monitoring and cost attribution.

This event is emitted by all workers on job completion and includes:
- LLM token usage and cost breakdown
- System resource consumption (CPU, RAM, disk I/O)
- Detailed timing breakdown by stage
- User and context attribution
- Model-specific metadata


        Args:
            data: Message payload
            opts: Optional dictionary of BullMQ job options

        Returns:
            JobResponse with job ID
        """
        return self.send_to_queue(types.MessageTypes.WORKER_METRICS_ENRICHED_EVENT, data, opts)


    def close(self) -> None:
        """Close the HTTP session"""
        self.session.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
