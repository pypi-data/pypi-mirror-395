"""Merge Request 查询功能的单元测试.

遵循G7E6标准：
- AAA模式（Arrange-Act-Assert）
- pytest + pytest-mock框架
- 覆盖率目标：≥50%
"""
import pytest
from unittest.mock import Mock, patch
from jira_mcp.server import format_merge_request, get_merge_requests_by_jira_id


class TestFormatMergeRequest:
    """测试format_merge_request函数."""

    def test_format_merge_request_with_all_fields(self):
        """测试格式化包含所有字段的 MR 数据."""
        # Arrange - 准备测试数据
        mr_data = {
            "id": 123,
            "mr_id": 456,
            "mr_iid": 101,
            "project_name": "test-project",
            "project_with_namespace": "group/test-project",
            "title": "[CYTRD-22680] 修复登录问题",
            "source_branch": "CYTRD-22680-fix-login",
            "target_branch": "master",
            "state": "merged",
            "web_url": "https://gitlab.com/group/test-project/-/merge_requests/101",
            "author": "test_user",
            "created_time": "2025-11-30 10:00:00",
            "merged_time": "2025-11-30 11:00:00",
            "merged_by": "reviewer",
            "closed_time": None,
            "commit_count": 5,
            "additions": 100,
            "deletions": 20,
            "status": 0,
            "create_time": "2025-11-30 09:00:00",
            "update_time": "2025-11-30 11:00:00"
        }

        # Act - 执行测试
        result = format_merge_request(mr_data)

        # Assert - 验证结果（只包含需要的字段）
        assert result["mr_iid"] == 101
        assert result["project_name"] == "test-project"
        assert result["project_with_namespace"] == "group/test-project"
        assert result["title"] == "[CYTRD-22680] 修复登录问题"
        assert result["source_branch"] == "CYTRD-22680-fix-login"
        assert result["target_branch"] == "master"
        assert result["state"] == "merged"
        assert result["web_url"] == "https://gitlab.com/group/test-project/-/merge_requests/101"
        assert result["author"] == "test_user"
        assert result["created_time"] == "2025-11-30 10:00:00"
        assert result["merged_time"] == "2025-11-30 11:00:00"
        assert result["merged_by"] == "reviewer"
        assert result["closed_time"] is None
        assert result["commit_count"] == 5
        assert result["additions"] == 100
        assert result["deletions"] == 20

        # 验证内部字段被过滤
        assert "id" not in result
        assert "mr_id" not in result
        assert "status" not in result
        assert "create_time" not in result
        assert "update_time" not in result

    def test_format_merge_request_with_missing_fields(self):
        """测试格式化缺少某些字段的 MR 数据."""
        # Arrange
        mr_data = {
            "mr_iid": 102,
            "title": "[CYTRD-22681] 测试功能",
            "state": "opened"
        }

        # Act
        result = format_merge_request(mr_data)

        # Assert - 验证缺失字段返回 None
        assert result["mr_iid"] == 102
        assert result["title"] == "[CYTRD-22681] 测试功能"
        assert result["state"] == "opened"
        assert result["project_name"] is None
        assert result["author"] is None
        assert result["merged_time"] is None


