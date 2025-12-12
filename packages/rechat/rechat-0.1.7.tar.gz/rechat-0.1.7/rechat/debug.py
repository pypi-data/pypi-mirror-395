html=r"""
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <title>Rechat Debug</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/styles/github.min.css">
        <style>
            body { font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 0; display: flex; height: 100vh; }
            #sidebar { width: 260px; border-right: 1px solid #ddd; padding: 12px; box-sizing: border-box; }
            #content { flex: 1; padding: 12px; overflow: auto; box-sizing: border-box; }
            input[type=text] { width: 100%; padding: 6px 8px; box-sizing: border-box; margin-bottom: 8px; }
            pre { white-space: pre-wrap; word-wrap: break-word; }

            /* Blockquote styling similar to GitHub's */
            blockquote {
                margin: 12px 0;
                padding: 8px 12px;
                border-left: 4px solid #d0d7de;  /* left border */
                background: #f6f8fa;             /* subtle background */
                border-radius: 4px;
                color: #24292f;
            }

            /* Optional: tighten nested paragraphs */
            blockquote > p {
                margin: 0;
            }

            /* Optional: if your markdown uses nested blockquotes, soften them slightly */
            blockquote blockquote {
                background: #eef2f7;
                border-left-color: #c5ced8;
            }

            /* Code block styling */
            pre code.hljs {
                display: block;
                padding: 12px;
                border-radius: 6px;
                background: #f5f5dc;    /* light GitHub-style background */
                font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
                font-size: 13px;
            }
            .match { background: #fff3bf; }
        </style>
        <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/highlight.min.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/languages/python.min.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.9.0/build/languages/markdown.min.js"></script>
    </head>
    <body>
        <div id="sidebar">
            <h3 style="margin-top:0">Rechat Debug</h3>
            <input id="search" type="text" placeholder="Search..." />
            <div id="status" style="font-size: 12px; color: #555;"></div>
        </div>
        <div id="content"><em>Loading...</em></div>
        <script>
            marked.setOptions({
                highlight: function(code, lang) {
                    if (lang && hljs.getLanguage(lang)) {
                        return hljs.highlight(code, { language: lang }).value;
                    }
                    return hljs.highlightAuto(code).value;
                }
            });

            async function loadMarkdown() {
                const res = await fetch('/debug.md', {cache: 'no-store'});
                if (!res.ok) {
                    document.getElementById('content').textContent = 'Failed to load markdown: ' + res.status;
                    return '';
                }
                const text = await res.text();
                return text;
            }

            function renderMarkdown(md, query) {
                let source = md;
                if (query) {
                    const esc = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
                    const re = new RegExp(esc, 'gi');
                    source = md.replace(re, m => `==${m}==`);
                }
                let html = marked.parse(source);
                if (query) {
                    const esc = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
                    const re = new RegExp('==(' + esc + ')==', 'gi');
                    html = html.replace(re, '<span class="match">$1</span>');
                }
                document.getElementById('content').innerHTML = html;

                // Ensure highlight.js actually runs on the rendered code blocks
                if (window.hljs) {
                    document
                        .querySelectorAll('#content pre code')
                        .forEach(block => hljs.highlightElement(block));
                }
            }

            (async () => {
                const md = await loadMarkdown();
                const search = document.getElementById('search');
                const status = document.getElementById('status');
                status.textContent = 'Loaded ' + md.length + ' characters';
                renderMarkdown(md, '');

                search.addEventListener('input', () => {
                    const q = search.value.trim();
                    renderMarkdown(md, q);
                });
            })();
        </script>
    </body>
</html>
"""


def get_debug_html() -> str:
    return html

