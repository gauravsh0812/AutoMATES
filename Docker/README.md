The 'Dockerfile' is the docker image file to build the docker container having all the dependencies and modules, provided in requirements.txt file.
To build the container, one needs to run the given command:

```
docker build -t <docker-image-tag> .
```

```
docker run -itd --rm -v <local-dir-to-mount>:/<location-to-mount-in-docker-container> --name <a-name-for-your-container> <docker-image-tag>
```

To execute the other scripts in the container:

```
docker exec -w <dir-to-use-as-cwd-in-docker-container> <a-name-for-your-container> [<command-agrs>]
```

### NOTE: Due to security issues, I have removed "Pillow" package from the requirement.txt file. The person can add that before building image.
