from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from werkzeug.utils import secure_filename
import os
from app import db, create_app
from app.models.project import Project
from app.models.sheet_name import SheetName
from app.models.wbs_header import WbsHeader
from app.models.wbs_detail import WbsDetail
from app.models.wbs_item import WbsItem
from app.models.wbs_header_project import WbsHeaderProject
from app.models.wbs_detail_project import WbsDetailProject
from app.models.wbs_item_project import WbsItemProject
import pandas as pd
from sqlalchemy import and_, asc
from datetime import datetime

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
    headers = WbsHeaderProject.query.filter(WbsHeaderProject.project_id == id).order_by(asc(WbsHeaderProject.created_at)).all()
    return render_template('project/_detail.html', project=project, headers=headers)

@project_bp.route('/project/<int:id>/wbs/<int:header_id>/detail')
def wbs_detail(id, header_id):
    if 'email' not in session:
        return redirect(url_for('auth.login'))

    project = Project.query.get(id)
    header = WbsHeaderProject.query.get(header_id)
    details = WbsDetailProject.query.filter(WbsDetailProject.wbs_header_project_id == header.id).all()
    
    for detail in details:
        items = WbsItemProject.query.filter(WbsItemProject.wbs_detail_project_id == detail.id).all()
        
        detail_items = []  # List to hold the items for the current detail
        for item in items:
            item_data = {
                'id': item.id,
                'name': item.name,
                'created_at': item.created_at,
                'updated_at': item.updated_at,
                # Add other item properties as needed
            }
            detail_items.append(item_data)
        
        detail.items = detail_items  # Assign the list of items to the detail

    return render_template('project/wbs/_detail.html', project=project, header=header, details=details)


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

    # Get the full path of the uploaded Excel file
    excel_file_full_path = os.path.join(app.config['UPLOAD_FOLDER'], excel_filename)

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

    # Access the ID of the newly inserted project
    project_id = project.id

    wbs = store_multiple_sheet(project_id, excel_file_full_path)

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

            update_multiple_sheet(id, excel_file)

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
    

