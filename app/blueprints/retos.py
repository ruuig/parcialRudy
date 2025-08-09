# app/blueprints/retos.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..db import query

retos_bp = Blueprint('retos', __name__, template_folder='../templates/retos')

CATEGORIAS = ['salud','educacion','negocios','arte','otros']
DIFICULTADES = ['bajo','medio','alto']
ESTADOS = ['pendiente','en_proceso','completado']

@retos_bp.get('/')
def index():
    categoria = request.args.get('categoria') or ''
    dificultad = request.args.get('dificultad') or ''
    estado = request.args.get('estado') or ''
    page = max(int(request.args.get('page', 1)), 1)
    per_page = 8
    offset = (page - 1) * per_page

    filters = []
    params = []

    if categoria:
        filters.append("categoria = %s")
        params.append(categoria)
    if dificultad:
        filters.append("dificultad = %s")
        params.append(dificultad)
    if estado:
        filters.append("estado = %s")
        params.append(estado)

    where = f"WHERE {' AND '.join(filters)}" if filters else ''
    total = query(f"SELECT COUNT(*) FROM retos {where}", params, fetch='one')[0]
    retos = query(f"""
        SELECT id, titulo, descripcion, categoria, dificultad, estado, creado_en
        FROM retos
        {where}
        ORDER BY creado_en DESC
        LIMIT %s OFFSET %s
    """, params + [per_page, offset], fetch='all')

    pages = (total + per_page - 1) // per_page
    return render_template('retos/index.html',
                           retos=retos, categorias=CATEGORIAS, dificultades=DIFICULTADES, estados=ESTADOS,
                           sel_categoria=categoria, sel_dificultad=dificultad, sel_estado=estado,
                           page=page, pages=pages, total=total)

@retos_bp.get('/nuevo')
def new():
    return render_template('retos/create.html',
                           categorias=CATEGORIAS, dificultades=DIFICULTADES)

@retos_bp.post('/')
def create():
    form = request.form
    titulo = form.get('titulo','').strip()
    descripcion = form.get('descripcion','').strip()
    categoria = form.get('categoria')
    dificultad = form.get('dificultad')

    if not titulo or not descripcion or categoria not in CATEGORIAS or dificultad not in DIFICULTADES:
        flash('Revisa los campos: título, descripción, categoría y dificultad son obligatorios.', 'danger')
        return redirect(url_for('retos.new'))

    query("""
        INSERT INTO retos (titulo, descripcion, categoria, dificultad)
        VALUES (%s, %s, %s, %s)
    """, [titulo, descripcion, categoria, dificultad], fetch=None)
    flash('Reto creado con éxito.', 'success')
    return redirect(url_for('retos.index'))

@retos_bp.get('/<int:reto_id>')
def detail(reto_id):
    reto = query("""
        SELECT id, titulo, descripcion, categoria, dificultad, estado, creado_en
        FROM retos WHERE id = %s
    """, [reto_id], fetch='one')
    if not reto:
        flash('Reto no encontrado.', 'warning')
        return redirect(url_for('retos.index'))
    return render_template('retos/detail.html', reto=reto)

@retos_bp.get('/<int:reto_id>/editar')
def edit(reto_id):
    reto = query("SELECT * FROM retos WHERE id = %s", [reto_id], fetch='one')
    if not reto:
        flash('Reto no encontrado.', 'warning')
        return redirect(url_for('retos.index'))
    return render_template('retos/edit.html', reto=reto,
                           categorias=CATEGORIAS, dificultades=DIFICULTADES, estados=ESTADOS)

@retos_bp.post('/<int:reto_id>/editar')
def update(reto_id):
    form = request.form
    titulo = form.get('titulo','').strip()
    descripcion = form.get('descripcion','').strip()
    categoria = form.get('categoria')
    dificultad = form.get('dificultad')
    estado = form.get('estado')

    if (not titulo or not descripcion or
        categoria not in CATEGORIAS or dificultad not in DIFICULTADES or estado not in ESTADOS):
        flash('Hay campos inválidos.', 'danger')
        return redirect(url_for('retos.edit', reto_id=reto_id))

    query("""
        UPDATE retos SET titulo=%s, descripcion=%s, categoria=%s, dificultad=%s, estado=%s
        WHERE id=%s
    """, [titulo, descripcion, categoria, dificultad, estado, reto_id], fetch=None)
    flash('Reto actualizado.', 'success')
    return redirect(url_for('retos.detail', reto_id=reto_id))

@retos_bp.post('/<int:reto_id>/estado')
def update_status(reto_id):
    estado = request.form.get('estado')
    if estado not in ESTADOS:
        flash('Estado inválido.', 'danger')
        return redirect(url_for('retos.detail', reto_id=reto_id))
    query("UPDATE retos SET estado=%s WHERE id=%s", [estado, reto_id], fetch=None)
    flash('Estado actualizado.', 'success')
    return redirect(url_for('retos.detail', reto_id=reto_id))

@retos_bp.post('/<int:reto_id>/eliminar')
def delete(reto_id):
    query("DELETE FROM retos WHERE id=%s", [reto_id], fetch=None)
    flash('Reto eliminado.', 'info')
    return redirect(url_for('retos.index'))
