# Meshy SDK Webhook-Based Architecture Design

## Overview

Webhook-first Meshy SDK for idempotent asset pipeline execution with task resumption capability.

## Four-Tier Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Workflow Orchestrator                     │
│  - Registers webhook callbacks                              │
│  - Chains dependent tasks                                   │
│  - Resumes from manifests                                   │
└──────────────────┬──────────────────────────────────────────┘
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
┌─────────────────┐  ┌──────────────────┐
│  Service Layer  │  │ Webhook Handler  │
│  - Submit tasks │  │ - Verify HMAC    │
│  - Record intent│  │ - Update state   │
│  - No polling   │  │ - Download GLBs  │
└────────┬────────┘  └────────┬─────────┘
         │                    │
         └──────────┬─────────┘
                    ▼
         ┌────────────────────┐
         │  Task Repository   │
         │  - Manifests       │
         │  - Task graph      │
         │  - Artifacts       │
         └──────────┬─────────┘
                    │
                    ▼
         ┌────────────────────┐
         │   BaseHttpClient   │
         │  - Rate limiting   │
         │  - Error mapping   │
         │  - Request tracing │
         └────────────────────┘
```

## Module Specifications

### 1. API Client (`api/`)

**BaseHttpClient**
```python
class BaseHttpClient:
    def __init__(
        self,
        api_key: str,
        rate_limiter: Optional[RateLimiter] = None,
        tracer: Optional[RequestTracer] = None
    ):
        """
        Args:
            api_key: Meshy API key
            rate_limiter: Token bucket rate limiter (default: 100 req/min)
            tracer: Request ID tracer for debugging
        """
    
    def request(
        self,
        method: str,
        endpoint: str,
        callback_url: Optional[str] = None,
        **kwargs
    ) -> httpx.Response:
        """Make rate-limited request with error mapping
        
        Raises:
            AuthenticationError: 401
            RateLimitError: 429
            ValidationError: 422
            MeshyAPIError: Other errors
        """
    
    def download_file(self, url: str, path: str) -> int:
        """Download artifact to path, return bytes written"""
    
    def generate_callback_url(self, base_url: str, species: str, task_type: str) -> str:
        """Generate webhook callback URL with signature token"""
```

**RateLimiter**
```python
class RateLimiter:
    def __init__(self, requests_per_minute: int = 100):
        """Token bucket rate limiter"""
    
    def acquire(self, endpoint: str) -> None:
        """Block until token available, raise on timeout"""
```

### 2. Service Layer (`services/`)

**Base Service Pattern**
```python
class Text3DService:
    def __init__(self, client: BaseHttpClient, repository: TaskRepository):
        self.client = client
        self.repository = repository
    
    def submit_task(
        self,
        species: str,
        prompt: str,
        callback_url: str,
        art_style: str = "sculpture",
        model_version: str = "latest",
        enable_retexture: bool = True,
        **kwargs
    ) -> TaskSubmission:
        """Submit task and record intent in repository
        
        Returns:
            TaskSubmission with task_id, spec_hash, intent record
        
        Does NOT poll - webhook handles completion
        """
    
    def resume_task(self, species: str, spec_hash: str) -> Optional[TaskSubmission]:
        """Resume from manifest if task exists"""
```

**TaskSubmission DTO**
```python
@dataclass
class TaskSubmission:
    task_id: str
    spec_hash: str
    species: str
    service: str
    status: TaskStatus
    callback_url: str
    created_at: datetime
```

### 3. Webhook Module (`webhooks/`)

**WebhookHandler**
```python
class WebhookHandler:
    def __init__(
        self,
        repository: TaskRepository,
        secret: str,
        downloader: ArtifactDownloader
    ):
        """
        Args:
            repository: TaskRepository for state updates
            secret: HMAC secret for signature verification
            downloader: Downloads GLBs to client/public/models/
        """
    
    def handle_webhook(self, payload: dict, signature: str) -> WebhookResponse:
        """Process Meshy webhook notification
        
        Steps:
        1. Verify HMAC signature
        2. Check idempotency (task_id already processed?)
        3. Update task state in repository
        4. Download artifacts if SUCCEEDED
        5. Dispatch event hooks
        6. Return 200 OK
        
        Returns:
            WebhookResponse with status, message, actions taken
        """
    
    def verify_signature(self, payload: bytes, signature: str) -> bool:
        """Verify Meshy HMAC signature"""
