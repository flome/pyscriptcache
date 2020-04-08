import logging
import os
import pickle
import time
from functools import partial

# globals
log = logging.getLogger(__name__)


class PickleCache:
    def __init__(self, checkpoint_file, warn_on_overwrite=True, save_on_assign=True):
        t0 = time.time()

        self.state = {}
        self.filename = checkpoint_file
        self.warn_on_overwrite = warn_on_overwrite
        self.save_on_assign = save_on_assign

        self.init_state()
        log.info("Created PickleCache in %.2f ms" % ((time.time() - t0) * 1000))

    def init_state(self):
        if os.path.isfile(self.filename):
            log.info("Using existing state file")
            try:
                data = pickle.load(open(self.filename, 'rb'))
            except EOFError as e:
                log.warning("State file may have been corrupted: %s" % str(e))
            assert isinstance(data, dict), "State creation not successful! Should be dict but is %s" % type(data)
            self.state = data
        return

    def var(self, name, val, recompute=True):
        if name not in self.state.keys():
            recompute = True

        if recompute:
            if name in self.keys():
                log.info('Overwriting existing variable %s in state' % name)
            if hasattr(val, 'pystate_func'):
                val = val()
            self.state[name] = val
        else:
            log.info('Fetching variable %s from state' % name)
            val = self.state[name]

        if self.save_on_assign:
            pickle.dump(self.state, open(self.filename, 'wb'))

        return val

    def save(self):
        pickle.dump(self.state, open(self.filename, 'wb'))
        return

    def keys(self):
        return self.state.keys()

    def __getitem__(self, item):
        return self.state[item]

    @staticmethod
    def func(f, *args, **kwargs):
        f = partial(f, *args, **kwargs)
        f.pystate_func = True
        return f
