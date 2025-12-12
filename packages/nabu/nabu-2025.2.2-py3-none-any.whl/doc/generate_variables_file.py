import os
from nabu import version as nabu_version

# This file is used by the "gen-files" mkdocs plugin
# It writes _data/variables.yml at build time
# which is then used by the "markdownextradata" plugin

template = """
nabu:
  version: {nabu_version}
"""


if not (os.path.exists("_data")):
    os.mkdir("_data")
with open(os.path.join("_data", "variables.yml"), "w") as f:
    content = template.format(nabu_version=nabu_version)
    f.write(content)
