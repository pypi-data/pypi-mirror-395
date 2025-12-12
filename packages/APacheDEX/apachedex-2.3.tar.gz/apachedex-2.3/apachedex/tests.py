import unittest
import sys
import json
import bz2
import gzip
import io
import tempfile
import apachedex
import lzma


class ApacheDEXTestCase(unittest.TestCase):
  def setUp(self):
    self._original_sys_argv = sys.argv
    self._original_sys_stdin = sys.stdin
    self._original_sys_stderr = sys.stderr
    self._original_sys_stdout = sys.stdout
    self._stderr_bytes = io.BytesIO()
    sys.stderr = io.TextIOWrapper(self._stderr_bytes, write_through=True)
    self._stdout_bytes = io.BytesIO()
    sys.stdout = io.TextIOWrapper(self._stdout_bytes, write_through=True)

  def tearDown(self):
    sys.argv = self._original_sys_argv
    sys.stdin = self._original_sys_stdin
    sys.stderr = self._original_sys_stderr
    sys.stdout = self._original_sys_stdout


class TestFiles(ApacheDEXTestCase):
  def test(self):
    with tempfile.NamedTemporaryFile() as fin, tempfile.NamedTemporaryFile() as fout:
      fin.write(
        b'''127.0.0.1 - - [14/Jul/2017:09:41:41 +0200] "GET / HTTP/1.1" 200 7499 "https://example.org/" "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36" 1754'''
      )
      fin.flush()
      sys.argv = ['apachedex', '--base=/', fin.name, '--out', fout.name]
      apachedex.main()
      fout.flush()
      fout.seek(0)
      self.assertIn(b"<html>", fout.read())


class TestMalformedInput(ApacheDEXTestCase):
  def test_timestamp_mixed_in_timestamp(self):
    sys.argv = ['apachedex', '--base=/', '-']
    sys.stdin = io.TextIOWrapper(io.BytesIO(
    # this first line is valid, but second is not
    b'''127.0.0.1 - - [14/Jul/2017:09:41:41 +0200] "GET / HTTP/1.1" 200 7499 "https://example.org/" "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36" 1754
127.0.0.1 - - [14/Jul/2017:127.0.0.1 - - [14/Jul/2017:09:41:41 +0200] "GET / HTTP/1.1" 200 7499 "https://example.org/" "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36" 1754'''))
    apachedex.main()

    self.assertNotIn(b'Malformed line at -:1', self._stderr_bytes.getvalue())
    self.assertIn(b'Malformed line at -:2', self._stderr_bytes.getvalue())


class TestCharacterEncoding(ApacheDEXTestCase):
  def test_apache_referer_encoding(self):
    with tempfile.NamedTemporaryFile() as fin, tempfile.NamedTemporaryFile() as fout:
      # with apache, referer is "backslash escaped" (but quite often, referrer is %-encoded by user agent, like on
      # this example line taken from request-caddy-frontend-1/SOFTINST-49218_access_log-20190220 )
      fin.write(
        b'127.0.0.1 --  [19/Feb/2019:17:49:22 +0100] "POST /erp5/budget_module/20181219-2B1DB4A/1/Base_edit HTTP/1.1" 302 194 "https://example.org/erp5/budget_module/20181219-2B1DB4A/1/BudgetLine_viewSpreadsheet?selection_index=0&selection_name=budget_line_list_selection&ignore_layout:int=1&editable_mode=1&portal_status_message=Donn%C3%A9es%20enregistr%C3%A9es." "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36" 2999\n')
      fin.flush()
      sys.argv = ['apachedex', '--base=/', fin.name, '-f', 'json', '-o', fout.name]
      apachedex.main()
      self.assertNotIn(b'Malformed line', self._stderr_bytes.getvalue())
      with open(fout.name) as f:
        self.assertTrue(json.load(f))

  def test_caddy_referer_encoding(self):
    with tempfile.NamedTemporaryFile() as fin, tempfile.NamedTemporaryFile() as fout:
      # with caddy, referer is written "as is"
      fin.write(
        # this is an (anonymised) line from request-caddy-frontend-1/SOFTINST-49218_access_log-20190220
        b'127.0.0.1 - - [19/Feb/2019:17:49:22 +0100] "GET / HTTP/1.1" 200 741 "https://example.org/erp5/budget_module/20190219-1F39610/9/BudgetLine_viewSpreadsheet?selection_index=4&selection_name=budget_line_list_selection&ignore_layout:int=1&editable_mode=1&portal_status_message=Donn\xe9es%20enregistr\xe9es." "Mozilla/5.0 (Windows NT 10.0; Win64;x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134" 7')
      fin.flush()
      sys.argv = ['apachedex', '--base=/', fin.name, '-f', 'json', '-o', fout.name]
      apachedex.main()
      with open(fout.name) as f:
        self.assertTrue(json.load(f))


