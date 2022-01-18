from DockerImageKiller import DockerImageKiller

client = DockerImageKiller()
client.get_images()
client.organize_images()
client.delete_images()