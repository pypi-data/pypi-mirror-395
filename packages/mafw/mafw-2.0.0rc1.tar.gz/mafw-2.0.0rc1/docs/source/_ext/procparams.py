#  Copyright 2025 European Union
#  Author: Bulgheroni Antonio (antonio.bulgheroni@ec.europa.eu)
#  SPDX-License-Identifier: EUPL-1.2
from sphinx.application import Sphinx


def _find_class(name):
    """
    Dynamically resolve a class from a fully-qualified name.
    This avoids importing the main library inside the extension.
    """
    try:
        components = name.split('.')
        module_name = '.'.join(components[:-1])
        class_name = components[-1]
        mod = __import__(module_name, fromlist=[class_name])
        return getattr(mod, class_name, None)
    except Exception:
        return None


def extract_proc_params_from_docstring(lines):
    """
    Extract manual overrides from :proc_param <name>: <desc>.
    """
    overrides = {}
    new_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith(':proc_param'):
            try:
                _, rest = stripped.split(' ', 1)
                name, desc = rest.split(':', 1)
                overrides[name.strip()] = desc.strip()
            except ValueError:
                pass
        else:
            new_lines.append(line)

    lines[:] = new_lines
    return overrides


def inject_processor_parameters_section(lines, params):
    if not params:
        return

    lines.append('')
    lines.append('Processor parameters')
    # lines.append("--------------------")
    lines.append('')

    for name, info in params.items():
        lines.append(f'* **{name}**:')
        if info['doc']:
            lines.append(f'  {info["doc"]}')
        default = info['default']
        value = info['value']
        meta = []
        if default is not None:
            meta.append(f'default: {default!r}')
        if value is not None:
            meta.append(f'initial value: {value!r}')
        if meta:
            lines.append(f'  ({", ".join(meta)})')
        lines.append('')


def process_docstring(app, what, name, obj, options, lines):
    """
    Main hook: autodoc callback.
    """
    builder = app.builder

    # Track processed classes only for this build (non-persistent)
    if not hasattr(builder, 'procparams_done'):
        builder.procparams_done = set()

    if what == 'class' and name in builder.procparams_done:
        return

    if what == 'class':
        builder.procparams_done.add(name)

    # Get configured fqdn for Processor and ActiveParameter
    Processor = app.config.processor_base_class
    ActiveParameter = app.config.processor_param_class

    # If user didn't configure these -> do nothing
    if Processor is None or ActiveParameter is None:
        return

    Processor = _find_class(Processor)
    ActiveParameter = _find_class(ActiveParameter)

    # If resolve failed -> do nothing
    if Processor is None or ActiveParameter is None:
        return

    # Only for classes that inherit from Processor
    if not (what == 'class' and isinstance(obj, type) and issubclass(obj, Processor)):
        return

    # --- Step 1: manual overrides
    overrides = extract_proc_params_from_docstring(lines)

    # --- Step 2: auto inference
    inferred = {}
    for attr_name in dir(obj):
        try:
            attr = getattr(obj, attr_name, None)
        except Exception:
            continue

        if isinstance(attr, ActiveParameter):
            inferred[attr._external_name] = {
                'doc': attr._help_doc,
                'default': attr._default,
                'value': attr._value,
            }

    # --- Step 3: overrides
    for name, desc in overrides.items():
        inferred.setdefault(name, {'doc': None, 'default': None, 'value': None})
        inferred[name]['doc'] = desc

    # --- Step 4: add section
    inject_processor_parameters_section(lines, inferred)


def setup(app: Sphinx):
    app.add_config_value('processor_base_class', None, 'env')
    app.add_config_value('processor_param_class', None, 'env')

    app.connect('autodoc-process-docstring', process_docstring)

    return {
        'version': '0.2',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
