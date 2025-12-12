from django.conf import settings
from django.http import HttpResponse
from importlib.metadata import version


def index(request):
    interfaz_name = getattr(settings, 'INTERFAZ_NAME')
    url_doc = getattr(settings, 'URL_DOCUMENTATION', '')
    if interfaz_name: interfaz_name = f'<i>{interfaz_name}</i>'

    isapilib_version = version("isapilib")

    return HttpResponse(f'''
        <style>
            * {{
                margin: 0;
                padding: 0;
                font-family: 'Roboto', sans-serif;
                color: #dfe2e6;
            }}

            body {{
                background-image: radial-gradient(circle, #004b75, #001c26);
                display: flex;
            }}

            div {{
                margin: auto;
                display: flex;
                font-size: 10vw;
                user-select: none;
                text-align: center;
                flex-direction: column;
            }}

            a {{
                opacity: 0.8;
                font-size: 1vw;
                text-decoration: none;
                transition: all 0.3s ease-in-out;
            }}

            a:hover {{
                transform: scale(1.3);
            }}

            i {{
                font-size: 30%;
                margin-bottom: 1.5vh;
            }}

            .version {{
                position: absolute;
                font-style: normal;
                font-size: 15%;
                opacity: 20%;
                margin: 1vw;
                bottom: 0;
                right: 0;
            }}
        </style>

        <div>
            <p>Intelisis</p>
            {interfaz_name}
            {f'<a href="{url_doc}">Documentation</a>' if url_doc != '' else ''}
            <i class="version">Version {isapilib_version}</i>
        </div>
    ''')
