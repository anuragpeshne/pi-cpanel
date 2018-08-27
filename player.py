import subprocess

class Player:
    def __init__(self):
        self.reset()

    def decode_url(self, url):
        ydl_proc = subprocess.Popen(["youtube-dl",
                                     "--get-url", url,
                                     "--playlist-start", str(self.playlist_index),
                                     "--no-playlist"],
                                    stdout = subprocess.PIPE,
                                    stdin = subprocess.PIPE)
        try:
            outs, errs = ydl_proc.communicate(input=None,timeout=15)
            outs = outs.decode("utf-8").strip().split("\n")
            self.playlist = outs
        except:
            outs = "Timeout during decoding"
        return outs

    def play(self):
        self.omx_proc = subprocess.Popen(["omxplayer",
                                          self.playlist[self.playlist_index]],
                                         stdout = subprocess.PIPE,
                                         stdin = subprocess.PIPE)
        try:
            outs, errs = self.omx_proc.communicate(input=None,timeout=3)
        except:
            outs = outs
            pass
        return outs.decode("utf-8")

    def control_omx_proc(self, req):
        if (req == "vol_up"):
            cmd = "+"
        elif (req == "vol_down"):
            cmd = "-"
        elif (req == "pause_toggle"):
            cmd = "p"
        elif (req == "quit"):
            cmd = "q"

        try:
            outs, errs = self.omx_proc.communicate(input=cmd,timeout=1)
        except:
            outs = outs
            pass
        if (cmd == "q"):
            self.reset()
        return outs.decode("utf-8")

    def reset(self):
        self.playlist_index = 1
        self.playlist = []
        self.nowplaying = None
        self.omx_proc = None
p = Player()
