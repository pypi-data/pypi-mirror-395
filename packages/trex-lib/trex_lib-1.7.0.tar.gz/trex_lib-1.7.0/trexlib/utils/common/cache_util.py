'''
Created on 15 Apr 2025

@author: jacklok
'''
import os
from flask_caching import Cache
import logging

AGE_TIME_FIVE_MINUTE    = 60*5
AGE_TIME_QUATER_HOUR    = AGE_TIME_FIVE_MINUTE * 3
AGE_TIME_HALF_HOUR      = AGE_TIME_QUATER_HOUR * 2
AGE_TIME_ONE_HOUR       = AGE_TIME_HALF_HOUR * 2
AGE_TIME_TWO_HOUR       = AGE_TIME_ONE_HOUR * 2
AGE_TIME_SIX_HOUR       = AGE_TIME_ONE_HOUR * 6
AGE_TIME_ONE_DAY        = AGE_TIME_ONE_HOUR * 24


def isCacheEnabled():
    cache_enabled=os.environ.get("CACHE_ENABLED")
    if cache_enabled is not None:
        if isinstance(cache_enabled, bool):
            return cache_enabled
        elif isinstance(cache_enabled, str):
            return cache_enabled.lower() =='true'
    return False

cache = None

if isCacheEnabled():
    cache = Cache()

logger = logging.getLogger('util')

def setCache(cache_key, value, timeout=300):
    logger.debug('set to cache with %s=%s', cache_key, value)
    if cache is not None:
        cache.set(cache_key, value, timeout=timeout)
    
def getFromCache(cache_key):
    if cache is not None:
        value =  cache.get(cache_key)
        logger.debug('get from cache with %s=%s', cache_key, value)
        return value

def deleteFromCache(cache_key):
    logger.debug('delete from cache with %s', cache_key)
    if cache is not None:
        cache.delete(cache_key)
        
        