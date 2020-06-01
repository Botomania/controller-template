import sys

import docker


def run(image, ports):
    d = docker.DockerClient(base_url="unix:///var/run/docker.sock")

    try:
        container = d.containers.create(image, ports=ports)
    except Exception as e:
        print(e)
        print(f"Error while creating image {image}")
        return False

    try:
        container.start()
    except Exception as e:
        print(e)
        print(f"Error while starting container for image {image}")
        return False

    return True
