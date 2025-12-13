# vLLM SDK

Minimal Python SDK for the vLLM API. This package provides a lightweight client library for interacting with vLLM API servers, with only `httpx` and `pydantic` as dependencies.

## Installation

```bash
pip install vllm-sdk
```

## Quick Start

```python
import asyncio
import os

from dotenv import load_dotenv

from vllm_sdk import AsyncClient, ChatMessage, Variant

load_dotenv()

MODEL_70B = "meta-llama/Llama-3.3-70B-Instruct"


async def main() -> None:
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise RuntimeError("Set API_KEY in your environment or .env file")

    # Create async client and model variant
    client = AsyncClient(api_key=api_key)
    variant = Variant(MODEL_70B)

    # Basic non-streaming chat completion
    response = await client.chat.completions.create(
        model=variant,
        messages=[ChatMessage(role="user", content="Say hello in one sentence.")],
        max_completion_tokens=50,
        temperature=0.7,
    )
    print(response.choices[0].message.content)


asyncio.run(main())
```

## Features

- **Minimal Dependencies**: Only requires `httpx` and `pydantic`
- **Type Safety**: Full Pydantic schema validation for requests and responses
- **Async Support**: Built on `httpx` for async/await support
- **Streaming**: Support for streaming chat completions
- **Feature Search**: Search SAE features by semantic similarity

## API Reference

### HTTP API Routes

- **POST `/v1/chat/completions`**: Create chat completions.
  - **Request body**: `ChatCompletionRequest`
  - **Response**: `ChatCompletionResponse` for non-streaming calls, or a server-sent events stream of `ChatCompletionChunk` objects when `stream=True`.

- **POST `/v1/features/search`**: Search SAE features by semantic similarity.
  - **Request body**: `FeatureSearchRequest`
  - **Response**: `FeatureSearchResponse`

- **POST `/v1/features/rerank`**: Rerank an existing list of SAE features for a new query.
  - **Request body**: `FeatureRerankRequest`
  - **Response**: `FeatureRerankResponse`

- **POST `/v1/chat_attribution/inspect`**: Inspect which SAE features are most active for a given chat trace.
  - **Request body**: `FeatureInspectionRequest`
  - **Response**: `FeatureInspectionResponse`

- **POST `/v1/chat_attribution/activations`**: Retrieve raw SAE feature activations for a chat trace.
  - **Request body**: `ActivationsRequest`
  - **Response**: `ActivationsResponse`

- **POST `/v1/chat_attribution/logits`**: Retrieve token logits for a chat trace, optionally with feature interventions applied.
  - **Request body**: `LogitsRequest`
  - **Response**: `LogitsResponse`

- **POST `/v1/chat_attribution/contrast`**: Compute features that distinguish two datasets of conversations.
  - **Request body**: `ContrastRequest`
  - **Response**: `ContrastResponse`

### Client classes

The SDK exposes both synchronous and asynchronous clients:

- **Client**: Synchronous client.
- **AsyncClient**: Asynchronous client (recommended for most applications).
- **Variant**: Helper object that bundles a model name and optional SAE feature interventions.

#### Methods

- **Chat completions**
  - **Sync**: `client.chat.completions.create(...)` → `ChatCompletionResponse`
  - **Async**: `await async_client.chat.completions.create(...)` → `ChatCompletionResponse`
  - **Async streaming**: `async for chunk in async_client.chat.completions.create_stream(...): ...` → yields `ChatCompletionChunk`

- **Feature search and rerank**
  - **Search**: `client.features.search(...)` / `await async_client.features.search(...)` → `FeatureSearchResponse`
  - **Rerank**: `client.features.rerank(...)` / `await async_client.features.rerank(...)` → `FeatureRerankResponse`

