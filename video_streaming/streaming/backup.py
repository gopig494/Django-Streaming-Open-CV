import cv2
import threading
from django.http import HttpResponse
from streaming.models import *
from django.views.decorators.csrf import csrf_exempt

class VideoStreamThread(threading.Thread):
    def __init__(self, request, video_file_path):
        super().__init__()
        self.request = request
        self.video_file_path = video_file_path
        self.stop_event = threading.Event()
    
    def __del__(self):
        self.video.release()

    def run(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        frame =  jpeg.tobytes()
        self.gen(frame)

    def gen(self,frame):
        while True:
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_stream(request, video_id):
    video = Video.objects.get(id=video_id)
    thread = VideoStreamThread(request, video.video_url.path)
    return StreamingHttpResponse(thread.start(),content_type='multipart/x-mixed-replace; boundary=frame')


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture("/home/gopi/Downloads/video.mp4")
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


from django.http import StreamingHttpResponse

# @csrf_exempt
def video_feed(request):

    return StreamingHttpResponse(gen(VideoCamera()),
                                                     content_type='multipart/x-mixed-replace; boundary=frame')







class VideoStreaming:
    def __init__(self, src=0):
        self.capture = cv2.VideoCapture(src)
        self.frame = None
        self.stopped = False

    def start(self):
        t = threading.Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self


    def update(self):
        while True:
            if self.stopped:
                self.capture.release()
                return
            ret, frame = self.capture.read()
            if ret:
                self.frame = frame
            else:
                self.stopped = True


    def read(self):
        if self.frame is not None:
            return self.frame.tobytes()
        else:
            return None


    def stop(self):
        self.stopped = True


def gen(camera):
    while True:
        frame = camera.read()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture("/home/gopi/Downloads/video.mp4")
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


from django.http import StreamingHttpResponse

# @csrf_exempt
def video_feed(request):

    return StreamingHttpResponse(gen(VideoCamera()),
                                                     content_type='multipart/x-mixed-replace; boundary=frame')

    # camera = VideoStreaming("/home/gopi/Downloads/video.mp4").start()

    # return HttpResponse(gen(camera), content_type="multipart/x-mixed-replace; boundary=frame")