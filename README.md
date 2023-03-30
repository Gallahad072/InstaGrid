# Instagram Collage

I wanted something that could make a collage of an instagram account's pictures so I could make a poster of [OpenAi's](https://openai.com/dall-e-2/) Dalle 2 [creations](https://www.instagram.com/openaidalle/).

This [program](main.py) will make a landscape or portrait collage of any Instagram account you can access to be used as a phone or computer wallpaper.

![pic couldn't load](examples/pcCollage.jpg)

## Instructions

Run the code in the terminal like this:

`python main.py <username> <search> <landscape>`

`<username>` is the username of the account you want to login with.
`<search>` is the name of the account you want to make the collage of.
`<landscape>` is True for landscape and False for portrait, defaults to True.

## Functions

`run(search, landscape=True)`

> Downloads images and creates collage.
>
> Pass in the username of account you want to retrieve the pictures from as 'search'.
> Pass in True to 'landscape' for landscape and False for Portrait.
> Returns True or False depending on success

`getPics(search, landscape=True)`

> Downloads images to pics folder.
>
> Pass in the username of account you want to retrieve the pictures from as 'search'.
> Pass in True to 'landscape' for landscape and False for Portrait.
> Returns True or False depending on success

`saveCollage()`

> Creates and saves collage of images in pics folder.
>
> Returns True or False depending on success
