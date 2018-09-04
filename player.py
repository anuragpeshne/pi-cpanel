import pexpect

class Player:
    def __init__(self):
        self.reset()

    def decode_url(self, url):
        ydl_proc = pexpect.spawn('youtube-dl --get-url ' + url +
                                 ' -f best ' +
                                 ' --playlist-start ' + str(self.playlist_index) +
                                 ' --no-playlist')
        ydl_proc.expect('http.*', timeout=15)
        output = ydl_proc.after.decode("utf-8")
        links = output.strip().split('\n')
        self.playlist = links
        return links

    def play(self):
        self.omx_proc = pexpect.spawn('omxplayer ' + self.playlist[self.playlist_index - 1])
        self.omx_proc.expect("Video.*")
        self.nowplaying = True
        return self.omx_proc.after.decode("utf-8")

    def stop(self):
        self.control_omx_proc('quit')
        self.nowplaying = False
        self.reset()

    def control_omx_proc(self, req):
        if (req == "vol_up"):
            cmd = "+"
            exp = "Current Volume: .*"
        elif (req == "vol_down"):
            cmd = "-"
            exp = "Current Volume: .*"
        elif (req == "pause_toggle"):
            cmd = "p"
            exp = ".*"
        elif (req == "quit"):
            cmd = "q"
            exp = "Stopped at.*"

        self.omx_proc.send(cmd)
        self.omx_proc.expect(exp)
        output = self.omx_proc.after.decode("utf-8")
        if (cmd == "q"):
            self.reset()
        return output

    def reset(self):
        self.playlist_index = 1
        self.playlist = []
        self.nowplaying = False
        self.omx_proc = None
p = Player()
