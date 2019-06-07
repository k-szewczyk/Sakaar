# Sakaar

Sakaar is REST api application. It simulates Colosseum like battles,
but in far and unfriendly planet.

Rules are simple:
 - Heroes can fight with each one only once,
 - Only GrandMaster can choose attendees for every fight,
 - Some races can't fight with another (for example hedgehogs can fight with hamsters, but can't fight with humans)


### Prerequisites

 - python 3.7
 - docker, and docker-compose
 - Make
 
### Installing
To start this app just simply type
```bash
make build-dev
make dev
```
