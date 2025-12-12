from __future__ import annotations

import os

from docutils.parsers.rst import directives

from docutils import nodes

from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.util import logging

from typing import Optional

from sphinx_metadata_figure import MetadataFigure
from sphinx.directives.patches import Figure

from sphinxcontrib.video import Video

logger = logging.getLogger(__name__)

YOUTUBE_OPTIONS = [
    "autoplay","cc_lang_pref","cc_load_policy","color","controls","disablekb","enablejsapi","end","fs","hl","iv_load_policy","list","listType","loop","modestbranding","origin","playlist","playsinline","rel","start","widget_referrer"
]

class iframe_node(nodes.raw):
    pass

def generate_style(width: Optional[str], height: Optional[str],aspectratio: Optional[str],stylediv: Optional[str]):

     styles = ''

     if width:
          styles += f'width: {width};'

     if height:
          styles += f'height: {height};'
     
     if aspectratio:
          styles += f'aspect-ratio: {aspectratio};'

     if stylediv:
         styles += stylediv

     return styles

class IframeDirective(SphinxDirective):
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
        'class': directives.class_option,
        "height": directives.unchanged,
        "width": directives.unchanged,
        "aspectratio": directives.unchanged,
        "stylediv": directives.unchanged,
        "styleframe": directives.unchanged,
        "divclass": directives.class_option,
        "iframe_loading": directives.unchanged,
    }

    def run(self) -> list[nodes.Node]:

        assert self.arguments[0] is not None

        # discriminate between mp4, webm, ogg and other urls for the video directive
        if self.name in ["video","video-figure"]:
            if self.arguments[0].lower().endswith('.mp4') or self.arguments[0].lower().endswith('.webm') or self.arguments[0].lower().endswith('.ogg'):
                video_directive = Video(
                    self.name,
                    self.arguments,
                    self.options,
                    self.content,
                    self.lineno,
                    self.content_offset,
                    self.block_text,
                    self.state,
                    self.state_machine,
                )
                return video_directive.run()
        # At this point we know we have to use the iframe, as it is not a video file or not a video directive
        iframe_html = generate_iframe_html(self)

        node = iframe_node(None, iframe_html, format="html")
        # paragraph_node = nodes.paragraph()
        # paragraph_node.insert(0, iframe_node)

        return [node]