class TestGetMergeRequestsByJiraId:
    """测试get_merge_requests_by_jira_id工具函数."""

    def test_get_merge_requests_by_jira_id_success(self, mocker):
        """测试成功获取 MR."""
        # Arrange - 准备 Mock 响应
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "total": 2,
            "query": "CYTRD-22680",
            "data": [
                {
                    "mr_iid": 101,
                    "project_name": "test-project",
                    "title": "[CYTRD-22680] 修复问题",
                    "source_branch": "CYTRD-22680-fix",
                    "target_branch": "master",
                    "state": "merged",
                    "web_url": "https://gitlab.com/...",
                    "author": "test_user",
                    "created_time": "2025-11-30 10:00:00",
                    "merged_time": "2025-11-30 11:00:00",
                    "additions": 100,
                    "deletions": 20
                },
                {
                    "mr_iid": 102,
                    "project_name": "test-project",
                    "title": "[CYTRD-22680] 另一个修复",
                    "source_branch": "CYTRD-22680-another-fix",
                    "target_branch": "develop",
                    "state": "opened",
                    "web_url": "https://gitlab.com/...",
                    "author": "another_user",
                    "created_time": "2025-11-30 12:00:00",
                    "additions": 50,
                    "deletions": 10
                }
            ]
        }
        mocker.patch("jira_mcp.server.requests.get", return_value=mock_response)

        # Act
        result = get_merge_requests_by_jira_id("CYTRD-22680")

        # Assert
        assert result["success"] is True
        assert result["total"] == 2
        assert result["query"] == "CYTRD-22680"
        assert len(result["merge_requests"]) == 2
        assert result["merge_requests"][0]["mr_iid"] == 101
        assert result["merge_requests"][1]["mr_iid"] == 102

    def test_get_merge_requests_by_jira_id_no_results(self, mocker):
        """测试无匹配结果的情况."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "total": 0,
            "query": "CYTRD-99999",
            "data": []
        }
        mocker.patch("jira_mcp.server.requests.get", return_value=mock_response)

        # Act
        result = get_merge_requests_by_jira_id("CYTRD-99999")

        # Assert
        assert result["success"] is True
        assert result["total"] == 0
        assert len(result["merge_requests"]) == 0

    def test_get_merge_requests_by_jira_id_with_limit(self, mocker):
        """测试带 limit 参数的查询."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "total": 1,
            "query": "22680",
            "data": [
                {
                    "mr_iid": 101,
                    "title": "[CYTRD-22680] 测试",
                    "state": "merged"
                }
            ]
        }
        mock_get = mocker.patch("jira_mcp.server.requests.get", return_value=mock_response)

        # Act
        result = get_merge_requests_by_jira_id("22680", limit=100)

        # Assert
        assert result["success"] is True
        # 验证 API 调用时传入了正确的参数
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        assert call_args[1]["params"]["jira_id"] == "22680"
        assert call_args[1]["params"]["limit"] == 100

    def test_get_merge_requests_by_jira_id_invalid_limit_too_small(self):
        """测试 limit 参数过小."""
        # Arrange & Act
        result = get_merge_requests_by_jira_id("CYTRD-22680", limit=0)

        # Assert
        assert "error" in result
        assert "limit must be between 1 and 200" in result["error"]

    def test_get_merge_requests_by_jira_id_invalid_limit_too_large(self):
        """测试 limit 参数过大."""
        # Arrange & Act
        result = get_merge_requests_by_jira_id("CYTRD-22680", limit=201)

        # Assert
        assert "error" in result
        assert "limit must be between 1 and 200" in result["error"]

    def test_get_merge_requests_by_jira_id_empty_jira_id(self):
        """测试空的 jira_id."""
        # Arrange & Act
        result = get_merge_requests_by_jira_id("")

        # Assert
        assert "error" in result
        assert "jira_id cannot be empty" in result["error"]

    def test_get_merge_requests_by_jira_id_whitespace_jira_id(self):
        """测试只包含空白字符的 jira_id."""
        # Arrange & Act
        result = get_merge_requests_by_jira_id("   ")

        # Assert
        assert "error" in result
        assert "jira_id cannot be empty" in result["error"]

    def test_get_merge_requests_by_jira_id_connection_error(self, mocker):
        """测试连接失败."""
        # Arrange
        import requests
        mocker.patch(
            "jira_mcp.server.requests.get",
            side_effect=requests.exceptions.ConnectionError("Connection refused")
        )

        # Act
        result = get_merge_requests_by_jira_id("CYTRD-22680")

        # Assert
        assert "error" in result
        assert "Cannot connect to DevLake service" in result["error"]

    def test_get_merge_requests_by_jira_id_timeout(self, mocker):
        """测试超时."""
        # Arrange
        import requests
        mocker.patch(
            "jira_mcp.server.requests.get",
            side_effect=requests.exceptions.Timeout("Request timeout")
        )

        # Act
        result = get_merge_requests_by_jira_id("CYTRD-22680")

        # Assert
        assert "error" in result
        assert "DevLake service timeout" in result["error"]

    def test_get_merge_requests_by_jira_id_http_error(self, mocker):
        """测试 HTTP 错误状态码."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 500
        mocker.patch("jira_mcp.server.requests.get", return_value=mock_response)

        # Act
        result = get_merge_requests_by_jira_id("CYTRD-22680")

        # Assert
        assert "error" in result
        assert "DevLake API error: 500" in result["error"]

    def test_get_merge_requests_by_jira_id_api_error_response(self, mocker):
        """测试 API 返回错误."""
        # Arrange
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": False,
            "error": "Missing required parameter: jira_id"
        }
        mocker.patch("jira_mcp.server.requests.get", return_value=mock_response)

        # Act
        result = get_merge_requests_by_jira_id("CYTRD-22680")

        # Assert
        assert "error" in result
        assert "Missing required parameter: jira_id" in result["error"]

    def test_get_merge_requests_by_jira_id_json_decode_error(self, mocker):
        """测试 JSON 解析错误."""
        # Arrange
        import requests
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = requests.exceptions.JSONDecodeError("Expecting value", "", 0)
        mocker.patch("jira_mcp.server.requests.get", return_value=mock_response)

        # Act
        result = get_merge_requests_by_jira_id("CYTRD-22680")

        # Assert - JSON 解码错误会被通用异常捕获
        assert "error" in result
        assert "Expecting value" in result["error"] or "获取 MR 失败" in result["error"]
