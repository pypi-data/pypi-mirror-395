# good-common

A small set of common dependencies for Good Kiwi.

# Dependency Provider

BaseProvider is a base class for creating fast_depends (so FastAPI and FastStream compatible) dependency providers.

```python

class APIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get(self, url: str):
        return f"GET {url} with {self.api_key}"

class APIClientProvider(BaseProvider[APIClient], APIClient):
    pass


from fast_depends import inject

@inject
def some_task(
    api_client: APIClient = APIClientProvider(api_key="1234"),
):
    return api_client.get("https://example.com")


```

Can also be used without fast_depends:

```python

client = APIClientProvider(api_key="1234").get()

```

Override `initializer` to customize how the dependency class is initialized.

```python

class APIClientProvider(BaseProvider[APIClient], APIClient):
    def initializer(
        self,
        cls_args: typing.Tuple[typing.Any, ...],  # args passed to the Provider
        cls_kwargs: typing.Dict[str, typing.Any],  # kwargs passed to the Provider
        fn_kwargs: typing.Dict[str, typing.Any],  # kwargs passed to the function at runtime
    ):
        return cls_args, {**cls_kwargs, **fn_kwargs}  # override the api_key with the one passed to the function


@inject
def some_task(
    api_key: str,
    api_client: APIClient = APIClientProvider(),
):
    return api_client.get("https://example.com")


some_task(api_key="5678")

```


# Pipeline

## Overview

The Pipeline library provides a flexible and efficient way to create and execute pipelines of components in Python. It supports both synchronous and asynchronous execution, type checking, parallel processing, and error handling.

## Features

- Create pipelines with multiple components that can accept multiple inputs and produce multiple outputs
- Typed "channels" for passing data between components
- Support for both synchronous and asynchronous components
- Type checking for inputs and outputs using Python type annotations
- Parallel execution of pipeline instances
- Error handling with Result types
- Function mapping for flexible component integration

## Quick Start

```python
from typing import Annotated
from good_common.pipeline import Pipeline, Attribute

def add(a: int, b: int) -> Annotated[int, Attribute("result")]:
    return a + b

def multiply(result: int, factor: int) -> Annotated[int, Attribute("result")]:
    return result * factor

# Create a pipeline
my_pipeline = Pipeline(add, multiply)

# Execute the pipeline
result = await my_pipeline(a=2, b=3, factor=4)
print(result.result)  # Output: 20
```

## Usage

### Creating a Pipeline

Use the `Pipeline` class to create a new pipeline:

```python
from pipeline import Pipeline

my_pipeline = Pipeline(component1, component2, component3)
```

### Defining Components

Components can be synchronous or asynchronous functions:

```python
from typing import Annotated
from pipeline import Attribute

def sync_component(x: int) -> Annotated[int, Attribute("result")]:
    return x + 1

async def async_component(x: int) -> Annotated[int, Attribute("result")]:
    await asyncio.sleep(0.1)
    return x * 2
```

### Executing a Pipeline

Execute a pipeline asynchronously:

```python
result = await my_pipeline(x=5)
print(result.result)
```

### Parallel Execution

Execute a pipeline with multiple inputs in parallel:

```python
inputs = [{"a": 1, "b": 2, "factor": 2}, {"a": 2, "b": 3, "factor": 3}]
results = [result async for result in my_pipeline.execute(*inputs, max_workers=3)]

for result in results:
    if result.is_ok():
        print(result.unwrap().result)
    else:
        print(f"Error: {result.unwrap_err()}")
```

### Error Handling

The pipeline handles errors gracefully in parallel execution:

```python
def faulty_component(x: int) -> Annotated[int, Attribute("result")]:
    if x == 2:
        raise ValueError("Error on purpose!")
    return x + 1

pipeline = Pipeline(faulty_component)
inputs = [{"x": 1}, {"x": 2}, {"x": 3}]
results = [result async for result in pipeline.execute(*inputs)]

for result in results:
    if result.is_ok():
        print(result.unwrap().result)
    else:
        print(f"Error: {result.unwrap_err()}")
```

### Function Mapping

Use `function_mapper` to adjust input parameter names:

```python
from pipeline import function_mapper

def multiply_diff(difference: int, factor: int) -> Annotated[int, Attribute("result")]:
    return difference * factor

pipeline = Pipeline(subtract, function_mapper(multiply_diff, diff="difference"))
```

## Advanced Features

- Mixed synchronous and asynchronous components in a single pipeline
- Custom output types with `Attribute` annotations
- Flexible error handling in both single and parallel executions


# URL Plugin System

The URL class in good-common now supports a plugin system for extending URL processing capabilities without modifying the core library.

## Features

- Extend URL canonicalization rules
- Add custom tracking parameters to filter
- Define domain-specific processing rules
- Add URL classification patterns
- Register short URL providers and bio link domains
- Apply custom URL transformations

## Built-in Plugins

Good-common includes several built-in plugins for common use cases:

### ECommerceURLPlugin
Handles e-commerce website URLs (Amazon, eBay, Etsy, AliExpress, etc.)
- Removes tracking parameters like `ref`, `hash`, `_trkparms`
- Preserves product identifiers and search parameters
- Transforms mobile URLs to desktop versions
- Classifies product pages, search results, shopping carts

