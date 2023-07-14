from flask import Blueprint, render_template, session, redirect, url_for, request
from flask import jsonify
from werkzeug.utils import secure_filename
import os
from app import db, create_app
from app.models.project import Project
from app.models.sheet_name import SheetName

project_bp = Blueprint('project', __name__)


@project_bp.route('/')
def index():
    if 'email' not in session:
        return redirect(url_for('auth.login'))

    projects = Project.query.all()
    return render_template('project/index.html', projects=projects)


@project_bp.route('/create')
def create():
    return render_template('project/_create.html')

@project_bp.route('/detail/<int:id>')
def detail(id):
    if 'email' not in session:
        return redirect(url_for('auth.login'))

    project = Project.query.get(id)
    return render_template('project/_detail.html', project=project)

@project_bp.route('/edit/<int:id>')
def edit(id):
    if 'email' not in session:
        return redirect(url_for('auth.login'))

    project = Project.query.get(id)
    return render_template('project/_edit.html', project=project)

@project_bp.route('/delete/<int:id>')
def delete(id):
    if 'email' not in session:
        return redirect(url_for('auth.login'))

    project = Project.query.get(id)
    return render_template('project/_delete.html', project=project)


@project_bp.route('/project/store', methods=['POST'])
def store():
    app = create_app()  # Get access to the app object

    # Get form data
    name = request.form['inputName']
    type = request.form['inputType']
    location = request.form['inputLocation']
    start_date = request.form['inputStartDate']
    end_date = request.form['inputEndDate']
    sheet_names = request.form.getlist('inputSheetName[]')

    # Get uploaded files
    revit_file = request.files['inputUploadRevit']
    excel_file = request.files['inputUploadExcel']
    photo_file = request.files['inputUploadPhoto']

    # Get file extensions
    revit_ext = os.path.splitext(revit_file.filename)[1]
    excel_ext = os.path.splitext(excel_file.filename)[1]
    photo_ext = os.path.splitext(photo_file.filename)[1]

    # Remove existing extensions
    revit_filename_base = os.path.splitext(revit_file.filename)[0]
    excel_filename_base = os.path.splitext(excel_file.filename)[0]
    photo_filename_base = os.path.splitext(photo_file.filename)[0]

    # Generate secure filenames with proper extensions
    revit_filename = secure_filename(revit_filename_base) + revit_ext
    excel_filename = secure_filename(excel_filename_base) + excel_ext
    photo_filename = secure_filename(photo_filename_base) + photo_ext

    # Save files to the desired folder
    revit_file.save(os.path.join(app.config['UPLOAD_FOLDER'], revit_filename))
    excel_file.save(os.path.join(app.config['UPLOAD_FOLDER'], excel_filename))
    photo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))

    # Create a new project object
    project = Project(
        name=name,
        type=type,
        location=location,
        start_date=start_date,
        end_date=end_date,
        revit_file=revit_filename,
        excel_file=excel_filename,
        photo_file=photo_filename
    )

    # Save project to the database
    db.session.add(project)
    db.session.commit()

    # Create sheet_name objects and associate them with the project
    for sheet_name in sheet_names:
        sheet = SheetName(name=sheet_name, project=project)
        db.session.add(sheet)

    db.session.commit()

    return jsonify({'message': 'Data stored successfully.'})