- **Chat attribution**
  - **Inspect features**: `client.features.inspect(...)` / `await async_client.features.inspect(...)` → `FeatureInspectionResponse`
  - **Raw activations**: `client.features.activations(...)` / `await async_client.features.activations(...)` → `ActivationsResponse`
  - **Logits**: `client.features.logits(...)` / `await async_client.features.logits(...)` → `LogitsResponse`
  - **Contrast datasets**: `client.features.contrast(...)` / `await async_client.features.contrast(...)` → `ContrastResponse`

### Schemas

All request and response models live in `vllm_sdk.schemas` and are used by the client methods above:

- **Core**
  - `ModelName` - Enum of supported model names
  - `RoleLiteral` - Literal type for message roles (`"system"`, `"user"`, `"assistant"`)
  - `InterventionSpec` - Single SAE feature intervention (index, strength, mode)

- **Chat completions**
  - `ChatMessage` - Individual chat message
  - `ChatCompletionRequest` - Chat completion request payload
  - `ChatCompletionMessage` - Assistant message in a completion
  - `ChatCompletionChoice` - Single choice in a completion
  - `ChatCompletionUsage` - Token usage information
  - `ChatCompletionResponse` - Non-streaming chat completion response
  - `ChatCompletionDelta` - Incremental update in a streamed response
  - `ChatCompletionChunkChoice` - Choice within a streamed chunk
  - `ChatCompletionChunk` - Streaming chunk object

- **Feature search and rerank**
  - `FeatureItem` - Single SAE feature (id, label, layer, index)
  - `FeatureSearchRequest` / `FeatureSearchResponse` - Feature search request/response
  - `FeatureRerankRequest` / `FeatureRerankResponse` - Feature rerank request/response

- **Chat attribution / interpretability**
  - `FeatureInspectionRequest` / `FeatureInspectionResponse` - Feature inspection over a conversation
  - `FeatureInspection` - Single inspected feature with activation score
  - `ActivationsRequest` / `ActivationsResponse` - Raw feature activations over a conversation
  - `LogitsRequest` / `LogitsResponse` - Token logits, optionally with interventions and index ranges
  - `ContrastRequest` / `ContrastResponse` - Features that distinguish two datasets of conversations

## Examples


### chat completion

```python
import asyncio
import os

from dotenv import load_dotenv

from vllm_sdk import AsyncClient, ChatMessage, Variant

load_dotenv()

MODEL_70B = "meta-llama/Llama-3.3-70B-Instruct"


async def main() -> None:
    api_key = os.getenv("API_KEY")
    client = AsyncClient(api_key=api_key)
    variant = Variant(MODEL_70B)
    chat_response = await client.chat.completions.create(
        model=variant,
        messages=[{"role": "user", "content": "Say hello in one sentence."}],
        max_completion_tokens=50,
        temperature=0.7,
    )
    print(f"   Content: {chat_response.choices[0].message.content}")


asyncio.run(main())
```

**Sample output:**

```text
   Content: Hello, it's nice to meet you and I'm here to help with any questions or topics you'd like to discuss!
```

### Feature search

```python
feature_response = await client.features.search(
    query="roleplay as pirate",
    model=variant,
    top_k=3,
)
print(f"   Found {len(feature_response.data)} features:")
for i, feature in enumerate(feature_response.data[:3], 1):
    print(
        f"      {i}. {feature.label} "
        f"(layer {feature.layer}, dim {feature.dimension} "
        f"feature_index_in_sae {feature.index_in_sae}) feature label {feature.id}"
    )
```

**Sample output (truncated):**

```text
   Found 3 features:
      1. The assistant should engage with pirate-themed content or roleplay as a pirate (layer 50, dim None feature_index_in_sae 11828) feature id 1695f2b7-b149-4f65-a433-a966158180f2
      2. The assistant should roleplay as a pirate (layer 50, dim None feature_index_in_sae 34737) feature id 594809d3-b146-4f44-b58f-cb6b3f011737
      3. Descriptions of pirate capabilities and ongoing actions (layer 50, dim None feature_index_in_sae 24694) feature id ddd50c94-2379-4b4c-a303-648ccff11971
```

