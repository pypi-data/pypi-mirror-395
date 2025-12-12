from ..models.profile import (
    FetchProfile,
    PrivacySettings,
    ProfileName,
    ProfilePicture,
    ProfileStatus,
)


class ProfileService:
    def __init__(self, client):
        self.client = client

    def fetch_business_profile(self, instance_id: str, data: FetchProfile, instance_token: str):
        return self.client.post(
            f"chat/fetchBusinessProfile/{instance_id}",
            data=data.__dict__,
            instance_token=instance_token,
        )

    def fetch_profile(self, instance_id: str, data: FetchProfile, instance_token: str):
        return self.client.post(
            f"chat/fetchProfile/{instance_id}", data=data.__dict__, instance_token=instance_token
        )

    def update_profile_name(self, instance_id: str, data: ProfileName, instance_token: str):
        return self.client.post(
            f"chat/updateProfileName/{instance_id}",
            data=data.__dict__,
            instance_token=instance_token,
        )

    def update_profile_status(self, instance_id: str, data: ProfileStatus, instance_token: str):
        return self.client.post(
            f"chat/updateProfileStatus/{instance_id}",
            data=data.__dict__,
            instance_token=instance_token,
        )

    def update_profile_picture(self, instance_id: str, data: ProfilePicture, instance_token: str):
        return self.client.post(
            f"chat/updateProfilePicture/{instance_id}",
            data=data.__dict__,
            instance_token=instance_token,
        )

    def remove_profile_picture(self, instance_id: str, instance_token: str):
        return self.client.delete(
            f"chat/removeProfilePicture/{instance_id}", instance_token=instance_token
        )

    def fetch_privacy_settings(self, instance_id: str, instance_token: str):
        return self.client.get(
            f"chat/fetchPrivacySettings/{instance_id}", instance_token=instance_token
        )

    def update_privacy_settings(self, instance_id: str, data: PrivacySettings, instance_token: str):
        return self.client.post(
            f"chat/updatePrivacySettings/{instance_id}",
            data=data.__dict__,
            instance_token=instance_token,
        )
