from __future__ import print_function
from os import path
import time
from gutenbergpy.utils import Utils

from gutenbergpy.gutenbergcachesettings import GutenbergCacheSettings
from gutenbergpy.parse.rdfparser import RdfParser
from gutenbergpy.caches.sqlitecache import SQLiteCache
from gutenbergpy.caches.mongodbcache import MongodbCache
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

##
# Cache types
# noinspection PyClassHasNoInit
class GutenbergCacheTypes:
    CACHE_TYPE_SQLITE = 0
    CACHE_TYPE_MONGODB = 1


##
# The main class (only this should be used to interface the cache)
class GutenbergCache:
    ##
    # Get the cache by type
    @staticmethod
    def get_cache(type=GutenbergCacheTypes.CACHE_TYPE_SQLITE):
        if type == GutenbergCacheTypes.CACHE_TYPE_SQLITE:
            return SQLiteCache()
        elif type == GutenbergCacheTypes.CACHE_TYPE_MONGODB:
            return MongodbCache()
        logger.info("CACHE TYPE UNKNOWN")
        return None

    ##
    # Create the cache
    @staticmethod
    def create(
        cache_type=GutenbergCacheTypes.CACHE_TYPE_SQLITE,
        refresh: bool = True,
        download: bool = True,
        unpack: bool = True,
        parse: bool = True,
        cache: bool = True,
        deleteTemp: bool = True,
    ):
        logger.info(f"Using cache parameters {GutenbergCacheSettings}")
        if (
            path.isfile(GutenbergCacheSettings.CACHE_FILENAME)
            and refresh
            and cache_type == GutenbergCacheTypes.CACHE_TYPE_SQLITE
        ):
            logger.info("Cache already exists")
            return

        if refresh:
            logger.info("Deleting old files")
            Utils.delete_tmp_files(True)

        if download:
            Utils.download_file()

        if unpack:
            Utils.unpack_tarbz2()

        if parse:
            t0 = time.time()
            parser = RdfParser()
            result = parser.do()
            logger.info("RDF PARSING took " + str(time.time() - t0))

            if cache:
                t0 = time.time()
                cache = GutenbergCache.get_cache(cache_type)
                cache.create_cache(result)
                logger.info("sql took %f" % (time.time() - t0))

        if deleteTemp:
            logger.info("Deleting temporary files")
            Utils.delete_tmp_files()

        logger.info("Done")

    ##
    # Method to check if the cache exists
    @staticmethod
    def exists():
        return path.isfile(GutenbergCacheSettings.CACHE_FILENAME)
