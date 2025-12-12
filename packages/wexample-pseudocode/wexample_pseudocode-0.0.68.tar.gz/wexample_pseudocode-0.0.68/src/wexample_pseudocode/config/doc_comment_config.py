from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from wexample_pseudocode.config.doc_comment_parameter_config import (
    DocCommentParameterConfig,
)
from wexample_pseudocode.config.doc_comment_return_config import DocCommentReturnConfig

if TYPE_CHECKING:
    from wexample_pseudocode.config.doc_comment_parameter_config import (
        DocCommentParameterConfig,
    )
    from wexample_pseudocode.config.doc_comment_return_config import (
        DocCommentReturnConfig,
    )


@dataclass
class DocCommentConfig:
    description: str | None = None
    parameters: list[DocCommentParameterConfig] = field(default_factory=list)
    returns: DocCommentReturnConfig | None = None
