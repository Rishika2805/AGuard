# sources/gmail/fetcher.py

def fetch_message_ids(service,max_results=10):
    """
    Fetch Gmail message ids.
    """
    response = service.users().messages().list(
    userId="me",
    maxResults=max_results
    ).execute()

    return response.get('messages',[])

def fetch_full_message(service,message_id):
    """
    Fetch full Gmail message using message id.
    """

    message = service.users().messages().get(
        userId="me",
        id=message_id,
        format = 'full'
    ).execute()

    return message