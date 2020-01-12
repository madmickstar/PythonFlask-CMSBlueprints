from flask import Blueprint, render_template, abort, request
from flask import redirect, url_for, flash
from .models import Type, Content, Setting, User, db

admin_bp = Blueprint('admin', __name__, 
                      url_prefix='/admin',
                      template_folder='templates')



## Admin Routes
def requested_type(type):
    types = [row.name for row in Type.query.all()]
    return True if type in types else False

@admin_bp.route('/', defaults={'type': 'page'})
@admin_bp.route('/<type>')
def content(type):
    if requested_type(type):
        content = Content.query.join(Type).filter(Type.name == type)
        return render_template('admin/content.html', type=type, content=content)
    else:
        abort(404)

@admin_bp.route('/create/<type>', methods=['GET', 'POST'])
def create(type):
    if requested_type(type):
        
        if request.method == 'POST':
            title = request.form['title']
            slug = request.form['slug']
            type_id = request.form['type_id']
            body = request.form['body']
            error = None
            if title is None:
                error = "Title can not be empty"
            elif type_id is None:
                error = "Type can not be empty" 
            if error is None:
                content = Content(title=title,
                                  slug=slug, 
                                  type_id=type_id, 
                                  body=body)
                db.session.add(content)
                db.session.commit()
                return redirect(url_for('admin.content',type=type))
            else:
                flash(error)
        types = Type.query.all()
        return render_template('admin/content_form.html', title='Create', types=types, type_name=type)
    else:
        abort(404)

@admin_bp.route('/users')
def users():
    users = User.query.all()
    return render_template('admin/users.html', title='Users', users=users)

@admin_bp.route('/settings')
def settings():
    settings = Setting.query.all()
    return render_template('admin/settings.html', title='Settings', settings=settings)