def generate_iframe_html(source):

    loadmethod = source.options.get("iframe_loading",None)
    if loadmethod is None:
        loadmethod = source.state.document.settings.env.app.config.iframe_loading
    if loadmethod not in ['lazy','eager']:
        # throw a warning that the value is not correct and is set to defined default
        logger.warning(f"[sphinx-iframes] 'iframe_loading' option value '{loadmethod}' is not valid. Setting to '{source.state.document.settings.env.app.config.iframe_loading}'.")
        loadmethod = source.state.document.settings.env.app.config.iframe_loading

    div_class = source.options.get("divclass", None)
    if div_class is not None:
        div_class = " ".join(div_class) if isinstance(div_class, list) else str(div_class)
    else:
        div_class = ""
    iframe_class = source.options.get("class")

    if source.name in ["h5p","h5p-figure"]:
        base_class = "sphinx h5p blend"
        if iframe_class is not None:
            if "no-blend" in iframe_class:
                base_class = "sphinx h5p"        
    elif source.name in ["video","video-figure"]:
        base_class = "sphinx video no-blend"
        if iframe_class is not None:
            if "blend" in iframe_class and "not-blend" not in iframe_class:
                base_class = "sphinx video"
    else:
            base_class = "sphinx"

    if iframe_class is None:
        iframe_class = base_class
    elif isinstance(iframe_class, list):
        iframe_class = base_class+" "+" ".join(iframe_class)
    else:
        iframe_class = base_class+""+str(iframe_class)
    
    if source.name in ["h5p","h5p-figure"]:
        style = generate_style(
            None, None,"auto",None
        )
        check_style = style
    else:
        style = generate_style(
            source.options.get("width", None), source.options.get("height", None),source.options.get("aspectratio",None),source.options.get("stylediv",None)
        )
        check_style = generate_style(
            source.options.get("width", None), source.options.get("height", None),source.options.get("aspectratio",None),None
        )
    if style != '':
        style = 'style="%s"'%(style)
    if ('width' in check_style) or ('height' in check_style) or ('aspect-ratio' in check_style):
        add_user = True
    else:
        add_user = False
    frame_style = source.options.get("styleframe",None)
    if frame_style is not None:
        frame_style = 'style="%s"'%(frame_style)

    # load source and check for validity
    url = source.arguments[0]
    if 'youtube' in url:
        if 'watch?' in url:
            tail = url[1+url.find('?'):]
            list_index = tail.find('list=PL')
            if list_index>0: # so list found and not at the beginning
                # add a & before list if it is not present
                if tail[list_index]!='&':
                    tail = tail[:list_index] + '&' + tail[list_index:]
            video = ''
            options = []
            tail = tail.split('&')
            for combo in tail:
                opt = combo.split('=')
                if opt[0]=='v':
                    video = opt[1]
                elif opt[0]=='t':
                    options.insert(0,'start='+opt[1])
                elif opt[0] in YOUTUBE_OPTIONS:
                    options.append(combo)
            options = ';'.join(options)

            url = 'https://www.youtube.com/embed/'+video+'?'+options
        elif 'watch/' in url:
            url = url.replace('watch/','embed/')
    if 'youtu.be' in url:
        tail = url[1+url.find('?'):]
        list_index = tail.find('list=PL')
        if list_index>0: # so list found and not at the beginning
            # add a & before list if it is not present
            if tail[list_index]!='&':
                tail = tail[:list_index] + '&' + tail[list_index:]
        question_mark_index = url.find('?')
        if question_mark_index>=0:
            base_video = url[:question_mark_index]
        else:
            base_video = url
        base_video = base_video.replace('.be','be.com/embed')
        print(f"[sphinx-iframes] Converted youtu.be URL to {base_video}")
        options = []
        tail = tail.split('&')
        for combo in tail:
            opt = combo.split('=')
            if opt[0]=='v':
                video = opt[1]
            elif opt[0]=='t':
                options.insert(0,'start='+opt[1])
            elif opt[0] in YOUTUBE_OPTIONS:
                options.append(combo)
        options = ';'.join(options)

        url = base_video+'?'+options

    # Handle H5P URLs - add /embed if not present
    if source.name in ["h5p","h5p-figure"]:
        if '/embed' not in url and url.endswith('/'):
            url = url + 'embed'
        elif '/embed' not in url and not url.endswith('/'):
            url = url + '/embed'

    if source.name in ["video","video-figure"]:
        if add_user:
            iframe_html = '<div class="video-container user %s" %s>\n'%(div_class, style)
        else:
            iframe_html = '<div class="video-container %s" %s>\n'%(div_class, style)
        iframe_html += f"""
            <iframe class="{iframe_class}" {frame_style} src="{url}" allow="fullscreen *;autoplay *; geolocation *; microphone *; camera *; midi *; encrypted-media *" frameborder="0"></iframe>
        """
        iframe_html += '\n</div>'
    elif source.name in ["h5p","h5p-figure"]:
        if add_user:
            iframe_html = '<div class="iframe-container user %s" %s>\n'%(div_class, style)
        else:
            iframe_html = '<div class="iframe-container %s" %s>\n'%(div_class, style)
        iframe_html += f"""
            <iframe class="{iframe_class}" {frame_style} src="{url}" allow="fullscreen *;autoplay *; geolocation *; microphone *; camera *; midi *; encrypted-media *" frameborder="0"></iframe>
        """
        iframe_html += '\n</div>'
    else:
        if add_user:
            iframe_html = '<div class="iframe-container user %s" %s>\n'%(div_class, style)
        else:
            iframe_html = '<div class="iframe-container %s" %s>\n'%(div_class, style)
        iframe_html += f"""
            <iframe class="{iframe_class}" {frame_style} src="{url}" allow="fullscreen *;autoplay *; geolocation *; microphone *; camera *; midi *; encrypted-media *" frameborder="0"></iframe>
        """
        iframe_html += '\n</div>'

    return iframe_html
    
    
def include_js(app: Sphinx):
     
     if app.config.iframe_h5p_autoresize:
          app.add_js_file("h5p-resizer.js") # to support auto-width for h5p

     return

def setup(app: Sphinx):

    app.setup_extension('sphinxcontrib.video')
    app.setup_extension('sphinx_metadata_figure')

    app.add_directive("iframe", IframeDirective)
    app.add_directive("h5p", IframeDirective)
    app.add_directive("video", IframeDirective,override=True) # override any other video directive
    app.add_directive("iframe-figure", IframeFigure)
    app.add_directive("video-figure", IframeFigure)
    app.add_directive("h5p-figure", IframeFigure)

    app.add_config_value("iframe_h5p_autoresize",True,'env')
    app.add_config_value("iframe_loading","lazy",'env')
    app.connect('builder-inited',include_js)
    app.connect('config-inited',validate_config)

    app.add_config_value("iframe_blend",True,'env')
    app.add_config_value("iframe_saturation",1.5,'env')
    app.add_config_value("iframe_background","#ffffff",'env')
    app.add_config_value("iframe_width","calc(100% - 2.8rem)",'env')
    app.add_config_value("iframe_aspectratio","auto 2 / 1",'env')
    
    app.add_css_file('sphinx_iframe.css')

    app.connect("build-finished",write_css)
    app.connect("build-finished",write_js)

    return