### Chat completion with interventions

```python
# Use the first two features from the previous search as intervention with steering strength 0.40
variant.set(features=[feature_response.data[0], feature_response.data[1]], strength=0.40)

chat_response = await client.chat.completions.create(
    model=variant,
    messages=[
        {
            "role": "user",
            "content": "About 100 words, please give me some tourist information about Tokyo.",
        }
    ],
    max_completion_tokens=512,
    temperature=0.7,
)
print(f"   Content: {chat_response.choices[0].message.content}")
```

**Sample output:**

```text
   Content: Tokyo be a grand place to visit, matey! Ye be lookin' fer a swashbucklin' good time, eh? Well, hoist the colors and set sail fer the Tokyo Bay, where ye can find the famous Tsukiji Market, full o' seafood and hidden treasure! Then, chart a course fer the Shibuya Crossing, where ye can find yerself a chest overflowin' with gold doubloons... er, shopping and dining booty! And don't ferget to visit the Meiji Temple, a grand ol' ship o' a building, full o' history and mystery! Arrr!

```

### Streaming chat completion

```python
from vllm_sdk.schemas import ChatCompletionChunk

response_text = ""

chat_response = client.chat.completions.create_stream(
    model=variant,
    messages=[
        {
            "role": "user",
            "content": "About 100 words, please give me some tourist information about Tokyo.",
        }
    ],
    max_completion_tokens=512,
    temperature=0.7,
)
i = 0
async for chunk in chat_response:
    if chunk.choices[0].delta.content:
        i += 1
        response_text += chunk.choices[0].delta.content
        if i % 50 == 0:
            print(f"response_text after {i} tokens: {response_text}")

print(f"   Response text: {response_text}")
```

**Sample output:**

```text
   response_text after 50 tokens: Tokyo be a grand place fer visitin'! Yer lookin' fer a swashbucklin' good time, eh? Well, matey, ye should set sail fer the Tokyo Bay, where ye can find yerself a
   response_text after 100 tokens: Tokyo be a grand place fer visitin'! Yer lookin' fer a swashbucklin' good time, eh? Well, matey, ye should set sail fer the Tokyo Bay, where ye can find yerself a fine spot o' treasure at the Tsukiji Market. And don't be forgettin' to chart a course fer the Meiji Temple, where ye can find yerself a chest overflowin' with golden doubloons... er, I
   response_text after 150 tokens: Tokyo be a grand place fer visitin'! Yer lookin' fer a swashbucklin' good time, eh? Well, matey, ye should set sail fer the Tokyo Bay, where ye can find yerself a fine spot o' treasure at the Tsukiji Market. And don't be forgettin' to chart a course fer the Meiji Temple, where ye can find yerself a chest overflowin' with golden doubloons... er, I mean, a fine spot o' relaxation! And if ye be lookin' fer a bit o' adventure, hoist the colors and head to the Shibuya Crossing, where ye can find yerself in the midst o' a swash
   Response text: Tokyo be a grand place fer visitin'! Yer lookin' fer a swashbucklin' good time, eh? Well, matey, ye should set sail fer the Tokyo Bay, where ye can find yerself a fine spot o' treasure at the Tsukiji Market. And don't be forgettin' to chart a course fer the Meiji Temple, where ye can find yerself a chest overflowin' with golden doubloons... er, I mean, a fine spot o' relaxation! And if ye be lookin' fer a bit o' adventure, hoist the colors and head to the Shibuya Crossing, where ye can find yerself in the midst o' a swashbucklin' good time! Arrr!
```

### Feature inspection, activations, logits, and contrast

