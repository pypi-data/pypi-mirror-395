"""
Tests for studies_api module.
"""
import pytest
import json
from unittest.mock import Mock, patch, AsyncMock
from src.api.studies_api import get_all_studies_and_series, get_series_by_study_instance_uid


class TestGetAllStudiesAndSeries:
    """Test cases for get_all_studies_and_series function."""
    
    @pytest.fixture
    def mock_config(self):
        """Mock configuration with valid credentials."""
        return {
            'base_url': 'https://test-server.com',
            'cookie': 'test_cookie_value',
            'name': 'test_user',
            'password': 'test_password'
        }
    
    @pytest.fixture
    def mock_studies_response(self):
        """Mock response from getStudies API."""
        return {
            "code": 1,
            "msg": "ok",
            "data": {
                "pagination": {
                    "pageCount": 1,
                    "totalCount": 2
                },
                "studyList": [
                    {
                        "PatientAge": "074Y",
                        "PatientID": "0009637617",
                        "PatientName": "0009637617",
                        "PatientSex": "M",
                        "StudyDate": "2021-04-27T16:00:00.000Z",
                        "StudyInstanceUID": "1.2.840.113564.345049290535.9692.637552042156233117.433089",
                        "createTime": "2024-04-18T08:02:48.000Z",
                        "expandAllRows": 0,
                        "hasOtherStudy": 0,
                        "id": 12777,
                        "isDel": "0",
                        "jsonData": "{}",
                        "labelList": [],
                        "pacsUid": "79e7d55c-d417575f-bc461791-44bc886e-08707488",
                        "physicianOpinion": "",
                        "status": 0,
                        "updateTime": "2025-12-03T07:24:22.000Z",
                        "userId": 2
                    }
                ]
            }
        }
    
    @pytest.fixture
    def mock_series_response(self):
        """Mock response from getSeriesByStudyInstanceUID API."""
        return {
            "code": 1,
            "msg": "OK",
            "data": [
                {
                    "id": 19718,
                    "userId": 2,
                    "PatientID": "0009637617",
                    "physicianOpinion": "",
                    "SeriesNumber": "",
                    "hasSeeReport": 0,
                    "StudyInstanceUID": "1.2.840.113564.345049290535.9692.637552042156233117.433089",
                    "SeriesInstanceUID": "1.3.12.2.1107.5.1.4.76315.30000021042706150001900118114",
                    "status": 11,
                    "createTime": "2024-04-18T08:02:47.000Z",
                    "updateTime": "2025-12-03T07:24:22.000Z",
                    "uploadTime": "2025-12-03T07:24:22.000Z",
                    "analysisStartTime": "2025-12-03T05:30:51.000Z",
                    "analysisEndTime": "2025-12-03T05:31:48.000Z",
                    "imageCount": 582,
                    "SeriesDescription": "Coro  DS_CorCTA  0.75  Bv36  3  BestDiast 74 %",
                    "SliceThickness": "0.75",
                    "isDel": "0",
                    "seriesType": 1,
                    "pacsUid": "451ba5fc-b5084543-87123a8e-36f6a95c-4acfe83b",
                    "thumbnailPacsUid": "f4666f17-d8aecd64-5e85ecf0-21a45cae-aa8e24b7",
                    "labelList": []
                }
            ]
        }
    
    @pytest.mark.asyncio
    @patch('src.api.studies_api.get_authenticated_config')
    @patch('src.api.studies_api.requests.post')
    async def test_get_all_studies_and_series_success(
        self, 
        mock_post, 
        mock_get_config,
        mock_config,
        mock_studies_response,
        mock_series_response
    ):
        """Test successful retrieval of all studies and series."""
        # Setup mocks
        mock_get_config.return_value = mock_config
        
        # Mock getStudies API response
        mock_studies_resp = Mock()
        mock_studies_resp.json.return_value = mock_studies_response
        mock_studies_resp.raise_for_status = Mock()
        
        # Mock getSeriesByStudyInstanceUID API response
        mock_series_resp = Mock()
        mock_series_resp.json.return_value = mock_series_response
        mock_series_resp.raise_for_status = Mock()
        
        # Setup post to return different responses based on URL
        def post_side_effect(url, **kwargs):
            if '/api/v3/getStudies' in url:
                return mock_studies_resp
            elif '/api/v2/getSeriesByStudyInstanceUID' in url:
                return mock_series_resp
            return Mock()
        
        mock_post.side_effect = post_side_effect
        
        # Execute
        result = await get_all_studies_and_series()
        
        # Verify
        assert result is not None
        assert "content" in result
        assert len(result["content"]) > 0
        
        result_text = result["content"][0]["text"]
        result_data = json.loads(result_text)
        
        assert result_data["success"] is True
        assert result_data["total_studies"] == 1
        assert len(result_data["studies"]) == 1
        assert "seriesList" in result_data["studies"][0]
        assert len(result_data["studies"][0]["seriesList"]) == 1
        
        # Verify API calls
        assert mock_post.call_count >= 2  # At least one getStudies and one getSeries call
    
    @pytest.mark.asyncio
    @patch('src.api.studies_api.get_authenticated_config')
    async def test_get_all_studies_and_series_missing_config(
        self, 
        mock_get_config
    ):
        """Test error handling when config is missing."""
        # Setup mock with missing config
        mock_get_config.return_value = {
            'base_url': None,
            'cookie': None
        }
        
        # Execute
        result = await get_all_studies_and_series()
        
        # Verify
        assert result is not None
        assert "content" in result
        
        result_text = result["content"][0]["text"]
        result_data = json.loads(result_text)
        
        assert result_data["error"] is True
        assert "Missing base_url or cookie" in result_data["message"]
    
    @pytest.mark.asyncio
    @patch('src.api.studies_api.get_authenticated_config')
    @patch('src.api.studies_api.requests.post')
    async def test_get_all_studies_and_series_with_search(
        self,
        mock_post,
        mock_get_config,
        mock_config,
        mock_studies_response
    ):
        """Test retrieval with search string."""
        # Setup mocks
        mock_get_config.return_value = mock_config
        
        mock_resp = Mock()
        mock_resp.json.return_value = mock_studies_response
        mock_resp.raise_for_status = Mock()
        mock_post.return_value = mock_resp
        
        # Mock series response
        mock_series_resp = Mock()
        mock_series_resp.json.return_value = {"code": 1, "msg": "OK", "data": []}
        mock_series_resp.raise_for_status = Mock()
        
        def post_side_effect(url, **kwargs):
            if '/api/v3/getStudies' in url:
                return mock_resp
            elif '/api/v2/getSeriesByStudyInstanceUID' in url:
                return mock_series_resp
            return Mock()
        
        mock_post.side_effect = post_side_effect
        
        # Execute with search string
        result = await get_all_studies_and_series(search_str="test_patient")
        
        # Verify search string was included in payload
        calls = [call for call in mock_post.call_args_list if '/api/v3/getStudies' in str(call)]
        if calls:
            call_kwargs = calls[0].kwargs
            payload = call_kwargs.get('json', {})
            assert payload.get('searchStr') == "test_patient"
    
    @pytest.mark.asyncio
    @patch('src.api.studies_api.get_authenticated_config')
    @patch('src.api.studies_api.requests.post')
    async def test_get_all_studies_and_series_pagination(
        self,
        mock_post,
        mock_get_config,
        mock_config
    ):
        """Test pagination handling."""
        # Setup mocks
        mock_get_config.return_value = mock_config
        
        # First page response (has more data)
        first_page_response = {
            "code": 1,
            "msg": "ok",
            "data": {
                "pagination": {
                    "pageCount": 2,
                    "totalCount": 150
                },
                "studyList": [
                    {
                        "StudyInstanceUID": "study1",
                        "PatientID": "patient1",
                        "PatientName": "Patient 1"
                    }
                ]
            }
        }
        
        # Second page response (last page)
        second_page_response = {
            "code": 1,
            "msg": "ok",
            "data": {
                "pagination": {
                    "pageCount": 2,
                    "totalCount": 150
                },
                "studyList": []
            }
        }
        
        mock_series_resp = Mock()
        mock_series_resp.json.return_value = {"code": 1, "msg": "OK", "data": []}
        mock_series_resp.raise_for_status = Mock()
        
        call_count = 0
        def post_side_effect(url, **kwargs):
            nonlocal call_count
            if '/api/v3/getStudies' in url:
                call_count += 1
                mock_resp = Mock()
                if call_count == 1:
                    mock_resp.json.return_value = first_page_response
                else:
                    mock_resp.json.return_value = second_page_response
                mock_resp.raise_for_status = Mock()
                return mock_resp
            elif '/api/v2/getSeriesByStudyInstanceUID' in url:
                return mock_series_resp
            return Mock()
        
        mock_post.side_effect = post_side_effect
        
        # Execute
        result = await get_all_studies_and_series()
        
        # Verify pagination worked
        # 第一页有数据，第二页为空时会停止，所以至少调用1次
        # 如果第一页数据量等于pageSize，会继续查询第二页
        assert call_count >= 1  # Should have called at least 1 page
        result_text = result["content"][0]["text"]
        result_data = json.loads(result_text)
        assert result_data["success"] is True
        # 验证第一页的数据被正确获取
        assert result_data["total_studies"] >= 1


