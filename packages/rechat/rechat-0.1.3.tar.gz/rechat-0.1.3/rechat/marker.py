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


def flow_to_markdown(flow: http.HTTPFlow) -> str:
    body = json.loads(flow.request.get_text())
    md = ""

    # Output Jekyll-compatible header with request settings, like model and temperature
    md += "---\n"
    for key, value in body.items():
        if key != "messages":
            md += f"{key}: {value}\n"
    md += "---\n\n"

    messages = body.get("messages", [])
    for message in messages:
        role = message.get("role", "unknown")
        content = message.get("content", "")
        md += f"### {role}\n<blockquote>\n\n{content}\n\n</blockquote>\n\n"

    response_body = json.loads(flow.response.get_text())
    choices = response_body.get("choices", [])
    for choice in choices:
        message = choice.get("message", {})
        content = message.get("content", "")
        md += f"### assistant\n<blockquote>\n\n{content}\n\n</blockquote>\n\n"

    return md



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