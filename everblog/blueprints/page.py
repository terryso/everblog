# coding=utf-8
"""
    everblog.blueprints.static
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    Static pages for the site
"""
from flask import Blueprint, render_template, abort, redirect, request, url_for
from everblog import db
from everblog.models import Page
from everblog.blueprints import admin_required


blueprint = Blueprint('page', __name__)


@blueprint.route('/<regex("(?:[a-z]{3,16}|[\u4e00-\u9fa5]{2,8})"):title>/', methods = ['GET', ])
def read(title):
    page = db.session.query(Page).filter_by(title = title.capitalize()).first()
    if not page:
        abort(404)
    return render_template('page/read.html', page = page)


@blueprint.route('/p/create/', methods = ['POST', ])
@admin_required
def create():
    page = Page(evernote_url = request.form['evernote_url'], order = request.form['order'])
    page.synchronize()
    db.session.add_then_commit(page)
    return redirect(url_for('admin.index'))


@blueprint.route('/p/delete/<int:id>/', methods = ['GET', ])
@admin_required
def delete(id):
    page = db.session.query(Page).get(id)
    if not page:
        abort(404)
    db.session.delete_then_commit(page)
    return redirect(url_for('admin.index'))


@blueprint.route('/p/synchronize/<int:id>/', methods = ['GET', ])
@admin_required
def synchronize(id):
    page = db.session.query(Page).get(id)
    if not page:
        abort(404)
    page.synchronize()
    db.session.commit()
    return redirect(url_for('admin.index'))