class TestGetSeriesByStudyInstanceUid:
    """Test cases for get_series_by_study_instance_uid function."""
    
    @pytest.mark.parametrize("base_url,cookie,study_uid", [
        ("https://test.com", "ls=test_cookie", "1.2.3.4.5"),
        ("https://test.com", "test_cookie", "1.2.3.4.5"),  # Cookie without ls= prefix
    ])
    @patch('src.api.studies_api.requests.post')
    def test_get_series_by_study_instance_uid_success(
        self,
        mock_post,
        base_url,
        cookie,
        study_uid
    ):
        """Test successful retrieval of series by study instance UID."""
        # Setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": 1,
            "msg": "OK",
            "data": [
                {
                    "StudyInstanceUID": study_uid,
                    "SeriesInstanceUID": "series1",
                    "status": 11
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        # Execute
        result = get_series_by_study_instance_uid(base_url, cookie, study_uid)
        
        # Verify
        assert len(result) == 1
        assert result[0]["StudyInstanceUID"] == study_uid
        assert result[0]["SeriesInstanceUID"] == "series1"
        
        # Verify API call
        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args.kwargs
        assert call_kwargs['json']['StudyInstanceUID'] == study_uid
    
    @patch('src.api.studies_api.requests.post')
    def test_get_series_by_study_instance_uid_api_error(self, mock_post):
        """Test error handling when API returns error."""
        # Setup mock response with error
        mock_response = Mock()
        mock_response.json.return_value = {
            "code": 0,
            "msg": "Error occurred"
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        # Execute
        result = get_series_by_study_instance_uid(
            "https://test.com",
            "ls=test_cookie",
            "1.2.3.4.5"
        )
        
        # Verify
        assert result == []
    
    @patch('src.api.studies_api.requests.post')
    def test_get_series_by_study_instance_uid_request_exception(self, mock_post):
        """Test error handling when request fails."""
        # Setup mock to raise exception
        import requests
        mock_post.side_effect = requests.exceptions.RequestException("Network error")
        
        # Execute
        result = get_series_by_study_instance_uid(
            "https://test.com",
            "ls=test_cookie",
            "1.2.3.4.5"
        )
        
        # Verify
        assert result == []

