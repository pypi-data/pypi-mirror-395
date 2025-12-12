import datetime
from collections.abc import Mapping
from typing import (
    Any,
    TypeVar,
    Union,
    cast,
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.script_type import ScriptType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ScriptResponse")


@_attrs_define
class ScriptResponse:
    """
    Attributes:
        active (bool): Whether the profile is active and may be used to run scripts
        created_by (UUID): The ID of the identity who created the profile
        date_added (datetime.datetime): The date the entity was added
        date_updated (datetime.datetime): The date the entity was updated
        description (str): The description of the script
        entry_point (str): The entry point of the script. Will usually be the path to a python file in the uploaded
            tarball
        id (UUID): The uniqueID of the entity
        name (str): The name of the script
        script_type (ScriptType): The type of the script. Use 'batch' for batch pipelines and 'interactive' for
            notebooks
        script_url (str): The URL where the script can be accessed if interactive
        version (int): The current version of the profile
        workspace_id (UUID): The ID of the workspace the script belongs to
        next_scheduled_run (Union[None, Unset, datetime.datetime]): The next scheduled run of the script, is None if no
            schedule is set
        profile (Union[None, Unset, str]): The name of the profile to use for the script
        public_secret (Union[None, UUID, Unset]): The secret UUID used to generate the public URL for this script
        public_url (Union[None, Unset, str]): The public URL where the script can be accessed without authentication, is
            None if not enabled
        schedule (Union[None, Unset, str]): The schedule of the script. Use 'cron' format for cron jobs
    """

    active: bool
    created_by: UUID
    date_added: datetime.datetime
    date_updated: datetime.datetime
    description: str
    entry_point: str
    id: UUID
    name: str
    script_type: ScriptType
    script_url: str
    version: int
    workspace_id: UUID
    next_scheduled_run: Union[None, Unset, datetime.datetime] = UNSET
    profile: Union[None, Unset, str] = UNSET
    public_secret: Union[None, UUID, Unset] = UNSET
    public_url: Union[None, Unset, str] = UNSET
    schedule: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        active = self.active

        created_by = str(self.created_by)

        date_added = self.date_added.isoformat()

        date_updated = self.date_updated.isoformat()

        description = self.description

        entry_point = self.entry_point

        id = str(self.id)

        name = self.name

        script_type = self.script_type.value

        script_url = self.script_url

        version = self.version

        workspace_id = str(self.workspace_id)

        next_scheduled_run: Union[None, Unset, str]
        if isinstance(self.next_scheduled_run, Unset):
            next_scheduled_run = UNSET
        elif isinstance(self.next_scheduled_run, datetime.datetime):
            next_scheduled_run = self.next_scheduled_run.isoformat()
        else:
            next_scheduled_run = self.next_scheduled_run

        profile: Union[None, Unset, str]
        if isinstance(self.profile, Unset):
            profile = UNSET
        else:
            profile = self.profile

        public_secret: Union[None, Unset, str]
        if isinstance(self.public_secret, Unset):
            public_secret = UNSET
        elif isinstance(self.public_secret, UUID):
            public_secret = str(self.public_secret)
        else:
            public_secret = self.public_secret

        public_url: Union[None, Unset, str]
        if isinstance(self.public_url, Unset):
            public_url = UNSET
        else:
            public_url = self.public_url

        schedule: Union[None, Unset, str]
        if isinstance(self.schedule, Unset):
            schedule = UNSET
        else:
            schedule = self.schedule

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "active": active,
                "created_by": created_by,
                "date_added": date_added,
                "date_updated": date_updated,
                "description": description,
                "entry_point": entry_point,
                "id": id,
                "name": name,
                "script_type": script_type,
                "script_url": script_url,
                "version": version,
                "workspace_id": workspace_id,
            }
        )
        if next_scheduled_run is not UNSET:
            field_dict["next_scheduled_run"] = next_scheduled_run
        if profile is not UNSET:
            field_dict["profile"] = profile
        if public_secret is not UNSET:
            field_dict["public_secret"] = public_secret
        if public_url is not UNSET:
            field_dict["public_url"] = public_url
        if schedule is not UNSET:
            field_dict["schedule"] = schedule

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        active = d.pop("active")

        created_by = UUID(d.pop("created_by"))

        date_added = isoparse(d.pop("date_added"))

        date_updated = isoparse(d.pop("date_updated"))

        description = d.pop("description")

        entry_point = d.pop("entry_point")

        id = UUID(d.pop("id"))

        name = d.pop("name")

        script_type = ScriptType(d.pop("script_type"))

        script_url = d.pop("script_url")

        version = d.pop("version")

        workspace_id = UUID(d.pop("workspace_id"))

        def _parse_next_scheduled_run(
            data: object,
        ) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                next_scheduled_run_type_0 = isoparse(data)

                return next_scheduled_run_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        next_scheduled_run = _parse_next_scheduled_run(
            d.pop("next_scheduled_run", UNSET)
        )

        def _parse_profile(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        profile = _parse_profile(d.pop("profile", UNSET))

        def _parse_public_secret(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                public_secret_type_0 = UUID(data)

                return public_secret_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        public_secret = _parse_public_secret(d.pop("public_secret", UNSET))

        def _parse_public_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        public_url = _parse_public_url(d.pop("public_url", UNSET))

        def _parse_schedule(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        schedule = _parse_schedule(d.pop("schedule", UNSET))

        script_response = cls(
            active=active,
            created_by=created_by,
            date_added=date_added,
            date_updated=date_updated,
            description=description,
            entry_point=entry_point,
            id=id,
            name=name,
            script_type=script_type,
            script_url=script_url,
            version=version,
            workspace_id=workspace_id,
            next_scheduled_run=next_scheduled_run,
            profile=profile,
            public_secret=public_secret,
            public_url=public_url,
            schedule=schedule,
        )

        script_response.additional_properties = d
        return script_response

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
