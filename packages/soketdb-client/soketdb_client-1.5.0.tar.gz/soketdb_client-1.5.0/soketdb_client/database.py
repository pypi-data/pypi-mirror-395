import requests

class mydatabase:
  def __init__(self, host_url=None, key=None, backup=None, restore=None):
    self.host_url = host_url
    self.backup = backup
    self.restore = restore
  def execute(self, qurel=None):
    execute_url = f"{self.host_url}?qurel={qurel}"
    result = requests.get(execute_url)
    return result