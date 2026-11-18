"""RF05: persistência, reentrega, falha e isolamento de mensagens inválidas."""
import json
import tempfile
import unittest
import uuid
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch
import worker


class WorkerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = patch.object(worker, 'JOBS', Path(self.tmp.name))
        self.path.start()
        self.addCleanup(self.path.stop)
        self.channel = Mock()
        self.method = SimpleNamespace(delivery_tag=7)
        self.jid = str(uuid.uuid4())
        self.body = json.dumps({'job_id': self.jid, 'seed': 42}).encode()

    def process(self, body=None):
        worker.process_message(self.channel, self.method, None, self.body if body is None else body)

    def saved(self):
        return json.loads((Path(self.tmp.name)/(self.jid+'.json')).read_text())

    def test_redelivery_republishes_without_retraining(self):
        with patch.object(worker, 'train', return_value={'test_accuracy': .9}) as train:
            self.process()
            self.process()
            train.assert_called_once_with(job_id=self.jid, seed=42)
        self.assertEqual('completed', self.saved()['status'])
        self.assertEqual(2, self.channel.basic_ack.call_count)

    def test_training_failure_is_persisted_and_does_not_loop(self):
        with patch.object(worker, 'train', side_effect=RuntimeError('internal details')) as train:
            self.process()
            self.process()
            train.assert_called_once()
        self.assertEqual('failed', self.saved()['status'])
        self.assertEqual('RuntimeError', self.saved()['error'])

    def test_failed_result_publish_leaves_message_unacknowledged(self):
        self.channel.basic_publish.side_effect = [None, OSError('broker disconnected')]
        with patch.object(worker, 'train', return_value={}) as train:
            with self.assertRaises(OSError):
                self.process()
            self.channel.basic_ack.assert_not_called()
            self.assertEqual('completed', self.saved()['status'])
            self.channel.basic_publish.side_effect = None
            self.process()
            train.assert_called_once()
        self.channel.basic_ack.assert_called_once_with(delivery_tag=7)

    def test_invalid_messages_are_quarantined_without_training(self):
        bad = [b'not json', b'[]', b'null', b'{}', b'\xff',
               b'{"job_id":"../escape"}',
               json.dumps({'job_id':self.jid,'seed':-1}).encode(),
               json.dumps({'job_id':self.jid,'seed':True}).encode()]
        with patch.object(worker, 'train') as train:
            for body in bad:
                with self.subTest(body=body):
                    self.process(body)
                    self.assertEqual('ml.training.invalid', self.channel.basic_publish.call_args.kwargs['routing_key'])
            train.assert_not_called()
        self.assertEqual(len(bad), self.channel.basic_ack.call_count)

    def test_quarantine_failure_does_not_ack_or_discard_message(self):
        self.channel.basic_publish.side_effect = OSError('broker offline')
        with self.assertRaises(OSError):
            self.process(b'bad json')
        self.channel.basic_ack.assert_not_called()


if __name__ == '__main__':
    unittest.main()
