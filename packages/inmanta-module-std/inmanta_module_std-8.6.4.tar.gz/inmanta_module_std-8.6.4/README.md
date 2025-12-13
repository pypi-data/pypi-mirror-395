# std module

Inmanta base module that defines primitive types, entities and plugins regularly used when developing models.

## Features

* Definition of Resource to define new resource:
  * `Resource`/ `PurgeableResource` / `ManagedResource`: Base classes to define new resources
  * `DiscoveryResource`: To define a resource that scans the infrastructure for a certain type of deployment
* Definition of `ResourceSet` (to manage resources in different sets) entities
* Create, Read, Update, Delete of ***Agent Configuration*** to manage the different settings of the agent
* Primitive type definitions such as:
  * `Datetime`
  * `IP`
  * `Port`
  * `URL`
  * `UUID`
* `NullResource` entity mainly used for testing


## Usage example

This simple example shows how to create an agent configuration. This configuration will try to update part of the agent configuration on the orchestrator. An agent configuration is mandatory to deploy the resource to the infrastructure because the orchestrator relies on an agent to do so.

```inmanta
std::AgentConfig(
    autostart=true,
    agentname="http://example.com",
    uri="local:",
)
```

The name of this agent `http://example.com` can now be referred to when defining a python Resource

```python
@inmanta.resources.resource(
    "__config__::MyNewResource",
    "uri",
    "agentname"  # This is the name of the field that will refer to the agent's name, in this case this field will contain `http://example.com`
)
class EntitlementResource(inmanta.resources.PurgeableResource):
    pass
```

More information about developing Python Resources and Handlers can be found [here](https://docs.inmanta.com/inmanta-service-orchestrator/latest/model_developers/handlers.html#handler).

Another example would be to define a new resource that can be created / updated / removed. The following example is really basic
and should probably not be implemented, an inventory would be better for that. But for the sake of a basic example, let's suppose that
we want a resource that represent the reservation of an IP address from a particular user. We would also save the datetime at which the
request has been made.

```inmanta
entity MyNewResource extends PurgeableResource:
    """
        A base class for a resource that can be purged and can be purged by Inmanta whenever the resource is no
        longer managed.

        :attr purged: Set whether this resource should exist or not.
    """
    ipv4_address reserved_ip
    datetime since
    name_email user
    string agentname
end

implement MyNewResource using parents

new_resource = MyNewResource(
    reserved_ip="192.168.1.1",
    since="1970-01-01T00:00:00",
    user="Fred Bloggs <fred.bloggs@example.com>",
    agentname="http://example.com",
)
```

If we wanted to remove ("purge" in inmanta terms) this resource, we would do the following:

```inmanta
new_resource = MyNewResource(
    reserved_ip="192.168.1.1",
    since="1970-01-01T00:00:00",
    user="Fred Bloggs <fred.bloggs@example.com>",
    purged=true,  # This is the diff
    agentname="http://example.com",
)
```

We can also define new types:
- Based on constraints on the type
- Provide a list of values (Enum)
- Use an existing pydantic type to enforce additional constraints
- Rely on regex
```inmanta
typedef port as int matching self >= 1024 and self < 65536
"""
    A TCP/UDP port number that an user can use.
"""

typedef protocol as string matching self in ["tcp", "udp"]
"""
    A protocol
"""

typedef negative_float as number matching std::validate_type("pydantic.NegativeFloat", self)
"""
    A floating point number less than zero.
"""

typedef alfanum as string matching std::validate_type("pydantic.constr", self, {"regex": "^[a-zA-Z0-9]*$", "strict": true})
"""
    An alfanumeric number (lower- and uppercase characters are allowed).
"""
```

```{toctree}
:maxdepth: 1
autodoc.rst
CHANGELOG.md
```
