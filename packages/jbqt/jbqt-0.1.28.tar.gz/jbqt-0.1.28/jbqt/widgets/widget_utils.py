from collections.abc import Callable

from jbqt.consts import QtGlobalRefs


def debug_scroll_pos(func: Callable):
    def wrapper(self, *args, **kwargs):
        if QtGlobalRefs.scroll_area is None:
            return func(self, *args, **kwargs)
        focus = None
        if QtGlobalRefs.main_window:
            focus = QtGlobalRefs.main_window.focusWidget()
        print(f"scroll pos {func.__name__}")
        # TODO: fix type checking
        print("before", QtGlobalRefs.scroll_area.verticalScrollBar().value(), focus)  # type: ignore
        result = func(self, *args, **kwargs)

        if QtGlobalRefs.main_window:
            focus = QtGlobalRefs.main_window.focusWidget()
        print(
            f"after {QtGlobalRefs.scroll_area.verticalScrollBar().value()} {focus}\n"  # type: ignore
        )

        return result

    return wrapper


def debug_scroll_pos_no_args(func: Callable):
    def wrapper(self):
        if QtGlobalRefs.scroll_area is None:
            return func(self)
        focus = None
        if QtGlobalRefs.main_window:
            focus = QtGlobalRefs.main_window.focusWidget()
        # TODO: fix type checking
        print(f"scroll pos {func.__name__}")
        print("before", QtGlobalRefs.scroll_area.verticalScrollBar().value(), focus)  # type: ignore
        result = func(self)
        if QtGlobalRefs.main_window:
            focus = QtGlobalRefs.main_window.focusWidget()
        print(
            f"after {QtGlobalRefs.scroll_area.verticalScrollBar().value()} {focus}\n"  # type: ignore
        )

        return result

    return wrapper


def _call_func(func: Callable, *args, **kwargs):
    if args and kwargs:
        return func(*args, **kwargs)
    elif args:
        return func(*args)
    elif kwargs:
        return func(**kwargs)
    else:
        return func()


def preserve_scroll(func: Callable):
    def wrapper(self, *args, **kwargs):
        if QtGlobalRefs.scroll_area is None:
            return _call_func(func, self, *args, **kwargs)

        scrollbar = QtGlobalRefs.scroll_area.verticalScrollBar()
        if not scrollbar:
            return

        scroll_pos = scrollbar.value()

        if not QtGlobalRefs.app:
            return

        focus = QtGlobalRefs.app.focusWidget()
        if not focus:
            return

        result = _call_func(
            func,
            self,
            *args,
            **kwargs,
        )
        scrollbar.setValue(scroll_pos)
        focus.setFocus()
        return result

    return wrapper
