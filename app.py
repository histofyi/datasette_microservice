from flask import Flask, request, Response
import requests


app = Flask(__name__)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello_world(path):
    datasette_root = 'http://datasette.histo.fyi'
    if len(path) == 0:
        path = '/'
        title = 'Histo: data tables'
    else:
        print (request.full_path)
        path = request.full_path


    url = f"{datasette_root}{path}"
    data = requests.get(url)
    plausible_snippet ='<script defer data-domain="datasette.histo.fyi" src="https://plausible.io/js/script.js"></script>'
    logo_snippet = '<link href="https://static.histo.fyi/histo-32-color.png" rel="icon" type="image/png" />'
    google_fonts_snippet1 = '<link rel="preconnect" href="https://fonts.googleapis.com">'
    google_fonts_snippet2 = '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    google_fonts_snippet3 = '<link href="https://fonts.googleapis.com/css2?family=Courier+Prime:wght@400;700&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400&display=swap" rel="stylesheet">'
    footer_front_snippet = '<footer class="ft">A service from <a href="https://histo.fyi">histo.fyi</a> | '
    footer_end_snippet = '| Database version 0.0.1<br /><br /><div class="grant-container"><img src="/static/europe-flag-icon.svg" height="40" class="eu_flag"><span>&nbsp;This project has received funding from the European Union\'s Horizon 2020 research and innovation programme under the Marie Skłodowska-Curie grant agreement No 945405</span></div></footer>'
    content = data.text
    if 'text/html' in data.headers['Content-Type']:
        print ('html, adding in a few additional snippets')
        content = content.replace('href="/-/static/', 'href="/static/')
        content = content.replace('src="/-/static/', 'src="/static/')
        content = content.replace('<head>', f'<head>{plausible_snippet}\n{logo_snippet}\n{google_fonts_snippet1}\n{google_fonts_snippet2}\n{google_fonts_snippet3}\n')
        content = content.replace('<footer class="ft">', footer_front_snippet)
        content = content.replace('</footer>', footer_end_snippet)
        content = content.replace('&middot;','|')
        content = content.replace('<a href="/">home</a>', '<strong>Histo</strong>: <a href="/">data tables</a>')
        return content
    elif 'application/json' in data.headers['Content-Type']:
        #TODO: prod plausible
        return Response(content, mimetype='application/json')
    elif 'text/plain' in data.headers['Content-Type']:
        #TODO: prod plausible
        return Response(content, mimetype='text/csv')
    else:
        return content
