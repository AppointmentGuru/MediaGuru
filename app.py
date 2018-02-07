import falcon, os, io, uuid, mimetypes, requests
from backends.transloadit import get_params

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
        ext = mimetypes.guess_extension(req.content_type)
        # name = '{uuid}{ext}'.format(uuid=uuid.uuid4(), ext=ext)
        name = 'mumtaz.png'
        image_path = os.path.join(self._storage_path, name)

        with io.open(image_path, 'wb') as image_file:
            while True:
                chunk = req.stream.read(self._CHUNK_SIZE_BYTES)
                if not chunk:
                    break

                image_file.write(chunk)

        # trasnload:
        files = {'file': open(image_path, 'rb')}
        data = {'template_id': '828c7570618411e7ba10e5947cea0feb'}
        params = get_params(data)
        url = 'http://api2.transloadit.com/assemblies'
        res = requests.post(url, data=params, files=files)
        print(res.content)

        resp.status = falcon.HTTP_201
        resp.location = '/images/' + name



api = falcon.API()
api.add_route('/image', ImageResource())
