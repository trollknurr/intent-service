# Intent Classification Service

## Bootstrap 

### Local dev process

* You will need [huggingface-cli](https://huggingface.co/docs/huggingface_hub/en/guides/cli) to get model weights for local development (no need for docker) and [UV](https://github.com/astral-sh/uv) for dependency management
* `uv sync --locked`
* Download embedder weights (will take time) `uv run huggingface-cli download jinaai/jina-embeddings-v3 --local-dir weights/jina-emb`

Run dev server: `make dev`

### Docker

* Build image: `make build`
* Run container: `make run`

### Code quality

* `make format` - format code with ruff
* `make lint` - lint code with ruff
* `make test` - run tests with pytest

TODO: add static type checking with mypy/pyright

## Research and Experiments

For given task my opinion is that we should not use LLM, and use more classic and robust solutions. I've tried several approaches to implement model:

* TF-IDF with Logistic Regression
* TF-IDF with Random Forest

This most classic approach gave good results, but I've decided to try something more complex and interesting because this is test project. In real project, if this is matches with business requirements (for example English language only), I would use this approach.

Second approach is to use text embeddings, i didn't have much experience with particular model, so I've decided to try jina embeddings.

* Jina embeddings with Logistic Regression
* Jina embeddings with Random Forest

This approach gave me good results, but I've faced with some problems:
* I had to download a lot of files (1.5GB)
* It took a lot of time to download all files
* Model runtime (this depends on technical requirements)

And finally I've decided to try something more fancy and interesting: zero-shot text classification with `facebook/bart-large-mnli`, but it's performs poorly.

All atemps are available in `train` folder in form of notebooks.

As a result I've decided to use Jina embeddings with Logistic Regression. I've found multi-language support is a plus, and it's still robust and fast enough.

## Implementation Overview

### Architecture
The service follows a hexagonal architecture pattern with clear separation of concerns:
- `port` - Contains interfaces for input/output adapters
- `adapter` - Implementation of interfaces (HTTP API, ML models)
- `domain` - Core models
- `service` - Application services orchestrating the flow

### Current Implementation
- FastAPI-based HTTP service
- Logistic Regression classifier with Jina embeddings
- Modular design allowing easy model swapping
- Full API spec compliance with proper error handling

### Key Features
- Language-agnostic approach using embeddings
- Proper error handling for edge cases
- Easy to extend with new model types


### API Endpoints
- `GET /ready` - Service health check
- `POST /intent` - Intent classification endpoint
- `GET /docs` - auto-generated API Swagger docs

### Adding New Models
To add a new model type:
1. Implement `IntentModel` interface
2. Add model configuration in `config.py`
3. Add model to application construction in `app.py` or make it conditional, depending on `Config`

## Future Improvements
- Add metrics with Prometheus client library or OpenTelemetry
- Implement model versioning
- Work with jina embedding to reduce amount of downloaded files
- Use ONNX runtime for embedder inference, JINA provides [support for it](https://huggingface.co/jinaai/jina-embeddings-v3)
