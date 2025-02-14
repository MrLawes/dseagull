import re
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-n', '--name', )

    def handle(self, *_, **options):

        project_name = settings.BASE_DIR.parts[-1]
        name = options['name']
        lower_name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()

        # 添加 model 文件
        Path(f"{settings.BASE_DIR}/app/models").mkdir(exist_ok=True)
        Path(f"{settings.BASE_DIR}/app/models/__init__.py").touch(exist_ok=True)
        Path(f"{settings.BASE_DIR}/app/models/{lower_name}.py").touch(exist_ok=True)
        modelpy = (f"from django.db import models\n"
                   f"from dseagull.models import BaseModel\n\n\n"
                   f"class {name}(BaseModel):\n"
                   f"    pass\n")
        Path(f"{settings.BASE_DIR}/app/models/{lower_name}.py").write_text(modelpy)

        # 添加 serializer 文件
        Path(f"{settings.BASE_DIR}/app/serializers").mkdir(exist_ok=True)
        Path(f"{settings.BASE_DIR}/app/serializers/__init__.py").touch(exist_ok=True)
        Path(f"{settings.BASE_DIR}/app/serializers/{lower_name}.py").touch(exist_ok=True)
        serializerpy = (f"from rest_framework.serializers import ModelSerializer\n"
                        f"from dseagull.serializers import DateTimeField\n\n"
                        f"from app.models.{lower_name} import {name}\n\n\n"
                        f"class {name}CreateSerializer(ModelSerializer):\n"
                        f"    create_at = DateTimeField(help_text='创建时间', format='%Y-%m-%d %H:%M:%S')  # todo\n\n"
                        f"    class Meta:\n"
                        f"        model = {name}\n"
                        f"        fields = (\n"
                        f"            'id', 'create_at',\n"
                        f"        )\n\n\n"
                        f"class {name}ListSerializer(ModelSerializer):\n"
                        f"    class Meta:\n"
                        f"        model = {name}\n"
                        f"        fields = (\n"
                        f"            'id',\n"
                        f"        )\n")
        Path(f"{settings.BASE_DIR}/app/serializers/{lower_name}.py").write_text(serializerpy)

        # 创建 view 文件
        Path(f"{settings.BASE_DIR}/app/views").mkdir(exist_ok=True)
        Path(f"{settings.BASE_DIR}/app/views/__init__.py").touch(exist_ok=True)
        Path(f"{settings.BASE_DIR}/app/views/{lower_name}.py").touch(exist_ok=True)
        viewpy = (f"from django_filters import rest_framework as filters\n"
                  f"from rest_framework.decorators import action\n"
                  f"from rest_framework.versioning import URLPathVersioning\n"
                  f"from rest_framework.viewsets import ModelViewSet\n\n"
                  f"from app.models.{lower_name} import {name}\n"
                  f"from app.serializers.{lower_name} import {name}CreateSerializer\n"
                  f"from app.serializers.{lower_name} import {name}ListSerializer\n"
                  f"from dseagull.filters import BaseFilterSet\n\n\n"
                  f"class {name}Filter(BaseFilterSet):\n"
                  f"    create_at = filters.CharFilter(help_text='创建时间', method='filter_datetime', )\n\n"
                  f"    class Meta:\n"
                  f"        model = {name}\n"
                  f"        fields = ('id',)\n\n\n"
                  f"class {name}ViewSet(ModelViewSet):\n"
                  f"    serializer_class = {name}CreateSerializer\n"
                  f"    queryset = {name}.objects.all()\n"
                  f"    filterset_class = {name}Filter\n"
                  f"    versioning_class = URLPathVersioning\n\n"
                  f"    def get_queryset(self):  # todo 请实现数据隔离\n"
                  f"        return super().get_queryset()\n\n"
                  f"    @action(methods=['get'], detail=False, serializer_class={name}ListSerializer, )\n"
                  f"    def paginator_list(self, request, *args, **kwargs):\n"
                  f"        return super().list(request=request, *args, **kwargs)\n")
        Path(f"{settings.BASE_DIR}/app/views/{lower_name}.py").write_text(viewpy)

        # 创建 routers 文件
        routers_path = Path(f"{settings.BASE_DIR}/{project_name}/routers.py")
        if not routers_path.exists():
            routers_path.touch()
            routerspy = ("from rest_framework import routers\n\n"
                         "router = routers.DefaultRouter()\n"
                         "router.trailing_slash = '/?'\n"
                         # f"router.routes[2].mapping['put'] = router.routes[2].mapping.pop('patch', None)\n"
                         "v1 = '^(?P<version>(1))'\n")
            routers_path.write_text(routerspy)
        write_text = read_text = routers_path.read_text()

        router_start_text = f'from app.views.{lower_name} import {name}ViewSet'
        if router_start_text not in read_text:
            write_text = f'{router_start_text}\n{write_text}'

        router_end_text = "router.register(f'{v1}/" + lower_name + f"s', {name}ViewSet, )"
        if router_end_text not in read_text:
            write_text = f'{write_text}\n{router_end_text}'

        routers_path.write_text(write_text)

        # 创建 testcase 文件
        Path(f"{settings.BASE_DIR}/app/tests").mkdir(exist_ok=True)
        Path(f"{settings.BASE_DIR}/app/tests/__init__.py").touch(exist_ok=True)
        Path(f"{settings.BASE_DIR}/app/tests/{lower_name}.py").touch(exist_ok=True)
        testcasepy = (f"import dseagull\n\n"
                      f"dseagull.django.setup('{project_name}.settings') # noqa\n\n"
                      f"from django.test.testcases import TestCase\n"
                      f"from rest_framework.test import APIClient\n\n\n"
                      f"class {name}TestCase(TestCase):\n"
                      f"    def test_cru(self):\n"
                      f"        client = APIClient()\n"
                      f"        r = client.post('/1/{lower_name}s/')\n"
                      f"        self.assertEqual(r.status_code, 201, r.data)\n"
                      f"        r = client.get('/1/{lower_name}s/')\n"
                      f"        self.assertEqual(r.status_code, 200, r.data)\n"
                      f"        self.assertEqual(r.data['paging']['total'], 1, r.data)\n")
        Path(f"{settings.BASE_DIR}/app/tests/{lower_name}.py").write_text(testcasepy)
        tests_path = Path(f"{settings.BASE_DIR}/app/tests/tests.py")
        tests_path.touch(exist_ok=True)
        read_text = tests_path.read_text()
        add_read_text = f"from app.tests.{lower_name} import {name}TestCase  # noqa"
        if add_read_text not in read_text:
            tests_path.write_text(f'{add_read_text}\n{read_text}')
