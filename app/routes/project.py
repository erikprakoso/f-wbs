from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from werkzeug.utils import secure_filename
import os
from app import db, create_app
from app.models.project import Project

project_bp = Blueprint('project', __name__)


def convert_size(size_bytes):
    # Konversi ukuran bytes menjadi KB atau MB
    KB = 1024
    MB = KB * 1024

    if size_bytes >= MB:
        size = "{:.2f} MB".format(size_bytes / MB)
    elif size_bytes >= KB:
        size = "{:.2f} KB".format(size_bytes / KB)
    else:
        size = "{:.2f} bytes".format(size_bytes)

    return size

@project_bp.route('/')
def index():
    if 'email' not in session:
        return redirect(url_for('auth.login'))

    projects = Project.query.all()
    return render_template('project/index.html', projects=projects)


@project_bp.route('/project/create')
def create():
    if 'email' not in session:
        return redirect(url_for('auth.login'))
    
    return render_template('project/_create.html')


@project_bp.route('/project/detail/<int:id>')
def detail(id):
    if 'email' not in session:
        return redirect(url_for('auth.login'))

    project = Project.query.get(id)
    return render_template('project/_detail.html', project=project)


@project_bp.route('/project/edit/<int:id>')
def edit(id):
    if 'email' not in session:
        return redirect(url_for('auth.login'))

    project = Project.query.get(id)
    return render_template('project/_edit.html', project=project)


@project_bp.route('/project/store', methods=['POST'])
def store():
    app = create_app()  # Get access to the app object

    # Get form data
    name = request.form['inputName']
    type = request.form['inputType']
    location = request.form['inputLocation']
    start_date = request.form['inputStartDate']
    end_date = request.form['inputEndDate']
    revit_link = request.form['inputLinkRevit']

    # Get uploaded files
    revit_file = request.files['inputUploadRevit']
    excel_file = request.files['inputUploadExcel']
    photo_file = request.files['inputUploadPhoto']

    # Cek ukuran file
    file_size_revit = len(revit_file.read())
    file_size_excel = len(excel_file.read())
    file_size_photo = len(photo_file.read())

    # Kembali ke awal file
    revit_file.seek(0)
    excel_file.seek(0)
    photo_file.seek(0)

    # Konversi ukuran file ke KB atau MB
    revit_file_size_formatted = convert_size(file_size_revit)
    excel_file_size_formatted = convert_size(file_size_excel)
    photo_file_size_formatted = convert_size(file_size_photo)

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
        photo_file=photo_filename,
        revit_file_size=revit_file_size_formatted,
        excel_file_size=excel_file_size_formatted,
        photo_file_size=photo_file_size_formatted,
        revit_link=revit_link,
    )

    # Save project to the database
    db.session.add(project)
    db.session.commit()

    return jsonify({'message': 'Data stored successfully.'})


@project_bp.route('/project/delete/<int:id>', methods=['POST'])
def delete_project(id):
    app = create_app()  # Get access to the app object

    project = Project.query.get(id)

    if project:
        # Hapus file upload dari sistem file jika file ada
        if project.excel_file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], project.excel_file)
            if os.path.exists(file_path):
                os.remove(file_path)

        if project.revit_file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], project.revit_file)
            if os.path.exists(file_path):
                os.remove(file_path)

        if project.photo_file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], project.photo_file)
            if os.path.exists(file_path):
                os.remove(file_path)

        # Hapus data proyek dari database
        db.session.delete(project)
        db.session.commit()

        return jsonify({'message': 'Data deleted successfully.'})
    else:
        return jsonify({'message': 'Project not found.'}), 404
    

@project_bp.route('/project/update/<int:id>', methods=['POST'])
def update(id):
    app = create_app()

    project = Project.query.get(id)

    if project:
        # Get form data
        name = request.form['inputName']
        type = request.form['inputType']
        location = request.form['inputLocation']
        start_date = request.form['inputStartDate']
        end_date = request.form['inputEndDate']
        revit_link = request.form['inputLinkRevit']

        # Get uploaded files
        revit_file = request.files['inputUploadRevit']
        excel_file = request.files['inputUploadExcel']
        photo_file = request.files['inputUploadPhoto']

        if revit_file.filename != '':
            # Hapus file lama dari sistem file
            if project.revit_file:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], project.revit_file)
                if os.path.exists(file_path):
                    os.remove(file_path)

            # Cek ukuran file
            file_size_revit = len(revit_file.read())

            # Kembali ke awal file
            revit_file.seek(0)

            # Konversi ukuran file ke KB atau MB
            revit_file_size_formatted = convert_size(file_size_revit)

            # Get file extensions
            revit_ext = os.path.splitext(revit_file.filename)[1]

            # Remove existing extensions
            revit_filename_base = os.path.splitext(revit_file.filename)[0]

            # Generate secure filenames with proper extensions
            revit_filename = secure_filename(revit_filename_base) + revit_ext

            # Save file to the desired folder
            revit_file.save(os.path.join(app.config['UPLOAD_FOLDER'], revit_filename))

            # Update project object
            project.revit_file = revit_filename
            project.revit_file_size = revit_file_size_formatted

        if excel_file.filename != '':
            # Hapus file lama dari sistem file
            if project.excel_file:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], project.excel_file)
                if os.path.exists(file_path):
                    os.remove(file_path)

            # Cek ukuran file
            file_size_excel = len(excel_file.read())

            # Kembali ke awal file
            excel_file.seek(0)

            # Konversi ukuran file ke KB atau MB
            excel_file_size_formatted = convert_size(file_size_excel)

            # Get file extensions
            excel_ext = os.path.splitext(excel_file.filename)[1]

            # Remove existing extensions
            excel_filename_base = os.path.splitext(excel_file.filename)[0]

            # Generate secure filenames with proper extensions
            excel_filename = secure_filename(excel_filename_base) + excel_ext

            # Save file to the desired folder
            excel_file.save(os.path.join(app.config['UPLOAD_FOLDER'], excel_filename))

            # Update project object
            project.excel_file = excel_filename
            project.excel_file_size = excel_file_size_formatted

        if photo_file.filename != '':
            # Hapus file lama dari sistem file
            if project.photo_file:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], project.photo_file)
                if os.path.exists(file_path):
                    os.remove(file_path)

            # Cek ukuran file
            file_size_photo = len(photo_file.read())

            # Kembali ke awal file
            photo_file.seek(0)

            # Konversi ukuran file ke KB atau MB
            photo_file_size_formatted = convert_size(file_size_photo)

            # Get file extensions
            photo_ext = os.path.splitext(photo_file.filename)[1]

            # Remove existing extensions
            photo_filename_base = os.path.splitext(photo_file.filename)[0]

            # Generate secure filenames with proper extensions
            photo_filename = secure_filename(photo_filename_base) + photo_ext

            # Save file to the desired folder
            photo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))

            # Update project object
            project.photo_file = photo_filename
            project.photo_file_size = photo_file_size_formatted

        # Update project object
        project.name = name
        project.type = type
        project.location = location
        project.start_date = start_date
        project.end_date = end_date
        project.revit_link = revit_link

        # Commit to database
        db.session.commit()

        return jsonify({'message': 'Data updated successfully.'})
    else:
        return jsonify({'message': 'Project not found.'}), 404