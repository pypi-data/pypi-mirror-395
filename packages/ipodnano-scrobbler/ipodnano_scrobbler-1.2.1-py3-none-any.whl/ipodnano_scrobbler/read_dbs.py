import sqlite3
import polars as pl
from datetime import datetime, timedelta, UTC
from ipodnano_scrobbler.scrobble import login, scrobble
from trainerlog import get_logger
LOGGER = get_logger("ipod-nano-scrobbler")
import time
from pathlib import Path
import pandas as pd
import tqdm

def mac_absolute_time_to_datetime(mac_timestamp):
    mac_epoch = datetime(2001, 1, 1, 0, 0, 0, tzinfo=UTC)
    return (mac_epoch + timedelta(seconds=mac_timestamp)).replace(tzinfo=None)

def one_month_ago(days=30):
    now = datetime.now(tz=UTC)
    return (now - timedelta(days=days)).replace(tzinfo=None)

def get_play_counts(ipod_path, days=30):
    dynamic_itdb = (Path(ipod_path) / "Dynamic.itdb").absolute()
    library_itdb = (Path(ipod_path) / "Library.itdb").absolute()

    conn_dynamic = sqlite3.connect(dynamic_itdb, cached_statements=2000)
    conn_library = sqlite3.connect(library_itdb, cached_statements=2000)
    dynamic_info = pd.read_sql_query("SELECT * FROM item_stats", conn_dynamic)
    dynamic_info = pl.from_pandas(dynamic_info)
    track_properties = pd.read_sql_query("SELECT pid, title, album, artist FROM item", conn_library)
    track_properties = pl.from_pandas(track_properties)
    conn_library.close()
    conn_dynamic.close()

    dynamic_info = dynamic_info.with_columns(
                        pl.col("date_played").map_elements(
                            lambda timestamp: mac_absolute_time_to_datetime(timestamp),
                            return_dtype=pl.Datetime
                        )
                    )
    track_properties = track_properties.select("pid", "title", "album", "artist")
    dynamic_info = dynamic_info.rename({"item_pid": "pid"})

    play_counts = dynamic_info.join(track_properties, on="pid")
    play_counts = play_counts.select("pid", "play_count_user", "play_count_recent", "date_played", "title", "album", "artist")
    play_counts = play_counts.filter(pl.col("play_count_recent") >= 1)
    return play_counts.sort("date_played")

def reset_recent_plays(ipod_path):
    LOGGER.info(f"Set recent play counts to 0")
    dynamic_itdb = (Path(ipod_path) / "Dynamic.itdb").absolute()
    conn_dynamic = sqlite3.connect(dynamic_itdb)
    cursor = conn_dynamic.cursor()
    cursor.execute("UPDATE item_stats SET play_count_recent = 0;")
    conn_dynamic.commit()
    conn_dynamic.close()

def read_timestamp(itdb_path):
    path = Path(itdb_path).parent / "SCROBBLER_TIMESTAMP.txt"
    if path.exists():
        timestamp_str = path.open().read()
        return datetime.fromtimestamp(int(float(timestamp_str)), tz=UTC).replace(tzinfo=None)

def write_timestamp(itdb_path):
    path = Path(itdb_path).parent / "SCROBBLER_TIMESTAMP.txt"
    with path.open("w") as f:
        now = datetime.now(tz=UTC)
        timestamp_str = now.timestamp()
        f.write(f"{timestamp_str}")

def get_timezone():
    return datetime(2025, 2,2,22,3,0,0).astimezone().tzinfo

def get_tz_delta():
    return get_timezone().utcoffset(datetime.now())
    
