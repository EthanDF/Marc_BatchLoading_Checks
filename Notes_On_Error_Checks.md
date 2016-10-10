#Notes on Error Checks

Notes on error checks related to streaming video mostly based on the OLAC Best Practices for Cataloging Streaming Video:

[http://olacinc.org/drupal/capc_files/Streaming_Media_RDA.pdf](http://olacinc.org/drupal/capc_files/Streaming_Media_RDA.pdf)

[my annotated version](https://via.hypothes.is/http://olacinc.org/drupal/capc_files/Streaming_Media_RDA.pdf)

#notes
------
* A RDA can be assumed to be RDA compliant when:
    1. Leader 18 (DESC) should be _i_ or _c_ (ISBD punctuation included or ISBD punctuation ommited, resp.)
    2. MARC 040 subfield e = "rda"
* RDA related fields that can appear in non-RDA records:
    * MARC 264 - can be following AACRD2 Rules
    * MARC 336, 337, and 338
    * Relationship designators in MARC 1xx, 7xx, and 8xx subfields, e and j
    * additional MARC fields could be included in both AACR2 and RDA records, such as the MARC 344, 346 and the 347 fields.
* In most cases, comprehensive description will be the best choice for individual streaming media resources ([RDA 1.5.2](http://access.rdatoolkit.org/rdachp1_rda1-678.html)).
* MARC 588 _should be_ present as the source of title information.
* MARC 245 is core to RDA, so it should be present - both subfields _a_ and _c_ at least
* MARC 264 can be the copyright date in subfield _c_ - it should be recorded with a copyright symbol (c) and second indicator = 4
* MARC 337 should always be 337 __ $a computer $b c $2 rdamedia
* MARC 338 should always be 338 __ $a online resource $b cr #2 rdacarrier
* MARC 300, record the extent and type of carrier as an online resource witht he extent and file type of the subunits, 300__ $a 1 online resource (1 video file). Include the extent parenthetically, eg: 300__ $a 1 online resource (video files (40 min. each)) : $b silent, color, with black and white sequences
	* If recording the color of the item in subfield _b_, should be in following list: ['black and white', 'black and white (tinted)', 'black and white (toned)', 'black and white (tinted and toned)', 'sepia', 'color']
	* minutes should be abbreviated as "min."
	* seconds should be abbreviated as "sec."
* MARC 506, Restrictions on Access or Use, should only be applicable locally and should tagged as such
* MARC 856, URL access - if the package/provider name will not be visible in the URL, include it in subfield _3_
* MARC 336, Content Type - eg: 336 __ $a two-dimensional moving image $b tdi $2 rdacontent
* MARC 380, Form of Work, use __ $a Motion Picture or "Television program" as applicable
* MARC 046, date of recording, should be the earliest date of recording (so no other dates should be earlier), may also be found in MARC 500
* Language - record in 008/35-37, MARC 041 1_, and MARC 546
* Aspect Ratio - try to have aspect ratio in MARC 500
* MARC 500 may contain proprietary information, figure out a way to identify and remove or update
* Summarization of Content - MARC 520 - it should be there hopefully!
* Intended audience - MARC 521, hopefully should be there - core element if intended for children
* Leader/06 (Type) = "g"
* Leader/07 (BLvl) = "m"
* MARC 006
	* 05 (Audn) - code as appropriate
	* 11 (GPub) - code as appropriate
	* 06 (Form) = "o"
	* 09 (File) = "c" for representational 
* MARC 008 008/29 (Form ov visual materials) = "o" for online resources
* MARC 007 - Visual Resources
	* 00 - "v" - category of material = videorecording
	* 01 - "z" - specific material designation = other
	* 03 - code as appropriate - color
	* 04 - "e" - videorecording format = other
	* 05 - "a" - sound on medium 
	* 06 - "z" - medium for sound = other
	* 07 - "u" - dimensions = "unknown"
	* 08 - code as appropriate - configuration of playback channels
* MARC 007 - Electronic Resource
	* 00 - "c"
	* 01 - "r"
	* 03 - code as appropriate
	* 04 - "n" - dimensions = "not applicable"
	* 05 - "a" 
* Digital File Characteristics - MARC 347, this is a good place to write in the provider (subfield _3_), eg: 347 __$3 Alexander Street Video, Dance in Video$a video file $b Windows media $b RealVideo $2 rda
* System Requirements - MARC 538 data should be local and system specific. Catalog accordingly
	