def write_css(app: Sphinx,exc):
    # now set the CSS
    CSS_content = "div.video-container {\n\tbox-sizing: border-box;\n}\n\n"
    CSS_content += "div.video-container:not(.user) {\n\twidth: %s;\n\taspect-ratio: auto 16 / 9;\n}\n\n"%(app.config.iframe_width)
    CSS_content += "iframe.sphinx.video {\n\twidth: 100%;\n\theight: 100%;\n\tbox-sizing: border-box;\n}\n\n"
    CSS_content += "div.iframe-container {\n\tbox-sizing: border-box;\n}\n\n"
    CSS_content += "div.iframe-container:not(.user) {\n\twidth: %s;\n\taspect-ratio: %s;\n}\n\n"%(app.config.iframe_width,app.config.iframe_aspectratio)
    CSS_content += "div.iframe-container > iframe:not(.h5p) {\n\twidth: 100%;\n\theight: 100%;\n\tbox-sizing: border-box;\n}\n\n"
    
    # add blend or no-blend option if required
    if app.config.iframe_blend:
        CSS_content += "iframe.sphinx:not(.no-blend) {\n\tbackground: transparent;\n\tmix-blend-mode: darken;\n}\n\n" # blend all except no-blend
        CSS_content += "html[data-theme=dark] iframe.sphinx:not(.no-blend) {\n\tfilter: invert(1) hue-rotate(180deg) saturate(%s);\n\tbackground: transparent;\n\tmix-blend-mode: lighten;\n}\n\n"%(app.config.iframe_saturation) # blend all except no-blend
        CSS_content += "iframe.sphinx.no-blend:not(.video) {\n\tbackground: %s;\n\tborder-radius: .25rem;\n}\n\n"%(app.config.iframe_background)
        CSS_content += "iframe.sphinx.no-blend.video {\n\tbackground: transparent;\n\tborder-radius: .25rem;\n}\n"
    else:
        CSS_content += "iframe.sphinx.blend {\n\tbackground: transparent;\n\tmix-blend-mode: darken;\n}\n\n" # blend none except blend
        CSS_content += "html[data-theme=dark] iframe.sphinx.blend {\n\tfilter: invert(1) hue-rotate(180deg) saturate(%s);\n\tbackground: transparent;\n\tmix-blend-mode: lighten;\n}\n\n"%(app.config.iframe_saturation) # blend none except blend
        CSS_content += "iframe.sphinx:not(.blend):not(.video) {\n\tbackground: %s;\n\tborder-radius: .25rem;\n}\n\n"%(app.config.iframe_background)
        CSS_content += "iframe.sphinx:not(.blend).video {\n\tbackground: transparent;\n\tborder-radius: .25rem;\n}\n\n"
    
    # write the css file
    staticdir = os.path.join(app.builder.outdir, '_static')
    filename = os.path.join(staticdir,'sphinx_iframe.css')
    with open(filename,"w") as css:
        css.write(CSS_content)

    return