```

**WebhookPayload Schema**
```python
class MeshyWebhookPayload(BaseModel):
    task_id: str
    status: str  # PENDING, IN_PROGRESS, SUCCEEDED, FAILED, EXPIRED
    progress: int  # 0-100
    task_type: str  # text-to-3d, rigging, animation, retexture
    model_urls: Optional[dict[str, str]] = None
    error: Optional[dict] = None
```

**ArtifactDownloader**
```python
class ArtifactDownloader:
    def __init__(self, client: BaseHttpClient, base_path: Path):
        """
        Args:
            base_path: client/public/models/
        """
    
    def download_glb(
        self,
        url: str,
        species: str,
        variant: str,
        task_id: str
    ) -> Path:
        """Download GLB to client/public/models/{species}/{variant}.glb
        
        Returns:
            Path to downloaded file
        """
```

### 4. Workflow Orchestrator (`workflows/`)

**OtterPipeline Example**
```python
class OtterPipeline:
    """Complete otter generation pipeline: Text3D → Rigging → Animation → Retexture"""
    
    def __init__(
        self,
        text3d: Text3DService,
        rigging: RiggingService,
        animation: AnimationService,
        retexture: RetextureService,
        repository: TaskRepository,
        webhook_base_url: str
    ):
        self.services = {
            "text3d": text3d,
            "rigging": rigging,
            "animation": animation,
            "retexture": retexture
        }
        self.repository = repository
        self.webhook_base_url = webhook_base_url
    
    def start(self, species: str, prompt: str) -> PipelineExecution:
        """Start pipeline from scratch"""
        
        # Submit text-to-3d with callback
        callback_url = f"{self.webhook_base_url}/{species}/text3d"
        submission = self.services["text3d"].submit_task(
            species=species,
            prompt=prompt,
            callback_url=callback_url
        )
        
        # Record pipeline intent
        self.repository.record_pipeline_intent(
            species=species,
            stages=["text3d", "rigging", "animation", "retexture"],
            current_stage="text3d",
            current_task_id=submission.task_id
        )
        
        return PipelineExecution(
            species=species,
            current_stage="text3d",
            task_id=submission.task_id
        )
    
    def resume(self, species: str) -> Optional[PipelineExecution]:
        """Resume pipeline from manifest"""
        manifest = self.repository.load_species_manifest(species)
        
        # Find incomplete pipeline
        for spec_hash, asset in manifest.asset_specs.items():
            if asset.status != "SUCCEEDED":
                return self._resume_from_asset(species, asset)
        
        return None
    
    def on_webhook_event(self, species: str, stage: str, webhook_data: dict):
        """Handle webhook completion, chain next stage"""
        
        if webhook_data["status"] == "SUCCEEDED":
            next_stage = self._get_next_stage(stage)
            
            if next_stage:
                # Chain to next stage
                model_id = webhook_data["task_id"]
                callback_url = f"{self.webhook_base_url}/{species}/{next_stage}"
                
                if next_stage == "rigging":
                    self.services["rigging"].submit_task(
                        species=species,
                        model_id=model_id,
                        callback_url=callback_url
                    )
                # etc for other stages
```

## Task State Machine

```
                     ┌──────────┐
                     │ PENDING  │
                     └────┬─────┘
                          │
                     (webhook)
                          │
                          ▼
                  ┌───────────────┐
                  │ IN_PROGRESS   │
                  └───────┬───────┘
                          │
                     (webhook)
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
        ┌──────────┐ ┌────────┐ ┌─────────┐
        │SUCCEEDED │ │ FAILED │ │ EXPIRED │
        └──────────┘ └────────┘ └─────────┘
             │
             ├─> Download GLB
             ├─> Update manifest
             └─> Trigger next stage
```

## Repository Schema Extensions

**PipelineIntent**
```python
class PipelineIntent(BaseModel):
    species: str
    stages: list[str]  # ["text3d", "rigging", "animation", "retexture"]
    current_stage: str
    current_task_id: str
    stage_status: dict[str, str]  # {"text3d": "SUCCEEDED", "rigging": "PENDING"}
    created_at: datetime
    updated_at: datetime
