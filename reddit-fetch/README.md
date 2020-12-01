# reddit-fetch

## grab-pictures

A python program to fetch the pictures of a given subreddit, wrote it when I was looking for some wallpapers to download. It grabs the pictures and puts them in a folder under the name of the supplied subreddit.
You can find the related [medium article here](https://medium.com/@naveenkumarspa/using-python-for-your-desktop-wallpaper-collection-focused-on-beginners-a66451d25660).

### Run

  - Clone the repository: `git clone https://github.com/nobodyme/reddit-fetch.git` or download
  - cd into the directory: `cd reddit-fetch`
  - pip3 install -r requirements.txt
  - Run the script with: `python3 grab_pictures.py -s *name-of-the-subreddits* -n *number-of-photos(optional)* -t *top posts of [day, week, month, year, all](optional)* -loc *directory-path(optional, defauts to current one)*`</br>
  eg: `python3 grab_pictures.py -s itookapicture CozyPlaces -n 100 -t all`
  - Check for help with `python3 grab_pictures.py -h`
