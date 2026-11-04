"""Flask Queue Simulator (FIFO)."""
import os
import secrets

from flask import (Flask, flash, redirect, render_template, request,
                   session, url_for)

from queue_model import Queue

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
# localhost cookies are shared across ports, so give this app its own cookie
# name. Otherwise it overwrites the stack app's session.
app.config['SESSION_COOKIE_NAME'] = 'queue_session'

MAX_ITEMS = 20
MAX_LENGTH = 24
MAX_HISTORY = 20


@app.route('/')
def index():
    queue = Queue(session.get('queue', []))
    removed = session.get('removed', [])
    highlight = request.args.get('peek') == '1'
    return render_template(
        'index.html',
        items=queue.items,                 # NOT reversed: front is shown first
        size=queue.size(),
        removed=list(reversed(removed)),   # newest removal first
        highlight=highlight,
    )


@app.route('/queue', methods=['POST'])
def operate():
    action = request.form.get('action', '').strip().lower()
    value = request.form.get('value', '').strip()
    queue = Queue(session.get('queue', []))
    removed = session.get('removed', [])
    highlight = False

    if action == 'enqueue':
        if not value:
            flash('Please type a value before enqueueing.', 'error')
        elif len(value) > MAX_LENGTH:
            flash(f'Value must be {MAX_LENGTH} characters or fewer.', 'error')
        elif queue.size() >= MAX_ITEMS:
            flash(f'Queue is full ({MAX_ITEMS} items).', 'error')
        else:
            queue.enqueue(value)
            flash(f'Enqueued "{value}" at the rear.', 'success')
    elif action == 'dequeue':
        if queue.is_empty():
            flash('The queue is empty. Nothing to dequeue.', 'error')
        else:
            item = queue.dequeue()
            removed.append(item)
            removed = removed[-MAX_HISTORY:]
            flash(f'Dequeued "{item}" from the front.', 'success')
    elif action == 'peek':
        if queue.is_empty():
            flash('The queue is empty. Nothing to peek.', 'error')
        else:
            highlight = True
            flash(f'Front of the queue is "{queue.peek()}".', 'success')
    elif action == 'clear':
        queue.clear()
        removed = []
        flash('Queue and removed items cleared.', 'success')
    else:
        flash('Unknown action.', 'error')

    session['queue'] = queue.items
    session['removed'] = removed
    if highlight:
        return redirect(url_for('index', peek=1))
    return redirect(url_for('index'))


@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)