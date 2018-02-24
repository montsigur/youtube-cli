#!/usr/bin/python3
from requests import request
from optparse import OptionParser
from textwrap import fill, indent
from os import system

API_KEY_FILE_PATH = '/etc/youtube/key.txt'
REQUEST_TEMPLATE = 'https://www.googleapis.com/youtube/v3/search?part=snippet&{}&key={}'
VIDEO_URL_TEMPLATE = 'https://www.youtube.com/watch?v={}'
DEFAULT_PLAYER_COMMAND = 'mplayer -quiet -cache {} -'

def print_results(results):
    """Print search results generated by search_by_keyword function call

The results will be printed as follows:

    [Video number] [Title of the video]
    [Description of the video]
    [~ChannelName]
    [Video URL]

Args:
    results (list): list of results, output of search_by_keyword function call
    """
    number = 1 # video number
    print()
    
    for item in results:

        video_id = item['id']['videoId']
            
        video_url = VIDEO_URL_TEMPLATE.format(video_id)
        
        print(number, fill(item['snippet']['title'], 64, break_long_words=False))
        print(indent(fill(item['snippet']['description'], 64, break_long_words=False), '  ' + number // 10 * ' '))
        print(indent(fill('~' + item['snippet']['channelTitle'], 64, break_long_words=False), '  ' + number // 10 * ' '))
        print(indent(fill(video_url, 64, break_long_words=False), '  ' + number // 10 * ' '), '\n')
        
        number += 1

def search_by_keyword(query, params, api_key):
    """Search for videos by keyword(s).

Args:
    query (string): keyword(s) passed to youtube search engine
    params (dict): python dictionary consisting of pairs {parameter_name: value,...},
                   which are optional search parameters. For full list of optional
                   search parameters see
                   https://developers.google.com/youtube/v3/docs/search/list
    api_key (string): youtube API key, generated and bounded with a google account

Returns:
    list: list of search results. It is the 'items' field of the original youtube
          JSON response with the search results.
    
    """
    params = 'q=' + query + '&' + '&'.join([param_key + '=' + str(params[param_key])\
                                            for param_key in params])\
                                                if params else 'q=' + query
    
    resp = request('GET', REQUEST_TEMPLATE.format(params, api_key))

    resp_json = resp.json()

    return resp_json['items']

def play_video(video_id, command):
"""Play the chosen video with a video player of your choice. Specify a command
the video will be played with in the "command" parameter. The player must read
data from the standard input.

Args:
    video_id (string): youtube video id, obtained from a list of search
                       results, generated by search_by_keyword function call
    command (string): consists of a video player program call and its options,
                      that will enable it to read video data from stdin.
                      Example: "mplayer -cache 1024 -"
"""
    video_url = VIDEO_URL_TEMPLATE.format(video_id)

    # system call
    # downloaded video data is being piped to the video player
    # '-o -' means that youtube-dl will output downloaded video to stdout
    system('youtube-dl {} -o - | {}'.format(video_url, command))

def filter_results(results):
    """
    Filter search results generated by search_by_keyword function call.

    Filtered results are those which don't have 'videoId' field.

    Args:
        results (list): list of results, output of search_by_keyword function call

    Returns:
        list: list of filtered results
    """

    # filter function; get rid of results without "videoId" field
    function = lambda item: 'videoId' in item['id'].keys() 
                                                           
    return list(filter(function, results)) # convert filter object to a list
                                           # and return filtered results


def get_video_id_by_number(number, results):
"""
Get video id by its number from the list of search results generated by search_by_keyword
function call.

Videos are numbered from 1 to maxResults (optional search parameter,
set by default to 5, see https://developers.google.com/youtube/v3/docs/search/list)
as in results list.

Args:
    number (int): number of video whose id is requested
    results (list): list of search results generated by search_by_keyword function call

Returns:
    string: youtube video id
"""

    return results[number-1]['id']['videoId']
                                    
if __name__ == "__main__":
    
    parser = OptionParser(usage='Usage: %prog [-q QUERY] [-l LIMIT_RESULTS]'
                          + ' [-c CACHE] [-L] [-n RESULT_NUMBER]')
    parser.add_option('-l', '--limit', dest='limit_results',
                      type=int, default=5, help='Limit number of search results.'
                      + ' Default value of LIMIT_RESULTS (positive integer) is 5.')
    parser.add_option('-q', '--query', dest='query',
                      default='', type=str, help='Query of the search. By'
                      + ' default QUERY is an empty string.')
    parser.add_option('-L', '--feeling-lucky', dest='feeling_lucky',
                      default=False, action='store_true',
                      help='Play the first video from the list of search results.')
    parser.add_option('-n', '--result-number', dest='result_number',
                      default=-1, type=int,
                      help='Choose a video to play from the list of search'
                      + ' results by its number and play it. Default value of'
                      + ' RESULT_NUMBER is -1 (integer, if not positive, then'
                      + ' don\'t play any).')
    parser.add_option('-c', '--cache', dest='cache',
                      default=10240, type=int,
                      help='Set cache size for the video player to temporarily'
                      + ' store the most recent part of the streamed video.'
                      + ' Default value of CACHE is 10240 (positive integer,'
                      + ' size in kB).')
    
    opts, args = parser.parse_args()

    with open(API_KEY_FILE_PATH) as api_key_file:

        api_key = api_key_file.read()
    
    params = {'maxResults': opts.limit_results} # dictionary for search parameters
                                                # see 'Optional parameters' section on
                                                # https://developers.google.com/youtube/v3/docs/search/list
                                                # 'q' parameter is added by default

    results = search_by_keyword(opts.query, params, api_key)

    results = filter_results(results)
    
    if not opts.feeling_lucky and opts.result_number < 1:

        print_results(results)

    elif opts.result_number > opts.limit_results:

        print('Video number out of range')
        
    else:

        video_number = 1 if opts.feeling_lucky else opts.result_number
                       
        video_id = get_video_id_by_number(video_number, results)

        command = DEFAULT_PLAYER_COMMAND.format(opts.cache)
        
        play_video(video_id, command)
