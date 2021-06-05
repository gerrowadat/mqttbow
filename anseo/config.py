import logging
import importlib


class AnseoConfigError(Exception):
    pass


class Config(object):
    HOOKS = []

    def get_hook(self, key, action):
        hooks = [h for h in self.HOOKS if h[0] == key and h[1] == action]
        if not hooks:
            logging.debug('No hook found for %s of key #%d' % (action, key))
            return (None, None)
        elif len(hooks) > 1:
            raise AnseoConfigError('duplicate hook for key %d, action %s' % (key, action))
        else:
            logging.debug('Found hook %s for %s of key #%d' % (hooks[0][2].__name__, action, key))
            return (hooks[0][2], hooks[0][3])

    def Load(self, filename=None, obj=None):
        if (not filename and not obj) or (filename and obj):
            raise AnseoConfigError('must pass either filename or object')
        if filename:
            local_vars = {}
            with open(filename) as f:
                code = compile(f.read(), "config", 'exec')
                # It seems cleaner to inject anseo.plugins into the global namespace here than importing it.
                exec(code, {**globals(), **{'plugins': importlib.import_module('anseo.plugins')}}, local_vars)
            config_objs = [o for o in local_vars.values() if Config in o.mro()]
            if len(config_objs) != 1:
                raise AnseoConfigError('config file must have exactly 1 config.Config subclass')
            self.HOOKS = config_objs[0].HOOKS
        if obj:
            if Config not in obj.mro():
                raise AnseoConfigError('config object passed must be a config.Config subclass')
            self.HOOKS = obj.HOOKS
