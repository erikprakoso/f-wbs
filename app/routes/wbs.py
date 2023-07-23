from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
from app.models.wbs_header import WbsHeader
from app.models.wbs_detail import WbsDetail
from app.models.wbs_item import WbsItem
from app import db

wbs_bp = Blueprint('wbs', __name__)

@wbs_bp.route('/wbs')
def wbs():
    if 'email' not in session:
        return redirect(url_for('auth.login'))

    wbs = WbsHeader.query.all()
    return render_template('wbs/index.html', wbs=wbs)

@wbs_bp.route('/wbs/store', methods=['POST'])
def store():
    if 'email' not in session:
        return redirect(url_for('auth.login'))

    wbs = WbsHeader()
    print(request.form['wbs_name'])
    wbs.name = request.form['wbs_name']
    db.session.add(wbs)
    db.session.commit()

    return redirect(url_for('wbs.wbs'))

@wbs_bp.route('/wbs/detail/<int:id>')
def detail(id):
    if 'email' not in session:
        return redirect(url_for('auth.login'))

    wbs = WbsHeader.query.get(id)
    wbs_details = WbsDetail.query.filter_by(wbs_header_id=id).all()
    return render_template('wbs/_detail.html', wbs=wbs, wbs_details=wbs_details)

@wbs_bp.route('/wbs/update/<int:id>', methods=['POST'])
def update_wbs(id):
    # Get the WBS name from the form data
    updated_name = request.form['wbs_edit']

    # Find the WBS by ID and update its name
    wbs = WbsHeader.query.get(id)
    if wbs:
        wbs.name = updated_name
        db.session.commit()
        return redirect(url_for('wbs.wbs'))
    else:
        return jsonify({'message': 'WBS not found.'}), 404
    
@wbs_bp.route('/wbs/delete/<int:id>', methods=['POST'])
def delete(id):
    wbs = WbsHeader.query.get(id)
    db.session.delete(wbs)
    db.session.commit()

    return jsonify({'message': 'Data deleted successfully.'})

@wbs_bp.route('/wbs/detail/store', methods=['POST'])
def store_detail():
    wbs_detail = WbsDetail()
    wbs_detail.wbs_header_id = request.form['wbs_header_id']
    wbs_detail.code = request.form['wbs_code']
    wbs_detail.name = request.form['wbs_name']
    db.session.add(wbs_detail)
    db.session.commit()

    return redirect(url_for('wbs.detail', id=request.form['wbs_header_id']))

@wbs_bp.route('/wbs/detail/update/<int:id>', methods=['POST'])
def update_detail(id):
    wbs_detail = WbsDetail.query.get(id)
    wbs_detail.code = request.form['wbs_code_edit']
    wbs_detail.name = request.form['wbs_name_edit']
    db.session.commit()

    return redirect(url_for('wbs.detail', id=request.form['wbs_header_id_edit']))

@wbs_bp.route('/wbs/detail/delete/<int:id>', methods=['POST'])
def delete_detail(id):
    wbs_detail = WbsDetail.query.get(id)
    db.session.delete(wbs_detail)
    db.session.commit()

    return jsonify({'message': 'Data deleted successfully.'})

@wbs_bp.route('/wbs/<int:id>/detail/<int:detail_id>/item')
def detail_item(id, detail_id):
    if 'email' not in session:
        return redirect(url_for('auth.login'))

    wbs = WbsHeader.query.get(id)
    wbs_detail = WbsDetail.query.get(detail_id)
    wbs_items = WbsItem.query.filter_by(wbs_detail_id=detail_id).all()
    return render_template('wbs/item/_detail.html', wbs=wbs, wbs_detail=wbs_detail, wbs_items=wbs_items)

@wbs_bp.route('/wbs/detail/item/store', methods=['POST'])
def store_item():
    wbs_item = WbsItem()
    wbs_item.wbs_detail_id = request.form['wbs_detail_id']
    wbs_item.code = request.form['wbs_item_code']
    wbs_item.name = request.form['wbs_item_name']
    db.session.add(wbs_item)
    db.session.commit()

    return redirect(url_for('wbs.detail_item', id=request.form['wbs_header_id'], detail_id=request.form['wbs_detail_id']))

@wbs_bp.route('/wbs/detail/item/delete/<int:id>', methods=['POST'])
def delete_item(id):
    wbs_item = WbsItem.query.get(id)
    db.session.delete(wbs_item)
    db.session.commit()

    return jsonify({'message': 'Data deleted successfully.'})

@wbs_bp.route('/wbs/detail/item/update/<int:id>', methods=['POST'])
def update_item(id):
    wbs_item = WbsItem.query.get(id)
    wbs_item.code = request.form['wbs_item_code_edit']
    wbs_item.name = request.form['wbs_item_name_edit']
    db.session.commit()

    return redirect(url_for('wbs.detail_item', id=request.form['wbs_header_id_edit'], detail_id=request.form['wbs_detail_id_edit']))