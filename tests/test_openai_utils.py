from types import SimpleNamespace
from unittest.mock import patch
import sys

# Provide dummy openai module if not installed
sys.modules.setdefault('openai', SimpleNamespace(ChatCompletion=SimpleNamespace(create=lambda **_: None)))

from travel_explorer.openai_utils import translate_to_sql


def test_translate_to_sql():
    mock_response = {
        'choices': [{
            'message': {'content': 'SELECT * FROM bookings;'}
        }]
    }
    with patch('openai.ChatCompletion.create', return_value=mock_response) as mock_create:
        sql = translate_to_sql('all bookings')
        mock_create.assert_called_once()
        assert sql == 'SELECT * FROM bookings;'
