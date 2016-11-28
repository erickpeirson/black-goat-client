# black-goat-client

A simple Python client for the [BlackGoat API](http://diging.github.io/black-goat/).

## Usage

```python
> import goat
> goat.GOAT = 'http://path.to.a.goat/rest'
> goat.GOAT_APP_TOKEN = 'myapptoken'
> concepts = goat.GoatConcept.search(q='Bradshaw')
> print concepts
[<goat.GoatConcept object at 0x1031cd9d0>,
 <goat.GoatConcept object at 0x1031cd990>,
 ...
 <goat.GoatConcept object at 0x1031cd790>,
 <goat.GoatConcept object at 0x1031cd6d0>]

> print concepts[0].__dict__
{
    'identifier': u'http://www.digitalhps.org/concepts/CONe5b55803-1ef6-4abe-b81c-1493e97421df',
    'data': {
        u'updated': u'2016-11-15T21:42:17.302105Z',
        u'added': u'2016-11-15T21:42:17.302056Z',
        u'name': u'Margaret Elizabeth Bradshaw',
        u'authority': {
            u'id': 1,
            u'name': u'Conceptpower'
        },
        u'local_identifier': u'http://www.digitalhps.org/concepts/CONe5b55803-1ef6-4abe-b81c-1493e97421df',
        u'concept_type': 7,
        u'identifier': u'http://www.digitalhps.org/concepts/CONe5b55803-1ef6-4abe-b81c-1493e97421df',
        u'id': 8,
        u'added_by': {
            u'username': u'erickpeirson',
            u'email': u'erick.peirson@asu.edu'
        },
        u'description': u'Botanist at the University of Exeter'
    },
    'id': 8
}
```
