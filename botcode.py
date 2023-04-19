import requests
import time
import os

# Set up Telegram bot
telegram_token = os.environ['6019237239:AAGm53nnczXiqtiIO5RBXeOzF3hhdn5yHZE']  # Replace with your own Telegram bot token
telegram_chat_id = os.environ['6052623127']  # Replace with your own Telegram chat ID

# Set up movie API
movie_api_key = os.environ['c7a04f211e318d982307efac90dbecf3']  # Replace with your own movie API key
movie_api_url = f'https://api.themoviedb.org/3/movie/upcoming?api_key=c7a04f211e318d982307efac90dbecf3'

# Set up notification interval
notification_interval = 1800  # Interval in seconds (1 hour)

# Set up initial notification time
last_notification_time = time.time() - notification_interval

# Send message function
def send_message(message):
    requests.post(f'https://api.telegram.org/bot{telegram_token}/sendMessage', data={
        'chat_id': telegram_chat_id,
        'text': message
    })

# Main loop
while True:
    # Check if it's time to send a notification
    current_time = time.time()
    if current_time - last_notification_time >= notification_interval:
        # Get upcoming movie data from API
        response = requests.get(movie_api_url)
        movie_data = response.json()
        
        # Filter movie data to only show new releases
        new_movies = []
        for movie in movie_data['results']:
            if movie['release_date'] == time.strftime('%Y-%m-%d'):
                new_movies.append(movie)
        
        # Send notification if there are new releases
        if new_movies:
            message = 'New movie trailers have been released!\n\n'
            for movie in new_movies:
                message += f'{movie["title"]} - {movie["overview"]}\n\n'
            send_message(message)
            
            # Update last notification time
            last_notification_time = current_time
    
    # Wait for a minute before checking again
    time.sleep(60)