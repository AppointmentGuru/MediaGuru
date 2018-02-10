import falcon, os, io, uuid, mimetypes, requests, json
from backends.transloadit import get_params
from falcon_multipart.middleware import MultipartMiddleware

class ImageResource:

    _CHUNK_SIZE_BYTES = 4096

    def __init__(self, storage_path = '/code/images/'):
        self._storage_path = storage_path

    def on_get(self, req, resp):
        """Handles GET requests"""
        quote = {
            'quote': (
                "I've always been more interested in "
                "the future than in the past."
            ),
            'author': 'Grace Hopper'
        }

        resp.media = quote

    def on_post(self, req, resp):

        # upload:
        # title = req.get_param('title')
        image = req.get_param('file')
        name = req.get_param('name')
        practitioner = req.get_param('practitioner')
        # Read image as binary
        raw = image.file.read()
        # Retrieve filename
        # filename = image.filename
        filename = '{}-{}'.format(practitioner, name)

        # trasnload:
        files = {}
        files[filename] = raw
        data = {'template_id': '828c7570618411e7ba10e5947cea0feb'}
        params = get_params(data)
        url = 'http://api2.transloadit.com/assemblies'
        res = requests.post(url, data=params, files=files)

        data = json.loads(res.content)
        img_data = data.get('uploads')[0]
        width = img_data.get('meta', {}).get('width')

        resp.status = falcon.HTTP_201
        resp.location = 'practitioner/logo/{}_{}-logo.png'.format(width, practitioner)

api = falcon.API()
# middleware:
api = falcon.API(middleware=[MultipartMiddleware()])
# api
api.add_route('/image', ImageResource())
