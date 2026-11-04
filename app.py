"""Flask Stack Simulator."""
import secrets

from flask import (Flask, flash, redirect, render_template, request,
                   session, url_for)

from stack_model import Stack

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)  # signs the session cookie

MAX_ITEMS = 20
MAX_LENGTH = 24
MAX_HISTORY = 20


@app.route('/')
def index():
    stack = Stack(session.get('stack', []))
    removed = session.get('removed', [])
    highlight = session.pop('highlight', False)   # one-time Peek flag
    return render_template(
        'index.html',
        items=list(reversed(stack.items)),        # top shown first
        size=stack.size(),
        popped=list(reversed(removed)),           # newest removal first
        highlight=highlight,
    )


@app.route('/stack', methods=['POST'])
def operate():
    action = request.form.get('action', '').strip().lower()
    value = request.form.get('value', '').strip()
    stack = Stack(session.get('stack', []))
    removed = session.get('removed', [])

    if action == 'push':
        if not value:
            flash('Please type a value before pushing.', 'error')
        elif len(value) > MAX_LENGTH:
            flash(f'Value must be {MAX_LENGTH} characters or fewer.', 'error')
        elif stack.size() >= MAX_ITEMS:
            flash(f'Stack is full ({MAX_ITEMS} items).', 'error')
        else:
            stack.push(value)
            flash(f'Pushed "{value}" onto the stack.')
    elif action == 'pop':
        if stack.is_empty():
            flash('The stack is empty. Nothing to pop.', 'error')
        else:
            item = stack.pop()
            removed.append(item)
            removed = removed[-MAX_HISTORY:]
            flash(f'Popped "{item}" from the top.')
    elif action == 'peek':
        if stack.is_empty():
            flash('The stack is empty. Nothing to peek.', 'error')
        else:
            session['highlight'] = True
            flash(f'Top of the stack is "{stack.peek()}".')
    elif action == 'clear':
        stack.clear()
        removed = []
        flash('Stack and removed items cleared.')
    else:
        flash('Unknown action.', 'error')

    session['stack'] = stack.items     # reassign so Flask saves the change
    session['removed'] = removed
    return redirect(url_for('index'))


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)