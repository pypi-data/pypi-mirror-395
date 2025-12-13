# PetName and Distributed Directory Name resolver

`petnames` resolves names to machine addresses (or any other value humans find difficult to remember).

Resolution starts from the local database on your device, which can contain references to any Distributed Directory service.

For a name like : **servers.work.server1**

+ **servers** is resolved locally to a collection

+ **work** is found in the local collection, pointing to a remote directory

+ **server1** is submitted as a query to that directory

+ The directory returns a PetName record, containing: **addr = abcd..eeff**

+ Your application can initiate a connection to that address.

The local database contains entries which can point directly to resources (e.g. on P2P networks) or to other directories e.g. a community-run directory, commercial directory, government directory, etc.


## BETA SOFTWARE!

This is still a work-in-progress. Currently only the local-directory resolving is implemented, but this is already useful to save having to copy-paste X25519 Ids, Bitcoin addresses, etc.


## Try it:

+ Install the package with `pip install petnames`
+ Create a file `~/.local/share/petnames/local/server1.txt` containing lines like these:

```
suggested_name=Server One
addr = aabbccddeeffaabbccddeeffaabbccdd
```

+ Run `ddig server1` which should display the properties you created


## Command-line usage:

ddig NAME [PROPERTY]

NAME is a sequence of names joined by periods

PROPERTY is the record property you want to retrieve (default: 'all')


## Application integration:

```
from petnames import get_property

addr1 = get_property(arg1, "b_addr")
if addr1:
    connect(addr1)
```


## Further information

See the examples at : [https://codeberg.org/skyguy/petnames](https://codeberg.org/skyguy/petnames)

Feedback welcome!