class EncodedInputTestMixin:
  DEFAULT_LINE = b'127.0.0.1 - - [14/Jul/2017:09:41:41 +0200] "GET / HTTP/1.1" 200 7499 "https://example.org/" "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36" 1754'

  def test(self):
    with tempfile.NamedTemporaryFile() as fin, tempfile.NamedTemporaryFile() as fout:
      fin.write(self._getInputData())
      fin.flush()
      sys.argv = ['apachedex', '--base=/', fin.name, '-f', 'json', '-o', fout.name]
      apachedex.main()
      self.assertNotIn(b'Malformed line', self._stderr_bytes.getvalue())
      with open(fout.name) as f:
        self.assertTrue(json.load(f))


class TestBzip2Encoding(ApacheDEXTestCase, EncodedInputTestMixin):
  def _getInputData(self):
    return bz2.compress(self.DEFAULT_LINE)


class TestZlibEncoding(ApacheDEXTestCase, EncodedInputTestMixin):
  def _getInputData(self):
    f = io.BytesIO()
    with gzip.GzipFile(mode="w", fileobj=f) as gzfile:
      gzfile.write(self.DEFAULT_LINE)
    return f.getvalue()


class TestLzmaEncoding(ApacheDEXTestCase, EncodedInputTestMixin):
  def _getInputData(self):
    return lzma.compress(self.DEFAULT_LINE)


class TestTimeEnconding(ApacheDEXTestCase):

  def test_seconds_timing(self):
    with tempfile.NamedTemporaryFile() as fin, tempfile.NamedTemporaryFile() as fout:
      fin.write(
        b'''127.0.0.1 - - [14/Jul/2017:09:41:41 +0200] "GET / HTTP/1.1" 200 7499 "https://example.org/" "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36" 1''')
      fin.flush()
      sys.argv = ['apachedex', '--base=/', fin.name, '--logformat', '%h %l %u %t "%r" %>s %O "%{Referer}i" "%{User-Agent}i" %T', '-f', 'json', '-o', fout.name]

      apachedex.main()

      fout.seek(0)
      state = json.load(fout)
      self.assertEqual(state[0][1]['apdex']['2017/07/14 09:41']['duration_max'], 1000000)

  def test_milliseconds_timing(self):
    with tempfile.NamedTemporaryFile() as fin, tempfile.NamedTemporaryFile() as fout:
      fin.write(
        b'''127.0.0.1 - - [14/Jul/2017:09:41:41 +0200] "GET / HTTP/1.1" 200 7499 "https://example.org/" "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36" 1000000''')
      fin.flush()
      sys.argv = ['apachedex', '--base=/', fin.name, '--logformat', '%h %l %u %t "%r" %>s %O "%{Referer}i" "%{User-Agent}i" %D', '-f', 'json', '-o', fout.name]

      apachedex.main()

      fout.seek(0)
      state = json.load(fout)
      self.assertEqual(state[0][1]['apdex']['2017/07/14 09:41']['duration_max'], 1000000)

  def test_microseconds_timing(self):
    with tempfile.NamedTemporaryFile() as fin, tempfile.NamedTemporaryFile() as fout:
      fin.write(
        b'''127.0.0.1 - - [14/Jul/2017:09:41:41 +0200] "GET / HTTP/1.1" 200 7499 "https://example.org/" "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36" 1000''')
      fin.flush()
      sys.argv = ['apachedex', '--base=/', fin.name, '--logformat', '%h %l %u %t "%r" %>s %O "%{Referer}i" "%{User-Agent}i" %{ms}T', '-f', 'json', '-o', fout.name]

      apachedex.main()
      fout.seek(0)
      state = json.load(fout)
      self.assertEqual(state[0][1]['apdex']['2017/07/14 09:41']['duration_max'], 1000000)

