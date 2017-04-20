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











     <script src="/static/js/selectFx.js"></script>
        <script src="/static/js/classie.js"></script>
    
    </head>
        <body class="color-2">
        <div class="container fondo">
            <!-- Top Navigation -->
            <div id="large-header" class="large-header">
                    <h1  class="main-title">{{ title }} <span href="{{ url_for('entrenamiento') }}" class="thin">{{ message }}</span></h1>
                    
            </div>
            <div class="content ">
                
            <section>
                <select class="cs-select cs-skin-underline">
                    <option value="" disabled selected>Choose a Bouquet</option>
                    <option value="1">Gardenia + Daisies</option>
                    <option value="2">Roses + Stephanotis</option>
                    <option value="3">Peony + Gerbera</option>
                    <option value="4">Orchid + Limonium</option>
                    <option value="5">Iris + Omithoalum</option>
                </select>
            </section>
        </div><!-- /container -->
        <script>
            (function() {
                [].slice.call( document.querySelectorAll( 'select.cs-select' ) ).forEach( function(el) {    
                    new SelectFx(el);
                } );
            })();
        </script>
    </body>