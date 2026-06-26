# Jellyfin-Discord-Rich-Presence
# Jellyfin Discord Rich Presence (RPC)

A lightweight Python script that monitors your local Jellyfin server and updates your Discord profile with a dynamic "Rich Presence" status, complete with live progress bars and official movie/TV show posters fetched from TMDb.

## Prerequisites

Before running this script, you need to gather a few free API keys and IDs:
1. **Discord Client ID:** Create a new application in the [Discord Developer Portal](https://discord.com/developers/applications) and copy the Application ID. (The name of the app here is what will show up as "Playing `[Name]`" on your profile).
2. **Jellyfin API Key:** Generate one in your Jellyfin web interface under **Dashboard** -> **API Keys**.
3. **TMDb API Key:** Create a free account on [The Movie Database (TMDb)](https://www.themoviedb.org/), go to **Settings** -> **API**, and generate an API key. This is required to fetch the high-quality posters.

## Setup Instructions

**1. Clone the repository**
Download the code to your local machine:
```bash
git clone [https://github.com/AdhavBai/Jellyfin-Discord-Rich-Presence.git](https://github.com/AdhavBai/Jellyfin-Discord-Rich-Presence.git)
cd Jellyfin-Discord-Rich-Presence
```

**2. Install dependencies**
Ensure you have Python installed on your system, then install the required libraries:
```bash
pip install requests pypresence python-dotenv
```

**3. Configure your environment variables**
This project uses a `.env` file to keep your API keys completely secure.
* Locate the `.env.example` file in the project folder.
* Rename this file to exactly `.env`.
* Open the new `.env` file in any text editor and replace the placeholder text with your actual keys and server URL:
```text
DISCORD_CLIENT_ID=your_discord_client_id_here
JELLYFIN_URL=http://your_jellyfin_ip:8096
JELLYFIN_API_KEY=your_jellyfin_api_key_here
TMDB_API_KEY=your_tmdb_api_key_here
```

## Usage

Make sure the Discord desktop application is currently running on your machine, then launch the script from your terminal:

```bash
python JellyfinDiscord.py
```

