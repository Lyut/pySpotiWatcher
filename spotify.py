import frida
import time
import requests
import subprocess


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


CMDADDTEXT = "0"
OPENTRACK = "0x1597090"
CEFPARSEURL = "0x1DDE250"

pid = frida.spawn("/opt/spotify/spotify")
session = frida.attach(pid)
stopped = False
destroyed = False


def on_message(message, data):
    global stopped
    stopped = True
    try:
        if message['payload'] is not None:
            print(bcolors.OKGREEN + "[+] CmdAddText pattern found! Address: " + bcolors.ENDC + message['payload'])
            CMDADDTEXT = message['payload']

            cmdaddtextscript = session.create_script("""
            Interceptor.attach(ptr("%s"), {
                onEnter(args) {
                    if (ptr(args[6]).readCString().indexOf("track") !== -1) {
                        send(ptr(args[7]).readCString());
                    }
                }
            });
            """ % int(CMDADDTEXT, 16))

            def get_access_token():
                endpoint = "https://open.spotify.com/get_access_token?reason=transport&productType=web_player"
                headers = {"Accept": "application/json", "Accept-Language": "it", "App-Platform": "WebPlayer",
                           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
                           "Spotify-App-Version": "1576851415", "Referer": "https://open.spotify.com/",
                           "Cookie": "'. ' sp_t=8216320f1a1b55329cc788d3861bda2d; sp_adid=e0c4b4b0-c2ce-47b1-91cd-9a6e500bd236; _gcl_au=1.1.930311039.1568296866; _hjid=3cfe7894-03cb-49b7-a008-59e9e02a58c6; _fbp=fb.1.1568296866726.817501151; open_env=php; sp_ab=%7B%222019_04_premium_menu%22%3A%22control%22%7D; sp_gaid=0088fcae70df1230ce6227ad4c27d9dfc16b52d53070edbb54dadd; sp_phash=5b159869266f788cd98cb9ddbdfb3bcbeacac1cd; spot=%7B%22t%22%3A1576582774%2C%22m%22%3A%22jp%22%2C%22p%22%3A%22open%22%7D; optimizelyEndUserId=oeu1576847786549r0.3765501627206682; optimizelySegments=%7B%226174980032%22%3A%22search%22%2C%226176630028%22%3A%22none%22%2C%226179250069%22%3A%22false%22%2C%226161020302%22%3A%22gc%22%7D; optimizelyBuckets=%7B%7D; sp_last_utm=%7B%22utm_campaign%22%3A%22your_account%22%2C%22utm_medium%22%3A%22menu%22%2C%22utm_source%22%3A%22spotify%22%7D; __gads=ID=46eef32200ade146:T=1577188825:S=ALNI_MaSsNN-fkmKLUqUmpi87Lkk6BJz4Q; _ga_0KW7E1R008=GS1.1.1577195047.3.1.1577195874.0; _derived_epik=dj0yJnU9ZHhLV1NmV3hhb2VKOWhEcWdGUTRuN0RhbC1OdEFBMnMmbj1tOU5DS1E5UU11U1pQeWlLNTJMRW1RJm09NyZ0PUFBQUFBRjRDR1dJ; _ga=GA1.2.1103680000.1568296854; sp_landing=http%3A%2F%2Fopen.spotify.com%2F; sss=1; _gid=GA1.2.1895535078.1577587497; sp_dc=AQAMQHYD7SGCY6Hu8aFyjDsPfTkv7s4LqxCm9fOMMsph1GR8yCxW_9cqOoeQH8TeFvcTrTEfcFcCiEZemGSWpCcSE9ESBTJVoW0X6ICQUg; sp_key=99d88c42-2b0f-41c8-b3e3-e764398ce474; _gat_gtag_UA_5784146_31=1"}
                response = requests.get(endpoint, headers=headers).json()
                return response['accessToken']

            def on_message(message, data):
                global stopped
                stopped = True
                try:
                    if message['payload'] is not None and "spotify:track" in message['payload']:
                        print(bcolors.OKGREEN + "[+] You're listening to track: " + bcolors.ENDC + message['payload'])
                        endpoint = "https://api.spotify.com/v1/tracks/" + message['payload'][-22:]
                        headers = {"Authorization": "Bearer " + get_access_token()}
                        response = requests.get(endpoint, headers=headers).json()
                        print(bcolors.OKCYAN + response['artists'][0]['name'] + " - " + response['name'] + bcolors.ENDC)
                        output = subprocess.getoutput(
                            "curl \"" + response['album']['images'][0]['url'] + "\" -o cover.png")
                        output = subprocess.getoutput("catimg cover.png -w 100")
                        print(output)

                except KeyError as ke:
                    pass

            def on_destroyed():
                global destroyed
                destroyed = True

            cmdaddtextscript.on('message', on_message)
            cmdaddtextscript.on("destroyed", on_destroyed)
            cmdaddtextscript.load()

            cefparseurlscript = session.create_script("""
            Interceptor.replace(ptr("%s"), new NativeCallback((pathPtr, flags) => {
              send("cef_called");
              return false;
            }, 'int', 'int', ['int', 'int']));
            """ % int(CEFPARSEURL, 16))

            def on_message(message, data):
                global stopped
                stopped = True
                try:
                    if message['payload'] is not None and "cef_called" in message['payload']:
                        print(bcolors.FAIL + "[+] ParseUpdateUrl called!" + bcolors.ENDC)
                except KeyError as ke:
                    pass

            def on_destroyed():
                global destroyed
                destroyed = True

            cefparseurlscript.on('message', on_message)
            cefparseurlscript.on("destroyed", on_destroyed)
            cefparseurlscript.load()
    except KeyError as ke:
        pass


script = session.create_script("""
    var processes = Process.enumerateModules();
    var process;
    
    function processNext(){
			process = processes.pop();
			if(!process){
				return;
			}
			
		Memory.scan(process.base, process.size, '%s', {
			onMatch: function(address, size){
			address = address.sub(14);
					send(address.toString());
				}, 
			onError: function(reason){
					console.log('[!] There was an error scanning memory');
				}, 
			onComplete: function(){
                    processNext();
				}
			});
	}
			processNext();
""" % "81 EC ?? ?? ?? ?? 44 89 4D D0 44 89 45 D4 49 89 CC 49 89 D5")

script.on('message', on_message)
script.load()

frida.get_local_device().resume(target=pid)

try:
    # load script & edit memory
    while not stopped:
        time.sleep(1)

    # wait until IDA is not closed to join gracefully
    while not destroyed:
        time.sleep(1)
except KeyboardInterrupt:
    pass
