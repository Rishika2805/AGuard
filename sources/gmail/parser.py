# sources/gmail/parser.py
import base64


def _get_header(headers,name):
    for header in headers:
        if header['name'].lower() == name.lower():
            return header['value']
    return None

def _get_body(payload):
    """
    Extract email body from payload
    """
    body_text = ""
    body_html = ""

    def decode(data):
        return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

    if "parts" in payload:
        for part in payload["parts"]:
            mime = part.get("mimeType", "").lower()
            data = part.get("body", {}).get("data")

            if mime == "text/plain" and data and not body_text:
                body_text = decode(data)

            elif mime == "text/html" and data and not body_html:
                body_html = decode(data)

    else:
        data = payload.get("body", {}).get("data")
        if data:
            body_text = decode(data)

    # Prefer plain text, fallback to HTML
    return body_text if body_text else body_html



def parse_email(message):
    """
    Parse raw email message into clean format
    """

    payload = message['payload']
    headers = payload.get('headers',[])

    return {
        'source': 'gmail',
        'id' : message['id'],
        'sender' : _get_header(headers,'From') or "",
        'title' : _get_header(headers,'Subject') or "",
        'timestamp' : _get_header(headers,'Date') or "",
        'content' : _get_body(payload) or "",
        'url' : None,
        'tags' : []
    }