import time
import requests
import os
from dotenv import load_dotenv
from pypresence import Presence
load_dotenv()

######################################################################################################
DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
JELLYFIN_LOCAL_URL = os.getenv("JELLYFIN_URL")
JELLYFIN_API_KEY = os.getenv("JELLYFIN_API_KEY")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
#######################################################################################################

def get_active_session():
    """Fetches the active playback session from your local Jellyfin."""
    headers = {"X-Emby-Token": JELLYFIN_API_KEY}
    url = f"{JELLYFIN_LOCAL_URL}/Sessions"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        sessions = response.json()
        for session in sessions:
            if "NowPlayingItem" in session:
                return session
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Jellyfin: {e}")
        return None

def get_tmdb_poster(media_type, search_title, tmdb_id=None):
    """Fetches the poster URL from TMDb."""
    if tmdb_id:
        url = f"https://api.themoviedb.org/3/{media_type}/{tmdb_id}?api_key={TMDB_API_KEY}"
        try:
            res = requests.get(url).json()
            if res.get("poster_path"):
                return f"https://image.tmdb.org/t/p/w500{res['poster_path']}"
        except Exception:
            pass

    search_url = f"https://api.themoviedb.org/3/search/{media_type}?api_key={TMDB_API_KEY}&query={search_title}"
    try:
        res = requests.get(search_url).json()
        results = res.get("results", [])
        if results and results[0].get("poster_path"):
            return f"https://image.tmdb.org/t/p/w500{results[0]['poster_path']}"
    except Exception as e:
        print(f"TMDb Search failed: {e}")

    return "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg" 

def format_time(seconds):
    """Helper to format seconds into HH:MM:SS for the paused status text."""
    return time.strftime('%H:%M:%S', time.gmtime(seconds))

def main():
    rpc = Presence(DISCORD_CLIENT_ID)
    rpc.connect()
    print("Connected to Discord RPC! Monitoring playback and tracking time progress...")

    last_item_id = None
    cached_poster_url = None

    while True:
        session = get_active_session()

        if session and "NowPlayingItem" in session:
            item = session["NowPlayingItem"]
            item_type = item.get("Type")
            item_id = item.get("Id")
            
            
            if item_type == "Movie":
                title = item.get("Name")
                state = f"Released: {item.get('ProductionYear', 'Unknown')}"
                media_type = "movie"
                search_title = title
                tmdb_id = item.get("ProviderIds", {}).get("Tmdb")
            elif item_type == "Episode":
                show_name = item.get("SeriesName", "Unknown Show")
                season = item.get("ParentIndexNumber", 0)
                episode = item.get("IndexNumber", 0)
                title = f"{show_name} (S{season:02d}E{episode:02d})"
                state = item.get("Name", "Unknown Episode")
                media_type = "tv"
                search_title = show_name 
                tmdb_id = None
            else:
                title = item.get("Name")
                state = "Watching Media"
                media_type = "movie"
                search_title = title
                tmdb_id = None

            
            if item_id != last_item_id:
                cached_poster_url = get_tmdb_poster(media_type, search_title, tmdb_id)
                last_item_id = item_id

            
            play_state = session.get("PlayState", {})
            position_ticks = play_state.get("PositionTicks", 0)
            runtime_ticks = item.get("RunTimeTicks", 0)
            
            position_secs = int(position_ticks / 10000000)
            runtime_secs = int(runtime_ticks / 10000000)

            now = int(time.time())
            
            
            rpc_kwargs = {
                "details": title,
                "state": state,
                "large_image": cached_poster_url,
                "large_text": title
            }

           
            if play_state.get("IsPaused"):
                
                rpc_kwargs["state"] = f"⏸️ [PAUSED] ({format_time(position_secs)} / {format_time(runtime_secs)})"
            else:
                
                start_timestamp = now - position_secs
                end_timestamp = start_timestamp + runtime_secs
                
                rpc_kwargs["start"] = start_timestamp
                rpc_kwargs["end"] = end_timestamp

            
            try:
                rpc.update(**rpc_kwargs)
                print(f"Updated RPC: {title} ({position_secs}s / {runtime_secs}s)")
            except Exception as e:
                print(f"Failed to update Discord: {e}")
                
        else:
            rpc.clear()
            print("Nothing playing. Cleared RPC.")
            last_item_id = None

        time.sleep(10)

if __name__ == "__main__":
    main()