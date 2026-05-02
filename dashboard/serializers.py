from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Project, Task, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'role']


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    members = UserSerializer(many=True, read_only=True)
    member_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        queryset=User.objects.all(),
        required=False,
    )

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'owner',
            'members',
            'member_ids',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['owner', 'members', 'created_at', 'updated_at']

    def create(self, validated_data):
        member_ids = validated_data.pop('member_ids', [])
        project = Project.objects.create(**validated_data)
        if member_ids:
            project.members.set(member_ids)
        return project

    def update(self, instance, validated_data):
        member_ids = validated_data.pop('member_ids', None)
        instance = super().update(instance, validated_data)
        if member_ids is not None:
            instance.members.set(member_ids)
        return instance


class TaskSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    assignee = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
    )
    assignee_name = serializers.SerializerMethodField()
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'project',
            'project_name',
            'title',
            'description',
            'assignee',
            'assignee_name',
            'status',
            'priority',
            'due_date',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at', 'project_name', 'assignee_name']

    def get_assignee_name(self, obj):
        return obj.assignee.username if obj.assignee else None
