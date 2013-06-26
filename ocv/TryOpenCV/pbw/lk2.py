import numpy as np
import cv2
#import video
from common import anorm2, draw_str
from time import clock

help_message = '''
USAGE: lk_track.py [<video_source>]

Keys:
  SPACE - reset features
'''

lk_params = dict( winSize  = (15, 15), 
                  maxLevel = 2, 
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03),
                  derivLambda = 0.0 )    

feature_params = dict( maxCorners = 500, 
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

class App:
    def __init__(self, video_src):
        self.track_len = 100
        self.detect_interval = 3
        self.tracks = []
        self.cam = cv2.VideoCapture(0)#video.create_capture(video_src)
        self.frame_idx = 0

    def run(self):
        while True:
            ret, frame = self.cam.read()#get frame
            
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            vis = frame.copy()
            
            
            if len(self.tracks) > 0:
                img0, img1 = self.prev_gray, frame_gray#old and new image
                p0 = np.float32([tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)#something strange
                p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
                
                p0r, st, err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
                d = abs(p0-p0r).reshape(-1, 2).max(-1)#calc error for every point(?)
                
                good = d < 1#flag(s)
                
                new_tracks = []
                
                for tr, (x, y), good_flag in zip(self.tracks, p1.reshape(-1, 2), good):#taking old points, new points and flags
                    if not good_flag:#if bad error then next
                        continue
                    tr.append((x, y))#maybe it is path?
                    if len(tr) > self.track_len:#delete old points
                        del tr[0]
                    new_tracks.append(tr)#create new list of tracking points
                    cv2.circle(vis, (x, y), 2, (0, 255, 0), -1)#draw it
                self.tracks = new_tracks
                
                cv2.polylines(vis, [np.int32(tr) for tr in self.tracks], False, (0, 255, 0))#draw tracks
                draw_str(vis, (20, 20), 'track count: %d' % len(self.tracks))

            if self.frame_idx % self.detect_interval == 0:
                mask = np.zeros_like(frame_gray)
                mask[:] = 0

                mask[100:200, 100:200] = 255
                
                for x, y in [np.int32(tr[-1]) for tr in self.tracks]:
                    cv2.circle(mask, (x, y), 5, 0, -1)
                p = cv2.goodFeaturesToTrack(frame_gray, mask = mask, **feature_params)
                #print p, '!!!!!!!!!!!'
                if p is not None:
                    for x, y in np.float32(p).reshape(-1, 2):
                        self.tracks.append([(x, y)])


            self.frame_idx += 1
            self.prev_gray = frame_gray
            cv2.imshow('lk_track', vis)

            ch = cv2.waitKey(1)
            if ch == 27:
                break

def main():
    import sys
    #try: video_src = sys.argv[1]
    #except: video_src = video.presets['chess']

    print help_message
    App(0).run()

if __name__ == '__main__':
    main()
