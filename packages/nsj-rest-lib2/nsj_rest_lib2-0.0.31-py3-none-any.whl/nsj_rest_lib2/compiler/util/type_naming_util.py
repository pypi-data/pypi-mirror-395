import uuid
from typing import Iterable

from nsj_rest_lib2.compiler.util.str_util import CompilerStrUtil


def compile_namespace_keys(
    tenant: str | int | None, grupo_empresarial: str | uuid.UUID | None
) -> tuple[str, str, str]:
    grupo_key = f"tenant_{tenant}.ge_{grupo_empresarial}"
    tenant_key = f"tenant_{tenant}"
    default_key = "default"

    return (grupo_key, tenant_key, default_key)


def compile_dto_class_name(entity_id: str, prefx_class_name: str = "") -> str:
    return f"{CompilerStrUtil.to_pascal_case(prefx_class_name)}{CompilerStrUtil.to_pascal_case(entity_id)}DTO"


def compile_entity_class_name(entity_id: str, prefx_class_name: str = "") -> str:
    return f"{CompilerStrUtil.to_pascal_case(prefx_class_name)}{CompilerStrUtil.to_pascal_case(entity_id)}Entity"


def compile_function_class_name(
    entity_id: str,
    prefx_class_name: str,
    path_parts: Iterable[str],
    operation: str,
) -> str:
    """
    Gera o nome da classe para FunctionTypes (insert/update),
    incorporando o caminho dos relacionamentos (quando houver).
    """

    suffix = "InsertType" if operation == "insert" else "UpdateType"
    path_suffix = "".join(CompilerStrUtil.to_pascal_case(part) for part in path_parts)
    return (
        f"{CompilerStrUtil.to_pascal_case(prefx_class_name)}"
        f"{CompilerStrUtil.to_pascal_case(entity_id)}"
        f"{path_suffix}"
        f"{suffix}"
    )
