from datetime import datetime
import numpy as np
import os
import shutil

import instaloader
import cv2

ASPECTS = {8: (4, 2), 18: (6, 3), 32: (8, 4), 10: (2, 5), 21: (3, 7)}


class InstaCollage:
    def __init__(self, username) -> None:
        self.loader = instaloader.Instaloader()
        self.loader.interactive_login(username)
        print("Login Successful")

    def saveCollage(self):
        try:
            dir_pics = len(os.listdir("pics"))
            num_of_rows = ASPECTS[dir_pics][1]
        except (FileNotFoundError, KeyError) as e:
            print("Error: Run getPics()")
            return False

        open_pics = [cv2.imread(f"pics/{i+1}.jpg") for i in range(dir_pics)]
        arrays = []
        for x in open_pics:
            axis_len = min(x.shape[:2])
            row_start = x.shape[0] // 2 - axis_len // 2
            row_end = row_start + axis_len
            col_start = x.shape[1] // 2 - axis_len // 2
            col_end = col_start + axis_len
            arrays.append(x[row_start:row_end, col_start:col_end])

        arrays = [cv2.resize(x, (720, 720)) for x in arrays]
        rows = [np.hstack(x) for x in np.array_split(arrays, num_of_rows)]
        self.collage = np.vstack(rows)
        cv2.imwrite("collage.jpg", self.collage)
        print("\nSuccess: Collage Saved\n")
        return True

    def getPics(self, search, landscape=True):
        totals = [8, 18, 32] if landscape else [10, 21]
        self.prof = instaloader.Profile.from_username(self.loader.context, search)
        try:
            num_of_pics = max(x for x in totals if x <= self.prof.mediacount)
        except ValueError:
            print(f"Error: Minimum {min(totals)} pics for this orientation")
            return False

        if os.path.exists("pics"):
            shutil.rmtree("pics")
        os.mkdir("pics")
        print(f"Downloading {num_of_pics} pics...")
        for i, post in enumerate(self.prof.get_posts()):
            if i == num_of_pics:
                break
            self.loader.download_pic(f"pics/{str(i+1)}", post.url, datetime.now())
        return True

    def run(self, search, landscape=True):
        if self.getPics(search, landscape):
            return self.saveCollage()
        return False


if __name__ == "__main__":
    ig = InstaCollage("rhyswalexander")
    ig.run("openaidalle")
