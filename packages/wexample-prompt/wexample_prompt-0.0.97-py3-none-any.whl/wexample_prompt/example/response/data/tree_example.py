"""Example for tree response."""

from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class TreeExample(AbstractResponseExample):
    """Example for tree response."""

    def example_class(self, indentation: int | None = None):
        """Example using class with context."""
        from wexample_prompt.responses.data.tree_prompt_response import (
            TreePromptResponse,
        )

        data = {
            "root": {
                "folder1": {
                    "file1": "content1",
                    "file2": "content2",
                },
                "folder2": {
                    "subfolder": {
                        "file3": "content3",
                    }
                },
            }
        }
        return TreePromptResponse.create_tree(
            data=data,
        )

    def example_deep_nesting(self) -> None:
        """Tree with deep nesting."""
        self.io.tree(
            data={
                "level1": {
                    "level2": {
                        "level3": {
                            "level4": {
                                "level5": {
                                    "deep_file.txt": None,
                                }
                            }
                        }
                    }
                }
            }
        )

    def example_extended(self) -> None:
        """Example using context."""
        data = {
            "root": {
                "folder1": {
                    "file1": "content1",
                    "file2": "content2",
                },
                "folder2": {
                    "subfolder": {
                        "file3": "content3",
                    }
                },
            }
        }
        self._class_with_methods.tree(data=data)

    def example_manager(self) -> None:
        """Example using IoManager directly."""
        data = {
            "root": {
                "folder1": {
                    "file1": "content1",
                    "file2": "content2",
                },
                "folder2": {
                    "subfolder": {
                        "file3": "content3",
                    }
                },
            }
        }
        self.io.tree(data=data)

    def example_mixed_structure(self) -> None:
        """Tree with mixed files and folders."""
        self.io.tree(
            data={
                "📁 webapp": {
                    "📁 frontend": {
                        "📁 src": {
                            "📁 components": {
                                "⚙️ Header.tsx": None,
                                "⚙️ Footer.tsx": None,
                            },
                            "🎨 App.css": None,
                            "⚙️ App.tsx": None,
                        },
                        "📦 package.json": None,
                    },
                    "📁 backend": {
                        "📁 api": {
                            "🐍 routes.py": None,
                            "🐍 models.py": None,
                        },
                        "📦 requirements.txt": None,
                    },
                }
            }
        )

    def example_nesting(self) -> None:
        """Tree with parent/child nesting."""
        from wexample_prompt.example.helpers.nesting_demo_classes import ParentTask

        self.io.tree(
            data={
                "@color:yellow+bold{Nesting Demo}": {
                    "tree_example": None,
                }
            }
        )
        parent = ParentTask(io=self.io)
        parent.execute(method_name="log")

    def example_simple(self) -> None:
        """Simple tree structure."""
        self.io.tree(
            data={
                "project": {
                    "src": {
                        "main.py": None,
                        "utils.py": None,
                    },
                    "tests": {
                        "test_main.py": None,
                    },
                    "README.md": None,
                }
            }
        )

    def example_with_emojis(self) -> None:
        """Tree with emojis."""
        self.io.tree(
            data={
                "📁 project": {
                    "📁 src": {
                        "🐍 main.py": None,
                        "🐍 utils.py": None,
                    },
                    "📁 tests": {
                        "🧪 test_main.py": None,
                    },
                    "📝 README.md": None,
                }
            }
        )

    def example_with_formatting(self) -> None:
        """Tree with inline formatting."""
        self.io.tree(
            data={
                "@color:cyan+bold{project}": {
                    "@color:yellow{src}": {
                        "@color:green{main.py}": None,
                        "@color:green{utils.py}": None,
                    },
                    "@color:yellow{tests}": {
                        "@color:blue{test_main.py}": None,
                    },
                    "@color:magenta{README.md}": None,
                }
            }
        )

    def example_with_indentation(self) -> None:
        """Trees at different indentation levels."""
        self.io.log("@color:cyan+bold{Trees at different levels:}")

        self.io.tree(data={"level0": {"file.txt": None}}, indentation=0)

        self.io.tree(data={"level1": {"file.txt": None}}, indentation=1)

        self.io.tree(data={"level3": {"file.txt": None}}, indentation=3)

    def example_with_paths(self) -> None:
        """Tree with clickable file paths."""
        self.io.tree(
            data={
                "📁 project": {
                    "@path:short{/home/user/project/src/main.py}": None,
                    "@path:short{/home/user/project/src/utils.py}": None,
                    "📁 tests": {
                        "@path:short{/home/user/project/tests/test_main.py}": None,
                    },
                    "@path:short{/home/user/project/README.md}": None,
                    "@path:short{/home/user/project/setup.py}": None,
                }
            }
        )

    def example_with_values(self) -> None:
        """Tree with values displayed."""
        self.io.tree(
            data={
                "config": {
                    "database": {
                        "host": "localhost",
                        "port": 5432,
                        "name": "mydb",
                    },
                    "cache": {
                        "type": "redis",
                        "ttl": 3600,
                    },
                }
            }
        )

    def get_examples(self) -> list[dict[str, Any]]:
        """Get list of examples.

        Returns:
            List of example configurations
        """
        return [
            {
                "title": "Simple",
                "description": "Simple tree structure",
                "callback": self.example_simple,
            },
            {
                "title": "With Emojis",
                "description": "Tree with emojis for files and folders",
                "callback": self.example_with_emojis,
            },
            {
                "title": "With Formatting",
                "description": "Tree with inline formatting (@color)",
                "callback": self.example_with_formatting,
            },
            {
                "title": "Deep Nesting",
                "description": "Tree with deep nesting (5 levels)",
                "callback": self.example_deep_nesting,
            },
            {
                "title": "With Values",
                "description": "Tree showing configuration values",
                "callback": self.example_with_values,
            },
            {
                "title": "Mixed Structure",
                "description": "Tree with mixed files and folders with emojis",
                "callback": self.example_mixed_structure,
            },
            {
                "title": "With Paths",
                "description": "Tree with clickable file paths (@path)",
                "callback": self.example_with_paths,
            },
            {
                "title": "With Indentation",
                "description": "Trees at different indentation levels",
                "callback": self.example_with_indentation,
            },
            {
                "title": "Nesting",
                "description": "Tree with parent/child nesting",
                "callback": self.example_nesting,
            },
        ]
