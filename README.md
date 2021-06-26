# Smeeta_Tracker

Description:

	Reads smeeta charm buffs from Warframe while in mission and keeps track
	of multiple charm buffs stacking at once.

	Bounding area of the buffs was manually calculated to my screen. Warframe
	hud is not straight so I crop, rotate, and then crop again to get the line
	of buff numbers if they exist and then split up that image into seperate
	potential numbers to detect with pytesseract which is a wrapper to a Google
	cv api. If I get a plausible affinity buff number back I added it to the
	list of buffs and keep tabs on it.

Usage:

	Configured for a 1920 x 1080 resolution with default Warframe hud settings.

	You need to pip install the modules below.

	Ran on python 3.7.
