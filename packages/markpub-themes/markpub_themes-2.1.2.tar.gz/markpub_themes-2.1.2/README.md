# markpub_themes

Management and use of themes with
[markpub](https://pypi.org/project/markpub), a markdown web publishing package.

## Installation

```shell
pip install markpub-themes
```  

Help information is available:  
```shell
markpub-themes -h
```  

## Available themes  
List the themes available for use:

```shell
markpub-themes list
```  

## Select a theme  
The default theme used by Markpub is named "dolce".  

To select another theme to use as the default:

```shell
markpub-themes activate
```  

## Clone a theme for customization  
A theme can be installed locally and customized.  
Cloning a theme (1) installs the HTML, JS, and CSS files in a Markpub initialized folder in the ".markpub/themes/" directory, and (2) sets the "theme" value in the Markpub config file: ".markpub/markpub.yaml".  

```shell
markpub-themes clone
```  


## Python usage  

```python
import markpub_themes

markpub_themes.list_themes()

markpub_themes.get_theme_path('dolce')
```

## License

MIT License - see LICENSE file for details.
