"""test utils file."""

import pytest
from assertpy import assert_that

from src.common.constants import CommonPaths
from src.core.utils import FileUtil


@pytest.mark.core
class TestUtils:
    """Unit Tests class to cover Utils methods."""

    def test_read_yaml_file(self):
        """Test: Validate read yaml file.

        :return:
        """
        file_path = CommonPaths.resource_path.joinpath("app_config.yml")
        file_content = FileUtil.read_yaml_file(file_path)
        # validation
        assert_that(file_content).is_not_none()
        assert_that(file_content).is_not_empty()
        assert_that(file_content).contains("host", "port")
