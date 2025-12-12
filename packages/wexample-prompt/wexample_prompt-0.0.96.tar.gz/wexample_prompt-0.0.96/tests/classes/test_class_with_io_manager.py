from __future__ import annotations

from wexample_prompt.testing.abstract_prompt_test import AbstractPromptTest


class TestIoManager(AbstractPromptTest):
    __test__ = True  # Re-enable test collection for concrete test class

    def assertClassHasNoneManager(self, class_type: type) -> None:
        instance = class_type()
        assert instance.io is None

    def assertClassInstanceSucceeded(self, class_type: type) -> None:
        from wexample_prompt.common.io_manager import IoManager

        instance = class_type(io=self._io)
        assert isinstance(instance.io, IoManager)

    def assertMissingArgumentError(self, class_type: type) -> None:
        with self.assertRaises(TypeError):
            class_type()

    def test_instantiate_base_class(self) -> None:
        from wexample_prompt.testing.resources.classes.base_class_with_io_manager import (
            ExtendedBaseClassWithIoManager,
        )

        self.assertClassHasNoneManager(ExtendedBaseClassWithIoManager)
        self.assertClassInstanceSucceeded(ExtendedBaseClassWithIoManager)

    def test_instantiate_base_class_required(self) -> None:
        from wexample_prompt.testing.resources.classes.base_class_with_required_io_manager import (
            BaseClassWithRequiredIoManager,
        )

        self.assertMissingArgumentError(BaseClassWithRequiredIoManager)
        self.assertClassInstanceSucceeded(BaseClassWithRequiredIoManager)

    def test_instantiate_class(self) -> None:
        from wexample_prompt.testing.resources.classes.class_with_io_manager import (
            ClassWithIoManager,
        )

        instance = ClassWithIoManager()
        assert instance.io is None

        self.assertClassHasNoneManager(ClassWithIoManager)
        self.assertClassInstanceSucceeded(ClassWithIoManager)

    def test_instantiate_class_required(self) -> None:
        from wexample_prompt.testing.resources.classes.class_with_required_io_manager import (
            ClassWithRequiredIoManager,
        )

        # Missing required 'io' should raise a TypeError from __init__
        self.assertMissingArgumentError(class_type=ClassWithRequiredIoManager)
        self.assertClassInstanceSucceeded(class_type=ClassWithRequiredIoManager)