def store_multiple_sheet(id, excel_file):
    print('excel_file', excel_file)
    print('id', id)
    # get all data from sheet name
    sheets = SheetName.query.all()

    # create empty list
    sheet_names = []

    # iterate through the sheets and append their names to sheet_names
    for sheet in sheets:
        sheet_names.append(sheet.name)

    # Initialize a set to store the unique desired values
    desired_values = set()

    print(sheet_names)

    for sheet_name in sheet_names:
        # Read the XLSX file, skipping the first row (header)
        df = pd.read_excel(excel_file, sheet_name=sheet_name, skiprows=2)

        # Convert DataFrame to a string with ~ delimiter
        df_string = df.to_csv(sep='~', index=False)

        # Save the string to a TXT file
        with open('output.txt', 'w') as txt_file:
            txt_file.write(df_string)

        # Read the TXT file and get the contents
        with open('output.txt', 'r') as txt_file:
            file_contents = txt_file.read()

        # Split the contents into lines
        lines = file_contents.split('\n')

        # Exclude any empty lines
        lines = [line for line in lines if line]

        for line in lines:
            rows = line.split('~')
            if len(rows) >= 3:
                value = rows[2]  # Access the value at index 2
                dimension = value.split(': ')[-1]  # Extract the dimension from the value
                desired_values.add(dimension)

        print(desired_values)
        for value in desired_values:
            print(value)
            header = WbsHeader.query.filter(WbsHeader.name.ilike(value.upper())).first()
            if header:
                print('header', header.id)
                print('header', header.name)
                
                get_project_header = WbsHeaderProject.query.filter(and_(WbsHeaderProject.name.ilike(header.name), WbsHeaderProject.project_id == id)).first()
                if get_project_header:
                    print('get_project_header', get_project_header.id)
                    print('get_project_header', get_project_header.name)
                else:
                    insert_project_header = WbsHeaderProject(
                        name=header.name,
                        project_id=id
                    )
                    db.session.add(insert_project_header)
                    db.session.commit()

                    new_project_header_id = insert_project_header.id
                    print('new_project_header_id', new_project_header_id)

                    details = WbsDetail.query.filter(WbsDetail.wbs_header_id == header.id).all()
                    for detail in details:
                        print('detail', detail.id)
                        print('detail', detail.name)
                        insert_project_detail = WbsDetailProject(
                            name=detail.name,
                            wbs_header_project_id=new_project_header_id
                        )
                        db.session.add(insert_project_detail)
                        db.session.commit()

                        new_project_detail_id = insert_project_detail.id
                        print('new_project_detail_id', new_project_detail_id)

                        items = WbsItem.query.filter(WbsItem.wbs_detail_id == detail.id).all()
                        for item in items:
                            print('item', item.id)
                            print('item', item.name)
                            insert_project_item = WbsItemProject(
                                name=item.name,
                                wbs_detail_project_id=new_project_detail_id
                            )
                            db.session.add(insert_project_item)
                            db.session.commit()

            else:
                detail = WbsDetail.query.filter(WbsDetail.name.ilike(value.upper())).first()
                if detail:
                    print('detail', detail.id)
                    print('detail', detail.name)
                    print('detail', detail.wbs_header_id)

                    get_header = WbsHeader.query.filter(WbsHeader.id == detail.wbs_header_id).first()
                    print('get_header', get_header.id)
                    print('get_header', get_header.name)

                    # Use and_ to combine the filter conditions for name and project_id
                    get_project_header = WbsHeaderProject.query.filter(and_(WbsHeaderProject.name.ilike(get_header.name), WbsHeaderProject.project_id == id)).first()
                    if get_project_header:
                        print('get_project_header', get_project_header.id)
                        print('get_project_header', get_project_header.name)
                    else:
                        insert_project_header = WbsHeaderProject(
                            name=get_header.name,
                            project_id=id
                        )
                        db.session.add(insert_project_header)
                        db.session.commit()

                        new_project_header_id = insert_project_header.id
                        print('new_project_header_id', new_project_header_id)

                        details = WbsDetail.query.filter(WbsDetail.wbs_header_id == get_header.id).all()
                        for detail in details:
                            print('detail', detail.id)
                            print('detail', detail.name)
                            insert_project_detail = WbsDetailProject(
                                name=detail.name,
                                wbs_header_project_id=new_project_header_id
                            )
                            db.session.add(insert_project_detail)
                            db.session.commit()

                            new_project_detail_id = insert_project_detail.id
                            print('new_project_detail_id', new_project_detail_id)

                            items = WbsItem.query.filter(WbsItem.wbs_detail_id == detail.id).all()
                            for item in items:
                                print('item', item.id)
                                print('item', item.name)
                                insert_project_item = WbsItemProject(
                                    name=item.name,
                                    wbs_detail_project_id=new_project_detail_id
                                )
                                db.session.add(insert_project_item)
                                db.session.commit()
                else:
                    print('Not found')

    return desired_values



