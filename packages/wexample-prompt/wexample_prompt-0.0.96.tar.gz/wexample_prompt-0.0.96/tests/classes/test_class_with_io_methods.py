from __future__ import annotations

from wexample_prompt.testing.abstract_prompt_test import AbstractPromptTest


class TestIoManager(AbstractPromptTest):
    __test__ = True  # Re-enable test collection for concrete test class

    def test_instantiate_base_class(self) -> None:
        from wexample_prompt.testing.resources.classes.base_class_with_io_methods import (
            BaseClassWithIoMethods,
        )

        instance = BaseClassWithIoMethods(io=self._io)
        assert instance.log(message="test instantiate base model") is not None

    def test_instantiate_class(self) -> None:
        from wexample_prompt.testing.resources.classes.class_with_io_methods import (
            ClassWithIoMethods,
        )

        instance = ClassWithIoMethods(io=self._io)
        assert instance.log(message="test instantiate class") is not None
