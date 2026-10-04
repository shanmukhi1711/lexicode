from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from models import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    from models import CheckHistory, Document
    checks = CheckHistory.query.filter_by(user_id=current_user.id).order_by(CheckHistory.date.desc()).limit(10).all()
    total_checks = CheckHistory.query.filter_by(user_id=current_user.id).count()
    all_checks = CheckHistory.query.filter_by(user_id=current_user.id).all()
    avg_sim = round(sum(c.score for c in all_checks) / len(all_checks), 1) if all_checks else 0
    total_docs = Document.query.count()
    return render_template('dashboard.html', checks=checks, total_checks=total_checks, avg_sim=avg_sim, total_docs=total_docs)

@main_bp.route('/check', methods=['GET', 'POST'])
@login_required
def check():
    if request.method == 'POST':
        title = request.form.get('title', 'Untitled Check')
        text = request.form.get('text', '')
        
        # Simple file handling (for demo)
        files = request.files.getlist('file')
        valid_files = []
        for file in files:
            if file and file.filename:
                valid_files.append((file.filename, file.read().decode('utf-8', errors='ignore')))
        
        from processing import preprocess_text
        from similarity import compute_cosine, compute_overall_score, get_verdict
        from models import Document, CheckHistory
        import json

        if len(valid_files) > 1:
            # Cross-compare mode
            matches = []
            max_score = 0.0
            for i in range(len(valid_files)):
                for j in range(i+1, len(valid_files)):
                    f1_name, f1_text = valid_files[i]
                    f2_name, f2_text = valid_files[j]
                    score = compute_cosine(f1_text, f2_text)
                    if score >= 0:
                        matches.append((f"{f1_name} vs {f2_name}", score))
                    if score > max_score:
                        max_score = score
                        
            overall_score = max_score * 100
            history = CheckHistory(
                user_id=current_user.id,
                type='Cross-Compare',
                title=title if title and title != 'Untitled Check' else 'Multiple Files Check',
                text=f"Cross comparison of {len(valid_files)} files.",
                score=overall_score,
                details=json.dumps({"matches": matches})
            )
            db.session.add(history)
            db.session.commit()
            return redirect(url_for('main.results', check_id=history.id))
            
        else:
            # Single file or text mode
            if valid_files:
                text = valid_files[0][1]
                
            if not text.strip():
                return "Error: No text provided.", 400
                
            # Get all reference documents
            docs = Document.query.all()
            matches = []
            max_score = 0.0
            
            for doc in docs:
                score = compute_cosine(text, doc.content)
                if score > 0:
                    matches.append((doc.title, score))
                if score > max_score:
                    max_score = score
                    
            overall_score = max_score * 100
            
            history = CheckHistory(
                user_id=current_user.id,
                type='Single',
                title=title,
                text=text[:500], # store snippet
                score=overall_score,
                details=json.dumps({"matches": matches})
            )
            db.session.add(history)
            db.session.commit()
            
            return redirect(url_for('main.results', check_id=history.id))
        
    return render_template('check.html')

@main_bp.route('/results/<int:check_id>')
@login_required
def results(check_id):
    from models import CheckHistory
    from similarity import get_verdict
    import json
    
    check_obj = CheckHistory.query.get_or_404(check_id)
    if check_obj.user_id != current_user.id:
        return "Unauthorized", 403
        
    details = json.loads(check_obj.details or '{}')
    verdict = get_verdict(check_obj.score)
    return render_template('results.html', check=check_obj, details=details, verdict=verdict)

@main_bp.route('/library')
@login_required
def library():
    from models import Document
    documents = Document.query.all()
    return render_template('reference.html', documents=documents)

@main_bp.route('/add_reference', methods=['POST'])
@login_required
def add_reference():
    from models import Document
    title = request.form.get('title')
    content = request.form.get('content')
    if title and content:
        doc = Document(title=title, content=content, user_id=current_user.id)
        db.session.add(doc)
        db.session.commit()
    return redirect(url_for('main.library'))

@main_bp.route('/delete_reference/<int:doc_id>', methods=['POST'])
@login_required
def delete_reference(doc_id):
    from models import Document
    doc = Document.query.get_or_404(doc_id)
    if doc.user_id == current_user.id or doc.user_id is None:
        db.session.delete(doc)
        db.session.commit()
    return redirect(url_for('main.library'))
