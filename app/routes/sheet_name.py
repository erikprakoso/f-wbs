from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
from app.models.sheet_name import SheetName
from app import db

sheet_name_bp = Blueprint('sheet_name', __name__)

@sheet_name_bp.route('/sheets')
def sheets():
    if 'email' not in session:
        return redirect(url_for('auth.login'))

    sheets = SheetName.query.all()
    return render_template('sheet_name/index.html', sheets=sheets)

@sheet_name_bp.route('/sheet/delete/<int:id>', methods=['POST'])
def delete(id):
    sheet = SheetName.query.get(id)
    db.session.delete(sheet)
    db.session.commit()
    
    return jsonify({'message': 'Data deleted successfully.'})

@sheet_name_bp.route('/sheet/update/<int:id>', methods=['POST'])
def update(id):
    # Get the sheet name from the form data
    updated_name = request.form['sheet_name_edit']

    # Find the sheet by ID and update its name
    sheet = SheetName.query.get(id)
    if sheet:
        sheet.name = updated_name
        db.session.commit()
        return redirect(url_for('sheet_name.sheets'))
    else:
        return jsonify({'message': 'Sheet not found.'}), 404

@sheet_name_bp.route('/sheet/store', methods=['POST'])
def store():
    if 'email' not in session:
        return redirect(url_for('auth.login'))

    sheet = SheetName()
    sheet.name = request.form['sheet_name']
    db.session.add(sheet)
    db.session.commit()

    return redirect(url_for('sheet_name.sheets'))