def main():
    import argparse
    parser = argparse.ArgumentParser(prog='ipodnano_scrobble')
    parser.add_argument('--ipod_path', required=True, type=str, help="Path to the iPod's 'iTunes Library.itlp' folder")
    parser.add_argument('--skipcount', default=30, type=int, help="Skip songs with this or more 'recent plays'")
    parser.add_argument('--days', default=30, type=int, help='Skip playcounts older than this')
    args = parser.parse_args()
    LOGGER.debug(f"Args: {args}")
    LOGGER.info(f"Setup last.fm login...")
    SESSION_KEY, LAST_FM_API, LAST_FM_API_SECRET = login()
    LOGGER.info("Login successful!")
    LOGGER.info(f"Get iTunes database from {args.ipod_path}...")
    play_counts = get_play_counts(args.ipod_path, days=args.days)

    skipped_songs = len(play_counts) - len(play_counts.filter(pl.col("date_played") >= one_month_ago(args.days)))
    if skipped_songs >= 1:
        LOGGER.warning(f"Skipping {skipped_songs} plays that are over {args.days} days old. Can be adjusted with the --days argument.")
        scrobble_anyway = input("Continue (y/N)?")
        if scrobble_anyway.lower() != "y":
            LOGGER.error("Do not scrobble anything. Exiting...")
            return

    play_counts = play_counts.filter(pl.col("date_played") >= one_month_ago(args.days))

    play_counts = play_counts.filter(pl.col("play_count_recent") < args.skipcount)
    recent_counts_total = play_counts.select("play_count_recent").sum().item()
    if recent_counts_total > len(play_counts):
        LOGGER.warning("Some tracks were played multiple times recently. Some of the play times need to be imputed.")
    
    tz = get_timezone()
    ts = read_timestamp(args.ipod_path)
    LOGGER.info(f"Last scrobbled on {ts} (UTC), (timezone : {tz})")
    if ts is not None:
        ts = ts - timedelta(hours=0)
        play_counts_old = play_counts.filter(pl.col("date_played") < ts)
        if len(play_counts_old) >= 1:
            old_row = play_counts_old.to_dicts()[0]
            LOGGER.warning(f"Song {old_row.get('title')} scrobbled on {old_row.get('date_played')}")
            LOGGER.error("Some of the 'recent plays' are older than most recent scrobbling timestamp. This is a sign of corrupt play data, maybe due to refreshing the database index.")
            scrobble_anyway = input("Continue and skip corrupt playcounts (y/N)?")
            if scrobble_anyway.lower() == "y":
                play_counts = play_counts.filter(pl.col("date_played") >= ts)
                LOGGER.warning("Some of the new playcounts might be duplicated due to data corruption.")
                only_once = input("Only scrobble once per track (Y/n)?")
                if only_once.lower() != "n":
                    play_counts = play_counts.with_columns(pl.min_horizontal(pl.col("play_count_recent"), 1))
            else:
                return None#exit()
    assert len(play_counts.filter(pl.col("date_played") < ts)) == 0
    recent_counts_total = play_counts.select("play_count_recent").sum().item()
    LOGGER.info(f"Scrobbling {recent_counts_total} recent plays of {len(play_counts)} tracks...")
    pbar = tqdm.tqdm(play_counts.rows(named=True), desc="Songtitle")
    for track in pbar:
        title, artist = track["title"], track["artist"]
        last_played = track["date_played"]
        recent_playcount = track["play_count_recent"]
        LOGGER.debug(f"Scrobble {title}, {artist}, {recent_playcount} times")
        for ix in range(recent_playcount):
            imputed_date = last_played-timedelta(days=ix)
            if imputed_date >= one_month_ago(days=args.days):
                imputed_date = imputed_date + get_tz_delta()
                LOGGER.debug(f"Scrobble {title}, {artist}, {imputed_date}")
                title_artist = f"[{ix+1}] {title} – {artist}".ljust(30)[:30]
                imputed_date_str = str(imputed_date)[:-3]
                pbar.set_description(f"{imputed_date_str} {title_artist}")
                date_timestamp = str(int(imputed_date.replace(tzinfo=tz).timestamp()))

                response = scrobble(title, artist, SESSION_KEY, LAST_FM_API, LAST_FM_API_SECRET, timestamp=date_timestamp)
                if response == "hasherror":
                    LOGGER.error(f"Hashing of track '{title}' by '{artist}' unsuccesful, not scrobbled!")
                elif response.status_code != 200:
                    LOGGER.error(f"Scrobbling status not ok {response.status_code}!")
                time.sleep(0.01)
            else:
                LOGGER.debug(f"Skip since imputed date {imputed_date} is further away than {args.days} days")

        time.sleep(0.1)

    reset_recent_plays(args.ipod_path)
    write_timestamp(args.ipod_path)


if __name__ == '__main__':
    main()
