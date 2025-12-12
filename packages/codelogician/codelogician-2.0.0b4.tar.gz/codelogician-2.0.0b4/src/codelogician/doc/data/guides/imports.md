----
title: Import System
description: Description of multi-file development and `import` statements
order: 4
----

- Path Imports with Implicit Module Names: `[@@@import "path/to/file.iml"]`
- Path Imports with Explicit Module Names: `[@@@import Mod_name, "path/to/file.iml"]`
- Integration with OCamlFind and Dune: `[@@@import Mod_name, "findlib:foo.bar"]`, `[@@@import Mod_name, "dune:foo.bar"]`
