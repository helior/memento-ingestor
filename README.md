Memento Ingestor
---



Ingestor TODO:
---
- ✓ Event Namespace definition



## Other
----------

API:
---
TODO: Fetch Momentos using date range filter
TODO: Build live manifest segments using a timestamp parameter
TODO: Fetch events model


Data Model:
---
- TODO: Raw probe output mapped to data model (JSON-SCHEMA defined).
- TODO: On Insert, validate if shape is still as expected (per version of ffprobe, or output changes via new input params)
- TODO: imperitively map input probe data into Memento shape (automate later)
May 3, 2022 ⬆ Meaning, map value from one data model, into another. Optinal: transforms in-between (Wait, this is just ETL but automated)
- TODO: Save to DB

(~ ❓OLY.AI idea ~)
- ↑ Automate that step of converting raw JSON to JSON-SCHEMA definition ↑
- Using definition, generate an User Interface
- Submission of form is validated/verified
- Using definition, generate database schema
- With a Form builder, create JSON-SCHEMEA definition to then map one schema to another.
- With map, automate reading of input model data, then saving as output model



---
✅ Generator
---
`model.py`

[] list of table name
- [ read below, it's all the same pattern ]
- generates function names
- reference generated class names

`serializers.py`
- import SuperClassView
- import * from model.py
-

buildSerializerClass(objectModel)

`view.py`
{} each object, build a block of code for integration
- import SuperClassView
- import * from serializer.py
- classes[] .append(fully-built-sub-class that extends something general)
- render classes one after the other.


`url.py`
include * from view.py
{} each object gets a route

`→ companyForm.js`
`routes.js`

OR...!

Parse... build full tree, iterate over tree again with tree reference in memory
- allows sub-classes to have entire tree and generate as deep as it wants

May 3, 2022 What the heck was I talking about ⬆

---
Data Model
---
🔺 Each data model type is saved in a namespaced filename, then referenced by systems which occupy that namespace.
