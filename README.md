# API

My main problem with APIs I usualy meet:

Getting all the nested information I want usualy require to make
multiple requests, possibly in nested loops. (Get object1, get all
objects in relation with that one, then ask for each objects in relation
to those objects, ...)

Even if each request in fairly fast, the number of increasing requests
tend to end with a high delay to gather all information. One easier way
would be to do a single request per object type to the end backend (ie:
one request per table for mysql backend)

To avoid having to maintain alot of different function, I tend to prefer
generic functions, even if some special cases might imply specific codes
here and there.


Those documents present a idea of API. Any comment about it would be
appreciated.

## types.json

Describe how the different known types will be presented.

Listing and describing the objects we are able to handle seems like a nice
thing to do, especialy for auto-discovery and generic applications.

## search.json

Describe a search request.

A search request will be able to:

  * Filter what objects we want to find
  * List exactly what fields and netsted fields we are interested in

Nesting results would allow to get **everything** we need from that point
without needing to loop on result and ask more information on each objects
because of lack of information.

## update.json

Describe a modification request.

Creating, Updating and/or Deleting objects might be an "atomic" operation. That api allow to find a few objects and ask multiple operations at once, with objects refering each others.
