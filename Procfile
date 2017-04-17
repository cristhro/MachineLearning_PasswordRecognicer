web gunicorn index:app

 <body>
        <!-- Top Navigation 
        <div class="codrops-top clearfix">
            <a class="codrops-icon codrops-icon-prev"  href="{{ url_for('entrenamiento') }}"><span>Entrenamiento</span></a>
            <span class="right"><a class="codrops-icon codrops-icon-drop"  href="{{ url_for('autenticacion') }}"><span>Autenticacion</span></a></span>
        </div>
        -->
        <div class="container">
            <div class="content">
                <div id="large-header" class="large-header">
                    <h1  class="main-title">{{ title }} <span href="{{ url_for('entrenamiento') }}" class="thin">{{ message }}</span></h1>
                    
                </div>

            {% block content %}{% endblock %}
            </div>
        </div>

        <!-- /container -->
        <script src="/static/js/demo-1.js"></script>

        {% block scripts %}{% endblock %}
    </body>