from datetime import datetime
import numpy as np
import os
from os import path
import shutil

import instaloader
import cv2


class InstaGrid:
    def __init__(self, username) -> None:
        self.L = instaloader.Instaloader()
        self.L.interactive_login(username)
        print("Login Successful")

    def saveCollage(self):
        aspects = {8: (4, 2), 18: (6, 3), 32: (8, 4), 10: (2, 5), 21: (3, 7)}

        try:
            picsInDir = len(os.listdir("pics"))
            numOfRows = aspects[picsInDir][1]
        except (FileNotFoundError, KeyError) as e:
            print("Error: Run getPics()")
            return False

        openImgs = [cv2.imread(f"pics/{i+1}.jpg") for i in range(picsInDir)]

        arrays = []
        for x in openImgs:
            axisLen = min(x.shape[:2])
            rowStart = x.shape[0] // 2 - axisLen // 2
            rowEnd = rowStart + axisLen
            colStart = x.shape[1] // 2 - axisLen // 2
            colEnd = colStart + axisLen
            arrays.append(x[rowStart:rowEnd, colStart:colEnd])

        arrays = [cv2.resize(x, (720, 720)) for x in arrays]
        rows = [np.hstack(x) for x in np.array_split(arrays, numOfRows)]
        self.collage = np.vstack(rows)
        cv2.imwrite("collage.jpg", self.collage)
        print("\nSuccess: Collage Saved\n")
        return True

    def getPics(self, search, landscape=True):
        totals = [8, 18, 32] if landscape else [10, 21]
        self.prof = instaloader.Profile.from_username(self.L.context, search)
        try:
            numOfPics = max(x for x in totals if x <= self.prof.mediacount)
        except ValueError:
            print(f"Error: Minimum {min(totals)} pics for this orientation")
            return False

        if path.exists("pics"):
            shutil.rmtree("pics")
        os.mkdir("pics")
        print(f"Downloading {numOfPics} pics...")
        for i, post in enumerate(self.prof.get_posts()):
            if i == numOfPics:
                break
            self.L.download_pic(f"pics/{str(i+1)}", post.url, datetime.now())

        return True

    def run(self, search, landscape=True):
        if self.getPics(search, landscape):
            return self.saveCollage()
        return False


if __name__ == "__main__":
    ig = InstaGrid("rhys.zip")
    ig.run("openaidalle")
