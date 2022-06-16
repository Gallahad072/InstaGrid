from datetime import datetime
import numpy as np
import os
import shutil

import instaloader
import cv2


class InstaGrid:
    def __init__(self, username=False, search=False, pcOrPhone=True) -> None:
        self.L = instaloader.Instaloader()
        self.username = username if username else input("Personal Username: ")
        self.L.interactive_login(username)
        search = search if search else input("Username of account to search: ")
        self.prof = instaloader.Profile.from_username(self.L.context, search)
        self.minPics = 8 if pcOrPhone else 10
        self.totals = [8, 18, 32] if pcOrPhone else [10, 21]

    def saveCollage(self):
        aspects = {8: (4, 2), 18: (6, 3), 32: (8, 4), 10: (2, 5), 21: (3, 7)}
        numOfRows = aspects[self.numOfPics][1]
        openImgs = [cv2.imread(f"pics/{i+1}.jpg") for i in range(self.numOfPics)]
        arrays = [cv2.resize(x, (720, 720)) for x in openImgs]
        rows = [np.hstack(x) for x in np.array_split(arrays, numOfRows)]
        self.collage = np.vstack(rows)
        shutil.rmtree("pics")
        cv2.imwrite("collage.jpg", self.collage)

    def showCollage(self):
        cv2.imshow("InstaGrid", self.collage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def getPics(self):
        try:
            numOfPics = max(x for x in self.totals if x <= self.prof.mediacount)
        except ValueError:
            print(f"Error: Minimum {self.minPics} pics for this wallpaper format")
            return False

        os.mkdir("pics")
        for i, post in enumerate(self.prof.get_posts()):
            if i == numOfPics:
                break
            self.L.download_pic(f"pics/{str(i+1)}", post.url, datetime.now())

        self.numOfPics = numOfPics

    def main(self):
        self.getPics()
        if self.numOfPics:
            self.saveCollage()


if __name__ == "__main__":
    ig = InstaGrid("rhys.zip", "openaidalle")
    ig.main()
