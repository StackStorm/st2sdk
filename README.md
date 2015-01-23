# StackStorm SDK

This repository contains different utilities and tools which help with the
StackStorm integration pack development.

## Tools

### Pack Bootstrap / Scaffolding tool

Pack bootstrap tool makes it easier to get started with the StackStorm pack
development.

Currently, the tool creates the correct pack directory structure.

#### Usage

Run tool in the non-interactive mode:

```bash
st2sdk bootstrap <pack name>
```

This will create a pack directory named ``<pack name>`` in the current
working directory. This directory will contain all the directories and files
which are needed by pack.

Run tool in the interactive mode:

```bash
st2sdk bootstrap -i [pack name]
```

In the interactive mode, the tool will ask you a couple of questions and the
answers will be used to populate pack metadata and other files.

## Copyright, License, and Contributors Agreement

Copyright 2015 StackStorm, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this work except in compliance with the License. You may obtain a copy of the
License in the [LICENSE](LICENSE) file, or at:

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

By contributing you agree that these contributions are your own (or approved by
your employer) and you grant a full, complete, irrevocable copyright license to
all users and developers of the project, present and future, pursuant to the
license of the project.
