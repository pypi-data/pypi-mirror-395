"""测试 get_issue_attachments 异步工具.

遵循G7E6标准：
- AAA模式（Arrange-Act-Assert）
- pytest + pytest-mock框架
- 覆盖率目标：≥50%
"""
import os
import pytest
from unittest.mock import Mock, AsyncMock
from jira_mcp.server import get_issue_attachments


class TestGetIssueAttachmentsAsync:
    """测试 get_issue_attachments 异步函数."""

    @pytest.mark.asyncio
    async def test_list_attachments_without_download(self, mocker):
        """测试 download=False 时列出附件信息."""
        # Arrange - 准备测试数据
        mock_client = Mock()
        mock_issue = Mock()
        mock_attachment = Mock()
        mock_attachment.id = "10001"
        mock_attachment.filename = "test.png"
        mock_attachment.size = 12345
        mock_attachment.mimeType = "image/png"
        mock_attachment.created = "2025-01-24T10:00:00.000+0800"
        mock_attachment.updated = "2025-01-24T10:00:00.000+0800"
        mock_attachment.content = "http://jira.example.com/attachment/10001"

        mock_issue.fields.attachment = [mock_attachment]
        mock_client.issue.return_value = mock_issue

        mocker.patch("jira_mcp.server.get_jira_client", return_value=mock_client)
        mocker.patch("os.path.exists", return_value=False)

        # Act - 执行测试
        result = await get_issue_attachments("TEST-123", download=False)

        # Assert - 验证结果
        assert result["issue_key"] == "TEST-123"
        assert result["total"] == 1
        assert len(result["attachments"]) == 1
        assert result["attachments"][0]["filename"] == "test.png"
        assert result["attachments"][0]["size"] == 12345
        assert result["attachments"][0]["exists_locally"] is False

    @pytest.mark.asyncio
    async def test_download_attachments_calls_download_all(self, mocker):
        """测试 download=True 时正确调用 download_all_attachments."""
        # Arrange - 准备测试数据
        expected_result = {
            "issue_key": "TEST-123",
            "total": 2,
            "success": 2,
            "failed": 0,
            "downloads": [
                {"filename": "file1.pdf", "size": 1000},
                {"filename": "file2.png", "size": 2000}
            ]
        }

        mock_download = mocker.patch(
            "jira_mcp.server.download_all_attachments",
            new_callable=AsyncMock,
            return_value=expected_result
        )

        # Act - 执行测试
        result = await get_issue_attachments("TEST-123", download=True)

        # Assert - 验证调用和返回
        mock_download.assert_called_once_with("TEST-123")
        assert result == expected_result
        assert result["issue_key"] == "TEST-123"
        assert result["success"] == 2

    @pytest.mark.asyncio
    async def test_no_attachments_returns_empty_list(self, mocker):
        """测试无附件时返回空列表."""
        # Arrange - 准备测试数据
        mock_client = Mock()
        mock_issue = Mock()
        mock_issue.fields.attachment = []
        mock_client.issue.return_value = mock_issue

        mocker.patch("jira_mcp.server.get_jira_client", return_value=mock_client)

        # Act - 执行测试
        result = await get_issue_attachments("TEST-123")

        # Assert - 验证结果
        assert result["total"] == 0
        assert result["attachments"] == []
        assert result["issue_key"] == "TEST-123"

    @pytest.mark.asyncio
    async def test_exception_handling_returns_error(self, mocker):
        """测试异常处理返回错误信息."""
        # Arrange - 准备测试数据
        mock_client = Mock()
        mock_client.issue.side_effect = Exception("JIRA API error")
        mocker.patch("jira_mcp.server.get_jira_client", return_value=mock_client)

        # Act - 执行测试
        result = await get_issue_attachments("TEST-123")

        # Assert - 验证错误信息
        assert "error" in result
        assert "JIRA API error" in result["error"]

    @pytest.mark.asyncio
    async def test_attachment_exists_locally_flag(self, mocker):
        """测试本地附件存在性检查."""
        # Arrange - 准备测试数据
        mock_client = Mock()
        mock_issue = Mock()
        mock_attachment = Mock()
        mock_attachment.id = "10001"
        mock_attachment.filename = "existing.pdf"
        mock_attachment.size = 5000
        mock_attachment.mimeType = "application/pdf"
        mock_attachment.created = "2025-01-24T10:00:00.000+0800"
        mock_attachment.updated = "2025-01-24T10:00:00.000+0800"
        mock_attachment.content = "http://jira.example.com/attachment/10001"

        mock_issue.fields.attachment = [mock_attachment]
        mock_client.issue.return_value = mock_issue

        mocker.patch("jira_mcp.server.get_jira_client", return_value=mock_client)
        mocker.patch("os.path.exists", return_value=True)  # 模拟文件已存在

        # Act - 执行测试
        result = await get_issue_attachments("TEST-123", download=False)

        # Assert - 验证本地存在标志
        assert result["attachments"][0]["exists_locally"] is True
        assert result["attachments"][0]["local_path"] is not None

    @pytest.mark.asyncio
    async def test_multiple_attachments(self, mocker):
        """测试多个附件的情况."""
        # Arrange - 准备测试数据
        mock_client = Mock()
        mock_issue = Mock()

        # 创建3个附件
        attachments = []
        for i in range(1, 4):
            mock_attachment = Mock()
            mock_attachment.id = f"1000{i}"
            mock_attachment.filename = f"file{i}.txt"
            mock_attachment.size = i * 1000
            mock_attachment.mimeType = "text/plain"
            mock_attachment.created = "2025-01-24T10:00:00.000+0800"
            mock_attachment.updated = "2025-01-24T10:00:00.000+0800"
            mock_attachment.content = f"http://jira.example.com/attachment/1000{i}"
            attachments.append(mock_attachment)

        mock_issue.fields.attachment = attachments
        mock_client.issue.return_value = mock_issue

        mocker.patch("jira_mcp.server.get_jira_client", return_value=mock_client)
        mocker.patch("os.path.exists", return_value=False)

        # Act - 执行测试
        result = await get_issue_attachments("TEST-456")

        # Assert - 验证多个附件
        assert result["total"] == 3
        assert len(result["attachments"]) == 3
        assert result["attachments"][0]["filename"] == "file1.txt"
        assert result["attachments"][1]["filename"] == "file2.txt"
        assert result["attachments"][2]["filename"] == "file3.txt"

    @pytest.mark.asyncio
    async def test_issue_without_attachment_field(self, mocker):
        """测试 issue 对象没有 attachment 字段的情况."""
        # Arrange - 准备测试数据
        mock_client = Mock()
        mock_issue = Mock()
        # fields 存在但没有 attachment 属性
        mock_issue.fields = Mock(spec=[])
        mock_client.issue.return_value = mock_issue

        mocker.patch("jira_mcp.server.get_jira_client", return_value=mock_client)

        # Act - 执行测试
        result = await get_issue_attachments("TEST-789")

        # Assert - 验证返回空列表
        assert result["total"] == 0
        assert result["attachments"] == []
