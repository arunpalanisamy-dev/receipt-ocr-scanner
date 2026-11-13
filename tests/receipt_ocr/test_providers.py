from unittest.mock import MagicMock, patch

import pytest

from receipt_ocr import OpenAIProvider


@patch("receipt_ocr.providers.OpenAI")
def test_provider_defaults_to_local_ollama(mock_openai_client_class, monkeypatch):
    monkeypatch.delenv("OLLAMA_BASE_URL", raising=False)

    provider = OpenAIProvider()

    assert provider.api_key == "ollama"
    assert provider.base_url == "http://localhost:11434/v1"
    mock_openai_client_class.assert_called_once_with(
        api_key="ollama", base_url="http://localhost:11434/v1"
    )


@patch("receipt_ocr.providers.OpenAI")
def test_get_response(mock_openai_client_class, dummy_image_path, mock_chat_completion):
    # Configure the mock OpenAI client that will be used by OpenAIProvider
    mock_openai_instance = MagicMock()
    mock_openai_client_class.return_value = mock_openai_instance

    provider = OpenAIProvider()

    mock_chat_completion.choices[
        0
    ].message.content = '{"merchant_name": "Test Merchant"}'
    mock_openai_instance.chat.completions.create.return_value = mock_chat_completion

    dummy_json_schema = {
        "type": "object",
        "properties": {"merchant_name": {"type": "string"}},
    }
    response = provider.get_response(
        dummy_image_path, json_schema=dummy_json_schema, model="qwen2.5vl:3b"
    )

    assert response.choices[0].message.content == '{"merchant_name": "Test Merchant"}'


@patch("receipt_ocr.providers.OpenAI")
def test_get_response_uses_local_default_model(
    mock_openai_client_class, dummy_image_path, mock_chat_completion, monkeypatch
):
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)
    mock_openai_instance = MagicMock()
    mock_openai_client_class.return_value = mock_openai_instance
    mock_openai_instance.chat.completions.create.return_value = mock_chat_completion
    provider = OpenAIProvider()

    provider.get_response(dummy_image_path, json_schema={"type": "object"})

    assert (
        mock_openai_instance.chat.completions.create.call_args.kwargs["model"]
        == "qwen2.5vl:3b"
    )


@patch("receipt_ocr.providers.OpenAI")
def test_get_response_api_error(mock_openai_client_class, dummy_image_path):
    mock_openai_instance = MagicMock()
    mock_openai_client_class.return_value = mock_openai_instance
    mock_openai_instance.chat.completions.create.side_effect = Exception("API Error")

    provider = OpenAIProvider()

    dummy_json_schema = {"type": "object"}

    with pytest.raises(Exception, match="API Error"):
        provider.get_response(
            dummy_image_path, json_schema=dummy_json_schema, model="gpt-4o"
        )


@patch("receipt_ocr.providers.OpenAI")
def test_get_response_json_schema_format(
    mock_openai_client_class, dummy_image_path, mock_chat_completion
):
    # Configure the mock OpenAI client
    mock_openai_instance = MagicMock()
    mock_openai_client_class.return_value = mock_openai_instance

    provider = OpenAIProvider()

    mock_chat_completion.choices[
        0
    ].message.content = '{"merchant_name": "Test Merchant"}'
    mock_openai_instance.chat.completions.create.return_value = mock_chat_completion

    dummy_json_schema = {
        "type": "object",
        "properties": {"merchant_name": {"type": "string"}},
    }
    provider.get_response(
        dummy_image_path,
        json_schema=dummy_json_schema,
        model="qwen2.5vl:3b",
        response_format_type="json_schema",
    )  # Verify the response_format was set correctly
    call_args = mock_openai_instance.chat.completions.create.call_args
    assert call_args[1]["response_format"] == {
        "type": "json_schema",
        "json_schema": {
            "name": "receipt_data",
            "schema": dummy_json_schema,
            "strict": True,
        },
    }


@patch("receipt_ocr.providers.OpenAI")
def test_get_response_text_format(
    mock_openai_client_class, dummy_image_path, mock_chat_completion
):
    # Configure the mock OpenAI client
    mock_openai_instance = MagicMock()
    mock_openai_client_class.return_value = mock_openai_instance

    provider = OpenAIProvider()

    mock_chat_completion.choices[0].message.content = "Merchant: Test Merchant"
    mock_openai_instance.chat.completions.create.return_value = mock_chat_completion

    dummy_json_schema = {
        "type": "object",
        "properties": {"merchant_name": {"type": "string"}},
    }
    provider.get_response(
        dummy_image_path,
        json_schema=dummy_json_schema,
        model="qwen2.5vl:3b",
        response_format_type="text",
    )

    # Verify the response_format was set to text
    call_args = mock_openai_instance.chat.completions.create.call_args
    assert call_args[1]["response_format"] == {"type": "text"}
