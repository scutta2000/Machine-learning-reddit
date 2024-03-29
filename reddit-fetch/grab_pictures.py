import sys
import requests
import re
import os
import colorama
import argparse
from fake_useragent import UserAgent  # !/usr/bin/python3


def get_valid_filename(s):
    ''' strips out special characters and replaces spaces with underscores, len 200 to avoid file_name_too_long error '''
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'[^\w.]', '', s)[:200]


def erase_previous_line():
    # cursor up one line
    sys.stdout.write("\033[F")
    # clear to the end of the line
    sys.stdout.write("\033[K")


def get_pictures_from_subreddit(data, subreddit, location, nsfw, imageCount):
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

        # for some reasons it downloads this despite being a gif, TODO: find root cause
        if current_post['title'] == " Lowland gorilla at Miami zoo uses sign language to tell someone that he's not allowed to be fed by visitors.":
            continue

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
            fileDest = location + '/' + \
                f'{imageCount:03}' + "_" + \
                get_valid_filename(current_post['title']) + extension
            with open(fileDest, mode='bx') as output_filehandle:
                output_filehandle.write(image.content)
            print("saving " + fileDest)
            with open("scores.csv", "a") as f:
                f.write(str(current_post['score'])+",\n")

            imageCount += 1
    return imageCount


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
    imageCount = 0
    for i in range(args.number // 100):
        for j in range(len(args.subreddit)):
            print('Connecting to r/' + args.subreddit[j])
            url = 'https://www.reddit.com/r/' + args.subreddit[j] + '/top/.json?sort=top&t=' + \
                args.top + '&limit=' + str(args.number)
            print(url)
            if after != '':
                url = url + '&after=' + after
            response = requests.get(url, headers={'User-agent': ua.random})
            after = response.json()['data']['after']
            if os.path.exists(args.location) or args.location == "":
                location = os.path.join(args.location, args.subreddit[j])
            else:
                print(
                    'Given path ('+args.location+')does not exist, try without the location parameter to default to the current directory')
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
            imageCount = get_pictures_from_subreddit(
                data, args.subreddit[j], location, args.nsfw, imageCount)
            erase_previous_line()
            print('Downloaded pictures from r/' + args.subreddit[j])


if __name__ == '__main__':
    main()
