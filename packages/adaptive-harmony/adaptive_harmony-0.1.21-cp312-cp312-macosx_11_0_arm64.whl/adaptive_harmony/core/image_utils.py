import base64
import html
import io
import os

from PIL import Image

from adaptive_harmony import StringThread


def save_inlined_string_to_png(image_str: str, path_to_save: str):
    _, base64_str = image_str.split(",")
    image_data = base64.b64decode(base64_str)
    image = Image.open(io.BytesIO(image_data))
    image.save(path_to_save)


def save_string_thread_to_markdown_dir(thread: StringThread, directory_path: str):
    all_fragments = thread.get_fragments()

    os.makedirs(directory_path, exist_ok=True)
    image_counter = 0
    with open(os.path.join(directory_path, "main.md"), "w") as w:
        for role, fragments in all_fragments:
            w.write(f"# {role}\n")
            for fragment in fragments:
                if fragment["type"] == "text":
                    w.write(fragment["text"])
                else:
                    assert fragment["type"] == "image"
                    filename = f"image_{image_counter}.jpeg"
                    image_path = os.path.join(directory_path, filename)
                    save_inlined_string_to_png(fragment["url"], image_path)
                    w.write(f"![image info]({filename})\n")


def string_thread_to_html_string(thread: StringThread) -> str:
    """
    Converts a StringThread into a single, valid HTML string.
    Text is converted to paragraphs, and images are embedded directly
    using their base64 data URIs.
    """
    html_parts = []
    all_fragments = thread.get_fragments()

    for role, fragments in all_fragments:
        # Use a heading for the role (e.g., 'user', 'model')
        html_parts.append(f"<h2>{role.capitalize()}</h2>")
        for fragment in fragments:
            if fragment["type"] == "text":
                # Escape HTML special characters. CSS will handle wrapping and newlines.
                text_content = html.escape(fragment["text"])
                html_parts.append(f"<p>{text_content}</p>")
            elif fragment["type"] == "image":
                # The 'url' is the data URI, which can be used directly in the <img> src
                image_url = fragment["url"]
                html_parts.append(
                    f'<img src="{image_url}" alt="Embedded image content" style="max-width: 500px; height: auto; display: block; margin: 10px 0;">'
                )

    # Combine all parts into a single string
    body_content = "\n".join(html_parts)

    # Wrap the content in a complete, styled HTML document
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>StringThread Conversation</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #000000; 
            margin: 20px auto;
            padding: 0 20px;
        }}
        h2 {{
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
            margin-top: 40px;
            margin-left: 40px;
            width: 600px;
            color: #000000; 
        }}
        p {{
            width: 600px;
            margin: 16px 0;
            margin-left: 40px;
            word-break: break-word; /* Helps with breaking long words if needed */
            white-space: pre-wrap; /* Preserve newlines and wrap long lines */
        }}
        img {{
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 5px;
            background-color: #ffffff; /* Changed to white */
        }}
    </style>
</head>
<body>
    <div style="background-color: #ffffff; width: 680px;">
        <h1>Conversation Thread</h1>
        {body_content}
    </div>
</body>
</html>
"""