class TestSkipStatusCode(ApacheDEXTestCase):
  def _run(self, args, logline):
    with tempfile.NamedTemporaryFile() as fin, tempfile.NamedTemporaryFile() as fout:
      fin.write(logline)
      fin.flush()
      sys.argv = ['apachedex', '--base=/', fin.name, '--logformat', '%h %l %u %t "%r" %>s %O "%{Referer}i" "%{User-Agent}i" %{ms}T', '-f', 'json', '-o', fout.name] + args
      apachedex.main()
      with open(fout.name) as f:
        return json.load(f)

  def test_basic_skip_status_code(self):
    state = self._run(['--skip-status-code', '429'],
    b'''127.0.0.1 - - [14/Jul/2017:09:41:41 +0200] "GET / HTTP/1.1" 429 7499 "https://example.org/" "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36" 1000''')
    self.assertEqual(len(state), 0)

  def test_multiple_skip_status_code(self):
    state = self._run(['--skip-status-code', '429', '--skip-status-code', '499'],
    b'''127.0.0.1 - - [14/Jul/2017:09:41:41 +0200] "GET / HTTP/1.1" 429 7499 "https://example.org/" "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36" 1000
        127.0.0.1 - - [14/Jul/2017:09:41:43 +0200] "GET / HTTP/1.1" 499 845 "https://example.org/" "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36" 1000
    ''')
    self.assertEqual(len(state), 0)

  def test_non_skipped_status_still_processed(self):
    state = self._run(['--skip-status-code', '429'],
    b'''127.0.0.1 - - [14/Jul/2017:09:41:41 +0200] "GET / HTTP/1.1" 200 7499 "https://example.org/" "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36" 1000''')
    self.assertGreater(len(state), 0)

class TestSkipUserAgent(ApacheDEXTestCase):
  def _run(self, args, logline):
    with tempfile.NamedTemporaryFile() as fin, tempfile.NamedTemporaryFile() as fout:
      fin.write(logline)
      fin.flush()
      sys.argv = ['apachedex', '--base=/', fin.name, '--logformat', '%h %l %u %t "%r" %>s %O "%{Referer}i" "%{User-Agent}i" %{ms}T', '-f', 'json', '-o', fout.name] + args
      apachedex.main()
      with open(fout.name) as f:
        return json.load(f)

  def test_basic_skip_user_agent(self):
    state = self._run(['--skip-user-agent', 'Mozilla'],
    b'''127.0.0.1 - - [14/Jul/2017:09:41:41 +0200] "GET / HTTP/1.1" 429 7499 "https://example.org/" "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36" 1000''')
    self.assertEqual(len(state), 0)

  def test_multiple_skip_user_agent(self):
    state = self._run(['--skip-user-agent', 'Mozilla', '--skip-user-agent', 'Zabbix'],
    b'''127.0.0.1 - - [14/Jul/2017:09:41:41 +0200] "GET / HTTP/1.1" 429 7499 "https://example.org/" "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36" 1000
        127.0.0.1 - - [14/Jul/2017:09:41:43 +0200] "GET / HTTP/1.1" 499 845 "https://example.org/" "Zabbix" 1000
    ''')
    self.assertEqual(len(state), 0)

  def test_non_skipped_user_agent_still_processed(self):
    state = self._run(['--skip-user-agent', 'Zabbix'],
    b'''127.0.0.1 - - [14/Jul/2017:09:41:41 +0200] "GET / HTTP/1.1" 200 7499 "https://example.org/" "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36" 1000''')
    self.assertGreater(len(state), 0)

if __name__ == '__main__':
  unittest.main()
