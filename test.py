import gutenbergpy.textget
from gutenbergpy.gutenbergcache import GutenbergCache
from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings
from pathlib import Path
import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

logging.getLogger().info("At least in here")
directory = Path("temp")
directory.mkdir(parents=True, exist_ok=True)
GutenbergCacheSettings.set(
    CacheUnpackDir="temp/unpack",  # This needs to be a separate directory, not totally sure why.
    CacheFilename="temp/gutenberg.db",
    CacheArchiveName="temp/rdf-files.tar.bz2",
)
GutenbergCacheSettings.log()

# create cache from scratchfrom scratch
GutenbergCache.create(
    refresh=True, download=True, unpack=True, parse=True, cache=True, deleteTemp=True
)
# get the default cache (SQLite)
cache = GutenbergCache.get_cache()
# For the query function you can use the following fields: languages authors types titles subjects publishers bookshelves
print(
    cache.query(
        downloadtype=["application/plain", "text/plain", "text/html; charset=utf-8"]
    )
)
# Print stripped text
print(gutenbergpy.textget.strip_headers(gutenbergpy.textget.get_text_by_id(1000))[:100])
