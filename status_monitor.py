import progressbar

class StatusMonitor:
    _widgets = ['Loading: ', progressbar.AnimatedMarker()]
    _bar = None
    _count = 0

    def new_bar(self, size):
        self._bar = progressbar.ProgressBar(maxval=size, widgets=self._widgets).start()
    
    def increment_bar(self):
        assert self._bar, "bar must be instantiated with `StatusMonitor#new_bar` before incrementing"
        count += 1
        self._bar.update(count)

    def clear_bar(self):
        self._bar.finish()
