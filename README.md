# ARES2APRS
Python Uploader for a Net Control Station to add locations of reports from spotters/volunteers to APRS.fi

**This project is in its infancy. Expect bugs to happen if you don't follow fields exactly. For example, you must use a full address of a location or crossroads with a town and state, or zip code. Otherwise, your icon may end up somewhere randomly.**

This software adds an object to the APRS.fi map via rotate.aprs2.net. The object will be named whatever is entered into the report field, and the comment on the object will be whatever is entered into the comment field, followed by "-Reported by {Spotter's Callsign}"

A dot symbol is hardcoded into the APRS string that is sent via a socket. Future releases will hopefully include an easy way to graphically change the icon, which will be useful for adding specific events to the map (Wx events, key locations, etc)


Example:
![image](https://github.com/N1OF/ARES2APRS/assets/125296450/ac1e8796-15fe-4bae-b117-840cfaa073a4)
