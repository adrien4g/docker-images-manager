import docker

class DockerImageKiller:
    def __init__(self):
        self.client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        self.images = []
        self.sorted_images = {}

    def get_images(self):
        self.images = self.client.api.images()
        return self.images

    def organize_images(self):
        images_with_app_tag = [x for x in self.images if x['Labels'] != None and 'app' in x['Labels']]
        sorted_images = sorted(images_with_app_tag, key=lambda d: (d['Labels']['app'], d['Created']))

        for img in sorted_images:
            key = img['Labels']['app']
            if not key in self.sorted_images:
                self.sorted_images[key] = []
            self.sorted_images[key].append(img)
        return self.sorted_images

    def delete_images(self, keep_last_versions = 2, output=True):
        for current_group in self.sorted_images:
            for current_image in self.sorted_images[current_group][:-keep_last_versions]:
                try:
                    self.client.api.remove_image(current_image['Id'])
                    if output: print('Deleting: {}'.format(current_image['Id']))
                except Exception as e:
                    print(e)
                    continue
