from pytube import YouTube
import argparse

def access_youtube_link():

    return 

def youtube_ext(url):
    #import the package
    my_video = YouTube(url)

    print("*********************Video Title************************")
    #get Video Title
    print(my_video.title)

    print("********************Tumbnail Image***********************")
    #get Thumbnail Image
    print(my_video.thumbnail_url)

    print("********************Download video*************************")
    #get all the stream resolution for the 
    for stream in my_video.streams:
        print(stream)

    #set stream resolution
    my_video = my_video.streams.get_highest_resolution()

    #Download video
    my_video.download("")


def main():
    parser = argparse.ArgumentParser("parameters to receive Youtube videos.")
    parser.add_argument('-url', type=str, default=None)

    args = parser.parse_args()
    youtube_ext(args.url)

if __name__ == '__main__':
    main()