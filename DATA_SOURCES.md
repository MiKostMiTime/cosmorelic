# DATA_SOURCES.md — CosmoRelic

All external data, resources, code and images used by this project are listed
below, as required by the NASA Space Apps submission form. Everything here is
publicly accessible with no login.

**No copyrighted material is used.** Only NASA public-domain sources and
open-source software appear in this file. No journal article, news article,
Wikipedia text or third-party image is used or cited.

Verified: 14 November 2026.

---

## 1. NASA data and resources used

| Link Text | URL | What it provides |
|---|---|---|
| JPL Horizons System | https://ssd.jpl.nasa.gov/horizons/ | Live Earth–Moon and Earth–Mars distance, queried at runtime |
| JPL Horizons API | https://ssd.jpl.nasa.gov/api/horizons.api | The endpoint the app calls (`COMMAND=301` Moon, `499` Mars, `CENTER=500@399`) |
| NASA NSSDCA Master Catalog | https://nssdc.gsfc.nasa.gov/nmc/ | Spacecraft records and mission status |
| Apollo Lunar Module Eagle (1969-059C) | https://nssdc.gsfc.nasa.gov/nmc/spacecraft/display.action?id=1969-059C | Eagle record |
| Apollo Lunar Module Challenger (1972-096C) | https://nssdc.gsfc.nasa.gov/nmc/spacecraft/display.action?id=1972-096C | Challenger record |
| NSSDCA Apollo Landing Site Coordinates | https://nssdc.gsfc.nasa.gov/planetary/lunar/lunar_sites.html | Apollo landing coordinates (the MEASURED values on lunar cards) |
| NSSDCA Apollo Lunar Landings | https://nssdc.gsfc.nasa.gov/planetary/lunar/apolloland.html | Apollo landing dates and sites |
| NSSDCA Moon Fact Sheet | https://nssdc.gsfc.nasa.gov/planetary/factsheet/moonfact.html | Archival Earth–Moon distance range (offline fallback) |
| NSSDCA Mars Fact Sheet | https://nssdc.gsfc.nasa.gov/planetary/factsheet/marsfact.html | Archival Earth–Mars distance range (offline fallback) |
| NASA GISS Mars24 — Mars Landers | https://www.giss.nasa.gov/tools/mars24/help/landers.html | Mars landing coordinates (Viking 1, Pathfinder, Spirit, Opportunity, InSight) |
| NASA Image and Video Library | https://images.nasa.gov/ | Archival photographs used in the UI |
| NASA Moon Trek | https://trek.nasa.gov/moon/ | Surface exploration link on lunar relics |
| NASA Mars Trek | https://trek.nasa.gov/mars/ | Surface exploration link on Mars relics |
| NASA Science — Ingenuity Mars Helicopter | https://science.nasa.gov/mission/mars-2020-perseverance/ingenuity-mars-helicopter/ | Ingenuity flight record and final flight date |
| NASA — Ingenuity Mission Ends | https://www.nasa.gov/news-release/after-three-years-on-mars-nasas-ingenuity-helicopter-mission-ends/ | Rotor damage on the final landing |
| NASA Planetary Data System | https://pds.nasa.gov/ | Archival ground truth for mission records |
| NASA Science — Viking 1 | https://science.nasa.gov/mission/viking-1/ | Viking 1 landing, first surface photograph, faulty-command ending |
| NASA Science — Mars Pathfinder | https://science.nasa.gov/mission/mars-pathfinder/ | Pathfinder and Sojourner mission record |
| NASA Science — Spirit & Opportunity | https://science.nasa.gov/mission/mars-exploration-rovers-spirit-and-opportunity/ | MER mission records and discoveries |
| NASA Science — InSight | https://science.nasa.gov/mission/insight/ | InSight mission record and seismology results |
| NASA — Apollo 11 Mission Overview | https://www.nasa.gov/history/apollo-11-mission-overview/ | Eagle descent-stage status and ascent-stage jettison |
| NASA — InSight's Mole Ends Its Journey | https://www.nasa.gov/centers-and-facilities/jpl/nasa-insights-mole-ends-its-journey-on-mars/ | The heat probe stopped far short of its target depth |
| NASA — Opportunity's Last Message | https://science.nasa.gov/resource/opportunitys-last-message/ | The final telemetry behind the "battery low" paraphrase |
| NASA — InSight Retirement Release | https://www.nasa.gov/press-release/nasa-retires-insight-mars-lander-mission-after-years-of-science/ | Last contact and the "dead bus" description |
| NASA — Spirit Contact Concluded | https://www.nasa.gov/home/hqnews/2011/may/HQ_11-167_Spirit_Status.html | Spirit's last communication date |
| NASA — Mars Pathfinder Winds Down | https://science.nasa.gov/solar-system/mars-pathfinder-winds-down-after-phenomenal-mission/ | Pathfinder's final transmission |
| NASA Media Usage Guidelines | https://www.nasa.gov/nasa-brand-center/images-and-media/ | The basis on which NASA imagery is reused here |