def update_multiple_sheet(id, excel_file):
    print('excel_file', excel_file)
    print('id', id)
    # get all data from sheet name
    sheets = SheetName.query.all()

    # create empty list
    sheet_names = []

    # iterate through the sheets and append their names to sheet_names
    for sheet in sheets:
        sheet_names.append(sheet.name)

    # Initialize a set to store the unique desired values
    desired_values = set()

    print(sheet_names)

    for sheet_name in sheet_names:
        # Read the XLSX file, skipping the first row (header)
        df = pd.read_excel(excel_file, sheet_name=sheet_name, skiprows=2)

        # Convert DataFrame to a string with ~ delimiter
        df_string = df.to_csv(sep='~', index=False)

        # Save the string to a TXT file
        with open('output.txt', 'w') as txt_file:
            txt_file.write(df_string)

        # Read the TXT file and get the contents
        with open('output.txt', 'r') as txt_file:
            file_contents = txt_file.read()

        # Split the contents into lines
        lines = file_contents.split('\n')

        # Exclude any empty lines
        lines = [line for line in lines if line]

        for line in lines:
            rows = line.split('~')
            if len(rows) >= 3:
                value = rows[2]  # Access the value at index 2
                dimension = value.split(': ')[-1]  # Extract the dimension from the value
                desired_values.add(dimension)

        print(desired_values)
        for value in desired_values:
            print(value)
            header = WbsHeader.query.filter(WbsHeader.name.ilike(value.upper())).first()
            if header:
                print('header', header.id)
                print('header', header.name)
                
                get_project_header = WbsHeaderProject.query.filter(and_(WbsHeaderProject.name.ilike(header.name), WbsHeaderProject.project_id == id)).first()
                if get_project_header:
                    print('get_project_header', get_project_header.id)
                    print('get_project_header', get_project_header.name)
                else:
                    insert_project_header = WbsHeaderProject(
                        name=header.name,
                        project_id=id
                    )
                    db.session.add(insert_project_header)
                    db.session.commit()

                    new_project_header_id = insert_project_header.id
                    print('new_project_header_id', new_project_header_id)

                    details = WbsDetail.query.filter(WbsDetail.wbs_header_id == header.id).all()
                    for detail in details:
                        print('detail', detail.id)
                        print('detail', detail.name)
                        insert_project_detail = WbsDetailProject(
                            name=detail.name,
                            wbs_header_project_id=new_project_header_id
                        )
                        db.session.add(insert_project_detail)
                        db.session.commit()

                        new_project_detail_id = insert_project_detail.id
                        print('new_project_detail_id', new_project_detail_id)

                        items = WbsItem.query.filter(WbsItem.wbs_detail_id == detail.id).all()
                        for item in items:
                            print('item', item.id)
                            print('item', item.name)
                            insert_project_item = WbsItemProject(
                                name=item.name,
                                wbs_detail_project_id=new_project_detail_id
                            )
                            db.session.add(insert_project_item)
                            db.session.commit()

            else:
                detail = WbsDetail.query.filter(WbsDetail.name.ilike(value.upper())).first()
                if detail:
                    print('detail', detail.id)
                    print('detail', detail.name)
                    print('detail', detail.wbs_header_id)

                    get_header = WbsHeader.query.filter(WbsHeader.id == detail.wbs_header_id).first()
                    print('get_header', get_header.id)
                    print('get_header', get_header.name)

                    # Use and_ to combine the filter conditions for name and project_id
                    get_project_header = WbsHeaderProject.query.filter(and_(WbsHeaderProject.name.ilike(get_header.name), WbsHeaderProject.project_id == id)).first()
                    if get_project_header:
                        print('get_project_header', get_project_header.id)
                        print('get_project_header', get_project_header.name)
                    else:
                        insert_project_header = WbsHeaderProject(
                            name=get_header.name,
                            project_id=id
                        )
                        db.session.add(insert_project_header)
                        db.session.commit()

                        new_project_header_id = insert_project_header.id
                        print('new_project_header_id', new_project_header_id)

                        details = WbsDetail.query.filter(WbsDetail.wbs_header_id == get_header.id).all()
                        for detail in details:
                            print('detail', detail.id)
                            print('detail', detail.name)
                            insert_project_detail = WbsDetailProject(
                                name=detail.name,
                                wbs_header_project_id=new_project_header_id
                            )
                            db.session.add(insert_project_detail)
                            db.session.commit()

                            new_project_detail_id = insert_project_detail.id
                            print('new_project_detail_id', new_project_detail_id)

                            items = WbsItem.query.filter(WbsItem.wbs_detail_id == detail.id).all()
                            for item in items:
                                print('item', item.id)
                                print('item', item.name)
                                insert_project_item = WbsItemProject(
                                    name=item.name,
                                    wbs_detail_project_id=new_project_detail_id
                                )
                                db.session.add(insert_project_item)
                                db.session.commit()
                else:
                    print('Not found')

    return desired_values


@project_bp.route('/project/<int:id>/wbs/store', methods=['POST'])
def wbs_store(id):
    if 'email' not in session:
        return redirect(url_for('auth.login'))

    wbs = WbsHeaderProject()
    wbs.name = request.form['wbs_name']
    wbs.project_id = id
    db.session.add(wbs)
    db.session.commit()

    return redirect(url_for('project.detail', id=id))


@project_bp.route('/project/wbs/<int:id>/delete', methods=['POST'])
def wbs_delete(id):
    wbs = WbsHeaderProject.query.get(id)
    db.session.delete(wbs)
    db.session.commit()

    return jsonify({'message': 'Data deleted successfully.'})


@project_bp.route('/project/wbs/<int:id>/update', methods=['POST'])
def wbs_update(id):
    # Get the WBS name from the form data
    updated_name = request.form['wbs_name']
    created_at_str = request.form['wbs_created_at']
    print('created_at_str', created_at_str)
    updated_at_str = request.form['wbs_updated_at']
    print('updated_at_str', updated_at_str)

    created_at = None
    updated_at = None

    if created_at_str and created_at_str.strip():
        created_at = datetime.strptime(created_at_str, '%Y-%m-%d')

    if updated_at_str and updated_at_str.strip():
        updated_at = datetime.strptime(updated_at_str, '%Y-%m-%d')

    # Find the WBS by ID and update its name
    wbs = WbsHeaderProject.query.get(id)
    if wbs:
        wbs.name = updated_name
        wbs.created_at = created_at
        wbs.updated_at = updated_at
        db.session.commit()
        return redirect(url_for('project.detail', id=wbs.project_id))
    else:
        return jsonify({'message': 'WBS not found.'}), 404
    

