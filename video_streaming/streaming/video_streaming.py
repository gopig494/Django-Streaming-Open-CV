import cv2
import threading
from django.http import HttpResponse
from streaming.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import StreamingHttpResponse

class VideoStreamThread(threading.Thread):
    def __init__(self, video_file_path):
        super().__init__()
        self.video_file_path = video_file_path
        self.stop_event = threading.Event()

    def __del__(self):
        self.stop_event.set()

    def run(self):
        video = cv2.VideoCapture(self.video_file_path)
        while not self.stop_event.is_set():
            success, image = video.read()
            if not success:
                break
            ret, jpeg = cv2.imencode('.jpg', image)
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        video.release()

def video_feed(request):
    thread = VideoStreamThread("/home/gopi/Downloads/video.mp4")
    thread.start()
    return StreamingHttpResponse(thread.run(), content_type='multipart/x-mixed-replace; boundary=frame')

def video_stream(request, video_id):
    video = Video.objects.get(id=video_id)
    thread = VideoStreamThread( video.video_url.path)
    thread.start()
    return StreamingHttpResponse(thread.run(), content_type='multipart/x-mixed-replace; boundary=frame')