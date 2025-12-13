from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Iterator, Optional

from nsj_rest_lib2.compiler.edl_model.entity_model import EntityModel
from nsj_rest_lib2.compiler.edl_model.entity_model_base import EntityModelBase
from nsj_rest_lib2.compiler.model import CompilerResult
from nsj_rest_lib2.compiler.util.type_naming_util import compile_namespace_keys
from nsj_rest_lib2.redis_config import set_redis
from nsj_rest_lib2.settings import ESCOPO_RESTLIB2


class EntityConfigWriter:
    """
    Serializa o resultado da compilação e publica no Redis usando o mesmo
    layout consumido pelo EntityLoader.
    """

    def __init__(self, escopo: str = ESCOPO_RESTLIB2) -> None:
        self._escopo = escopo or ESCOPO_RESTLIB2

    def publish(
        self,
        entity_model: EntityModelBase,
        compiler_result: CompilerResult,
        *,
        entity_hash: str | None = None,
    ) -> Dict[str, Any]:
        """
        Serializa e grava o resultado da compilação no Redis.

        :return: Payload serializado (útil para inspeção/testes).
        """

        payload = self.build_payload(
            entity_model, compiler_result, entity_hash=entity_hash
        )
        namespace_key = self._resolve_namespace_key(entity_model)
        resource = self._resolve_resource(entity_model)

        set_redis(
            "entity_config",
            self._escopo,
            namespace_key,
            resource,
            json.dumps(payload, ensure_ascii=False),
        )

        return payload

    def build_payload(
        self,
        entity_model: EntityModelBase,
        compiler_result: CompilerResult,
        *,
        entity_hash: str | None = None,
    ) -> Dict[str, Any]:
        """
        Constrói o dicionário serializável que representa a entidade compilada.
        """

        resource = self._resolve_resource(entity_model)
        relations = [
            rd.to_dict()
            for rd in (compiler_result.relations_dependencies or [])
        ]

        return {
            "dto_class_name": compiler_result.dto_class_name,
            "entity_class_name": compiler_result.entity_class_name,
            "insert_function_class_name": compiler_result.insert_function_class_name,
            "source_insert_function": compiler_result.source_insert_function,
            "update_function_class_name": compiler_result.update_function_class_name,
            "source_update_function": compiler_result.source_update_function,
            "source_dto": compiler_result.dto_code,
            "source_entity": compiler_result.entity_code,
            "entity_hash": entity_hash
            if entity_hash is not None
            else self._build_entity_hash(compiler_result),
            "api_expose": compiler_result.api_expose,
            "api_resource": resource,
            "api_verbs": compiler_result.api_verbs or [],
            "relations_dependencies": relations,
        }

    def _resolve_namespace_key(self, entity_model: EntityModelBase) -> str:
        tenant = getattr(entity_model, "tenant", None)
        grupo_empresarial = getattr(entity_model, "grupo_empresarial", None)

        grupo_key, tenant_key, default_key = compile_namespace_keys(
            tenant,
            grupo_empresarial,
        )

        if (
            tenant
            and tenant != 0
            and grupo_empresarial
            and str(grupo_empresarial) != "00000000-0000-0000-0000-000000000000"
        ):
            return grupo_key
        if tenant and tenant != 0:
            return tenant_key
        return default_key

    def _resolve_resource(self, entity_model: EntityModelBase) -> str:
        if not isinstance(entity_model, EntityModel) or not entity_model.api:
            raise ValueError(
                "EntityModel precisa possuir bloco de API para publicação no Redis."
            )
        if not entity_model.api.resource:
            raise ValueError("api.resource é obrigatório para publicação no Redis.")
        return entity_model.api.resource

    def _build_entity_hash(self, compiler_result: CompilerResult) -> str:
        hasher = hashlib.sha256()

        for content in self._iter_hash_chunks(
            compiler_result.dto_code,
            compiler_result.entity_code,
            compiler_result.source_insert_function,
            compiler_result.source_update_function,
        ):
            hasher.update(content)

        return hasher.hexdigest()

    @staticmethod
    def _iter_hash_chunks(*chunks: Optional[str]) -> Iterator[bytes]:
        for chunk in chunks:
            if chunk:
                yield chunk.encode("utf-8")
