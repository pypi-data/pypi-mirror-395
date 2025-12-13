# NWeb Client 

Client to access the NWeb-API


## Installation
```
pip install --upgrade nwebclient

# oder

pip install .

```

```
python -m nwebclient help
```

More [Documentation](https://gitlab.com/bsalgert/nwebclient/-/wikis/home)

### Docker

```
docker run --rm -it -p 7171:7070 -e PIP_PKGS=/parent/home/pi/dev/nxbot -v /:/parent/ nxware/nxdev npy serv --install
```


## Beispiel
```
import nwebclient
```


```
class NWebClient
  """ Anstatt url kann auch ein Pfad zur einer JSON-Datei, die die Schluessel enthaelt, angegeben werden. """
  __init__(url, username,password)
  doc(id)
  docs(q)
  group(id)
  getOrCreateGroup(guid, title)
  downloadImages()

metric_val(endpointUrl:string, metricName:string, val:numeric)
```


Links: [Gitlab-Repo](https://gitlab.com/bsalgert/nwebclient) [PyPi-Package](https://pypi.org/project/nwebclient/)

Git-URL: `git@gitlab.com:bsalgert/nwebclient.git`

---
Packaging: https://packaging.python.org/tutorials/packaging-projects/
