# -*- coding: utf-8 -*-

import os
from PIL import Image, ImageFont, ImageDraw

def Make(Input='raw_input',Codec='gb2312',Font='msyh.ttc',Size=32,Return='File'):
	if Input=='raw_input':
		RawText=raw_input()
	else:
		RawText=Input
	Text=RawText.decode(Codec)
	I=Image.new('RGBA',(90,45),(0,0,0,0))
	ID=ImageDraw.Draw(I)
	Font=ImageFont.truetype(os.path.join(Font),Size)
	ID.text((10,5),Text,font=Font,fill="#000000")
	if Return=='File':
		I.save(Text+'.png')
	else:
		return I

if __name__=='__main__':
	Make()