```

## Testing Strategy

### Unit Tests

1. **test_rate_limiter.py** - Token bucket logic, timeout handling
2. **test_error_mapping.py** - Meshy error codes → custom exceptions
3. **test_webhook_handler.py** - HMAC verification, idempotency guard
4. **test_artifact_downloader.py** - GLB download, path construction

### Integration Tests (pytest-vcr)

1. **test_task_submission.py** - Record HTTP for create_task calls
2. **test_webhook_contract.py** - Fixture webhook payloads → handler
3. **test_otter_pipeline.py** - End-to-end: manifest → webhook → GLB

**Webhook Test Pattern**
```python
def test_text3d_webhook_success(webhook_handler, webhook_fixture):
    """Test webhook handling with recorded payload"""
    
    # Load fixture (JSON file with webhook payload)
    payload = webhook_fixture("text3d_success.json")
    signature = generate_test_signature(payload)
    
    # Trigger webhook handler
    response = webhook_handler.handle_webhook(payload, signature)
    
    assert response.status == 200
    assert Path("client/public/models/otter/sculptured.glb").exists()
```

## Package Structure

```
mesh_toolkit/
├── src/
│   └── mesh_toolkit/
│       ├── api/
│       │   ├── __init__.py
│       │   ├── base_client.py
│       │   ├── rate_limiter.py
│       │   └── tracer.py
│       ├── services/
│       │   ├── __init__.py
│       │   ├── text3d_service.py
│       │   ├── rigging_service.py
│       │   ├── animation_service.py
│       │   ├── retexture_service.py
│       │   └── models.py  # DTOs
│       ├── webhooks/
│       │   ├── __init__.py
│       │   ├── handler.py
│       │   ├── schemas.py
│       │   ├── verifier.py
│       │   └── downloader.py
│       ├── workflows/
│       │   ├── __init__.py
│       │   ├── otter_pipeline.py
│       │   └── base_orchestrator.py
│       ├── persistence/
│       │   ├── __init__.py
│       │   ├── repository.py
│       │   ├── schemas.py
│       │   └── utils.py
│       ├── catalog/
│       │   ├── __init__.py
│       │   ├── animations.json
│       │   └── constants.py  # Grouped animation IDs
│       ├── __init__.py
│       ├── client.py  # High-level MeshyClient
│       └── exceptions.py
└── pyproject.toml
```

## Default Configuration

```python
MESHY_DEFAULTS = {
    "art_style": "sculpture",
    "model_version": "latest",
    "enable_pbr": True,
    "enable_retexture": True,
    "topology": "quad",
    "ai_model": "meshy-4"
}
```

## Idempotent Build Flow

1. Check manifest for existing task with same spec_hash
2. If exists and SUCCEEDED → skip, return cached GLB path
3. If exists and PENDING/IN_PROGRESS → wait for webhook (or resume)
4. If exists and FAILED → retry with exponential backoff
5. If not exists → submit new task, record intent

## Animation Catalog Structure

```python
# catalog/constants.py
class AnimationGroups:
    LOCOMOTION = [1, 2, 3, ...]  # Walking, Running, etc
    COMBAT = [4, 5, 6, ...]      # Attack, Block, etc
    EMOTES = [50, 51, 52, ...]   # Wave, Dance, etc
    IDLE = [100, 101, ...]       # Various idle poses

class DefaultAnimations:
    OTTER_IDLE = 100
    OTTER_WALK = 1
    OTTER_ATTACK = 4
    OTTER_SWIM = 25
```

## Error Handling

**Retry Logic**
- 5xx errors: Exponential backoff (3 attempts)
- 429 rate limit: Wait for Retry-After header
- 4xx validation: Raise immediately, no retry

**Webhook Failures**
- Return 200 even on processing error (prevent Meshy retries)
- Log error, mark task as FAILED in repository
- Trigger error event hooks for monitoring

## Security

1. **HMAC Verification** - Verify all webhook signatures
2. **API Key Rotation** - Support key rotation without downtime
3. **Request Signing** - Optional request signing for submissions
4. **Rate Limiting** - Prevent API abuse

## Implementation Order

1. API Client (base_client.py, rate_limiter.py, exceptions.py)
2. Service Layer (text3d_service.py, models.py)
3. Webhook Module (handler.py, schemas.py, verifier.py)
4. Repository Extensions (pipeline_intent support)
5. Workflow Orchestrator (otter_pipeline.py)
6. Testing (unit tests → integration tests)

## Acceptance Criteria

- [ ] No polling loops - all task completion via webhooks
- [ ] Idempotent builds with manifest-based resumption
- [ ] Rate limiting (100 req/min default)
- [ ] Complete error handling (4xx, 5xx, network)
- [ ] HMAC webhook signature verification
- [ ] GLB artifacts in `client/public/models/{species}/`
- [ ] 600+ animation catalog as grouped constants
- [ ] pytest-vcr tests for all services
- [ ] Webhook contract tests with fixture payloads
- [ ] End-to-end pipeline test: manifest → GLB
