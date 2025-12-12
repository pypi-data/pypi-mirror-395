from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ServiceDeploymentRequest")


@_attrs_define
class ServiceDeploymentRequest:
    """ECS Service Deployment Request.

    Attributes:
        image (str): The container image to use for the service
        force (Union[None, Unset, bool]): Force deployment of same image Default: False.
        secret_arns (Union[None, Unset, list[str]]): List of secret ARNs to attach to the service
    """

    image: str
    force: Union[None, Unset, bool] = False
    secret_arns: Union[None, Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        image = self.image

        force: Union[None, Unset, bool]
        if isinstance(self.force, Unset):
            force = UNSET
        else:
            force = self.force

        secret_arns: Union[None, Unset, list[str]]
        if isinstance(self.secret_arns, Unset):
            secret_arns = UNSET
        elif isinstance(self.secret_arns, list):
            secret_arns = self.secret_arns

        else:
            secret_arns = self.secret_arns

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "image": image,
            }
        )
        if force is not UNSET:
            field_dict["force"] = force
        if secret_arns is not UNSET:
            field_dict["secret_arns"] = secret_arns

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        image = d.pop("image")

        def _parse_force(data: object) -> Union[None, Unset, bool]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, bool], data)

        force = _parse_force(d.pop("force", UNSET))

        def _parse_secret_arns(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                secret_arns_type_0 = cast(list[str], data)

                return secret_arns_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        secret_arns = _parse_secret_arns(d.pop("secret_arns", UNSET))

        service_deployment_request = cls(
            image=image,
            force=force,
            secret_arns=secret_arns,
        )

        service_deployment_request.additional_properties = d
        return service_deployment_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