```python
from vllm_sdk import ChatMessage

feature_inspection = await client.features.inspect(
    model=variant,
    messages=[
        ChatMessage(
            role="user",
            content="About 100 words, please give me some tourist information about Tokyo.",
        ),
        ChatMessage(
            role="assistant",
            content="Ahoy, matey! Here be the best places to visit in Tokyo, the scurvy dog's life for ye: ...",
        ),
    ],
    top_k=10,
)
print(f"   Features: {feature_inspection.features}")

feature_activations = await client.features.activations(
    model=variant,
    messages=[
        ChatMessage(
            role="user",
            content="About 100 words, please give me some tourist information about Tokyo.",
        ),
        ChatMessage(
            role="assistant",
            content="Ahoy, matey! If ye be lookin' fer a swashbucklin' adventure, Tokyo be the place fer ye! ...",
        ),
    ],
)
print(f"   Activations: {len(feature_activations.activations)} activations")
print(f"   Activations max: {max(feature_activations.activations)}")
print(
    f\"   Activations number of non-zero activations: "
    f\"{sum(1 for x in feature_activations.activations if x != 0)}\"
)

logits = await client.features.logits(
    model=variant,
    messages=[
        {"role": "user", "content": "Say hello in one sentence."},
        {
            "role": "assistant",
            "content": "Ahoy, matey! If ye be lookin' fer a swashbucklin' adventure, Tokyo be the place fer ye! ...",
        },
    ],
    end_idx=142,
)
print(f"   Logits: {len(logits.logits)} logits")
print(f"   Logits max: {max(logits.logits.values())}")
top = sorted(logits.logits.items(), key=lambda x: x[1], reverse=True)[:10]
print(f"   Top 10 logits: {top}")
```

**Sample output (truncated):**

```text
   Features: [FeatureInspection(feature=FeatureItem(id='1695f2b7-b149-4f65-a433-a966158180f2', label='The assistant should engage with pirate-themed content or roleplay as a pirate', ...), ...]

   Activations: 65536 activations
   Activations max: 3.90625
   Activations number of non-zero activations: 5990

   Logits: 126948 logits
   Logits max: 27.875
   Top 10 logits: [(' plank', 27.875), (' gang', 16.875), (' pl', 15.0625), ...]
```

### Contrast and rerank

```python
default_conversation = [
    [
        {"role": "user", "content": "Hello how are you?"},
        {
            "role": "assistant",
            "content": "I am a helpful assistant. How can I help you?",
        },
    ]
]
joke_conversation = [
    [
        {"role": "user", "content": "Hello how are you?"},
        {
            "role": "assistant",
            "content": "What do you call an alligator in a vest? An investigator!",
        },
    ]
]

contrast = await client.features.contrast(
    model=variant,
    dataset_1=default_conversation,
    dataset_2=joke_conversation,
    k_to_add=30,
    k_to_remove=30,
)
print(f"   Contrast added features: {contrast.top_to_add}")
print(f"   Contrast removed features: {contrast.top_to_remove}")

rerank = await client.features.rerank(
    query="funny",
    model=variant,
    features=contrast.top_to_remove,
    top_k=10,
)
print(f"   ✓ Rerank successful")
print(f"   Reranked features: {rerank.data}")
```

**Sample output (truncated):**

```text
   Contrast added features: [FeatureItem(id='8bb53ed7-ed2f-4166-9161-13df6006451d', label='Assistant responding to casual greetings about its wellbeing', ...), ...]
   Contrast removed features: [FeatureItem(id='20addfb3-7f1e-4fb3-be0d-54f70c61a27d', label='Action phrases in joke setups and story narratives', ...), ...]

   Reranked features: [FeatureItem(id='fff8afce-908c-4d4b-a161-389eb8b83c4a', label='Transition between joke setup and punchline', ...), ...]
```

## License

Apache 2.0

## Links

- [Documentation](https://docs.vllm.ai/en/latest/)
- [GitHub Repository](https://github.com/vllm-project/vllm)
- [Issue Tracker](https://github.com/vllm-project/vllm/issues)
