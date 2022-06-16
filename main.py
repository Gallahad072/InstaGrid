from datetime import datetime
import numpy as np
import os
import shutil

import instaloader
import cv2


def makeCollage(numOfPics):
    aspects = {8: (4, 2), 18: (6, 3), 32: (8, 4), 10: (2, 5), 21: (3, 7)}
    numOfRows = aspects[numOfPics][1]
    openImgs = [cv2.imread(f"pics/{i+1}.jpg") for i in range(numOfPics)]
    arrays = [cv2.resize(x, (720, 720)) for x in openImgs]
    rows = [np.hstack(x) for x in np.array_split(arrays, numOfRows)]
    collage = np.vstack(rows)
    shutil.rmtree("pics")
    cv2.imwrite("collage.jpg", collage)


def getPics(username=False, search=False, pcOrPhone=True):
    L = instaloader.Instaloader()
    username = username if username else input("Personal Username: ")
    L.interactive_login(username)
    search = search if search else input("Username of account to search: ")

    prof = instaloader.Profile.from_username(L.context, search)
    minPics = 8 if pcOrPhone else 10
    totals = [8, 18, 32] if pcOrPhone else [10, 21]

    try:
        numOfPics = max(x for x in totals if x <= prof.mediacount)
    except ValueError:
        print(f"Error: Minimum {minPics} pics for this wallpaper format")
        return False

    os.mkdir("pics")
    for i, post in enumerate(prof.get_posts()):
        if i == numOfPics:
            break
        L.download_pic(f"pics/{str(i+1)}", post.url, datetime.now())

    makeCollage(numOfPics)


def main():
    makeCollage(getPics())


if __name__ == "__main__":
    getPics("rhys.zip", "openaidalle")
