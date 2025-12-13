
![coverage badge](https://gitlab.com/frederic-zinelli/mkdocs-addresses/badges/main/pipeline.svg) ![coverage badge](https://gitlab.com/frederic-zinelli/mkdocs-addresses/badges/main/coverage.svg)


## Links

* [Project repository (GitLab)](https://gitlab.com/frederic-zinelli/mkdocs-addresses)
* [Full online documentation](http://frederic-zinelli.gitlab.io/mkdocs-addresses/)
* [The project on PyPI](https://pypi.org/project/mkdocs-addresses/)



## Dependencies

* Python 3.8+
* mkdocs 1.4+
* BeautifulSoup 4+



## Overview

### About

The [`mkdocs-addresses`](https://pypi.org/project/mkdocs-addresses/) is a plugin for `mkdocs` which offers:

* Abstraction of the concrete tree hierarchy of pages and anchors within those when writing a link, utilizing unique identifiers:

    Benefit from a strong separation between logic and content, avoiding all addresses rewrite steps when some files are modified, split, merged or moved.
    <br>

* Verification of numerous links and addresses to ensure the absence of dead links or images within the documentation (including verifications beyond mkdocs 1.5+ capabilities):

    The tool warns you when something becomes wrong during development.
    <br>

* Convenient helpers to facilitate the usage of those identifiers within the docs pages. For users working with compatible IDEs, this translates to the availability of auto-completion features:

    Don't lose time searching for the exact name of the anchor in the file that is... where is it again? Let the autocompletion tool find them for you.
    <br>



### Identifiers: separating structure from content

Relying on the `attr_list` markdown extension, use identifiers instead of actual paths to point to specific anchors in the documentation:

```code
## Very important title with anchor and id {: #point-here }
```

```code
In another file: navigate to [this very important title](--point-here).
```

The plugin automatically rebuilds the appropriate addresses, considering various factors such as the source file  location, the target, the `use_directory_urls` option, ...


### Reduce dependencies on the files hierarchy

Identifiers still work after:
- Changing header content
- Moving sections from one file to another
- Renaming files
- Moving files

![move-deeper](http://frederic-zinelli.gitlab.io/mkdocs-addresses/assets/move-deeper.png)


### Provide [autocompletion helpers](http://frederic-zinelli.gitlab.io/mkdocs-addresses/autocompletion/) (_IDE dependent_)

_(Currently only available for VSC-like IDEs)_

* All snippets are automatically kept up to date while working on the documentation.
* They provide various markdown snippets, to get a quick and easy access to all the references defined in the documentation, and use them within the markdown code they are usual used for.

| Kind | Suggestion completion | Inserted markdown |
|:-|:-|:-|
| Doc identifier | `--point-here` | `--point-here` |
| Doc links | `Link.point-here` | `[link to some place in the docs](--point-here)` |
| Images in `assets/` (identifier) | `!!file_in_assets_jpg` | `!!file_in_assets_jpg` |
| Images in `assets/` | `Img.file_in_assets_jpg` | `![alt content](!!file_in_assets_jpg)` |
| Other files links | `++file_path_in_docs_html` | `++file_path_in_docs_html` |
| Other files links | `File.file_path_in_docs_html` | `[link to a file](++file_path_in_docs_html)` |
| External Links <sup>\*</sup> | `Ext.global_ref` | `[global_ref][global_ref]` |
| Code inclusions<sup>\*\*</sup> | `::md that_file_md` | `--<8-- "include/that_file.md"` |


\*: requires an [external_links_file](http://frederic-zinelli.gitlab.io/mkdocs-addresses/configuration/#mkdocs_addresses.config_plugin.PluginOptions.external_links_file) for global references is configured.

\*\*: requires the use of [inclusions](http://frederic-zinelli.gitlab.io/mkdocs-addresses/configuration/#mkdocs_addresses.config_plugin.PluginOptions.inclusions) directories.


![autocomplete](docs/assets/auto-completion-point-here.png)



### Tracking dead links or addresses in the docs

The plugin also explores the documentation and warns you if it finds invalid addresses or identifiers. This works for:

- Addresses in links
- Addresses of images
- Identifiers used by the plugin

![errors-example](http://frederic-zinelli.gitlab.io/mkdocs-addresses/assets/errors-summary.png)


### User handed configuration

A lot of [options](http://frederic-zinelli.gitlab.io/mkdocs-addresses/configuration/) are available for the user to fine tune the plugin's behavior.





## Installation

Install the package on your machine (or in your project if you are using a virtual env):

```
pip install mkdocs-addresses
```

Register the plugin in the `mkdocs.yml` file:

```yaml
plugins:
    - search            # To redeclare when plugins are added to mkdocs.yml
    - mkdocs-addresses
```

Configure the plugin (see below).




### Recommended `mkdocs.yml` configuration

See the [online documentation](http://frederic-zinelli.gitlab.io/mkdocs-addresses/#installation) for more details.

#### Markdown extensions

```yaml
markdown_extensions:
    - attr_list             # To define the identifiers in the markdown content
    - pymdownx.snippets:    # If you need inclusions code snippets
        check_paths: true
        auto_append: ["path_to_external_links_definition.md"]
        #               ^ see plugin's external_link_file configuration
```

#### Plugin configuration

```yaml
plugins:
    - search
    - mkdocs-addresses:
        - external_links_file: path_to_links_definition_if_any.md
        - inclusions:
            - location1_if_any
            - location2...
```

Note that the default configuration also implies the following choices:

```yaml
        - dump_snippets_file: .vscode/links.code-snippets
        - fail_fast: false
        - ignore_auto_headers: true
        - ide: vsc
```
So, if VSC isn't the utilized IDE, the [`ide`](http://frederic-zinelli.gitlab.io/mkdocs-addresses/configuration/#mkdocs_addresses.config_plugin.PluginOptions.ide) option should at the very least be modified.


#### When using mkdocs 1.5+

Significant enhancements in address verification logic (which was notoriously lacking in earlier versions...) have been added in `mkdocs 1.5+`. But the plugin does more work, and the identifiers it is utilizing are generating warnings in the console.

Hence, deactivate the default verification logic for mkdocs 1.5+:

```yaml
validation:
    absolute_links: ignore
    unrecognized_links: ignore
```


## Links

* [Project repository (GitLab)](https://gitlab.com/frederic-zinelli/mkdocs-addresses)
* [Full online documentation](http://frederic-zinelli.gitlab.io/mkdocs-addresses/)
* [The project on PyPI](https://pypi.org/project/mkdocs-addresses/)


## License

[Apache-2.0](https://www.tldrlegal.com/license/apache-license-2-0-apache-2-0)
Copyright © 2023 Zinelli Frédéric