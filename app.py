from flask import Flask, render_template, redirect, url_for

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # Configuration for upload folder
    app.config['UPLOAD_FOLDER']

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.project import project_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(project_bp)

    return app

if __name__ == '__main__':
    app = create_app()

    @app.route('/')
    def index():
        return redirect(url_for('project.index'))

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

    app.run()