@project_bp.route('/project/<int:id>/wbs/<int:header_id>/header/store', methods=['POST'])
def wbs_detail_store(id, header_id):
    if 'email' not in session:
        return redirect(url_for('auth.login'))

    wbs_detail = WbsDetailProject()
    wbs_detail.name = request.form['wbs_detail_name']
    wbs_detail.wbs_header_project_id = header_id
    db.session.add(wbs_detail)
    db.session.commit()

    return redirect(url_for('project.wbs_detail', id=id, header_id=header_id))


@project_bp.route('/project/wbs/detail/<int:id>/delete', methods=['POST'])
def wbs_detail_delete(id):
    wbs_detail = WbsDetailProject.query.get(id)
    db.session.delete(wbs_detail)
    db.session.commit()

    return jsonify({'message': 'Data deleted successfully.'})


@project_bp.route('/project/<int:id>/wbs/<int:header_id>/header/<int:detail_id>/detail/update', methods=['POST'])
def wbs_detail_update(id, header_id, detail_id):
    # Get the WBS name from the form data
    updated_name = request.form['wbs_detail_name']
    created_at_str = request.form['wbs_detail_created_at']
    updated_at_str = request.form['wbs_detail_updated_at']

    created_at = None
    updated_at = None

    if created_at_str and created_at_str.strip():
        created_at = datetime.strptime(created_at_str, '%Y-%m-%d')

    if updated_at_str and updated_at_str.strip():
        updated_at = datetime.strptime(updated_at_str, '%Y-%m-%d')

    # Find the WBS by ID and update its name and dates
    wbs_detail = WbsDetailProject.query.get(detail_id)
    if wbs_detail:
        wbs_detail.name = updated_name
        wbs_detail.created_at = created_at
        wbs_detail.updated_at = updated_at
        db.session.commit()
        return redirect(url_for('project.wbs_detail', id=id, header_id=header_id))
    else:
        return jsonify({'message': 'WBS Detail not found.'}), 404


@project_bp.route('/project/<int:id>/wbs/<int:header_id>/header/<int:detail_id>/detail/store', methods=['POST'])
def wbs_item_store(id, header_id, detail_id):
    if 'email' not in session:
        return redirect(url_for('auth.login'))

    wbs_item = WbsItemProject()
    wbs_item.name = request.form['wbs_item_name']
    wbs_item.wbs_detail_project_id = detail_id
    db.session.add(wbs_item)
    db.session.commit()

    return redirect(url_for('project.wbs_detail', id=id, header_id=header_id))


@project_bp.route('/project/wbs/item/<int:id>/delete', methods=['POST'])
def wbs_item_delete(id):
    wbs_item = WbsItemProject.query.get(id)
    db.session.delete(wbs_item)
    db.session.commit()

    return jsonify({'message': 'Data deleted successfully.'})


@project_bp.route('/project/<int:id>/wbs/<int:header_id>/header/<int:detail_id>/detail/<int:item_id>/update', methods=['POST'])
def wbs_item_update(id, header_id, detail_id, item_id):
    # Get the WBS name from the form data
    updated_name = request.form['wbs_item_name']
    created_at_str = request.form['wbs_item_created_at']
    updated_at_str = request.form['wbs_item_updated_at']

    created_at = None
    updated_at = None

    if created_at_str and created_at_str.strip():
        created_at = datetime.strptime(created_at_str, '%Y-%m-%d')

    if updated_at_str and updated_at_str.strip():
        updated_at = datetime.strptime(updated_at_str, '%Y-%m-%d')

    # Find the WBS by ID and update its name and dates
    wbs_item = WbsItemProject.query.get(item_id)
    if wbs_item:
        wbs_item.name = updated_name
        wbs_item.created_at = created_at
        wbs_item.updated_at = updated_at
        db.session.commit()
        return redirect(url_for('project.wbs_detail', id=id, header_id=header_id))
    else:
        return jsonify({'message': 'WBS Item not found.'}), 404