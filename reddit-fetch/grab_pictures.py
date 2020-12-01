import sys
import requests
import re
import os
import colorama
import argparse
from fake_useragent import UserAgent
w  # !/usr/bin/python3


def get_valid_filename(s):
    ''' strips out special characters and replaces spaces with underscores, len 200 to avoid file_name_too_long error '''
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'[^\w.]', '', s)[:200]


def erase_previous_line():
    # cursor up one line
    sys.stdout.write("\033[F")
    # clear to the end of the line
    sys.stdout.write("\033[K")


def get_pictures_from_subreddit(data, subreddit, location, nsfw):
    for i in range(len(data)):
        if data[i]['data']['over_18']:
            # if nsfw post and you only want sfw
            if nsfw == 'n':
                continue
        else:
            # if sfw post and you only want nsfw
            if nsfw == 'x':
                continue

        current_post = data[i]['data']
        image_url = current_post['url']
        if '.png' in image_url:
            extension = '.png'
        elif '.jpg' in image_url or '.jpeg' in image_url:
            extension = '.jpeg'
        elif 'imgur' in image_url:
            image_url += '.jpeg'
            extension = '.jpeg'
        else:
            continue

        erase_previous_line()
        print('downloading pictures from r/' + subreddit +
              '.. ' + str((i*100)//len(data)) + '%')

        # redirects = False prevents thumbnails denoting removed images from getting in
        image = requests.get(image_url, allow_redirects=False)
        if(image.status_code == 200):
            try:
                output_filehandle = open(
                    location + '/' + get_valid_filename(current_post['title']) + extension, mode='bx')
                output_filehandle.write(image.content)
            except:
                pass


def main():
    colorama.init()
    ua = UserAgent(
        fallback='Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11')
    parser = argparse.ArgumentParser(
        description='Fetch images from a subreddit (eg: python3 grab_pictures.py -s itookapicture CozyPlaces -n 100 -t all)')
    parser.add_argument('-s', '--subreddit', nargs='+', type=str, metavar='',
                        required=True, help='Exact name of the subreddits you want to grab pictures')
    parser.add_argument('-n', '--number', type=int, metavar='', default=100,
                        help='Optionally specify number of images to be downloaded (default=100, maximum=1000)')
    parser.add_argument('-t', '--top', type=str, metavar='', choices=['day', 'week', 'month', 'year', 'all'],
                        default='week', help='Optionally specify whether top posts of [day, week, month, year or all] (default=week)')
    parser.add_argument('-l', '--location', type=str, metavar='', default='',
                        help='Optionally specify the directory/location to be downloaded')
    parser.add_argument('-x', '--nsfw', type=str, metavar='', default='y',
                        help='Optionally specify the behavior for handling NSFW content. y=yes download, n=no skip nsfw, x=only download nsfw content')

    args = parser.parse_args()
    global after
    after = ''
    for i in range(0, args.number // 100):
        for j in range(len(args.subreddit)):
            print('starting download ' + str(i + 1))
            print('Connecting to r/' + args.subreddit[j])
            url = 'https://www.reddit.com/r/' + args.subreddit[j] + '/top/.json?sort=top&t=' + \
                args.top + '&limit=' + str(args.number)
            if after != '':
                url = url + '&after=' + after
            response = requests.get(url, headers={'User-agent': ua.random})
            after = response.json()['data']['after']
            if os.path.exists(args.location):
                location = os.path.join(args.location, args.subreddit[j])
            else:
                print(
                    'Given path does not exist, try without the location parameter to default to the current directory')
                exit()

            if not response.ok:
                print("Error check the name of the subreddit",
                      response.status_code)
                exit()

            if not os.path.exists(location):
                os.mkdir(location)
            # notify connected and downloading pictures from subreddit
            erase_previous_line()
            print('downloading pictures from r/' + args.subreddit[j] + '..')
            data = response.json()['data']['children']
            get_pictures_from_subreddit(
                data, args.subreddit[j], location, args.nsfw)
            erase_previous_line()
            print('Downloaded pictures from r/' + args.subreddit[j])


if __name__ == '__main__':
    main()
