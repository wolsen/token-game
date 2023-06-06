# Token Game

The token game provides a service which will generate tokens and
a validate tokens that were issued. Tokens are pre-generated.


# Building

This can be tested locally using the func tox target. Alternatively,
build a rock and run it in docker:

$ sudo snap install rockcraft --classic --edge

$ rockcraft pack

$ /snap/rockcraft/current/bin/skopeo --insecure-policy copy oci-archive:merch-game_0.1_amd64.rock docker-daemon:merch-game:0.1

$ docker run -p 8000:8080 -it --rm merch-game:0.1
