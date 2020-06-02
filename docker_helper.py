import sys

import docker

from . import secrets


def run(image, ports):
    print("Connecting to docker client...")
    try:
        d = docker.DockerClient(base_url="tcp://docker:2735")
    except Exception as e:
        print(e)
        print("Error while connecting to docker client")
        return False

    print("Connected")

    try:
        d.login(username=secrets.username, password=secrets.password)
    except Exception as e:
        print(e)
        print("Error during login")
        return False

    print("Logged in")

    try:
        d.images.pull(image)
    except Exception as e:
        print(e)
        print("Error while pulling the image")
        return False

    print("Pulled image")

    try:
        container = d.containers.create(image, ports=ports)
    except Exception as e:
        print(e)
        print(f"Error while creating image {image}")
        return False

    print(f"Created container for image {image}")

    try:
        container.start()
    except Exception as e:
        print(e)
        print(f"Error while starting container for image {image}")
        return False

    print(f"Started container for image {image}")

    return True
