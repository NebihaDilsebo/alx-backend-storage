import requests
import redis

def get_page(url: str) -> str:
    # Initialize a Redis client
    redis_client = redis.Redis()

    # Check if the URL access count is stored in the cache
    count_key = f"count:{url}"
    access_count = redis_client.get(count_key)

    if access_count is not None:
        access_count = int(access_count)
    else:
        access_count = 0

    # If the URL was accessed fewer than 10 times, fetch the HTML content
    if access_count < 10:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Cache the HTML content with a 10-second expiration
                redis_client.setex(url, 10, response.text)

                # Update the access count and store it in the cache
                access_count += 1
                redis_client.set(count_key, access_count)

                return response.text
            else:
                return f"Failed to retrieve the page at {url}. Status code: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"
    else:
        return "Access limit reached for this URL."

if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/https://example.com"  # Replace with your desired URL
    html_content = get_page(url)
    print(html_content)

