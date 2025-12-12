import contextlib
from collections.abc import Generator
from tagflow import tag
from tagflow.tagflow import AttrValue


@contextlib.contextmanager
def Link(
    text: str = None,
    **kwargs: AttrValue,
) -> Generator[None]:
    
    with tag.a(**kwargs):
        if text:
            tag.text(text)
        yield



