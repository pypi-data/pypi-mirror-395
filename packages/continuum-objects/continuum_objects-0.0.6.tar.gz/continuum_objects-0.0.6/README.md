# Continuum Objects

This python library is used to describe objects of the digital continuum :

- computing clusters,

- data centers,

- user workspaces,

- ...

All objects are described through [pydantic BaseModel](https://docs.pydantic.dev), ensuring easy **importation**, **exportation** and **validation**.

## Examples

See file [example.py](example.py) to get an example of usage.

Example of object description :

```json
{
  "id": "c11a0535-b154-4deb-ba71-ed1613290271",
  "type": "Partition",
  "name": "cpu_p1",
  "totalNodeCount": 720,
  "nodes": [
    {
      "type": "NodeGroup",
      "id": "415a18d3-ae83-43e6-8013-a19d771ed3d5",
      "nodeComponents": [
        {
          "type": "CPU",
          "name": "Intel Xeon Gold 6248",
          "count": 2
        },
        {
          "type": "RAM",
          "capacity": {
            "value": 192,
            "unit": "GB"
          },
          "count": 1
        },
        {
          "type": "MotherBoard",
          "count": 1
        }
      ]
    }
  ]
}
```
