import tkinter as tk
from tkinter import ttk
from datetime import datetime
from decimal import Decimal, InvalidOperation
from .constants import FieldTypes as FT


class BoundText(tk.Text):
    """A Text widget with a bound variable."""

    def __init__(self, *args, textvariable=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._variable = textvariable

        if self._variable:
            self.insert('1.0', self._variable.get())
            self._variable.trace_add('write', self._set_content)
            self.bind('<<Modified>>', self._set_var)

    def _set_content(self, *_):
        """Set the text contents to the variable"""
        self.delete('1.0', tk.END)
        self.insert('1.0', self._variable.get())

    def _set_var(self, *_):
        """Set the variable to the text contents."""
        if self.edit_modified():
            content = self.get('1.0', 'end-1chars')
            self._variable.set(content)
            self.edit_modified(False)


class ValidatedMixin:
    """Adds validation functionality to an input widget"""

    def __init__(self, *args, error_var=None, **kwargs):
        self.error = error_var or tk.StringVar()
        super().__init__(*args, **kwargs)

        vcmd = self.register(self._validate)
        invcmd = self.register(self._invalid)

        self.configure(
            validate='all',
            validatecommand=(vcmd, '%P', '%s', '%S', '%V', '%i', '%d'),
            invalidcommand=(invcmd, '%P', '%s', '%S', '%V', '%i', '%d')
            )

    def _toggle_error(self, on=False):
        self.configure(foreground=('red' if on else 'black'))

    def _validate(self, proposed, current, char, event, index, action):
        self.error.set('')
        self._toggle_error()
        valid = True
        
        # if the widget is disabled, don't validate
        state = str(self.configure('state')[-1])
        
        if state == tk.DISABLED:
            return valid

        if event == 'focusout':
            valid = self._focusout_validate(event=event)
        elif event == 'key':
            valid = self._key_validate(proposed=proposed, current=current, 
                char=char, event=event, index=index, action=action)

        return valid

    def _focusout_validate(self, **kwargs):
        return True

    def _key_validate(self, **kwargs):
        return True

    def _invalid(self, proposed, current, char, event, index, action):
        if event == 'focusout':
            self._focusout_validate(event=event)
        elif event == 'key':
            self._key_invalid(proposed=proposed, current=current, char=char,
                event=event, index=index, action=action)

    def _focusout_invalid(self, **kwargs):
        """Handle invalid data on a focus event"""
        self._toggle_error(True)

    def _key_invalid(self, **kwargs):
        """Handle invalid data on a key event. 
        By default we want to do nothing"""
        pass

    def trigger_focusout_validation(self):
        valid = self._validate('', '', '', 'focusout', '', '')
        if not valid:
            self._focusout_invalid(event='focusout')
        return valid


class RequiredEntry(ValidatedMixin, ttk.Entry):
    """An Entry that requires a value"""

    def _focusout_validate(self, event):
        valid = True
        
        if not self.get():
            valid = False
            self.error.set("A value is required")
        
        return valid


class DateEntry(ValidatedMixin, ttk.Entry):
    """An Entry that only accepts ISO Date strings"""

    def _key_validate(self, action, index, char, **kwargs):
        valid = True

        if action == '0': # This is a delete action
            valid = True
        elif index in ('0', '1', '3', '4', '6', '7', '8', '9'):
            valid = char.isdigit()
        elif index in ('2', '5'):
            valid = char == '.'
        else:
            valid = False

        return valid

    def _focusout_validate(self, event):
        valid = True

        if not self.get():
            self.error.set('Datum je potrebno vnesti')
            valid = False
        
        try:
            datetime.strptime(self.get(), '%d.%m.%Y')
        except ValueError:
            self.error.set('Nepravilen vnos')
            valid = False
        
        return valid


class LabelInput(tk.Frame):
    """A widget containing a label and input together."""

    field_types = {
    FT.string: RequiredEntry,
    FT.date_string: DateEntry,
    FT.long_string: BoundText,
    FT.decimal: RequiredEntry,
    FT.integer: RequiredEntry,
    FT.boolean: ttk.Checkbutton
    }

    def __init__(
        self, parent, label, var, input_class=None, input_args=None, 
        label_args=None, field_spec=None, disable_var=None, **kwargs
        ):
        
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = var
        self.variable.label_widget = self

        if field_spec:
            field_type = field_spec.get('type', FT.string)
            input_class = input_class or self.field_types.get(field_type)
            if 'min' in field_spec and 'from_' not in input_args:
                input_args['from_'] = field_spec.get('min')
            if 'max' in field_spec and 'to' not in input_args:
                input_args['to'] = field_spec.get('max')
            if 'inc' in field_spec and 'increment' not in input_args:
                input_args['increment'] = field_spec.get('inc')
            if 'values' in field_spec and 'values' not in input_args:
                input_args['values'] = field_spec.get('values')

        if input_class in (ttk.Checkbutton, ttk.Button):
            input_args["text"] = label
        else:
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=0, sticky=(tk.W + tk.E))

        if input_class in (ttk.Checkbutton, ttk.Button, ttk.Radiobutton):
            input_args['variable'] = self.variable
        else:
            input_args['textvariable'] = self.variable

        if input_class == ttk.Radiobutton:
            self.input = tk.Frame(self)
            for v in input_args.pop('values', []):
                button = ttk.Radiobutton(self.input, value=v, text=v, 
                    **input_args)
                button.pack(side=tk.LEFT, ipadx=10, ipady=2, expand=True, 
                    fill='x')
        else:
            self.input = input_class(self, **input_args)

        self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))
        self.columnconfigure(0, weight=1)

        if disable_var:
            self.disable_var = disable_var
            self.disable_var.trace_add('write', self._check_disable)

        self.error = getattr(self.input, 'error', tk.StringVar())
        ttk.Label(self, textvariable=self.error, **label_args).grid(
            row=2, column=0, sticky=(tk.W + tk.E))

    def _check_disable(self, *_):
        if not hasattr(self, 'disable_var'):
            return

        if self.disable_var.get():
            self.input.configure(state=tk.DISABLED)
            self.variable.set('')
            self.error.set('')
        else:
            self.input.configure(state=tk.NORMAL)

    def grid(self, sticky=(tk.E + tk.W), **kwargs):
        """Override grid to add default sticky values"""
        super().grid(sticky=sticky, **kwargs)