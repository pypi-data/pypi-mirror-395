import os
import requests
import json

class AgentAiClient:
    """
    A Python client for the Agent.ai Actions API (Action-Based Interface).
    
    Example:
        >>> from agentai import AgentAiClient
        >>> client = AgentAiClient()  # Uses AGENTAI_API_KEY env var
        >>> # or
        >>> client = AgentAiClient(bearer_token="your_token_here")
    """
    BASE_URL = "https://api-lr.agent.ai/v1"

    ACTION_ENDPOINTS = {
        "grabWebText": "/action/grab_web_text",
        "grabWebScreenshot": "/action/grab_web_screenshot",
        "getYoutubeTranscript": "/action/get_youtube_transcript",
        "getYoutubeChannel": "/action/get_youtube_channel",
        "getTwitterUsers": "/action/get_twitter_users",
        "getGoogleNews": "/action/get_google_news",
        "runYoutubeSearch": "/action/run_youtube_search",
        "getSearchResults": "/action/get_search_results",
        "getRecentTweets": "/action/get_recent_tweets",
        "getLinkedinProfile": "/action/get_linkedin_profile",
        "getLinkedinActivity": "/action/get_linkedin_activity",
        "getCompanyObject": "/action/get_company_object",
        "getBlueskyPosts": "/action/get_bluesky_posts",
        "searchBlueskyPosts": "/action/search_bluesky_posts",
        "getInstagramProfile": "/action/get_instagram_profile",
        "getInstagramFollowers": "/action/get_instagram_followers",
        "outputAudio": "/action/output_audio",
        "invokeLlm": "/action/invoke_llm",
        "generateImage": "/action/generate_image",
        "storeVariableToDatabase": "/action/store_variable_to_database",
        "getVariableFromDatabase": "/action/get_variable_from_database",
        "invokeAgent": "/action/invoke_agent",
        "restCall": "/action/rest_call",
        "convertFile": "/action/convert_file",
        "convertFileOptions": "/action/convert_file_options",
    }

    def __init__(self, bearer_token=None):
        """
        Initializes the AgentAiClient with a Bearer token.

        Args:
            bearer_token (str, optional): The Bearer token for API authentication.
                If not provided, will look for AGENTAI_API_KEY environment variable.
        
        Raises:
            ValueError: If no bearer token is provided and AGENTAI_API_KEY env var is not set.
        """
        self.bearer_token = bearer_token or os.environ.get("AGENTAI_API_KEY")
        
        if not self.bearer_token:
            raise ValueError(
                "No API key provided. Either pass bearer_token to the constructor "
                "or set the AGENTAI_API_KEY environment variable."
            )
        
        self.headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "Content-Type": "application/json"
        }

    def _handle_response(self, response):
        """
        Handles API responses, checks for errors, and returns a consistent dictionary.

        Args:
            response (requests.Response): The response object from requests.

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
                  'status' (int): HTTP status code.
                  'error' (str or None): Error message if status is not 200, None otherwise.
                  'results' (dict or str or None): API response data if successful, None otherwise.
                  'metadata' (dict or None): Metadata from the API response, if available.

        """
        response_data = {
            "status": response.status_code,
            "error": None,
            "results": None,
            "metadata": None
        }

        try:
            json_response = response.json()
            if response.status_code == 200:
                response_data["results"] = json_response.get('response')
                response_data["metadata"] = json_response.get('metadata')
            else:
                response_data["error"] = json_response.get('error', response.text) # Get error from JSON or text
        except json.JSONDecodeError:
            if response.status_code != 200: # Only set error if not successful
                response_data["error"] = f"JSON Decode Error: {response.text}"
            else:
                response_data["results"] = response.text # if 200 but not json, return text as result


        return response_data


    def _post(self, endpoint, data, timeout=60):
        """
        Internal method to make a POST request to the API.

        Args:
            endpoint (str): The API endpoint path.
            data (dict): The request body data as a dictionary.
            timeout (int): Request timeout in seconds. Default is 60.

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
        """
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.post(url, headers=self.headers, json=data, timeout=timeout)
            # Don't raise_for_status() - let _handle_response() process the response
            # so we can extract meaningful error messages from the API
            return self._handle_response(response)
        except requests.exceptions.Timeout:
            return {
                "status": None,
                "error": "Request timed out. Try increasing the timeout or try again later.",
                "results": None,
                "metadata": None
            }
        except requests.exceptions.ConnectionError:
            return {
                "status": None,
                "error": "Connection error. Please check your internet connection.",
                "results": None,
                "metadata": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "status": None,
                "error": f"Request Exception: {e}",
                "results": None,
                "metadata": None
            }


    def action(self, action_id, params):
        """
        Generic method to execute an AI action by its ID.

        Args:
            action_id (str): The ID of the action to execute (operationId from OpenAPI spec).
            params (dict):  Parameters for the action as a dictionary.

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
        """
        endpoint_path = self.ACTION_ENDPOINTS.get(action_id)
        if not endpoint_path:
            return {
                "status": 400, # Or another appropriate error code
                "error": f"Invalid action_id: {action_id}",
                "results": None,
                "metadata": None
            }
        return self._post(endpoint_path, params)


    def chat(self, prompt, model="gpt4o", **kwargs):
        """
        Use the invokeLlm action to generate text based on a prompt.

        Args:
            prompt (str): The text prompt for the LLM.
            model (str, optional): LLM model to use. Defaults to "gpt4o".
                Available models: "gpt4o", "gpt4o-mini", "claude-sonnet", "claude-haiku", 
                "gemini-pro", "gemini-flash", "llama-70b", "llama-8b", "deepseek"
            **kwargs: Additional parameters to pass to the invokeLlm action.

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
        """
        params = {"instructions": prompt, "llm_engine": model, **kwargs}
        return self.action(action_id="invokeLlm", params=params)

    # Convenience methods for common actions
    
    def grab_web_text(self, url, mode="scrape"):
        """
        Fetch text content from a web page.

        Args:
            url (str): The URL to fetch text from.
            mode (str, optional): "scrape" for single page, "crawl" for multiple pages. 
                Defaults to "scrape".

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
        """
        return self.action(action_id="grabWebText", params={"url": url, "mode": mode})
    
    def grab_web_screenshot(self, url, full_page=False):
        """
        Take a screenshot of a web page.

        Args:
            url (str): The URL to screenshot.
            full_page (bool, optional): Whether to capture the full page. Defaults to False.

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
                  Results contains the screenshot URL.
        """
        return self.action(action_id="grabWebScreenshot", params={
            "url": url, 
            "full_page": full_page
        })
    
    def get_youtube_transcript(self, url):
        """
        Get the transcript of a YouTube video.

        Args:
            url (str): The YouTube video URL.

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
        """
        return self.action(action_id="getYoutubeTranscript", params={"url": url})
    
    def get_youtube_channel(self, channel_url):
        """
        Get information about a YouTube channel.

        Args:
            channel_url (str): The YouTube channel URL.

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
        """
        return self.action(action_id="getYoutubeChannel", params={"channel_url": channel_url})
    
    def search_youtube(self, query, max_results=10):
        """
        Search YouTube for videos.

        Args:
            query (str): The search query.
            max_results (int, optional): Maximum number of results. Defaults to 10.

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
        """
        return self.action(action_id="runYoutubeSearch", params={
            "query": query,
            "max_results": str(max_results)
        })
    
    def get_google_news(self, query, date_range="7d", location="US"):
        """
        Get Google News articles for a query.

        Args:
            query (str): The search query.
            date_range (str, optional): Time range - "1d", "7d", "30d", "1y". Defaults to "7d".
            location (str, optional): Location for news. Defaults to "US".

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
        """
        return self.action(action_id="getGoogleNews", params={
            "query": query,
            "date_range": date_range,
            "location": location
        })
    
    def search_web(self, query, num_results=10):
        """
        Get search results from the web.

        Args:
            query (str): The search query.
            num_results (int, optional): Number of results to return. Defaults to 10.

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
        """
        return self.action(action_id="getSearchResults", params={
            "query": query,
            "num_results": str(num_results)
        })
    
    def get_linkedin_profile(self, profile_handle):
        """
        Get LinkedIn profile information.

        Args:
            profile_handle (str): The LinkedIn profile handle (e.g., "in/username" or "company/name").

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
        """
        return self.action(action_id="getLinkedinProfile", params={"profile_handle": profile_handle})
    
    def get_linkedin_activity(self, profile_handle, num_posts=10):
        """
        Get recent LinkedIn activity for a profile.

        Args:
            profile_handle (str): The LinkedIn profile handle.
            num_posts (int, optional): Number of posts to retrieve. Defaults to 10.

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
        """
        return self.action(action_id="getLinkedinActivity", params={
            "profile_handle": profile_handle,
            "num_posts": str(num_posts)
        })
    
    def get_company_info(self, domain):
        """
        Get company information from a domain.

        Args:
            domain (str): The company's domain (e.g., "hubspot.com").

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
        """
        return self.action(action_id="getCompanyObject", params={"domain": domain})
    
    def get_twitter_user(self, handle):
        """
        Get Twitter/X user profile information.

        Args:
            handle (str): The Twitter handle (without @).

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
        """
        return self.action(action_id="getTwitterUsers", params={"profile_handle": handle})
    
    def get_recent_tweets(self, handle, count=10):
        """
        Get recent tweets from a Twitter/X user.

        Args:
            handle (str): The Twitter handle (without @).
            count (int, optional): Number of tweets to retrieve. Defaults to 10.

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
        """
        return self.action(action_id="getRecentTweets", params={
            "profile_handle": handle,
            "recent_tweets_count": str(count)
        })
    
    def get_bluesky_posts(self, handle, count=10):
        """
        Get recent posts from a Bluesky user.

        Args:
            handle (str): The Bluesky handle.
            count (int, optional): Number of posts to retrieve. Defaults to 10.

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
        """
        return self.action(action_id="getBlueskyPosts", params={
            "profile_handle": handle,
            "num_posts": str(count)
        })
    
    def search_bluesky(self, query, count=10):
        """
        Search Bluesky posts.

        Args:
            query (str): The search query.
            count (int, optional): Number of results. Defaults to 10.

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
        """
        return self.action(action_id="searchBlueskyPosts", params={
            "query": query,
            "num_posts": str(count)
        })
    
    def get_instagram_profile(self, handle):
        """
        Get Instagram profile information.

        Args:
            handle (str): The Instagram handle.

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
        """
        return self.action(action_id="getInstagramProfile", params={"profile_handle": handle})
    
    def generate_image(self, prompt, model="DALL-E 3", style="digital art", aspect_ratio="1:1"):
        """
        Generate an image from a text prompt.

        Args:
            prompt (str): The image description prompt.
            model (str, optional): Image model to use. Defaults to "DALL-E 3".
                Available: "DALL-E 3", "Stable Diffusion"
            style (str, optional): Image style. Defaults to "digital art".
            aspect_ratio (str, optional): Aspect ratio. Defaults to "1:1".
                Options: "1:1", "16:9", "9:16", "4:3", "3:4"

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
                  Results contains image URLs.
        """
        return self.action(action_id="generateImage", params={
            "prompt": prompt,
            "model": model,
            "model_style": style,
            "model_aspect_ratio": aspect_ratio
        })
    
    def text_to_audio(self, text, voice="alloy"):
        """
        Convert text to audio/speech.

        Args:
            text (str): The text to convert to speech.
            voice (str, optional): Voice to use. Defaults to "alloy".

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
                  Results contains the audio URL.
        """
        return self.action(action_id="outputAudio", params={
            "input_text": text,
            "voice": voice
        })
    
    def invoke_agent(self, agent_id, message, **kwargs):
        """
        Invoke another agent.ai agent.

        Args:
            agent_id (str): The ID of the agent to invoke.
            message (str): The message to send to the agent.
            **kwargs: Additional parameters for the agent.

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
        """
        params = {"agent_id": agent_id, "message": message, **kwargs}
        return self.action(action_id="invokeAgent", params=params)
    
    def rest_call(self, url, method="GET", headers=None, body=None):
        """
        Make a REST API call.

        Args:
            url (str): The URL to call.
            method (str, optional): HTTP method. Defaults to "GET".
            headers (dict, optional): Request headers.
            body (dict, optional): Request body for POST/PUT.

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
        """
        params = {"url": url, "method": method}
        if headers:
            params["headers"] = json.dumps(headers)
        if body:
            params["body"] = json.dumps(body)
        return self.action(action_id="restCall", params=params)
    
    def convert_file(self, file_url, target_format):
        """
        Convert a file to a different format.

        Args:
            file_url (str): URL of the file to convert.
            target_format (str): Target file format/extension (e.g., "pdf", "txt", "docx").

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
                  Results contains the converted file URL.
        """
        return self.action(action_id="convertFile", params={
            "input_file": file_url,
            "convert_to_extension": target_format
        })
    
    def get_convert_options(self, extension):
        """
        Get available conversion options for a file type.

        Args:
            extension (str): The source file extension (e.g., "pdf").

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
                  Results contains list of available target formats.
        """
        return self.action(action_id="convertFileOptions", params={"extension": extension})
    
    def store_variable(self, name, value):
        """
        Store a variable in the agent's database.

        Args:
            name (str): The variable name.
            value (str): The value to store.

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
        """
        return self.action(action_id="storeVariableToDatabase", params={
            "variable": name,
            "variable_value": value
        })
    
    def get_variable(self, name, retrieval_depth="most_recent_value"):
        """
        Retrieve a variable from the agent's database.

        Args:
            name (str): The variable name.
            retrieval_depth (str, optional): Retrieval mode. Defaults to "most_recent_value".
                Options: "most_recent_value", "all_values"

        Returns:
            dict: A dictionary containing 'status', 'error', 'results', and 'metadata'.
        """
        return self.action(action_id="getVariableFromDatabase", params={
            "variable": name,
            "variable_retrieval_depth": retrieval_depth
        })