---

## 2. Archival images used (all NASA, all credited in the UI)

| Relic | Link Text | URL | Credit |
|---|---|---|---|
| Eagle | Apollo 11: Second Look (LRO) | https://images-assets.nasa.gov/image/PIA12909/PIA12909~small.jpg | NASA/GSFC/Arizona State University |
| Challenger | Apollo 17 LM "Challenger" liftoff | https://images-assets.nasa.gov/image/S72-55421/S72-55421~medium.jpg | NASA/JSC |
| Ingenuity | Perseverance's Selfie with Ingenuity | https://images-assets.nasa.gov/image/PIA24542/PIA24542~medium.jpg | NASA/JPL-Caltech/MSSS |
| Viking 1 | First Photograph Taken On Mars Surface | https://images-assets.nasa.gov/image/PIA00381/PIA00381~thumb.jpg | NASA/JPL |
| Sojourner | Color Mosaic of Rover & Terrain | https://images-assets.nasa.gov/image/PIA00621/PIA00621~small.jpg | NASA/JPL |
| Spirit | Spirit, McMurdo Panorama | https://images-assets.nasa.gov/image/PIA16442/PIA16442~medium.jpg | NASA/JPL-Caltech/Cornell/Arizona State University |
| Opportunity | Opportunity's First Selfie | https://images-assets.nasa.gov/image/PIA22222/PIA22222~medium.jpg | NASA/JPL-Caltech |
| InSight | InSight's Final Selfie | https://images-assets.nasa.gov/image/PIA25287/PIA25287~medium.jpg | NASA/JPL-Caltech |

All eight URLs were checked and returned HTTP 200 on 14 November 2026. Each is a
credit-line image with no identifiable person in it. The Spirit credit names
Cornell University and Arizona State University because that is how NASA
publishes the image; the credit line is reproduced exactly as NASA gives it.

---

## 3. Open-source software used

| Link Text | URL | License |
|---|---|---|
| Gradio | https://github.com/gradio-app/gradio | Apache-2.0 |
| OpenAI Python SDK | https://github.com/openai/openai-python | Apache-2.0 |
| requests | https://github.com/psf/requests | Apache-2.0 |
| python-dotenv | https://github.com/theskumar/python-dotenv | BSD-3-Clause |
| JupyterLab | https://github.com/jupyterlab/jupyterlab | BSD-3-Clause |
| nbformat | https://github.com/jupyter/nbformat | BSD-3-Clause |
| Python | https://www.python.org/ | PSF-2.0 |
| openai/gpt-oss-20b | https://huggingface.co/openai/gpt-oss-20b | Apache-2.0 |
| Groq API | https://console.groq.com/docs/deprecations | Commercial terms of service |

---

## 4. Runtime data flow (why every number is traceable)

1. **Live distance.** `core.live_range()` queries JPL Horizons for the current
   day and reads the center-to-center distance in AU (column 4 of the returned
   ephemeris), converting to kilometres. Badge: **EPHEMERIS**.
2. **Light travel time.** That distance divided by the speed of light. Badge:
   **DERIVED**.
3. **Time since last contact.** Calendar arithmetic from a recorded date.
   Badge: **DERIVED**.
4. **Coordinates and mission status.** Static values in `cosmorelic_data.py`,
   each carrying its own source string. Badge: **MEASURED** or **ARCHIVAL**.
5. **Offline.** Horizons is not reachable, so the card shows the NSSDCA archival
   range for the body and labels it **ARCHIVAL** with the words "typical range,
   not live". No number is ever invented.

The AI persona receives only the rendered card text. It cannot introduce a
number that is not already on the card.

---

## 5. Space Agency Partner data

None used. All data in this project comes from NASA sources listed in section 1.
