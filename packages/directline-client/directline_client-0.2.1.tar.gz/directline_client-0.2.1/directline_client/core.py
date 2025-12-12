"""
directline_client.client
========================

A lightweight Python client for Microsoft Bot Framework Direct Line,
suitable for interacting with LLM-powered bots. The client handles:

- Conversation creation
- Sending user messages
- Polling bot responses
- A helper method (`call_llm`) to send a prompt and wait for the bot’s answer
"""

import logging
import time
import uuid
import requests

class DirectLineClient:
    """
    A simple Direct Line (Bot Framework) client for interacting with bots
    as if they were LLM endpoints.

    Parameters
    ----------
    secret : str, optional
        The Direct Line secret (required to authenticate).
    endpoint : str, optional
        Base Direct Line API endpoint.
        Default: "https://directline.botframework.com/v3/directline"
    user_name : str, optional
        Display name for the user sending messages.
        Default: "PythonUser"

    Attributes
    ----------
    secret : str
        Authentication secret.
    endpoint : str
        Target Direct Line endpoint.
    user_id : str
        Randomly generated unique identifier for the client.
    conversation_id : str | None
        ID of the active conversation.
    watermark : str
        Tracks last processed bot message.
    headers : dict
        Authorization header for Direct Line.
    user_name : str
        User display name.

    Usage Example
    -------------
    >>> from directline_client import DirectLineClient
    >>> client = DirectLineClient(secret="YOUR_SECRET")
    >>> response = client.call_llm("Hello bot!")
    >>> print(response)
    """

    def __init__(
        self,
        secret: str | None = None,
        endpoint: str | None = None,
        user_name: str = "PythonUser",
    ):
        self.secret = secret
        self.endpoint = endpoint or "https://directline.botframework.com/v3/directline"
        self.user_id = f"dl_user_{uuid.uuid4()}"
        self.conversation_id = None
        self.watermark = "0"
        self.user_name = user_name

        self.headers = {"Authorization": f"Bearer {self.secret}"} if self.secret else {}

        if not self.secret:
            logging.warning(
                "DirectLineClient: No secret provided. "
                "Client will not work until a Direct Line secret is supplied."
            )

    # ----------------------------------------------------------------------
    def start_conversation(self) -> str | None:
        """
        Starts a new Direct Line conversation.

        Returns
        -------
        str | None
            The conversation ID, or None if the request fails.
        """
        if not self.secret:
            return None

        try:
            resp = requests.post(
                f"{self.endpoint}/conversations",
                headers=self.headers,
                timeout=10,
            )
            resp.raise_for_status()

            self.conversation_id = resp.json().get("conversationId")
            self.watermark = "0"

            logging.info(f"DirectLine: conversation started {self.conversation_id}")
            return self.conversation_id

        except requests.RequestException as e:
            logging.error(f"DirectLine: error starting conversation: {e}")
            return None

    # ----------------------------------------------------------------------
    def send_message(self, conversation_id: str, message_text: str) -> bool:
        """
        Sends a text message to the bot.

        Parameters
        ----------
        conversation_id : str
            The conversation ID returned by `start_conversation()`.
        message_text : str
            The message text to send.

        Returns
        -------
        bool
            True if the message was sent successfully, False otherwise.
        """
        if not self.secret:
            return False

        payload = {
            "type": "message",
            "from": {"id": self.user_id, "name": self.user_name},
            "text": message_text,
        }

        try:
            resp = requests.post(
                f"{self.endpoint}/conversations/{conversation_id}/activities",
                headers=self.headers,
                json=payload,
                timeout=10,
            )
            resp.raise_for_status()
            return True

        except requests.RequestException as e:
            logging.error(f"DirectLine: error sending message: {e}")
            return False

    # ----------------------------------------------------------------------
    def poll_responses(self, conversation_id: str, since_watermark: str = "0"):
        """
        Polls bot messages since the last seen watermark.

        Parameters
        ----------
        conversation_id : str
            The Direct Line conversation ID.
        since_watermark : str, optional
            Last watermark processed.

        Returns
        -------
        (list[str], str)
            A tuple (messages, new_watermark).
        """
        if not self.secret:
            return [], since_watermark

        url = (
            f"{self.endpoint}/conversations/"
            f"{conversation_id}/activities?watermark={since_watermark}"
        )

        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            bot_messages = []
            for activity in data.get("activities", []):
                if (
                    activity.get("type") == "message"
                    and activity.get("from", {}).get("id") != self.user_id
                ):
                    if activity.get("text"):
                        bot_messages.append(activity["text"])

            new_watermark = data.get("watermark", since_watermark)
            return bot_messages, new_watermark

        except requests.RequestException as e:
            logging.error(f"DirectLine: poll error: {e}")
            return [], since_watermark

    # ----------------------------------------------------------------------
    def call_llm(
        self,
        prompt: str,
        timeout: int = 30,
        poll_interval: float = 1.0,
    ) -> str:
        """
        Sends a prompt to the bot and waits for a response.

        Parameters
        ----------
        prompt : str
            The prompt or user query to send to the bot.
        timeout : int, optional
            Maximum wait time in seconds.
        poll_interval : float, optional
            Pause between polling attempts.

        Returns
        -------
        str
            The concatenated bot response (or empty string if no response was received).
        """
        if not self.secret:
            logging.error("Direct Line secret not set. call_llm cannot run.")
            return "Direct Line secret not set. call_llm cannot run."
        
        if self.conversation_id is None: 
            self.start_conversation()

        if self.conversation_id is None:
            logging.error("DirectLine: failed to start conversation.")
            return "DirectLine: failed to start conversation."

        if not self.send_message(self.conversation_id, prompt):
            logging.error("DirectLine: failed to send prompt.")
            return "DirectLine: failed to send prompt."

        start_time = time.time()
        collected = []
        current_wm = self.watermark or "0"

        while time.time() - start_time < timeout:
            msgs, new_wm = self.poll_responses(self.conversation_id, current_wm)

            if msgs:
                collected.extend(msgs)
                current_wm = new_wm
                break

            time.sleep(poll_interval)

        self.watermark = current_wm

        if collected:
            return "\n\n".join(collected)

        logging.warning("DirectLine: no messages received before timeout.")
        return "DirectLine: no messages received before timeout."