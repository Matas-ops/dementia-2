# Discord bot

Python version used: 3.13

Packages are listed in requirements.txt

BOT_TOKEN, GIF_CHANNEL_ID should be stored in .env file at root folder

GIF_CHANNEL_ID is where the bot can grab all available gifs and display one of them randomly

Project contains server to satisfy google cloud

I will need to fix requirements.txt

## Example for running docker

docker build -t dementia2:dev -f Dockerfile.dev .

docker run -d -p 8080:8080 --name dementia2 dementia2:dev
