from difflib import unified_diff
from mitmproxy import http, io, ctx
import json, argparse, re

def markdown_blockquote(md: str) -> str:
    """Converts HTML style '<blockquote>\n\n...\n\n</blockquote>' to markdown style chevrons.
       It supports nested blockquotes and uses '> ' for blockquote levels.    
    """
    print(md)

    pattern = r'(<blockquote[^>]*>\n\n|\n\n</blockquote>)'
    parts = re.split(pattern, md)
    
    result = []
    level = 0
    
    for part in parts:
        if re.match(r'<blockquote[^>]*>\n\n', part):
            level += 1
        elif part == '\n\n</blockquote>':
            level = max(0, level - 1)
        else:
            lines = part.split('\n')
            for i, line in enumerate(lines):
                if level > 0:
                    result.append('> ' * level + line)
                else:
                    result.append(line)
                if i < len(lines) - 1:
                    result.append('\n')
    
    return ''.join(result)


def message_to_markdown(role: str, content: str, blockquote: str = 'html') -> str:
    if blockquote == 'html':
        md = f"### {role}\n<blockquote>\n\n{content}\n\n</blockquote>\n\n"
    elif blockquote == 'markdown':
        content = '\n'.join([f"> {line}" for line in content.splitlines()])
        md = f"### {role}\n{content}\n"
    else:
        content = markdown_blockquote(content)
        md = f"### {role}\n{content}\n"
    return md



def request_to_markdown(request: http.Request, blockquote: str = 'html') -> str:
    body = json.loads(request.get_text())
    md = ""

    # Output Jekyll-compatible header with request settings, like model and temperature
    md += "---\n"
    for key, value in body.items():
        if key != "messages":
            md += f"{key}: {value}\n"
    md += "---\n\n"

    # Output messages
    messages = body.get("messages", [])
    for message in messages:
        md += message_to_markdown(message["role"], message["content"], blockquote=blockquote)

    return md

def response_to_markdown(response: http.Response, blockquote: str = 'html') -> str:
    # TODO: handle reasoning traces, response choices, etc.
    body = json.loads(response.get_text())
    choices = body.get("choices", [])
    md = ""
    for choice in choices:
        message = choice["message"]
        md += message_to_markdown(message["role"], message["content"], blockquote=blockquote)

    return md


def flow_to_markdown(flow: http.HTTPFlow, blockquote: str = 'html') -> str:
    md = request_to_markdown(flow.request, blockquote=blockquote)
    md += response_to_markdown(flow.response, blockquote=blockquote)
    return md


def unified_requests_diff(a: http.Request, b: http.Request, fromfile='', tofile=''):
    """Generate a unified diff for chat requests."""

    a_md = request_to_markdown(a, blockquote='markdown')
    b_md = request_to_markdown(b, blockquote='markdown')

    diff = '\n'.join(unified_diff(a_md.splitlines(), b_md.splitlines(), fromfile=fromfile, tofile=tofile))
    return diff




def test_unified_requests_diff():
    a = {"messages":[{"role":"user","content":"What is the capital of France?"},{"role":"assistant","content":"Paris. "},{"role":"user","content":"Write a Python example that returns a string: This is a test."},{"role":"assistant","content":"Here is a small Python example that returns the string:\n\n```python\ndef get_string():\n    return \"This is a test.\"\n\n# Example usage\nresult = get_string()\nprint(result)\n```"},{"role":"user","content":"Can you provide a very basic example of Markdown formatting?"},{"role":"assistant","content":"Sure! Here's a very basic example of Markdown formatting:\n\n```markdown\n# Heading 1\n## Heading 2\n```\n\nThe above example shows how to create headings in Markdown:\n- A single `#` creates a top-level heading (Heading 1)\n- Two `##` create a second-level heading (Heading 2).\n         \nHere's how it looks when rendered:\n# Heading 1\n## Heading 2\n"},{"role":"user","content":"Thank you!, that's all for now, goodbye."}],"model":"gpt-5-nano"}
    b = {"messages":[{"role":"user","content":"What is the capital of France?"},{"role":"assistant","content":"Paris.  "},{"role":"user","content":"Write a Python example that returns a string: This is a test."},{"role":"assistant","content":"Here is a small Python example that returns the string:\n\n```python\ndef get_string():\n    return \"This is a test.\"\n\n# Example usage\nresult = get_string()\nprint(result)\n```"},{"role":"user","content":"Can you provide a very basic example of Markdown formatting?"},{"role":"assistant","content":"Sure! Here's a very basic example of Markdown formatting:\n\n```markdown\n# Heading 1\n## Heading 2\n```\n\nThe above example shows how to create headings in Markdown:\n- A single `#` creates a top-level heading (Heading 1)\n- Two `##` create a second-level heading (Heading 2).\n         \nHere's how it looks when rendered:\n# Heading 1\n## Heading 2\n"},{"role":"user","content":"Thank you!, that's all for now, goodbye."}],"model":"gpt-5-nano"}


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Convert mitmproxy flows to markdown")
    parser.add_argument("dump_path", help="Path to the mitmproxy dump file")
    args = parser.parse_args()

    with open(args.dump_path, "rb") as f:
        reader = io.FlowReader(f)
        for flow in reader.stream():
            if isinstance(flow, http.HTTPFlow):
                if flow.request.method.upper() == "POST":
                    print(f"## interaction: {flow.id}\n<blockquote>\n")
                    print(flow_to_markdown(flow))
                    print("</blockquote>\n")