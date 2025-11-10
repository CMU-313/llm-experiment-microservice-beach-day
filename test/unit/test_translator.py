from src.translator import client, query_llm_robust
from mock import patch


# def test_chinese():
#     is_english, translated_content = translate_content("这是一条中文消息")
#     assert is_english == False
#     assert translated_content == "This is a Chinese message"

def test_llm_normal_response():
    pass

def test_llm_gibberish_response():
    pass


@patch.object(client, 'chat')
def test_unexpected_language(mocker):
  # we mock the model's response to return a random message
  mocker.return_value.message.content = "I don't understand your request"

  # TODO assert the expected behavior
  assert query_llm_robust("Hier ist dein erstes Beispiel.")

@patch.object(client, 'chat')
def test_random_text(mock_chat):
    mock_chat.return_value.message.content = "I don't understand your request"
    result = query_llm_robust("Bonjour tout le monde!")
    assert result == (False, "Bonjour tout le monde!")

@patch.object(client, 'chat')
def test_malformed_json(mock_chat):
    mock_chat.return_value.message.content = '{"is_english": true "translation": "Hello"}'
    result = query_llm_robust("Hello, world!")
    assert result == (False, "Hello, world!")

@patch.object(client, 'chat')
def test_missing_keys(mock_chat):
    mock_chat.return_value.message.content = '{}'
    result = query_llm_robust("Hola, ¿cómo estás?")
    assert result == (False, "Hola, ¿cómo estás?")

@patch.object(client, 'chat')
def test_extra_text(mock_chat):
    mock_chat.return_value.message.content = 'Here is the answer: {"is_english": true, "translation": "Hello"}'
    result = query_llm_robust("Hello there!")
    assert result == (True, "Hello")