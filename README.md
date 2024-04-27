# ARES2APRS
Python Uploader for a Net Control Station to add locations of reports from spotters/volunteers to APRS.fi

**This project is in its infancy. Expect bugs to happen if you don't follow fields exactly. For example, you must use a full address of a location or crossroads with a town and state, or zip code. Otherwise, your icon may end up somewhere randomly.**

This software adds an object to the APRS.fi map via rotate.aprs2.net. The object will be named whatever is entered into the report field, and the comment on the object will be whatever is entered into the comment field, followed by "-Reported by {Spotter's Callsign}"

**PREREQUISITES**

-Python (duh)

-Pillow and Geopy libraries. Installable using pip.

-Internet Connection

-Patience with the developers

-Valid Amateur Radio Callsign and APRS passcode. (Magicbug has a great APRS passcode generator available here: https://github.com/magicbug/PHP-APRS-Passcode)

**APRS SYMBOLS**

To add symbols to your APRS packet, you must use notation for either primary (/) or alternate (\\) icon tables, followed by the symbol. You may use any symbol you desire, however, modifiers are not accepted at this time.
 
Example: You want to add the wall cloud symbol to your report. You would type \\ (no quotes) into the table select, followed by [ in the Symbol field. Lookup tables can be found 
here: https://www.yachttrack.org/info_camper/downloads/APRS_Symbol_Chart.pdf


**Examples:**

APRS Object

![image](https://github.com/N1OF/ARES2APRS/assets/125296450/ac1e8796-15fe-4bae-b117-840cfaa073a4)


Software GUI

![image](https://github.com/N1OF/ARES2APRS/assets/125296450/a78dbd60-acb9-4add-aa52-54b81f257861)




**About our versioning:**
Our versioning is as follows:
v(Major).(Minor).(Bugfix)(Type)-(Build)

So for example, v0.2.0b-2 reads out to be
"Version 0, minor update 2, bugfix 0, beta, build 2"

Why the build number? Sometimes changes don't neatly fall into one of the options above, so hence the build number. 
Maybe there was a typo in documentation, or code was cleaned up. It allows more granularity to the versioning.
 