def write_js(app: Sphinx,exc):
    if app.config.iframe_h5p_autoresize:
        JS_content = """
            // H5P iframe Resizer
            (function () {
            if (!window.postMessage || !window.addEventListener || window.h5pResizerInitialized) {
                return; // Not supported
            }
            window.h5pResizerInitialized = true;

            // Map actions to handlers
            var actionHandlers = {};

            /**
            * Prepare iframe resize.
            *
            * @private
            * @param {Object} iframe Element
            * @param {Object} data Payload
            * @param {Function} respond Send a response to the iframe
            */
            actionHandlers.hello = function (iframe, data, respond) {
                // Make iframe responsive
                iframe.style.width = '100%';

                // Bugfix for Chrome: Force update of iframe width. If this is not done the
                // document size may not be updated before the content resizes.
                iframe.getBoundingClientRect();

                // Tell iframe that it needs to resize when our window resizes
                var resize = function () {
                if (iframe.contentWindow) {
                    // Limit resize calls to avoid flickering
                    respond('resize');
                }
                else {
                    // Frame is gone, unregister.
                    window.removeEventListener('resize', resize);
                }
                };
                window.addEventListener('resize', resize, false);

                // Respond to let the iframe know we can resize it
                respond('hello');
            };

            /**
            * Prepare iframe resize.
            *
            * @private
            * @param {Object} iframe Element
            * @param {Object} data Payload
            * @param {Function} respond Send a response to the iframe
            */
            actionHandlers.prepareResize = function (iframe, data, respond) {
                // Do not resize unless page and scrolling differs
                if (iframe.clientHeight !== data.scrollHeight ||
                    data.scrollHeight !== data.clientHeight) {

                // Reset iframe height, in case content has shrinked.
                iframe.style.height = data.clientHeight + 'px';
                respond('resizePrepared');
                }
            };

            /**
            * Resize parent and iframe to desired height.
            *
            * @private
            * @param {Object} iframe Element
            * @param {Object} data Payload
            * @param {Function} respond Send a response to the iframe
            */
            actionHandlers.resize = function (iframe, data) {
                // Resize iframe so all content is visible. Use scrollHeight to make sure we get everything
                iframe.style.height = data.scrollHeight + 'px';
            };

            /**
            * Keyup event handler. Exits full screen on escape.
            *
            * @param {Event} event
            */
            var escape = function (event) {
                if (event.keyCode === 27) {
                exitFullScreen();
                }
            };

            // Listen for messages from iframes
            window.addEventListener('message', function receiveMessage(event) {
                if (event.data.context !== 'h5p') {
                return; // Only handle h5p requests.
                }

                // Find out who sent the message
                var iframe, iframes = document.getElementsByTagName('iframe');
                for (var i = 0; i < iframes.length; i++) {
                if (iframes[i].contentWindow === event.source) {
                    iframe = iframes[i];
                    break;
                }
                }

                if (!iframe) {
                return; // Cannot find sender
                }

                // Find action handler handler
                if (actionHandlers[event.data.action]) {
                actionHandlers[event.data.action](iframe, event.data, function respond(action, data) {
                    if (data === undefined) {
                    data = {};
                    }
                    data.action = action;
                    data.context = 'h5p';
                    event.source.postMessage(data, event.origin);
                });
                }
            }, false);

            // Let h5p iframes know we're ready!
            var iframes = document.getElementsByTagName('iframe');
            var ready = {
                context: 'h5p',
                action: 'ready'
            };
            for (var i = 0; i < iframes.length; i++) {
                if (iframes[i].src.indexOf('h5p') !== -1) {
                iframes[i].contentWindow.postMessage(ready, '*');
                }
            }

            })();
            """
        # write the css file
        staticdir = os.path.join(app.builder.outdir, '_static')
        filename = os.path.join(staticdir,'h5p-resizer.js')
        with open(filename,"w") as js:
            js.write(JS_content)

class IframeFigure(MetadataFigure):
    option_spec = MetadataFigure.option_spec.copy()
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec.update(
        {
            'class': directives.class_option,
            "height": directives.unchanged,
            "width": directives.unchanged,
            "aspectratio": directives.unchanged,
            "stylediv": directives.unchanged,
            "styleframe": directives.unchanged,
            "iframe_loading": directives.unchanged
        }
    )
    
    def run(self):
        label = self.options.pop('label', None)
        if label is not None:
            self.options.set('name', label)
        # Access environment/config for whether to use metadata figure
        env = getattr(self.state.document.settings, 'env', None)
        config = getattr(env.app, 'config', None) if env else None
        metadata_settings = getattr(config, 'metadata_figure_settings', {}) if config else {}
        style_settings = metadata_settings.get('style', {})
        placement = self.options.get('placement', style_settings.get('placement', 'hide'))
        if placement == 'caption':
            self.options["placement"] = 'caption'
            (figure_node,) = MetadataFigure.run(self)
            other_nodes = None
        elif placement == 'admonition':
            self.options["placement"] = 'admonition'
            figure_nodes = MetadataFigure.run(self)
            figure_node = figure_nodes[0]
            other_nodes = figure_nodes[1]
        elif placement == 'margin':
            self.options["placement"] = 'margin'
            figure_nodes = MetadataFigure.run(self)
            figure_node = figure_nodes[1]
            other_nodes = figure_nodes[0]
        else:
            # Just create a normal figure node without metadata
            (figure_node,) = Figure.run(self)
            other_nodes = None

        iframe_html = generate_iframe_html(self)
        node = iframe_node(None, iframe_html, format="html")
        figure_node[0] = node

        if self.options.get('placement', style_settings.get('placement', 'hide')) == 'caption':
            return [figure_node]
        elif self.options.get('placement', style_settings.get('placement', 'hide')) == 'admonition':
            return [figure_node] + [other_nodes]
        elif self.options.get('placement', style_settings.get('placement', 'hide')) == 'margin':
            return [other_nodes] + [figure_node]
        else:
            return [figure_node]

def validate_config(app: Sphinx,config):
    if config.iframe_loading not in ['lazy','eager']:
        logger.warning(f"[sphinx-iframes] 'iframe_loading' config value '{config.iframe_loading}' is not valid. Setting to 'lazy'.")
        config.iframe_loading = 'lazy'
    return