### AnalyticsTrackingPlugin  
Removes analytics and tracking parameters from all major platforms
- Google Analytics (`utm_*`, `gclid`, etc.)
- Facebook (`fbclid`, `fb_*`)
- Microsoft/Bing (`msclkid`)
- Email marketing (`mc_cid`, `_hsenc`, `mkt_tok`)
- Social media tracking parameters
- Preserves content identifiers and navigation parameters

### VideoStreamingPlugin
Handles video platform URLs (YouTube, Vimeo, Twitch, etc.)
- Removes tracking parameters like `feature`, `ab_channel`
- Preserves video IDs, timestamps, and playlist information
- Transforms mobile YouTube URLs to desktop
- Classifies video pages, channels, playlists

### SearchEnginePlugin
Processes search engine URLs (Google, Bing, DuckDuckGo)
- Removes search tracking parameters (`ved`, `ei`, `source`)
- Preserves search queries and result types
- Overrides built-in disable rules for Google
- Classifies different search types (images, videos, maps)

### DocumentSharingPlugin
Handles document and cloud storage platforms (Google Drive/Docs, Dropbox, Box)
- Removes sharing tracking parameters (`usp`, `dl`, `raw`)
- Preserves document identifiers and view settings
- Classifies different document types

## Using Built-in Plugins

```python
from good_common.types.builtin_plugins import load_builtin_plugins

# Load all built-in plugins
load_builtin_plugins()

# Load specific plugins only
load_builtin_plugins(["ecommerce", "analytics", "video"])

# Use enhanced URL processing
url = URL("https://www.amazon.com/dp/B123?ref=sr&utm_source=google")
canonical = url.canonicalize()  # Removes both ref and utm_source
```

## Creating a Plugin

```python
from good_common.types import URLPlugin
import re

class MyURLPlugin(URLPlugin):
    def get_tracking_params(self) -> Set[str]:
        """Additional tracking parameters to remove during canonicalization."""
        return {"my_tracking_id", "custom_ref"}
    
    def get_canonical_params(self) -> Set[str]:
        """Parameters that should be preserved."""
        return {"article_id", "product_id"}
    
    def get_domain_rules(self) -> Dict[str, Dict[str, Any]]:
        """Domain-specific canonicalization rules."""
        return {
            r".*\.mysite\.com": {
                "canonical": {"id", "page"},
                "non_canonical": {"session", "temp"},
                "force_www": True,
            }
        }
    
    def get_short_url_providers(self) -> Set[str]:
        """Additional short URL domains."""
        return {"mylink.co", "short.link"}
    
    def get_classification_patterns(self) -> Dict[str, Pattern]:
        """Custom URL classification patterns."""
        return {
            "product_page": re.compile(r"/products?/[\w-]+"),
            "category_page": re.compile(r"/categor(y|ies)/[\w-]+"),
        }
    
    def transform_url(self, url: 'URL', config: 'UrlParseConfig') -> Optional['URL']:
        """Apply custom URL transformations."""
        from good_common.types import URL
        
        # Example: Rewrite mobile URLs to desktop
        if url.host == "m.mysite.com":
            return URL.build(
                scheme="https",
                host="www.mysite.com",
                path=url.path,
                query=url.query_params(format="plain", flat_delimiter=","),
            )
        return None
```

## Registering Plugins

### Method 1: Entry Points (Recommended for Packages)

Add to your package's `pyproject.toml`:

```toml
[project.entry-points."good_common.url_plugins"]
my_plugin = "my_package.plugins:MyURLPlugin"
social_media = "my_package.plugins:SocialMediaPlugin"
```

Plugins registered via entry points are automatically loaded when the good-common module is imported.

### Method 2: Direct Registration

```python
from good_common.types import URL, URLPlugin

class MyPlugin(URLPlugin):
    # ... implementation ...

# Register at class level
URL.register_plugin(MyPlugin())

# Or use the global registry
from good_common.types import url_plugin_registry
url_plugin_registry.register(MyPlugin())
```

### Method 3: Runtime Registration

```python
from good_common.types import URL

# Create and register a plugin at runtime
plugin = MyURLPlugin()
URL.register_plugin(plugin)

# Use the enhanced URL functionality
url = URL("https://example.com/page?my_tracking_id=123&article_id=456")
canonical = url.canonicalize()  # my_tracking_id will be removed, article_id preserved

# Check custom classifications
classifications = url.classify()
if classifications.get("product_page"):
    print("This is a product page")

# Unregister when done
URL.unregister_plugin(plugin)
```

## Example Plugins

The library includes example plugins in `good_common.types.example_plugin`:

- **SocialMediaURLPlugin**: Handles social media specific parameters and transformations
- **NewsMediaURLPlugin**: Manages news site tracking parameters and classifications

```python
from good_common.types.example_plugin import SocialMediaURLPlugin

# Use the pre-built social media plugin
plugin = SocialMediaURLPlugin()
URL.register_plugin(plugin)

# Now URLs from social media sites will be processed with specialized rules
url = URL("https://instagram.com/p/ABC123?igshid=tracker")
canonical = url.canonicalize()  # igshid parameter will be removed
```

## Performance Considerations

- Plugins are designed with minimal overhead (<10% when registered)
- Plugin data is cached for efficiency
- Lazy loading ensures plugins only impact performance when used
- Use entry points for automatic loading or register manually for fine control

# Utilities

Various utility functions for common tasks.

Look at `/tests/good_common/utilities` for usage