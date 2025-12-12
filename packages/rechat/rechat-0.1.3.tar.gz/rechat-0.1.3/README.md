# Rechat

Rechat is a caching and replaying man-in-the-middle proxy for OpenAI's APIs, it provides inspection and debugging layer, particularly useful for quick inspection of interactions of existing clients, developing multi-request workflows, and benchmarks.

Rechat is for you, if you ever wanted to:
- speed up your code that makes repeated calls to OpenAI APIs
- quickly inspect what is being sent to OpenAI APIs
- emulate an endpoint with pre-recorded (or pre-defined) responses



## Quickstart

1. `pip install rechat`   (dev: `pip install git+https://gitlab-master.nvidia.com/dchichkov/rechat.git`)
2. Run `rechat`, it will listen on eight-nine-ten port (http://localhost:8910/v1) and use OpenAI's endpoint by default as upstream.
3. Configure your OpenAI client to use it `export OPENAI_BASE_URL=http://localhost:8910/v1` and run your requests as usual.

You can specify a different upstream endpoint by providing it as an argument, e.g. `rechat https://api.openai.com/v1`.

By default, rechat outputs intercepted chat content onto the console:

![Rechat Console](docs/rechat.jpg)


And it records the session to `flows_<timestamp>.dump` file in the current directory. During subsequent runs, if a `-f/--flow [dump_file]` argument is provided, rechat would attempt to load `flows_[timestamp].dump` files, or the specified dump file. It always tries to use cached responses for any matching requests.


## Inspection and Debugging

Rechat provides `http://localhost:8910` web UI for inspecting the current session, with search and filtering capabilities.

By default, rechat will output chat content to the console. Use `--quiet` flag to reduce verbosity. Use `--verbose` flag to include cache hits. Any markdown editor, for example VSCode or GitHub/GitLab web UI, can be used to view and edit the logs, and these modified logs can be loaded into rechat, to emulate model's responses.

## Example
Example markdown snippet, in markdown format. Note `<blockquote>` tags. See more details in [sample.md](docs/sample.md).
```markdown
### user
<blockquote>
What is the capital of France?
</blockquote>

### assistant
<blockquote>
Paris.
</blockquote>
```

## Intercepting traffic to existing OpenAI endpoints

Rechat can intercept traffic to existing OpenAI endpoints, without changing the client code, by using `mitmproxy` as a transparent proxy. For example, to use mitmproxy local proxy mode and intercept traffic to `https://api.openai.com/v1`, run:

```bash
mitmproxy --mode local --scripts rechat.py
```


## Routing and Load Balancing

Rechat supports multiple endpoints, using `<endpoint>:[local_port]:[model_name]` arguments, e.g. `https://api.openai.com/v1:8910:gpt-5`. It would route the requests to the appropriate endpoint based on the model name in the request, and it'd balance the load between endpoints for the same model.


## Miscellaneous

* Replaying queries against an endpoint
* Multiple responses for the same request


